#pragma once

#include "CoreMinimal.h"
#include "PokeMonsterExperienceView.h"
#include "PokeMonsterOverworldView.generated.h"

class UPokeMonsterItemData;
class UPokeMonsterMoveData;
class UPokeMonsterEncounterSubsystem;
class UPokeMonsterInventorySubsystem;
class UPokeMonsterQuestSubsystem;

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterRepertoireRow
{
 GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly) TSoftObjectPtr<UPokeMonsterMoveData> Move;
 UPROPERTY(BlueprintReadOnly) FText Name;
 UPROPERTY(BlueprintReadOnly) FText Type;
 UPROPERTY(BlueprintReadOnly) FText Effect;
 UPROPERTY(BlueprintReadOnly) int32 Power=0;
 UPROPERTY(BlueprintReadOnly) int32 Accuracy=0;
 UPROPERTY(BlueprintReadOnly) int32 CurrentPP=0;
 UPROPERTY(BlueprintReadOnly) int32 MaxPP=0;
 UPROPERTY(BlueprintReadOnly) int32 ActiveSlot=INDEX_NONE;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterOverworldTeamRow
{
	GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly) FPokeMonsterExperienceView Experience;
	UPROPERTY(BlueprintReadOnly) FGuid InstanceId;
	UPROPERTY(BlueprintReadOnly) FText Name;
	UPROPERTY(BlueprintReadOnly) int32 Level = 1;
	UPROPERTY(BlueprintReadOnly) int32 CurrentHP = 0;
	UPROPERTY(BlueprintReadOnly) int32 MaxHP = 0;
	UPROPERTY(BlueprintReadOnly) bool bKnockedOut = false;
 UPROPERTY(BlueprintReadOnly) TArray<FPokeMonsterRepertoireRow> Repertoire;
 UPROPERTY(BlueprintReadOnly) TArray<TSoftObjectPtr<UPokeMonsterMoveData>> ActiveMoves;
 UPROPERTY(BlueprintReadOnly) bool bPendingLearning=false;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterOverworldItemRow
{
	GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly) TSoftObjectPtr<UPokeMonsterItemData> Item;
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
	UPROPERTY(BlueprintReadOnly) FText WorldTimeLabel;
 UPROPERTY(BlueprintReadOnly) FText Notification;
	UPROPERTY(BlueprintReadOnly) FText ActiveQuestName;
	UPROPERTY(BlueprintReadOnly) FText ActiveQuestObjective;
};

class POKEMONSTER_API FPokeMonsterOverworldViewBuilder
{
public:
	static FPokeMonsterOverworldView Build(const UPokeMonsterEncounterSubsystem* Encounter,
		const UPokeMonsterInventorySubsystem* Inventory, const UPokeMonsterQuestSubsystem* Quests = nullptr);
};
