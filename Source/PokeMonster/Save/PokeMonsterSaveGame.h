#pragma once

#include "CoreMinimal.h"
#include "Engine/AssetManager.h"
#include "GameFramework/SaveGame.h"
#include "PokeMonsterSaveGame.generated.h"

/** Only stable asset identities and mutable PP are stored, never move definitions. */
USTRUCT()
struct POKEMONSTER_API FPokeMonsterSavedMove
{
	GENERATED_BODY()
	UPROPERTY() FPrimaryAssetId MoveId;
	UPROPERTY() int32 CurrentPP = 0;
};

USTRUCT()
struct POKEMONSTER_API FPokeMonsterSavedCreature
{
	GENERATED_BODY()
	UPROPERTY() FGuid InstanceId;
	UPROPERTY() FPrimaryAssetId SpeciesId;
	UPROPERTY() int32 Level = 1;
	UPROPERTY() int64 Experience = 0;
	UPROPERTY() int32 CurrentHP = 0;
	UPROPERTY() TArray<FPokeMonsterSavedMove> Moves;
};

USTRUCT()
struct POKEMONSTER_API FPokeMonsterSavedItemStack
{
	GENERATED_BODY()
	UPROPERTY() FPrimaryAssetId ItemId;
	UPROPERTY() int32 Quantity = 0;
};

/** Versioned, engine-native snapshot of the GameInstance session state. */
UCLASS()
class POKEMONSTER_API UPokeMonsterSaveGame : public USaveGame
{
	GENERATED_BODY()
public:
	static constexpr int32 CurrentVersion = 1;
	UPROPERTY() int32 SaveVersion = CurrentVersion;
	UPROPERTY() TArray<FPokeMonsterSavedCreature> PlayerTeam;
	UPROPERTY() TArray<FPokeMonsterSavedItemStack> InventoryStacks;
	UPROPERTY() TArray<FName> DefeatedTrainerIds;
	UPROPERTY() TArray<FName> CompletedEncounterIds;
};
