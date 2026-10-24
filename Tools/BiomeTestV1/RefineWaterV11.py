"""Scoped shoreline/observation corrections justified by WaterPIE03; preserve all trees and original sources."""
import unreal,json,sys,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1';O=R/'Saved/BiomeTestV11/WaterRefinement.json';assert not O.exists()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
actors=list(ES.get_all_level_actors());hab={a.habitat_name:a for a in actors if isinstance(a,unreal.PokeMonsterBiomeHabitat)};g=hab['Garados'];centre=(2920,2810);g.set_actor_location(unreal.Vector(*L.world(*centre)),False,True);g.bounds.set_box_extent(unreal.Vector(450,450,600));arr=list(g.specimens);arr[0].set_editor_property('local_position',unreal.Vector(2780-centre[0],-(2750-centre[1]),L.height(2780,2750)));g.set_editor_property('specimens',arr);g.set_editor_property('travel_points',[unreal.Vector(u-centre[0],-(v-centre[1]),0)for u,v in [(2780,2750),(3090,2950),(3020,2630)]])
disabled=[]
for a in actors:
 if a.actor_has_tag('BiomePlayerWaterBarrier'):
  p=a.get_actor_location();u,v=L.local(p.x,p.y);block=L.height(u,v)<-48 and abs(v-4100)>=230
  a.set_actor_enable_collision(block)
  if not block:disabled.append(a.get_actor_label())
# Free the right shoreline's observation lane, moving only these map-owned bank trees/trunks.
trees=[a for a in actors if a.get_actor_label().startswith('Biome_RevealTree_')];trunks=[a for a in actors if a.get_actor_label().startswith('Biome_Trunk_')];moved=[]
for a in trees:
 p=a.get_actor_location();u,v=L.local(p.x,p.y)
 if not(3950<u<4700 and 1800<v<4300):continue
 i=len(moved);nu=4770+(i%2)*110;nv=1750+(i//2)*380
 while nv>4750:nv-=2900;nu-=180
 trunk=min(trunks,key=lambda b:(b.get_actor_location().x-p.x)**2+(b.get_actor_location().y-p.y)**2);assert (trunk.get_actor_location().x-p.x)**2+(trunk.get_actor_location().y-p.y)**2<1
 a.set_actor_location(unreal.Vector(*L.world(nu,nv,L.height(nu,nv))),False,True);trunk.set_actor_location(unreal.Vector(*L.world(nu,nv,L.height(nu,nv)+130)),False,True);moved.append({'tree':a.get_actor_label(),'from_uv':[u,v],'to_uv':[nu,nv]})
assert len(trees)==103;assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1')
O.write_text(json.dumps({'reason':'Observed Schiggy shore block and canopy occlusion in WaterPIE03; shallower entry, wet bed instead of grass, Garados nearer observable west shore','temporarily_disabled_no_longer_deep_water_blockers':disabled,'retained_tree_count':len(trees),'moved_only_new_map_trees':moved},indent=2))
