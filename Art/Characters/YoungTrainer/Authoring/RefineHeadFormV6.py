"""Local, topology-preserving head refinement from V5; save only new V6.

Run in live Blender with saved V5 open. Never run twice on the same scene.
Existing mesh data, materials, rig, packed references and files stay unchanged.
"""
import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector

R = Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath) == R/'Source/YoungTrainer_HeadForm_V5.blend'
assert 'YT6_Player' not in bpy.data.collections
assert not (R/'Source/YoungTrainer_HeadForm_V6.blend').exists()
C = bpy.data.collections.new('YT6_Player')
bpy.context.scene.collection.children.link(C)
old = bpy.data.collections['YT5_Player']
copies = {}
for o in old.objects:
    n = o.copy()
    if o.data: n.data = o.data.copy()
    n.name = o.name.replace('YT5_', 'YT6_', 1)
    C.objects.link(n)
    copies[o] = n
    n['source_v5_object'] = o.name
    n.hide_render = False
    n.hide_set(False)
for o, n in copies.items():
    n.parent = copies.get(o.parent, o.parent)
root = bpy.data.objects['YT6_PlayerRoot']
root['scope'] = 'V6 local hair, eye, lid, brow, mouth and ear refinement only'

def smooth(a, b, x):
    t = max(0., min(1., (x-a)/(b-a)))
    return t*t*(3-2*t)

def interp(z, rows):
    xs=[r[0] for r in rows]; ys=[r[1] for r in rows]
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
            return (2*t**3-3*t*t+1)*ys[i]+(t**3-2*t*t+t)*h*slopes[i]+(-2*t**3+3*t*t)*ys[i+1]+(t**3-t*t)*h*slopes[i+1]

def facial_surface(x,z):
    rx=interp(z,[(1.029,.021),(1.050,.073),(1.080,.104),(1.110,.124),(1.170,.142),(1.220,.131),(1.260,.113),(1.307,.025)])
    ry=interp(z,[(1.029,.036),(1.050,.068),(1.080,.090),(1.110,.104),(1.170,.110),(1.220,.107),(1.260,.085),(1.307,.028)])
    y=.006-ry*math.sqrt(max(.015,1-min(.999,abs(x)/rx)**2.5))
    y-=.002*math.exp(-((abs(x)-.067)/.040)**2-((z-1.107)/.031)**2)
    y-=.009*math.exp(-(x/.014)**2-((z-1.121)/.013)**2)
    return y

def hair_metrics(o):
    bm=bmesh.new();bm.from_mesh(o.data)
    vol=abs(bm.calc_volume(signed=True));bm.free()
    lo=[min(v.co[i] for v in o.data.vertices) for i in range(3)]
    hi=[max(v.co[i] for v in o.data.vertices) for i in range(3)]
    return {'volume_m3':vol,'bounds_m':{'min':lo,'max':hi},'dimensions_cm':[(b-a)*100 for a,b in zip(lo,hi)]}

hair = bpy.data.objects['YT6_HairSculptVolume']
hair_before = hair_metrics(hair)
changed=0; max_delta=0.; frozen_fringe=0
for v in hair.data.vertices:
    p=v.co.copy();x,y,z=p
    # Leave central front locks and crown extremum exactly unchanged.
    front_lock = y < -.115 and abs(x) < .103
    crown = 1-smooth(1.369,1.397,z)
    if front_lock:
        frozen_fringe+=1
        continue
    side=smooth(.104,.171,abs(x))*(1-smooth(1.345,1.392,z))
    side*=smooth(-.149,-.068,y)
    side*=.96 if x<0 else 1.04
    v.co.x=x-math.copysign(.0135*side*crown,x)
    rear=smooth(.044,.182,y)
    v.co.y=y-.021*rear*crown
    # Reduce the upper bulk in X/Y, never lower the crown or alter hairline Z.
    upper=smooth(1.285,1.343,z)*crown*smooth(-.100,.035,y)
    v.co.x-=x*.037*upper
    v.co.y-=(y-.020)*.043*upper
    delta=(v.co-p).length
    changed+=v.co!=p;max_delta=max(max_delta,delta)
hair.data.update()
hair_after=hair_metrics(hair)
hair['v6_refinement']='Local temple/back/upper bulk reduction; central frontal locks and crown preserved; same topology'

# Light hooding of the upper whites. Corners stay fixed and remain asymmetric almond.
def white_xz(x,z):
    cx=.052337 if x>0 else -.052337
    u=min(1.,abs(x-cx)/.035)
    z-=.0037*smooth(1.155,1.185,z)*(1-.32*u*u)
    return x,z

def surface_y(x,z,offset):
    cx=.052337 if x>0 else -.052337
    r=min(1.,((x-cx)/.0315)**2+((z-1.156)/.0345)**2)
    return facial_surface(x,z)-offset-.0012*(1-r)

head=bpy.data.objects['YT6_Head']
for v in head.data.vertices:
    names={head.vertex_groups[g.group].name for g in v.groups}
    if names & {'Topology_EyeR','Topology_EyeL'}:
        x,z=white_xz(v.co.x,v.co.z)
        v.co=(x,facial_surface(x,z),z)

for side in ['R','L']:
    white=bpy.data.objects['YT6_EyeWhite_'+side]
    for v in white.data.vertices:
        x,z=white_xz(v.co.x,v.co.z)
        v.co=(x,surface_y(x,z,.001),z)
    for name,off in [('Iris',.0016),('IrisWarm',.0018),('Pupil',.002),('EyeGlint',.0025),('EyeGlintSmall',.0026)]:
        o=bpy.data.objects['YT6_'+name+'_'+side]
        for v in o.data.vertices:
            x,y,z=v.co;cx=.052337 if x>0 else -.052337
            x=cx+(x-cx)*1.015
            z=1.156+(z-1.156)*.99+.0025
            v.co=(x,surface_y(x,z,off),z)
    for name,thickness,off in [('UpperLid',1.38,.0018),('LowerLid',.62,.0003)]:
        o=bpy.data.objects['YT6_'+name+'_'+side]
        coords=[v.co.copy() for v in o.data.vertices]
        assert len(coords)==202
        centers=[sum(coords[i*8:(i+1)*8],Vector())/8 for i in range(25)]
        for i,v in enumerate(o.data.vertices):
            ring=min(i//8,24) if i<200 else (0 if i==200 else 24)
            center=centers[ring];p=center+(coords[i]-center)*thickness
            x,z=white_xz(p.x,p.z)
            # Define only the outer fifth of the corner; no global eye widening.
            outer=smooth(.80,1.,ring/24)
            x+=math.copysign(.0012*outer,x)
            z-=.0006*outer
            v.co=(x,surface_y(x,z,off),z)
    brow=bpy.data.objects['YT6_Brow_'+side]
    for v in brow.data.vertices:
        x,y,z=v.co
        z=1.196+(z-1.196)*.88-.0015
        v.co=(x,facial_surface(x,z)-.002,z)

# Narrow neutral smile, not a broad permanent grin. Only oral loops and mouth.
for name in ['MouthLine','MouthCavity']:
    o=bpy.data.objects['YT6_'+name]
    for v in o.data.vertices:
        x,y,z=v.co;x*=.97
        z+=.00065*(abs(x)/.025)**2
        v.co=(x,facial_surface(x,z)-(.0015 if name=='MouthLine' else .0003),z)
for v in head.data.vertices:
    if any(head.vertex_groups[g.group].name=='Topology_Mouth' for g in v.groups):
        x,y,z=v.co;x*=.97;z+=.00065*(abs(x)/.025)**2
        v.co=(x,facial_surface(x,z),z)

# Body stores ears as two disconnected components; all non-ear vertices untouched.
body=bpy.data.objects['YT6_Body']
assert len(body.data.vertices)==746
for v in body.data.vertices:
    if v.index<302:continue
    p=v.co.copy();sign=1 if p.x>0 else -1
    cx=sign*.13515;cz=1.123591;cy=.0109243
    x=cx+(p.x-cx)*.92
    z=cz+(p.z-cz)*.95
    z+=.0030*(1-smooth(1.102,1.121,p.z))
    # Soft bowl in the front surface, broad rim; no fine cartilage geometry.
    radial=((p.x-cx)/.022)**2+((p.z-cz)/.023)**2
    front=1-smooth(.006,.016,p.y)
    cup=.0033*math.exp(-radial*3.8)
    rim=.0007*math.exp(-((radial-.70)/.26)**2)
    y=p.y+front*(cup-rim)
    # The ear bowl must also read from the side, not only from the front.
    lateral=smooth(.134,.153,abs(p.x))
    bowl=math.exp(-((p.y-cy)/.009)**2-((p.z-cz)/.017)**2)
    x-=sign*.0024*lateral*bowl
    v.co=(x,y,z)
for o in C.objects:
    if o.type=='MESH':o.data.update()
old.hide_render=True;old.hide_viewport=True
# Preserve the V5 cameras intact; copy only the current camera for new viewport.
oldcam=bpy.context.scene.camera
cam=oldcam.copy();cam.data=oldcam.data.copy();cam.name='YT6_FormReview_Game'
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera=cam
bpy.ops.object.select_all(action='DESELECT')
head.select_set(True);bpy.context.view_layer.objects.active=head
bpy.context.view_layer.update()
result={'version':'HeadForm V6','source':'Source/YoungTrainer_HeadForm_V5.blend',
        'output':'Source/YoungTrainer_HeadForm_V6.blend','height_m':1.4,
        'hair_before':hair_before,'hair_after':hair_after,
        'hair_volume_reduction_percent':100*(1-hair_after['volume_m3']/hair_before['volume_m3']),
        'hair_changed_vertices':changed,'hair_preserved_front_vertices':frozen_fringe,
        'maximum_hair_displacement_cm':max_delta*100,
        'upper_lid_cross_section_factor':1.38,'lower_lid_cross_section_factor':.62,
        'upper_whites_hooding_max_mm':3.7,'iris_width_factor':1.015,'iris_height_factor':.99,
        'iris_upward_mm':2.5,'ear_width_factor':.92,'ear_height_factor':.95,
        'ear_cup_depth_max_mm':3.3,'ear_lobe_lift_max_mm':3.0,'ear_side_bowl_max_mm':2.4,'non_ear_body_vertices_unchanged':302,
        'materials_uv_rig_animation_unchanged':True,
        'camera_note':'Fixed Blender illustration inspection camera; no Unreal changes'}
(R/'HEAD_FORM_V6.json').write_text(json.dumps(result,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/YoungTrainer_HeadForm_V6.blend'))
print(json.dumps(result,indent=2))
