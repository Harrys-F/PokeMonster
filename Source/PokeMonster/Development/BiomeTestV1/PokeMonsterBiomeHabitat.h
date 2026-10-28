#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../../Game/PokeMonsterGameMode.h"
#include "PokeMonsterBiomeHabitat.generated.h"
class UBoxComponent;
class APokeMonsterBuildingCutaway;
class UPokeMonsterCreatureSpeciesData;
class APokeMonsterCreatureVisualActor;
class UPokeMonsterCreaturePresentationData;
class UPokeMonsterCreatureRoamingComponent;
class UMaterialInterface;
struct FCollisionQueryParams;
UENUM(BlueprintType)
enum class EPokeMonsterBiomeMedium : uint8 { Land, Amphibious, WaterOnly, Floating, Aerial };
USTRUCT(BlueprintType)
struct FPokeMonsterBiomeSpecimen
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TSoftObjectPtr<UPokeMonsterCreatureSpeciesData> Species;
 /** Optional test-only presentation override; species identity/save assets remain unchanged. */
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TSoftObjectPtr<UPokeMonsterCreaturePresentationData> PresentationOverride;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FVector LocalPosition=FVector::ZeroVector;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) int32 Seed=101;
 /** Explicit generic water marker, never masquerades as a real species or save instance. */
 UPROPERTY(EditAnywhere,BlueprintReadWrite) bool bWaterDiagnostic=false;
};
/** Opt-in test mode. Same character/camera/input; no battle UI, companion, save or progression. */
UCLASS()
class POKEMONSTER_API APokeMonsterBiomeTestGameMode : public APokeMonsterGameMode
{
 GENERATED_BODY()
public:
 APokeMonsterBiomeTestGameMode();
 virtual void StartPlay() override;
 /** Explicit PIE QA only, existing save transport switches to RAM before any gameplay is enabled. */
 UFUNCTION(BlueprintCallable,Category="Development|Biome") bool BeginIsolatedGameplayReview();
 UFUNCTION(BlueprintCallable,Category="Development|Biome") bool EndIsolatedGameplayReview();
 UFUNCTION(BlueprintPure,Category="Development|Biome") bool IsIsolatedGameplayReview()const{return bReviewActive;}
private:
 bool bReviewActive=false;
};
/** Placed configuration; runtime visuals reuse the existing roaming/path and animation systems. */
UCLASS()
class POKEMONSTER_API APokeMonsterBiomeHabitat : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterBiomeHabitat();
 virtual void BeginPlay() override;
 virtual void Tick(float Delta) override;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<UBoxComponent> Bounds;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString HabitatName;
 /** Optional same-map interior owner. Empty retains exclusion of all building interiors. */
 UPROPERTY(EditInstanceOnly,BlueprintReadWrite) TObjectPtr<APokeMonsterBuildingCutaway> InteriorOwner;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) EPokeMonsterBiomeMedium Medium=EPokeMonsterBiomeMedium::Land;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float WaterSurfaceZ=-20.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float WaterDraftCm=20.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float FloatClearanceCm=45.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float MinimumDepthCm=20.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ClearanceRadiusCm=20.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ActiveDistanceCm=3800.f;
 /** Natural production zones opt in; existing visual-only biome specimens remain unchanged. */
 UPROPERTY(EditAnywhere,BlueprintReadWrite) bool bAllowNaturalActivities=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) bool bAllowGroundFlight=false;
 /** Opt-in only: existing GroundHover cruise may cross low obstacles; takeoff/landing stay ground-safe. */
 UPROPERTY(EditAnywhere,BlueprintReadWrite) bool bAllowGroundFlightOverObstacles=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(ClampMin="10",ClampMax="200")) float AirCruiseSpeedCm=80.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(ClampMin="5")) float MinimumAirClearanceCm=20.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(ClampMin="50")) float MaximumAirClearanceCm=350.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FVector> TravelPoints;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FPokeMonsterBiomeSpecimen> Specimens;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TObjectPtr<UMaterialInterface> DiagnosticMaterial;
 UPROPERTY(Transient,BlueprintReadOnly) TArray<TObjectPtr<AActor>> RuntimeSpecimens;
 UPROPERTY(Transient,BlueprintReadOnly) int32 MediaTransitions=0;
 UPROPERTY(Transient,BlueprintReadOnly) int32 SuspendedCount=0;
 UFUNCTION(BlueprintPure) bool ContainsFootprint(FVector Point,float Radius) const;
 bool ContainsFlightColumn(const FVector& Point,float Height,const FBox& MeshBounds) const;
 bool ProjectFoot(const FVector& Point,float Radius,float HalfHeight,const FCollisionQueryParams& Query,FVector& Foot,float AirLiftCm=0.f) const;
 void IgnorePlayerWaterBarriers(FCollisionQueryParams& Query) const;
 static bool AirFootHeight(float Plane,float Floor,float Lift,float MinClearance,float MaxClearance,float& Foot);
 static bool MediumFootHeight(EPokeMonsterBiomeMedium Mode,float Floor,float Surface,float Draft,float FloatHeight,float MinDepth,float& Height);
private:
 UPROPERTY(Transient) TArray<TObjectPtr<UPokeMonsterCreatureRoamingComponent>> Movements;
 TArray<TWeakObjectPtr<AActor>> PlayerWaterBarriers;
 TArray<bool> WasSwimming;
 bool bRunning=false;
};
