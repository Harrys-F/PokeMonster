// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "PokeMonsterCreatureTypes.h"
#include "../Moves/PokeMonsterMoveSlot.h"
#include "PokeMonsterCreatureInstance.generated.h"

class UPokeMonsterCreatureSpeciesData;

/** Mutable data for one concrete creature. Species-wide values remain in the referenced data asset. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureInstance
{
	GENERATED_BODY()

public:
	static constexpr int32 MoveSlotCount = 4;
	FPokeMonsterCreatureInstance() { MoveSlots.SetNum(MoveSlotCount); }

	const TArray<FPokeMonsterMoveSlot>& GetMoveSlots() const { return MoveSlots; }
	bool AssignMove(int32 SlotIndex, UPokeMonsterMoveData* Move)
	{
		return SlotIndex < MoveSlotCount && MoveSlots.IsValidIndex(SlotIndex) && MoveSlots[SlotIndex].AssignMove(Move);
	}
	bool ConsumeMovePP(int32 SlotIndex, int32 Amount = 1)
	{
		return SlotIndex < MoveSlotCount && MoveSlots.IsValidIndex(SlotIndex) && MoveSlots[SlotIndex].ConsumePP(Amount);
	}
	/** Restore only mutable data; species stats are recalculated from the asset. */
	bool RestoreIndividualState(const FGuid& InId, int32 InLevel, int64 InExperience,
		int32 InCurrentHP, const TArray<FPokeMonsterMoveSlot>& InSlots);

	static FPokeMonsterCreatureInstance CreateFromSpecies(
		UPokeMonsterCreatureSpeciesData* InSpecies,
		int32 RequestedLevel = 0);

	bool IsValid() const;

	/** Adds cumulative XP, caps at level 100; negative input or inconsistent data fails without mutation. */
	FPokeMonsterExperienceResult AddExperience(int64 Amount);
	int64 GetExperienceToNextLevel() const;
	int32 GetMaxHP() const { return CalculatedStats.MaxHP; }

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Creature")
	FGuid InstanceId;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Creature")
	TSoftObjectPtr<UPokeMonsterCreatureSpeciesData> Species;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Creature", meta = (ClampMin = "1", ClampMax = "100"))
	int32 Level = 1;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Creature", meta = (ClampMin = "0"))
	int32 CurrentHP = 0;

	/** Cumulative experience, including the threshold for the starting level. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Creature", meta = (ClampMin = "0"))
	int64 Experience = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Creature")
	FPokeMonsterCreatureStats CalculatedStats;

private:
	/** Exactly four individually owned slots; no learning or automatic assignment. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Creature", meta = (AllowPrivateAccess = "true"))
	TArray<FPokeMonsterMoveSlot> MoveSlots;
};
