#pragma once

#include "CoreMinimal.h"
#include "PokeMonsterOverworldView.generated.h"

class UPokeMonsterEncounterSubsystem;
class UPokeMonsterInventorySubsystem;

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterOverworldTeamRow
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly) FText Name;
	UPROPERTY(BlueprintReadOnly) int32 Level = 1;
	UPROPERTY(BlueprintReadOnly) int32 CurrentHP = 0;
	UPROPERTY(BlueprintReadOnly) int32 MaxHP = 0;
	UPROPERTY(BlueprintReadOnly) bool bKnockedOut = false;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterOverworldItemRow
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly) FText Name;
	UPROPERTY(BlueprintReadOnly) FText Category;
	UPROPERTY(BlueprintReadOnly) int32 Quantity = 0;
};

/** Read-only UI snapshot; the inventory and encounter subsystems retain ownership of gameplay state. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterOverworldView
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly) TArray<FPokeMonsterOverworldTeamRow> Team;
	UPROPERTY(BlueprintReadOnly) TArray<FPokeMonsterOverworldItemRow> Inventory;
};

class POKEMONSTER_API FPokeMonsterOverworldViewBuilder
{
public:
	static FPokeMonsterOverworldView Build(const UPokeMonsterEncounterSubsystem* Encounter,
		const UPokeMonsterInventorySubsystem* Inventory);
};
