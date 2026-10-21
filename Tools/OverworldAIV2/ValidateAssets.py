"""Read-only active presentation, animation, material and import contracts."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();rows=[]
for name in ['Zunderlauf','Schiggy','Bisasam']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);p=s.get_visuals().presentation;assert not p.get_validation_errors();cfg=s.overworld.behavior
 row={'species':str(s.get_internal_id()),'profile':p.get_path_name(),'mesh':p.mesh.get_path_name(),'height_cm':p.reference_size_cm,'skeleton':p.mesh.skeleton.get_path_name(),'materials':[slot.material_interface.get_path_name()for slot in p.mesh.materials],'clips':{str(k):v.get_path_name()for k,v in p.clips.items()},'behavior':str(cfg.temperament),'notice_cm':cfg.notice_radius,'personal_space_cm':cfg.personal_space,'disengage_cm':cfg.disengage_radius,'warning_seconds':cfg.warning_seconds,'encounter_cm':cfg.encounter_radius,'cooldown_seconds':cfg.encounter_cooldown,'walk_cm_s':p.walk_speed*s.overworld.behavior.walk_multiplier,'run_clip_cm_s':p.run_speed};rows.append(row)
 if name=='Schiggy':
  old=unreal.load_asset('/Game/Characters/Creatures/Schiggy/MeshyV1/DA_Schiggy_Presentation');assert old.mesh.skeleton==p.mesh.skeleton;assert dict(old.clips)==dict(p.clips);assert old.mesh.materials[0].material_interface==p.mesh.materials[0].material_interface;assert len(p.mesh.materials)==2;assert p.reference_size_cm==50
  row['import_sources']=list(p.mesh.get_editor_property('asset_import_data').extract_filenames());assert all(Path(x).resolve().is_relative_to(R)for x in row['import_sources']);row['original_material_and_7_clips_reused']=True
textures=[]
for path in unreal.EditorAssetLibrary.list_assets('/Game/Characters/Creatures/Schiggy/MeshyV1/Textures',True,False):
 t=unreal.load_asset(path)
 if isinstance(t,unreal.Texture2D):textures.append({'asset':path,'width':t.blueprint_get_size_x(),'height':t.blueprint_get_size_y(),'mips':str(t.mip_gen_settings),'lod_bias':t.lod_bias})
assert len(textures)==3
(R/'Saved/OverworldAIV2/AssetContracts.json').write_text(json.dumps({'species':rows,'original_textures':textures},indent=2))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
