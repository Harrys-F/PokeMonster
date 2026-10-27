#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "Scalability.h"
#include "../Development/PokeMonsterEnvironmentRenderProfile.h"
#include "PokeMonsterGraphicsProfile.generated.h"

class UGameUserSettings;
class UGameViewportClient;

UENUM()
enum class EPokeMonsterGraphicsProfile : uint8
{
    VariantC,
    Reference100
};

/** Rendering only. Uses UE scalability/user settings, never game saves or gameplay classes.
 * The editor's pre-PIE quality and viewport sizing are restored at world teardown.
 */
UCLASS(Config=PokeMonsterGraphics, DefaultConfig)
class POKEMONSTER_API UPokeMonsterGraphicsProfile final : public UWorldSubsystem
{
    GENERATED_BODY()
public:
    virtual void OnWorldBeginPlay(UWorld& InWorld) override;
    virtual void Deinitialize() override;
    virtual bool DoesSupportWorldType(EWorldType::Type WorldType) const override;

    UPROPERTY(Config)
    EPokeMonsterGraphicsProfile DefaultProfile = EPokeMonsterGraphicsProfile::VariantC;

    static bool ParseProfile(const FString& Text, EPokeMonsterGraphicsProfile& Out);
    static float ScreenPercentage(EPokeMonsterGraphicsProfile Profile);
    static void Configure(UGameUserSettings& Settings, EPokeMonsterGraphicsProfile Profile);
    void SelectProfile(EPokeMonsterGraphicsProfile Profile);
    void LogStatus() const;

private:
    void Release();
    bool bApplied = false;
    EPokeMonsterGraphicsProfile CurrentProfile = EPokeMonsterGraphicsProfile::VariantC;
    Scalability::FQualityLevels PreviousQuality, PreviousUserQuality, AppliedQuality;
    FIntPoint PreviousResolution = FIntPoint::ZeroValue;
    int32 PreviousWindowMode = 2;
    bool bPreviousDynamicResolution = false;
    TWeakObjectPtr<UGameUserSettings> Settings;
    TWeakObjectPtr<UGameViewportClient> ViewportClient;
    TArray<FPokeMonsterEnvironmentCVarOverride> Overrides;
};
