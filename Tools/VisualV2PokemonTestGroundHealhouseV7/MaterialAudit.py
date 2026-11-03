"""Read final private graphs; never compile, edit or save assets."""
import unreal,json
from pathlib import Path
D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';rows=[]
for name in ['LimePlaster','SageLimewash','OakFloor','OakJoinery','ReviewWater']:
 m=unreal.load_asset('/Game/Environment/VisualV2InteriorV7/Materials/M_V7_'+name);assert m;expressions=unreal.MaterialEditingLibrary.get_material_expressions(m);textures=[n.texture.get_path_name()for n in expressions if isinstance(n,unreal.MaterialExpressionTextureSample)and n.texture];codes=[n.get_editor_property('code')for n in expressions if isinstance(n,unreal.MaterialExpressionCustom)]
 if name in ['LimePlaster','SageLimewash']:
  assert any('/T_V7_PlasterGrainNormal.'in p for p in textures),(name,textures)
  assert not any('/T_WR4_PlasterMicroNormal.'in p for p in textures),(name,textures)
 rows.append(dict(name=name,textures=textures,codes=codes,instanced=m.get_editor_property('used_with_instanced_static_meshes')))
(D/'MaterialAuditFinal.json').write_text(json.dumps(dict(passed=True,materials=rows),indent=2));print('V7 FINAL MATERIALS VALID')
