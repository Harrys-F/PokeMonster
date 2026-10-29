"""Add exactly twelve generic, nonblocking world pickups to the existing VisualV2 only."""
import unreal,json,re,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/InventoryV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert W.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
existing=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterWorldItem)
assert not existing,'Already authored; inspect before updating'
points=[('Village1',-2500,-1500,'PokeBall',2),('Village2',-2050,-1350,'Potion',1),('Village3',-3180,-1060,'Antidote',1),('Meadow1',-400,-700,'PokeBall',1),('Meadow2',-1000,-1350,'Potion',1),('Meadow3',-600,400,'ParalyzeHeal',1),('Forest1',-2550,1400,'PokeBall',1),('Forest2',-4350,1400,'Antidote',1),('Forest3',-4000,1800,'SuperPotion',1),('Forest4',750,1900,'Awakening',1),('Pond1',-300,-1900,'Potion',1),('Pond2',1100,-2600,'GreatBall',1)]
def trace(x,y):
 h=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,800),unreal.Vector(x,y,-300),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],unreal.DrawDebugTrace.NONE)
 if not h:return None
 text=h.export_text();v=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',text)
 return float(v[1])if v else None
def clear(x,y,z):
 return not unreal.SystemLibrary.capsule_trace_single(W,unreal.Vector(x,y,z+51),unreal.Vector(x+1,y,z+51),30,48,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],unreal.DrawDebugTrace.NONE)
rows=[];before={a.get_name():a.get_actor_transform().export_text()for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)}
for label,x,y,item,qty in points:
 chosen=None
 for dx,dy in [(0,0),(80,0),(-80,0),(0,80),(0,-80),(120,100),(-120,-100)]:
  px,py=x+dx,y+dy;z=trace(px,py)
  if z is None or not -2<=z<=8 or not clear(px,py,z):continue
  for ax,ay in [(0,-170),(-170,0),(170,0),(0,170)]:
   az=trace(px+ax,py+ay)
   if az is not None and abs(az-z)<5 and clear(px+ax,py+ay,az):chosen=(px,py,z,px+ax,py+ay,az);break
  if chosen:break
 assert chosen,('No safe candidate',label)
 px,py,z,ax,ay,az=chosen;a=A.spawn_actor_from_class(unreal.PokeMonsterWorldItem,unreal.Vector(px,py,z+1),unreal.Rotator(0,15,0));a.set_actor_label('IV2_Pickup_'+label)
 a.set_editor_property('pickup_id','Pickup.VisualV2.V1.'+label);a.set_editor_property('item',unreal.load_asset('/Game/Data/Items/DA_'+('TestHealingItem'if item=='Potion'else item)));a.set_editor_property('quantity',qty)
 rows.append({'id':str(a.pickup_id),'actor':a.get_name(),'label':a.get_actor_label(),'area':re.sub(r'\d','',label),'item':item,'quantity':qty,'position':[px,py,z+1],'approach':[ax,ay,az+50.15],'capsule_clear':True,'generic_model':a.mesh.static_mesh.get_path_name()})
after={a.get_name():a.get_actor_transform().export_text()for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if a.get_name()in before};assert before==after
assert len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterWorldItem))==12
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(D/'PickupLocations.json').write_text(json.dumps(rows,indent=2));print('INVENTORY_V2_PICKUPS',len(rows),'old actor transforms preserved')
