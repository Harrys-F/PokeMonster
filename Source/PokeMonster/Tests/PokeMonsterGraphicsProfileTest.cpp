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
    TestTrue(TEXT("C selection"), P::ParseProfile(TEXT("C"), Choice));
    TestEqual(TEXT("C is 75%"), P::ScreenPercentage(Choice), 75.f);
    UGameUserSettings* User = NewObject<UGameUserSettings>();
    User->SetScreenResolution(FIntPoint(2560, 1440));
    User->SetFullscreenMode(EWindowMode::Windowed);
    const float DesiredDisplayScale = User->GetDefaultResolutionScale();
    const int32 AA = IConsoleManager::Get().FindConsoleVariable(TEXT("r.AntiAliasingMethod"))->GetInt();
    for (const auto Preset : {EPokeMonsterGraphicsProfile::VariantC, EPokeMonsterGraphicsProfile::Reference100})
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
#endif
