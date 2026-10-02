"""Architectural art pass; run via the existing live Blender MCP connection.

Creates a separate scene and source. Coordinates are authored in Unreal metres,
then Y is mirrored once for Blender/FBX. All modules share an applied origin;
review cameras/lights never enter the mesh-only export. V1 is never modified.
"""
import bpy
import bmesh
import json
import math
import random
from pathlib import Path
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'Art/HealingHouse'
REVIEW = ART / 'Review/V2'
SOURCE = ART / 'Source/HealingHouse_V2.blend'
EXPORT = ART / 'Exports/HealingHouse_V2.fbx'
if SOURCE.exists() or EXPORT.exists() or bpy.data.scenes.get('HealingHouse_V2'):
    raise RuntimeError('V2 already exists; preserve existing work.')
REVIEW.mkdir(parents=True, exist_ok=True)
scene = bpy.data.scenes.new('HealingHouse_V2')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
architecture = bpy.data.collections.new('HH_V2_Architecture')
scene.collection.children.link(architecture)
groups = {}
openings = []
materials = {}
for name in ('Plaster', 'Wood', 'Timber', 'Stone', 'Roof', 'Metal', 'Glass'):
    mat = bpy.data.materials.new('HH_V2_' + name)
    mat.use_nodes = True
    shader = next(n for n in mat.node_tree.nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled')
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(str(ART / 'Textures/V2' / ('T_HH_V2_' + name + '.png')))
    mat.node_tree.links.new(tex.outputs['Color'], shader.inputs['Base Color'])
    shader.inputs['Roughness'].default_value = .82
    if name == 'Metal': shader.inputs['Metallic'].default_value = .15
    if name == 'Glass':
        mat.node_tree.links.new(tex.outputs['Color'], shader.inputs['Emission Color'])
        shader.inputs['Emission Strength'].default_value = .25
    mat.diffuse_color = {'Plaster': (.72,.64,.46,1), 'Wood': (.35,.20,.08,1),
                        'Timber': (.16,.08,.04,1), 'Stone': (.36,.36,.28,1),
                        'Roof': (.5,.18,.09,1), 'Metal': (.09,.12,.09,1),
                        'Glass': (.85,.54,.13,1)}[name]
    materials[name] = mat


def mesh(group, vertices, faces, material):
    data = bpy.data.meshes.new(group + '_Geometry')
    data.from_pydata(vertices, [], faces)
    data.materials.append(materials[material])
    data.update()
    obj = bpy.data.objects.new(group + '_Part', data)
    architecture.objects.link(obj)
    groups.setdefault(group, []).append(obj)
    return obj


def box(group, center, size, material='Timber'):
    vertices = [(center[0] + x * size[0] / 2, center[1] + y * size[1] / 2,
                 center[2] + z * size[2] / 2)
                for x,y,z in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
                              (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
    return mesh(group, vertices, [(0,3,2,1),(4,5,6,7),(0,1,5,4),
                                  (1,2,6,5),(2,3,7,6),(3,0,4,7)], material)


def beam(group, a, b, width=.24, depth=None, material='Timber'):
    direction = Vector(b) - Vector(a)
    obj = box(group, (0,0,0), (width, depth or width, direction.length), material)
    rotate = Vector((0,0,1)).rotation_difference(direction.normalized()).to_matrix().to_4x4()
    obj.data.transform(Matrix.Translation((Vector(a)+Vector(b))/2) @ rotate)
    return obj


def profile(group, points, plane, center, depth, material):
    # A closed profile swept through a wall; supports arched, round and gable modules.
    def coord(d, h, z):
        return (d,h,z) if plane == 'X' else (h,d,z)
    verts = [coord(d,h,z) for d in (center-depth/2, center+depth/2) for h,z in points]
    n = len(points)
    faces = [tuple(reversed(range(n))), tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(group, verts, faces, material)


def cut(wall, cutter):
    mod = wall.modifiers.new('TrueOpening', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.context.view_layer.objects.active = wall
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for parts in groups.values():
        if cutter in parts: parts.remove(cutter)
    bpy.data.objects.remove(cutter, do_unlink=True)


def arch(h, sill, width, height):
    radius = width / 2
    spring = sill + height - radius
    return [(h-radius,sill),(h+radius,sill),(h+radius,spring)] + [
        (h + radius * math.cos(a*math.pi/12), spring + radius*math.sin(a*math.pi/12))
        for a in range(1,13)]


def frame(group, pts, plane, center, width=.14, depth=.18, material='Wood'):
    def c(h,z): return (center,h,z) if plane == 'X' else (h,center,z)
    for i in range(len(pts)):
        beam(group, c(*pts[i]), c(*pts[(i+1)%len(pts)]), width, depth, material)


box('Floor', (0,0,-.08), (8.7,9.7,.16), 'Wood')
box('Foundation', (0,0,-.22), (9.3,10.3,.28), 'Stone')
front = box('Walls_Front', (-4.5,0,1.3), (.3,10,2.6), 'Plaster')
near = box('Walls_CameraSide', (0,5,1.3), (8.7,.3,2.6), 'Plaster')
rear = box('Walls_Rear', (4.5,0,1.3), (.3,10,2.6), 'Plaster')
far = box('Walls_Far', (0,-5,1.3), (8.7,.3,2.6), 'Plaster')
cut(front, box('Temporary', (-4.5,0,1.13), (.9,2.4,2.34), 'Plaster'))
openings.append({'id':'main_door','kind':'door','wall':'Walls_Front',
                 'width_m':2.4,'height_m':2.3,'threshold_m':0,'depth_m':.3,
                 'destination':'Existing free central aisle; real exterior/interior passage'})


def window(wall, group, plane, wallcenter, h, style):
    width, height, sill = (1.25,1.25,1.0) if style == 'Arch' else (1.2,1.15,1.08)
    pts = arch(h,sill,width,height) if style == 'Arch' else [
        (h-width/2,sill),(h+width/2,sill),(h+width/2,sill+height-.18),
        (h+width/2-.18,sill+height),(h-width/2+.18,sill+height),
        (h-width/2,sill+height-.18)]
    cut(wall, profile('Temporary', pts,plane,wallcenter,.9,'Plaster'))
    profile('Glass_'+group, pts,plane,wallcenter,.035,'Glass')
    outer = wallcenter + (-.24 if wallcenter < 0 else .24)
    frame('Windows_'+group,pts,plane,outer)
    def c(hh,z): return (outer,hh,z) if plane=='X' else (hh,outer,z)
    beam('Windows_'+group,c(h,sill),c(h,sill+height),.08,.12,'Wood')
    beam('Windows_'+group,c(h-width/2,sill+.45),c(h+width/2,sill+.45),.075,.12,'Wood')
    # Broad projecting sill and canopy, no decorative props or individual panes.
    size = (.35,width+.32,.13) if plane=='X' else (width+.32,.35,.13)
    center = c(h,sill-.10)
    box('Windows_'+group,center,size,'Stone')
    openings.append({'id':group+'_'+str(h),'kind':'window','style':style,
                     'width_m':width,'height_m':height,'sill_m':sill,'depth_m':.3,
                     'wall':wall.name})


for y in (-3.1,3.1): window(front,'Front','X',-4.5,y,'Arch')
for x in (-2.3,2.3):
    window(near,'CameraSide','Y',5,x,'Twin')
    window(far,'Far','Y',-5,x,'Twin')

gable_pts = [(-5,2.6),(5,2.6),(.6,6.25)]
gable_front = profile('Gable_Front',gable_pts,'X',-4.5,.24,'Plaster')
profile('Gable_Rear',gable_pts,'X',4.5,.24,'Plaster')
loft = [(.6 + .47*math.cos(i*math.tau/20),4.45 + .47*math.sin(i*math.tau/20))
        for i in range(20)]
cut(gable_front,profile('Temporary',loft,'X',-4.5,.9,'Plaster'))
profile('Glass_Loft',loft,'X',-4.5,.035,'Glass')
frame('Windows_Loft',loft,'X',-4.77,.15,.18)
beam('Windows_Loft',(-4.78,.6,3.98),(-4.78,.6,4.92),.08,.12,'Wood')
beam('Windows_Loft',(-4.78,.13,4.45),(-4.78,1.07,4.45),.08,.12,'Wood')
openings.append({'id':'loft_round','kind':'window','style':'Round','wall':'Gable_Front',
                 'width_m':.94,'height_m':.94,'sill_m':3.98,'depth_m':.24})


def roof(group,x0,x1,points,thickness=.18):
    # Each slope segment is a sealed solid, so there are no open single-sided shells.
    for (y0,z0),(y1,z1) in zip(points,points[1:]):
        verts=[(x,y,z+dz) for dz in (-thickness,0) for x,y,z in
               ((x0,y0,z0),(x1,y0,z0),(x1,y1,z1),(x0,y1,z1))]
        mesh(group,verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),
                          (1,2,6,5),(2,3,7,6),(3,0,4,7)],'Roof')


roof_profile=[(-5.55,2.68),(-4.85,2.9),(-2.7,4.42),(.6,6.4),
              (3.0,4.46),(4.85,2.9),(5.55,2.68)]
roof('Roof_Main',-4.95,4.95,roof_profile)
# Curved/flared eaves and substantial verge beams are readable at 25 metres.
for x in (-4.97,4.97):
    for a,b in zip(roof_profile,roof_profile[1:]):
        beam('Roof_Trim',(x,a[0],a[1]-.12),(x,b[0],b[1]-.12),.27,.24,'Wood')
for y,z in (roof_profile[0],roof_profile[-1]):
    beam('Roof_Trim',(-5.0,y,z-.12),(5.0,y,z-.12),.27,.30,'Wood')
beam('Roof_Trim',(-5.0,.6,6.26),(5.0,.6,6.26),.26,.28,'Wood')
roof('Roof_Porch',-3.7,.25,[(-6.35,2.08),(-6.02,2.20),(-4.95,2.78)],.17)
for x in (-3.7,.25):
    beam('Roof_Porch', (x,-6.35,1.99),(x,-4.95,2.69),.22,.2,'Wood')
beam('Timber_Porch',(-3.68,-6.16,2.04),(.2,-6.16,2.04),.25)
for x in (-3.45,.0):
    box('Timber_Porch',(x,-6.16,1.035),(.25,.25,2.07))
    box('Timber_Porch',(x,-6.16,.14),(.43,.43,.28),'Stone')
    beam('Timber_Porch',(x,-6.16,1.6),(x+.35 if x<0 else x-.35,-6.16,2.04),.15)
    beam('Timber_Porch',(x,-6.16,1.6),(x,-5.73,2.16),.15)
box('PorchFloor',(-1.675,-5.8,-.08),(3.55,1.7,.16),'Stone')

# Entrance hood: a real projecting secondary gable connected to the front wall.
roof('Roof_Entry',-5.0,-4.32,[(-1.55,2.69),(0,3.83),(1.55,2.69)],.16)
for a,b in zip([(-1.55,2.69),(0,3.83),(1.55,2.69)],[(0,3.83),(1.55,2.69)]):
    beam('Timber_Entry',(-5.0,a[0],a[1]-.10),(-5.0,b[0],b[1]-.10),.25)
beam('Timber_Entry',(-4.78,-1.43,2.47),(-4.78,1.43,2.47),.25)
for y in (-1.35,1.35):
    box('DoorFrame',(-4.76,y,1.16),(.30,.22,2.32),'Stone')
    box('DoorFrame',(-4.81,y,1.17),(.20,.17,2.34),'Wood')
    box('DoorFrame',(-4.76,y,.22),(.4,.3,.44),'Stone')
box('DoorFrame',(-4.76,0,2.46),(.3,2.92,.26),'Stone')
box('DoorFrame',(-4.88,0,2.48),(.12,2.56,.18),'Wood')
# Open leaf stays outside the +/-1.20 m passage. No door interaction/gameplay changes.
box('DoorLeaf',(-5.04,-1.39,1.12),(.96,.095,2.2),'Wood')
for z in (.37,1.83): box('DoorLeaf',(-5.04,-1.45,z),(.84,.035,.105),'Metal')
box('DoorLeaf',(-5.42,-1.46,1.06),(.06,.055,.14),'Metal')

# Bold frames: no diagonal strut is placed across a real window or doorway.
for x,group in ((-4.70,'Timber_Front'),(4.70,'Timber_Rear')):
    for y in (-4.88,-1.42,1.42,4.88):
        box(group,(x,y,1.31),(.25,.27,2.62))
    box(group,(x,0,2.55),(.27,10.16,.27))
    for y in (-3.2,3.2): box(group,(x,y,.64),(.23,3.16,.22))
    for y0,y1 in ((-4.75,-4.05),(4.75,4.05)):
        beam(group,(x,y0,.79),(x,y1,1.46),.22)
    for a,b in ((-5,.6),(.6,5)):
        za=2.6 if a!=-0 else 2.6
        beam(group,(x,a,2.65 if a in (-5,5) else 6.20),
                   (x,b,2.65 if b in (-5,5) else 6.20),.27)
    # Loft king post split around the round opening rather than cutting through it.
    if group=='Timber_Front':
        beam(group,(x,.6,2.75),(x,.6,3.80),.22)
        beam(group,(x,.6,5.10),(x,.6,6.18),.22)
    else: beam(group,(x,.6,2.75),(x,.6,6.18),.22)
    for y in (-3.45,3.55):
        z=2.6+(y+5)/5.6*3.65 if y<.6 else 2.6+(5-y)/4.4*3.65
        beam(group,(x,y,2.76),(x,y,z-.14),.20)
    beam(group,(x,-3.55,2.72),(x,-1.6,4.68),.22)
    beam(group,(x,3.6,2.72),(x,2.15,4.45),.22)
for y,group in ((5.20,'Timber_CameraSide'),(-5.20,'Timber_Far')):
    for x in (-4.25,0,4.25): box(group,(x,y,1.31),(.28,.25,2.62))
    for z in (.64,2.56): box(group,(0,y,z),(8.8,.24,.24))
    for x in (-3.93,3.93):
        beam(group,(x,y,.77),(x+(.66 if x<0 else -.66),y,1.47),.22)

# A modest irregular fieldstone base. Coarse blocks use shared stone texture;
# this is architectural massing, not an expensive detail/decoration pass.
rng=random.Random(870516)
def masonry(group,plane,line,spans,sill=0,rows=2,blockheight=.27):
    for row in range(rows):
        for start,end in spans:
            h=start
            while h<end-.05:
                width=min(rng.uniform(.46,.86),end-h)
                z=sill+(row+.5)*blockheight
                centre=(line,h+width/2,z) if plane=='X' else (h+width/2,line,z)
                dims=(.32,width-.022,blockheight-.018) if plane=='X' else (width-.022,.32,blockheight-.018)
                o=box(group,centre,dims,'Stone')
                for v in o.data.vertices:
                    v.co.z+=rng.uniform(-.012,.012)
                    if plane=='X': v.co.x+=rng.uniform(-.018,.018)
                    else: v.co.y+=rng.uniform(-.018,.018)
                h+=width
masonry('Stone_Front','X',-4.69,[(-5.04,-1.25),(1.25,5.04)])
masonry('Stone_CameraSide','Y',5.18,[(-4.35,4.35)])
masonry('Stone_Rear','X',4.68,[(-5.04,5.04)])
masonry('Stone_Far','Y',-5.18,[(-4.35,4.35)])

# Masonry chimney intersects the roof; a broad crown is a restrained silhouette.
box('Chimney',(2.8,-1.45,4.55),(.85,.90,4.70),'Stone')
for z in (5.15,5.55,5.95,6.35,6.75):
    box('Chimney',(2.8,-1.45,z),(.91,.96,.12),'Stone')
box('Chimney',(2.8,-1.45,6.86),(1.10,1.15,.18),'Stone')
box('ChimneyCap',(2.8,-1.45,6.98),(1.0,1.05,.08),'Metal')

# Interior architecture leaves the complete central diagonal walking area open.
for y in (-4.78,4.78):
    group='InteriorBeams_CameraSide' if y>0 else 'InteriorBeams'
    box(group,(0,y,2.44),(8.65,.24,.25))
    for x in (-3.8,0,3.8):
        box(group,(x,y,1.26),(.20,.18,2.52))
        beam(group,(x,y,2.08),(x+.36 if x<3 else x-.36,y,2.44),.16)
box('InteriorBeams',(4.27,0,2.44),(.24,9.5,.25))
box('InteriorStone',(4.28,0,.20),(.13,9.45,.40),'Stone')
# Counter retains the exact 173-cm leading edge and 92-cm top for V1 collision.
box('Counter',(2.2,-.8,.42),(.8,3.4,.84),'Wood')
box('Counter',(2.2,-.8,.88),(.94,3.5,.08),'Wood')
for y in (-2.39,-.8,.79): box('Counter',(1.793,y,.43),(.024,.08,.72),'Timber')
for z in (.12,.73): box('Counter',(1.795,-.8,z),(.022,3.26,.065),'Timber')

modules=[]
for group,parts in groups.items():
    if not parts: continue
    for obj in scene.objects: obj.select_set(False)
    for obj in parts: obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    if len(parts)>1: bpy.ops.object.join()
    obj=parts[0]
    obj.name='HH_V2_'+group
    # Thick walls/openings retain exact boundaries. Edges of timber/stone/roof
    # receive a restrained physical bevel; no shade-smoothing across broad walls.
    if group not in ('Floor','Foundation','PorchFloor') and not group.startswith(('Walls','Gable','Glass')):
        bevel=obj.modifiers.new('ArchitecturalEdgeSoftness','BEVEL')
        bevel.width=.015 if group.startswith('Windows') else .022
        bevel.segments=1
        bevel.affect='EDGES'
        bevel.use_clamp_overlap=True
        bpy.ops.object.modifier_apply(modifier=bevel.name)
    # Assign a stable world-oriented UV layout before handedness conversion.
    uv=obj.data.uv_layers.new(name='ArchitecturalUV')
    obj.data.update()
    for poly in obj.data.polygons:
        matname=obj.data.materials[poly.material_index].name.removeprefix('HH_V2_')
        scale={'Roof':(3.2,2.8),'Wood':(1.7,3.0),'Timber':(.8,3.0),
               'Stone':(1.8,1.8),'Plaster':(3,3),'Metal':(1,1),'Glass':(1.3,1.3)}[matname]
        axis=max(range(3),key=lambda a:abs(poly.normal[a]))
        axes=((1,2),(0,2),(0,1))[axis]
        for li in poly.loop_indices:
            co=obj.data.vertices[obj.data.loops[li].vertex_index].co
            uv.data[li].uv=(co[axes[0]]/scale[0],co[axes[1]]/scale[1])
    for v in obj.data.vertices: v.co.y*=-1
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    nonmanifold=sum(not e.is_manifold for e in bm.edges)
    volume=bm.calc_volume(signed=True)
    if nonmanifold or volume<=0: raise RuntimeError('Invalid closed module '+group)
    bm.to_mesh(obj.data);bm.free();obj.data.update()
    obj.data.calc_loop_triangles()
    coords=[v.co for v in obj.data.vertices]
    mins=[min(v[i] for v in coords) for i in range(3)]
    maxs=[max(v[i] for v in coords) for i in range(3)]
    modules.append({'name':obj.name,'triangles':len(obj.data.loop_triangles),
                    'non_manifold_edges':nonmanifold,'volume_m3':volume,
                    'unreal_bounds_min_m':[mins[0],-maxs[1],mins[2]],
                    'unreal_bounds_max_m':[maxs[0],-mins[1],maxs[2]],
                    'materials':[m.name for m in obj.data.materials]})

report={'source':str(SOURCE),'export':str(EXPORT),'module_count':len(modules),
        'total_triangles':sum(m['triangles'] for m in modules),'modules':modules,
        'openings':openings,'materials':list(materials),
        'functional_dimensions_m':{'main':[9.3,10.3],'ridge':6.4,
                                    'door':[2.4,2.3],'counter_height':.92},
        'production_camera':{'distance_cm':2500,'fov_degrees':35,'rotation':[-55,-45,0]},
        'reserved_interior_zones_unreal_m':{
            'treatment_beds':[[-1.5,-3.8],[1.0,-2.7]],
            'waiting': [[-2.8,2.5],[.5,4.4]],
            'shelves_and_herb_table':[[2.9,-4.4],[4.2,-2.8]]}}
if report['total_triangles']>45000: raise RuntimeError('Architecture exceeds 45k-triangle budget')
(REVIEW/'GeometryAudit.json').write_text(json.dumps(report,indent=2)+'\n')
for obj in scene.objects: obj.select_set(True)
bpy.context.view_layer.objects.active=next(iter(architecture.objects))
bpy.ops.export_scene.fbx(filepath=str(EXPORT),use_selection=True,object_types={'MESH'},
    global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',
    axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,
    use_triangles=True,mesh_smooth_type='FACE',use_custom_props=False)
# Pack our own textures so V2 remains a self-contained editable source.
for mat in materials.values():
    for node in mat.node_tree.nodes:
        if node.bl_idname=='ShaderNodeTexImage': node.image.pack()
bpy.data.libraries.write(str(SOURCE),{scene},fake_user=True,compress=True)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.shading.color_type='MATERIAL'
        area.spaces.active.overlay.show_overlays=False
        area.spaces.active.region_3d.view_location=Vector((0,-.3,2.5))
        area.spaces.active.region_3d.view_distance=22
        area.spaces.active.region_3d.view_rotation=Vector((-1,-1,1.4)).to_track_quat('Z','Y')
print(json.dumps({'source':str(SOURCE),'export':str(EXPORT),
                  'module_count':len(modules),'triangles':report['total_triangles']}))
# The same source also carries the three hidden, locally pivoted window prefabs.
import runpy
runpy.run_path(str(ROOT/'Tools/Blender/BuildHealingHouseV2WindowLibrary.py'))
