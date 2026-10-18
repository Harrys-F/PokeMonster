import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2AASoftShadowsV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1'
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
s=scene(w);assert s==json.loads((O/'TestScene.json').read_text())
root='/Game/Development/VisualV2AASoftShadowsV1';m=unreal.load_asset(root+'/M_SoftGroundBlob');assert m.material_domain==unreal.MaterialDomain.MD_DEFERRED_DECAL and m.blend_mode==unreal.BlendMode.BLEND_TRANSLUCENT
for prop in [unreal.MaterialProperty.MP_NORMAL,unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialProperty.MP_METALLIC,unreal.MaterialProperty.MP_SPECULAR]:assert not unreal.MaterialEditingLibrary.get_material_property_input_node(m,prop),'Decal must only write color/opacity'
# An already saved valid graph is never rebuilt or re-saved by this verification.
d={'assets':list(unreal.EditorAssetLibrary.list_assets(root)),'domain':str(m.material_domain),'blend':str(m.blend_mode),'scene_unchanged':True,'new_map_created':False,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
(O/'AssetsVerified.json').write_text(json.dumps(d,indent=2));assert not d['dirty_maps'] and not d['dirty_content']
