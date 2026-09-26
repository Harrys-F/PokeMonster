#include "PokeMonsterMoveSlot.h"
#include "PokeMonsterMoveData.h"

bool FPokeMonsterMoveSlot::AssignMove(UPokeMonsterMoveData* InMove)
{
	if (!IsValid(InMove) || !InMove->IsConfigured()) return false;
	Move = InMove;
	MaxPP = InMove->MaxPP;
	CurrentPP = MaxPP;
	return true;
}

bool FPokeMonsterMoveSlot::ConsumePP(const int32 Amount)
{
	if (Amount <= 0 || CurrentPP < Amount || CurrentPP > MaxPP) return false;
	const UPokeMonsterMoveData* Data = Move.LoadSynchronous();
	if (!IsValid(Data) || !Data->IsConfigured() || MaxPP != Data->MaxPP) return false;
	CurrentPP -= Amount;
	return true;
}

bool FPokeMonsterMoveSlot::RestoreCurrentPP(const int32 InCurrentPP)
{
	const UPokeMonsterMoveData* Data = Move.LoadSynchronous();
	if (!IsValid(Data) || !Data->IsConfigured() || MaxPP != Data->MaxPP
		|| InCurrentPP < 0 || InCurrentPP > MaxPP) return false;
	CurrentPP = InCurrentPP;
	return true;
}
