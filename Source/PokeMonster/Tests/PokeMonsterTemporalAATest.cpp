#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Rendering/PokeMonsterTemporalAABlendable.h"
#include "SceneView.h"
#include "GameTime.h"
#include "HAL/IConsoleManager.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterTemporalAATest,
    "PokeMonster.Rendering.TemporalAA.MapBlendableScope", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterTemporalAATest::RunTest(const FString&)
{
    FSceneViewFamilyContext Family(FSceneViewFamily::ConstructionValues(nullptr, nullptr, FEngineShowFlags(ESFIM_Game)).SetTime(FGameTime()));
    FSceneViewInitOptions Options;
    Options.ViewFamily = &Family;
    Options.SetViewRectangle(FIntRect(0, 0, 1280, 720));
    Options.ViewRotationMatrix = FMatrix::Identity;
    Options.ProjectionMatrix = FMatrix::Identity;
    FSceneView View(Options);
    const auto* Blendable = GetDefault<UPokeMonsterTemporalAABlendable>();
    const auto* AA = IConsoleManager::Get().FindConsoleVariable(TEXT("r.AntiAliasingMethod"));
    const int32 Before = AA->GetInt();
    View.bIsGameView = true;
    View.AntiAliasingMethod = AAM_TSR;
    const auto PP = View.FinalPostProcessSettings;
    const auto Origin = View.ViewMatrices.GetViewOrigin();
    Blendable->OverrideBlendableSettings(View, 0.f);
    TestEqual(TEXT("Zero weight keeps TSR"), View.AntiAliasingMethod, AAM_TSR);
    View.bIsGameView = false;
    Blendable->OverrideBlendableSettings(View, 1.f);
    TestEqual(TEXT("Editor preview retains its AA"), View.AntiAliasingMethod, AAM_TSR);
    View.bIsGameView = true; View.bIsSceneCapture = true;
    Blendable->OverrideBlendableSettings(View, 1.f);
    TestEqual(TEXT("Scene captures retain their AA"), View.AntiAliasingMethod, AAM_TSR);
    View.bIsSceneCapture = false;
    Blendable->OverrideBlendableSettings(View, 1.f);
    TestEqual(TEXT("Game view uses TAA"), View.AntiAliasingMethod, AAM_TemporalAA);
    TestEqual(TEXT("Global AA setting unchanged"), AA->GetInt(), Before);
    TestEqual(TEXT("Camera unchanged"), View.ViewMatrices.GetViewOrigin(), Origin);
    TestEqual(TEXT("Bloom unchanged"), View.FinalPostProcessSettings.BloomIntensity, PP.BloomIntensity);
    TestEqual(TEXT("Exposure unchanged"), View.FinalPostProcessSettings.AutoExposureBias, PP.AutoExposureBias);
    View.AntiAliasingMethod = AAM_None;
    Blendable->OverrideBlendableSettings(View, 1.f);
    TestEqual(TEXT("No-AA diagnostic stays disabled"), View.AntiAliasingMethod, AAM_None);
    return true;
}
#endif
