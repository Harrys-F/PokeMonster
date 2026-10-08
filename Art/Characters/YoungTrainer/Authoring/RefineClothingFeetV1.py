"""Clothing/scarf/barefoot form pass from immutable V6, static modelling only.

Run once in live Blender with saved V6 open. All original objects and materials
remain intact, and only a new .blend may be saved. No face, body, pack or rig edits.
"""
import bpy,bmesh,math,json
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath)==R/'Source/YoungTrainer_HeadForm_V6.blend'
assert not bpy.data.is_dirty
assert 'YTCF_Player' not in bpy.data.collections
assert not (R/'Source/YoungTrainer_ClothingFeet_V1.blend').exists()
s=bpy.context.scene
C=bpy.data.collections.new('YTCF_Player');s.collection.children.link(C)
old=bpy.data.collections['YT6_Player'];copies={}
for o in old.objects:
    if o.name=='YT6_ScarfWrappedVolume':continue
    n=o.copy()
    if o.data:n.data=o.data.copy()
    n.name=o.name.replace('YT6_','YTCF_',1);C.objects.link(n);copies[o]=n
    n['source_v6_object']=o.name;n.hide_render=False;n.hide_set(False)
for o,n in copies.items():n.parent=copies.get(o.parent,o.parent)
root=bpy.data.objects['YTCF_PlayerRoot'];root['scope']='Clothing/scarf/bare feet only; V6 head frozen'

def smooth(a,b,x):
    t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)

def gauss(x,c,w):return math.exp(-((x-c)/w)**2)

def components(o):
    bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();seen=set();rows=[]
    for v in bm.verts:
        if v.index in seen:continue
        stack=[v];seen.add(v.index);ids=[]
        while stack:
            cur=stack.pop();ids.append(cur.index)
            for e in cur.link_edges:
                n=e.other_vert(cur)
                if n.index not in seen:seen.add(n.index);stack.append(n)
        rows.append((ids,sum((bm.verts[i].co for i in ids),Vector())/len(ids)))
    bm.free();return rows

# Open vest: reduce excessive lower coat flare while retaining long curved tips.
def vest_map(p):
    x,y,z=p;lower=1-smooth(.47,.74,z)
    x*=1-.13*lower
    if y<0:y+=.026*lower*smooth(.02,.12,-y)
    z+=.066*lower
    z+=.004*math.sin(x*21+.4)*lower
    y-=.0035*gauss(z,.84,.13)*math.sin(x*21+.7)
    return Vector((x,y,z))
vest=bpy.data.objects['YTCF_Vest']
for v in vest.data.vertices:v.co=vest_map(v.co)

shirt=bpy.data.objects['YTCF_Shirt']
source=[v.co.copy() for v in shirt.data.vertices]
# Torso/button/collar coordinates follow the same loose shirt shell.
def torso_map(p):
    x,y,z=p;low=1-smooth(.51,.73,z)
    z+=.080*low
    z+=.005*math.sin(x*23+.6)*low
    z+=.024*gauss(x,0.,.055)*low*smooth(.025,.085,-y)
    belly=gauss(z,.82,.13)
    x*=1+.035*belly;y*=1+.045*belly
    y-=.003*gauss(x,.025,.075)*gauss(z,.76,.11)
    return Vector((x,y,z))
for v in shirt.data.vertices:
    i=v.index;p=source[i]
    if i<258 or 586<=i<818:
        v.co=torso_map(p)
    elif 258<=i<360 or 422<=i<524:
        # Existing sleeve rings remain in place along the preserved A-pose arms.
        side=1 if p.x>0 else -1;t=max(0.,min(1.,(.983-p.z)/.26))
        cx=side*(.128+.057*t);cy=.004+.005*math.sin(t*math.pi)
        dx=p.x-cx;dy=p.y-cy;a=math.atan2(dx*side,dy)
        bulk=math.sin(math.pi*t)**.8
        wrinkle=.005*gauss(t,.78,.20)*math.cos(3*a+side*.8+t*3)
        v.co.x=cx+dx*(1+.12*bulk)+side*wrinkle*.6
        v.co.y=cy+dy*(1+.15*bulk)+wrinkle
        v.co.z=p.z+.003*math.sin(2*a+side)*gauss(t,.80,.20)
    elif i>=818:
        # Soften separate shoulder blend pieces without moving the underlying body.
        side=1 if p.x>0 else -1;cx=side*.1506
        v.co.x=cx+(p.x-cx)*.96
        v.co.y=.005+(p.y-.005)*1.025
# Remove only redundant old cuff shells from this new shirt copy; V6 stays intact.
bm=bmesh.new();bm.from_mesh(shirt.data);bm.verts.ensure_lookup_table()
bmesh.ops.delete(bm,geom=[v for v in bm.verts if 360<=v.index<422 or 524<=v.index<586],context='VERTS')
bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=1,use_grid_fill=True)
bm.to_mesh(shirt.data);bm.free()
shirt['v1_change']='Loose torso, rounded sleeve bulk/gathers; redundant source cuffs archived, only rolled cuffs visible'
# Both visible rolled cuffs: less toroidal symmetry, broad irregular rolled cloth.
for side,label in [(1,'R'),(-1,'L')]:
    o=bpy.data.objects['YTCF_RolledCuff_'+label];c=Vector((side*.190,-.002,.714))
    for v in o.data.vertices:
        p=v.co-c;a=math.atan2(p.y,p.x*side)
        p.x*=.94+.025*math.cos(3*a+side*.6)
        p.y*=.97+.025*math.sin(2*a+side)
        p.z+=.0025*math.sin(2*a+side*.7)
        v.co=c+p

pants=bpy.data.objects['YTCF_Pants']
# Connected source islands supply a stable left/right identity, including patches.
for ids,center in components(pants):
    side=1 if center.x>0 else -1
    for i in ids:
        v=pants.data.vertices[i];x,y,z=v.co
        cx=side*(.125-.043*smooth(.42,.71,z));dx=x-cx
        angle=math.atan2(dx*side,-y-.002)
        mid=gauss(z,.365,.145)
        radial=1+mid*(.035+.025*math.sin(2*angle+side*.75))
        depth=0.
        # Diagonal folds confined to the cloth panels, not uniform horizontal rings.
        for height,shift,width,amp in [(.265,.029,.017,.009),(.355,-.034,.022,.008),(.445,.025,.024,.005)]:
            bend=height+shift*math.sin(angle+side*.70)+(0.004 if side>0 else -.003)
            front=.42+.58*max(0,math.cos(angle))
            depth-=amp*gauss(z,bend,width)*front
            depth+=amp*.32*gauss(z,bend+.025,width*1.35)*front
        rr=math.hypot(dx,y)
        if rr>.035:
            x=cx+dx*radial+dx/rr*depth
            y=y*radial+y/rr*depth
        x+=side*(.004 if side>0 else -.002)*mid
        y+=(.004 if side<0 else -.003)*mid
        z+=.003*math.sin(angle+side*.6)*gauss(z,.31,.10)
        v.co=(x,y,z)
pants['v1_change']='Broad asymmetrical diagonal drape; fuller knee/thigh panels, narrow cropped cuffs preserved'

# Pouches: bring both closer to hip/belt, keep different dimensions and heights.
pouches=bpy.data.objects['YTCF_Pouches']
for v in pouches.data.vertices:
    x,y,z=v.co;side=1 if x>0 else -1
    cx=side*.175;cy=-.073 if side<0 else -.058;cz=.617 if side<0 else .640
    factor=.89 if side<0 else .95
    nx=side*(.158 if side<0 else .157)+(x-cx)*factor
    ny=cy+(y-cy)*.92+.006
    nz=cz+(z-cz)*factor+(.034 if side<0 else .025)
    # A slight lean replaces the two nearly upright boxes; no extra details.
    nx+=side*.045*(nz-cz-.025)
    v.co=(nx,ny,nz)
belt=bpy.data.objects['YTCF_DiagonalWaistBelt']
for v in belt.data.vertices:
    x,y,z=v.co
    v.co.z=z+.006*(x/.169)+.002*math.sin(math.atan2(x,-y)+.4)
    v.co.y=y+.002*gauss(x,-.05,.10)*smooth(.02,.10,-y)
# Buckle stays at the centre and the pendant remains exactly unchanged.

# Existing five-toed barefoot volumes: modest shortening, broad forefoot, toe hierarchy.
feet={}
for side,label,oldangle,newangle in [(1,'R',10,9),(-1,'L',-28,-21)]:
    o=bpy.data.objects['YTCF_BareFoot_'+label]
    ca=math.cos(math.radians(oldangle));sa=math.sin(math.radians(oldangle))
    cb=math.cos(math.radians(newangle));sb=math.sin(math.radians(newangle))
    max_displacement=0.
    for v in o.data.vertices:
        before=v.co.copy();px=v.co.x-side*.131;py=v.co.y;z=v.co.z
        x=(px*ca+py*sa)*side;y=-px*sa+py*ca
        foot=1-smooth(.100,.165,z)
        fore=gauss(y,-.115,.065)*foot
        x*=1+.045*fore
        y=.014+(y-.014)*(1-.055*foot)
        # Medial big toe gets a mild pad increase, lesser toes remain distinct.
        big=gauss(x,-.044,.022)*gauss(y,-.169,.036)*foot
        y-=.0008*big
        z-=.0045*big*smooth(.025,.046,z)
        # Raise only the inner arch; retain heel/ball/forefoot ground contact.
        arch=gauss(y,-.024,.043)*(1-smooth(-.006,.020,x))*(1-smooth(.030,.060,z))
        z+=.0033*arch
        # Subtle toe dorsal flattening, no sole slab or shoe-like outline.
        toes=gauss(y,-.177,.031)
        z-=.0022*toes*smooth(.031,.053,z)
        lesser=gauss(x,-.007,.019)+.65*gauss(x,.020,.017)
        y+=.0018*lesser*toes
        x*=side
        v.co=(side*.131+x*cb-y*sb,x*sb+y*cb,z)
        max_displacement=max(max_displacement,(v.co-before).length)
    # Preserve exact common ground after the local arch deformation.
    ground=min(v.co.z for v in o.data.vertices)
    for v in o.data.vertices:v.co.z-=ground
    o['barefoot']=True;o['toe_count']=5;o['sole_z']=0.
    o['v1_change']='Refined existing five-toed connected volume; broad ball, larger medial toe, heel and medial arch; no footwear'
    feet[label]={'source_outturn_deg':oldangle,'outturn_deg':newangle,'max_local_displacement_cm':max_displacement*100}

# New low-density closed cloth forms reuse existing red preview materials.
M={k:bpy.data.materials['YT4_Preview_Scarf'] for k in ['Scarf','ScarfLight','ScarfDeep']}
def mesh(name,vs,fs,mat,level=1):
    d=bpy.data.meshes.new('YTCF_'+name);d.from_pydata(vs,[],fs);d.update()
    bm=bmesh.new();bm.from_mesh(d);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(d);bm.free()
    o=bpy.data.objects.new('YTCF_'+name,d);C.objects.link(o);o.parent=root
    d.materials.append(M[mat])
    for p in d.polygons:p.use_smooth=True
    mod=o.modifiers.new('Soft broad cloth preview','SUBSURF');mod.levels=level;mod.render_levels=level
    o['purpose']='Broad scarf form; no fine seams, textures or rig'
    return o
for layer in range(3):
    N=96;B=16;vs=[];fs=[]
    for i in range(N):
        a=math.tau*i/N;front=max(0,math.cos(a))
        rx=.070+layer*.013+.0035*math.sin(3*a+layer*.7)
        ry=.073+layer*.016+.0045*math.sin(2*a+layer*.9)
        cz=1.035-layer*.022-(.016+layer*.009)*front+.012*math.sin(a+layer*.85)+.0035*math.sin(3*a+layer)
        for j in range(B):
            b=math.tau*j/B;radial=.0085*math.cos(b)+.0028*math.sin(b)*math.sin(2*a+layer*.8)
            z=cz+(.018+.003*math.sin(a+layer))*math.sin(b)+.003*math.sin(2*a+layer)*math.sin(b)**2+.0018*math.cos(3*b)*math.sin(3*a+layer*.5)
            vs.append(((rx+radial)*math.sin(a),.005-(ry+radial)*math.cos(a),z))
    for i in range(N):
        for j in range(B):fs.append((i*B+j,((i+1)%N)*B+j,((i+1)%N)*B+(j+1)%B,i*B+(j+1)%B))
    mesh('ScarfWrap_'+str(layer+1),vs,fs,['ScarfLight','Scarf','ScarfDeep'][layer],2)

def ribbon(name,centers,widths,mat):
    N=len(centers);B=12;vs=[];fs=[];stride=2*(B+1)
    for i,(x,y,z) in enumerate(centers):
        for face in [0,1]:
            for j in range(B+1):
                u=-1+2*j/B
                zz=z-.006*u*u+.0028*math.cos(u*math.pi*2+i*.33)
                yy=y+(face-.5)*.007+.0045*math.cos(u*math.pi)+.002*math.sin(u*4+i*.8)
                vs.append((x+u*widths[i],yy,zz))
    for i in range(N-1):
        for q in [0,1]:
            for j in range(B):
                a=i*stride+q*(B+1)+j;fs.append((a,a+1,a+stride+1,a+stride))
        for j in [0,B]:
            a=i*stride+j;fs.append((a,a+B+1,a+stride+B+1,a+stride))
    for i in [0,N-1]:
        for j in range(B):
            a=i*stride+j;fs.append((a,a+1,a+B+2,a+B+1))
    return mesh(name,vs,fs,mat,2)
# Controlled asymmetric drapes, with rounded hems rather than rigid triangles.
ribbon('ScarfFrontDrape',[(-.027,-.117,1.013),(-.020,-.126,1.001),(-.013,-.133,.987),(-.003,-.140,.972),(.008,-.143,.957),(.019,-.144,.943),(.023,-.141,.930),(.016,-.133,.919)],[.073,.077,.075,.067,.058,.047,.038,.031],'Scarf')
ribbon('ScarfOverlapFold',[(-.046,-.133,.994),(-.036,-.143,.984),(-.021,-.151,.972),(-.003,-.155,.960),(.010,-.154,.950),(.017,-.148,.944)],[.043,.048,.047,.040,.027,.018],'ScarfLight')
ribbon('ScarfSideTail',[(.060,-.046,1.023),(.086,-.065,1.008),(.112,-.082,.988),(.136,-.088,.965),(.153,-.092,.941),(.155,-.104,.919),(.152,-.115,.897),(.157,-.116,.875),(.173,-.109,.856)],[.030,.034,.035,.036,.034,.032,.029,.025,.019],'Scarf')
for o in C.objects:
    if o.type=='MESH':o.data.update()
old.hide_render=True;old.hide_viewport=True
cam=s.camera.copy();cam.data=s.camera.data.copy();cam.name='YTCF_FormReview';s.collection.objects.link(cam);s.camera=cam
bpy.ops.object.select_all(action='DESELECT');vest.select_set(True);bpy.context.view_layer.objects.active=vest
bpy.context.view_layer.update()
meta={'version':'ClothingFeet V1','source':'Source/YoungTrainer_HeadForm_V6.blend','output':'Source/YoungTrainer_ClothingFeet_V1.blend','height_m':1.4,'frozen':['V6 head/face/hair/eyes/ears','body and hands','backpack and bedroll','pendant','rig/weights/actions of originals','all existing material datablocks and files'],'changed':['shirt','vest','pants','rolled cuffs','pouches','waist belt','bare feet'],'new_scarf_forms':6,'feet':feet,'no_unreal_export':True,'no_new_final_uv_or_texture':True,'camera_note':'Fixed elevated Blender form review, not Unreal PIE'}
(R/'CLOTHING_FEET_V1.json').write_text(json.dumps(meta,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/YoungTrainer_ClothingFeet_V1.blend'))
print('CLOTHING_FEET_V1_SAVED',len(C.objects),'objects. Head/backpack/body/pendant unchanged.')
