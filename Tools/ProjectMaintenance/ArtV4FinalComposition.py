"""Final production-camera composition: uncover real fireplace and vary shrub heights without removal."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();moves=[];hearth=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 label=a.get_actor_label();p=a.get_actor_location()
 if label.startswith('ArtV4_Hearth'):
  a.set_actor_location(unreal.Vector(17342,60,0),False,True);hearth.append({'actor':a.get_name(),'position':a.get_actor_location().to_tuple()})
 match=label in ['V2_House_HH_V3_HerbShelf','V2_House_HH_Q3_Visual_HH_V3_HerbShelf'] or label.startswith(('V2_House_HH_V3_ShelfVial_','V2_House_HH_V3_ShelfHerb_','V2_House_HH_Art_HerbShelfStock_')) or (label.startswith('ArtV4_HerbalWindowShelf') and abs(p.x-17190)<1)
 if match:
  old=p.to_tuple();p.x-=280;a.set_actor_location(p,False,True);moves.append({'name':a.get_name(),'label':label,'before':old,'after':p.to_tuple()})
 if label=='ArtV4_Edge_Shrubs':
  c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,False);t.scale3d=t.scale3d*(.60 if i%3 else .86);c.update_instance_transform(i,t,False,True,True)
(R/'Art/HealingHouse/ArtV4_HearthPlacement.json').write_text(json.dumps(hearth,indent=2));assert len(moves)>20;assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(R/'Art/HealingHouse/ArtV4_FurnitureMoves.json').write_text(json.dumps(moves,indent=2));(R/'Saved/ArtPassV4/FinalComposition.json').write_text(json.dumps({'moved_furniture_and_owning_blocker_together':moves,'shrub_instances_retained':23,'shrub_scale_multipliers':[.60,.86]},indent=2))
