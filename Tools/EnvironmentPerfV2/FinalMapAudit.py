"""Read-only baseline comparison; no save or mutation of original actors/assets."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV2'
baseline=unreal.load_asset('/Game/Maps/Dev_TestMap_EnvironmentPerfV1')
def transform(t):
 return {'translation':t.translation.to_tuple(),'rotation':(t.rotation.x,t.rotation.y,t.rotation.z,t.rotation.w),'scale':t.scale3d.to_tuple()}
def snap(world):
 out={}
 for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
  if a.get_actor_label()=='WorldSettings' or a.get_class().get_path_name() in ['/Script/Water.BuoyancyManager','/Script/GameplayDebugger.GameplayDebuggerPlayerManager','/Script/NavigationSystem.AbstractNavData']:continue
  row={'class':a.get_class().get_path_name(),'position':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple(),'scale':a.get_actor_scale3d().to_tuple(),'components':[]}
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   row['components'].append({'name':c.get_name(),'mesh':c.static_mesh.get_path_name() if c.static_mesh else None,'transform':transform(c.get_world_transform()),'collision':str(c.get_collision_enabled()),'shadow':c.get_editor_property('cast_shadow'),'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],'instances':[transform(c.get_instance_transform(i,False)) for i in range(c.get_instance_count())] if isinstance(c,unreal.InstancedStaticMeshComponent) else []})
  out[a.get_actor_label()]=row
 return out
b=snap(baseline);a=snap(w);new={k:v for k,v in a.items() if k not in b};missing=sorted(set(b)-set(a));diff={k:{'before':b[k],'after':a[k]} for k in set(a)&set(b) if a[k]!=b[k]}
out={'map':w.get_path_name(),'baseline':baseline.get_path_name(),'actor_count':len(a),'baseline_actor_count':len(b),'new_actors':new,'missing_actors':missing,'existing_actor_transform_geometry_material_collision_differences':diff,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
profiles=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterEnvironmentRenderProfileV2);assert len(profiles)==1;out['persisted_renderer_overrides']=dict(profiles[0].get_editor_property('renderer_overrides'));assert out['persisted_renderer_overrides']==json.loads((O/'SelectedCandidate.json').read_text())['renderer_overrides']
(O/'FinalMapAudit.json').write_text(json.dumps(out,indent=2));assert not missing and not diff,(missing,list(diff));assert len(new)==1 and next(iter(new.values()))['class'].endswith('PokeMonsterEnvironmentRenderProfileV2'),new
unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.log('ENVIRONMENT_PERF_FINAL_MAP_CHECK_REQUESTED')
