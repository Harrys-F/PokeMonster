#include "PokeMonsterBattleSession.h"
#include "PokeMonsterTypeChart.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"

namespace
{
	using EError = EPokeMonsterBattleError;
	using ESide = EPokeMonsterBattleSide;
	using EPhase = EPokeMonsterBattlePhase;
	using EEvent = EPokeMonsterBattleEventType;
	using B = UPokeMonsterBattleLibrary;

	EError ValidateCreature(const FPokeMonsterCreatureInstance& Creature)
	{
		if (Creature.Species.IsNull()) return EError::MissingSpecies;
		if (!Creature.IsValid()) return EError::InvalidCreature;
		const auto* Species = Creature.Species.LoadSynchronous();
		if (!IsValid(Species)) return EError::MissingSpecies;
		if (Creature.CurrentHP <= 0) return EError::CreatureFainted;
		const auto& Stats = Creature.CalculatedStats;
		if (Stats.MaxHP <= 0 || Creature.CurrentHP > Stats.MaxHP || Stats.Attack <= 0 || Stats.Defense <= 0
			|| Stats.SpecialAttack <= 0 || Stats.SpecialDefense <= 0 || Stats.Speed <= 0
			|| PokeMonsterTypeChart::GetMultiplier(EPokeMonsterCreatureType::Normal,
				Species->GetPrimaryType(), Species->GetSecondaryType()) < 0.0f) return EError::InvalidStats;
		return EError::None;
	}

	EError ValidateSelection(const FPokeMonsterCreatureInstance& Creature, const int32 SlotIndex, UPokeMonsterMoveData*& OutMove)
	{
		if (SlotIndex < 0 || SlotIndex >= FPokeMonsterCreatureInstance::MoveSlotCount
			|| !Creature.GetMoveSlots().IsValidIndex(SlotIndex)) return EError::InvalidSlot;
		const auto& Slot = Creature.GetMoveSlots()[SlotIndex];
		OutMove = Slot.GetMove().LoadSynchronous();
		if (!IsValid(OutMove)) return EError::MissingMove;
		if (!OutMove->IsConfigured()) return EError::InvalidMove;
		if (Slot.GetMaxPP() != OutMove->MaxPP || Slot.GetCurrentPP() < 0 || Slot.GetCurrentPP() > Slot.GetMaxPP()) return EError::InvalidPP;
		return Slot.GetCurrentPP() == 0 ? EError::NoPP : EError::None;
	}

	FPokeMonsterBattleEvent& AddEvent(FPokeMonsterBattleResult& Result, const FPokeMonsterBattleState& State,
		const EEvent Type, const ESide Source, const int32 SlotIndex, const UPokeMonsterMoveData* Move)
	{
		auto& Event = Result.Events.AddDefaulted_GetRef();
		Event.Type = Type;
		Event.RoundNumber = State.RoundNumber;
		Event.Source = Source;
		Event.Target = Source == ESide::A ? ESide::B : ESide::A;
		Event.SourceInstanceId = Source == ESide::A ? State.SideA.InstanceId : State.SideB.InstanceId;
		Event.TargetInstanceId = Source == ESide::A ? State.SideB.InstanceId : State.SideA.InstanceId;
		Event.SlotIndex = SlotIndex;
		if (Move)
		{
			Event.MoveId = Move->GetPrimaryAssetId();
			Event.Category = Move->Category;
		}
		return Event;
	}
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::Reject(const EError Error, const ESide Side) const
{
	FPokeMonsterBattleResult Result;
	Result.Error = Error;
	Result.ErrorSide = Side;
	Result.RoundNumber = State.RoundNumber;
	Result.Winner = State.Winner;
	return Result;
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::Initialize(const FPokeMonsterCreatureInstance& SideA,
	const FPokeMonsterCreatureInstance& SideB, const int32 RandomSeed)
{
	if (State.Phase != EPhase::Uninitialized) return Reject(EError::AlreadyInitialized);
	const EError ErrorA = ValidateCreature(SideA);
	if (ErrorA != EError::None) return Reject(ErrorA, ESide::A);
	const EError ErrorB = ValidateCreature(SideB);
	if (ErrorB != EError::None) return Reject(ErrorB, ESide::B);
	if (SideA.InstanceId == SideB.InstanceId) return Reject(EError::DuplicateCreature);
	State.SideA = SideA;
	State.SideB = SideB;
	State.Phase = EPhase::AwaitingChoices;
	Random.Initialize(RandomSeed);
	for (const auto* Creature : {&State.SideA, &State.SideB})
	{
		RetainedData.AddUnique(Creature->Species.LoadSynchronous());
		for (const auto& Slot : Creature->GetMoveSlots())
		{
			if (auto* Move = Slot.GetMove().LoadSynchronous()) RetainedData.AddUnique(Move);
		}
	}
	FPokeMonsterBattleResult Result;
	Result.bSucceeded = true;
	return Result;
}

FPokeMonsterBattleResult UPokeMonsterBattleSession::ResolveRound(const int32 SlotA, const int32 SlotB)
{
	if (State.Phase == EPhase::Uninitialized) return Reject(EError::NotInitialized);
	if (State.Phase == EPhase::Finished) return Reject(EError::BattleFinished);
	if (State.RoundNumber == MAX_int32) return Reject(EError::RoundLimitReached);
	UPokeMonsterMoveData* Moves[2] = {nullptr, nullptr};
	const int32 Slots[2] = {SlotA, SlotB};
	const FPokeMonsterCreatureInstance* Creatures[2] = {&State.SideA, &State.SideB};
	FPokeMonsterDamageResult Damage[2];
	for (int32 Index = 0; Index < 2; ++Index)
	{
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		EError Error = ValidateCreature(*Creatures[Index]);
		if (Error != EError::None) return Reject(Error, Side);
		Error = ValidateSelection(*Creatures[Index], Slots[Index], Moves[Index]);
		if (Error != EError::None) return Reject(Error, Side);
	}
	// Preflight both damage calculations before PP, RNG or HP changes. No stat-changing effects yet.
	for (int32 Index = 0; Index < 2; ++Index)
	{
		Damage[Index] = B::CalculateDamage(*Creatures[Index], *Creatures[1 - Index], Moves[Index]);
		if (!Damage[Index].bValid) return Reject(EError::InvalidDamage, Index == 0 ? ESide::A : ESide::B);
	}
	const bool bAFirst = Moves[0]->Priority != Moves[1]->Priority ? Moves[0]->Priority > Moves[1]->Priority
		: State.SideA.CalculatedStats.Speed >= State.SideB.CalculatedStats.Speed; // Exact ties: A first.
	const int32 Order[2] = {bAFirst ? 0 : 1, bAFirst ? 1 : 0};
	FPokeMonsterBattleState Next = State;
	FRandomStream NextRandom = Random;
	++Next.RoundNumber;
	FPokeMonsterBattleResult Result;
	Result.RoundNumber = Next.RoundNumber;
	AddEvent(Result, Next, EEvent::MoveChosen, ESide::A, SlotA, Moves[0]);
	AddEvent(Result, Next, EEvent::MoveChosen, ESide::B, SlotB, Moves[1]);
	for (const int32 Index : Order)
	{
		auto& Attacker = Index == 0 ? Next.SideA : Next.SideB;
		auto& Defender = Index == 0 ? Next.SideB : Next.SideA;
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		if (Attacker.CurrentHP <= 0 || Defender.CurrentHP <= 0) break;
		const int32 BeforePP = Attacker.GetMoveSlots()[Slots[Index]].GetCurrentPP();
		if (!Attacker.ConsumeMovePP(Slots[Index])) return Reject(EError::InvalidPP, Side);
		const int32 Roll = NextRandom.RandRange(0, 99);
		auto& Executed = AddEvent(Result, Next, EEvent::MoveExecuted, Side, Slots[Index], Moves[Index]);
		Executed.PPBefore = BeforePP;
		Executed.PPAfter = BeforePP - 1;
		Executed.HitRoll = Roll;
		if (!B::CheckHit(Moves[Index], Roll))
		{
			AddEvent(Result, Next, EEvent::Missed, Side, Slots[Index], Moves[Index]).HitRoll = Roll;
			continue;
		}
		if (Moves[Index]->Category == EPokeMonsterMoveCategory::Status) continue;
		const float Multiplier = Damage[Index].TypeMultiplier;
		if (Multiplier != 1.0f)
		{
			const EEvent Effect = Multiplier == 0.0f ? EEvent::Immune
				: Multiplier > 1.0f ? EEvent::SuperEffective : EEvent::NotVeryEffective;
			AddEvent(Result, Next, Effect, Side, Slots[Index], Moves[Index]).TypeMultiplier = Multiplier;
		}
		if (Multiplier == 0.0f) continue;
		const int32 BeforeHP = Defender.CurrentHP;
		const int32 AppliedDamage = FMath::Min(BeforeHP, Damage[Index].Damage);
		Defender.CurrentHP -= AppliedDamage;
		auto& DamageEvent = AddEvent(Result, Next, EEvent::Damage, Side, Slots[Index], Moves[Index]);
		DamageEvent.Damage = AppliedDamage;
		DamageEvent.TypeMultiplier = Multiplier;
		DamageEvent.HPBefore = BeforeHP;
		DamageEvent.HPAfter = Defender.CurrentHP;
		if (Defender.CurrentHP == 0)
		{
			AddEvent(Result, Next, EEvent::KnockedOut, Side, Slots[Index], Moves[Index]).HPAfter = 0;
			Next.Phase = EPhase::Finished;
			Next.Winner = Side;
			AddEvent(Result, Next, EEvent::BattleEnded, Side, INDEX_NONE, nullptr);
			break; // The defeated opponent neither attacks nor spends PP/a random draw.
		}
	}
	State = MoveTemp(Next);
	Random = NextRandom;
	Result.bSucceeded = true;
	Result.Winner = State.Winner;
	return Result;
}
