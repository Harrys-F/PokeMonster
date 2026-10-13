"""Read-only validation of the saved VisualV2 map and its dependencies."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/DevTestMapVisualV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=list(A.get_all_level_actors());by={a.get_actor_label():a for a in actors};old=json.loads((O/'InitialActors.json').read_text());checks=[]
for entry in old['actors']:
 if 'PokeMonster' in entry['class'] or entry['class'].endswith('.PlayerStart'):
  a=by[entry['label']];assert (a.get_actor_location()-unreal.Vector(*entry['location'])).length()<.001;checks.append(entry['label'])
occ=[];hism=[];npc=[]
for a in actors:
 if isinstance(a,unreal.PokeMonsterBuildingCutaway):
  os=list(a.get_editor_property('occluding_actors'));assert os and all(x.get_world()==w for x in os);occ.append({'label':a.get_actor_label(),'count':len(os),'fade_s':a.get_editor_property('fade_duration'),'actors':[x.get_actor_label() for x in os]})
 for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):hism.append({'label':a.get_actor_label(),'instances':c.get_instance_count(),'mesh':c.get_editor_property('static_mesh').get_path_name(),'collision':str(c.get_collision_enabled()),'shadow':c.get_editor_property('cast_shadow'),'mobility':str(c.mobility),'cull_cm':[c.get_editor_property('instance_start_cull_distance'),c.get_editor_property('instance_end_cull_distance')]})
 if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterTrainerNPC,unreal.PokeMonsterRestPoint)):
  for c in a.get_components_by_class(unreal.PaperSpriteComponent):
   s=c.get_sprite();npc.append({'label':a.get_actor_label(),'sprite':s.get_path_name() if s else None,'scale':c.get_editor_property('relative_scale3d').to_tuple(),'source_dimension':str(s.get_editor_property('source_dimension')) if s else None,'ppu':s.get_editor_property('pixels_per_unreal_unit') if s else None})
base=json.loads((O/'Baseline.json').read_text());changed=[p for p,h in base['files'].items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not changed,changed
out={'map':w.get_path_name(),'actors':len(actors),'original_gameplay_positions_preserved':checks,'cutaway':occ,'hism':hism,'npc':npc,'baseline_changed':changed,'dirty_maps':[str(p.get_path_name()) for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[str(p.get_path_name()) for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
(O/'FinalAudit.json').write_text(json.dumps(out,indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
