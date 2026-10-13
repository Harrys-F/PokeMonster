import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/DevTestMapVisualV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
# These six initially-clean shared materials were dirtied solely by the building automation test.
packages=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/Environment/Architecture/Westland/Materials/')]
if packages:result,error=unreal.EditorLoadingAndSavingUtils.reload_packages(packages,unreal.ReloadPackagesInteractionMode.ASSUME_POSITIVE);assert result,str(error)
changed=[];sprites=[]
for a in A.get_all_level_actors():
 n=a.get_actor_label()
 if n.startswith(('V2_Instanced_','V2_Cottage_')):
  for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):
   c.set_mobility(unreal.ComponentMobility.STATIC)
   if n.startswith('V2_Instanced_'):
    c.set_editor_property('affect_distance_field_lighting',False);c.set_editor_property('affect_dynamic_indirect_lighting',False)
   changed.append(n)
 if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterTrainerNPC,unreal.PokeMonsterRestPoint)):
  for c in a.get_components_by_class(unreal.PaperSpriteComponent):
   sp=c.get_sprite()
   if not sp:continue
   tex=sp.get_editor_property('source_texture');data=tex.get_editor_property('asset_import_data')
   sprites.append({'actor':n,'texture_file':data.get_first_filename() if data else None,'dimension':sp.get_editor_property('source_dimension').to_tuple(),'ppu':sp.get_editor_property('pixels_per_unreal_unit'),'pivot_mode':str(sp.get_editor_property('pivot_mode')),'custom_pivot':sp.get_editor_property('custom_pivot_point').to_tuple(),'component_scale':c.get_editor_property('relative_scale3d').to_tuple(),'component_location':c.get_editor_property('relative_location').to_tuple(),'component_rotation':str(c.get_editor_property('relative_rotation'))})
# Match legacy illustrated NPC screen presence to the unchanged 140-cm 3D player.
# Alpha spans measured from the existing source PNGs (threshold 32/255).
# Outdoor sprites face the camera; 95 cm in their plane approximates a 166-cm upright
# figure at -55 deg. Healer stays upright in the existing interior and is 160 cm tall.
visual_changes=[]
alpha={'Slice_Wanderer_Hinweis':(1257,61,95),'Slice_Archivarin_Abzweig':(1485,33,95),'Slice_Waldhueterin_Liora':(1456,59,95),'V2_House_HouseHealer':(1485,33,160)}
for a in A.get_all_level_actors():
 n=a.get_actor_label()
 if n not in alpha:continue
 c=a.get_component_by_class(unreal.PaperSpriteComponent);sp=c.get_sprite();span,gap,target=alpha[n];old=c.get_editor_property('relative_scale3d').to_tuple();ppu=sp.get_editor_property('pixels_per_unreal_unit');sc=target*ppu/span
 c.set_relative_scale3d(unreal.Vector(sc,sc,sc));pos=a.get_actor_location();up=c.get_up_vector();c.set_world_location(unreal.Vector(pos.x,pos.y,0)-up*(gap*sc/ppu),False,False)
 visual_changes.append({'actor':n,'previous_scale':old,'scale':sc,'visible_plane_height_cm':target,'alpha_span_px':span,'sprite_foot_on_ground':True})
(O/'NPCVisualCorrection.json').write_text(json.dumps(visual_changes,indent=2))
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(O/'Optimizations.json').write_text(json.dumps({'static_hism_groups':changed,'small_foliage_distance_field_indirect_exclusion':True,'reloaded_automation_dirtied_materials':[p.get_path_name() for p in packages]},indent=2));(O/'NPCSpriteAudit.json').write_text(json.dumps(sprites,indent=2))
