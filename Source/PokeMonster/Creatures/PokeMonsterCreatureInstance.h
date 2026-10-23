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
	/** Technical creation/learning hook, never a player-facing loadout editor. */
	bool AssignMove(int32 SlotIndex, UPokeMonsterMoveData* Move);
	bool ConsumeMovePP(int32 SlotIndex, int32 Amount = 1);
	const TArray<FPokeMonsterMoveSlot>& GetLearnedMoves() const { return LearnedMoves; }
	/** Save transport: validates uniqueness, PP bounds and active membership atomically. */
	bool RestoreLearnedMoves(const TArray<FPokeMonsterMoveSlot>& Moves);
	/** Restore only mutable data; species stats are recalculated from the asset. */
	bool RestoreIndividualState(const FGuid& InId, int32 InLevel, int64 InExperience,
		int32 InCurrentHP, const TArray<FPokeMonsterMoveSlot>& InSlots, EPokeMonsterCreatureStatus InStatus = EPokeMonsterCreatureStatus::None, int32 InStatusTurns = 0);
	/** Fully restores HP and the PP of assigned moves, including a fainted creature. */
	bool RestoreFully();

	static FPokeMonsterCreatureInstance CreateFromSpecies(
		UPokeMonsterCreatureSpeciesData* InSpecies,
		int32 RequestedLevel = 0);

	bool IsValid() const;

	/** Adds cumulative XP, caps at level 100; negative input or inconsistent data fails without mutation. */
	FPokeMonsterExperienceResult AddExperience(int64 Amount);
	int64 GetExperienceToNextLevel() const;
 /** Evolution preserves the individual's existing XP curve, including historical Glumanda saves. */
 EPokeMonsterGrowthRate GetExperienceGrowthRate() const;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Progression") bool bHasExperienceGrowthOverride=false;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Progression") EPokeMonsterGrowthRate ExperienceGrowthOverride=EPokeMonsterGrowthRate::MediumFast;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Evolution") FPrimaryAssetId PendingEvolutionTarget;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Evolution") int32 LastEvolutionOfferedLevel=0;
 /** Validate saved offer metadata against this species' routes without requiring the target model. */
 bool ValidateEvolutionState() const;
	int32 GetMaxHP() const { return CalculatedStats.MaxHP; }
	/** Explicit species opt-in; does not alter the generic factory contract. */
	bool AssignSpeciesMoves();
	bool UpgradeLegacyGlumandaMoves();
	/** INDEX_NONE declines only the first offer; 0..3 replaces exactly that slot. */
	bool ResolveMoveLearning(int32 SlotIndex);
	bool RestorePendingMoves(const TArray<TSoftObjectPtr<UPokeMonsterMoveData>>& Moves);
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Progression")
	TArray<TSoftObjectPtr<UPokeMonsterMoveData>> PendingMoves;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Creature") int32 StatusTurns = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Creature") EPokeMonsterCreatureStatus Status = EPokeMonsterCreatureStatus::None;

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
	friend class UPokeMonsterEncounterSubsystem;
 friend class UPokeMonsterCreatureProgression;
	friend class FMoveManagementV2Repertoire;
	/** Only the encounter subsystem's authorized NPC transaction may call this. */
	bool SetActiveLearnedMoves(const TArray<TSoftObjectPtr<UPokeMonsterMoveData>>& Moves);
	void RememberActiveMoves();
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Progression", meta=(AllowPrivateAccess="true"))
	TArray<FPokeMonsterMoveSlot> LearnedMoves;
	/** Exactly four individually owned slots. Explicit species learnsets may fill empty slots. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Creature", meta = (AllowPrivateAccess = "true"))
	TArray<FPokeMonsterMoveSlot> MoveSlots;
};
