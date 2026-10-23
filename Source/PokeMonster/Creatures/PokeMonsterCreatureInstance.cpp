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
	const int64 InExperience, const int32 InCurrentHP, const TArray<FPokeMonsterMoveSlot>& InSlots, EPokeMonsterCreatureStatus InStatus)
{
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!InId.IsValid() || !::IsValid(Data) || InLevel < UPokeMonsterCreatureProgression::MinLevel
		|| InLevel > UPokeMonsterCreatureProgression::MaxLevel || InSlots.Num() != MoveSlotCount) return false;
	const int64 Floor = UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), InLevel);
	const int64 Ceiling = InLevel == UPokeMonsterCreatureProgression::MaxLevel
		? Floor + 1 : UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(), InLevel + 1);
	const FPokeMonsterCreatureStats Stats = UPokeMonsterCreatureProgression::CalculateStats(Data->GetBaseStats(), InLevel);
	if (Floor < 0 || InExperience < Floor || InExperience >= Ceiling
		|| InCurrentHP < 0 || InCurrentHP > Stats.MaxHP || uint8(InStatus)>uint8(EPokeMonsterCreatureStatus::Burn)) return false;
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
 Status=InStatus;
	return true;
}

bool FPokeMonsterCreatureInstance::RestoreFully()
{
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!IsValid() || !::IsValid(Data)) return false;
	TArray<FPokeMonsterMoveSlot> RestoredSlots = MoveSlots;
	for (FPokeMonsterMoveSlot& Slot : RestoredSlots)
	{
		if (!Slot.GetMove().IsNull() && !Slot.RestoreCurrentPP(Slot.GetMaxPP())) return false;
	}
	const int32 FullHP = UPokeMonsterCreatureProgression::CalculateStats(
		Data->GetBaseStats(), Level).MaxHP;
	return RestoreIndividualState(InstanceId, Level, Experience, FullHP, RestoredSlots);
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
	if (Result.LevelsGained > 0)
	{
		auto Ordered = Data->LevelUpMoves;
		Ordered.StableSort([](const auto& A, const auto& B) { return A.Level < B.Level; });
		for (const auto& Entry : Ordered)
		{
			if (Entry.Level <= OldLevel || Entry.Level > Level) continue;
			auto* Move = Entry.Move.LoadSynchronous();
			if (!Move || !Move->IsConfigured() || PendingMoves.Contains(Entry.Move)) continue;
			if (MoveSlots.ContainsByPredicate([Move](const auto& S) { return S.GetMove().LoadSynchronous() == Move; })) continue;
			const int32 Free = MoveSlots.IndexOfByPredicate([](const auto& S) { return S.GetMove().IsNull(); });
			if (Free != INDEX_NONE) MoveSlots[Free].AssignMove(Move);
			else PendingMoves.Add(Entry.Move); // Never silently replace a player's move.
		}
	}
	return Result;
}

bool FPokeMonsterCreatureInstance::AssignSpeciesMoves()
{
 const auto* D=Species.LoadSynchronous();if(!D)return false;const auto Moves=D->MovesForLevel(Level);if(Moves.IsEmpty())return false;TArray<FPokeMonsterMoveSlot> Slots;Slots.SetNum(4);for(int I=0;I<Moves.Num();++I)if(!Slots[I].AssignMove(Moves[I]))return false;MoveSlots=MoveTemp(Slots);return true;
}
bool FPokeMonsterCreatureInstance::UpgradeLegacyGlumandaMoves()
{
 const auto* D=Species.LoadSynchronous();if(!D||D->GetInternalId()!=TEXT("Zunderlauf")||D->LevelUpMoves.IsEmpty())return true;
 TMap<FName,int32> Spent;for(const auto& Slot:MoveSlots)if(auto* M=Slot.GetMove().LoadSynchronous()){
  FName Name=M->InternalId;if(Name!=TEXT("TestNormalPhysical")&&Name!=TEXT("TestFireSpecial")&&Name!=TEXT("TestStatus"))return true;
  Spent.FindOrAdd(Name)+=Slot.GetMaxPP()-Slot.GetCurrentPP();
 }
 if(Spent.IsEmpty())return true;auto Copy=*this;if(!Copy.AssignSpeciesMoves())return false;
 for(auto& Slot:Copy.MoveSlots)if(auto* M=Slot.GetMove().LoadSynchronous()){
  const FName Legacy=M->InternalId==TEXT("Scratch")?TEXT("TestNormalPhysical"):M->InternalId==TEXT("Growl")?TEXT("TestStatus"):TEXT("TestFireSpecial");
  Slot.RestoreCurrentPP(FMath::Max(0,Slot.GetMaxPP()-Spent.FindRef(Legacy)));
 }
 MoveSlots=Copy.MoveSlots;return true;
}


bool FPokeMonsterCreatureInstance::RestorePendingMoves(const TArray<TSoftObjectPtr<UPokeMonsterMoveData>>& Moves)
{
	const auto* Data = Species.LoadSynchronous();
	if (!IsValid() || !Data || Moves.Num() > Data->LevelUpMoves.Num()) return false;
	TSet<FSoftObjectPath> Seen;
	for (const auto& Ref : Moves)
	{
		const auto* Move = Ref.LoadSynchronous();
		if (!Move || !Move->IsConfigured() || Seen.Contains(Ref.ToSoftObjectPath())
			|| MoveSlots.ContainsByPredicate([Move](const auto& S) { return S.GetMove().LoadSynchronous() == Move; })
			|| !Data->LevelUpMoves.ContainsByPredicate([&](const auto& E) { return E.Level >= 1 && E.Level <= Level && E.Move == Ref; })) return false;
		Seen.Add(Ref.ToSoftObjectPath());
	}
	PendingMoves = Moves;
	return true;
}

bool FPokeMonsterCreatureInstance::ResolveMoveLearning(int32 SlotIndex)
{
	if (PendingMoves.IsEmpty() || SlotIndex < INDEX_NONE || SlotIndex >= MoveSlotCount) return false;
	if (SlotIndex != INDEX_NONE)
	{
		auto* Move = PendingMoves[0].LoadSynchronous();
		if (!Move || !Move->IsConfigured() || !AssignMove(SlotIndex, Move)) return false;
	}
	PendingMoves.RemoveAt(0);
	return true;
}
