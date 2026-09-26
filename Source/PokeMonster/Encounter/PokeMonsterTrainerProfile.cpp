#include "PokeMonsterTrainerProfile.h"

#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"

FPrimaryAssetId UPokeMonsterTrainerProfile::GetPrimaryAssetId() const
{
	return FPrimaryAssetId(TEXT("TrainerProfile"), GetFName());
}

bool UPokeMonsterTrainerProfile::BuildTeam(TArray<FPokeMonsterCreatureInstance>& OutTeam) const
{
	OutTeam.Reset();
	if (InternalId.IsNone() || DisplayName.IsEmpty() || TrainerClass.IsEmpty()
		|| Team.IsEmpty() || Team.Num() > 6) return false;
	for (const FPokeMonsterTrainerTeamEntry& Entry : Team)
	{
		if (Entry.Level < 1 || Entry.Level > 100 || Entry.Species.IsNull()
			|| Entry.StartingMoves.IsEmpty()
			|| Entry.StartingMoves.Num() > FPokeMonsterCreatureInstance::MoveSlotCount)
		{
			OutTeam.Reset();
			return false;
		}
		UPokeMonsterCreatureSpeciesData* Species = Entry.Species.LoadSynchronous();
		if (!IsValid(Species)) { OutTeam.Reset(); return false; }
		FPokeMonsterCreatureInstance Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, Entry.Level);
		if (!Creature.IsValid()) { OutTeam.Reset(); return false; }
		for (int32 Slot = 0; Slot < Entry.StartingMoves.Num(); ++Slot)
		{
			UPokeMonsterMoveData* Move = Entry.StartingMoves[Slot].LoadSynchronous();
			if (!IsValid(Move) || !Creature.AssignMove(Slot, Move))
			{
				OutTeam.Reset();
				return false;
			}
		}
		OutTeam.Add(MoveTemp(Creature));
	}
	return true;
}
