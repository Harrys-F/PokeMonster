"""Fix only the unpublished V6 material's confirmed texture sampler mismatch."""
import unreal,subprocess
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P='/Game/Characters/Creatures/Glurak/AnimationV6';assert not subprocess.check_output(['git','ls-files','--','Content/Characters/Creatures/Glurak/AnimationV6'],cwd=R).strip();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();m=unreal.load_asset(P+'/M_Glurak_CompleteRear_V6');assert m;n=0
for e in unreal.ObjectIterator(unreal.MaterialExpressionTextureSample):
 if e.get_outer()==m and e.texture and 'MetallicRoughness'in e.texture.get_name():e.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS);n+=1
assert n==1;unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);unreal.log('V6_GLURAK_SAMPLER_CORRECTED')
