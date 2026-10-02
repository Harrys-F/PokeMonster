#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterBuildingCutaway.generated.h"

class UBoxComponent;
class UPrimitiveComponent;

/** Doorway-driven visual cutaway; never changes gameplay collision. */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterBuildingCutaway : public AActor
{
	GENERATED_BODY()
public:
	APokeMonsterBuildingCutaway();
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Building") TObjectPtr<UBoxComponent> InteriorArea;
	/** Local +X points into the building. This box never generates gameplay overlaps. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Building") TObjectPtr<UBoxComponent> DoorThreshold;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building", meta=(ClampMin="0.05")) float FadeDuration = 0.4f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Building", meta=(ClampMin="0.0", ClampMax="10.0")) float ThresholdHysteresis = 4.f;
	/** Roof and camera-facing facade parts; rear walls and functional actors stay visible. */
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Building") TArray<TObjectPtr<AActor>> OccludingActors;
	UFUNCTION(BlueprintPure, Category="Building") bool IsViewerInside(FVector WorldLocation) const;
	UFUNCTION(BlueprintPure, Category="Building") bool IsViewerInDoorway(FVector WorldLocation) const;
	UFUNCTION(BlueprintPure, Category="Building") bool IsCutawayActive() const { return bCutawayActive; }
	UFUNCTION(BlueprintPure, Category="Building") float GetCutawayAmount() const { return CutawayAmount; }
	virtual void Tick(float DeltaSeconds) override;
protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
	void RefreshVisibility(float DeltaSeconds);
	void ApplyVisibility();
	TMap<TWeakObjectPtr<AActor>, bool> OriginalHiddenStates;
	TMap<TWeakObjectPtr<UPrimitiveComponent>, float> OriginalFadeData;
	UPROPERTY(Transient, VisibleInstanceOnly, BlueprintReadOnly, Category="Building", meta=(AllowPrivateAccess="true"))
	float CutawayAmount = 0.f;
	UPROPERTY(Transient, VisibleInstanceOnly, BlueprintReadOnly, Category="Building", meta=(AllowPrivateAccess="true"))
	bool bCutawayActive = false;
	bool bViewerInitialized = false;
};
