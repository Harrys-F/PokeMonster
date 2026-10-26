#pragma once

#include "CoreMinimal.h"
#include "Engine/AssetManager.h"
#include "GameFramework/SaveGame.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
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
 UPROPERTY() TArray<FPrimaryAssetId> PendingMoves;
 UPROPERTY() TArray<FPokeMonsterSavedMove> LearnedMoves;
 UPROPERTY() bool bHasExperienceGrowthOverride=false;
 UPROPERTY() EPokeMonsterGrowthRate ExperienceGrowthOverride=EPokeMonsterGrowthRate::MediumFast;
 UPROPERTY() FPrimaryAssetId PendingEvolutionTarget;
 UPROPERTY() int32 LastEvolutionOfferedLevel=0;
 UPROPERTY() int32 StatusTurns=0;
 UPROPERTY() EPokeMonsterCreatureStatus Status=EPokeMonsterCreatureStatus::None;
};

USTRUCT()
struct POKEMONSTER_API FPokeMonsterSavedItemStack
{
	GENERATED_BODY()
	UPROPERTY() FPrimaryAssetId ItemId;
	UPROPERTY() int32 Quantity = 0;
};

/** Independent manual-resume position; never substitutes for the defeat checkpoint. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterSavedPlayerLocation
{
 GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly) bool bHasPosition = false;
 UPROPERTY(BlueprintReadOnly) FName MapPackage;
 UPROPERTY(BlueprintReadOnly) FVector Location = FVector::ZeroVector;
 UPROPERTY(BlueprintReadOnly) FRotator Rotation = FRotator::ZeroRotator;
 UPROPERTY(BlueprintReadOnly) FVector FacingDirection = FVector::ForwardVector;
 UPROPERTY(BlueprintReadOnly) FName InteriorActor;
 UPROPERTY(BlueprintReadOnly) bool bRelocatedInterior = false;
 bool IsValid() const;
};

/** Versioned, engine-native snapshot of the GameInstance session state. */
UCLASS()
class POKEMONSTER_API UPokeMonsterSaveGame : public USaveGame
{
	GENERATED_BODY()
public:
	static constexpr int32 CurrentVersion = 9;
	UPROPERTY() int32 SaveVersion = CurrentVersion;
	UPROPERTY() TArray<FPokeMonsterSavedCreature> PlayerTeam;
	UPROPERTY() TArray<FPokeMonsterSavedItemStack> InventoryStacks;
	UPROPERTY() TArray<FName> DefeatedTrainerIds;
	UPROPERTY() TArray<FName> CompletedEncounterIds;
	UPROPERTY() FPokeMonsterCheckpointData ActiveCheckpoint;
 UPROPERTY() FPokeMonsterSavedPlayerLocation PlayerLocation;
	UPROPERTY() TArray<FPokeMonsterQuestProgress> QuestProgress;
	UPROPERTY() TArray<FName> CapturedSpeciesIds;
};
