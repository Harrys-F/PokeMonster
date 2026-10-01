#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterBuildingCutaway.generated.h"

class UBoxComponent;

/** Small building-specific cutaway: visibility only, with no changes to gameplay collision. */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterBuildingCutaway : public AActor
{
	GENERATED_BODY()
public:
	APokeMonsterBuildingCutaway();
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Building") TObjectPtr<UBoxComponent> InteriorArea;
	/** Roof and camera-facing facade parts; rear walls and functional actors stay visible. */
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Building") TArray<TObjectPtr<AActor>> OccludingActors;
	UFUNCTION(BlueprintPure, Category="Building") bool IsViewerInside(FVector WorldLocation) const;
	UFUNCTION(BlueprintPure, Category="Building") bool IsCutawayActive() const { return bCutawayActive; }
	virtual void Tick(float DeltaSeconds) override;
protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
	void RefreshVisibility();
	void ApplyVisibility(bool bInside);
	TMap<TWeakObjectPtr<AActor>, bool> OriginalHiddenStates;
	bool bCutawayActive = false;
};
