import unreal,json,runpy,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();W=E.get_editor_world();reg=unreal.AssetRegistryHelpers.get_asset_registry();ML=unreal.MaterialEditingLibrary;out={};wanted=[]
for prefix in ['/Game/Environment/Architecture/Westland/Meshes','/Game/Environment/HealingHouse/Meshes','/Game/Environment/HealingHouse/QualityV3/Meshes']:
 for d in reg.get_assets_by_path(prefix,recursive=True):
  if str(d.asset_class_path.asset_name)=='StaticMesh'and any(k in str(d.asset_name)for k in ['Window','Brace','Eave','Ridge','Chimney','Beam','Plinth','Roof']):wanted.append(str(d.object_path)if hasattr(d,'object_path')else str(d.package_name))
for p in wanted:
 m=unreal.load_asset(p);b=m.get_bounding_box();out[p]=dict(min=b.min.to_tuple(),max=b.max.to_tuple(),triangles=m.get_num_triangles(0),materials=[s.material_interface.get_path_name()if s.material_interface else None for s in m.static_materials])
(D/'ArchitectureAssets.json').write_text(json.dumps(out,indent=2));mats={}
for p in ['/Game/Environment/VisualV2WorldOverhaulV3/Materials/M_WOV_Ground','/Game/Environment/VisualV2WorldOverhaulV3/Materials/M_WOV_Roof','/Game/Environment/WestlandAssetLibrary/Materials/M_WLA_Painted','/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_FlowerWhite']:
 m=unreal.load_asset(p)
 if not m:continue
 try:stats=ML.get_material_statistics(m).export_text()
 except Exception:stats=None
 mats[p]=dict(stats=stats,custom=[n.get_editor_property('code')for n in ML.get_material_expressions(m)if isinstance(n,unreal.MaterialExpressionCustom)]if isinstance(m,unreal.Material)else[],parent=m.parent.get_path_name()if isinstance(m,unreal.MaterialInstanceConstant)else None)
(D/'MaterialAudit.json').write_text(json.dumps(mats,indent=2))
# Export only existing source texture pixels into this task's read-only visual evidence.
P=D/'TexturePreviews';P.mkdir(exist_ok=True)
for q in ['/Game/Pack_Bonus/Textures/Grass_1/T_Pack_Bonus_Grass_1_basecolor','/Game/Pack_Bonus/Textures/Grass_3/T_Pack_Bonus_Grass_3_basecolor','/Game/Pack_Bonus/Textures/Wall_1/T_Pack_Bonus_Wall_1_basecolor','/Game/Pack_Bonus/Textures/Wall_2/T_Pack_Bonus_Wall_2_basecolor','/Game/Pack_Bonus/Textures/Wall_3/T_Pack_Bonus_Wall_3_basecolor','/Game/Pack_Bonus/Textures/Tile_1/T_Pack_Bonus_Tile_1_basecolor','/Game/Pack_Bonus/Textures/Tile_2/T_Pack_Bonus_Tile_2_basecolor','/Game/Pack_Bonus/Textures/Tile_3/T_Pack_Bonus_Tile_3_basecolor']:
 a=unreal.load_asset(q);assert a;task=unreal.AssetExportTask();task.object=a;task.filename=str(P/(a.get_name()+'.tga'));task.automated=True;task.replace_identical=False;task.prompt=False;task.exporter=unreal.TextureExporterTGA();assert unreal.Exporter.run_asset_export_task(task)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
