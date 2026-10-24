"""Only the newly authored map: physical cave-wall collision and a readable forest clearing."""
import unreal,json,sys,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();assert w.get_name()=='Dev_BiomeTestMap_V1';ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);O=R/'Saved/BiomeTestV1/SceneryRefinement.json';assert not O.exists()
assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
actors=ES.get_all_level_actors();trees=[a for a in actors if a.get_actor_label().startswith('Biome_RevealTree_')];trunks=[a for a in actors if a.get_actor_label().startswith('Biome_Trunk_')];walls=[];moved=[];positions=[L.local(a.get_actor_location().x,a.get_actor_location().y)for a in trees]
for a in actors:
 if a.get_actor_label().startswith('Biome_CaveRockWall_'):
  # Existing roaming ignores decorative AABB cores when a mesh provides actual world collision.
  # The existing aligned wall proxy remains as a secondary solid barrier.
  a.static_mesh_component.set_collision_profile_name('BlockAll');walls.append(a.get_actor_label())
for a in trees:
 q=a.get_actor_location();u,v=L.local(q.x,q.y);c=a.static_mesh_component;b=c.static_mesh.get_bounding_box();s=a.get_actor_scale3d();r=max(abs(b.min.x),abs(b.max.x))*s.x
 if not(u>500 and v<0 and abs(u-1650)<r+450 and abs(v+b.max.z*s.z*.65+1750)<r+450):continue
 candidate=None
 for nv in range(-850,-4701,-350):
  for nu in [4300,4700,4000]:
   if L.path_distance(nu,nv)<330 or any(math.hypot(nu-x,nv-y)<260 for x,y in positions):continue
   if 2100<nu<3950 and -4250<nv<-2700:continue
   candidate=(nu,nv);break
  if candidate:break
 assert candidate
 trunk=min(trunks,key=lambda t:(t.get_actor_location().x-q.x)**2+(t.get_actor_location().y-q.y)**2);assert (trunk.get_actor_location().x-q.x)**2+(trunk.get_actor_location().y-q.y)**2<1
 nu,nv=candidate;a.set_actor_location(unreal.Vector(*L.world(nu,nv,L.height(nu,nv))),False,True);t=trunk.get_actor_location();trunk.set_actor_location(unreal.Vector(*L.world(nu,nv,L.height(nu,nv)+130)),False,True);positions.append(candidate)
 moved.append({'tree':a.get_actor_label(),'trunk':trunk.get_actor_label(),'from_uv':[u,v],'to_uv':candidate})
assert len(walls)==3 and moved
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1')
O.write_text(json.dumps({'cave_walls_actual_collision':walls,'reason_cave':'rotated noncolliding boulder AABB inflated into walkable cave and rejected all creature paths; actual mesh collision removes that fallback without weakening walls','reason_forest':'camera-projected canopy covered floating habitat; relocate only new trees and matching trunk blockers into denser peripheral clumps','moved':moved,'tree_count_retained':len(trees),'existing_maps_saved':False},indent=2))
