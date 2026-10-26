#include "PokeMonsterBattleSession.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "PokeMonsterTypeChart.h"
#include "../Items/PokeMonsterItemData.h"
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
		if(uint8(Creature.Status)>uint8(EPokeMonsterCreatureStatus::Freeze) || (Creature.Status==EPokeMonsterCreatureStatus::Sleep?Creature.StatusTurns<1||Creature.StatusTurns>15:Creature.StatusTurns!=0))return EError::InvalidCreature;
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
 FPokeMonsterBattleVolatileEffects& EffectsFor(FPokeMonsterBattleState& S,ESide Side){return Side==ESide::A?S.EffectsA:S.EffectsB;}
 int32& StageFor(FPokeMonsterBattleState& S,ESide Side,EPokeMonsterBattleStat Stat)
 {
  auto& E=EffectsFor(S,Side);
  switch(Stat){case EPokeMonsterBattleStat::Attack:return Side==ESide::A?S.AttackStageA:S.AttackStageB;
   case EPokeMonsterBattleStat::Defense:return Side==ESide::A?S.DefenseStageA:S.DefenseStageB;
   case EPokeMonsterBattleStat::Speed:return Side==ESide::A?S.SpeedStageA:S.SpeedStageB;
   case EPokeMonsterBattleStat::SpecialAttack:return E.SpecialAttack;case EPokeMonsterBattleStat::SpecialDefense:return E.SpecialDefense;
   case EPokeMonsterBattleStat::Accuracy:return E.Accuracy;default:return E.Evasion;}
 }
 void ResetVolatile(FPokeMonsterBattleState& S,ESide Side)
 {
  const ESide Other=Side==ESide::A?ESide::B:ESide::A;
  // Both escape restraints belong to the current opposing active combatant.
  EffectsFor(S,Other).TrapTurns=0;EffectsFor(S,Other).TrapSource.Invalidate();EffectsFor(S,Other).SwitchBlockSource.Invalidate();
  EffectsFor(S,Side)=FPokeMonsterBattleVolatileEffects();
  StageFor(S,Side,EPokeMonsterBattleStat::Attack)=StageFor(S,Side,EPokeMonsterBattleStat::Defense)=StageFor(S,Side,EPokeMonsterBattleStat::Speed)=0;
  if(Side==ESide::A)S.bSeededA=false;else S.bSeededB=false;
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
	const TArray<FPokeMonsterCreatureInstance>& TeamB, int32 RandomSeed, bool bAllowCapture, bool bAllowFlee, bool bTrainerExperience)
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
   if(!EffectRules.bExtendedStatus && uint8(Team[Index].Status)>uint8(EPokeMonsterCreatureStatus::Burn))return Reject(EError::InvalidCreature,Side);
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
 State.Weather=EffectRules.InitialWeather;State.WeatherTurns=State.Weather==EPokeMonsterBattleWeather::Clear?0:EffectRules.InitialWeatherTurns;
 State.bFleeAllowed=bAllowFlee;State.bTrainerExperience=bTrainerExperience;State.ParticipantsA.Add(State.SideA.InstanceId);
	Random.Initialize(RandomSeed);
	for (const auto* Team : {&State.TeamA, &State.TeamB})
		for (const auto& Creature : *Team)
		{
			const auto* Species=Creature.Species.LoadSynchronous();
			RetainedData.AddUnique(const_cast<UPokeMonsterCreatureSpeciesData*>(Species));
			if(Species)for(const auto& Entry:Species->LevelUpMoves)
				if(auto* Move=Entry.Move.LoadSynchronous())RetainedData.AddUnique(Move);
			for (const auto& Slot : Creature.GetLearnedMoves())
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
	if (HasPendingLearning()) return Reject(EError::LearningRequired);
	if (State.RoundNumber == MAX_int32) return Reject(EError::RoundLimitReached);
	FPokeMonsterBattleChoice Choices[2] = {ChoiceA, ChoiceB};
 for(int32 I=0;I<2;++I){const ESide Side=I==0?ESide::A:ESide::B;const int32 Forced=ForcedMoveSlot(Side);
  if(Forced!=INDEX_NONE){if(Choices[I].Type!=EPokeMonsterBattleChoiceType::Move)return Reject(Choices[I].Type==EPokeMonsterBattleChoiceType::Flee?EError::FleeNotAllowed:EError::InvalidMove,Side);Choices[I].Index=Forced;}}
	UPokeMonsterMoveData* Moves[2] = {nullptr, nullptr};
	UPokeMonsterCaptureDeviceData* Device = nullptr;
 UPokeMonsterItemData* Item=nullptr;
	for (int32 Index = 0; Index < 2; ++Index)
	{
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		const auto& Creature = Index == 0 ? State.SideA : State.SideB;
		EError Error = ValidateCreature(Creature);
		if (Error != EError::None) return Reject(Error, Side);
		if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Move)
			{
    if(Choices[Index].Index==INDEX_NONE&&!HasSelectableMove(Side)){
     auto* Fallback=NewObject<UPokeMonsterMoveData>(this);Fallback->InternalId=TEXT("Struggle");Fallback->DisplayName=FText::FromString(TEXT("Verzweifler"));Fallback->BasePower=50;Fallback->MaxPP=1;Fallback->Effect.EffectId=TEXT("Struggle");RetainedData.Add(Fallback);Moves[Index]=Fallback;
    }else {
     Error=ValidateSelection(Creature,Choices[Index].Index,Moves[Index]);
     if(Error==EError::NoPP && ForcedMoveSlot(Side)==Choices[Index].Index)Error=EError::None;
     if(Error==EError::None && !CanSelectMove(Side,Choices[Index].Index))Error=EError::InvalidMove;
     if(Error==EError::None && ForcedMoveSlot(Side)==Choices[Index].Index)
      if(auto* Forced=EffectsFor(State,Side).ForcedMoveData.LoadSynchronous())Moves[Index]=Forced;
    }
   }
		else if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Switch)
		{
   if(!CanLeave(Side))return Reject(EError::InvalidSwitch,Side);
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
  else if(Choices[Index].Type==EPokeMonsterBattleChoiceType::Flee){if(Side!=ESide::A||!State.bFleeAllowed||!CanLeave(Side))Error=EError::FleeNotAllowed;}
  else if(Choices[Index].Type==EPokeMonsterBattleChoiceType::Item){
   Item=Choices[Index].Item.LoadSynchronous();const auto& T=State.TeamA;const int Target=Choices[Index].Index;
   if(Side!=ESide::A||!Item||!Item->IsConfigured()||!Item->CanUseInBattle()||Item->GetCategory()!=EPokeMonsterItemCategory::Healing)Error=EError::InvalidItem;
   else if(!T.IsValidIndex(Target)||T[Target].CurrentHP<=0||T[Target].CurrentHP>=T[Target].GetMaxHP())Error=EError::InvalidItemTarget;
  }
		else Error = EError::InvalidSlot;
  if(!EffectRules.bExtendedStatus && Moves[Index])for(const auto& E:Moves[Index]->GetEffectComponents())
   if(E.Kind==EPokeMonsterEffectKind::PrimaryStatus && E.Status!=EPokeMonsterCreatureStatus::Burn)Error=EError::InvalidMove;
		if (Error != EError::None) return Reject(Error, Side);
	}
	FPokeMonsterBattleState Next = State;
	++Next.RoundNumber;
 Next.EffectsA.bFlinched=Next.EffectsB.bFlinched=false;
 Next.EffectsA.bProtected=Next.EffectsB.bProtected=false;
	FPokeMonsterBattleResult Result;
	Result.RoundNumber = Next.RoundNumber;
	for (int32 Index = 0; Index < 2; ++Index)
	{
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		auto& Event = AddEvent(Result, Next,
			Choices[Index].Type == EPokeMonsterBattleChoiceType::Switch ? EEvent::SwitchChosen
				: Choices[Index].Type == EPokeMonsterBattleChoiceType::Capture ? EEvent::CaptureChosen
    : Choices[Index].Type==EPokeMonsterBattleChoiceType::Flee?EEvent::FleeChosen
    : Choices[Index].Type==EPokeMonsterBattleChoiceType::Item?EEvent::ItemChosen:EEvent::MoveChosen,
			Side, Moves[Index] ? Choices[Index].Index : INDEX_NONE, Moves[Index]);
		if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Switch) Event.TeamIndex = Choices[Index].Index;
		if (Choices[Index].Type == EPokeMonsterBattleChoiceType::Capture) Event.CaptureDeviceId = Device->GetPrimaryAssetId();
	}
 // Use the existing switch transaction for ordinary switches and forced replacements.
 auto PerformSwitch=[&](int32 Index,int32 Target)
 {
  const ESide Side=Index==0?ESide::A:ESide::B;
  SyncActive(Next);ActiveIndexFor(Next,Side)=Target;ActiveFor(Next,Side)=TeamFor(Next,Side)[Target];
  ResetVolatile(Next,Side);
  if(Side==ESide::A)Next.ParticipantsA.Add(Next.SideA.InstanceId);
  else {Next.ParticipantsA.Reset();if(Next.SideA.CurrentHP>0)Next.ParticipantsA.Add(Next.SideA.InstanceId);}
  auto& E=AddEvent(Result,Next,EEvent::SwitchedIn,Side);E.TeamIndex=Target;E.HPBefore=E.HPAfter=ActiveFor(Next,Side).CurrentHP;
 };
 bool DeferredSwitch[2]={false,false};
 for(int32 I=0;I<2;++I)if(Choices[I].Type==EPokeMonsterBattleChoiceType::Switch)
 {
  DeferredSwitch[I]=Moves[1-I] && Moves[1-I]->HasEffect(EPokeMonsterEffectKind::SwitchPunish);
  if(!DeferredSwitch[I])PerformSwitch(I,Choices[I].Index);
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
	auto TurnSpeed=[&](ESide Side){const auto& C=ActiveFor(Next,Side);const int32 Speed=EffectRules.bCrystal?B::ApplyCrystalStage(C.CalculatedStats.Speed,StageFor(Next,Side,EPokeMonsterBattleStat::Speed)):B::ApplyStage(C.CalculatedStats.Speed,StageFor(Next,Side,EPokeMonsterBattleStat::Speed));return C.Status==EPokeMonsterCreatureStatus::Paralysis?FMath::Max(1,Speed/EffectRules.ParalysisSpeedDivisor):Speed;};
 const bool bAFirst = DeferredSwitch[0]?false:DeferredSwitch[1]?true:!bBothMove || (Moves[0]->Priority != Moves[1]->Priority
		? Moves[0]->Priority > Moves[1]->Priority
		: TurnSpeed(ESide::A) >= TurnSpeed(ESide::B));
	const int32 Order[2] = {bAFirst ? 0 : 1, bAFirst ? 1 : 0};
 bool HasActed[2]={Choices[0].Type!=EPokeMonsterBattleChoiceType::Move,Choices[1].Type!=EPokeMonsterBattleChoiceType::Move};
	FRandomStream NextRandom = Random;
 // All mutations, including RNG, remain provisional until the turn commits.
 auto AwardExperience=[&](){
  SyncActive(Next);const auto* Species=Next.SideB.Species.LoadSynchronous();const int Yield=Species?Species->GetBaseExperienceYield():0;if(Yield<=0)return;
  int Count=0;for(const auto& C:Next.TeamA)if(C.CurrentHP>0&&Next.ParticipantsA.Contains(C.InstanceId))++Count;if(!Count)return;
  int64 XP=int64(Yield)*Next.SideB.Level/7/Count;if(Next.bTrainerExperience)XP=XP*3/2;
  for(int I=0;I<Next.TeamA.Num();++I){auto& C=Next.TeamA[I];if(C.CurrentHP<=0||!Next.ParticipantsA.Contains(C.InstanceId))continue;const int32 OldLevel=C.Level;const auto OldSlots=C.GetMoveSlots();const auto G=C.AddExperience(XP);if(!G.bSucceeded||G.ExperienceAdded<=0)continue;
   auto& E=AddEvent(Result,Next,EEvent::ExperienceGained,ESide::A);E.TeamIndex=I;E.Target=ESide::A;E.TargetInstanceId=C.InstanceId;E.ExperienceAdded=G.ExperienceAdded;
   if(G.LevelsGained>0){auto& L=AddEvent(Result,Next,EEvent::LevelUp,ESide::A);L.TeamIndex=I;L.Target=ESide::A;L.TargetInstanceId=C.InstanceId;L.LevelsGained=G.LevelsGained;L.LevelBefore=OldLevel;L.LevelAfter=C.Level;
    for(const auto& Entry:C.Species.LoadSynchronous()->LevelUpMoves)
    {
     if(Entry.Level<=OldLevel||Entry.Level>C.Level)continue;
     if(!Entry.UnavailableMoveName.IsEmpty())
     {
      auto& N=AddEvent(Result,Next,EEvent::MoveUnavailable,ESide::A);N.TargetInstanceId=C.InstanceId;N.Information=FText::Format(FText::FromString(TEXT("{0}: noch nicht spielbar ({1}).")),Entry.UnavailableMoveName,Entry.UnavailableReason);
     }
     else if(auto* Move=Entry.Move.LoadSynchronous())
     {
      if(!OldSlots.ContainsByPredicate([Move](const auto& S){return S.GetMove().LoadSynchronous()==Move;})&&C.GetMoveSlots().ContainsByPredicate([Move](const auto& S){return S.GetMove().LoadSynchronous()==Move;}))
      {auto& N=AddEvent(Result,Next,EEvent::MoveLearned,ESide::A);N.TargetInstanceId=C.InstanceId;N.Information=FText::Format(FText::FromString(TEXT("{0} erlernt!")),Move->GetPlayerFacingName());}
     }
    }
    const auto Options=UPokeMonsterCreatureProgression::GetEvolutionOptions(C,FPokeMonsterEvolutionContext());
    if(!Options.IsEmpty()){auto& Notice=AddEvent(Result,Next,EEvent::EvolutionPending,ESide::A);Notice.TargetInstanceId=C.InstanceId;Notice.TeamIndex=I;}
   }
  }Next.SideA=Next.TeamA[Next.ActiveIndexA];
 };
 auto Knockout=[&](ESide Fainted){
  for(ESide Side:{ESide::A,ESide::B})if(ActiveFor(Next,Side).CurrentHP==0){auto& K=AddEvent(Result,Next,EEvent::KnockedOut,Side==ESide::A?ESide::B:ESide::A);K.HPAfter=0;}
  for(ESide Dead:{ESide::A,ESide::B})if(ActiveFor(Next,Dead).CurrentHP==0){auto& Other=EffectsFor(Next,Dead==ESide::A?ESide::B:ESide::A);Other.TrapTurns=0;Other.TrapSource.Invalidate();Other.SwitchBlockSource.Invalidate();}
  SyncActive(Next);if(Next.SideB.CurrentHP==0)AwardExperience();
  if(!HasLiving(Next.TeamA)||!HasLiving(Next.TeamB)){Next.Phase=EPhase::Finished;Next.Winner=!HasLiving(Next.TeamA)?ESide::B:ESide::A;Next.EndReason=EPokeMonsterBattleEndReason::Knockout;AddEvent(Result,Next,EEvent::BattleEnded,Next.Winner);}else Next.Phase=EPhase::AwaitingSwitch;
 };
 auto BurnTick=[&](ESide Side){
  if(EffectRules.bCrystal)EffectsFor(Next,Side==ESide::A?ESide::B:ESide::A).bDestinyBond=false;
  auto& C=ActiveFor(Next,Side);if(C.CurrentHP<=0||Next.Phase!=EPhase::AwaitingChoices)return;
  auto Tick=[&](int Divisor,EEvent Type){const int Before=C.CurrentHP;C.CurrentHP=FMath::Max(0,C.CurrentHP-FMath::Max(1,C.GetMaxHP()/Divisor));auto& E=AddEvent(Result,Next,Type,Side);E.Target=Side;E.TargetInstanceId=C.InstanceId;E.HPBefore=Before;E.HPAfter=C.CurrentHP;E.Damage=Before-C.CurrentHP;if(C.CurrentHP==0)Knockout(Side);return Before-C.CurrentHP;};
  if(C.Status==EPokeMonsterCreatureStatus::Burn)Tick(8,EEvent::BurnDamage);
  else if(EffectRules.bCrystal && C.Status==EPokeMonsterCreatureStatus::Poison)Tick(EffectRules.PoisonDenominator,EEvent::StatusDamage);
  if(!EffectRules.bCrystal || Next.Phase!=EPhase::AwaitingChoices)return;
  if(Side==ESide::A?Next.bSeededA:Next.bSeededB)
  {
   const int Removed=Tick(8,EEvent::SeedDamage);auto& Other=ActiveFor(Next,Side==ESide::A?ESide::B:ESide::A);
   if(Other.CurrentHP>0){const int Before=Other.CurrentHP;Other.CurrentHP=FMath::Min(Other.GetMaxHP(),Before+Removed);auto& E=AddEvent(Result,Next,EEvent::SeedHeal,Side==ESide::A?ESide::B:ESide::A);E.Target=E.Source;E.TargetInstanceId=Other.InstanceId;E.HPBefore=Before;E.HPAfter=Other.CurrentHP;E.RestoredHP=Other.CurrentHP-Before;}
  }
  if(Next.Phase==EPhase::AwaitingChoices && EffectsFor(Next,Side).bCursed)Tick(4,EEvent::StatusDamage);
 };

 auto Notice=[&](EEvent Type,ESide Source,ESide Target,const FString& Text,int32 Slot,const UPokeMonsterMoveData* Move)->FPokeMonsterBattleEvent&
 {
  auto& E=AddEvent(Result,Next,Type,Source,Slot,Move);E.Target=Target;E.TargetInstanceId=ActiveFor(Next,Target).InstanceId;E.Information=FText::FromString(Text);return E;
 };
 auto ApplyComponents=[&](ESide Side,const UPokeMonsterMoveData* Move,int32 Slot,int32 ActualDamage,bool bSecondary)
 {
  const ESide Other=Side==ESide::A?ESide::B:ESide::A;
  for(const auto& C:Move->GetEffectComponents())
  {
   if(C.Kind==EPokeMonsterEffectKind::FixedDamage || C.Kind==EPokeMonsterEffectKind::MultiHit || C.Kind==EPokeMonsterEffectKind::Charge || C.Kind==EPokeMonsterEffectKind::Rampage)continue;
   // Status moves resolve once before damage, damaging moves once after their hit sequence.
   if(bSecondary != (Move->Category!=EPokeMonsterMoveCategory::Status))continue;
   const ESide Target=C.bSelf?Side:Other;auto& T=ActiveFor(Next,Target);auto& V=EffectsFor(Next,Target);
   if(T.CurrentHP<=0)continue;
   auto Failed=[&](){Notice(EEvent::EffectFailed,Side,Target,TEXT("Die Wirkung schlägt fehl."),Slot,Move);};
   if(C.Kind==EPokeMonsterEffectKind::Drain || C.Kind==EPokeMonsterEffectKind::Recoil)
   {
    if(!bSecondary || ActualDamage<=0)continue;
   }
   if(!C.bSelf && !Move->bBypassProtect && EffectsFor(Next,Other).bProtected){Notice(EEvent::Protected,Side,Target,TEXT("Das Ziel ist geschützt."),Slot,Move);continue;}
   if(!C.bSelf && (C.Kind==EPokeMonsterEffectKind::PrimaryStatus || C.Kind==EPokeMonsterEffectKind::Confusion)
    && (Target==ESide::A?Next.SafeguardTurnsA:Next.SafeguardTurnsB)>0)
   {if(!C.bSecondary)Notice(EEvent::Protected,Side,Target,TEXT("Bodyguard verhindert das Statusproblem."),Slot,Move);continue;}
   // Eligibility precedes the legacy burn RNG draw, as in the original battle session.
   if(C.Kind==EPokeMonsterEffectKind::PrimaryStatus)
   {
    if(C.Status==EPokeMonsterCreatureStatus::Freeze && Next.Weather==EPokeMonsterBattleWeather::Sun){if(!C.bSecondary)Failed();continue;}
    const auto* S=T.Species.LoadSynchronous();
    if(T.Status!=EPokeMonsterCreatureStatus::None || !S || C.ImmuneTypes.Contains(S->GetPrimaryType()) || C.ImmuneTypes.Contains(S->GetSecondaryType())){if(!C.bSecondary)Failed();continue;}
   }
   const bool LegacyDraw=Move->Effects.IsEmpty() && C.bSecondary;
   if(C.ChancePercent==0 && !LegacyDraw)continue;
   if((LegacyDraw || C.ChancePercent<100) && (EffectRules.bCrystal?NextRandom.RandRange(0,255)>=C.ChancePercent*255/100:NextRandom.RandRange(0,99)>=C.ChancePercent))continue;
   if(C.Kind==EPokeMonsterEffectKind::Stage)
   {
    int32& Stage=StageFor(Next,Target,C.Stat);const int32 Was=Stage;Stage=FMath::Clamp(Stage+C.Stages,-6,6);
    EEvent Type=EEvent::StatChanged;
    if(C.Stat==EPokeMonsterBattleStat::Attack && C.Stages<0)Type=EEvent::AttackLowered;
    else if(C.Stat==EPokeMonsterBattleStat::Defense)Type=C.Stages>0?EEvent::DefenseRaised:EEvent::DefenseLowered;
    else if(C.Stat==EPokeMonsterBattleStat::Speed && C.Stages<0)Type=EEvent::SpeedLowered;
    static const TCHAR* Names[]={TEXT("Angriff"),TEXT("Verteidigung"),TEXT("Spezial-Angriff"),TEXT("Spezial-Verteidigung"),TEXT("Initiative"),TEXT("Genauigkeit"),TEXT("Ausweichwert")};
    auto& E=Notice(Was==Stage?EEvent::EffectFailed:Type,Side,Target,Was==Stage?TEXT("Die Stufengrenze ist erreicht."):FString::Printf(TEXT("%s %s (%+d)."),Names[uint8(C.Stat)],C.Stages>0?TEXT("steigt"):TEXT("sinkt"),Stage-Was),Slot,Move);E.StageAfter=Stage;
   }
   else if(C.Kind==EPokeMonsterEffectKind::PrimaryStatus)
   {
    const auto* Species=T.Species.LoadSynchronous();
    if(T.Status!=EPokeMonsterCreatureStatus::None || !Species || C.ImmuneTypes.Contains(Species->GetPrimaryType()) || C.ImmuneTypes.Contains(Species->GetSecondaryType())){Failed();continue;}
    T.Status=C.Status;T.StatusTurns=C.Status==EPokeMonsterCreatureStatus::Sleep?NextRandom.RandRange(C.MinTurns,C.MaxTurns):0;
    V.bJustFrozen=C.Status==EPokeMonsterCreatureStatus::Freeze;
    Notice(C.Status==EPokeMonsterCreatureStatus::Burn?EEvent::Burned:EEvent::StatusApplied,Side,Target,TEXT("Statusproblem: ")+B::StatusLabel(C.Status).ToString(),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Heal || C.Kind==EPokeMonsterEffectKind::Drain)
   {
    const int32 Base=C.Kind==EPokeMonsterEffectKind::Drain?ActualDamage:T.GetMaxHP();
    int32 Numerator=C.Numerator,Denominator=C.Denominator;
    if(C.Kind==EPokeMonsterEffectKind::Heal && C.Amount>0){const bool Favored=C.Amount==EffectRules.TimeOfDay;Denominator=Favored?2:4;if(Next.Weather==EPokeMonsterBattleWeather::Rain || Next.Weather==EPokeMonsterBattleWeather::Sand)Denominator*=2;Numerator=Next.Weather==EPokeMonsterBattleWeather::Sun?2:1;}
    const int32 Amount=int32(FMath::Min<int64>(MAX_int32,FMath::Max<int64>(1,int64(Base)*Numerator/Denominator)));
    const int32 Before=T.CurrentHP;T.CurrentHP=int32(FMath::Min<int64>(T.GetMaxHP(),int64(Before)+Amount));
    if(T.CurrentHP==Before){if(C.Kind==EPokeMonsterEffectKind::Heal)Failed();continue;}
    auto& E=Notice(EEvent::Healed,Side,Target,TEXT("KP wiederhergestellt."),Slot,Move);E.HPBefore=Before;E.HPAfter=T.CurrentHP;E.RestoredHP=T.CurrentHP-Before;
   }
   else if(C.Kind==EPokeMonsterEffectKind::Recoil)
   {
    const int32 Before=T.CurrentHP;T.CurrentHP=int32(FMath::Max<int64>(0,int64(Before)-FMath::Max<int64>(1,int64(ActualDamage)*C.Numerator/C.Denominator)));
    auto& E=Notice(EEvent::Recoil,Side,Target,TEXT("Rückstoß."),Slot,Move);E.HPBefore=Before;E.HPAfter=T.CurrentHP;E.Damage=Before-T.CurrentHP;
   }
   else if(C.Kind==EPokeMonsterEffectKind::Flinch)V.bFlinched=true;
   else if(C.Kind==EPokeMonsterEffectKind::Confusion)
   {
    if(V.ConfusionTurns>0){Failed();continue;}V.ConfusionTurns=NextRandom.RandRange(C.MinTurns,C.MaxTurns);Notice(EEvent::Confused,Side,Target,TEXT("Verwirrung!"),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Protect)
   {
    int64 Chance=100;for(int32 I=0;I<FMath::Min(V.ProtectStreak,20);++I)Chance=Chance*C.Numerator/C.Denominator;
    const bool Success=EffectRules.bCrystal?(!HasActed[Side==ESide::A?1:0] && NextRandom.RandRange(0,254)<(255>>FMath::Min(V.ProtectStreak,8))):NextRandom.RandRange(0,99)<Chance;
    if(!Success){V.ProtectStreak=0;Failed();continue;}
    V.bProtected=true;++V.ProtectStreak;Notice(EEvent::Protected,Side,Target,TEXT("Schutz aufgebaut."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Disable)
   {
    const int32 Last=V.LastMoveSlot;
    if(V.DisableTurns>0 || !T.GetMoveSlots().IsValidIndex(Last) || T.GetMoveSlots()[Last].GetCurrentPP()<=0){Failed();continue;}
    V.DisabledSlot=Last;V.DisableTurns=NextRandom.RandRange(C.MinTurns,C.MaxTurns);
    Notice(EEvent::StatusApplied,Side,Target,TEXT("Die zuletzt verwendete Attacke ist blockiert."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Spite)
   {
    const int32 Last=V.LastMoveSlot;if(!T.GetMoveSlots().IsValidIndex(Last) || T.GetMoveSlots()[Last].GetCurrentPP()<=0){Failed();continue;}
    const int32 Before=T.GetMoveSlots()[Last].GetCurrentPP(),Removed=FMath::Min(Before,NextRandom.RandRange(C.MinTurns,C.MaxTurns));
    if(!T.ConsumeMovePP(Last,Removed)){Failed();continue;}
    auto& E=Notice(EEvent::StatusApplied,Side,Target,FString::Printf(TEXT("Die letzte Attacke verliert %d AP."),Removed),Slot,Move);E.PPBefore=Before;E.PPAfter=Before-Removed;
   }
   else if(C.Kind==EPokeMonsterEffectKind::CopyStages)
   {
    bool Any=false;for(int32 I=0;I<7;++I)Any|=StageFor(Next,Other,EPokeMonsterBattleStat(I))!=0;
    if(!Any){Failed();continue;}
    for(int32 I=0;I<7;++I)StageFor(Next,Side,EPokeMonsterBattleStat(I))=StageFor(Next,Other,EPokeMonsterBattleStat(I));
    Notice(EEvent::StatChanged,Side,Side,TEXT("Die Statuswertstufen des Gegners wurden kopiert."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Identify)
   {
    if(V.bIdentified){Failed();continue;}V.bIdentified=true;
    Notice(EEvent::StatusApplied,Side,Target,TEXT("Das Ziel wurde durchschaut."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::ClearBindings)
   {
    auto& Own=EffectsFor(Next,Side);Own.TrapTurns=0;Own.TrapSource.Invalidate();
    if(Side==ESide::A)Next.bSeededA=false;else Next.bSeededB=false;
    Notice(EEvent::StatusRecovered,Side,Side,TEXT("Fesselnde Wirbel und Egelsamen entfernt."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Rain)
   {
    Next.Weather=EPokeMonsterBattleWeather::Rain;Next.WeatherTurns=C.MaxTurns;Notice(EEvent::StatusApplied,Side,Side,TEXT("Regen setzt ein."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::PreventSwitch)
   {
    if(V.SwitchBlockSource.IsValid()){Failed();continue;}V.SwitchBlockSource=ActiveFor(Next,Side).InstanceId;
    Notice(EEvent::StatusApplied,Side,Target,TEXT("Das Ziel kann nicht entkommen."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Trap)
   {
    if(V.TrapTurns>0)continue;V.TrapTurns=NextRandom.RandRange(C.MinTurns,C.MaxTurns)+1;V.TrapSource=ActiveFor(Next,Side).InstanceId;
    Notice(EEvent::StatusApplied,Side,Target,TEXT("Im Feuerwirbel gefangen."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::CriticalFocus)
   {
    auto& Own=EffectsFor(Next,Side);if(Own.FocusStage>0){Failed();continue;}Own.FocusStage=1;Notice(EEvent::StatusApplied,Side,Side,TEXT("Konzentriert sich auf Volltreffer."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::DestinyBond)
   {
    EffectsFor(Next,Side).bDestinyBond=true;Notice(EEvent::StatusApplied,Side,Side,TEXT("Abgangsbund ist aktiv."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Curse)
   {
    const auto* Species=ActiveFor(Next,Side).Species.LoadSynchronous();
    const bool Ghost=Species->GetPrimaryType()==EPokeMonsterCreatureType::Ghost || Species->GetSecondaryType()==EPokeMonsterCreatureType::Ghost;
    if(Ghost)
    {
     if(EffectsFor(Next,Other).bCursed){Failed();continue;}
     EffectsFor(Next,Other).bCursed=true;auto& User=ActiveFor(Next,Side);const int32 Before=User.CurrentHP;User.CurrentHP=FMath::Max(0,Before-FMath::Max(1,User.GetMaxHP()/2));
     auto& E=Notice(EEvent::Recoil,Side,Side,TEXT("Das Ziel wurde mit einem Fluch belegt."),Slot,Move);E.HPBefore=Before;E.HPAfter=User.CurrentHP;E.Damage=Before-User.CurrentHP;
    }
    else
    {
     auto& Atk=StageFor(Next,Side,EPokeMonsterBattleStat::Attack);auto& Def=StageFor(Next,Side,EPokeMonsterBattleStat::Defense);
     if(Atk==6 && Def==6){Failed();continue;}Atk=FMath::Min(6,Atk+1);Def=FMath::Min(6,Def+1);auto& Speed=StageFor(Next,Side,EPokeMonsterBattleStat::Speed);Speed=FMath::Max(-6,Speed-1);
     Notice(EEvent::StatChanged,Side,Side,TEXT("Angriff und Verteidigung steigen, Initiative sinkt."),Slot,Move);
    }
   }
   else if(C.Kind==EPokeMonsterEffectKind::Rage){EffectsFor(Next,Side).bRage=true;}
   else if(C.Kind==EPokeMonsterEffectKind::Safeguard)
   {
    int32& Turns=Target==ESide::A?Next.SafeguardTurnsA:Next.SafeguardTurnsB;
    if(Turns>0){Failed();continue;}Turns=C.MaxTurns;
    Notice(EEvent::Protected,Side,Target,TEXT("Ein schützender Schleier umhüllt das Team."),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::NoEffect)
    Notice(EEvent::EffectFailed,Side,Target,TEXT("Aber es geschieht nichts."),Slot,Move);
   else if(C.Kind==EPokeMonsterEffectKind::ForceSwitch)
   {
    if(Next.bTrainerExperience)
    {
     TArray<int32> Options;auto& Team=TeamFor(Next,Other);
     for(int32 I=0;I<Team.Num();++I)if(I!=ActiveIndexFor(Next,Other) && Team[I].CurrentHP>0)Options.Add(I);
     if(!HasActed[Other==ESide::A?0:1] || Options.IsEmpty()){Failed();continue;}
     PerformSwitch(Other==ESide::A?0:1,Options[NextRandom.RandRange(0,Options.Num()-1)]);
     Notice(EEvent::StatusApplied,Side,Other,TEXT("Ein anderes Pokémon wird in den Kampf geweht."),Slot,Move);
    }
    else if(Next.bFleeAllowed)
    {
     const int32 UserLevel=ActiveFor(Next,Side).Level,TargetLevel=T.Level;
     if(UserLevel<TargetLevel && NextRandom.RandRange(0,UserLevel+TargetLevel)<TargetLevel/4){Failed();continue;}
     Next.Phase=EPhase::Finished;Next.Winner=ESide::None;Next.EndReason=EPokeMonsterBattleEndReason::ForcedOut;
     Notice(EEvent::BattleEnded,Side,Other,TEXT("Der Kampf wurde durch den Wirbelwind beendet."),Slot,Move);
    }
    else Failed();
   }
   else if(C.Kind==EPokeMonsterEffectKind::Screen)
   {
    int32& Turns=Target==ESide::A?Next.ScreenTurnsA:Next.ScreenTurnsB;
    if(Turns>0){Failed();continue;}Turns=C.MaxTurns;Notice(EEvent::Protected,Side,Target,TEXT("Spezialschutz aufgebaut."),Slot,Move);
   }
  }
 };
 if(ChoiceA.Type==EPokeMonsterBattleChoiceType::Flee){
  Next.FleeAttempts=FMath::Min(100,Next.FleeAttempts+1);const int Threshold=EscapeThreshold(Next.SideA.CalculatedStats.Speed,Next.SideB.CalculatedStats.Speed,Next.FleeAttempts),Roll=NextRandom.RandRange(0,255);const bool Escaped=Roll<Threshold;
  auto& E=AddEvent(Result,Next,Escaped?EEvent::FleeSucceeded:EEvent::FleeFailed,ESide::A);E.FleeThreshold=Threshold;E.FleeRoll=Roll;
  if(Escaped){Next.Phase=EPhase::Finished;Next.Winner=ESide::None;Next.EndReason=EPokeMonsterBattleEndReason::Escaped;AddEvent(Result,Next,EEvent::BattleEnded,ESide::None);SyncActive(Next);State=MoveTemp(Next);Random=NextRandom;Result.bSucceeded=true;return Result;}
 }else Next.FleeAttempts=0;
 if(ChoiceA.Type==EPokeMonsterBattleChoiceType::Item){
  auto& C=Next.TeamA[ChoiceA.Index];const int Before=C.CurrentHP;C.CurrentHP=int32(FMath::Min<int64>(C.GetMaxHP(),int64(C.CurrentHP)+Item->GetHealAmount()));if(ChoiceA.Index==Next.ActiveIndexA)Next.SideA=C;
  auto& E=AddEvent(Result,Next,EEvent::Healed,ESide::A);E.Target=ESide::A;E.TargetInstanceId=C.InstanceId;E.TeamIndex=ChoiceA.Index;E.ItemId=Item->GetPrimaryAssetId();E.HPBefore=Before;E.HPAfter=C.CurrentHP;E.RestoredHP=C.CurrentHP-Before;
 }
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
  HasActed[Index]=true;
		auto& Attacker = Index == 0 ? Next.SideA : Next.SideB;
		auto& Defender = Index == 0 ? Next.SideB : Next.SideA;
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
  auto& OwnEffects=EffectsFor(Next,Side);
  OwnEffects.bDestinyBond=false;
  if(OwnEffects.RechargeSlot!=INDEX_NONE)
  {
   OwnEffects.RechargeSlot=INDEX_NONE;OwnEffects.ForcedMoveData.Reset();OwnEffects.LastExecutedMove.Reset();
   Notice(EEvent::StatusPrevented,Side,Side,TEXT("Muss sich nach dem Angriff erholen."),Choices[Index].Index,Moves[Index]);
   BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
  }
  auto TickDisable=[&](){if(OwnEffects.DisableTurns>0 && --OwnEffects.DisableTurns==0){OwnEffects.DisabledSlot=INDEX_NONE;Notice(EEvent::StatusRecovered,Side,Side,TEXT("Die blockierte Attacke ist wieder verfügbar."),INDEX_NONE,nullptr);}};
  if(!EffectRules.bCrystal)TickDisable();
  bool LateDisabled=false;
  bool CannotAct=!EffectRules.bCrystal && OwnEffects.DisableTurns>0 && OwnEffects.DisabledSlot==Choices[Index].Index;
  if(!EffectRules.bCrystal && OwnEffects.bFlinched){Notice(EEvent::Flinched,Side,Side,TEXT("Zurückgeschreckt."),Choices[Index].Index,Moves[Index]);CannotAct=true;}
  else if(Attacker.Status==EPokeMonsterCreatureStatus::Sleep)
  {
   if(--Attacker.StatusTurns<=0){Attacker.Status=EPokeMonsterCreatureStatus::None;Attacker.StatusTurns=0;Notice(EEvent::StatusRecovered,Side,Side,TEXT("Aufgewacht."),Choices[Index].Index,Moves[Index]);}
   else CannotAct=true;
  }
  else if(Attacker.Status==EPokeMonsterCreatureStatus::Freeze)
  {
   if(!EffectRules.bCrystal && NextRandom.RandRange(0,99)<EffectRules.FreezeThawPercent){Attacker.Status=EPokeMonsterCreatureStatus::None;Notice(EEvent::StatusRecovered,Side,Side,TEXT("Aufgetaut."),Choices[Index].Index,Moves[Index]);}
   else CannotAct=true;
  }
  else if(!EffectRules.bCrystal && Attacker.Status==EPokeMonsterCreatureStatus::Paralysis && NextRandom.RandRange(0,99)<EffectRules.ParalysisSkipPercent)CannotAct=true;
  // Crystal checks sleep/freeze, flinch, the Disable timer, confusion, paralysis, then the selected disabled move.
  if(EffectRules.bCrystal && !CannotAct)
  {
   if(OwnEffects.bFlinched){Notice(EEvent::Flinched,Side,Side,TEXT("Zurückgeschreckt."),Choices[Index].Index,Moves[Index]);CannotAct=true;}
   else{TickDisable();LateDisabled=OwnEffects.DisableTurns>0 && OwnEffects.DisabledSlot==Choices[Index].Index;}
  }
  if(CannotAct){OwnEffects.ChargeSlot=OwnEffects.RampageSlot=INDEX_NONE;OwnEffects.RampageTurns=0;OwnEffects.ForcedMoveData.Reset();OwnEffects.LastExecutedMove.Reset();OwnEffects.bAirborne=false;Notice(EEvent::StatusPrevented,Side,Side,TEXT("Kann diese Runde nicht angreifen."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;}
  if(OwnEffects.ConfusionTurns>0)
  {
   --OwnEffects.ConfusionTurns;
   if(OwnEffects.ConfusionTurns>0 && NextRandom.RandRange(0,99)<50)
   {
    int32 ConfusionAttack=EffectRules.bCrystal?B::ApplyCrystalStage(Attacker.CalculatedStats.Attack,StageFor(Next,Side,EPokeMonsterBattleStat::Attack)):B::ApplyStage(Attacker.CalculatedStats.Attack,StageFor(Next,Side,EPokeMonsterBattleStat::Attack));
    int32 ConfusionDefense=EffectRules.bCrystal?B::ApplyCrystalStage(Attacker.CalculatedStats.Defense,StageFor(Next,Side,EPokeMonsterBattleStat::Defense)):B::ApplyStage(Attacker.CalculatedStats.Defense,StageFor(Next,Side,EPokeMonsterBattleStat::Defense));
    if(EffectRules.bCrystal){if(Attacker.Status==EPokeMonsterCreatureStatus::Burn)ConfusionAttack=FMath::Max(1,ConfusionAttack/2);while(ConfusionAttack>255 || ConfusionDefense>255){ConfusionAttack=FMath::Max(1,ConfusionAttack/4);ConfusionDefense=FMath::Max(1,ConfusionDefense/4);}}
    const int64 DamageSelf=FMath::FloorToDouble((2*Attacker.Level/5+2)*40.0*ConfusionAttack/ConfusionDefense/50)+2;
    const int Before=Attacker.CurrentHP;Attacker.CurrentHP=int32(FMath::Max<int64>(0,int64(Before)-DamageSelf));auto& E=Notice(EEvent::ConfusionDamage,Side,Side,TEXT("Verletzt sich selbst."),Choices[Index].Index,Moves[Index]);E.HPBefore=Before;E.HPAfter=Attacker.CurrentHP;E.Damage=Before-Attacker.CurrentHP;
    if(Attacker.CurrentHP==0){Knockout(Side);break;}OwnEffects.ChargeSlot=OwnEffects.RampageSlot=INDEX_NONE;OwnEffects.RampageTurns=0;OwnEffects.ForcedMoveData.Reset();OwnEffects.LastExecutedMove.Reset();OwnEffects.bAirborne=false;BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
   }
  }
  if(EffectRules.bCrystal && ((Attacker.Status==EPokeMonsterCreatureStatus::Paralysis && NextRandom.RandRange(0,99)<EffectRules.ParalysisSkipPercent) || LateDisabled))
  {
   OwnEffects.ChargeSlot=OwnEffects.RampageSlot=INDEX_NONE;OwnEffects.RampageTurns=0;OwnEffects.ForcedMoveData.Reset();OwnEffects.LastExecutedMove.Reset();OwnEffects.bAirborne=false;
   Notice(EEvent::StatusPrevented,Side,Side,TEXT("Kann diese Runde nicht angreifen."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
  }
  if(!Moves[Index]->HasEffect(EPokeMonsterEffectKind::Protect))OwnEffects.ProtectStreak=0;
  const bool Continuing=OwnEffects.ChargeSlot!=INDEX_NONE || OwnEffects.RampageSlot!=INDEX_NONE;
  const bool Releasing=OwnEffects.ChargeSlot!=INDEX_NONE;
  if(!Moves[Index]->HasEffect(EPokeMonsterEffectKind::Rage)){OwnEffects.bRage=false;OwnEffects.RageCounter=0;}
		const bool Fallback=Choices[Index].Index==INDEX_NONE;
		const int32 BeforePP = Fallback?0:Attacker.GetMoveSlots()[Choices[Index].Index].GetCurrentPP();
		if (!Fallback&&!Continuing&&!Attacker.ConsumeMovePP(Choices[Index].Index)) return Reject(EError::InvalidPP, Side);
		const int32 Roll = NextRandom.RandRange(0, EffectRules.bCrystal?255:99);
		auto& Executed = AddEvent(Result, Next, EEvent::MoveExecuted, Side, Choices[Index].Index, Moves[Index]);
		Executed.PPBefore = BeforePP;
		Executed.PPAfter = Fallback?0:BeforePP - (Continuing?0:1);
  OwnEffects.LastMoveSlot=Choices[Index].Index;
  Executed.HitRoll=Roll;
  // Copy the definition into this same resolution path, never the copied move's PP/slot.
  if(Moves[Index]->HasEffect(EPokeMonsterEffectKind::CopyLastMove))
  {
   auto* Copied=EffectsFor(Next,Index==0?ESide::B:ESide::A).LastExecutedMove.LoadSynchronous();
   if(!Copied || !Copied->IsConfigured() || Copied->HasEffect(EPokeMonsterEffectKind::CopyLastMove) || Copied->Effect.EffectId==TEXT("Struggle"))
   {
    OwnEffects.LastExecutedMove.Reset();Notice(EEvent::EffectFailed,Side,Side,TEXT("Keine geeignete Attacke zum Spiegeln."),Choices[Index].Index,Moves[Index]);
    BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
   }
   Moves[Index]=Copied;RetainedData.AddUnique(Copied);
   Notice(EEvent::StatChanged,Side,Side,TEXT("Spiegeltrick kopiert ")+Copied->GetPlayerFacingName().ToString()+TEXT("."),Choices[Index].Index,Copied);
  }
  OwnEffects.LastExecutedMove=Moves[Index];
		const ESide Opposite=Side==ESide::A?ESide::B:ESide::A;
  if(Moves[Index]->HasEffect(EPokeMonsterEffectKind::Charge) && !Releasing && !(Next.Weather==EPokeMonsterBattleWeather::Sun && Moves[Index]->InternalId==TEXT("SolarBeam")))
  {
   OwnEffects.ChargeSlot=Choices[Index].Index;OwnEffects.ForcedMoveData=Moves[Index];
   OwnEffects.LastExecutedMove.Reset();
   const auto ChargeEffects=Moves[Index]->GetEffectComponents();
   OwnEffects.bAirborne=ChargeEffects.ContainsByPredicate([](const auto& C){return C.Kind==EPokeMonsterEffectKind::Charge && C.Amount==1;});
   if(Moves[Index]->InternalId==TEXT("SkullBash")){auto& Def=StageFor(Next,Side,EPokeMonsterBattleStat::Defense);Def=FMath::Min(6,Def+1);}
   Notice(EEvent::StatusApplied,Side,Side,TEXT("Bereitet den Angriff vor."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
  }
  if(Releasing){OwnEffects.ChargeSlot=INDEX_NONE;OwnEffects.bAirborne=false;OwnEffects.ForcedMoveData.Reset();}
  const auto Components=Moves[Index]->GetEffectComponents();const auto* Rampage=Components.FindByPredicate([](const auto& E){return E.Kind==EPokeMonsterEffectKind::Rampage;});
  if(Rampage)
  {
   if(OwnEffects.RampageSlot==INDEX_NONE){OwnEffects.RampageSlot=Choices[Index].Index;OwnEffects.ForcedMoveData=Moves[Index];OwnEffects.RampageTurns=NextRandom.RandRange(Rampage->MinTurns,Rampage->MaxTurns);}
   if(--OwnEffects.RampageTurns<=0){OwnEffects.RampageSlot=INDEX_NONE;OwnEffects.ForcedMoveData.Reset();OwnEffects.ConfusionTurns=NextRandom.RandRange(2,EffectRules.bCrystal?5:3);Notice(EEvent::Confused,Side,Side,TEXT("Nach dem Angriff verwirrt."),Choices[Index].Index,Moves[Index]);}
  }
  int32 Evasion=EffectsFor(Next,Opposite).Evasion;if(EffectsFor(Next,Opposite).bIdentified && Evasion>0)Evasion=0;
  const int32 BaseAccuracy=Next.Weather==EPokeMonsterBattleWeather::Sun && Moves[Index]->InternalId==TEXT("Thunder")?50:Moves[Index]->Accuracy;
  const int32 Accuracy=EffectRules.bCrystal?B::CrystalAccuracy(BaseAccuracy,OwnEffects.Accuracy,EffectsFor(Next,Opposite).Evasion,EffectsFor(Next,Opposite).bIdentified):B::AccuracyAtStages(Moves[Index]->Accuracy,OwnEffects.Accuracy,Evasion);
  const bool RainThunder=Next.Weather==EPokeMonsterBattleWeather::Rain && Moves[Index]->InternalId==TEXT("Thunder");
  if (!Moves[Index]->bNeverMiss && !RainThunder && !(EffectRules.bCrystal && Accuracy==255) && Roll>=Accuracy)
		{
			AddEvent(Result, Next, EEvent::Missed, Side, Choices[Index].Index, Moves[Index]).HitRoll = Roll;
   BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
  }
  if(Moves[Index]->bRequiresSleepingTarget && Defender.Status!=EPokeMonsterCreatureStatus::Sleep)
  {
   Notice(EEvent::EffectFailed,Side,Opposite,TEXT("Das Ziel schläft nicht."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
  }
  if(Moves[Index]->Category==EPokeMonsterMoveCategory::Status)
  {
   if(Moves[Index]->InternalId==TEXT("ThunderWave") && B::GetTypeMultiplier(Moves[Index]->Type,Defender.Species.LoadSynchronous()->GetPrimaryType(),Defender.Species.LoadSynchronous()->GetSecondaryType())==0){Notice(EEvent::Immune,Side,Opposite,TEXT("Keine Wirkung."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;}
   if(EffectsFor(Next,Index==0?ESide::B:ESide::A).bProtected && !Moves[Index]->bBypassProtect && !Moves[Index]->GetEffectComponents().ContainsByPredicate([](const auto& C){return C.bSelf;}))
    Notice(EEvent::Protected,Side,Side==ESide::A?ESide::B:ESide::A,TEXT("Das Ziel ist geschützt."),Choices[Index].Index,Moves[Index]);
   else if(Moves[Index]->Effect.EffectId==TEXT("LeechSeed"))
   {
    bool& Seed=Index==0?Next.bSeededB:Next.bSeededA;const auto* D=Defender.Species.LoadSynchronous();const bool Can=!Seed&&D->GetPrimaryType()!=EPokeMonsterCreatureType::Grass&&D->GetSecondaryType()!=EPokeMonsterCreatureType::Grass;
    if(Can)Seed=true;AddEvent(Result,Next,Can?EEvent::Seeded:EEvent::EffectFailed,Side,Choices[Index].Index,Moves[Index]);
   }
   else ApplyComponents(Side,Moves[Index],Choices[Index].Index,0,false);
   if(Attacker.CurrentHP==0){Knockout(Side);break;}
   BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
  }
  if(EffectsFor(Next,Index==0?ESide::B:ESide::A).bProtected){Notice(EEvent::Protected,Side,Side==ESide::A?ESide::B:ESide::A,TEXT("Das Ziel ist geschützt."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;}

  static const int32 CritChances[]={17,32,64,85,128,128,128};
  auto DrawCritical=[&](){return EffectRules.bCrystal && !Moves[Index]->HasEffect(EPokeMonsterEffectKind::FixedDamage) && !Moves[Index]->HasEffect(EPokeMonsterEffectKind::LowHPPower) && NextRandom.RandRange(0,255)<CritChances[FMath::Clamp(OwnEffects.FocusStage+Moves[Index]->CriticalStageBonus,0,6)];};
  bool CrystalCritical=DrawCritical();
  auto CalculateHit=[&](){return EffectRules.bCrystal?B::CalculateCrystalDamage(Attacker,Defender,Moves[Index],StageFor(Next,Side,EPokeMonsterBattleStat::Attack),StageFor(Next,Opposite,EPokeMonsterBattleStat::Defense),OwnEffects.SpecialAttack,EffectsFor(Next,Opposite).SpecialDefense,CrystalCritical,Moves[Index]->HasEffect(EPokeMonsterEffectKind::LowHPPower)?255:NextRandom.RandRange(217,255),Next.Weather==EPokeMonsterBattleWeather::Rain,(Opposite==ESide::A?Next.ScreenTurnsA:Next.ScreenTurnsB)>0,EffectsFor(Next,Opposite).bIdentified,Next.Weather==EPokeMonsterBattleWeather::Sun,Next.Weather==EPokeMonsterBattleWeather::Sand,Moves[Index]->HasEffect(EPokeMonsterEffectKind::Rage)?1+OwnEffects.RageCounter:1):B::CalculateDamage(Attacker,Defender,Moves[Index],StageFor(Next,Side,EPokeMonsterBattleStat::Attack),StageFor(Next,Opposite,EPokeMonsterBattleStat::Defense),OwnEffects.SpecialAttack,EffectsFor(Next,Opposite).SpecialDefense);};
  Damage[Index]=CalculateHit();if(!Damage[Index].bValid)return Reject(EError::InvalidDamage,Side);
  if(CrystalCritical)Notice(EEvent::StatChanged,Side,Opposite,TEXT("Ein Volltreffer!"),Choices[Index].Index,Moves[Index]);
		const float Multiplier = Damage[Index].TypeMultiplier;
		if (Multiplier != 1.0f)
		{
			const EEvent Effect = Multiplier == 0.0f ? EEvent::Immune
				: Multiplier > 1.0f ? EEvent::SuperEffective : EEvent::NotVeryEffective;
			AddEvent(Result, Next, Effect, Side, Choices[Index].Index, Moves[Index]).TypeMultiplier = Multiplier;
		}
		if (Multiplier == 0.0f){BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;}
  const auto Specs=Moves[Index]->GetEffectComponents();const auto* Multi=Specs.FindByPredicate([](const auto& E){return E.Kind==EPokeMonsterEffectKind::MultiHit;});
  int32 HitLimit=1;
  if(Multi){int32 Total=0;for(int W:Multi->HitWeights)Total+=W;int32 Pick=NextRandom.RandRange(0,Total-1);for(int I=0;I<Multi->HitWeights.Num();++I){if(Pick<Multi->HitWeights[I]){HitLimit=Multi->MinHits+I;break;}Pick-=Multi->HitWeights[I];}}
  int32 AppliedDamage=0,Hits=0;
  for(int H=0;H<HitLimit && Defender.CurrentHP>0;++H)
  {
   const int32 BeforeHP=Defender.CurrentHP;
   if(H>0 && EffectRules.bCrystal){CrystalCritical=DrawCritical();Damage[Index]=CalculateHit();if(CrystalCritical)Notice(EEvent::StatChanged,Side,Opposite,TEXT("Ein Volltreffer!"),Choices[Index].Index,Moves[Index]);}
   int32 ThisDamage=Damage[Index].Damage;
   const bool Intercept=DeferredSwitch[1-Index] && Moves[Index]->HasEffect(EPokeMonsterEffectKind::SwitchPunish);
   const bool AirBonus=EffectsFor(Next,Opposite).bAirborne && Moves[Index]->HasEffect(EPokeMonsterEffectKind::AirborneBonus);
   if(Intercept || AirBonus)ThisDamage=int32(FMath::Min<int64>(MAX_int32,int64(ThisDamage)*2));
   if(!EffectRules.bCrystal && Moves[Index]->Category==EPokeMonsterMoveCategory::Special && (Opposite==ESide::A?Next.ScreenTurnsA:Next.ScreenTurnsB)>0 && !Moves[Index]->HasEffect(EPokeMonsterEffectKind::FixedDamage))ThisDamage=FMath::Max(1,ThisDamage/2);
   const int32 Removed=FMath::Min(BeforeHP,ThisDamage);Defender.CurrentHP-=Removed;AppliedDamage=int32(FMath::Min<int64>(MAX_int32,int64(AppliedDamage)+Removed));++Hits;
   auto& E=AddEvent(Result,Next,EEvent::Damage,Side,Choices[Index].Index,Moves[Index]);E.Damage=Removed;E.TypeMultiplier=Multiplier;E.HPBefore=BeforeHP;E.HPAfter=Defender.CurrentHP;
  }
  if(AppliedDamage>0 && Moves[Index]->HasEffect(EPokeMonsterEffectKind::Recharge))
  {OwnEffects.RechargeSlot=Choices[Index].Index;OwnEffects.ForcedMoveData=Moves[Index];}
  if(Multi)Notice(EEvent::HitCount,Side,Opposite,FString::Printf(TEXT("%d Treffer."),Hits),Choices[Index].Index,Moves[Index]);
  if(Defender.CurrentHP==0 && EffectsFor(Next,Opposite).bDestinyBond){const int Before=Attacker.CurrentHP;Attacker.CurrentHP=0;auto& E=Notice(EEvent::Damage,Opposite,Side,TEXT("Abgangsbund nimmt den Angreifer mit."),INDEX_NONE,nullptr);E.HPBefore=Before;E.HPAfter=0;E.Damage=Before;}
  if(Defender.CurrentHP>0 && EffectsFor(Next,Opposite).bRage && AppliedDamage>0){auto& Rage=EffectsFor(Next,Opposite).RageCounter;Rage=FMath::Min(255,Rage+Hits);Notice(EEvent::StatChanged,Opposite,Opposite,TEXT("Rasereis Stärke steigt."),INDEX_NONE,nullptr);}
  const bool ThawByFire=Defender.CurrentHP>0 && Defender.Status==EPokeMonsterCreatureStatus::Freeze && Moves[Index]->Type==EPokeMonsterCreatureType::Fire;
  ApplyComponents(Side,Moves[Index],Choices[Index].Index,AppliedDamage,true);
  if(ThawByFire){Defender.Status=EPokeMonsterCreatureStatus::None;EffectsFor(Next,Opposite).bJustFrozen=false;Notice(EEvent::StatusRecovered,Side,Opposite,TEXT("Durch Feuer aufgetaut."),INDEX_NONE,nullptr);}
  if(Fallback){const int Before=Attacker.CurrentHP;Attacker.CurrentHP=FMath::Max(0,Before-FMath::Max(1,AppliedDamage/4));auto& R=AddEvent(Result,Next,EEvent::Recoil,Side);R.Target=Side;R.TargetInstanceId=Attacker.InstanceId;R.HPBefore=Before;R.HPAfter=Attacker.CurrentHP;R.Damage=Before-Attacker.CurrentHP;}
  if(Defender.CurrentHP==0||Attacker.CurrentHP==0){Knockout(Defender.CurrentHP==0?(Index==0?ESide::B:ESide::A):Side);break;}

  BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;
	}
 for(int32 I=0;I<2;++I)if(DeferredSwitch[I] && Next.Phase!=EPhase::Finished)
 {
  PerformSwitch(I,Choices[I].Index);
  Next.Phase=Next.SideA.CurrentHP==0 || Next.SideB.CurrentHP==0?EPhase::AwaitingSwitch:EPhase::AwaitingChoices;
 }
 for(int I=0;I<2&&Next.Phase==EPhase::AwaitingChoices;++I)if(!Moves[I])BurnTick(I==0?ESide::A:ESide::B);
 // Leech Seed is volatile, grass-immune, and drains once at round end.
 for(int I:Order)
 {
  if(Next.Phase!=EPhase::AwaitingChoices)break;
  const ESide Victim=I==0?ESide::A:ESide::B, Recipient=I==0?ESide::B:ESide::A;
  if(EffectRules.bCrystal || !(I==0?Next.bSeededA:Next.bSeededB))continue;
  auto& V=ActiveFor(Next,Victim);auto& H=ActiveFor(Next,Recipient);
  if(V.CurrentHP<=0||H.CurrentHP<=0)continue;
  const int Before=V.CurrentHP,Removed=FMath::Min(Before,FMath::Max(1,V.GetMaxHP()/8));V.CurrentHP-=Removed;
  auto& D=AddEvent(Result,Next,EEvent::SeedDamage,Recipient);D.Target=Victim;D.TargetInstanceId=V.InstanceId;D.HPBefore=Before;D.HPAfter=V.CurrentHP;D.Damage=Removed;
  const int Healed=FMath::Min(Removed,H.GetMaxHP()-H.CurrentHP);
  if(Healed>0){auto& E=AddEvent(Result,Next,EEvent::SeedHeal,Recipient);E.Target=Recipient;E.TargetInstanceId=H.InstanceId;E.HPBefore=H.CurrentHP;H.CurrentHP+=Healed;E.HPAfter=H.CurrentHP;E.RestoredHP=Healed;}
  if(V.CurrentHP==0)Knockout(Victim);
 }
 for(ESide Side:{ESide::A,ESide::B})
 {
  if(Next.Phase!=EPhase::AwaitingChoices)break;
  auto& C=ActiveFor(Next,Side);
  if(!EffectRules.bCrystal && C.CurrentHP>0 && C.Status==EPokeMonsterCreatureStatus::Poison)
  {
   const int Before=C.CurrentHP;C.CurrentHP=FMath::Max(0,Before-FMath::Max(1,C.GetMaxHP()/EffectRules.PoisonDenominator));auto& E=Notice(EEvent::StatusDamage,Side,Side,TEXT("Vergiftung verursacht Schaden."),INDEX_NONE,nullptr);E.HPBefore=Before;E.HPAfter=C.CurrentHP;E.Damage=Before-C.CurrentHP;if(C.CurrentHP==0)Knockout(Side);
  }
 }
 if(Next.WeatherTurns>0 && --Next.WeatherTurns==0)Next.Weather=EPokeMonsterBattleWeather::Clear;
 for(ESide Side:{ESide::A,ESide::B})
 {
  if(Next.Phase!=EPhase::AwaitingChoices)break;
  auto& C=ActiveFor(Next,Side);auto& V=EffectsFor(Next,Side);
  auto Residual=[&](int32 Divisor,const TCHAR* Text){const int Before=C.CurrentHP;C.CurrentHP=FMath::Max(0,Before-FMath::Max(1,C.GetMaxHP()/Divisor));auto& E=Notice(EEvent::StatusDamage,Side,Side,Text,INDEX_NONE,nullptr);E.HPBefore=Before;E.HPAfter=C.CurrentHP;E.Damage=Before-C.CurrentHP;if(C.CurrentHP==0)Knockout(Side);};
  if(Next.Weather==EPokeMonsterBattleWeather::Sand){const auto* Species=C.Species.LoadSynchronous();auto Immune=[](EPokeMonsterCreatureType Type){return Type==EPokeMonsterCreatureType::Rock || Type==EPokeMonsterCreatureType::Ground || Type==EPokeMonsterCreatureType::Steel;};if(!Immune(Species->GetPrimaryType()) && !Immune(Species->GetSecondaryType()))Residual(8,TEXT("Sandsturm verursacht Schaden."));}
  if(Next.Phase!=EPhase::AwaitingChoices)break;
  if(V.TrapTurns>0){if(--V.TrapTurns>0)Residual(16,TEXT("Der Feuerwirbel verursacht Schaden."));else V.TrapSource.Invalidate();}
  if(EffectRules.bCrystal && C.CurrentHP>0 && C.Status==EPokeMonsterCreatureStatus::Freeze && !V.bJustFrozen && NextRandom.RandRange(0,99)<EffectRules.FreezeThawPercent){C.Status=EPokeMonsterCreatureStatus::None;Notice(EEvent::StatusRecovered,Side,Side,TEXT("Aufgetaut."),INDEX_NONE,nullptr);}
  V.bJustFrozen=false;
 }
 if(Next.SafeguardTurnsA>0)--Next.SafeguardTurnsA;
 if(Next.SafeguardTurnsB>0)--Next.SafeguardTurnsB;
 if(Next.ScreenTurnsA>0)--Next.ScreenTurnsA;
 if(Next.ScreenTurnsB>0)--Next.ScreenTurnsB;

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
 ResetVolatile(State,Side);
 if(Side==ESide::A){State.AttackStageA=0;State.ParticipantsA.Add(State.SideA.InstanceId);}else{State.AttackStageB=0;State.ParticipantsA.Reset();if(State.SideA.CurrentHP>0)State.ParticipantsA.Add(State.SideA.InstanceId);}
 if(Side==ESide::A){State.DefenseStageA=State.SpeedStageA=0;State.bSeededA=false;}
 else{State.DefenseStageB=State.SpeedStageB=0;State.bSeededB=false;}
	State.Phase = State.SideA.CurrentHP==0||State.SideB.CurrentHP==0?EPhase::AwaitingSwitch:EPhase::AwaitingChoices;
	FPokeMonsterBattleResult Result;
	Result.bSucceeded = true;
	Result.RoundNumber = State.RoundNumber;
	auto& Switched = AddEvent(Result, State, EEvent::SwitchedIn, Side);
	Switched.TeamIndex = TeamIndex;
	Switched.HPBefore = Switched.HPAfter = ActiveFor(State, Side).CurrentHP;
	return Result;
}

int32 UPokeMonsterBattleSession::EscapeThreshold(int32 A,int32 BSpeed,int32 Attempts)
{
 if(A<=0||BSpeed<=0||Attempts<1)return 0;if(A>=BSpeed)return 256;const int BDiv=(BSpeed/4)%256;if(BDiv==0)return 256;return int32(FMath::Clamp<int64>(int64(A)*32/BDiv+30LL*Attempts,0,256));
}

bool UPokeMonsterBattleSession::HasUsableMove(const FPokeMonsterCreatureInstance& Creature)
{
 for(const auto& Slot:Creature.GetMoveSlots())if(const auto* M=Slot.GetMove().LoadSynchronous())if(M->IsConfigured()&&Slot.GetCurrentPP()>0&&Slot.GetMaxPP()==M->MaxPP)return true;return false;
}


bool UPokeMonsterBattleSession::HasPendingLearning() const
{
	return State.TeamA.ContainsByPredicate([](const auto& C) { return !C.PendingMoves.IsEmpty(); });
}

bool UPokeMonsterBattleSession::ResolveMoveLearning(int32 TeamIndex, int32 SlotIndex)
{
 if(!State.TeamA.IsValidIndex(TeamIndex))return false;
 const auto OldMove=SlotIndex>=0 && State.TeamA[TeamIndex].GetMoveSlots().IsValidIndex(SlotIndex)?State.TeamA[TeamIndex].GetMoveSlots()[SlotIndex].GetMove():TSoftObjectPtr<UPokeMonsterMoveData>();
 if(!State.TeamA[TeamIndex].ResolveMoveLearning(SlotIndex))return false;
 if(TeamIndex==State.ActiveIndexA)
 {
  State.SideA=State.TeamA[TeamIndex];
  // Volatile restraints identify an attack, not a storage position subsequently reused by learning.
  if(SlotIndex>=0 && State.SideA.GetMoveSlots()[SlotIndex].GetMove()!=OldMove)
  {
   auto& V=State.EffectsA;
   if(V.LastMoveSlot==SlotIndex)V.LastMoveSlot=INDEX_NONE;
   if(V.DisabledSlot==SlotIndex){V.DisabledSlot=INDEX_NONE;V.DisableTurns=0;}
   if(V.ChargeSlot==SlotIndex)V.ChargeSlot=INDEX_NONE;
   if(V.RampageSlot==SlotIndex){V.RampageSlot=INDEX_NONE;V.RampageTurns=0;}
  }
 }
	return true;
}

bool UPokeMonsterBattleSession::ConfigureEffectRules(const FPokeMonsterBattleEffectRules& InRules)
{
 if(State.Phase!=EPhase::Uninitialized || !InRules.IsConfigured())return false;
 EffectRules=InRules;return true;
}

int32 UPokeMonsterBattleSession::ForcedMoveSlot(ESide Side)const
{
 const auto& V=Side==ESide::A?State.EffectsA:State.EffectsB;return V.RechargeSlot!=INDEX_NONE?V.RechargeSlot:V.ChargeSlot!=INDEX_NONE?V.ChargeSlot:V.RampageSlot;
}
bool UPokeMonsterBattleSession::CanSelectMove(ESide Side,int32 Slot)const
{
 const auto& C=Side==ESide::A?State.SideA:State.SideB;const auto& V=Side==ESide::A?State.EffectsA:State.EffectsB;
 const int Forced=ForcedMoveSlot(Side);if(Forced!=INDEX_NONE)return Slot==Forced;
 if(V.DisableTurns>0 && Slot==V.DisabledSlot)return false;
 UPokeMonsterMoveData* M=nullptr;return ValidateSelection(C,Slot,M)==EError::None;
}
bool UPokeMonsterBattleSession::HasSelectableMove(ESide Side)const
{
 for(int32 Slot=0;Slot<4;++Slot)if(CanSelectMove(Side,Slot))return true;return false;
}
bool UPokeMonsterBattleSession::CanLeave(ESide Side)const
{
 const auto& V=Side==ESide::A?State.EffectsA:State.EffectsB;
 return V.TrapTurns<=0 && !V.SwitchBlockSource.IsValid() && ForcedMoveSlot(Side)==INDEX_NONE;
}
