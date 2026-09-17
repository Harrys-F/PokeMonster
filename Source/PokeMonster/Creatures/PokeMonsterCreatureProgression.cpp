#include "PokeMonsterCreatureProgression.h"

#include "PokeMonsterCreatureSpeciesData.h"

int64 UPokeMonsterCreatureProgression::ExperienceForLevel(const EPokeMonsterGrowthRate GrowthRate, const int32 Level)
{
	const int64 N = FMath::Clamp(Level, MinLevel, MaxLevel);
	const int64 Cube = N * N * N;
	int64 XP;
	switch (GrowthRate)
	{
	case EPokeMonsterGrowthRate::Fast: XP = 4 * Cube / 5; break;
	case EPokeMonsterGrowthRate::MediumFast: XP = Cube; break;
	case EPokeMonsterGrowthRate::MediumSlow: XP = 6 * Cube / 5 - 15 * N * N + 100 * N - 140; break;
	case EPokeMonsterGrowthRate::Slow: XP = 5 * Cube / 4; break;
	case EPokeMonsterGrowthRate::Erratic:
		if (N <= 50) XP = Cube * (100 - N) / 50;
		else if (N <= 68) XP = Cube * (150 - N) / 100;
		else if (N <= 98) XP = Cube * ((1911 - 10 * N) / 3) / 500;
		else XP = Cube * (160 - N) / 100;
		break;
	case EPokeMonsterGrowthRate::Fluctuating:
		if (N <= 15) XP = Cube * ((N + 1) / 3 + 24) / 50;
		else if (N <= 36) XP = Cube * (N + 14) / 50;
		else XP = Cube * (N / 2 + 32) / 50;
		break;
	default: return -1;
	}
	return N == MinLevel ? 0 : FMath::Max<int64>(0, XP);
}

FPokeMonsterCreatureStats UPokeMonsterCreatureProgression::CalculateStats(const FPokeMonsterCreatureBaseStats& BaseStats, const int32 Level)
{
	const int32 ClampedLevel = FMath::Clamp(Level, MinLevel, MaxLevel);
	const auto Scale = [ClampedLevel](const int32 Base, const int32 Bonus)
	{
		return static_cast<int32>(FMath::Min<int64>(MAX_int32, 2LL * FMath::Max(1, Base) * ClampedLevel / 100 + Bonus));
	};
	FPokeMonsterCreatureStats Stats;
	Stats.MaxHP = Scale(BaseStats.HP, ClampedLevel + 10);
	Stats.Attack = Scale(BaseStats.Attack, 5);
	Stats.Defense = Scale(BaseStats.Defense, 5);
	Stats.SpecialAttack = Scale(BaseStats.SpecialAttack, 5);
	Stats.SpecialDefense = Scale(BaseStats.SpecialDefense, 5);
	Stats.Speed = Scale(BaseStats.Speed, 5);
	return Stats;
}

FPokeMonsterExperienceResult UPokeMonsterCreatureProgression::AddExperience(FPokeMonsterCreatureInstance& Creature, const int64 Amount)
{
	return Creature.AddExperience(Amount);
}

int64 UPokeMonsterCreatureProgression::ExperienceToNextLevel(const FPokeMonsterCreatureInstance& Creature)
{
	return Creature.GetExperienceToNextLevel();
}

bool UPokeMonsterCreatureProgression::IsEvolutionEligible(const FPokeMonsterEvolutionData& Rule, const int32 Level, const FPokeMonsterEvolutionContext& Context)
{
	if (!Rule.TargetSpecies.IsValid() || Rule.TargetSpecies.PrimaryAssetType != FPrimaryAssetType(TEXT("CreatureSpecies"))
		|| Level < MinLevel || Level > MaxLevel || Rule.MinimumLevel < MinLevel || Rule.MinimumLevel > MaxLevel
		|| Level < Rule.MinimumLevel || Rule.Trigger != Context.Trigger
		|| Rule.MinimumFriendship < 0 || Rule.MinimumFriendship > 255 || Context.Friendship < 0 || Context.Friendship > 255
		|| Context.Friendship < Rule.MinimumFriendship)
	{
		return false;
	}
	const auto Matches = [](FName Required, FName Actual) { return Required.IsNone() || Required == Actual; };
	if (!Matches(Rule.RequiredItemId, Context.UsedItemId) || !Matches(Rule.RequiredLocationId, Context.LocationId)
		|| !Matches(Rule.RequiredActionId, Context.ActionId))
	{
		return false;
	}
	switch (Rule.Trigger)
	{
	case EPokeMonsterEvolutionTrigger::Level:
		return Rule.RequirementId.IsNone(); // An untyped legacy requirement must not be silently ignored.
	case EPokeMonsterEvolutionTrigger::Item:
		return (!Rule.RequiredItemId.IsNone() || !Rule.RequirementId.IsNone()) && Matches(Rule.RequirementId, Context.UsedItemId);
	case EPokeMonsterEvolutionTrigger::Friendship:
		return Rule.MinimumFriendship > 0 && Rule.RequirementId.IsNone();
	case EPokeMonsterEvolutionTrigger::Location:
		return (!Rule.RequiredLocationId.IsNone() || !Rule.RequirementId.IsNone()) && Matches(Rule.RequirementId, Context.LocationId);
	case EPokeMonsterEvolutionTrigger::SpecialInteraction:
		return (!Rule.RequiredActionId.IsNone() || !Rule.RequirementId.IsNone()) && Matches(Rule.RequirementId, Context.ActionId);
	default:
		return false; // Custom is reserved until an explicit evaluator is introduced.
	}
}

TArray<FPrimaryAssetId> UPokeMonsterCreatureProgression::GetEligibleEvolutions(const FPokeMonsterCreatureInstance& Creature, const FPokeMonsterEvolutionContext& Context)
{
	TArray<FPrimaryAssetId> Targets;
	if (!Creature.IsValid()) return Targets;
	const UPokeMonsterCreatureSpeciesData* Species = Creature.Species.LoadSynchronous();
	if (!IsValid(Species)) return Targets;
	for (const FPokeMonsterEvolutionData& Rule : Species->GetEvolutions())
	{
		if (Rule.TargetSpecies != Species->GetPrimaryAssetId() && IsEvolutionEligible(Rule, Creature.Level, Context))
		{
			Targets.AddUnique(Rule.TargetSpecies);
		}
	}
	return Targets;
}
