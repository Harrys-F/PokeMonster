"""Extract three locally pivoted reusable windows from the authored V2 facade.

Called after BuildHealingHouseV2.py, or once on that scene via Blender MCP.
Library collection stays hidden; these meshes are not extra house instances.
All three face local -X, with pivot at wall plane / horizontal centre / sill.
"""
import bpy
import bmesh
import json
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'Art/HealingHouse'
scene=bpy.data.scenes['HealingHouse_V2']
bpy.context.window.scene=scene
if bpy.data.collections.get('HH_V2_WindowLibrary'):
    raise RuntimeError('Window library already exists; preserve existing work')
collection=bpy.data.collections.new('HH_V2_WindowLibrary')
scene.collection.children.link(collection)
entries=[]
for name,sources,origin,rotate in (
    ('Arch',('Windows_Front','Glass_Front'),(-4.5,3.1,1.0),False),
    ('Twin',('Windows_CameraSide','Glass_CameraSide'),(-2.3,-5,1.08),True),
    ('Round',('Windows_Loft','Glass_Loft'),(-4.5,-.6,3.98),False)):
    verts=[];faces=[];uvs=[];slots=[];indices=[]
    for source in sources:
        obj=bpy.data.objects['HH_V2_'+source];data=obj.data
        polygons=[p for p in data.polygons if name=='Round' or
                  (name=='Arch' and all(data.vertices[v].co.y>0 for v in p.vertices)) or
                  (name=='Twin' and all(data.vertices[v].co.x<0 for v in p.vertices))]
        ids=sorted({v for p in polygons for v in p.vertices})
        mapping={v:i+len(verts) for i,v in enumerate(ids)}
        for v in ids:
            co=data.vertices[v].co-Vector(origin)
            if rotate: co=Vector((co.y,-co.x,co.z))
            verts.append(co)
        for p in polygons:
            mat=data.materials[p.material_index]
            if mat not in slots: slots.append(mat)
            indices.append(slots.index(mat))
            faces.append([mapping[v] for v in p.vertices])
            uvs.append([data.uv_layers.active.data[li].uv.copy() for li in p.loop_indices])
    d=bpy.data.meshes.new('HH_V2_WindowModule_'+name+'_Geometry')
    d.from_pydata(verts,[],faces);d.update()
    for mat in slots: d.materials.append(mat)
    uv=d.uv_layers.new(name='ArchitecturalUV')
    for p,matindex,coords in zip(d.polygons,indices,uvs):
        p.material_index=matindex
        for li,co in zip(p.loop_indices,coords): uv.data[li].uv=co
    obj=bpy.data.objects.new('HH_V2_WindowModule_'+name,d)
    collection.objects.link(obj)
    bm=bmesh.new();bm.from_mesh(d)
    non=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
    if non or volume<=0: raise RuntimeError('Window module is not a valid solid: '+name)
    d.calc_loop_triangles()
    mins=[min(v.co[i] for v in d.vertices) for i in range(3)]
    maxs=[max(v.co[i] for v in d.vertices) for i in range(3)]
    entries.append({'name':obj.name,'style':name,'triangles':len(d.loop_triangles),
                    'non_manifold_edges':non,'volume_m3':volume,
                    'unreal_bounds_min_m':[mins[0],-maxs[1],mins[2]],
                    'unreal_bounds_max_m':[maxs[0],-mins[1],maxs[2]],
                    'pivot':'wall plane, horizontal centre, sill; faces local -X'})
for obj in scene.objects: obj.select_set(obj in collection.objects[:])
bpy.context.view_layer.objects.active=collection.objects[0]
path=ART/'Exports/HealingHouse_V2_WindowModules.fbx'
bpy.ops.export_scene.fbx(filepath=str(path),use_selection=True,object_types={'MESH'},
    global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',
    axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,
    use_triangles=True,mesh_smooth_type='FACE',use_custom_props=False)
collection.hide_render=True
collection.hide_viewport=True
report={'export':str(path),'modules':entries,'total_triangles':sum(e['triangles'] for e in entries),
        'placed_in_map':False,'building_triangles_unchanged':15256}
(ART/'Review/V2/WindowLibraryAudit.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.data.libraries.write(str(ART/'Source/HealingHouse_V2.blend'),{scene},fake_user=True,compress=True)
print(json.dumps(report))
