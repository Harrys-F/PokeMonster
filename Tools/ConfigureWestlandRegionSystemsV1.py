import unreal,runpy,sys
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'));import WestlandRegionLayout as L
A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert w.get_name()=='Dev_WestlandRegion'
for i,(speaker,texts) in enumerate([('Wanderer',['Willkommen in Westland. Der Weg durch die Obstwiese führt zum Dorf.','Vom Brunnen erreichst du das Heilhaus im Norden. Über die Steinbrücke liegen die Wildwiesen.']),('Dorfbewohner',['Am Brunnen treffen sich die Wege. Das Gasthaus liegt gleich östlich davon.','Der Nordweg führt zum Heilhaus und zum Steinkreis. Die Mühlenrunde bringt dich am Fluss zurück zum Hof.']),('Archivarin',['Diese alten Steine stehen hoch über dem Dorf.','Jenseits der Brücke liegt eine Ruinenlichtung am Waldrand. Die Nebenpfade führen wieder zu den Wiesen zurück.'])]):
 path=L.ASSETS+'/Data/DA_WR_Dialogue_'+str(i);d=unreal.load_asset(path)
 if not d:
  f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',unreal.PokeMonsterDialogueData);d=unreal.AssetToolsHelpers.get_asset_tools().create_asset(path.rsplit('/',1)[1],path.rsplit('/',1)[0],unreal.PokeMonsterDialogueData,f)
 pages=[]
 for t in texts:
  p=unreal.PokeMonsterDialoguePage();p.speaker_name=speaker;p.text=t;pages.append(p)
 d.set_editor_property('pages',pages);unreal.EditorAssetLibrary.save_loaded_asset(d,False)
 a=next(a for a in A.get_all_level_actors() if a.get_actor_label()=='WR_NPC_'+str(i));a.set_editor_property('dialogue',d)
healer=next(a for a in A.get_all_level_actors() if a.get_actor_label()=='HouseHealer');healer.set_editor_property('checkpoint_id','WestlandRegion_HealingHouse')
for name in ['Crag','StandingStone','RuinColumn','RuinArch']:
 sm=unreal.load_asset(L.ASSETS+'/Meshes/WR_'+name);sm.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).enable_section_collision(sm,True,0,0);unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
for a in A.get_all_level_actors():
 cs=a.get_components_by_class(unreal.StaticMeshComponent)
 for c in cs:
  sm=c.get_editor_property('static_mesh')
  if sm and sm.get_path_name().rsplit('.',1)[1] in ['WR_Crag','WR_StandingStone','WR_RuinColumn','WR_RuinArch']:
   c.set_collision_profile_name('BlockAll');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
unreal.EditorLoadingAndSavingUtils.save_map(w,L.MAP);unreal.log('REGION_SYSTEM_CONFIG_DONE')
