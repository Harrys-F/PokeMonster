#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PokeMonsterCaptureDeviceData.generated.h"

/** Reusable capture item data. Inventory and item consumption are intentionally separate. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterCaptureDeviceData : public UPrimaryDataAsset
{
	GENERATED_BODY()
public:
	virtual FPrimaryAssetId GetPrimaryAssetId() const override;
	UFUNCTION(BlueprintPure, Category="PokeMonster|Capture") bool IsConfigured() const;
	UFUNCTION(BlueprintPure, Category="PokeMonster|Capture") FName GetInternalId() const { return InternalId; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Capture") FText GetDisplayName() const { return DisplayName; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Capture") float GetCaptureBonus() const { return CaptureBonus; }
private:
	UPROPERTY(EditDefaultsOnly, Category="Capture") FName InternalId = NAME_None;
	UPROPERTY(EditDefaultsOnly, Category="Capture") FText DisplayName;
	UPROPERTY(EditDefaultsOnly, Category="Capture", meta=(ClampMin="0.01")) float CaptureBonus = 1.0f;
};
