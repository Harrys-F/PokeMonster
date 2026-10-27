#include "PokeMonsterGraphicsProfile.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "GameFramework/GameUserSettings.h"
#include "HAL/IConsoleManager.h"
#include "Misc/App.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Slate/SceneViewport.h"

namespace
{
    TWeakObjectPtr<UPokeMonsterGraphicsProfile> Owner;
    TOptional<EPokeMonsterGraphicsProfile> SessionChoice;
    constexpr int32 OutputX = 2560, OutputY = 1440;
}

bool UPokeMonsterGraphicsProfile::DoesSupportWorldType(EWorldType::Type Type) const
{
    return Type == EWorldType::Game || Type == EWorldType::PIE;
}

bool UPokeMonsterGraphicsProfile::ParseProfile(const FString& Text, EPokeMonsterGraphicsProfile& Out)
{
    if (Text.Equals(TEXT("C"), ESearchCase::IgnoreCase) || Text == TEXT("75"))
    { Out = EPokeMonsterGraphicsProfile::VariantC; return true; }
    if (Text == TEXT("100") || Text.Equals(TEXT("Reference100"), ESearchCase::IgnoreCase))
    { Out = EPokeMonsterGraphicsProfile::Reference100; return true; }
    return false;
}

float UPokeMonsterGraphicsProfile::ScreenPercentage(EPokeMonsterGraphicsProfile Profile)
{
    return Profile == EPokeMonsterGraphicsProfile::VariantC ? 75.f : 100.f;
}

void UPokeMonsterGraphicsProfile::Configure(UGameUserSettings& User, EPokeMonsterGraphicsProfile Profile)
{
    User.SetScreenResolution(FIntPoint(OutputX, OutputY));
    User.SetFullscreenMode(EWindowMode::Windowed);
    User.SetOverallScalabilityLevel(2);
    // The public quality cache controls the profile without changing the user's
    // DesiredScreenWidth/Height used by later editor display-mode changes.
    User.ScalabilityQuality.ResolutionQuality = ScreenPercentage(Profile);
    User.SetDynamicResolutionEnabled(false);
}

void UPokeMonsterGraphicsProfile::OnWorldBeginPlay(UWorld& InWorld)
{
    Super::OnWorldBeginPlay(InWorld);
    if (!FApp::CanEverRender() || IsRunningCommandlet() || !GEngine
        || !InWorld.GetGameInstance() || !InWorld.GetGameInstance()->GetGameViewportClient()) return;
    auto Profile = SessionChoice.Get(DefaultProfile);
    FString Requested;
    if (FParse::Value(FCommandLine::Get(), TEXT("PMGraphicsProfile="), Requested))
    {
        if (!ParseProfile(Requested, Profile))
            UE_LOG(LogTemp, Warning, TEXT("GRAPHICS_PROFILE invalid command-line choice; using configured default"));
    }
    SelectProfile(Profile);
}

void UPokeMonsterGraphicsProfile::SelectProfile(EPokeMonsterGraphicsProfile Profile)
{
    UWorld* World = GetWorld();
    if (!GEngine || !World || !World->IsGameWorld() || !World->GetGameInstance()) return;
    UGameViewportClient* Client = World->GetGameInstance()->GetGameViewportClient();
    if (!Client || !Client->GetGameViewport()) return;
    // A travel destination may begin before the previous world is destroyed.
    if (Owner.IsValid() && Owner.Get() != this) Owner->Release();
    if (bApplied) Release();
    UGameUserSettings* User = GEngine->GetGameUserSettings();
    if (!User) return;
    Owner = this; Settings = User; ViewportClient = Client;
    PreviousQuality = Scalability::GetQualityLevels();
    PreviousUserQuality = User->ScalabilityQuality;
    PreviousResolution = User->GetScreenResolution();
    PreviousWindowMode = int32(User->GetFullscreenMode());
    bPreviousDynamicResolution = User->IsDynamicResolutionEnabled();
    IConsoleVariable* Screen = IConsoleManager::Get().FindConsoleVariable(TEXT("r.ScreenPercentage"));
    const FString PreviousScreenValue = Screen->GetString();
    const auto PreviousScreenPriority = static_cast<EConsoleVariableFlags>(Screen->GetFlags() & ECVF_SetByMask);
    Configure(*User, Profile);
    AppliedQuality = User->ScalabilityQuality;
    Scalability::SetQualityLevels(AppliedQuality);
    const FString Percentage = FString::FromInt(int32(ScreenPercentage(Profile)));
    auto& ScreenScope = Overrides.AddDefaulted_GetRef();
    ScreenScope.Apply(TEXT("r.ScreenPercentage"), *Percentage);
    // Scalability can change this CVar before our explicit rendering override.
    ScreenScope.PreviousValue = PreviousScreenValue;
    ScreenScope.PreviousPriority = PreviousScreenPriority;
    Overrides.AddDefaulted_GetRef().Apply(TEXT("r.DynamicRes.OperationMode"), TEXT("0"));
    Overrides.AddDefaulted_GetRef().Apply(TEXT("r.SecondaryScreenPercentage.GameViewport"), TEXT("100"));
    Overrides.AddDefaulted_GetRef().Apply(TEXT("r.Editor.Viewport.OverridePIEScreenPercentage"), TEXT("0"));
    // VisualV2 already selects native TAA through its existing map blendable.
    Overrides.AddDefaulted_GetRef().Apply(TEXT("r.TemporalAA.Upsampling"), TEXT("1"));
    // Measured VisualV2-only sampling budget. Preserve the old 100% reference,
    // other maps and higher-priority user overrides through the existing scope.
    if (Profile == EPokeMonsterGraphicsProfile::VariantC
        && UWorld::RemovePIEPrefix(World->GetPackage()->GetName()) == TEXT("/Game/Maps/Dev_TestMap_VisualV2"))
        Overrides.AddDefaulted_GetRef().Apply(TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"), TEXT("4"));
    if (World->WorldType == EWorldType::Game) User->ApplyResolutionSettings(true);
    Client->GetGameViewport()->SetFixedViewportSize(OutputX, OutputY);
    CurrentProfile = Profile; bApplied = true;
    LogStatus();
    // No ApplySettings/SaveSettings: no automatic user-config or game-save write.
}

void UPokeMonsterGraphicsProfile::Release()
{
    if (!bApplied) return;
    IConsoleVariable* Screen = IConsoleManager::Get().FindConsoleVariable(TEXT("r.ScreenPercentage"));
    const auto ScreenScope = Overrides[0];
    const bool bRestoreQuality = Scalability::GetQualityLevels() == AppliedQuality;
    const bool bRestoreScreen = ScreenScope.bOwned && Screen->GetString() == ScreenScope.AppliedValue
        && (Screen->GetFlags() & ECVF_SetByMask) == ECVF_SetByCode;
    for (auto& Scope : Overrides) Scope.Restore();
    Overrides.Empty();
    if (bRestoreQuality) Scalability::SetQualityLevels(PreviousQuality);
    // The previous scalability callback may also write ScreenPercentage. Restore
    // its exact pre-PIE value/priority only while we still owned both settings.
    if (bRestoreQuality && bRestoreScreen)
    {
        Screen->ClearFlags(ECVF_SetByMask);
        Screen->Set(*ScreenScope.PreviousValue, ScreenScope.PreviousPriority);
    }
    if (UGameUserSettings* User = Settings.Get())
    {
        const bool bRestoreUserQuality = User->ScalabilityQuality == AppliedQuality;
        if (User->GetScreenResolution() == FIntPoint(OutputX, OutputY)) User->SetScreenResolution(PreviousResolution);
        if (User->GetFullscreenMode() == EWindowMode::Windowed) User->SetFullscreenMode(EWindowMode::Type(PreviousWindowMode));
        if (!User->IsDynamicResolutionEnabled()) User->SetDynamicResolutionEnabled(bPreviousDynamicResolution);
        if (bRestoreUserQuality) User->ScalabilityQuality = PreviousUserQuality;
    }
    if (auto* Client = ViewportClient.Get())
        if (auto* Viewport = Client->GetGameViewport()) Viewport->SetFixedViewportSize(0, 0);
    if (Owner.Get() == this) Owner.Reset();
    Settings.Reset(); ViewportClient.Reset(); bApplied = false;
}

void UPokeMonsterGraphicsProfile::Deinitialize()
{
    Release();
    Super::Deinitialize();
}

void UPokeMonsterGraphicsProfile::LogStatus() const
{
    const auto* SP = IConsoleManager::Get().FindConsoleVariable(TEXT("r.ScreenPercentage"));
    const auto* Client = ViewportClient.Get();
    const FIntPoint Size = Client && Client->GetGameViewport() ? Client->GetGameViewport()->GetSizeXY() : FIntPoint::ZeroValue;
    UE_LOG(LogTemp, Display, TEXT("GRAPHICS_PROFILE %s requested=%.0f effective=%.2f output=%dx%d High=2 TAAUpsampling=1; renderer measurement required for internal pixels"),
        CurrentProfile == EPokeMonsterGraphicsProfile::VariantC ? TEXT("C") : TEXT("Reference100"),
        ScreenPercentage(CurrentProfile), SP ? SP->GetFloat() : -1.f, Size.X, Size.Y);
}

namespace
{
    FAutoConsoleCommandWithWorldAndArgs Select(TEXT("pm.Graphics"),
        TEXT("C: 1440p High 75% TAAU. 100: native 1440p High comparison. status: actual settings. Session-only; no save writes."),
        FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args, UWorld* World)
    {
        auto* Profile = World ? World->GetSubsystem<UPokeMonsterGraphicsProfile>() : nullptr;
        if (!Profile) return;
        if (Args.Num() == 0 || Args[0].Equals(TEXT("status"), ESearchCase::IgnoreCase)) { Profile->LogStatus(); return; }
        EPokeMonsterGraphicsProfile Choice;
        if (!UPokeMonsterGraphicsProfile::ParseProfile(Args[0], Choice))
        { UE_LOG(LogTemp, Display, TEXT("Usage: pm.Graphics C | 100 | status")); return; }
        SessionChoice = Choice;
        Profile->SelectProfile(Choice);
    }));
}
