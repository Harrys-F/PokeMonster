import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/Ranger/Review/V2');m=unreal.load_asset('/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2');settings=m.lod_settings;groups=list(settings.get_editor_property('lod_groups'));before=[]
for i,g in enumerate(groups):
 r=g.get_editor_property('reduction_settings');before.append({k:str(r.get_editor_property(k)) for k in ['num_of_triangles_percentage','num_of_vert_percentage','base_lod','recalc_normals']})
 r.set_editor_property('num_of_triangles_percentage',1.);r.set_editor_property('num_of_vert_percentage',1.);r.set_editor_property('base_lod',i);r.set_editor_property('recalc_normals',False);g.set_editor_property('reduction_settings',r)
settings.set_editor_property('lod_groups',groups);unreal.EditorAssetLibrary.save_loaded_asset(settings,False);m.set_editor_property('lod_settings',settings);s=unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem);assert s.reimport_all_custom_lods(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False);(P/'ImplicitReductionCorrection.json').write_text(json.dumps({'before':before,'after_registry':{str(k):str(v) for k,v in unreal.EditorAssetLibrary.get_tag_values(m.get_path_name()).items()}},indent=2))
