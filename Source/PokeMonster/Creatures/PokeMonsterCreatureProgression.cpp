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
 const bool Timed=Rule.RequiredStartMinute!=-1||Rule.RequiredEndMinute!=-1;
 if(Timed)
 {
  const int32 Start=Rule.RequiredStartMinute,End=Rule.RequiredEndMinute,Now=Context.MinuteOfDay;
  if(Start<0||Start>=1440||End<0||End>=1440||Start==End||Now<0||Now>=1440)return false;
  if(!(Start<End?(Now>=Start&&Now<End):(Now>=Start||Now<End)))return false;
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


#include "PokeMonsterCreaturePresentation.h"
#include "Engine/AssetManager.h"
#include "../Moves/PokeMonsterMoveData.h"

TArray<FPokeMonsterEvolutionOption> UPokeMonsterCreatureProgression::GetEvolutionOptions(
	const FPokeMonsterCreatureInstance& Creature, const FPokeMonsterEvolutionContext& Context)
{
	TArray<FPokeMonsterEvolutionOption> Options;
	for (const auto& Target : GetEligibleEvolutions(Creature, Context))
	{
		auto& Option = Options.AddDefaulted_GetRef(); Option.TargetSpecies = Target;
		const auto Path = UAssetManager::Get().GetPrimaryAssetPath(Target);
		const auto* Species = Path.IsValid() ? Cast<UPokeMonsterCreatureSpeciesData>(Path.TryLoad()) : nullptr;
		if (!Species || Species->GetPrimaryAssetId() != Target)
		{
			Option.Reason = FText::FromString(TEXT("Entwicklung vorbereitet – Zielart und Zielmodell noch nicht integriert."));
			continue;
		}
		const auto* Visual = Species->GetVisuals().Presentation.LoadSynchronous();
		Option.Readiness = Visual && Visual->Clips.Num()==7 && Visual->GetValidationErrors().IsEmpty()
			? EPokeMonsterEvolutionReadiness::Ready : EPokeMonsterEvolutionReadiness::MissingVisuals;
		Option.Reason = FText::FromString(Option.Readiness == EPokeMonsterEvolutionReadiness::Ready
			? TEXT("Entwicklungsbedingungen und vollständige Zielpräsentation verfügbar.")
			: TEXT("Entwicklung vorbereitet – gültiges Zielmodell fehlt."));
	}
	return Options;
}

bool UPokeMonsterCreatureProgression::ApplyEvolution(FPokeMonsterCreatureInstance& Creature,const FPrimaryAssetId& Target,const FPokeMonsterEvolutionContext& Context)
{
 if(!Creature.IsValid()||!Creature.PendingMoves.IsEmpty())return false;
 bool Ready=false;for(const auto& O:GetEvolutionOptions(Creature,Context))if(O.TargetSpecies==Target&&O.Readiness==EPokeMonsterEvolutionReadiness::Ready)Ready=true;
 if(!Ready)return false;
 auto* Destination=Cast<UPokeMonsterCreatureSpeciesData>(UAssetManager::Get().GetPrimaryAssetPath(Target).TryLoad());
 if(!Destination||Destination->GetPrimaryAssetId()!=Target)return false;
 auto Copy=Creature;
 Copy.ExperienceGrowthOverride=Creature.GetExperienceGrowthRate();Copy.bHasExperienceGrowthOverride=true;
 Copy.Species=Destination;Copy.CalculatedStats=CalculateStats(Destination->GetBaseStats(),Copy.Level);
 Copy.CurrentHP=Creature.CurrentHP==0?0:FMath::Clamp(Creature.CurrentHP+Copy.GetMaxHP()-Creature.GetMaxHP(),1,Copy.GetMaxHP());
 Copy.PendingEvolutionTarget=FPrimaryAssetId();Copy.PendingEvolutionItemId=NAME_None;Copy.LastEvolutionOfferedLevel=0;
 // Only the current level's evolution-time offer, not a retroactive species learnset grant.
 for(const auto& Entry:Destination->LevelUpMoves)if(Entry.Level==Copy.Level)
 {
  auto* Move=Entry.Move.LoadSynchronous();if(!Move||!Move->IsConfigured())continue;
  if(Copy.LearnedMoves.ContainsByPredicate([Move](const auto& M){return M.GetMove().LoadSynchronous()==Move;})||Copy.PendingMoves.Contains(Entry.Move))continue;
  // Keep this a real player decision even with a free slot; no invented automatic replacement.
  Copy.PendingMoves.Add(Entry.Move);
 }
 auto Validated=Copy;
 if(!Validated.RestoreIndividualState(Copy.InstanceId,Copy.Level,Copy.Experience,Copy.CurrentHP,Copy.GetMoveSlots(),Copy.Status,Copy.StatusTurns)
  ||!Validated.RestoreLearnedMoves(Copy.GetLearnedMoves())||!Validated.RestorePendingMoves(Copy.PendingMoves)||!Copy.ValidateEvolutionState())return false;
 Creature=MoveTemp(Copy);return true;
}
