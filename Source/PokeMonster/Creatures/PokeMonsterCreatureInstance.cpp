// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterCreatureInstance.h"

#include "PokeMonsterCreatureSpeciesData.h"
#include "PokeMonsterCreatureProgression.h"
#include "../Moves/PokeMonsterMoveData.h"

FPokeMonsterCreatureInstance FPokeMonsterCreatureInstance::CreateFromSpecies(
	UPokeMonsterCreatureSpeciesData* InSpecies,
	const int32 RequestedLevel)
{
	FPokeMonsterCreatureInstance Instance;
	if (!::IsValid(InSpecies))
	{
		return Instance;
	}

	Instance.Level = FMath::Clamp(RequestedLevel == 0 ? InSpecies->GetStartingLevel() : RequestedLevel,
		UPokeMonsterCreatureProgression::MinLevel, UPokeMonsterCreatureProgression::MaxLevel);
	Instance.Experience = UPokeMonsterCreatureProgression::ExperienceForLevel(InSpecies->GetGrowthRate(), Instance.Level);
	if (Instance.Experience < 0) return FPokeMonsterCreatureInstance();
	Instance.InstanceId = FGuid::NewGuid();
	Instance.Species = InSpecies;
	Instance.CalculatedStats = UPokeMonsterCreatureProgression::CalculateStats(InSpecies->GetBaseStats(), Instance.Level);
	Instance.CurrentHP = Instance.GetMaxHP();
	return Instance;
}

bool FPokeMonsterCreatureInstance::IsValid() const
{
	return InstanceId.IsValid() && !Species.IsNull()
		&& Level >= UPokeMonsterCreatureProgression::MinLevel && Level <= UPokeMonsterCreatureProgression::MaxLevel;
}

bool FPokeMonsterCreatureInstance::RestoreIndividualState(const FGuid& InId, const int32 InLevel,
	const int64 InExperience, const int32 InCurrentHP, const TArray<FPokeMonsterMoveSlot>& InSlots)
{
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!InId.IsValid() || !::IsValid(Data) || InLevel < UPokeMonsterCreatureProgression::MinLevel
		|| InLevel > UPokeMonsterCreatureProgression::MaxLevel || InSlots.Num() != MoveSlotCount) return false;
	const int64 Floor = UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), InLevel);
	const int64 Ceiling = InLevel == UPokeMonsterCreatureProgression::MaxLevel
		? Floor + 1 : UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), InLevel + 1);
	const FPokeMonsterCreatureStats Stats = UPokeMonsterCreatureProgression::CalculateStats(Data->GetBaseStats(), InLevel);
	if (Floor < 0 || InExperience < Floor || InExperience >= Ceiling
		|| InCurrentHP < 0 || InCurrentHP > Stats.MaxHP) return false;
	for (const FPokeMonsterMoveSlot& Slot : InSlots)
	{
		if (Slot.GetMove().IsNull())
		{
			if (Slot.GetCurrentPP() != 0 || Slot.GetMaxPP() != 0) return false;
		}
		else
		{
			const UPokeMonsterMoveData* MoveData = Slot.GetMove().LoadSynchronous();
			if (!::IsValid(MoveData) || !MoveData->IsConfigured()
				|| Slot.GetMaxPP() != MoveData->MaxPP
				|| Slot.GetCurrentPP() < 0 || Slot.GetCurrentPP() > Slot.GetMaxPP()) return false;
		}
	}
	InstanceId = InId;
	Level = InLevel;
	Experience = InExperience;
	CalculatedStats = Stats;
	CurrentHP = InCurrentHP;
	MoveSlots = InSlots;
	return true;
}

int64 FPokeMonsterCreatureInstance::GetExperienceToNextLevel() const
{
	if (!IsValid() || Level == UPokeMonsterCreatureProgression::MaxLevel) return 0;
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!::IsValid(Data)) return 0;
	const int64 Next = UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), Level + 1);
	return Next < 0 ? 0 : Next - FMath::Clamp<int64>(Experience, 0, Next);
}

FPokeMonsterExperienceResult FPokeMonsterCreatureInstance::AddExperience(const int64 Amount)
{
	FPokeMonsterExperienceResult Result;
	if (Amount < 0 || !IsValid()) return Result;
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!::IsValid(Data)) return Result;
	const int64 Floor = UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), Level);
	const int64 Cap = UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), UPokeMonsterCreatureProgression::MaxLevel);
	if (Floor < 0 || Experience < Floor || Experience > Cap
		|| (Level < UPokeMonsterCreatureProgression::MaxLevel
			&& Experience >= UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), Level + 1))) return Result;

	Result.bSucceeded = true;
	Result.ExperienceAdded = FMath::Min(Amount, Cap - Experience); // Subtract before adding to avoid overflow.
	Experience += Result.ExperienceAdded;
	const int32 OldLevel = Level;
	while (Level < UPokeMonsterCreatureProgression::MaxLevel
		&& Experience >= UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), Level + 1)) ++Level;
	Result.LevelsGained = Level - OldLevel;
	if (Result.LevelsGained > 0)
	{
		const int32 OldMaxHP = GetMaxHP();
		CalculatedStats = UPokeMonsterCreatureProgression::CalculateStats(Data->GetBaseStats(), Level);
		// Preserve missing HP on level-up; zero HP stays zero (no implicit revival).
		CurrentHP = CurrentHP <= 0 ? 0 : static_cast<int32>(FMath::Clamp<int64>(
			static_cast<int64>(CurrentHP) + GetMaxHP() - OldMaxHP, 0, GetMaxHP()));
	}
	return Result;
}
