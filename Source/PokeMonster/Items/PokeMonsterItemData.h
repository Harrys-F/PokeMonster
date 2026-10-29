#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PokeMonsterItemData.generated.h"

class UTexture2D;
class UStaticMesh;
struct FPokeMonsterCreatureInstance;

UENUM(BlueprintType)
enum class EPokeMonsterMedicineEffect : uint8 { RestoreHP, CureStatus, Revive, RestorePP };
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

/** One pure effect evaluator shared by battle, overworld and target previews. No consumption. */
 bool ApplyMedicine(FPokeMonsterCreatureInstance& Creature, int32 MoveSlot = INDEX_NONE) const;
 bool CuresConfusion() const { return Category==EPokeMonsterItemCategory::Healing&&MedicineEffect==EPokeMonsterMedicineEffect::CureStatus&&bAllStatuses; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|Item") bool NeedsMoveTarget() const { return MedicineEffect==EPokeMonsterMedicineEffect::RestorePP && !bAllMoves; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|Item") bool CanDiscard() const { return Category!=EPokeMonsterItemCategory::KeyItem && !bProtectedItem; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|Item") bool IsConsumedOnUse() const { return bConsumeOnUse; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|Item") UStaticMesh* GetWorldMesh() const;
private:
 UPROPERTY(EditDefaultsOnly, Category="Usage|Medicine") EPokeMonsterMedicineEffect MedicineEffect=EPokeMonsterMedicineEffect::RestoreHP;
 /** Restore all HP/PP, or fully revive. Otherwise HealAmount / RestorePPAmount / half HP. */
 UPROPERTY(EditDefaultsOnly, Category="Usage|Medicine") bool bFullRestore=false;
 UPROPERTY(EditDefaultsOnly, Category="Usage|Medicine") bool bAllStatuses=false;
 UPROPERTY(EditDefaultsOnly, Category="Usage|Medicine") uint8 CuredStatus=0;
 UPROPERTY(EditDefaultsOnly, Category="Usage|Medicine") bool bAllMoves=false;
 UPROPERTY(EditDefaultsOnly, Category="Usage|Medicine",meta=(ClampMin="0")) int32 RestorePPAmount=0;
 UPROPERTY(EditDefaultsOnly, Category="Usage") bool bConsumeOnUse=true;
 UPROPERTY(EditDefaultsOnly, Category="Inventory") bool bProtectedItem=false;
 UPROPERTY(EditDefaultsOnly, Category="Inventory",meta=(ClampMin="0")) int32 SellValue=0;
 UPROPERTY(EditDefaultsOnly, Category="Identity") TSoftObjectPtr<UStaticMesh> WorldMesh;
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
