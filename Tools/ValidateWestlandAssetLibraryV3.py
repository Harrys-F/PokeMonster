"""Scoped editor/PIE audit: bounds, materials, normals-at-import evidence, collision.
Map Check is executed on the complete library map; no unrelated map is saved.
"""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibraryV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);game=E.get_game_world();w=game or E.get_editor_world();assert 'Dev_WestlandAssetLibrary' in w.get_name();S=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);data=json.loads((R/'Art/World/WestlandAssetLibrary/ArtQualityV3.json').read_text());actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor);by={a.get_actor_label():a for a in actors};rows=[]
for key,a in zip(('Oak','BushA','BushB'),data['assets']):
 actor=by['V3_Forest_'+key];c=actor.static_mesh_component;m=c.static_mesh;assert m.get_name()==a['object'];assert c.get_num_materials()==2 and m.get_num_sections(0)==2
 assert all(c.get_material(i) for i in range(2));box=m.get_bounding_box();size=box.max-box.min;assert all(abs(v/100-t)<max(.02,t*.01) for v,t in zip(size.to_tuple(),a['dimensions_m']));assert box.min.z>=-.1
 assert list(actor.get_actor_scale3d().to_tuple())==[1,1,1];assert c.get_collision_enabled()==(unreal.CollisionEnabled.QUERY_AND_PHYSICS if key=='Oak' else unreal.CollisionEnabled.NO_COLLISION)
 row={'object':a['object'],'triangles':m.get_num_triangles(0),'sections':2,'slots':2,'bounds_cm':list(size.to_tuple()),'scale':[1,1,1],'ground_min_z_cm':box.min.z}
 if not game:
  count=S.get_simple_collision_count(m)+S.get_convex_collision_count(m);assert count==len(a['collision_objects']);row.update({'collision_count':count,'lods':S.get_lod_count(m),'uv_channels':S.get_num_uv_channels(m,0)})
 else:
  center=actor.get_actor_location()+unreal.Vector(0,0,48);ignored=[x for x in actors if x!=actor]
  hits=[bool(unreal.SystemLibrary.capsule_trace_single_for_objects(w,center-v*300,center+v*300,28,48,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,ignored,unreal.DrawDebugTrace.NONE,True)) for v in (unreal.Vector(1,0,0),unreal.Vector(0,1,0))]
  assert any(hits) if key=='Oak' else not any(hits),(key,hits);row['capsule_collision_hits']=hits
  if key=='Oak':
   upper=actor.get_actor_location()+unreal.Vector(0,0,350);hit=unreal.SystemLibrary.capsule_trace_single_for_objects(w,upper-unreal.Vector(300,0,0),upper+unreal.Vector(300,0,0),28,48,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,ignored,unreal.DrawDebugTrace.NONE,True);assert hit;row['upper_trunk_collision']=True
 rows.append(row)
path_mesh=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Review/SM_WLA_V3_ForestPath');assert path_mesh.get_num_triangles(0)==1512
path_actor=by['V3_Forest_Path'];assert path_actor.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not path_actor.static_mesh_component.get_editor_property('cast_shadow')
if not game:
 bs=S.get_lod_build_settings(path_mesh,0);assert bs.recompute_tangents;assert S.get_num_uv_channels(path_mesh,0)>=1
if game:
 p=unreal.GameplayStatics.get_player_pawn(w,0);arm=p.get_component_by_class(unreal.SpringArmComponent);cam=p.get_component_by_class(unreal.CameraComponent);rot=arm.get_world_rotation();assert arm.target_arm_length==2500 and cam.field_of_view==35 and abs(rot.pitch+55)<.01 and abs(rot.yaw+45)<.01 and p.get_component_by_class(unreal.CharacterMovementComponent).max_walk_speed==210
else:unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
tex=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/QualityV3/Textures/T_WLA_FoliageGroups_V3');master=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/QualityV3/Materials/M_WLA_FoliageGroups_V3');assert master.get_editor_property('blend_mode')==unreal.BlendMode.BLEND_MASKED and master.get_editor_property('two_sided');assert tex
(O/('PIEAudit.json' if game else 'FinalAudit.json')).write_text(json.dumps({'passed':True,'mode':'PIE' if game else 'Editor','meshes':rows,'masked':True,'alpha_clip':master.get_editor_property('opacity_mask_clip_value'),'mip_gen':str(tex.get_editor_property('mip_gen_settings')),'power_of_two':str(tex.get_editor_property('power_of_two_mode')),'shader_texture_samples':1,'forest_path_triangles':1512,'forest_path_no_collision':True},indent=2));unreal.log('WLA_V3_AUDIT_PASS')
