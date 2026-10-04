#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterBuildingCutaway.generated.h"

class UBoxComponent;
class APokeMonsterPlayerCharacter;
class APawn;
struct FMinimalViewInfo;
class UPrimitiveComponent;

/** Optional box in InteriorArea-local centimetres; multiple boxes form one room footprint. */
USTRUCT(BlueprintType)
struct FPokeMonsterBuildingInteriorRegion
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building") FVector Center = FVector::ZeroVector;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building", meta=(ClampMin="0.0")) FVector Extent = FVector(100.f);
};

/** Doorway-driven visual cutaway; never changes gameplay collision. */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterBuildingCutaway : public AActor
{
	GENERATED_BODY()
public:
	APokeMonsterBuildingCutaway();
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Building") TObjectPtr<UBoxComponent> InteriorArea;
	/** Empty preserves the original InteriorArea box. Non-empty supports joined/L-shaped rooms. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building") TArray<FPokeMonsterBuildingInteriorRegion> InteriorRegions;
	/** Local +X points into the building. This box never generates gameplay overlaps. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Building") TObjectPtr<UBoxComponent> DoorThreshold;
	/** Optional same-map room. Both doors must share their inward orientation and unit scale. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Relocated Interior") bool bUseRelocatedInterior = false;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Building|Relocated Interior") TObjectPtr<UBoxComponent> RelocatedInteriorArea;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Building|Relocated Interior") TObjectPtr<UBoxComponent> RelocatedDoorThreshold;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Relocated Interior") FVector RelocatedCameraTarget = FVector(0.f, 0.f, -70.f);
	/** Short blackout around the midpoint; the two spatial camera views never interpolate. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Relocated Interior", meta=(ClampMin="0.05", ClampMax="0.5")) float RelocationMaskHalfWidth = .2f;
	UFUNCTION(BlueprintPure, Category="Building|Relocated Interior") bool IsViewerInRelocatedRoom(FVector WorldLocation) const;
	UFUNCTION(BlueprintPure, Category="Building|Relocated Interior") bool IsViewerRelocated() const { return bViewerRelocated; }
	UFUNCTION(BlueprintPure, Category="Building|Relocated Interior") float GetRelocationMask() const;
	/** Absolute doorway-relative mapping preserves depth/lateral offset; no accumulated delta. */
	FVector MapDoorwayPosition(FVector WorldLocation, bool bEntering) const;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building", meta=(ClampMin="0.05")) float FadeDuration = 0.4f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building", meta=(ClampMin="0.0", ClampMax="10.0")) float ThresholdHysteresis = 4.f;
	/** Roof and camera-facing facade parts; rear walls and functional actors stay visible. */
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Building") TArray<TObjectPtr<AActor>> OccludingActors;
	/** Opt-in: existing healing houses retain their original camera. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Interior Camera") bool bUseInteriorCamera = false;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Interior Camera", meta=(ClampMin="100.0")) float InteriorCameraDistance = 1600.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Interior Camera", meta=(ClampMin="-80.0", ClampMax="-10.0")) float InteriorCameraPitch = -50.f;
	/** Relative to the doorway's local inward +X axis. Zero gives a frontal view. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Interior Camera") float InteriorCameraYawOffset = 0.f;
	/** Room-local look-at point; default is 80 cm above a 150-cm root. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building|Interior Camera") FVector InteriorCameraTarget = FVector(0.f, 0.f, -70.f);
	void GetInteriorCameraView(FMinimalViewInfo& OutView) const;
	UFUNCTION(BlueprintPure, Category="Building") bool IsViewerInside(FVector WorldLocation) const;
	UFUNCTION(BlueprintPure, Category="Building") bool IsViewerInDoorway(FVector WorldLocation) const;
	UFUNCTION(BlueprintPure, Category="Building") bool IsCutawayActive() const { return bCutawayActive; }
	UFUNCTION(BlueprintPure, Category="Building") float GetCutawayAmount() const { return CutawayAmount; }
	virtual void Tick(float DeltaSeconds) override;
protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
	TWeakObjectPtr<APokeMonsterPlayerCharacter> CameraViewer;
	void RefreshVisibility(float DeltaSeconds);
	void UpdateRelocation(APawn* Player, bool bInside, float DeltaSeconds);
	void ApplyRelocationMask(APawn* Player);
	void ApplyVisibility();
	TMap<TWeakObjectPtr<AActor>, bool> OriginalHiddenStates;
	TMap<TWeakObjectPtr<UPrimitiveComponent>, float> OriginalFadeData;
	UPROPERTY(Transient, VisibleInstanceOnly, BlueprintReadOnly, Category="Building", meta=(AllowPrivateAccess="true"))
	float CutawayAmount = 0.f;
	UPROPERTY(Transient, VisibleInstanceOnly, BlueprintReadOnly, Category="Building", meta=(AllowPrivateAccess="true"))
	bool bCutawayActive = false;
	bool bViewerInitialized = false;
	bool bViewerRelocated = false;
	bool bMidpointArmed = false;
	bool bOwnsCameraMask = false;
	bool bRelocationRejected = false;
};
