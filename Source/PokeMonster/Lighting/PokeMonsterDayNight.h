#pragma once
#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "../Time/PokeMonsterWorldClock.h"
#include "PokeMonsterDayNight.generated.h"
class UDirectionalLightComponent;
class UStaticMesh;
class UMaterialInterface;
class UMaterialInstanceDynamic;
class AStaticMeshActor;

UENUM(BlueprintType)
enum class EPokeMonsterNoonSun : uint8 { B75, C85 };

/** A lighting sample, never a second clock. Time is supplied by WorldClock V1. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterDayNightSample
{
 GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly) float SunElevation=0;
 UPROPERTY(BlueprintReadOnly) float SunAzimuth=0;
 UPROPERTY(BlueprintReadOnly) FRotator LightRotation=FRotator::ZeroRotator;
 UPROPERTY(BlueprintReadOnly) float DirectIntensity=0;
 UPROPERTY(BlueprintReadOnly) float FillIntensity=0;
 UPROPERTY(BlueprintReadOnly) float Temperature=5700;
 UPROPERTY(BlueprintReadOnly) float Stars=0;
 UPROPERTY(BlueprintReadOnly) FLinearColor Zenith=FLinearColor::Black;
 UPROPERTY(BlueprintReadOnly) FLinearColor Horizon=FLinearColor::Black;
 UPROPERTY(BlueprintReadOnly) EPokeMonsterDayPhase Phase=EPokeMonsterDayPhase::Day;
};

UCLASS(Config=Game,DefaultConfig)
class POKEMONSTER_API UPokeMonsterDayNightSettings : public UObject
{
 GENERATED_BODY()
public:
 /** Provisional recommendation only. Both requested comparison candidates remain available. */
 UPROPERTY(Config,EditAnywhere) EPokeMonsterNoonSun NoonVariant=EPokeMonsterNoonSun::B75;
 UPROPERTY(Config,EditAnywhere) float NoonAzimuth=-100;
 UPROPERTY(Config,EditAnywhere) float UpdateSeconds=.1f;
 UPROPERTY(Config,EditAnywhere) float DayDirectIntensity=7.5f;
 UPROPERTY(Config,EditAnywhere) float DayFillIntensity=1.8f;
 UPROPERTY(Config,EditAnywhere) float MoonIntensity=.5f;
 UPROPERTY(Config,EditAnywhere) float NightFillIntensity=.9f;
 UPROPERTY(Config,EditAnywhere) FName SunActor=TEXT("DirectionalLight_1");
 UPROPERTY(Config,EditAnywhere) FName FillActor=TEXT("DirectionalLight_0");
 bool IsValidConfiguration() const;
 FPokeMonsterDayNightSample Evaluate(double DayFraction,EPokeMonsterNoonSun Variant,
  const UPokeMonsterWorldClockSettings& ClockSettings) const;
 static float MaximumElevation(EPokeMonsterNoonSun Variant) { return Variant==EPokeMonsterNoonSun::C85?85.f:75.f; }
};

/** VisualV2-only controller: existing lights + one cheap Engine sky dome, no map writes. */
UCLASS()
class POKEMONSTER_API UPokeMonsterDayNightSubsystem : public UWorldSubsystem
{
 GENERATED_BODY()
public:
 UPokeMonsterDayNightSubsystem();
 virtual void OnWorldBeginPlay(UWorld& World) override;
 virtual void Deinitialize() override;
 static bool IsTargetMap(const FString& PackageName);
 UFUNCTION(BlueprintPure,Category="PokeMonster|Day Night") FPokeMonsterDayNightSample GetLightingSample() const { return LastSample; }
 UFUNCTION(BlueprintPure,Category="PokeMonster|Day Night") bool IsCycleEnabled() const { return bEnabled; }
 UFUNCTION(BlueprintCallable,Category="PokeMonster|Day Night") void SetCycleEnabled(bool Enabled);
 UFUNCTION(BlueprintCallable,Category="PokeMonster|Day Night") void SetNoonVariant(EPokeMonsterNoonSun Variant);
 UFUNCTION(BlueprintPure,Category="PokeMonster|Day Night") EPokeMonsterNoonSun GetNoonVariant() const { return NoonVariant; }
 UFUNCTION(BlueprintPure,Category="PokeMonster|Day Night") bool IsSkyReady() const { return SkyMID!=nullptr; }
 UFUNCTION(BlueprintCallable,Category="PokeMonster|Day Night") void RefreshLighting();
protected:
 virtual bool DoesSupportWorldType(EWorldType::Type Type) const override;
private:
 UFUNCTION() void HandleTimeSet(FPokeMonsterWorldTime Time);
 void UpdateFromClock();
 void RestoreLights();
 UPROPERTY(Transient) TObjectPtr<UPokeMonsterWorldClock> Clock;
 UPROPERTY(Transient) TObjectPtr<UDirectionalLightComponent> Sun;
 UPROPERTY(Transient) TObjectPtr<UDirectionalLightComponent> Fill;
 UPROPERTY(Transient) TObjectPtr<AStaticMeshActor> Sky;
 UPROPERTY(Transient) TObjectPtr<UMaterialInstanceDynamic> SkyMID;
 UPROPERTY() TObjectPtr<UStaticMesh> SkyMeshAsset;
 UPROPERTY() TObjectPtr<UMaterialInterface> SkyMaterialAsset;
 UPROPERTY(Transient) FPokeMonsterDayNightSample LastSample;
 FTimerHandle UpdateTimer;
 FRotator OriginalSunRotation;
 float OriginalSunIntensity=0,OriginalSunTemperature=0,OriginalFillIntensity=0;
 bool OriginalSunTemperatureEnabled=false,bBound=false,bEnabled=false;
 EPokeMonsterNoonSun NoonVariant=EPokeMonsterNoonSun::B75;
 double LastSeconds=-1;
};
