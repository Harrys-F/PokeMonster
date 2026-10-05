"""Read-only asset, placement and collision audit. Evidence stays in Saved/.
Optional Saved/HealingQualityV2/BeforeMap.json checks the original scene exactly.
"""
import unreal,json,math,runpy,re
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/HealingQualityV2';OUT.mkdir(parents=True,exist_ok=True)
runpy.run_path(str(ROOT/'Tools/ValidateHealingHouseExpandedInterior.py'))
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();by={a.get_actor_label():a for a in actors};cut=by['HouseCutaway']
def vec(v):return [v.x,v.y,v.z]
def normalized(s):return re.sub(r' \(0x[0-9a-fA-F]+\)','',str(s))
def box(a):
 o,e=a.get_actor_bounds(False);return ([o.x-e.x,o.y-e.y,o.z-e.z],[o.x+e.x,o.y+e.y,o.z+e.z])
def overlap(a,b):return all(min(a[1][i],b[1][i])-max(a[0][i],b[0][i])>.1 for i in range(3))
missing=[];collision_changed=[];furniture=[]
architecture=[a for n,a in by.items() if n.startswith(('HH_Expanded_Side','HH_Expanded_Rear'))]
for n in ['HH_V3_HerbShelf','HH_Art_RearApothecary_0','HH_Art_RearApothecary_1']:
 b=box(by[n]);intersections=[a.get_actor_label() for a in architecture if overlap(b,box(a))];assert not intersections,(n,intersections);furniture.append({'actor':n,'position_cm':vec(by[n].get_actor_location()),'bounds_cm':b,'architecture_intersections':intersections})
for a in actors:
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh:missing.append(a.get_actor_label()+': mesh')
  for i,m in enumerate(c.get_materials()):
   if not m:missing.append(a.get_actor_label()+': material '+str(i))
assert not missing,missing
components=by['HH_Q2_GrassInstances'].get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert len(components)==6
hism=[];catalog=json.loads((ROOT/'Art/HealingHouse/QualityV2/Props.json').read_text());instance_triangles=0
for c in components:
 name=c.static_mesh.get_name().removeprefix('SM_WL_NG_');count=c.get_instance_count();assert count>0
 assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.get_editor_property('cast_shadow')
 assert c.get_editor_property('instance_start_cull_distance')==3200 and c.get_editor_property('instance_end_cull_distance')==4300
 instance_triangles+=count*catalog[name]['triangles'];hism.append({'mesh':c.static_mesh.get_path_name(),'instances':count,'triangles_per_mesh':catalog[name]['triangles'],'collision':'NoCollision','cull_cm':[3200,4300]})
assert sum(i['instances'] for i in hism)==321
assets=[];textures=[];mesh_editor=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for base in ['/Game/Environment/HealingHouse/QualityV2','/Game/Environment/Westland/NaturalGroundV1']:
 for path in unreal.EditorAssetLibrary.list_assets(base,True,False):
  obj=unreal.load_asset(path);assert obj,path;assets.append(path)
  if isinstance(obj,unreal.StaticMesh):
   assert all(s.get_editor_property('material_interface') for s in obj.get_editor_property('static_materials')),path
   assert mesh_editor.get_number_verts(obj,0)>0,path
   if obj.get_name().startswith('SM_WL_NG_'):assert mesh_editor.get_simple_collision_count(obj)==0,path
  elif isinstance(obj,unreal.Material):
   lib=unreal.MaterialEditingLibrary
   for expression in lib.get_material_expressions(obj):
    if isinstance(expression,unreal.MaterialExpressionTextureSample):
     inputs=lib.get_inputs_for_material_expression(obj,expression);assert inputs and inputs[0],path+': missing UV input'
    if isinstance(expression,unreal.MaterialExpressionCustom):
     assert all(lib.get_inputs_for_material_expression(obj,expression)),path+': missing Custom input'
    if isinstance(expression,unreal.MaterialExpressionDesaturation):
     assert lib.get_inputs_for_material_expression(obj,expression)[0],path+': missing desaturation input'
  elif isinstance(obj,unreal.Texture2D):
   assert obj.get_editor_property('srgb') and obj.get_editor_property('max_texture_size')==1024
   assert obj.get_editor_property('power_of_two_mode')==unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO
   assert not obj.get_editor_property('never_stream');textures.append({'asset':path,'runtime_max_dimension':1024,'mips':'power-of-two stretch/default generation','streaming':True})
assert len(assets)==36 and len(textures)==6,(len(assets),len(textures))
sm=by['HH_Q2_OrganicApproach'].static_mesh_component.static_mesh;dm=unreal.DynamicMesh();dm,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(sm,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert result==unreal.GeometryScriptOutcomePins.SUCCESS
assert dm.get_triangle_count()==1152;normal,valid=dm.get_triangle_face_normal(0);assert valid and normal.z>.99
uv=unreal.GeometryScript_UVs.get_mesh_uv_size_info(dm,0,unreal.GeometryScriptMeshSelection());assert uv[-2] and not uv[-1] and uv[2]>.99
assert by['HH_Q2_OrganicApproach'].static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
baseline_file=OUT/'BeforeMap.json';baseline_checks=False
if baseline_file.exists():
 baseline=json.loads(baseline_file.read_text());assert all(a['name'] in by for a in baseline)
 previous=next(a for a in baseline if a['name']=='HouseCutaway');assert [a.get_actor_label() for a in cut.get_editor_property('occluding_actors')]==previous['occluders']
 for key in ['interior_camera_distance','interior_camera_pitch','interior_camera_yaw_offset','interior_camera_target','use_interior_camera','use_relocated_interior','fade_duration']:assert normalized(cut.get_editor_property(key))==normalized(previous[key]),key
 for a in baseline:
  current=by[a['name']]
  if 'collision' in a:
   c=current.static_mesh_component
   if str(c.get_collision_enabled())!=a['collision'] or str(c.get_collision_profile_name())!=a['profile']:collision_changed.append(a['name'])
  if (a['position'][0]<19400 or a['position'][0]>20700) and a['name'] not in ('Ground','Forecourt','ApproachPath'):
   assert vec(current.get_actor_location())==a['position'] and vec(current.get_actor_scale3d())==a['scale'],a['name']
   assert normalized(current.get_actor_rotation())==normalized(a['rotation']),a['name']
   assert current.get_editor_property('hidden')==a['hidden'],a['name']
   if 'mesh' in a:
    assert current.static_mesh_component.static_mesh.get_path_name()==a['mesh'],a['name']
    assert [m.get_path_name() for m in current.static_mesh_component.get_materials()]==a['materials'],a['name']
 assert not collision_changed,collision_changed;baseline_checks=True
report={'passed':True,'map':w.get_path_name(),'actor_count':len(actors),'furniture_clearance':furniture,'missing_assets':missing,'original_collision_profiles_unchanged':not collision_changed,'baseline_compared':baseline_checks,'occluder_count':len(cut.get_editor_property('occluding_actors')),'textures':textures,'new_assets':assets,'hism':hism,'vegetation_instance_triangles':instance_triangles,'path_triangles':1152,'upward_normal':vec(normal),'complete_path_uvs':True}
(OUT/'QualityAudit.json').write_text(json.dumps(report,indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.log('HEALING_QUALITY_V2_AUDIT_PASSED')
