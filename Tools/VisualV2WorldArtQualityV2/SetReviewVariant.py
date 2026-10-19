import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';sys.path.insert(0,str(R/'Tools/VisualV2WorldArtQualityV2'));from RuntimeVariants import Variants
w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));j=json.loads((S/'ReviewVariant.json').read_text())
if not hasattr(unreal,'_waq2_review_variants'):unreal._waq2_review_variants=Variants(w)
unreal._waq2_review_variants.apply(j['mode'])
