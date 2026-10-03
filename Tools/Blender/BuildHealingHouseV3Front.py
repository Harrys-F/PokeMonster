"""Build V3 front in a separate source; V1/V2 sources are never overwritten.
Run background Blender with HEAD V2 loaded. Review and export are separate.
"""
import bpy, bmesh, json, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'Art/HealingHouse'; REVIEW=ART/'Review/V3/Front'
SOURCE=ART/'Source/HealingHouse_V3.blend'
assert bpy.app.background and Path(bpy.data.filepath)==ART/'Source/HealingHouse_V2.blend'
assert not SOURCE.exists(), 'Preserve existing V3 source'
scene=bpy.data.scenes['HealingHouse_V2']; bpy.context.window.scene=scene
architecture=bpy.data.collections['HH_V2_Architecture']
assert len(architecture.objects)==39
REVIEW.mkdir(parents=True,exist_ok=True)
# Current HEAD source accidentally retains the earlier 10.30-m geometry.
# Recover the documented map proportions on copied mesh data, never actor scale.
span=max(v.co.y for v in bpy.data.objects['HH_V2_Foundation'].data.vertices)-min(v.co.y for v in bpy.data.objects['HH_V2_Foundation'].data.vertices)
assert abs(span-10.3)<.01, span
def facade_y(y):
    # Windows retain their width in the middle strip; only the free doorway
    # and outer infill strips contract. Outside extensions move with the wall.
    sign = 1 if y >= 0 else -1
    a = abs(y)
    if a <= 1.2: out = a * .85 / 1.2
    elif a <= 3.85: out = a - .35
    elif a <= 5: out = 3.5 + (a-3.85) * .85/1.15
    else: out = a - .65
    return sign * out

def islands(data):
    parent = list(range(len(data.vertices)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for edge in data.edges:
        a,b = edge.vertices
        parent[find(a)] = find(b)
    result = {}
    for vertex in data.vertices:
        result.setdefault(find(vertex.index), []).append(vertex)
    return result.values()

roof_ratio = 9/10.3
loft_shift = .6 * (roof_ratio-1)
changed = []
for obj in architecture.objects:
    name = obj.name.removeprefix('HH_V2_')
    before = [tuple(v.co) for v in obj.data.vertices]
    # Work in authoring Unreal metres, undoing the one FBX handedness mirror.
    for vertex in obj.data.vertices: vertex.co.y *= -1
    vertices = obj.data.vertices
    if name == 'Foundation':
        for v in vertices: v.co.y *= 9/10.3
    elif name == 'Floor':
        for v in vertices: v.co.y *= 8.4/9.7
    elif name in ('Walls_Front', 'Walls_Rear', 'Stone_Front', 'Stone_Rear'):
        for v in vertices:
            old_y = v.co.y
            v.co.y = facade_y(old_y)
            if name == 'Walls_Front' and abs(abs(old_y)-1.2)<.001 and abs(v.co.z-2.3)<.001:
                v.co.z = 2.15
    elif name in ('Walls_CameraSide','Glass_CameraSide','Windows_CameraSide',
                  'Timber_CameraSide','Stone_CameraSide','InteriorBeams_CameraSide'):
        for v in vertices: v.co.y -= .65
    elif name in ('Walls_Far','Glass_Far','Windows_Far','Timber_Far','Stone_Far'):
        for v in vertices: v.co.y += .65
    elif name in ('Roof_Main','Roof_Trim','Gable_Front','Gable_Rear'):
        for v in vertices:
            old_y = v.co.y
            radius = ((old_y-.6)**2+(v.co.z-4.45)**2)**.5
            v.co.y = old_y * roof_ratio
            if name == 'Gable_Front' and abs(radius-.47)<.002:
                v.co.y = old_y + loft_shift
    elif name in ('Glass_Loft','Windows_Loft'):
        for v in vertices: v.co.y += loft_shift
    elif name in ('Glass_Front','Windows_Front'):
        for part in islands(obj.data):
            centre = (min(v.co.y for v in part)+max(v.co.y for v in part))/2
            delta = -.35 if centre > 0 else .35
            for v in part: v.co.y += delta
    elif name in ('Timber_Front','Timber_Rear'):
        for part in islands(obj.data):
            lo,hi = min(v.co.y for v in part),max(v.co.y for v in part)
            if min(v.co.z for v in part) >= 2.6:
                for v in part: v.co.y *= roof_ratio
            elif hi-lo < .5:
                delta = facade_y((lo+hi)/2)-(lo+hi)/2
                for v in part: v.co.y += delta
            else:
                for v in part: v.co.y = facade_y(v.co.y)
    elif name in ('Roof_Porch','Timber_Porch','PorchFloor'):
        for v in vertices: v.co.y += .65
    elif name in ('Roof_Entry','Timber_Entry'):
        for v in vertices:
            v.co.y *= 2.4/3.1
            v.co.z -= .15
    elif name == 'DoorFrame':
        for part in islands(obj.data):
            lo,hi = min(v.co.y for v in part),max(v.co.y for v in part)
            if hi-lo < .5:
                delta = -.35 if (lo+hi)>0 else .35
                for v in part: v.co.y += delta
            else:
                for v in part: v.co.y *= (hi-lo-.7)/(hi-lo)
            for v in part: v.co.z *= 2.15/2.3
    elif name == 'DoorLeaf':
        for v in vertices:
            v.co.x = -4.56 + (v.co.x+4.56)*1.7/2.4
            v.co.y += .35
            v.co.z *= 2.15/2.3
    elif name == 'InteriorBeams':
        for part in islands(obj.data):
            lo,hi = min(v.co.y for v in part),max(v.co.y for v in part)
            if hi-lo > 8:
                for v in part: v.co.y *= 8.2/9.5
            else:
                for v in part: v.co.y += .65
    elif name == 'InteriorStone':
        for v in vertices: v.co.y *= 8.15/9.45
    elif name not in ('Counter','Chimney','ChimneyCap'):
        raise RuntimeError('Unhandled module: '+name)
    for v in vertices: v.co.y *= -1
    obj.data.update()
    if before != [tuple(v.co) for v in vertices]: changed.append(obj.name)

# All following edits affect only the corrected front and roof connection.
front_changed=[]
peak=.6*9/10.3
edge=5*9/10.3
roofedge=5.55*9/10.3
def center_profile(y,end):
    return -end+(y+end)*end/(peak+end) if y<=peak else (y-peak)*end/(end-peak)
def door_y(y):
    a=abs(y)
    if a<=.85: new=a*.75/.85
    elif a<1.7: new=a-.1*(1.7-a)/.85
    else: new=a
    return math.copysign(new,y)
for obj in architecture.objects:
    name=obj.name.removeprefix('HH_V2_')
    before=[tuple(v.co) for v in obj.data.vertices]
    for v in obj.data.vertices: v.co.y*=-1
    if name=='Walls_Front':
        for v in obj.data.vertices: v.co.y=door_y(v.co.y)
    elif name=='Stone_Front':
        for v in obj.data.vertices:
            a=abs(v.co.y)
            if a<1.7: v.co.y-=math.copysign(.1*(1.7-a)/.8,v.co.y)
    elif name=='DoorFrame':
        for part in islands(obj.data):
            lo,hi=min(v.co.y for v in part),max(v.co.y for v in part)
            if hi-lo<.5:
                for v in part:v.co.y-=math.copysign(.1,(lo+hi)/2)
            else:
                for v in part:v.co.y*=(hi-lo-.2)/(hi-lo)
    elif name=='DoorLeaf':
        for v in obj.data.vertices:
            v.co.x=-4.56+(v.co.x+4.56)*1.5/1.7
            v.co.y+=.1
    elif name in ('Glass_Loft','Windows_Loft'):
        for v in obj.data.vertices:v.co.y-=peak
    elif name in ('Gable_Front','Gable_Rear'):
        for v in obj.data.vertices:
            radius=((v.co.y-peak)**2+(v.co.z-4.45)**2)**.5
            v.co.y=v.co.y-peak if name=='Gable_Front' and abs(radius-.47)<.002 else center_profile(v.co.y,edge)
    elif name in ('Roof_Main','Roof_Trim'):
        for v in obj.data.vertices:v.co.y=center_profile(v.co.y,roofedge)
    elif name=='Timber_Rear':
        for part in islands(obj.data):
            if max(v.co.z for v in part)>2.8:
                for v in part:v.co.y=center_profile(v.co.y,edge)
    elif name=='Timber_Front':
        # Retain lower posts/rails. Upper members are rebuilt as balanced pairs,
        # with a split central king post around the true round-window aperture.
        keep=[v.index for part in islands(obj.data) if max(v.co.z for v in part)<=2.8 for v in part]
        keep=set(keep)
        coords=[]; remap={}
        for v in obj.data.vertices:
            if v.index in keep:
                co=v.co.copy()
                if abs(co.y)<1.5:co.y=door_y(co.y)
                remap[v.index]=len(coords);coords.append(tuple(co))
        faces=[tuple(remap[i] for i in p.vertices) for p in obj.data.polygons if all(i in keep for i in p.vertices)]
        def beam(a,b,width=.22):
            a,b=Vector(a),Vector(b);q=Vector((0,0,1)).rotation_difference((b-a).normalized())
            start=len(coords);length=(b-a).length
            coords.extend(tuple((a+b)/2+q@Vector((x*width/2,y*width/2,z*length/2))) for x,y,z in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)))
            faces.extend(tuple(start+i for i in f) for f in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)))
        for z0,z1 in ((2.75,3.8),(5.1,6.18)):beam((-4.7,0,z0),(-4.7,0,z1))
        for sign in (-1,1):
            beam((-4.7,sign*edge,2.65),(-4.7,0,6.20),.27)
            h=3.05; top=2.6+(1-h/edge)*3.65
            beam((-4.7,sign*h,2.76),(-4.7,sign*h,top-.14),.20)
            beam((-4.7,sign*3.10,2.72),(-4.7,sign*1.70,4.18),.22)
        materials=list(obj.data.materials)
        data=bpy.data.meshes.new('V3_FrontBalancedGeometry');data.from_pydata(coords,[],faces)
        for m in materials:data.materials.append(m)
        obj.data=data
        # UVs retain the established world-oriented timber texture scale.
        uv=data.uv_layers.new(name='ArchitecturalUV');data.update()
        for p in data.polygons:
            axis=max(range(3),key=lambda a:abs(p.normal[a]));axes=((1,2),(0,2),(0,1))[axis]
            for li in p.loop_indices:
                c=data.vertices[data.loops[li].vertex_index].co
                uv.data[li].uv=(c[axes[0]]/.8,c[axes[1]]/3)
    for v in obj.data.vertices:v.co.y*=-1
    obj.data.update()
    if before!=[tuple(v.co) for v in obj.data.vertices]:front_changed.append(obj.name)

modules=[]
for o in architecture.objects:
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    nm=sum(not e.is_manifold for e in bm.edges)
    assert nm==(8 if o.name in ('HH_V2_InteriorBeams','HH_V2_InteriorBeams_CameraSide') else 0),(o.name,nm)
    bm.to_mesh(o.data);bm.free();o.data.update();o.data.calc_loop_triangles()
    c=[v.co for v in o.data.vertices];lo=[min(v[i] for v in c) for i in range(3)];hi=[max(v[i] for v in c) for i in range(3)]
    modules.append({'name':o.name,'triangles':len(o.data.loop_triangles),'non_manifold_edges':nm,'unreal_bounds_min_m':[lo[0],-hi[1],lo[2]],'unreal_bounds_max_m':[hi[0],-lo[1],hi[2]],'materials':[m.name for m in o.data.materials]})
scene.name='HealingHouse_V3'
scene['v3_front']='Door 1.50 x 2.15; facade axis Y=0; main 9.00 x 9.30; no global scale'
scene['source_head']='477e6f6'
for s in list(bpy.data.scenes):
    if s!=scene:bpy.data.scenes.remove(s)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
(REVIEW/'GeometryAudit.json').write_text(json.dumps({'source':str(SOURCE),'source_head':'477e6f6','modules':modules,'changed_front_modules':front_changed,'recovered_source_proportions':True,'door_m':[1.5,2.15],'main_m':[9.3,9.0],'axis_y_m':0,'unchanged_counter':True,'total_triangles':sum(m['triangles'] for m in modules)},indent=2)+'\n')
print('V3_FRONT_SAVED',front_changed)
