#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Development/PokeMonsterEnvironmentRenderProfile.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterEnvironmentRenderProfileTest,
    "PokeMonster.Rendering.EnvironmentProfile.ScopeAndBaselineProtection",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterEnvironmentRenderProfileTest::RunTest(const FString& Parameters)
{
    using Profile = APokeMonsterEnvironmentRenderProfile;
    for (const TCHAR* Baseline : {TEXT("Dev_TestMap"), TEXT("Dev_TestMap_VisualV2"), TEXT("Dev_TestMap_RangerPerfV2"), TEXT("Dev_WestlandRegion"), TEXT("Dev_WestlandAssetLibrary")})
        TestFalse(TEXT("Preserved maps cannot opt into the experiment"), Profile::IsTargetLevelName(Baseline));
    TestTrue(TEXT("Only the separate experiment can opt in"), Profile::IsTargetLevelName(TEXT("Dev_TestMap_EnvironmentPerfV1")));
    TestFalse(TEXT("Render-only actor has no tick"), GetDefault<Profile>()->PrimaryActorTick.bCanEverTick);
    TestFalse(TEXT("Render-only actor adds no collider"), GetDefault<Profile>()->GetActorEnableCollision());

    auto& Manager = IConsoleManager::Get();
    const TCHAR* Name = TEXT("pm.EnvironmentPerf.AutomationScope");
    IConsoleVariable* Variable = Manager.RegisterConsoleVariable(Name, 7, TEXT("Temporary automation fixture"), ECVF_Default);
    ON_SCOPE_EXIT { Manager.UnregisterConsoleObject(Variable, false); };
    const auto OriginalPriority = static_cast<EConsoleVariableFlags>(Variable->GetFlags() & ECVF_SetByMask);
    FPokeMonsterEnvironmentCVarOverride Scope;
    TestTrue(TEXT("Scoped override can apply over a default"), Scope.Apply(Name, TEXT("2")));
    TestEqual(TEXT("Override is effective"), Variable->GetInt(), 2);
    Scope.Restore();
    TestEqual(TEXT("Original value is restored"), Variable->GetInt(), 7);
    TestEqual(TEXT("Original priority is restored"), static_cast<EConsoleVariableFlags>(Variable->GetFlags() & ECVF_SetByMask), OriginalPriority);
    TestTrue(TEXT("Override can be reused"), Scope.Apply(Name, TEXT("2")));
    Variable->Set(11, ECVF_SetByConsole);
    Scope.Restore();
    TestEqual(TEXT("Later user console changes are never overwritten"), Variable->GetInt(), 11);
    TestFalse(TEXT("Higher-priority user changes block the experiment"), Scope.Apply(Name, TEXT("2")));
    TestEqual(TEXT("Blocked application leaves user value intact"), Variable->GetInt(), 11);
    return true;
}
#endif
