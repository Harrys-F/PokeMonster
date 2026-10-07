"""Head-only form pass from preserved V4. No material, UV, rig or body edits.

Run in the live Blender after opening Stage 09. Re-running requires reopening
that stage first, so iterations never accumulate deformation.
"""
import bpy, bmesh, math
from pathlib import Path
from mathutils import Vector

R = Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name in ['09_BeforeHeadFormV5_20261007.blend', 'YoungTrainer_BarefootReference_V4.blend']
assert 'YT5_Player' not in bpy.data.collections
s = bpy.context.scene
C = bpy.data.collections.new('YT5_Player')
s.collection.children.link(C)
root = bpy.data.objects.new('YT5_PlayerRoot', None)
C.objects.link(root)
root['height_m'] = 1.4
root['scope'] = 'Head, face and hair only; static modelling version'
old = bpy.data.collections['YT4_Player']
hair_parts = ('Hair', 'ForeheadGroup', 'OutlineCurl', 'CrownSweep')
for o in old.objects:
    if o.type != 'MESH' or o.name.removeprefix('YT4_').startswith(hair_parts):
        continue
    n = o.copy()
    n.data = o.data.copy()
    n.name = o.name.replace('YT4_', 'YT5_', 1)
    C.objects.link(n)
    n.parent = root
    n.hide_render = False
    n.hide_set(False)
    n['source_v4_object'] = o.name

def gauss(x, z, cx, cz, wx, wz):
    return math.exp(-((x-cx)/wx)**2-((z-cz)/wz)**2)

h = bpy.data.objects['YT5_Head']
# Broad soft cheek planes and a narrower, readable chin; preserve eye/mouth loops.
for v in h.data.vertices:
    x, y, z = v.co
    front = max(0.0, min(1.0, (-y-.012)/.07))
    cheek = gauss(abs(x), z, .066, 1.100, .052, .052)*front
    v.co.x *= 1 + .035*cheek - .11*gauss(x, z, 0, 1.036, .075, .026)*front
    v.co.y -= .005*cheek
    # Remove the broad spherical nose bump, retain a small forward tip.
    v.co.y += .004*gauss(x,z,0,1.113,.030,.027)*front
    v.co.y -= .003*gauss(x,z,0,1.119,.013,.013)*front
    v.co.z += .0018*gauss(x,z,0,1.038,.050,.022)*front

def interp(z, rows):
    # Monotonic cubic Hermite profile: no horizontal ridges at row boundaries.
    xs=[r[0] for r in rows];ys=[r[1] for r in rows]
    if z<=xs[0]:return ys[0]
    if z>=xs[-1]:return ys[-1]
    ds=[(ys[i+1]-ys[i])/(xs[i+1]-xs[i]) for i in range(len(xs)-1)]
    slopes=[ds[0]]
    for i in range(1,len(xs)-1):
        if ds[i-1]*ds[i]<=0:slopes.append(0)
        else:
            w1=2*(xs[i+1]-xs[i])+(xs[i]-xs[i-1]);w2=(xs[i+1]-xs[i])+2*(xs[i]-xs[i-1])
            slopes.append((w1+w2)/(w1/ds[i-1]+w2/ds[i]))
    slopes.append(ds[-1])
    for i in range(len(xs)-1):
        if xs[i]<=z<=xs[i+1]:
            h=xs[i+1]-xs[i];t=(z-xs[i])/h
            return (2*t**3-3*t**2+1)*ys[i]+(t**3-2*t*t+t)*h*slopes[i]+(-2*t**3+3*t*t)*ys[i+1]+(t**3-t*t)*h*slopes[i+1]


def facial_surface(x,z):
    rx=interp(z,[(1.029,.021),(1.050,.073),(1.080,.104),(1.110,.124),(1.170,.142),(1.220,.131),(1.260,.113),(1.307,.025)])
    ry=interp(z,[(1.029,.036),(1.050,.068),(1.080,.090),(1.110,.104),(1.170,.110),(1.220,.107),(1.260,.085),(1.307,.028)])
    y=.006-ry*math.sqrt(max(.015,1-(min(.999,abs(x)/rx))**2.5))
    # Continuous cheek plane, and a small readable nose rather than a socket dent.
    y-=.002*gauss(abs(x),z,.067,1.107,.040,.031)
    y-=.009*gauss(x,z,0,1.121,.014,.013)
    return y

for v in h.data.vertices:
    if v.co.y<-.015 and v.co.z<1.27:
        blend=min(1,max(0,(-v.co.y-.015)/.030))
        blend=blend*blend*(3-2*blend)
        v.co.y=v.co.y*(1-blend)+facial_surface(v.co.x,v.co.z)*blend

# Flatten the eye assembly into the facial surface, with almond-shaped corners.
def eye_xy(p, iris=False):
    x,y,z=p
    cx=.052337 if x>0 else -.052337
    dx=x-cx
    u=min(1, abs(dx)/.030)
    x=cx+dx*(1.16 if not iris else .94)
    dz=z-1.156
    z=1.156+dz*(.88-.15*u*u if not iris else .91)
    # Outer corner rises mildly; inner corner softens instead of a round rim.
    z+=.002*(dx*(1 if cx>0 else -1)/.032)
    return x,z

for v in h.data.vertices:
    names={h.vertex_groups[g.group].name for g in v.groups}
    if names & {'Topology_EyeR','Topology_EyeL'}:
        x,z=eye_xy(v.co)
        v.co.x=x;v.co.z=z
        # Keep the supporting loops following the face, not a raised socket.
        v.co.y=facial_surface(x,z)

for o in C.objects:
    part=o.name.removeprefix('YT5_')
    if not any(t in part for t in ['EyeWhite','Iris','Pupil','Glint','Lid']):
        continue
    iris=any(t in part for t in ['Iris','Pupil','Glint'])
    offset = {'EyeWhite': .0010, 'Iris': .0016, 'IrisWarm': .0018,
              'Pupil': .0020, 'EyeGlint': .0025, 'EyeGlintSmall': .0026,
              'UpperLid': .0018, 'LowerLid': .0003}
    key=part.rsplit('_',1)[0]
    for v in o.data.vertices:
        x,z=eye_xy(v.co,iris)
        cx=.052337 if x>0 else -.052337
        r=min(1, ((x-cx)/.0315)**2+((z-1.156)/.0345)**2)
        # Curved facial tangent and only 1.2 mm of eye convexity.
        y=facial_surface(x,z) - offset[key] -.0012*(1-r)
        if 'LowerLid' in part:
            z=1.156+(z-1.156)*.96
        v.co=(x,y,z)

# Eyebrows follow the broad orbital plane with a mild friendly inner lift.
for side in ['R','L']:
    o=bpy.data.objects['YT5_Brow_'+side]
    for v in o.data.vertices:
        x,y,z=v.co
        v.co.y=facial_surface(x,z)-.002
        v.co.z-=.002
        v.co.z+=.002*max(0,1-abs(x)/.09)
    # Shape change only: existing simple preview material stays unchanged.

for o in [bpy.data.objects['YT5_MouthLine'],bpy.data.objects['YT5_MouthCavity']]:
    for v in o.data.vertices:
        v.co.x*=1.25
        if 'Cavity' in o.name:v.co.z=1.078+(v.co.z-1.078)*.45
        v.co.z+=.0012*(abs(v.co.x)/.025)**2
        v.co.y=facial_surface(v.co.x,v.co.z)-(.0015 if 'Line' in o.name else .0003)
for v in h.data.vertices:
    if any(h.vertex_groups[g.group].name=='Topology_Mouth' for g in v.groups):
        v.co.x*=1.25
        v.co.z+=.0012*(abs(v.co.x)/.025)**2
        v.co.y=facial_surface(v.co.x,v.co.z)

# The single connected hair envelope supports broad directional flows.
M=bpy.data.materials['YT4_Preview_Hair']
def mesh(name,vs,fs):
    d=bpy.data.meshes.new('YT5_'+name);d.from_pydata(vs,[],fs);d.update()
    bm=bmesh.new();bm.from_mesh(d);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(d);bm.free()
    o=bpy.data.objects.new('YT5_'+name,d);C.objects.link(o);o.parent=root
    d.materials.append(M)
    for p in d.polygons:p.use_smooth=True
    return o

N=144;K=64;vs=[(0,.018,1.387)];fs=[]
flows=[(-.90,.8,.013,.40,.38),(.45,.65,.008,.50,.40),
       (-1.5,1.25,.014,.42,.40),(1.4,1.1,.012,.48,.34),
       (2.4,.7,.014,.42,.4),(-2.6,1.2,.013,.44,.38),
       (3.1,1.7,.015,.5,.35),(-2,2,.012,.4,.38),
       (1.9,1.9,.014,.44,.32)]
for j in range(1,K+1):
    for k in range(N):
        a=math.tau*k/N;t=j/K
        front=max(0,math.cos(a));back=max(0,-math.cos(a))
        end=2.27-.43*front+.26*back+.07*math.sin(3*a+.5)
        phi=end*t
        push=0
        for aa,pp,amp,wa,wp in flows:
            da=(a-aa+.30*math.sin(phi*2)+math.pi)%math.tau-math.pi
            push+=amp*math.exp(-(da/wa)**2-((phi-pp)/wp)**2)
        x=(.164+push)*math.sin(a)*math.sin(phi)
        y=.020-(.145+push)*math.cos(a)*math.sin(phi)
        z=1.242+(.145+push*.30)*math.cos(phi)
        z-=.024*back*max(0,(phi-1.85)/.60)
        if phi>1.45 and front>0:
            y+=.032*front*max(0,min(1,(phi-1.45)/.35))
            z+=.022*front*max(0,min(1,(phi-1.45)/.35))
        vs.append((x,y,z))
for k in range(N):fs.append((0,1+k,1+(k+1)%N))
for j in range(K-1):
    for k in range(N):
        a=1+j*N+k;b=1+j*N+(k+1)%N
        fs.append((a,b,b+N,a+N))
end=len(vs);vs.append((0,.025,1.105))
for k in range(N):fs.append((end,1+(K-1)*N+(k+1)%N,1+(K-1)*N+k))
env=mesh('HairFlowVolume',vs,fs)
mod=env.modifiers.new('Continuous volume preview','SUBSURF');mod.levels=1;mod.render_levels=1

def catmull(points,steps=10):
    ps=[Vector(p) for p in points];out=[]
    for i in range(len(ps)-1):
        a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(len(ps)-1,i+2)]
        for j in range(steps):
            t=j/steps
            out.append((2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)*.5)
    return out+[ps[-1]]

def lock(name,points,width,depth):
    ps=catmull(points);vs=[];fs=[];B=16;previous_n=None;previous_t=None
    # An elliptical swept volume, with buried broad roots and tapered hooked tips.
    # This avoids the two flat surfaces / thick leaf edge of the earlier pads.
    for i,p in enumerate(ps):
        t=i/(len(ps)-1)
        tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized()
        if previous_n is None:
            n=p-Vector((0,.020,1.24));n.normalize()
            n=(n-tangent*n.dot(tangent)).normalized()
        else:
            n=previous_t.rotation_difference(tangent)@previous_n
            n=(n-tangent*n.dot(tangent)).normalized()
        previous_n=n;previous_t=tangent
        lateral=tangent.cross(n).normalized()
        w=width*(.75+.40*math.sin(math.pi*t))*(1-t**2.1)
        w=max(.0006,w)
        d=depth*(.65+.35*math.sin(math.pi*t))*(1-t**1.5)
        d=max(.0005,d)
        for b in range(B):
            angle=math.tau*b/B
            # Soft asymmetric crest follows the curl, without extra thin strands.
            q=p+lateral*w*math.cos(angle)+n*d*math.sin(angle)
            vs.append(tuple(q))
    for i in range(len(ps)-1):
        for b in range(B):
            a=i*B+b;c=i*B+(b+1)%B;fs.append((a,c,c+B,a+B))
    vs.append(tuple(ps[0]));v0=len(vs)-1
    vs.append(tuple(ps[-1]));v1=len(vs)-1
    for b in range(B):
        fs.append((v0,(b+1)%B,b));a=(len(ps)-1)*B;fs.append((v1,a+b,a+(b+1)%B))
    o=mesh(name,vs,fs);o['purpose']='Broad directional hair form; no fine strands'
    return o

# Authored asymmetric major sweeps, coordinated from front and side references.
paths=[
 ('FringeMain',[(.085,-.018,1.365),(.060,-.115,1.350),(.020,-.175,1.290),(-.015,-.161,1.228),(-.053,-.139,1.216)],.033,.013),
 ('FringeLeft',[(-.042,-.015,1.358),(-.115,-.103,1.345),(-.110,-.162,1.291),(-.068,-.170,1.257),(-.014,-.149,1.276)],.038,.013),
 ('FringeRight',[(.105,-.005,1.337),(.136,-.084,1.324),(.142,-.139,1.277),(.124,-.145,1.240),(.101,-.122,1.232)],.027,.012),
 ('FringeSweep',[(-.030,-.050,1.354),(-.060,-.144,1.325),(-.031,-.180,1.291),(.006,-.171,1.298),(.015,-.151,1.319)],.024,.011),
 ('FringeTemple',[(-.103,-.040,1.304),(-.146,-.116,1.282),(-.135,-.151,1.244),(-.111,-.146,1.225),(-.093,-.126,1.235)],.023,.010),
 ('FringeTurn',[(.115,-.020,1.309),(.134,-.117,1.282),(.111,-.151,1.259),(.097,-.143,1.240),(.073,-.124,1.237)],.019,.010),
 ('TopFlow',[(-.101,.036,1.333),(-.066,-.033,1.378),(.003,-.047,1.391),(.060,-.033,1.370),(.076,-.016,1.356)],.035,.012),
 ('TopWave',[(.052,.045,1.354),(.094,.010,1.389),(.128,-.020,1.384),(.133,-.042,1.362),(.111,-.047,1.356)],.024,.010),
 ('CrownRear',[(-.078,.093,1.331),(-.024,.094,1.373),(.046,.094,1.364),(.079,.125,1.331),(.075,.145,1.309)],.032,.012),
]
for side in [-1,1]:
    # Staggered outward-curving temple groups, leaving the eyes and ear fronts free.
    for i,(y,z,w) in enumerate([(-.082,1.292,.031),(-.028,1.240,.029),(.026,1.195,.025),(.086,1.226,.030),(.115,1.285,.030)]):
        shift=.005*side*(i%2)
        p=[(side*.120,y+.012,z+.039+shift),(side*.164,y-.022,z+.018+shift),
           (side*.175,y-.022,z-.014+shift),(side*.177,y-.004,z-.027+shift),
           (side*.162,y+.010,z-.020+shift)]
        paths.append(('Temple%s_%d'%(side,i),p,w,.012))
    for i,(y,z) in enumerate([(.100,1.315),(.147,1.250),(.139,1.170)]):
        p=[(side*.095,y-.020,z+.038),(side*.142,y+.028,z+.016),
           (side*.161,y+.047,z-.014),(side*.155,y+.055,z-.040),(side*.136,y+.038,z-.043)]
        paths.append(('RearSide%s_%d'%(side,i),p,.031,.013))
for i,(x,z) in enumerate([(-.073,1.335),(.025,1.315),(.092,1.295),(-.021,1.253),(-.085,1.210),(.059,1.201)]):
    p=[(x-.012,.117,z+.042),(x+.030,.160,z+.026),(x+.048,.180,z-.004),
       (x+.033,.177,z-.040),(x+.011,.155,z-.045)]
    paths.append(('BackFlow%d'%i,p,.033,.014))
# Broad shallow flows cover the crown and rear cap without isolated leaf pads.
# Roots sit inside the envelope; visible ridges fan from a parting and curl down.
for j,(phi,n) in enumerate([(.63,7),(1.12,9),(1.67,10),(2.05,7)]):
    for k in range(n):
        a=math.tau*(k+.26*j)/n
        if phi>1.50 and math.cos(a)>.40:continue
        points=[]
        for t,da,dp,lift in [(0,-.28,-.23,-.007),(.25,-.06,-.05,.009),
                              (.55,.28,.13,.013),(.82,.44,.30,.009),(1,.30,.39,.012)]:
            aa=a+da;pp=phi+dp
            rr=lift
            x=(.166+rr)*math.sin(aa)*math.sin(pp)
            y=.020-(.149+rr)*math.cos(aa)*math.sin(pp)
            z=1.242+(.146+rr*.7)*math.cos(pp)
            if math.cos(aa)<0 and pp>1.85:z-=.024*max(0,(pp-1.85)/.60)
            points.append((x,y,z))
        paths.append(('CrownConnected%d_%d'%(j,k),points,.023+.004*math.sin(k*2.3),.009))
for name,p,w,d in paths:lock(name,p,w,d)

# Blend overlapping roots and broad flows into a single sculptable hair volume.
parts=[o for o in C.objects if o.type=='MESH' and not o.get('source_v4_object')]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True);o.modifiers.clear()
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();hair=parts[0];hair.name='YT5_HairSculptVolume'
mod=hair.modifiers.new('Join broad curl roots','REMESH');mod.mode='VOXEL';mod.voxel_size=.0018;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=hair.modifiers.new('Soft connected flow transitions','SMOOTH');mod.factor=.65;mod.iterations=8;bpy.ops.object.modifier_apply(modifier=mod.name)
# Remove only tiny voxel crumbs generated in this new working mesh.
bm=bmesh.new();bm.from_mesh(hair.data);seen=set();components=[]
for v in bm.verts:
    if v in seen:continue
    stack=[v];seen.add(v);group=[]
    while stack:
        q=stack.pop();group.append(q)
        for edge in q.link_edges:
            n=edge.other_vert(q)
            if n not in seen:seen.add(n);stack.append(n)
    components.append(group)
crumbs=[v for group in components if len(group)<100 for v in group]
if crumbs:bmesh.ops.delete(bm,geom=crumbs,context='VERTS')
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bm.to_mesh(hair.data);bm.free()
hair['major_flow_count']=len(paths)
hair['removed_generated_voxel_crumbs']=len(crumbs)


# Preserve total height exactly, with only a local crown adjustment.
allhair=[o for o in C.objects if o.type=='MESH' and not o.get('source_v4_object')]
high=max(v.co.z for o in allhair for v in o.data.vertices)
for o in allhair:
    for v in o.data.vertices:
        if v.co.z>1.33:v.co.z=1.33+(v.co.z-1.33)*(.07/(high-1.33))

# Reference silhouette: narrower lateral spread and hair down to the nape.
for o in allhair:
    for v in o.data.vertices:
        v.co.x*=.94
        back=max(0,min(1,(v.co.y-.025)/.055))
        low=max(0,min(1,(1.215-v.co.z)/.100))
        nape=max(0,1-(abs(v.co.x)/.155)**2)
        v.co.z-=.052*back*low*low*nape
        # Keep lower rear curls close to the head, rather than stretching hooks.
        r=math.hypot(v.co.x,v.co.y-.020)
        inward=max(0,min(1,(1.19-v.co.z)/.060))*back
        if r>.185:
            f=1-inward*(1-.185/r)
            v.co.x*=f;v.co.y=.020+(v.co.y-.020)*f

# Hide, never delete, the V4 collection and keep packed reference objects intact.
old.hide_render=True;old.hide_viewport=True
for o in C.objects:o.hide_set(False)
bpy.context.view_layer.objects.active=h
bpy.ops.object.select_all(action='DESELECT');h.select_set(True)
# Dedicated locked Blender inspection cameras; original cameras stay untouched.
review=bpy.data.collections.new('YT5_ReviewCameras');s.collection.children.link(review)
for name,az,elev,kind,scale,dist,center in [
 ('Front',0,0,'ORTHO',1.62,4,(0,0,.70)),
 ('RightOrtho',90,0,'ORTHO',1.62,4,(0,0,.70)),
 ('Back',180,0,'ORTHO',1.62,4,(0,0,.70)),
 ('Game',-45,35,'PERSP',1.62,3.4,(0,0,.70)),
 ('HeadQuarter',-45,0,'ORTHO',.45,4,(0,.02,1.21))]:
    d=bpy.data.cameras.new('YT5_FormReview_'+name);o=bpy.data.objects.new(d.name,d);review.objects.link(o)
    a=math.radians(az);e=math.radians(elev);c=Vector(center)
    o.location=c+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*dist
    o.rotation_euler=(c-o.location).to_track_quat('-Z','Y').to_euler()
    d.type=kind;d.ortho_scale=scale;d.sensor_fit='HORIZONTAL' if kind=='PERSP' else 'VERTICAL'
    d.sensor_width=36;d.lens=36/(2*math.tan(math.radians(35)/2))
    o.lock_location=(True,True,True);o.lock_rotation=(True,True,True);o.lock_scale=(True,True,True);o.hide_select=True
    o['purpose']='Blender form inspection only; not Unreal camera; reference perspective approximate'
s.camera=bpy.data.objects['YT5_FormReview_Game']
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_location=(0,0,.75)
            area.spaces.active.region_3d.view_distance=2.6
            area.spaces.active.region_3d.view_rotation=s.camera.rotation_euler.to_quaternion()
            area.spaces.active.region_3d.view_perspective='ORTHO'
s['V5_review_camera']='Frozen review: orthographic front/side/back; game 35 deg elevation, 35 deg horizontal FOV, 3.40 m. Approximation, not solved camera calibration.'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/YoungTrainer_HeadForm_V5.blend'))
print('V5 HEAD FORM SAVED',len(paths),'broad flows; body unchanged')
