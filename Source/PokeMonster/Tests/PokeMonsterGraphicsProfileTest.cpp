#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Rendering/PokeMonsterGraphicsProfile.h"
#include "GameFramework/GameUserSettings.h"
#include "HAL/IConsoleManager.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterGraphicsProfiles,
    "PokeMonster.Rendering.GraphicsProfile.CAndReference", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterGraphicsProfiles::RunTest(const FString&)
{
    using P = UPokeMonsterGraphicsProfile;
    const auto* Profile = GetDefault<P>();
    TestEqual(TEXT("Configured default is C"), Profile->DefaultProfile, EPokeMonsterGraphicsProfile::VariantC);
    TestFalse(TEXT("Editor asset previews are excluded"), Profile->DoesSupportWorldType(EWorldType::Editor));
    TestTrue(TEXT("PIE supported"), Profile->DoesSupportWorldType(EWorldType::PIE));
    TestTrue(TEXT("Standalone supported"), Profile->DoesSupportWorldType(EWorldType::Game));
    EPokeMonsterGraphicsProfile Choice = EPokeMonsterGraphicsProfile::VariantC;
    TestFalse(TEXT("Invalid text rejected"), P::ParseProfile(TEXT("Medium"), Choice));
    TestEqual(TEXT("Rejected input preserves choice"), Choice, EPokeMonsterGraphicsProfile::VariantC);
    TestTrue(TEXT("Reference selection"), P::ParseProfile(TEXT("100"), Choice));
    TestEqual(TEXT("Reference is 100%"), P::ScreenPercentage(Choice), 100.f);
    TestTrue(TEXT("Hardware SPG selection"), P::ParseProfile(TEXT("HardwareSPG"), Choice));
    TestEqual(TEXT("Hardware reference keeps 75%"), P::ScreenPercentage(Choice), 75.f);
    TestTrue(TEXT("C selection"), P::ParseProfile(TEXT("C"), Choice));
    TestEqual(TEXT("C is 75%"), P::ScreenPercentage(Choice), 75.f);
    UGameUserSettings* User = NewObject<UGameUserSettings>();
    User->SetScreenResolution(FIntPoint(2560, 1440));
    User->SetFullscreenMode(EWindowMode::Windowed);
    const float DesiredDisplayScale = User->GetDefaultResolutionScale();
    const int32 AA = IConsoleManager::Get().FindConsoleVariable(TEXT("r.AntiAliasingMethod"))->GetInt();
    for (const auto Preset : {EPokeMonsterGraphicsProfile::VariantC, EPokeMonsterGraphicsProfile::Reference100, EPokeMonsterGraphicsProfile::HardwareReference75})
    {
        P::Configure(*User, Preset);
        TestEqual(TEXT("Output QHD"), User->GetScreenResolution(), FIntPoint(2560, 1440));
        const auto& Q = User->ScalabilityQuality;
        for (int32 Level : {Q.ViewDistanceQuality, Q.AntiAliasingQuality, Q.ShadowQuality,
            Q.GlobalIlluminationQuality, Q.ReflectionQuality, Q.PostProcessQuality,
            Q.TextureQuality, Q.EffectsQuality, Q.FoliageQuality, Q.ShadingQuality, Q.LandscapeQuality})
            TestEqual(TEXT("Every non-resolution group is High"), Level, 2);
        TestEqual(TEXT("User desired display-mode scale is preserved"), User->GetDefaultResolutionScale(), DesiredDisplayScale);
        TestEqual(TEXT("Requested internal fraction"), User->ScalabilityQuality.ResolutionQuality, P::ScreenPercentage(Preset));
        TestFalse(TEXT("No dynamic resolution"), User->IsDynamicResolutionEnabled());
    }
    TestEqual(TEXT("Configuration does not change global AA"), IConsoleManager::Get().FindConsoleVariable(TEXT("r.AntiAliasingMethod"))->GetInt(), AA);
    return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterGraphicsLumenScopes,
    "PokeMonster.Rendering.GraphicsProfile.LumenPathAndRestoration", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterGraphicsLumenScopes::RunTest(const FString&)
{
    using P = UPokeMonsterGraphicsProfile;
    auto* HW = IConsoleManager::Get().FindConsoleVariable(TEXT("r.Lumen.HardwareRayTracing"));
    auto* FG = IConsoleManager::Get().FindConsoleVariable(TEXT("r.Lumen.FinalGatherMethod"));
    if (!TestNotNull(TEXT("Lumen hardware selector is registered"), HW)
        || !TestNotNull(TEXT("Lumen gather selector is registered"), FG)) return false;
    const FString PreviousHW = HW->GetString(), PreviousFG = FG->GetString();
    const auto HWPriority = static_cast<EConsoleVariableFlags>(HW->GetFlags() & ECVF_SetByMask);
    const auto FGPriority = static_cast<EConsoleVariableFlags>(FG->GetFlags() & ECVF_SetByMask);
    // Exercise the production scope against real renderer CVars. Each profile
    // must restore both values and their source priority, including PIE exit.
    for (const auto Profile : {EPokeMonsterGraphicsProfile::VariantC,
        EPokeMonsterGraphicsProfile::HardwareReference75, EPokeMonsterGraphicsProfile::Reference100})
    {
        TArray<FPokeMonsterEnvironmentCVarOverride> Scopes;
        P::ApplyLumenOverrides(Profile, Scopes);
        const int32 Expected = Profile == EPokeMonsterGraphicsProfile::VariantC ? 0 : 1;
        TestEqual(TEXT("Requested hardware path, unless user override"), HW->GetInt(), HWPriority > ECVF_SetByCode ? FCString::Atoi(*PreviousHW) : Expected);
        TestEqual(TEXT("Requested gather path, unless user override"), FG->GetInt(), FGPriority > ECVF_SetByCode ? FCString::Atoi(*PreviousFG) : Expected);
        for (auto& Scope : Scopes) Scope.Restore();
        TestEqual(TEXT("Previous hardware value restored"), HW->GetString(), PreviousHW);
        TestEqual(TEXT("Previous gather value restored"), FG->GetString(), PreviousFG);
        TestEqual(TEXT("Previous hardware priority restored"), HW->GetFlags() & ECVF_SetByMask, uint32(HWPriority));
        TestEqual(TEXT("Previous gather priority restored"), FG->GetFlags() & ECVF_SetByMask, uint32(FGPriority));
    }
    const FName UserTag(TEXT("GraphicsLumenScopeTest"));
    HW->Set(1, ECVF_SetByConsole, UserTag);
    TArray<FPokeMonsterEnvironmentCVarOverride> Scopes;
    P::ApplyLumenOverrides(EPokeMonsterGraphicsProfile::VariantC, Scopes);
    TestEqual(TEXT("Explicit user hardware override preserved"), HW->GetInt(), 1);
    TestFalse(TEXT("Profile does not own user override"), Scopes[0].bOwned);
    for (auto& Scope : Scopes) Scope.Restore();
    TestEqual(TEXT("Teardown leaves user override intact"), HW->GetInt(), 1);
    HW->Unset(ECVF_SetByConsole, UserTag);
    HW->ClearFlags(ECVF_SetByMask);
    HW->Set(*PreviousHW, HWPriority);
    TestEqual(TEXT("User gather priority also preserved"), FG->GetFlags() & ECVF_SetByMask, uint32(FGPriority));
    return true;
}
#endif
