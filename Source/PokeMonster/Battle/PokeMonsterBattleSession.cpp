#include "PokeMonsterBattleSession.h"
#include "PokeMonsterTypeChart.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Capture/PokeMonsterCaptureLibrary.h"

namespace
{
	using EError = EPokeMonsterBattleError;
	using ESide = EPokeMonsterBattleSide;
	using EPhase = EPokeMonsterBattlePhase;
	using EEvent = EPokeMonsterBattleEventType;
	using B = UPokeMonsterBattleLibrary;

	TArray<FPokeMonsterCreatureInstance>& TeamFor(FPokeMonsterBattleState& State, ESide Side)
	{
		return Side == ESide::A ? State.TeamA : State.TeamB;
	}
	FPokeMonsterCreatureInstance& ActiveFor(FPokeMonsterBattleState& State, ESide Side)
	{
		return Side == ESide::A ? State.SideA : State.SideB;
	}
	int32& ActiveIndexFor(FPokeMonsterBattleState& State, ESide Side)
	{
		return Side == ESide::A ? State.ActiveIndexA : State.ActiveIndexB;
	}
	void SyncActive(FPokeMonsterBattleState& State)
	{
		State.TeamA[State.ActiveIndexA] = State.SideA;
		State.TeamB[State.ActiveIndexB] = State.SideB;
	}
	bool HasLiving(const TArray<FPokeMonsterCreatureInstance>& Team)
	{
		for (const auto& Creature : Team) if (Creature.CurrentHP > 0) return true;
		return false;
	}
	EError ValidateCreature(const FPokeMonsterCreatureInstance& Creature, bool bAllowFainted = false)
	{
		if (Creature.Species.IsNull()) return EError::MissingSpecies;
		if (!Creature.IsValid()) return EError::InvalidCreature;
		const auto* Species = Creature.Species.LoadSynchronous();
		if (!IsValid(Species)) return EError::MissingSpecies;
		if (Creature.CurrentHP <= 0 && !bAllowFainted) return EError::CreatureFainted;
		const auto& Stats = Creature.CalculatedStats;
		if (Stats.MaxHP <= 0 || Creature.CurrentHP < 0 || Creature.CurrentHP > Stats.MaxHP
			|| Stats.Attack <= 0 || Stats.Defense <= 0 || Stats.SpecialAttack <= 0
			|| Stats.SpecialDefense <= 0 || Stats.Speed <= 0
			|| PokeMonsterTypeChart::GetMultiplier(EPokeMonsterCreatureType::Normal,
				Species->GetPrimaryType(), Species->GetSecondaryType()) < 0.0f) return EError::InvalidStats;
		return EError::None;
	}
	EError ValidateSelection(const FPokeMonsterCreatureInstance& Creature, int32 Slot, UPokeMonsterMoveData*& OutMove)
	{
		if (Slot < 0 || Slot >= FPokeMonsterCreatureInstance::MoveSlotCount
			|| !Creature.GetMoveSlots().IsValidIndex(Slot)) return EError::InvalidSlot;
		const auto& Data = Creature.GetMoveSlots()[Slot];
		OutMove = Data.GetMove().LoadSynchronous();
		if (!IsValid(OutMove)) return EError::MissingMove;
		if (!OutMove->IsConfigured()) return EError::InvalidMove;
		if (Data.GetMaxPP() != OutMove->MaxPP || Data.GetCurrentPP() < 0
			|| Data.GetCurrentPP() > Data.GetMaxPP()) return EError::InvalidPP;
		return Data.GetCurrentPP() == 0 ? EError::NoPP : EError::None;
	}
	FPokeMonsterBattleEvent& AddEvent(FPokeMonsterBattleResult& Result, const FPokeMonsterBattleState& State,
		EEvent Type, ESide Source, int32 Slot = INDEX_NONE, const UPokeMonsterMoveData* Move = nullptr)
	{
		auto& Event = Result.Events.AddDefaulted_GetRef();
		Event.Type = Type;
		Event.RoundNumber = State.RoundNumber;
		Event.Source = Source;
		Event.Target = Source == ESide::A ? ESide::B : ESide::A;
		Event.SourceInstanceId = Source == ESide::A ? State.SideA.InstanceId : State.SideB.InstanceId;
		Event.TargetInstanceId = Source == ESide::A ? State.SideB.InstanceId : State.SideA.InstanceId;
		Event.SlotIndex = Slot;
		if (Move)
		{
			Event.MoveId = Move->GetPrimaryAssetId();
			Event.Category = Move->Category;
		}
		return Event;
	}
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::Reject(EError Error, ESide Side) const
{
	FPokeMonsterBattleResult Result;
	Result.Error = Error;
	Result.ErrorSide = Side;
	Result.RoundNumber = State.RoundNumber;
	Result.Winner = State.Winner;
	return Result;
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::Initialize(const FPokeMonsterCreatureInstance& SideA,
	const FPokeMonsterCreatureInstance& SideB, int32 RandomSeed)
{
	TArray<FPokeMonsterCreatureInstance> A, BTeam;
	A.Add(SideA); BTeam.Add(SideB);
	return InitializeTeams(A, BTeam, RandomSeed);
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::InitializeTeams(
	const TArray<FPokeMonsterCreatureInstance>& TeamA,
	const TArray<FPokeMonsterCreatureInstance>& TeamB, int32 RandomSeed, bool bAllowCapture)
{
	if (State.Phase != EPhase::Uninitialized) return Reject(EError::AlreadyInitialized);
	if (TeamA.IsEmpty() || TeamB.IsEmpty() || TeamA.Num() > 6 || TeamB.Num() > 6)
		return Reject(EError::InvalidTeam);
	TSet<FGuid> Seen;
	for (int32 SideIndex = 0; SideIndex < 2; ++SideIndex)
	{
		const auto& Team = SideIndex == 0 ? TeamA : TeamB;
		const ESide Side = SideIndex == 0 ? ESide::A : ESide::B;
		for (int32 Index = 0; Index < Team.Num(); ++Index)
		{
			const EError Error = ValidateCreature(Team[Index], Index != 0);
			if (Error != EError::None) return Reject(Error, Side);
			if (Seen.Contains(Team[Index].InstanceId)) return Reject(EError::DuplicateCreature, Side);
			Seen.Add(Team[Index].InstanceId);
		}
	}
	State.TeamA = TeamA;
	State.TeamB = TeamB;
	State.ActiveIndexA = State.ActiveIndexB = 0;
	State.SideA = TeamA[0];
	State.SideB = TeamB[0];
	State.Phase = EPhase::AwaitingChoices;
	State.bCaptureAllowed = bAllowCapture;
	Random.Initialize(RandomSeed);
	for (const auto* Team : {&State.TeamA, &State.TeamB})
		for (const auto& Creature : *Team)
		{
			RetainedData.AddUnique(Creature.Species.LoadSynchronous());
			for (const auto& Slot : Creature.GetMoveSlots())
				if (auto* Move = Slot.GetMove().LoadSynchronous()) RetainedData.AddUnique(Move);
		}
	FPokeMonsterBattleResult Result;
	Result.bSucceeded = true;
	return Result;
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::ResolveRound(int32 SlotA, int32 SlotB)
{
	FPokeMonsterBattleChoice A, BChoice;
	A.Index = SlotA; BChoice.Index = SlotB;
	return ResolveTurn(A, BChoice);
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::ResolveTurn(
	const FPokeMonsterBattleChoice& ChoiceA, const FPokeMonsterBattleChoice& ChoiceB)
{
	if (State.Phase == EPhase::Uninitialized) return Reject(EError::NotInitialized);
	if (State.Phase == EPhase::Finished) return Reject(EError::BattleFinished);
	if (State.Phase == EPhase::AwaitingSwitch) return Reject(EError::SwitchRequired);
	if (State.RoundNumber == MAX_int32) return Reject(EError::RoundLimitReached);
	const FPokeMonsterBattleChoice Choices[2] = {ChoiceA, ChoiceB};
	UPokeMonsterMoveData* Moves[2] = {nullptr, nullptr};
	UPokeMonsterCaptureDeviceData* Device = nullptr;
	for (int32 Index = 0; Index < 2; ++Index)
	{
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		const auto& Creature = Index == 0 ? State.SideA : State.SideB;
		EError Error = ValidateCreature(Creature);
		if (Error != EError::None) return Reject(Error, Side);
		if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Move)
			Error = ValidateSelection(Creature, Choices[Index].Index, Moves[Index]);
		else if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Switch)
		{
			const auto& Team = Index == 0 ? State.TeamA : State.TeamB;
			const int32 ActiveIndex = Index == 0 ? State.ActiveIndexA : State.ActiveIndexB;
			Error = Team.IsValidIndex(Choices[Index].Index) && Choices[Index].Index != ActiveIndex
				&& Team[Choices[Index].Index].CurrentHP > 0 ? EError::None : EError::InvalidSwitch;
		}
		else if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Capture)
		{
			if (Side != ESide::A || !State.bCaptureAllowed) Error = EError::CaptureNotAllowed;
			else
			{
				Device = Choices[Index].CaptureDevice.LoadSynchronous();
				Error = IsValid(Device) && Device->IsConfigured()
					? EError::None : EError::InvalidCaptureDevice;
			}
		}
		else Error = EError::InvalidSlot;
		if (Error != EError::None) return Reject(Error, Side);
	}
	FPokeMonsterBattleState Next = State;
	++Next.RoundNumber;
	FPokeMonsterBattleResult Result;
	Result.RoundNumber = Next.RoundNumber;
	for (int32 Index = 0; Index < 2; ++Index)
	{
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		auto& Event = AddEvent(Result, Next,
			Choices[Index].Type == EPokeMonsterBattleChoiceType::Switch ? EEvent::SwitchChosen
				: Choices[Index].Type == EPokeMonsterBattleChoiceType::Capture ? EEvent::CaptureChosen : EEvent::MoveChosen,
			Side, Moves[Index] ? Choices[Index].Index : INDEX_NONE, Moves[Index]);
		if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Switch) Event.TeamIndex = Choices[Index].Index;
		if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Capture) Event.CaptureDeviceId = Device->GetPrimaryAssetId();
	}
	// Switching takes precedence over attacks; the remaining attack targets the incoming creature.
	for (int32 Index = 0; Index < 2; ++Index)
	{
		if (Choices[Index].Type != EPokeMonsterBattleChoiceType::Switch) continue;
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		ActiveIndexFor(Next, Side) = Choices[Index].Index;
		ActiveFor(Next, Side) = TeamFor(Next, Side)[Choices[Index].Index];
		auto& Switched = AddEvent(Result, Next, EEvent::SwitchedIn, Side);
		Switched.TeamIndex = Choices[Index].Index;
		Switched.HPBefore = Switched.HPAfter = ActiveFor(Next, Side).CurrentHP;
	}
	FPokeMonsterDamageResult Damage[2];
	for (int32 Index = 0; Index < 2; ++Index)
	{
		if (!Moves[Index]) continue;
		Damage[Index] = B::CalculateDamage(Index == 0 ? Next.SideA : Next.SideB,
			Index == 0 ? Next.SideB : Next.SideA, Moves[Index]);
		if (!Damage[Index].bValid) return Reject(EError::InvalidDamage, Index == 0 ? ESide::A : ESide::B);
	}
	const bool bBothMove = Moves[0] != nullptr && Moves[1] != nullptr;
	const bool bAFirst = !bBothMove || (Moves[0]->Priority != Moves[1]->Priority
		? Moves[0]->Priority > Moves[1]->Priority
		: Next.SideA.CalculatedStats.Speed >= Next.SideB.CalculatedStats.Speed);
	const int32 Order[2] = {bAFirst ? 0 : 1, bAFirst ? 1 : 0};
	FRandomStream NextRandom = Random;
	// A capture attempt is the player's entire turn and resolves before the wild creature attacks.
	if (ChoiceA.Type == EPokeMonsterBattleChoiceType::Capture)
	{
		const auto* Species = Next.SideB.Species.LoadSynchronous();
		const float Chance = FPokeMonsterCaptureLibrary::CalculateChance(Next.SideB.CurrentHP,
			Next.SideB.GetMaxHP(), Species->GetBaseCaptureRate(), Device->GetCaptureBonus());
		const int32 Roll = NextRandom.RandRange(0, 9999);
		const bool bCaught = FPokeMonsterCaptureLibrary::CheckCapture(Chance, Roll);
		auto& Event = AddEvent(Result, Next, bCaught ? EEvent::CaptureSucceeded : EEvent::CaptureFailed, ESide::A);
		Event.CaptureDeviceId = Device->GetPrimaryAssetId();
		Event.CaptureChance = Chance;
		Event.CaptureRoll = Roll;
		if (bCaught)
		{
			Next.CapturedCreature = Next.SideB;
			Next.Phase = EPhase::Finished;
			Next.Winner = ESide::A;
			Next.EndReason = EPokeMonsterBattleEndReason::Captured;
			AddEvent(Result, Next, EEvent::BattleEnded, ESide::A);
			SyncActive(Next);
			State = MoveTemp(Next);
			Random = NextRandom;
			Result.bSucceeded = true;
			Result.Winner = State.Winner;
			return Result;
		}
	}
	for (const int32 Index : Order)
	{
		if (!Moves[Index]) continue;
		auto& Attacker = Index == 0 ? Next.SideA : Next.SideB;
		auto& Defender = Index == 0 ? Next.SideB : Next.SideA;
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		if (Attacker.CurrentHP <= 0 || Defender.CurrentHP <= 0) break;
		const int32 BeforePP = Attacker.GetMoveSlots()[Choices[Index].Index].GetCurrentPP();
		if (!Attacker.ConsumeMovePP(Choices[Index].Index)) return Reject(EError::InvalidPP, Side);
		const int32 Roll = NextRandom.RandRange(0, 99);
		auto& Executed = AddEvent(Result, Next, EEvent::MoveExecuted, Side, Choices[Index].Index, Moves[Index]);
		Executed.PPBefore = BeforePP;
		Executed.PPAfter = BeforePP - 1;
		Executed.HitRoll = Roll;
		if (!B::CheckHit(Moves[Index], Roll))
		{
			AddEvent(Result, Next, EEvent::Missed, Side, Choices[Index].Index, Moves[Index]).HitRoll = Roll;
			continue;
		}
		if (Moves[Index]->Category == EPokeMonsterMoveCategory::Status) continue;
		const float Multiplier = Damage[Index].TypeMultiplier;
		if (Multiplier != 1.0f)
		{
			const EEvent Effect = Multiplier == 0.0f ? EEvent::Immune
				: Multiplier > 1.0f ? EEvent::SuperEffective : EEvent::NotVeryEffective;
			AddEvent(Result, Next, Effect, Side, Choices[Index].Index, Moves[Index]).TypeMultiplier = Multiplier;
		}
		if (Multiplier == 0.0f) continue;
		const int32 BeforeHP = Defender.CurrentHP;
		const int32 AppliedDamage = FMath::Min(BeforeHP, Damage[Index].Damage);
		Defender.CurrentHP -= AppliedDamage;
		auto& DamageEvent = AddEvent(Result, Next, EEvent::Damage, Side, Choices[Index].Index, Moves[Index]);
		DamageEvent.Damage = AppliedDamage;
		DamageEvent.TypeMultiplier = Multiplier;
		DamageEvent.HPBefore = BeforeHP;
		DamageEvent.HPAfter = Defender.CurrentHP;
		if (Defender.CurrentHP == 0)
		{
			AddEvent(Result, Next, EEvent::KnockedOut, Side, Choices[Index].Index, Moves[Index]).HPAfter = 0;
			SyncActive(Next);
			const ESide FaintedSide = Side == ESide::A ? ESide::B : ESide::A;
			if (!HasLiving(TeamFor(Next, FaintedSide)))
			{
				Next.Phase = EPhase::Finished;
				Next.Winner = Side;
				Next.EndReason = EPokeMonsterBattleEndReason::Knockout;
				AddEvent(Result, Next, EEvent::BattleEnded, Side);
			}
			else Next.Phase = EPhase::AwaitingSwitch;
			break;
		}
	}
	SyncActive(Next);
	State = MoveTemp(Next);
	Random = NextRandom;
	Result.bSucceeded = true;
	Result.Winner = State.Winner;
	return Result;
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::ForceSwitch(ESide Side, int32 TeamIndex)
{
	if (State.Phase == EPhase::Uninitialized) return Reject(EError::NotInitialized);
	if (State.Phase == EPhase::Finished) return Reject(EError::BattleFinished);
	if (State.Phase != EPhase::AwaitingSwitch || Side == ESide::None
		|| ActiveFor(State, Side).CurrentHP > 0) return Reject(EError::SwitchRequired, Side);
	const auto& Team = TeamFor(State, Side);
	if (!Team.IsValidIndex(TeamIndex) || TeamIndex == ActiveIndexFor(State, Side)
		|| Team[TeamIndex].CurrentHP <= 0) return Reject(EError::InvalidSwitch, Side);
	ActiveIndexFor(State, Side) = TeamIndex;
	ActiveFor(State, Side) = Team[TeamIndex];
	State.Phase = EPhase::AwaitingChoices;
	FPokeMonsterBattleResult Result;
	Result.bSucceeded = true;
	Result.RoundNumber = State.RoundNumber;
	auto& Switched = AddEvent(Result, State, EEvent::SwitchedIn, Side);
	Switched.TeamIndex = TeamIndex;
	Switched.HPBefore = Switched.HPAfter = ActiveFor(State, Side).CurrentHP;
	return Result;
}
