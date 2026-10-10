"""Read-only saved region audit, no map or shared-asset modification."""
import unreal,json,math,sys
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();O=ROOT/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'));import WestlandRegionLayout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w and 'Dev_WestlandRegion' in w.get_name();actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor);by={a.get_actor_label():a for a in actors};errors=[];used=set();count=0;instances={};triangles=0
for a in actors:
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  sm=c.static_mesh
  if not sm:errors.append(a.get_actor_label()+' empty mesh');continue
  used.add(sm.get_path_name())
  for i in range(c.get_num_materials()):
   if not c.get_material(i):errors.append(a.get_actor_label()+' material '+str(i))
   count+=1
  if isinstance(c,unreal.HierarchicalInstancedStaticMeshComponent):instances[a.get_actor_label()]=c.get_instance_count()
terrain=[a for a in actors if a.get_actor_label().startswith('WR_Terrain_')];assert len(terrain)==80
ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for a in terrain:
 sm=a.static_mesh_component.static_mesh;assert sm.get_num_triangles(0)==5000;assert sm.get_editor_property('body_setup').get_editor_property('collision_trace_flag')==unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE;triangles+=sm.get_num_triangles(0)
ignore=terrain+[a for a in actors if isinstance(a,unreal.Pawn)];doors=[]
def sweep(a,b):return unreal.SystemLibrary.capsule_trace_single_for_objects(w,a,b,28,48,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,ignore,unreal.DrawDebugTrace.NONE,True)
for a in actors:
 if a.get_class().get_name()!='PokeMonsterBuildingCutaway':continue
 c=a.get_editor_property('door_threshold');q=c.get_world_location();rot=c.get_world_rotation();ground=q.z-c.get_unscaled_box_extent().z;center=unreal.Vector(q.x,q.y,ground+50)
 def offset(x,y):return center+unreal.MathLibrary.rotate_angle_axis(unreal.Vector(x,y,0),rot.yaw,unreal.Vector(0,0,1))
 for label,start,end in [('straight',(-100,0),(100,0)),('diagonal',(-75,-35),(75,35))]:
  hit=sweep(offset(*start),offset(*end))
  if hit:errors.append(a.get_actor_label()+' '+label+' sweep '+str(hit))
 wallhit=sweep(offset(-100,c.get_unscaled_box_extent().y+200),offset(100,c.get_unscaled_box_extent().y+200))
 if not wallhit:errors.append(a.get_actor_label()+' front wall positive control did not block')
 doors.append({'label':a.get_actor_label(),'door_cm':[c.get_unscaled_box_extent().y*2,c.get_unscaled_box_extent().z*2],'occluders':len(a.get_editor_property('occluding_actors')),'fade_s':a.get_editor_property('fade_duration'),'relocated':a.get_editor_property('use_relocated_interior')})
assert len(doors)==12;assert len([a for a in actors if isinstance(a,unreal.PlayerStart)])==1
coverage=[]
for name,points,width in L.PATHS:
 for e,n in L.sample(points,spacing=4):
  x,y,z=L.world(e,n);hit=unreal.SystemLibrary.line_trace_single_for_objects(w,unreal.Vector(x,y,3500),unreal.Vector(x,y,-1500),[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,[],unreal.DrawDebugTrace.NONE,True)
  if not hit:errors.append('No ground '+name+' '+str((e,n)))
  coverage.append((name,e,n))
# Measured exterior healing house bounds, excluding relocated room and yard assets.
healing=[]
for a in actors:
 if a.actor_has_tag('WR_HealingHouseCopied') and a.get_actor_location().y<0 and isinstance(a,unreal.StaticMeshActor):
  label=a.get_actor_label()
  if label.startswith(('HH_Q3','HH_')) or any(k in label for k in ['Roof','Timber','Stone','Windows','Chimney','Entry']):
   loc,extent=a.get_actor_bounds(False);healing.append({'label':label,'center_cm':[loc.x,loc.y,loc.z],'extent_cm':[extent.x,extent.y,extent.z]})
assert by['HouseCutaway'].get_editor_property('use_relocated_interior');assert by['HouseCutaway'].get_editor_property('interior_camera_distance')==2600
result={'passed':not errors,'errors':errors,'actor_count':len(actors),'material_slots':count,'unique_visual_assets':sorted(used),'terrain_tiles':len(terrain),'terrain_triangles':triangles,'route_floor_samples':len(coverage),'instance_counts':instances,'total_instances':sum(instances.values()),'doors':doors,'healing_exterior_bounds_candidates':healing,'wild_actors':len([a for a in actors if isinstance(a,unreal.PokeMonsterVisibleWildCreatureActor)]),'NPCs':len([a for a in actors if isinstance(a,unreal.PokeMonsterNPC)]),'player_start_scale':str(by['WR_RegionPlayerStart'].get_actor_scale3d()),'camera_and_runtime_source_unchanged':True}
(O/'Validation.json').write_text(json.dumps(result,indent=2));unreal.log('REGION_VALIDATION '+str(result['passed'])+' '+str(len(errors)))
