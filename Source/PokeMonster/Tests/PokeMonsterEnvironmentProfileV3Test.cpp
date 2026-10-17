#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Development/PokeMonsterEnvironmentRenderProfileV3.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterEnvironmentProfileV3Test,
    "PokeMonster.Rendering.EnvironmentProfileV3.IndependentExperiment",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterEnvironmentProfileV3Test::RunTest(const FString&)
{
    using P = APokeMonsterEnvironmentRenderProfileV3;
    for (const TCHAR* Name : {TEXT("Dev_TestMap"), TEXT("Dev_TestMap_VisualV2"), TEXT("Dev_TestMap_EnvironmentPerfV1"), TEXT("Dev_TestMap_EnvironmentPerfV2"), TEXT("Dev_TestMap_RangerPerfV2"), TEXT("Dev_WestlandRegion"), TEXT("Dev_WestlandAssetLibrary")})
        TestFalse(TEXT("Existing maps cannot opt in"), P::IsTargetLevelName(Name));
    TestTrue(TEXT("Only V3 opts in"), P::IsTargetLevelName(TEXT("Dev_TestMap_EnvironmentPerfV3")));
    const auto* CDO = GetDefault<P>();
    TestFalse(TEXT("No tick"), CDO->PrimaryActorTick.bCanEverTick);
    TestFalse(TEXT("No collision"), CDO->GetActorEnableCollision());
    TestEqual(TEXT("Default begins at V1 integration"), CDO->RendererOverrides.FindRef(TEXT("r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor")), FString(TEXT("2")));
    TestEqual(TEXT("Default begins at V1 shadow rays"), CDO->RendererOverrides.FindRef(TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional")), FString(TEXT("2")));
    return true;
}
#endif
