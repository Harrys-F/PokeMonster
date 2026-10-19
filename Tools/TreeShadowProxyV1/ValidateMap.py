"""Read-only audit against original VisualV2, plus Map Check of new test map."""

# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_TreeShadowProxyV1'
def transform(t):return {'translation':t.translation.to_tuple(),'rotation':(t.rotation.x,t.rotation.y,t.rotation.z,t.rotation.w),'scale':t.scale3d.to_tuple()}
def snap(world):
 out={}
 for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
  if a.get_actor_label()=='WorldSettings' or a.get_class().get_path_name() in ['/Script/Water.BuoyancyManager','/Script/GameplayDebugger.GameplayDebuggerPlayerManager','/Script/NavigationSystem.AbstractNavData']:continue
  row={'class':a.get_class().get_path_name(),'position':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple(),'scale':a.get_actor_scale3d().to_tuple(),'components':[]}
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   row['components'].append({'mesh':c.static_mesh.get_path_name() if c.static_mesh else None,'transform':transform(c.get_world_transform()),'shadow':bool(c.cast_shadow),'collision':str(c.get_collision_enabled()),'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],'instances':[transform(c.get_instance_transform(i,False)) for i in range(c.get_instance_count())] if isinstance(c,unreal.InstancedStaticMeshComponent) else []})
  out[a.get_actor_label()]=row
 return out
b=snap(unreal.load_asset('/Game/Maps/Dev_TestMap_VisualV2'));a=snap(w);new={k:v for k,v in a.items() if k not in b};missing=sorted(set(b)-set(a));diff={k:{'before':b[k],'after':a[k]} for k in set(a)&set(b) if a[k]!=b[k]}
assert not missing;assert set(diff)=={'V2_ForestOak_'+str(i) for i in range(3)}
for name in diff:
 before=diff[name]['before'];after=diff[name]['after'];assert before['components'][0]['shadow'] and not after['components'][0]['shadow'];after['components'][0]['shadow']=True;assert before==after;after['components'][0]['shadow']=False
assert len(new)==6 and all(k.startswith('TSP_') for k in new)
bark_positions=[]
for asset,strip in [('/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3',True),('/Game/Environment/TreeShadowProxyV1/SM_TSP_OakAncient_Bark',False)]:
 dm=unreal.DynamicMesh();dm,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(unreal.load_asset(asset),dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 if strip:unreal.GeometryScript_Materials.delete_triangles_by_material_id(dm,1)
 _,positions,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);vs=unreal.GeometryScript_List.convert_vector_list_to_array(positions)
 bark_positions.append([p.to_tuple() for p in vs])
buckets={}
for p in bark_positions[0]:buckets.setdefault(tuple(math.floor(x/.01) for x in p),[]).append(p)
errors=[]
for p in bark_positions[1]:
 key=tuple(math.floor(x/.01) for x in p);near=[]
 for dx in [-1,0,1]:
  for dy in [-1,0,1]:
   for dz in [-1,0,1]:near+=buckets.get((key[0]+dx,key[1]+dy,key[2]+dz),[])
 assert near,'Imported bark position mismatch'
 errors.append(min(math.sqrt(sum((x-y)**2 for x,y in zip(p,q))) for q in near))
bark_match={'original_vertices':len(bark_positions[0]),'proxy_vertices':len(bark_positions[1]),'max_nearest_position_error_cm':max(errors),'matching_to_0_001cm':max(errors)<.001}
assert bark_match['matching_to_0_001cm']
wind=[]
for name in diff:
 tree=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if x.get_actor_label()==name)
 for j in range(tree.static_mesh_component.get_num_materials()):
  m=tree.static_mesh_component.get_material(j).get_base_material();node=unreal.MaterialEditingLibrary.get_material_property_input_node(m,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET);wind.append({'tree':name,'material':m.get_path_name(),'world_position_offset_connected':node is not None,'input_class':node.get_class().get_name() if node else None})
(O/'MapValidation.json').write_text(json.dumps({'new_actors':new,'missing_actors':missing,'changed_actors':diff,'wind':wind,'bark_match':bark_match,'original_visual_geometry_materials_transforms_collisions_equal':True,'dirty_maps':[str(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[str(x) for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]},indent=2))
unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.log('TREE_SHADOW_MAP_CHECK_REQUESTED')
