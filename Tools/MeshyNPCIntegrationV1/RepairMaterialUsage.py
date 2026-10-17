import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();I=R/'Art/Characters/NPCs/IntegrationV1';L=unreal.MaterialEditingLibrary;master=unreal.load_asset('/Game/Characters/NPCs/Shared/Materials/M_NPC_MeshyBase_V1');master.set_editor_property('used_with_skeletal_mesh',True);L.recompile_material(master);unreal.EditorAssetLibrary.save_loaded_asset(master,False);out=[]
for id in ['Ranger','WhiteHairedWarrior','ElvenArcher','DwarfWarrior','SilverLady','TreeBeing','ElvenScholar','Wizard','DarkArmored','CrouchedCreature']:
 mi=unreal.load_asset('/Game/Characters/NPCs/'+id+'/Materials/MI_'+id+'_V1');L.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi,False);out.append({'id':id,'material':mi.get_path_name(),'updated':True})
(I/'MaterialUsageRepair.json').write_text(json.dumps({'skeletal_usage':master.get_editor_property('used_with_skeletal_mesh'),'instances':out},indent=2))
