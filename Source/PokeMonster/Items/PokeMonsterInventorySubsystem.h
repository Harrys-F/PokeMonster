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

/** Session inventory. Get/restore stacks form the handoff for a future SaveGame. */
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
	/** Out-of-battle healing; never revives a KO creature or consumes an item without healing. */
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Inventory") bool UseHealingItem(const UPokeMonsterItemData* Item,
		UPARAM(ref) FPokeMonsterCreatureInstance& Creature);

private:
	UPROPERTY(Transient) TArray<FPokeMonsterInventoryStack> Stacks;
};
