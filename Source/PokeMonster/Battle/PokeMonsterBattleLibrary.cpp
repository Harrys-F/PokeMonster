#include "PokeMonsterBattleLibrary.h"
#include "PokeMonsterTypeChart.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"

bool UPokeMonsterBattleLibrary::CheckHit(const UPokeMonsterMoveData* Move, const int32 Roll)
{
	return IsValid(Move) && Move->IsConfigured() && Roll >= 0 && Roll < 100 && Roll < Move->Accuracy;
}

FPokeMonsterDamageResult UPokeMonsterBattleLibrary::CalculateDamage(const FPokeMonsterCreatureInstance& Attacker,
	const FPokeMonsterCreatureInstance& Defender, const UPokeMonsterMoveData* Move)
{
	FPokeMonsterDamageResult Result;
	if (!IsValid(Move) || !Move->IsConfigured() || !Attacker.IsValid() || !Defender.IsValid()) return Result;
	const UPokeMonsterCreatureSpeciesData* AttackerSpecies = Attacker.Species.LoadSynchronous();
	const UPokeMonsterCreatureSpeciesData* DefenderSpecies = Defender.Species.LoadSynchronous();
	if (!IsValid(AttackerSpecies) || !IsValid(DefenderSpecies)) return Result;
	if (Move->Category == EPokeMonsterMoveCategory::Status)
	{
		Result.bValid = true; // Status effects and their own immunity/targeting rules are not implemented.
		return Result;
	}
	const bool bPhysical = Move->Category == EPokeMonsterMoveCategory::Physical;
	const int32 Offense = bPhysical ? Attacker.CalculatedStats.Attack : Attacker.CalculatedStats.SpecialAttack;
	const int32 Defense = bPhysical ? Defender.CalculatedStats.Defense : Defender.CalculatedStats.SpecialDefense;
	if (Offense <= 0 || Defense <= 0) return Result;
	Result.TypeMultiplier = GetTypeMultiplier(Move->Type, DefenderSpecies->GetPrimaryType(), DefenderSpecies->GetSecondaryType());
	if (Result.TypeMultiplier < 0.0f) return Result;
	Result.bValid = true;
	if (Result.TypeMultiplier == 0.0f) return Result;
	// Working formula only: no STAB, critical hits, random damage, abilities or stat stages.
	// Double intermediates avoid integer overflow even for malformed/extreme positive designer values.
	const double Base = FMath::FloorToDouble((2 * Attacker.Level / 5 + 2) * static_cast<double>(Move->BasePower)
		* Offense / Defense / 50.0) + 2.0;
	Result.Damage = static_cast<int32>(FMath::Clamp(FMath::FloorToDouble(Base * Result.TypeMultiplier), 1.0, double(MAX_int32)));
	return Result;
}

float UPokeMonsterBattleLibrary::GetTypeMultiplier(const EPokeMonsterCreatureType Attack,
	const EPokeMonsterCreatureType Primary, const EPokeMonsterCreatureType Secondary)
{
	return PokeMonsterTypeChart::GetMultiplier(Attack, Primary, Secondary);
}

bool UPokeMonsterBattleLibrary::AssignMove(FPokeMonsterCreatureInstance& Creature, const int32 SlotIndex, UPokeMonsterMoveData* Move)
{
	return Creature.IsValid() && Creature.AssignMove(SlotIndex, Move);
}

bool UPokeMonsterBattleLibrary::ConsumeMovePP(FPokeMonsterCreatureInstance& Creature, const int32 SlotIndex, const int32 Amount)
{
	return Creature.IsValid() && Creature.ConsumeMovePP(SlotIndex, Amount);
}
