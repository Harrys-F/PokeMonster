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
	return uint8(Status)<=uint8(EPokeMonsterCreatureStatus::Freeze)
  && (Status==EPokeMonsterCreatureStatus::Sleep?StatusTurns>=1&&StatusTurns<=15:StatusTurns==0)
  && InstanceId.IsValid() && !Species.IsNull()
		&& Level >= UPokeMonsterCreatureProgression::MinLevel && Level <= UPokeMonsterCreatureProgression::MaxLevel;
}

bool FPokeMonsterCreatureInstance::RestoreIndividualState(const FGuid& InId, const int32 InLevel,
	const int64 InExperience, const int32 InCurrentHP, const TArray<FPokeMonsterMoveSlot>& InSlots, EPokeMonsterCreatureStatus InStatus, int32 InStatusTurns)
{
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!InId.IsValid() || !::IsValid(Data) || InLevel < UPokeMonsterCreatureProgression::MinLevel
		|| InLevel > UPokeMonsterCreatureProgression::MaxLevel || InSlots.Num() != MoveSlotCount) return false;
	const int64 Floor = UPokeMonsterCreatureProgression::ExperienceForLevel(GetExperienceGrowthRate(), InLevel);
	const int64 Ceiling = InLevel == UPokeMonsterCreatureProgression::MaxLevel
		? Floor + 1 : UPokeMonsterCreatureProgression::ExperienceForLevel(GetExperienceGrowthRate(), InLevel + 1);
	const FPokeMonsterCreatureStats Stats = UPokeMonsterCreatureProgression::CalculateStats(Data->GetBaseStats(), InLevel);
	if (Floor < 0 || InExperience < Floor || InExperience >= Ceiling
		|| InCurrentHP < 0 || InCurrentHP > Stats.MaxHP || uint8(InStatus)>uint8(EPokeMonsterCreatureStatus::Freeze)
  || (InStatus==EPokeMonsterCreatureStatus::Sleep ? InStatusTurns<1 || InStatusTurns>15 : InStatusTurns!=0)) return false;
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
	RememberActiveMoves();
 Status=InStatus; StatusTurns=InStatusTurns;
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
	auto Copy = *this;
	if (!Copy.RestoreIndividualState(InstanceId, Level, Experience, FullHP, RestoredSlots)) return false;
	for (auto& Known : Copy.LearnedMoves) if (!Known.RestoreCurrentPP(Known.GetMaxPP())) return false;
	*this = MoveTemp(Copy);
	return true;
}

int64 FPokeMonsterCreatureInstance::GetExperienceToNextLevel() const
{
	if (!IsValid() || Level == UPokeMonsterCreatureProgression::MaxLevel) return 0;
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!::IsValid(Data)) return 0;
	const int64 Next = UPokeMonsterCreatureProgression::ExperienceForLevel(GetExperienceGrowthRate(), Level + 1);
	return Next < 0 ? 0 : Next - FMath::Clamp<int64>(Experience, 0, Next);
}

FPokeMonsterExperienceResult FPokeMonsterCreatureInstance::AddExperience(const int64 Amount)
{
	FPokeMonsterExperienceResult Result;
	if (Amount < 0 || !IsValid()) return Result;
	const UPokeMonsterCreatureSpeciesData* Data = Species.LoadSynchronous();
	if (!::IsValid(Data)) return Result;
	const int64 Floor = UPokeMonsterCreatureProgression::ExperienceForLevel(GetExperienceGrowthRate(), Level);
	const int64 Cap = UPokeMonsterCreatureProgression::ExperienceForLevel(GetExperienceGrowthRate(), UPokeMonsterCreatureProgression::MaxLevel);
	if (Floor < 0 || Experience < Floor || Experience > Cap
		|| (Level < UPokeMonsterCreatureProgression::MaxLevel
			&& Experience >= UPokeMonsterCreatureProgression::ExperienceForLevel(GetExperienceGrowthRate(), Level + 1))) return Result;

	Result.bSucceeded = true;
	Result.ExperienceAdded = FMath::Min(Amount, Cap - Experience); // Subtract before adding to avoid overflow.
	Experience += Result.ExperienceAdded;
	const int32 OldLevel = Level;
	while (Level < UPokeMonsterCreatureProgression::MaxLevel
		&& Experience >= UPokeMonsterCreatureProgression::ExperienceForLevel(GetExperienceGrowthRate(), Level + 1)) ++Level;
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
			if (LearnedMoves.ContainsByPredicate([Move](const auto& S) { return S.GetMove().LoadSynchronous() == Move; })) continue;
			const int32 Free = MoveSlots.IndexOfByPredicate([](const auto& S) { return S.GetMove().IsNull(); });
			if (Free != INDEX_NONE) AssignMove(Free, Move);
			else PendingMoves.Add(Entry.Move); // Never silently replace a player's move.
		}
	}
	return Result;
}

bool FPokeMonsterCreatureInstance::AssignSpeciesMoves()
{
 const auto* D=Species.LoadSynchronous();if(!D)return false;const auto Moves=D->MovesForLevel(Level);if(Moves.IsEmpty())return false;TArray<FPokeMonsterMoveSlot> Slots;Slots.SetNum(4);for(int I=0;I<Moves.Num();++I)if(!Slots[I].AssignMove(Moves[I]))return false;MoveSlots=MoveTemp(Slots);RememberActiveMoves();return true;
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
 MoveSlots=Copy.MoveSlots;LearnedMoves.Reset();RememberActiveMoves();return true;
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
			|| LearnedMoves.ContainsByPredicate([Move](const auto& S) { return S.GetMove().LoadSynchronous() == Move; })
			|| !Data->LevelUpMoves.ContainsByPredicate([&](const auto& E) { return E.Level >= 1 && E.Level <= Level && E.Move == Ref; })) return false;
		Seen.Add(Ref.ToSoftObjectPath());
	}
	PendingMoves = Moves;
	return true;
}

bool FPokeMonsterCreatureInstance::ResolveMoveLearning(int32 SlotIndex)
{
	if (PendingMoves.IsEmpty() || SlotIndex < INDEX_NONE || SlotIndex >= MoveSlotCount
  || !RestorePendingMoves(PendingMoves)) return false;
	if (SlotIndex != INDEX_NONE)
	{
		auto* Move = PendingMoves[0].LoadSynchronous();
		if (!Move || !Move->IsConfigured() || !AssignMove(SlotIndex, Move)) return false;
	}
	PendingMoves.RemoveAt(0);
	return true;
}

void FPokeMonsterCreatureInstance::RememberActiveMoves()
{
 // Old technical saves may have duplicate active slots with independent PP. Keep them intact;
 // a unique remembered entry conservatively retains the lowest remaining PP. Master sets are unique.
 for (const auto& Slot : MoveSlots)
 {
  if (Slot.GetMove().IsNull()) continue;
  auto* Known = LearnedMoves.FindByPredicate([&](const auto& K) { return K.GetMove() == Slot.GetMove(); });
  if (!Known) LearnedMoves.Add(Slot);
  else Known->RestoreCurrentPP(FMath::Min(Known->GetCurrentPP(), Slot.GetCurrentPP()));
 }
}

bool FPokeMonsterCreatureInstance::AssignMove(int32 SlotIndex, UPokeMonsterMoveData* Move)
{
 if (!MoveSlots.IsValidIndex(SlotIndex) || !MoveSlots[SlotIndex].AssignMove(Move)) return false;
 RememberActiveMoves();
 return true;
}

bool FPokeMonsterCreatureInstance::ConsumeMovePP(int32 SlotIndex, int32 Amount)
{
 if (!MoveSlots.IsValidIndex(SlotIndex) || !MoveSlots[SlotIndex].ConsumePP(Amount)) return false;
 RememberActiveMoves();
 return true;
}

bool FPokeMonsterCreatureInstance::RestoreLearnedMoves(const TArray<FPokeMonsterMoveSlot>& Moves)
{
 TSet<FSoftObjectPath> Seen;
 for (const auto& Slot : Moves)
 {
  const auto* Move = Slot.GetMove().LoadSynchronous();
  if (!Move || !Move->IsConfigured() || Slot.GetMaxPP() != Move->MaxPP
   || Slot.GetCurrentPP() < 0 || Slot.GetCurrentPP() > Move->MaxPP
   || Seen.Contains(Slot.GetMove().ToSoftObjectPath())) return false;
  Seen.Add(Slot.GetMove().ToSoftObjectPath());
 }
 for (const auto& Slot : MoveSlots)
 {
  if (Slot.GetMove().IsNull()) continue;
  const auto* Known = Moves.FindByPredicate([&](const auto& K) { return K.GetMove() == Slot.GetMove(); });
  if (!Known || Known->GetCurrentPP() > Slot.GetCurrentPP()) return false;
 }
 for (const auto& Pending : PendingMoves)
  if (Seen.Contains(Pending.ToSoftObjectPath())) return false;
 LearnedMoves = Moves;
 return true;
}

bool FPokeMonsterCreatureInstance::SetActiveLearnedMoves(const TArray<TSoftObjectPtr<UPokeMonsterMoveData>>& Moves)
{
 if (!IsValid() || Moves.IsEmpty() || Moves.Num() > MoveSlotCount || !PendingMoves.IsEmpty()) return false;
 TArray<FPokeMonsterMoveSlot> Next; Next.SetNum(MoveSlotCount);
 TSet<FSoftObjectPath> Seen;
 for (int32 I=0; I<Moves.Num(); ++I)
 {
  const auto* Known=LearnedMoves.FindByPredicate([&](const auto& K) { return K.GetMove()==Moves[I]; });
  if (!Known || Moves[I].IsNull() || Seen.Contains(Moves[I].ToSoftObjectPath())) return false;
  Seen.Add(Moves[I].ToSoftObjectPath());
  Next[I]=*Known; // Never AssignMove here: reactivation must retain spent PP.
 }
 MoveSlots=MoveTemp(Next);
 return true;
}

EPokeMonsterGrowthRate FPokeMonsterCreatureInstance::GetExperienceGrowthRate() const
{
 const auto* Data=Species.LoadSynchronous();
 return bHasExperienceGrowthOverride?ExperienceGrowthOverride:Data?Data->GetGrowthRate():EPokeMonsterGrowthRate::MediumFast;
}
bool FPokeMonsterCreatureInstance::ValidateEvolutionState() const
{
 if(LastEvolutionOfferedLevel<0||LastEvolutionOfferedLevel>Level)return false;
 if(bHasExperienceGrowthOverride&&UPokeMonsterCreatureProgression::ExperienceForLevel(ExperienceGrowthOverride,Level)<0)return false;
 if(!PendingEvolutionTarget.IsValid())return PendingEvolutionTarget==FPrimaryAssetId();
 FPokeMonsterEvolutionContext C;
 // Saved metadata proves a possible offer, not that its time window is open at load time.
 // Actual offering/acceptance rechecks the current central world time separately.
 const auto* Data=Species.LoadSynchronous();if(!Data||LastEvolutionOfferedLevel<=0||PendingEvolutionTarget==Data->GetPrimaryAssetId())return false;
 for(const auto& Rule:Data->GetEvolutions())if(Rule.TargetSpecies==PendingEvolutionTarget)
 {
  C.MinuteOfDay=Rule.RequiredStartMinute;
  if(UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,LastEvolutionOfferedLevel,C))return true;
 }
 return false;
}
