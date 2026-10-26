"""Read-only current species/learnset/binding and existing VisualV2 source inventory."""
import unreal,json,re,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2';out={'moves':[],'species':[],'npcs':[],'wild':[]}
def norm(s):return re.sub('[^A-Z0-9]','',s.upper())
for path in unreal.EditorAssetLibrary.list_assets('/Game/Data/Moves',True,False):
 m=unreal.load_asset(path)
 if isinstance(m,unreal.PokeMonsterMoveData):out['moves'].append({'path':m.get_path_name(),'id':str(m.internal_id),'name':str(m.display_name),'power':m.base_power,'accuracy':m.accuracy,'pp':m.max_pp,'type':str(m.type),'category':str(m.category)})
for path in unreal.EditorAssetLibrary.list_assets('/Game/Data/Creatures',True,False):
 s=unreal.load_asset(path)
 if not isinstance(s,unreal.PokeMonsterCreatureSpeciesData):continue
 rows=[]
 for x in s.level_up_moves:
  missing=str(x.unavailable_move_name);rows.append({'level':x.level,'move':x.move.get_path_name()if x.move else None,'unavailable':missing,'reason':str(x.unavailable_reason),'existing_candidates':[m for m in out['moves']if norm(m['id'])==norm(missing)]if not x.move else[]})
 out['species'].append({'path':s.get_path_name(),'id':str(s.get_internal_id()),'dex':s.get_pokedex_number(),'start_level':s.get_starting_level(),'learnset':rows})
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterNPC):out['npcs'].append({'name':a.get_actor_label(),'position':a.get_actor_location().to_tuple(),'display':str(a.display_name)})
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):out['wild'].append({'name':a.get_actor_label(),'position':a.get_actor_location().to_tuple(),'species':str(a.visual_species),'encounter':str(a.encounter_id)})
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
p=D/'OriginalScene.json';assert not p.exists();p.write_text(json.dumps(scene(W),indent=2));out['controller_backend']=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');out['missing_entries']=[{'species':s['id'],**x}for s in out['species']for x in s['learnset']if not x['move']];assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'AssetAudit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));unreal.log('PRAXIS_READONLY_INVENTORY '+str(len(out['species']))+' species, '+str(len(out['missing_entries']))+' unbound entries')
