#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PokeMonsterItemData.generated.h"

class UTexture2D;
class UPokeMonsterCaptureDeviceData;

UENUM(BlueprintType)
enum class EPokeMonsterItemCategory : uint8
{
	Capture, Healing, Battle, Evolution, KeyItem, Misc
};

/** Shared item definition. Consumable quantities belong to the inventory, never to this asset. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterItemData : public UPrimaryDataAsset
{
	GENERATED_BODY()
public:
	virtual FPrimaryAssetId GetPrimaryAssetId() const override;
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") bool IsConfigured() const;
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") FName GetInternalId() const { return InternalId; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") FText GetDisplayName() const { return DisplayName; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") FText GetDescription() const { return Description; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") UTexture2D* GetIcon() const { return Icon.LoadSynchronous(); }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") EPokeMonsterItemCategory GetCategory() const { return Category; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") int32 GetMaxStackSize() const { return MaxStackSize; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") bool CanUseInOverworld() const { return bUsableInOverworld; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") bool CanUseInBattle() const { return bUsableInBattle; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") int32 GetHealAmount() const { return HealAmount; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Item") UPokeMonsterCaptureDeviceData* GetCaptureDevice() const;

private:
	UPROPERTY(EditDefaultsOnly, Category="Identity") FName InternalId = NAME_None;
	UPROPERTY(EditDefaultsOnly, Category="Identity") FText DisplayName;
	UPROPERTY(EditDefaultsOnly, Category="Identity", meta=(MultiLine="true")) FText Description;
	UPROPERTY(EditDefaultsOnly, Category="Identity") EPokeMonsterItemCategory Category = EPokeMonsterItemCategory::Misc;
	UPROPERTY(EditDefaultsOnly, Category="Identity") TSoftObjectPtr<UTexture2D> Icon;
	UPROPERTY(EditDefaultsOnly, Category="Inventory", meta=(ClampMin="1")) int32 MaxStackSize = 99;
	UPROPERTY(EditDefaultsOnly, Category="Usage") bool bUsableInOverworld = false;
	UPROPERTY(EditDefaultsOnly, Category="Usage") bool bUsableInBattle = false;
	/** Existing capture-bonus asset is reused by BattleSession. */
	UPROPERTY(EditDefaultsOnly, Category="Usage|Capture", meta=(EditCondition="Category==EPokeMonsterItemCategory::Capture"))
	TSoftObjectPtr<UPokeMonsterCaptureDeviceData> CaptureDevice;
	UPROPERTY(EditDefaultsOnly, Category="Usage|Healing", meta=(ClampMin="0", EditCondition="Category==EPokeMonsterItemCategory::Healing"))
	int32 HealAmount = 0;
};
