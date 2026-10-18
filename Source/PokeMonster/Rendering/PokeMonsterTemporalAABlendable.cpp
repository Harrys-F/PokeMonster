#include "PokeMonsterTemporalAABlendable.h"
#include "SceneView.h"
#include "HAL/IConsoleManager.h"

void UPokeMonsterTemporalAABlendable::OverrideBlendableSettings(FSceneView& View, float Weight) const
{
    // A discrete AA method cannot be fractionally blended. Preserve editor/capture/debug views.
    if (Weight < .5f || !View.bIsGameView || View.bIsSceneCapture
        || (View.AntiAliasingMethod != AAM_TSR && View.AntiAliasingMethod != AAM_TemporalAA)) return;

    View.AntiAliasingMethod = AAM_TemporalAA;
    const auto* Upsampling = IConsoleManager::Get().FindTConsoleVariableDataInt(TEXT("r.TemporalAA.Upsampling"));
    View.PrimaryScreenPercentageMethod = Upsampling && Upsampling->GetValueOnGameThread() != 0
        ? EPrimaryScreenPercentageMethod::TemporalUpscale : EPrimaryScreenPercentageMethod::SpatialUpscale;
}
