"""Reusable V3 furniture/sign props; run only after the actual front PIE gate.

Architecture is read-only. Small scene dressing is authored separately in Unreal.
Save the explicit source, reopen for review, then use ExportHealingHouseV3.py.
"""
import bpy, math, json, shutil
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'Art/HealingHouse'
SOURCE = ART/'Source/HealingHouse_V3.blend'
REVIEW = ART/'Review/V3/Dressing'
assert bpy.app.background and Path(bpy.data.filepath) == SOURCE
assert json.loads((ART/'Review/V3/Front/PIEGate.json').read_text())['phase1_passed']
assert not bpy.data.collections.get('HH_V3_Props'), 'Do not duplicate existing dressing'
REVIEW.mkdir(parents=True, exist_ok=True)
front_source = ART/'Source/HealingHouse_V3_Front.blend'
assert not front_source.exists()
shutil.copy2(SOURCE, front_source)
scene = bpy.data.scenes['HealingHouse_V3']
bpy.context.window.scene = scene
collection = bpy.data.collections.new('HH_V3_Props')
scene.collection.children.link(collection)
materials = {n:bpy.data.materials['HH_V2_'+n] for n in ('Wood','Timber','Metal','Glass','Stone')}
def material(name, color, emission=0):
    mat = bpy.data.materials.new('HH_V3_'+name)
    mat.diffuse_color = (*color,1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color,1)
    shader.inputs['Roughness'].default_value = .88
    if emission:
        shader.inputs['Emission Color'].default_value = (*color,1)
        shader.inputs['Emission Strength'].default_value = emission
    materials[name] = mat
material('Linen',(.64,.60,.45))
material('Sage',(.23,.36,.25))
material('Ochre',(.49,.32,.16))
material('Cream',(.88,.77,.49))
material('Lamp',(.95,.54,.18),.65)
parts = []
def finish(obj, mat, bevel=0):
    obj.data.materials.append(materials[mat])
    if bevel:
        mod = obj.modifiers.new('Soft crafted edges','BEVEL')
        mod.width = bevel; mod.segments = 2
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    parts.append(obj)
    return obj
def box(location,size,mat,bevel=.015):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj=bpy.context.object; obj.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(obj,mat,bevel)
def cylinder(location,radius,depth,mat,rotation=(0,0,0),vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=location,rotation=rotation)
    return finish(bpy.context.object,mat,.006)
def beam(a,b,width,mat):
    delta=Vector(b)-Vector(a)
    obj=box((Vector(a)+Vector(b))/2,(width,width,delta.length),mat,.009)
    obj.rotation_euler=delta.to_track_quat('Z','Y').to_euler()
def join(name, position):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.object.join()
    obj=parts[0];obj.name='HH_V3_'+name
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    scene.cursor.location=(0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    for c in list(obj.users_collection):c.objects.unlink(obj)
    collection.objects.link(obj)
    # Local metre UVs; existing wood/timber materials remain reusable.
    uv=obj.data.uv_layers.get('UVMap') or obj.data.uv_layers.new(name='UVMap')
    for polygon in obj.data.polygons:
        axis=max(range(3),key=lambda i:abs(polygon.normal[i]))
        a,b=((1,2),(0,2),(0,1))[axis]
        for li in polygon.loop_indices:
            co=obj.data.vertices[obj.data.loops[li].vertex_index].co
            uv.data[li].uv=(co[a],co[b])
    obj.location=(position[0],-position[1],position[2])
    obj['role']='Reusable visual prop; collision assigned in Unreal'
    parts.clear()
    return obj
placements={}
def placed(name,cm):
    placements[name]={'unreal_location_cm':cm}
    return join(name,tuple(v/100 for v in cm))

for name,length,width,pos in [('TreatmentBedSmall',1.40,.82,[-45,345,0]),
                             ('TreatmentBedLarge',1.80,1.05,[165,345,0])]:
    for x in (-length/2+.10,length/2-.10):
        for y in (-width/2+.10,width/2-.10):box((x,y,.18),(.12,.12,.36),'Timber')
    box((0,0,.35),(length,width,.14),'Wood',.025)
    box((0,0,.45),(length-.10,width-.10,.15),'Linen',.055)
    box((.12,0,.535),(length*.64,width-.12,.035),'Sage',.012)
    box((-length/2+.24,0,.565),(.32,width-.20,.10),'Cream',.04)
    for y in (-width/2+.03,width/2-.03):beam((-length/2,y,.4),(-length/2,y,.7),.07,'Timber')
    box((-length/2,0,.64),(.08,width,.12),'Wood')
    placed(name,pos)

for name,length,height,pos in [('HerbShelf',1.90,1.70,[155,-385,0]),
                              ('Bookcase',1.05,1.80,[-170,-385,0])]:
    for x in (-length/2+.05,length/2-.05):box((x,0,height/2),(.09,.40,height),'Timber')
    box((0,.17,height/2),(length,.05,height),'Wood',.01)
    for z in (.12,.58,1.06,height-.07):box((0,0,z),(length,.42,.07),'Wood')
    box((0,0,height+.04),(length+.12,.46,.10),'Timber')
    placed(name,pos)

for x in (-.50,.50):
    for y in (-.25,.25):box((x,y,.39),(.09,.09,.78),'Timber')
box((0,0,.80),(1.20,.65,.08),'Wood',.02)
box((0,0,.20),(1.05,.52,.05),'Wood')
placed('HerbTable',[-255,315,0])

# Wall-mounted iron arm, with a gentle brace and two visible hanging loops.
box((0,0,.04),(.055,.14,.55),'Metal')
beam((0,0,.21),(-.68,0,.21),.045,'Metal')
beam((0,0,-.18),(-.57,0,.21),.033,'Metal')
for y in (-.20,.20):
    beam((-.63,y,.20),(-.63,y,-.10),.025,'Metal')
placed('SignBracket',[-477,142,235])

# Original emblem: two growing leaves inside a protective ring, three small
# creature toe marks at its base. No bisected ball or franchise logo.
box((-.63,0,-.49),(.065,.74,.83),'Sage',.06)
box((-.674,0,-.49),(.022,.66,.75),'Timber',.025)
bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=8,
    location=(-.696,0,-.44),rotation=(0,math.pi/2,0),major_radius=.255,minor_radius=.018)
finish(bpy.context.object,'Cream')
beam((-.717,0,-.58),(-.717,0,-.27),.018,'Cream')
for sign in (-1,1):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(-.72,sign*.092,-.35))
    obj=bpy.context.object;obj.scale=(.013,.056,.113);obj.rotation_euler.x=sign*.62
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    finish(obj,'Cream')
for y,z in ((-.065,-.66),(0,-.68),(.065,-.66)):
    cylinder((-.72,y,z),.025,.015,'Cream',(0,math.pi/2,0))
placed('GuardianSign',[-477,142,235])

# A small reusable lantern; the scene light is a separate Unreal component.
box((0,0,.18),(.18,.18,.30),'Lamp',.012)
for x in (-.115,.115):
    for y in (-.115,.115):box((x,y,.18),(.025,.025,.36),'Metal',.006)
box((0,0,.02),(.27,.27,.04),'Metal')
box((0,0,.365),(.30,.30,.055),'Metal')
bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.235,radius2=.05,depth=.13,location=(0,0,.455),rotation=(0,0,math.pi/4))
finish(bpy.context.object,'Metal',.012)
beam((0,0,.50),(0,0,.60),.028,'Metal')
placed('Lantern',[-520,-135,165])

for name,entry in placements.items():
    obj=bpy.data.objects['HH_V3_'+name]
    mins=[min(v.co[i] for v in obj.data.vertices) for i in range(3)]
    maxs=[max(v.co[i] for v in obj.data.vertices) for i in range(3)]
    obj.data.calc_loop_triangles()
    entry.update({'name':obj.name,'size_cm':[100*(b-a) for a,b in zip(mins,maxs)],
                  'triangles':len(obj.data.loop_triangles)})
(REVIEW/'PropAudit.json').write_text(json.dumps(placements,indent=2)+'\n')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
print('V3_PROPS_SAVED',len(placements),str(SOURCE))
