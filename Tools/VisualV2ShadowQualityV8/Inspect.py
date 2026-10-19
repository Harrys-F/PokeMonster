import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2ShadowQualityV8'
r={'blendable_locations':[s for s in dir(unreal.BlendableLocation) if s.isupper()],'scene_texture_ids':[s for s in dir(unreal.SceneTextureId) if s.isupper()],'camera_blendable':hasattr(unreal.CameraComponent,'add_or_update_blendable'),'volume_blendable':hasattr(unreal.PostProcessVolume,'add_or_update_blendable'),'material_nodes':hasattr(unreal,'MaterialExpressionSceneTexture')}
(S/'Interfaces.json').write_text(json.dumps(r,indent=2));unreal.log('SV8_INTERFACES_READONLY')

(S/'MIDInterface.json').write_text(json.dumps([k for k in dir(unreal.MaterialInstanceDynamic) if 'vector_parameter' in k or 'scalar_parameter' in k],indent=2))
