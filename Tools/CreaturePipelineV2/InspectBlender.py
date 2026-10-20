"""Background Blender only; inspect existing source without saving it or generating a model.
blender --background --python InspectBlender.py -- PROJECT_RELATIVE_SOURCE SAVED_REPORT
"""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];args=sys.argv[sys.argv.index('--')+1:];assert len(args)==2
source=(R/args[0]).resolve();out=(R/args[1]).resolve()
assert source.is_relative_to(R) and source.is_file();assert out.is_relative_to(R/'Saved') and not out.exists()
sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert bpy.app.background,'Never replace a live Blender session'
if source.suffix.lower()=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source))
elif source.suffix.lower()=='.glb':
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete();bpy.ops.import_scene.gltf(filepath=str(source))
else:raise ValueError('Inspect actual GLB input or preserved Blender source only')
for a in bpy.data.objects:
 if a.type=='ARMATURE':a.data.pose_position='REST'
bpy.context.view_layer.update();meshes=[]
for obj in bpy.data.objects:
 if obj.type!='MESH':continue
 obj.data.calc_loop_triangles();points=[obj.matrix_world@Vector(p) for p in obj.bound_box]
 meshes.append({'name':obj.name,'vertices':len(obj.data.vertices),'triangles':len(obj.data.loop_triangles),'uv_layers':len(obj.data.uv_layers),'materials':[s.material.name if s.material else None for s in obj.material_slots],'negative_transform':obj.matrix_world.determinant()<0,'world_z_extent_m':(max(p.z for p in points)-min(p.z for p in points))*bpy.context.scene.unit_settings.scale_length,'world_y_extent_m':(max(p.y for p in points)-min(p.y for p in points))*bpy.context.scene.unit_settings.scale_length})
result={'source':str(source.relative_to(R)),'source_sha256':sha,'meshes':meshes,'rigs':[{'name':o.name,'bones':len(o.data.bones)} for o in bpy.data.objects if o.type=='ARMATURE'],'actions':[a.name for a in bpy.data.actions],'textures':[{'name':i.name,'resolution':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images if i.type=='IMAGE'],'unit_scale_length':bpy.context.scene.unit_settings.scale_length,'forward_confirmed_by_human':False,'size_basis':None,'measured_size_m':None,'note':'Per-object bounds only; exclude effects and choose reference measurement explicitly before planning. No file saved/repaired.'}
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2));print('READ_ONLY_BLENDER_INSPECTION',len(meshes),sum(m['triangles'] for m in meshes))
