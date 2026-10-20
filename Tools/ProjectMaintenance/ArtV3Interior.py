"""Apply isolated, shadowless room lighting, bounded furniture layout and existing healer presentation."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and w.get_name()=='Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'InteriorApplied.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(w);actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};changed=[];channel=unreal.LightingChannels(channel0=False,channel1=True,channel2=False)
for a in actors.values():
 x=a.get_actor_location().x
 if not 16300<x<17500:continue
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  changed.append({'actor':a.get_name(),'label':a.get_actor_label(),'component':c.get_name(),'old_cast_shadow':bool(c.cast_shadow),'old_channels':c.get_editor_property('lighting_channels').export_text()});c.set_lighting_channels(False,True,False);c.set_cast_shadow(False)
 for c in a.get_components_by_class(unreal.LightComponent):
  old={'actor':a.get_name(),'label':a.get_actor_label(),'light':True,'old_cast_shadows':bool(c.cast_shadows),'old_channels':c.get_editor_property('lighting_channels').export_text()};c.set_editor_property('lighting_channels',channel);c.set_cast_shadows(False);changed.append(old)
cut=actors['V2_House_HouseCutaway'];cut.set_editor_property('use_shadowless_interior_lighting',True)
# Move matched visual and authoritative blocker together. Existing collision profiles are untouched.
moves=[]
def move(label,dx,dy):
 a=actors[label];old=a.get_actor_location();a.set_actor_location(old+unreal.Vector(dx,dy,0),False,True);moves.append({'name':a.get_name(),'label':label,'before':old.to_tuple(),'after':a.get_actor_location().to_tuple()})
for label in ['V2_House_HH_Art_BenchCompanion','V2_House_HH_Q3_Visual_HH_Art_BenchCompanion']:move(label,-305,-10)
for label in ['V2_House_HH_Art_TableWaiting','V2_House_HH_Q3_Visual_HH_Art_TableWaiting']:move(label,-35,0)
# Tabletop details follow their reused table, including the newer independent mortar.
for label,a in actors.items():
 p=a.get_actor_location()
 if 16610<p.x<16730 and 175<p.y<250 and 55<p.z<105 and not any(r['label']==label for r in moves):move(label,-35,0)
# A narrower entrance runner replaces the overlapping carpet impression; the centre remains open wood.
runner=actors['V2_House_HH_Art_MainRunner'];old=runner.get_actor_transform();runner.set_actor_scale3d(unreal.Vector(1.25,.86,1));move(runner.get_actor_label(),-120,0)
rug=actors['V2_House_HH_Art_ReceptionRug'];rug.set_actor_hidden_in_game(True);rug.static_mesh_component.set_visibility(False)
# The source healer, its capsule, identity and save/checkpoint/dialogue properties stay untouched.
healer=actors['V2_House_HouseHealer'];assert healer.get_actor_location().to_tuple()==(17230.,420.,62.)
C=R/'Art/Characters/NPCs/SilverLady';D='/Game/Characters/NPCs/SilverLady/Meshes';name='SM_SilverLady_HealerPose';path=D+'/'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(path)
ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'transform_vertex_to_absolute':True,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.static_mesh_import_data.set_editor_property(k,v)
t=unreal.AssetImportTask();t.filename=str(C/'Exports'/(name+'.fbx'));t.destination_path=D;t.destination_name=name;t.options=ui;t.automated=True;t.save=False;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);mesh=unreal.load_asset(path);assert mesh;mesh.set_material(0,unreal.load_asset('/Game/Characters/NPCs/SilverLady/Materials/MI_SilverLady_V1'));assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).get_simple_collision_count(mesh)==0;assert mesh.get_num_triangles(0)==149999;assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
AS=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);visual=AS.spawn_actor_from_class(unreal.PokeMonsterNPCVisualActor,unreal.Vector(17230,420,.25),unreal.Rotator(yaw=180));visual.set_actor_label('V2_House_SilverLady_HealerVisual');visual.set_folder_path('VisualV2/HealingHouse/NPC');visual.tags=['HealerPresentation','VisualOnly_NoCollision','ArtPassV3'];visual.set_editor_property('source_actor',healer);visual.set_editor_property('static_presentation_mesh',mesh);visual.set_editor_property('shadowless_interior_presentation',True);visual.set_actor_scale3d(unreal.Vector(.905,.905,.905));visual.refresh_presentation()
assert visual.static_visual and visual.static_visual.is_visible();assert not healer.sprite.is_visible();assert visual.static_visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');after=scene(w)
record={'room_components':changed,'cutaway':cut.get_name(),'furniture_moves':moves,'entrance_runner_old_transform':str(old),'entrance_runner_scale':[1.25,.86,1],'hidden_redundant_rug':rug.get_name(),'new_healer_visual':visual.get_name(),'healer_source':healer.get_name(),'healer_source_transform_unchanged':True,'static_mesh':mesh.get_path_name(),'static_triangles':mesh.get_num_triangles(0),'height_cm':190.32146*.905,'rig_status':'Static pose only; no validated animation rig or clips','outdoor_lights_unchanged':True};(S/'InteriorApplied.json').write_text(json.dumps(record,indent=2));(R/'Art/HealingHouse/ArtPassV3_Interior.json').write_text(json.dumps(record,indent=2));(S/'InteriorScene.json').write_text(json.dumps(after,indent=2));unreal.log('ART_V3_INTERIOR_SAVED')
