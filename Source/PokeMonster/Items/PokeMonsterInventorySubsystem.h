#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterItemData.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "PokeMonsterInventorySubsystem.generated.h"

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterInventoryStack
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Inventory") TSoftObjectPtr<UPokeMonsterItemData> Item;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Inventory", meta=(ClampMin="1")) int32 Quantity = 0;
};

/** Existing session inventory; SaveGame V2 transports stable item identities and stacks. */
UCLASS()
class POKEMONSTER_API UPokeMonsterInventorySubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Inventory") bool AddItem(const UPokeMonsterItemData* Item, int32 Quantity);
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Inventory") bool RemoveItem(const UPokeMonsterItemData* Item, int32 Quantity);
	UFUNCTION(BlueprintPure, Category="PokeMonster|Inventory") int32 GetQuantity(const UPokeMonsterItemData* Item) const;
	UFUNCTION(BlueprintPure, Category="PokeMonster|Inventory") bool HasItem(const UPokeMonsterItemData* Item, int32 Quantity = 1) const;
	UFUNCTION(BlueprintPure, Category="PokeMonster|Inventory") const TArray<FPokeMonsterInventoryStack>& GetStacks() const { return Stacks; }
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Inventory") bool RestoreStacks(const TArray<FPokeMonsterInventoryStack>& SavedStacks);
	/** Shared overworld medicine; only an eligible, effective use consumes stock. */
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Inventory") bool UseHealingItem(const UPokeMonsterItemData* Item,
		UPARAM(ref) FPokeMonsterCreatureInstance& Creature,int32 MoveSlot=-1);
 UFUNCTION(BlueprintCallable,Category="PokeMonster|Inventory") bool DiscardItem(const UPokeMonsterItemData* Item,int32 Quantity);
 /** Stable source IDs reuse persisted world flags. Atomic item/reward/pickup transaction. */
 UFUNCTION(BlueprintCallable,Category="PokeMonster|Inventory") bool CollectItem(const UPokeMonsterItemData* Item,int32 Quantity,FName SourceId);
 UFUNCTION(BlueprintPure,Category="PokeMonster|Inventory") FText GetNotification() const;
 void Notify(const FString& Message);
 /** Zero preserves the existing unbounded gameplay capacity. Optional authoring/test limit. */
 UPROPERTY(Transient,EditAnywhere,BlueprintReadWrite,Category="Inventory") int32 MaxStackSlots=0;

private:
 FText Notification;
 double NotificationUntil=0;
 bool bTransactionActive=false;
	UPROPERTY(Transient) TArray<FPokeMonsterInventoryStack> Stacks;
};
