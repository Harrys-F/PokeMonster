"""Targeted V3 form library; preserve all previous sources and room geometry.
Background Blender only. Save/reopen/review precedes separate FBX export.
"""
import bpy, bmesh, math, random, json, sys
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'Art/HealingHouse'
SOURCE = ART/'Source/HealingHouse_QualityV3.blend'
assert bpy.app.background and (not SOURCE.exists() or '--revise-owned-source' in sys.argv), 'Existing source must be preserved'
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene
s.name = 'HealingHouse_QualityV3'
s.unit_settings.system = 'METRIC'
s.unit_settings.scale_length = 1
bpy.context.preferences.filepaths.save_version = 0
rng = random.Random(10537)
colors = {'Wood':(.29,.145,.065),'Timber':(.105,.052,.025),
          'Stone':(.36,.32,.26),'Mortar':(.105,.08,.05),
          'Sage':(.18,.27,.13),'Linen':(.58,.53,.40),
          'Metal':(.048,.05,.036),'Gold':(.49,.32,.11),
          'Leaf':(.10,.23,.085),'LeafLight':(.22,.34,.12),
          'LeafDark':(.065,.14,.06),'Flower':(.57,.30,.24),
          'FlowerCream':(.75,.63,.36),'Ceramic':(.39,.23,.12),
          'Roof':(.56,.23,.11)}
mats = {}
for name,color in colors.items():
    m=bpy.data.materials.new('HH_Q3_'+name);m.use_nodes=True
    m.diffuse_color=(*color,1)
    bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=.83
    texture={'Wood':'Wood','Timber':'Wood','Stone':'Stone','Sage':'Cloth','Linen':'Cloth'}.get(name)
    file=(ART/'Textures/QualityV2'/('T_HH_Painted'+texture+'.png')) if texture else None
    if name=='Roof':file=ART/'Textures/QualityV3/T_HH_PaintedTerracotta.png'
    if file:
        t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(file),check_existing=True)
        mix=m.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
        mix.inputs[2].default_value=(.48,.42,.35,1) if name=='Timber' else (1,1,1,1)
        m.node_tree.links.new(t.outputs['Color'],mix.inputs[1]);m.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
    mats[name]=m

parts=[];catalog={};objects={};provenance={}
def add(o,key,bevel=0):
    o.data.materials.append(mats[key]);parts.append(o)
    if bevel:
        b=o.modifiers.new('Crafted edge','BEVEL');b.width=bevel;b.segments=3
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
    return o
def box(p,size,key='Wood',bevel=.012):
    bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return add(o,key,bevel)
def rod(a,b,r,key='Timber',vertices=12):
    a,b=Vector(a),Vector(b);delta=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=delta.length,location=(a+b)/2)
    o=bpy.context.object;o.rotation_euler=delta.to_track_quat('Z','Y').to_euler()
    for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
    return add(o,key)
def beam(a,b,width,key='Timber'):
    a,b=Vector(a),Vector(b);delta=b-a
    o=box((a+b)/2,(width,width,delta.length),key,.009)
    o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o
def ellipsoid(p,scale,key):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=p)
    o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for f in o.data.polygons:f.use_smooth=True
    return add(o,key)
def torus(p,r,t,key='Metal',rotation=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=24,minor_segments=6,major_radius=r,minor_radius=t,location=p,rotation=rotation)
    return add(bpy.context.object,key)
def raw(vertices,faces,key,indices=None):
    me=bpy.data.meshes.new('Crafted surface');me.from_pydata(vertices,[],faces);me.update()
    o=bpy.data.objects.new('Crafted surface',me);s.collection.objects.link(o);add(o,key)
    return o
def end(name,source='new reusable prop',collision='NoCollision',uv_scale=1):
    global parts
    assert parts,name
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.hide_set(False);o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=parts[0]
    o.name='HH_Q3_'+name;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-10],context='FACES')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
    uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
    for f in o.data.polygons:
        axis=max(range(3),key=lambda i:abs(f.normal[i]));a,b=((1,2),(0,2),(0,1))[axis]
        for li in f.loop_indices:
            c=o.data.vertices[o.data.loops[li].vertex_index].co
            uv.data[li].uv=(c[a]*uv_scale,c[b]*uv_scale)
    o.data.calc_loop_triangles();bpy.context.view_layer.update()
    c=[v.co for v in o.data.vertices];lo=[min(v[i] for v in c) for i in range(3)];hi=[max(v[i] for v in c) for i in range(3)]
    catalog[name]={'object':o.name,'size_cm':[round((b-a)*100,4) for a,b in zip(lo,hi)],
                   'bounds_min_cm':[v*100 for v in lo],'bounds_max_cm':[v*100 for v in hi],
                   'triangles':len(o.data.loop_triangles),'materials':[m.name for m in o.data.materials],
                   'source':source,'collision':collision,'units':'metres; FBX centimetre conversion'}
    objects[name]=o;parts=[];return o
def imported(source,name):
    with bpy.data.libraries.load(str(ART/'Source'/source),link=False) as (fr,to):
        assert name in fr.objects;to.objects=[name]
    o=to.objects[0];s.collection.objects.link(o);o.hide_set(False);o.hide_render=False
    # Source data is copied into this new file, never written back.
    o.location=(0,0,0);o.rotation_euler=(0,0,0);o.scale=(1,1,1)
    for i,m in enumerate(o.data.materials):
        key=m.name.split('_')[-1]
        if key in mats:o.data.materials[i]=mats[key]
    parts.append(o);return o
def islands(me):
    adjacency={v.index:set() for v in me.vertices}
    for e in me.edges:a,b=e.vertices;adjacency[a].add(b);adjacency[b].add(a)
    remaining=set(adjacency)
    while remaining:
        group={remaining.pop()};todo=list(group)
        while todo:
            for v in adjacency[todo.pop()]:
                if v in remaining:remaining.remove(v);group.add(v);todo.append(v)
        yield [me.vertices[i] for i in group]

# A single crafted reception carcass, continuous plinth and two intentional tops.
box((0,0,.12),(.80,3.35,.20),'Timber',.025)
for i in range(20):
    y=-1.595+i*.168;h=.76 if y>.84 else 1.01
    o=box((-.355,y,h/2+.02),(.075,.16,h-.09),'Wood',.009)
    for v in o.data.vertices:v.co.x+=.0018*math.sin(v.co.z*11+i)
box((.345,0,.40),(.07,3.34,.63),'Wood')
for y in (-1.62,-.78,.04,.85,1.62):
    h=.77 if y>1 else 1.02
    box((-.398,y,h/2),(.085,.095,h-.035),'Timber')
    for z in (.14,h-.12):box((-.442,y,z),(.020,.11,.046),'Gold',.004)
for center,width,h in [(-.425,2.55,1.05),(1.275,.85,.80)]:
    for j in range(4):
        box((-.345+j*.23,center,h-.038),(.227,width-.008,.076),'Wood',.014)
    box((-.436,center,.20),(.036,width-.06,.060),'Timber')
    box((-.436,center,h-.16),(.036,width-.06,.065),'Timber')
# Stepped joint and repeated framed panels visibly tie both heights together.
box((-.42,.85,.91),(.06,.08,.22),'Timber')
for y in (-1.18,-.38,.46):
    for z in (.34,.68):box((-.418,y,z),(.021,.54,.035),'Timber',.005)
    for dy in (-.27,.27):box((-.418,y+dy,.51),(.021,.035,.36),'Timber',.005)
box((-.457,-.38,.52),(.025,.50,.48),'Sage',.020)
beam((-.48,-.38,.33),(-.48,-.38,.70),.025,'Gold')
for z in (.40,.49,.58):
    for sign in (-1,1):beam((-.48,-.38,z),(-.48,-.38+sign*.15,z+.095),.018,'Gold')
end('CounterStepped','V2 dimensions/function retained; rebuilt continuous construction')

# Preserve shelf levels and the stock support planes; add crafted stiles/crown.
for name,original,width in [('Bookcase','HH_V3_Bookcase',1.17),('HerbShelf','HH_V3_HerbShelf',2.02)]:
    o=imported('HealingHouse_V3.blend',original)
    for group in islands(o.data):
        center=sum((v.co for v in group),Vector())/len(group)
        for v in group:v.co.x+=.002*math.sin(v.co.z*7+center.x*3)
    height=1.89 if name=='Bookcase' else 1.79
    for x in (-width/2+.045,width/2-.045):
        rod((x,-.246,.10),(x,-.246,height-.10),.018,'Timber')
        for z in (.15,height-.17):torus((x,-.246,z),.021,.006,'Gold')
    for j in range(5):
        x=-width*.45+j*width*.225
        box((x,-.17,height+.018+.035*math.cos(x/width*math.pi)),(width*.215,.09,.070),'Wood',.014)
    end(name,'retained V3 shelf geometry/support planes plus crown, stiles and small joints')

# Slatted seating with tapered legs, curved crest, pegged braces, existing cushions.
o=imported('HealingHouse_QualityV2.blend','HH_Q2_Bench')
for x in (-.55,.55):
    beam((x,-.28,.12),(x,.28,.39),.045,'Timber')
    ellipsoid((x,.345,.995),(.068,.07,.068),'Wood')
for i in range(7):
    x=-.58+i*.193;z=1.055-.095*(x/.65)**2
    box((x,.35,z),(.193,.065,.10),'Wood',.018)
end('Bench','retained V2 seat/cushions with crafted back crest and supports','retain original simple collision')

# Replace the tabletop slab by individual planks and turned/tapered leg profiles.
for j in range(4):box((0,-.258+j*.172,.714),(1.14,.168,.072),'Wood',.015)
for x in (-.43,.43):
    for y in (-.22,.22):
        for z,r in [(.12,.052),(.30,.038),(.43,.060),(.57,.045),(.69,.052)]:
            ellipsoid((x,y,z),(r,r,.080),'Timber')
        rod((x,y,.03),(x,y,.70),.036,'Timber')
        box((x,y,.04),(.105,.105,.06),'Wood',.009)
for y in (-.22,.22):beam((-.43,y,.22),(.43,y,.22),.054,'Timber')
for x in (-.43,.43):beam((x,-.22,.16),(x,.22,.16),.055,'Timber')
end('Table','V1 115x70 cm footprint / 75 cm top retained','retain original simple collision')

o=imported('HealingHouse_V3.blend','HH_V3_HerbTable')
for y in (-.275,.275):beam((-.48,y,.13),(.48,y,.13),.06,'Timber')
for x in (-.49,.49):box((x,-.303,.64),(.075,.045,.20),'Metal',.007)
end('HerbTable','V3 treatment table preserved; braces and discreet straps')
for name,L,W in [('TreatmentBedSmall',1.40,.82),('TreatmentBedLarge',1.80,1.05)]:
    o=imported('HealingHouse_V3.blend','HH_V3_'+name)
    for x in (-L/2+.09,L/2-.09):
        for y in (-W/2+.07,W/2-.07):
            rod((x,y,.20),(x,y,.58 if x>0 else .72),.04,'Timber')
            ellipsoid((x,y,.72 if x<0 else .58),(.055,.055,.055),'Wood')
    for y in (-W/2+.03,W/2-.03):box((0,y,.32),(L-.13,.09,.10),'Wood',.014)
    end(name,'V3 bed dimensions/supports retained; shaped end posts and frame')

# Leaves are curved broad surfaces with a raised midrib, never ellipsoid blobs.
def leaf(base,tip,width,key='Leaf',curl=.10):
    a,b=Vector(base),Vector(tip);d=b-a;side=d.cross(Vector((0,0,1)))
    if side.length<.01:side=Vector((1,0,0))
    side.normalize();normal=side.cross(d).normalized();vs=[];fs=[]
    for i in range(7):
        t=i/6;mid=a+d*t+normal*math.sin(t*math.pi)*curl
        span=width*math.sin(t*math.pi)**.8
        vs.extend([tuple(mid-side*span),tuple(mid+normal*.013*math.sin(t*math.pi)),tuple(mid+side*span)])
    for i in range(6):
        q=i*3
        for j in range(2):fs.append((q+j,q+j+1,q+j+4,q+j+3))
    o=raw(vs,fs,key)
    for f in o.data.polygons:f.use_smooth=True
    return o
def pot(radius=.18,height=.27):
    vs=[];fs=[];profile=[(0,.01),(.02,radius*.68),(height*.20,radius*.75),(height*.82,radius),(height,radius*1.08),(height,radius*.89),(height*.78,radius*.87),(height*.72,.01)]
    N=24
    for z,r in profile:
        for i in range(N):
            a=i*math.tau/N;vs.append((r*math.cos(a),r*math.sin(a),z))
    for j in range(len(profile)-1):
        for i in range(N):fs.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
    o=raw(vs,fs,'Ceramic')
    for f in o.data.polygons:f.use_smooth=True
    torus((0,0,height*.91),radius*1.015,.015,'Ceramic')
    return height
for family in ['BroadHerb','NarrowHerb','LeafPlant','FlowerPlant','TrailingHerb','HangingHerb','HerbBundle']:
    hanging=family in ('HangingHerb','HerbBundle');trailing=family in ('TrailingHerb','HangingHerb')
    z0=pot(.17,.25) if family!='HerbBundle' else .65
    count={'BroadHerb':9,'NarrowHerb':14,'LeafPlant':11,'FlowerPlant':8,'TrailingHerb':7,'HangingHerb':8,'HerbBundle':10}[family]
    for i in range(count):
        ang=i*2.399+rng.uniform(-.12,.12)
        if family=='HerbBundle':
            base=Vector((0,0,.63));tip=Vector((math.cos(ang)*.11,math.sin(ang)*.11,.08+rng.random()*.12))
        else:
            h=rng.uniform(.30,.58) if family!='NarrowHerb' else rng.uniform(.44,.69)
            radius=.19 if family=='LeafPlant' else .30
            tip=Vector((math.cos(ang)*radius,math.sin(ang)*radius,z0+h))
            if trailing:tip.z=z0-rng.uniform(.08,.38);tip.x*=1.7;tip.y*=1.7
            base=Vector((0,0,z0-.03))
        rod(base,tip,.006,'LeafDark',8)
        for t in (.38,.68):
            origin=base.lerp(tip,t)
            for sign in (-1,1):
                direction=Vector((math.cos(ang+sign*.72),math.sin(ang+sign*.72),.25))
                length=.22 if family!='NarrowHerb' else .28
                width=.075 if family in ('BroadHerb','LeafPlant') else .027
                if trailing:direction.z=-.30
                leaf(origin,origin+direction*length,width,'LeafLight' if i%3==0 else 'Leaf',.035)
        if family=='BroadHerb':leaf(base,tip,.085,'Leaf' if i%2 else 'LeafLight',.05)
        if family=='FlowerPlant' and i%2==0:
            for j in range(5):
                a=j*math.tau/5
                leaf(tip,tip+Vector((math.cos(a)*.065,math.sin(a)*.065,.018)),.025,'Flower',.012)
            ellipsoid(tip,(.019,.019,.018),'FlowerCream')
    if hanging and family!='HerbBundle':
        for a in (0,2.094,4.188):rod((.18*math.cos(a),.18*math.sin(a),.23),(0,0,.70),.009,'Gold')
        torus((0,0,.72),.045,.01,'Metal',rotation=(math.pi/2,0,0))
    if family=='HerbBundle':torus((0,0,.58),.045,.018,'Gold')
    end(family,'modular botanical family; curved leaves/midribs and hand-thrown pot' if family!='HerbBundle' else 'tied hanging herb bundle')

# Reusable carved planter/flowerbox, empty so botanical families stay independent.
for y in (-.19,.19):
    for i in range(8):box((-.51+i*.145,y,.13),(.14,.055,.24),'Wood',.008)
for x in (-.58,.58):box((x,0,.13),(.055,.40,.24),'Wood',.01)
box((0,0,.035),(1.18,.36,.055),'Timber')
for y in (-.212,.212):box((0,y,.22),(1.25,.03,.06),'Timber',.01)
for x in (-.43,.43):box((x,-.23,.12),(.045,.025,.22),'Metal',.004)
end('WindowPlanter','reusable 125 cm window box; ornamental, not a blocker')

# Existing leaf/protective-ring emblem, now surrounded by a carved timber rim.
o=imported('HealingHouse_V3.blend','HH_V3_GuardianSign')
for y in (-.355,.355):box((-.715,y,-.49),(.045,.035,.80),'Wood',.01)
for z in (-.89,-.09):box((-.715,0,z),(.045,.70,.045),'Wood',.01)
for y in (-.28,.28):
    for z in (-.83,-.15):ellipsoid((-.752,y,z),(.013,.015,.015),'Metal')
end('GuardianSign','existing V3 protective ring/leaves/toe marks; carved frame and rivets')
for a in [(-.14,0,.52),(.14,0,.52)]:
    rod(a,(0,0,.68),.013,'Metal')
torus((0,0,.70),.044,.01,'Metal',rotation=(math.pi/2,0,0))
beam((0,0,.52),(0,.24,.40),.035,'Metal')
end('LanternHook','reusable wrought-iron hanger with visible mounting')

# Add low overlapping roof courses instead of thousands of separate shingles.
def roof_courses(name):
    o=imported('HealingHouse_V3.blend','HH_V2_'+name)
    # Read the largest near-rectangular upward roof faces from the real source.
    panels=[f for f in o.data.polygons if f.area>.28 and abs(f.normal.z)>.20 and len(f.vertices)==4]
    for panel in panels:
        corners=[o.data.vertices[i].co.copy() for i in panel.vertices]
        if sum(c.z for c in corners)/4<2:continue
        if panel.normal.z<0:continue
        pairs=sorted([( (corners[j]-corners[i]).length,i,j) for i in range(4) for j in range(i+1,4)],reverse=True)
        # Roof panels are parallelograms; choose the long horizontal edge.
        horiz=[(i,(corners[(i+1)%4]-corners[i]).length) for i in range(4) if abs(corners[(i+1)%4].z-corners[i].z)<.10]
        if not horiz:continue
        index=max(horiz,key=lambda x:x[1])[0]
        a=corners[index];b=corners[(index+1)%4];c=corners[(index+2)%4];d=corners[(index+3)%4]
        if a.z>d.z:a,d=d,a;b,c=c,b
        across=b-a;slope=d-a;rows=max(4,round(slope.length/.39));columns=max(3,round(across.length/.38));normal=panel.normal.normalized()
        for row in range(rows):
            low=row/rows;high=min(1,(row+1.22)/rows);vs=[];fs=[]
            for col in range(columns*2+1):
                u=col/(columns*2);scallop=.025*math.sin(u*columns*math.tau)**2
                lowco=a+across*u+slope*(low+scallop/slope.length)
                highco=a+across*u+slope*high
                lift=.018+.004*math.sin(col*2.37+row)
                vs.extend([tuple(lowco+normal*lift),tuple(highco+normal*.010)])
            for col in range(columns*2):
                q=col*2;fs.append((q,q+2,q+3,q+1))
            raw(vs,fs,'Roof')
            # The course lip casts a small contact shadow and breaks roof edges.
            for col in range(columns):
                u=(col+.08)/columns
                aa=a+across*u+slope*low+normal*.020
                bb=aa+slope*(high-low)*.60
                side=across.normalized()*.0045
                raw([tuple(aa-side),tuple(aa+side),tuple(bb+side),tuple(bb-side)],[(0,1,2,3)],'Timber')
    end(name,'retained roof substrate plus continuous scalloped overlapping courses',uv_scale=.9)
for name in ['Roof_Main','Roof_Porch','Roof_Entry']:roof_courses(name)

# Preserve architecture openings/origins; only shallow surface/edge variation.
for name in ['Roof_Trim','Timber_Front','Timber_CameraSide','Timber_Far','Timber_Entry',
             'Stone_Front','Stone_CameraSide','Stone_Far','Chimney','Windows_Front',
             'Windows_CameraSide','Windows_Far','DoorFrame']:
    o=imported('HealingHouse_V3.blend','HH_V2_'+name)
    for group in islands(o.data):
        center=sum((v.co for v in group),Vector())/len(group)
        fac=rng.uniform(.985,1.015) if name.startswith('Stone') else 1
        for v in group:
            if name.startswith('Stone'):v.co=center+(v.co-center)*fac
            if name not in ('DoorFrame',):
                v.co+=Vector((.002*math.sin(v.co.z*5+center.y),.003*math.sin(v.co.x*3+center.z),.002*math.sin(v.co.y*4)))
    # Shallow pegged joints / window trim; door clear aperture unchanged.
    if name=='DoorFrame':
        for side in (-1,1):
            for z in (.35,1.70):box((-4.77,side*.91,z),(.035,.07,.12),'Metal',.008)
    if name=='Chimney':
        # Existing stack gets staggered, beveled masonry rather than seven blocks.
        co=[v.co for v in o.data.vertices];xmin=min(v.x for v in co);xmax=max(v.x for v in co);ymin=min(v.y for v in co);ymax=max(v.y for v in co);zmin=min(v.z for v in co);zmax=max(v.z for v in co)
        for row in range(15):
            z=zmin+(zmax-zmin)*(row+.5)/15
            for j in range(3):
                yy=ymin+(ymax-ymin)*(j+.5)/3
                box((xmin-.009,yy,z),(.075,(ymax-ymin)/3-.022,(zmax-zmin)/15-.020),'Stone',.025)
                xx=xmin+(xmax-xmin)*(j+.5)/3
                box((xx,ymin-.009,z),((xmax-xmin)/3-.022,.075,(zmax-zmin)/15-.020),'Stone',.025)
    end(name,'V3 architectural module; retained openings/size/origin, crafted surface details')

# One export object per modular asset, review linked copies in a separate scene.
preview=bpy.data.scenes.new('Quality V3 Review')
world=bpy.data.worlds.new('Soft neutral studio');world.use_nodes=True
world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.65;preview.world=world
for i,(name,o) in enumerate(objects.items()):
    p=o.copy();p.data=o.data;preview.collection.objects.link(p)
    lo=Vector(catalog[name]['bounds_min_cm'])/100;hi=Vector(catalog[name]['bounds_max_cm'])/100
    p.location=Vector(((i%5)*4,(i//5)*3.1,0))-(lo+hi)/2;p.location.z-=lo.z-(lo.z+hi.z)/2
    if name.startswith(('Roof','Timber_','Stone_','Windows_','Chimney','Door')):p.scale=(.24,.24,.24);p.location=Vector(((i%5)*4,(i//5)*3.1,0))-(lo+hi)/2*.24;p.location.z=-lo.z*.24
bpy.context.window.scene=preview
bpy.ops.object.light_add(type='AREA',location=(8,-5,17));bpy.context.object.data.energy=2600;bpy.context.object.data.size=11
bpy.ops.object.camera_add(location=(26,-26,31));cam=bpy.context.object
cam.rotation_euler=(Vector((8,10,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=29;preview.camera=cam
preview.render.engine='CYCLES';preview.cycles.samples=16
preview.render.resolution_x=1800;preview.render.resolution_y=1600;preview.render.resolution_percentage=100
for image in bpy.data.images:
    if image.source=='FILE':image.pack()
(ART/'QualityV3/Props.json').write_text(json.dumps(catalog,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
print('QUALITY_V3_SOURCE_SAVED',len(catalog),'assets',str(SOURCE))
