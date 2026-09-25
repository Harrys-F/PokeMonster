#include "PokeMonsterEncounterProfile.h"

#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"

bool FPokeMonsterWildEncounterEntry::Matches(const FPokeMonsterEncounterContext& Context) const
{
	return Weight > 0 && MinLevel >= 1 && MaxLevel <= 100 && MaxLevel >= MinLevel
		&& !Species.IsNull() && !Moves.IsEmpty() && Moves.Num() <= FPokeMonsterCreatureInstance::MoveSlotCount
		&& (Time == EPokeMonsterEncounterTime::Any || Time == Context.Time)
		&& (RegionId.IsNone() || RegionId == Context.RegionId)
		&& (RequiredCondition.IsNone() || Context.ActiveConditions.Contains(RequiredCondition));
}

FPrimaryAssetId UPokeMonsterEncounterProfile::GetPrimaryAssetId() const
{
	return FPrimaryAssetId(TEXT("EncounterProfile"), GetFName());
}

bool UPokeMonsterEncounterProfile::Roll(const FPokeMonsterEncounterContext& Context,
	FRandomStream& Random, FPokeMonsterCreatureInstance& OutCreature, int32* OutEntryIndex) const
{
	OutCreature = FPokeMonsterCreatureInstance();
	if (OutEntryIndex) *OutEntryIndex = INDEX_NONE;
	int32 TotalWeight = 0;
	TArray<int32> EligibleIndices;
	for (int32 Index = 0; Index < Entries.Num(); ++Index)
	{
		const auto& Entry = Entries[Index];
		if (!Entry.Matches(Context) || Entry.Weight > MAX_int32 - TotalWeight) continue;
		TotalWeight += Entry.Weight;
		EligibleIndices.Add(Index);
	}
	if (TotalWeight == 0) return false;
	int32 Ticket = Random.RandRange(1, TotalWeight);
	for (const int32 Index : EligibleIndices)
	{
		const auto& Entry = Entries[Index];
		Ticket -= Entry.Weight;
		if (Ticket > 0) continue;
		UPokeMonsterCreatureSpeciesData* Species = Entry.Species.LoadSynchronous();
		if (!IsValid(Species)) return false;
		FPokeMonsterCreatureInstance Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(
			Species, Random.RandRange(Entry.MinLevel, Entry.MaxLevel));
		if (!Creature.IsValid()) return false;
		for (int32 Slot = 0; Slot < Entry.Moves.Num(); ++Slot)
		{
			UPokeMonsterMoveData* Move = Entry.Moves[Slot].LoadSynchronous();
			if (!IsValid(Move) || !Creature.AssignMove(Slot, Move)) return false;
		}
		OutCreature = MoveTemp(Creature);
		if (OutEntryIndex) *OutEntryIndex = Index;
		return true;
	}
	return false;
}
