"""Read-only V3 import/material/collision/frozen-setting audit.
Run with the saved Healing House map outside PIE. Evidence stays in Saved/.
The optional BeforeMap.json is a capture of the original V2 scene.
"""
import unreal,json,runpy,re,math
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/HealingQualityV3'
OUT.mkdir(parents=True,exist_ok=True)
runpy.run_path(str(ROOT/'Tools/ValidateHealingHouseExpandedInterior.py'))
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
by={a.get_actor_label():a for a in actors};cut=by['HouseCutaway']
lib=unreal.MaterialEditingLibrary;sm_editor=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
def vec(v):return [v.x,v.y,v.z]
def normalized(s):return re.sub(r' \(0x[0-9a-fA-F]+\)','',str(s))
missing=[];new_assets=[];mesh_counts={};mesh_triangles={};shader_count=0
for a in actors:
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh:missing.append(a.get_actor_label()+': mesh')
  if not all(c.get_materials()):missing.append(a.get_actor_label()+': material')
  if a.get_actor_label().startswith('HH_Q3_'):
   assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION,a.get_actor_label()
assert not missing,missing
def box(a):
 o,e=a.get_actor_bounds(False);return ([o.x-e.x,o.y-e.y,o.z-e.z],[o.x+e.x,o.y+e.y,o.z+e.z])
def overlaps(a,b):return all(min(a[1][i],b[1][i])-max(a[0][i],b[0][i])>.1 for i in range(3))
architecture=[a for n,a in by.items() if n.startswith(('HH_Expanded_Side','HH_Expanded_Rear'))]
for n in ['HH_Q3_Visual_HH_V3_HerbShelf','HH_Q3_Visual_HH_Art_RearApothecary_0','HH_Q3_Visual_HH_Art_RearApothecary_1']:
 collisions=[a.get_actor_label() for a in architecture if overlaps(box(by[n]),box(a))]
 assert not collisions,(n,collisions)
catalog=json.loads((ROOT/'Art/HealingHouse/QualityV3/Props.json').read_text())
for path in unreal.EditorAssetLibrary.list_assets('/Game/Environment/HealingHouse/QualityV3',True,False):
 o=unreal.load_asset(path);assert o,path;new_assets.append(path)
 if isinstance(o,unreal.StaticMesh):
  assert all(s.get_editor_property('material_interface') for s in o.get_editor_property('static_materials')),path
  assert sm_editor.get_number_verts(o,0)>0 and sm_editor.get_simple_collision_count(o)==0,path
  mesh_counts[o.get_name()]=sm_editor.get_number_verts(o,0)
  dm=unreal.DynamicMesh()
  dm,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(o,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD())
  assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS,path
  count=dm.get_triangle_count();key=o.get_name().removeprefix('SM_HH_Q3_')
  assert count==catalog[key]['triangles'],(key,count,catalog[key]['triangles'])
  bounds=o.get_bounding_box();size=bounds.max-bounds.min
  assert all(abs(x-y)<.02 for x,y in zip(vec(size),catalog[key]['size_cm'])),(key,vec(size),catalog[key]['size_cm'])
  mesh_triangles[o.get_name()]=count
 elif isinstance(o,unreal.Texture2D):
  assert o.get_editor_property('srgb') and o.get_editor_property('max_texture_size')==1024
  assert not o.get_editor_property('never_stream')
 elif isinstance(o,unreal.Material):
  nodes=lib.get_material_expressions(o)
  if 'Fade_' in o.get_name() or any(k in o.get_name() for k in ['Leaf','Flower']):
   assert o.get_editor_property('blend_mode')==unreal.BlendMode.BLEND_MASKED,path
   assert any(isinstance(x,unreal.MaterialExpressionScalarParameter) and str(x.get_editor_property('parameter_name'))=='HouseCutaway' for x in nodes),path
  for x in nodes:
   if isinstance(x,unreal.MaterialExpressionTextureSample):
    assert x.get_editor_property('texture') and lib.get_inputs_for_material_expression(o,x)[0],path
assert len(mesh_counts)==len(catalog)==34
assert len(new_assets)==51,len(new_assets)
for name in ['Grass','Earth','PathBlend','ForecourtBlend']:
 o=unreal.load_asset('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_'+name)
 custom=[n for n in lib.get_material_expressions(o) if isinstance(n,unreal.MaterialExpressionCustom)]
 assert len(custom)==1 and all(lib.get_inputs_for_material_expression(o,custom[0]))
 assert custom[0].get_editor_property('code').count('Texture2DSample')==5
 shader_count+=1
components=by['HH_Q2_GrassInstances'].get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
assert len(components)==6 and sum(c.get_instance_count() for c in components)==321
for c in components:
 assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
 assert not c.get_editor_property('cast_shadow')
 assert c.get_editor_property('instance_end_cull_distance')==4300
baseline_checks=False;changed_visuals=[]
if (OUT/'BeforeMap.json').exists():
 baseline=json.loads((OUT/'BeforeMap.json').read_text())
 assert all(a['name'] in by for a in baseline)
 oldcut=next(a for a in baseline if a['name']=='HouseCutaway')
 occ=[a.get_actor_label() for a in cut.get_editor_property('occluding_actors')]
 assert occ[:len(oldcut['occluders'])]==oldcut['occluders']
 assert all(n.startswith(('HH_Q3_WindowBox_','HH_Q3_WindowHerb_','HH_Q3_EntranceHerb_')) for n in occ[len(oldcut['occluders']):])
 for key in oldcut:
  if key not in ['name','class','position','rotation','scale','hidden','occluders']:
   assert normalized(cut.get_editor_property(key))==normalized(oldcut[key]),key
 for old in baseline:
  a=by[old['name']]
  if a.get_actor_label().startswith('HH_Art_Light_'):continue
  expected={'HH_Art_FloorHerb_1':[19620,480,1],'HH_Art_FloorHerb_2':[20380,410,1]}.get(old['name'],old['position'])
  assert vec(a.get_actor_location())==expected,old['name']
  assert vec(a.get_actor_scale3d())==([.85,.85,.85] if old['name']=='HH_Art_FloorHerb_1' else old['scale']),old['name']
  assert normalized(a.get_actor_rotation())==normalized(old['rotation']),old['name']
  if 'collision' in old:
   c=a.static_mesh_component
   assert str(c.get_collision_enabled())==old['collision'] and str(c.get_collision_profile_name())==old['profile'],old['name']
   if old['collision']!=str(unreal.CollisionEnabled.NO_COLLISION):
    assert c.static_mesh.get_path_name()==old['mesh'],old['name']+': original collider changed'
   if c.static_mesh.get_path_name()!=old['mesh']:changed_visuals.append(old['name'])
 baseline_checks=True
record={'passed':True,'map':world.get_path_name(),'actor_count':len(actors),'missing_assets':missing,
        'new_assets':new_assets,'mesh_vertex_counts':mesh_counts,'library_triangles':sum(x['triangles'] for x in catalog.values()),
        'imported_triangles':mesh_triangles,'visible_q3_instance_triangles':sum(mesh_triangles.get(a.static_mesh_component.static_mesh.get_name(),0) for a in actors if isinstance(a,unreal.StaticMeshActor) and not a.get_editor_property('hidden') and a.static_mesh_component.is_visible()),
        'anti_tiling_materials':shader_count,'max_ground_texture_fetches':5,'grass_instances':321,
        'baseline_compared':baseline_checks,'original_collision_preserved':True,'changed_visuals':changed_visuals,
        'occluders':[a.get_actor_label() for a in cut.get_editor_property('occluding_actors')]}
(OUT/'QualityAudit.json').write_text(json.dumps(record,indent=2)+'\n')
unreal.SystemLibrary.execute_console_command(world,'MAP CHECK')
unreal.log('HEALING_QUALITY_V3_AUDIT_PASSED')
