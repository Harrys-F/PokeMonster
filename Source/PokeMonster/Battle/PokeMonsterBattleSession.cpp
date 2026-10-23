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
	const FPokeMonsterBattleChoice Choices[2] = {ChoiceA, ChoiceB};
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
    if(Choices[Index].Index==INDEX_NONE&&!HasUsableMove(Creature)){
     auto* Fallback=NewObject<UPokeMonsterMoveData>(this);Fallback->InternalId=TEXT("Struggle");Fallback->DisplayName=FText::FromString(TEXT("Verzweifler"));Fallback->BasePower=50;Fallback->MaxPP=1;Fallback->Effect.EffectId=TEXT("Struggle");RetainedData.Add(Fallback);Moves[Index]=Fallback;
    }else Error = ValidateSelection(Creature, Choices[Index].Index, Moves[Index]);
   }
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
  else if(Choices[Index].Type==EPokeMonsterBattleChoiceType::Flee){if(Side!=ESide::A||!State.bFleeAllowed)Error=EError::FleeNotAllowed;}
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
	// Switching takes precedence over attacks; the remaining attack targets the incoming creature.
	for (int32 Index = 0; Index < 2; ++Index)
	{
		if (Choices[Index].Type != EPokeMonsterBattleChoiceType::Switch) continue;
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
		ActiveIndexFor(Next, Side) = Choices[Index].Index;
		ActiveFor(Next, Side) = TeamFor(Next, Side)[Choices[Index].Index];
  ResetVolatile(Next,Side);
  if(Side==ESide::A){Next.AttackStageA=0;Next.ParticipantsA.Add(Next.SideA.InstanceId);}else {Next.AttackStageB=0;Next.ParticipantsA.Reset();Next.ParticipantsA.Add(Next.SideA.InstanceId);}
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
	// Battle-only stages reset on switching; persistent individual data stays unchanged.
 for(int I=0;I<2;++I)if(Choices[I].Type==EPokeMonsterBattleChoiceType::Switch)
 {
  if(I==0){Next.DefenseStageA=Next.SpeedStageA=0;Next.bSeededA=false;}
  else{Next.DefenseStageB=Next.SpeedStageB=0;Next.bSeededB=false;}
 }
 const bool bBothMove = Moves[0] != nullptr && Moves[1] != nullptr;
	auto TurnSpeed=[&](ESide Side){const auto& C=ActiveFor(Next,Side);const int32 Speed=B::ApplyStage(C.CalculatedStats.Speed,StageFor(Next,Side,EPokeMonsterBattleStat::Speed));return C.Status==EPokeMonsterCreatureStatus::Paralysis?FMath::Max(1,Speed/EffectRules.ParalysisSpeedDivisor):Speed;};
 const bool bAFirst = !bBothMove || (Moves[0]->Priority != Moves[1]->Priority
		? Moves[0]->Priority > Moves[1]->Priority
		: TurnSpeed(ESide::A) >= TurnSpeed(ESide::B));
	const int32 Order[2] = {bAFirst ? 0 : 1, bAFirst ? 1 : 0};
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
  SyncActive(Next);if(Next.SideB.CurrentHP==0)AwardExperience();
  if(!HasLiving(Next.TeamA)||!HasLiving(Next.TeamB)){Next.Phase=EPhase::Finished;Next.Winner=!HasLiving(Next.TeamA)?ESide::B:ESide::A;Next.EndReason=EPokeMonsterBattleEndReason::Knockout;AddEvent(Result,Next,EEvent::BattleEnded,Next.Winner);}else Next.Phase=EPhase::AwaitingSwitch;
 };
 auto BurnTick=[&](ESide Side){
  auto& C=ActiveFor(Next,Side);if(C.CurrentHP<=0||C.Status!=EPokeMonsterCreatureStatus::Burn||Next.Phase!=EPhase::AwaitingChoices)return;
  const int Before=C.CurrentHP;C.CurrentHP=FMath::Max(0,C.CurrentHP-FMath::Max(1,C.GetMaxHP()/8));auto& E=AddEvent(Result,Next,EEvent::BurnDamage,Side);E.Target=Side;E.TargetInstanceId=C.InstanceId;E.HPBefore=Before;E.HPAfter=C.CurrentHP;E.Damage=Before-C.CurrentHP;if(C.CurrentHP==0)Knockout(Side);
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
   if(C.Kind==EPokeMonsterEffectKind::FixedDamage || C.Kind==EPokeMonsterEffectKind::MultiHit)continue;
   // Status moves resolve once before damage, damaging moves once after their hit sequence.
   if(bSecondary != (Move->Category!=EPokeMonsterMoveCategory::Status))continue;
   const ESide Target=C.bSelf?Side:Other;auto& T=ActiveFor(Next,Target);auto& V=EffectsFor(Next,Target);
   if(T.CurrentHP<=0)continue;
   auto Failed=[&](){Notice(EEvent::EffectFailed,Side,Target,TEXT("Die Wirkung schlägt fehl."),Slot,Move);};
   if(C.Kind==EPokeMonsterEffectKind::Drain || C.Kind==EPokeMonsterEffectKind::Recoil)
   {
    if(!bSecondary || ActualDamage<=0)continue;
   }
   if(!C.bSelf && EffectsFor(Next,Other).bProtected){Notice(EEvent::Protected,Side,Target,TEXT("Das Ziel ist geschützt."),Slot,Move);continue;}
   // Eligibility precedes the legacy burn RNG draw, as in the original battle session.
   if(C.Kind==EPokeMonsterEffectKind::PrimaryStatus)
   {
    const auto* S=T.Species.LoadSynchronous();
    if(T.Status!=EPokeMonsterCreatureStatus::None || !S || C.ImmuneTypes.Contains(S->GetPrimaryType()) || C.ImmuneTypes.Contains(S->GetSecondaryType())){if(!C.bSecondary)Failed();continue;}
   }
   const bool LegacyDraw=Move->Effects.IsEmpty() && C.bSecondary;
   if(C.ChancePercent==0 && !LegacyDraw)continue;
   if((LegacyDraw || C.ChancePercent<100) && NextRandom.RandRange(0,99)>=C.ChancePercent)continue;
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
    Notice(C.Status==EPokeMonsterCreatureStatus::Burn?EEvent::Burned:EEvent::StatusApplied,Side,Target,TEXT("Statusproblem: ")+B::StatusLabel(C.Status).ToString(),Slot,Move);
   }
   else if(C.Kind==EPokeMonsterEffectKind::Heal || C.Kind==EPokeMonsterEffectKind::Drain)
   {
    const int32 Base=C.Kind==EPokeMonsterEffectKind::Drain?ActualDamage:T.GetMaxHP();
    const int32 Amount=int32(FMath::Min<int64>(MAX_int32,FMath::Max<int64>(1,int64(Base)*C.Numerator/C.Denominator)));
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
    if(NextRandom.RandRange(0,99)>=Chance){V.ProtectStreak=0;Failed();continue;}
    V.bProtected=true;++V.ProtectStreak;Notice(EEvent::Protected,Side,Target,TEXT("Schutz aufgebaut."),Slot,Move);
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
		auto& Attacker = Index == 0 ? Next.SideA : Next.SideB;
		auto& Defender = Index == 0 ? Next.SideB : Next.SideA;
		const ESide Side = Index == 0 ? ESide::A : ESide::B;
  auto& OwnEffects=EffectsFor(Next,Side);
  bool CannotAct=false;
  if(OwnEffects.bFlinched){Notice(EEvent::Flinched,Side,Side,TEXT("Zurückgeschreckt."),Choices[Index].Index,Moves[Index]);CannotAct=true;}
  else if(Attacker.Status==EPokeMonsterCreatureStatus::Sleep)
  {
   if(--Attacker.StatusTurns<=0){Attacker.Status=EPokeMonsterCreatureStatus::None;Attacker.StatusTurns=0;Notice(EEvent::StatusRecovered,Side,Side,TEXT("Aufgewacht."),Choices[Index].Index,Moves[Index]);}
   else CannotAct=true;
  }
  else if(Attacker.Status==EPokeMonsterCreatureStatus::Freeze)
  {
   if(NextRandom.RandRange(0,99)<EffectRules.FreezeThawPercent){Attacker.Status=EPokeMonsterCreatureStatus::None;Notice(EEvent::StatusRecovered,Side,Side,TEXT("Aufgetaut."),Choices[Index].Index,Moves[Index]);}
   else CannotAct=true;
  }
  else if(Attacker.Status==EPokeMonsterCreatureStatus::Paralysis && NextRandom.RandRange(0,99)<EffectRules.ParalysisSkipPercent)CannotAct=true;
  if(CannotAct){Notice(EEvent::StatusPrevented,Side,Side,TEXT("Kann diese Runde nicht angreifen."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;}
  if(OwnEffects.ConfusionTurns>0)
  {
   --OwnEffects.ConfusionTurns;
   if(OwnEffects.ConfusionTurns>0 && NextRandom.RandRange(0,99)<50)
   {
    const int64 DamageSelf=FMath::FloorToDouble((2*Attacker.Level/5+2)*40.0*B::ApplyStage(Attacker.CalculatedStats.Attack,StageFor(Next,Side,EPokeMonsterBattleStat::Attack))/B::ApplyStage(Attacker.CalculatedStats.Defense,StageFor(Next,Side,EPokeMonsterBattleStat::Defense))/50)+2;
    const int Before=Attacker.CurrentHP;Attacker.CurrentHP=int32(FMath::Max<int64>(0,int64(Before)-DamageSelf));auto& E=Notice(EEvent::ConfusionDamage,Side,Side,TEXT("Verletzt sich selbst."),Choices[Index].Index,Moves[Index]);E.HPBefore=Before;E.HPAfter=Attacker.CurrentHP;E.Damage=Before-Attacker.CurrentHP;
    if(Attacker.CurrentHP==0){Knockout(Side);break;}BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
   }
  }
  if(!Moves[Index]->HasEffect(EPokeMonsterEffectKind::Protect))OwnEffects.ProtectStreak=0;
  Damage[Index]=B::CalculateDamage(Attacker,Defender,Moves[Index],Index==0?Next.AttackStageA:Next.AttackStageB,Index==0?Next.DefenseStageB:Next.DefenseStageA,EffectsFor(Next,Side).SpecialAttack,EffectsFor(Next,Side==ESide::A?ESide::B:ESide::A).SpecialDefense);if(!Damage[Index].bValid)return Reject(EError::InvalidDamage,Side);
		const bool Fallback=Choices[Index].Index==INDEX_NONE;
		const int32 BeforePP = Fallback?0:Attacker.GetMoveSlots()[Choices[Index].Index].GetCurrentPP();
		if (!Fallback&&!Attacker.ConsumeMovePP(Choices[Index].Index)) return Reject(EError::InvalidPP, Side);
		const int32 Roll = NextRandom.RandRange(0, 99);
		auto& Executed = AddEvent(Result, Next, EEvent::MoveExecuted, Side, Choices[Index].Index, Moves[Index]);
		Executed.PPBefore = BeforePP;
		Executed.PPAfter = Fallback?0:BeforePP - 1;
		Executed.HitRoll = Roll;
		const ESide Opposite=Side==ESide::A?ESide::B:ESide::A;
  const int32 Accuracy=B::AccuracyAtStages(Moves[Index]->Accuracy,OwnEffects.Accuracy,EffectsFor(Next,Opposite).Evasion);
  if (!Moves[Index]->bNeverMiss && Roll>=Accuracy)
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
   if(EffectsFor(Next,Index==0?ESide::B:ESide::A).bProtected && !Moves[Index]->GetEffectComponents().ContainsByPredicate([](const auto& C){return C.bSelf;}))
    Notice(EEvent::Protected,Side,Side==ESide::A?ESide::B:ESide::A,TEXT("Das Ziel ist geschützt."),Choices[Index].Index,Moves[Index]);
   else if(Moves[Index]->Effect.EffectId==TEXT("LeechSeed"))
   {
    bool& Seed=Index==0?Next.bSeededB:Next.bSeededA;const auto* D=Defender.Species.LoadSynchronous();const bool Can=!Seed&&D->GetPrimaryType()!=EPokeMonsterCreatureType::Grass&&D->GetSecondaryType()!=EPokeMonsterCreatureType::Grass;
    if(Can)Seed=true;AddEvent(Result,Next,Can?EEvent::Seeded:EEvent::EffectFailed,Side,Choices[Index].Index,Moves[Index]);
   }
   else ApplyComponents(Side,Moves[Index],Choices[Index].Index,0,false);
   BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;
  }
  if(EffectsFor(Next,Index==0?ESide::B:ESide::A).bProtected){Notice(EEvent::Protected,Side,Side==ESide::A?ESide::B:ESide::A,TEXT("Das Ziel ist geschützt."),Choices[Index].Index,Moves[Index]);BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;continue;}

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
   int32 ThisDamage=Damage[Index].Damage;
   if(Moves[Index]->Category==EPokeMonsterMoveCategory::Special && (Opposite==ESide::A?Next.ScreenTurnsA:Next.ScreenTurnsB)>0 && !Moves[Index]->HasEffect(EPokeMonsterEffectKind::FixedDamage))ThisDamage=FMath::Max(1,ThisDamage/2);
   const int32 Removed=FMath::Min(BeforeHP,ThisDamage);Defender.CurrentHP-=Removed;AppliedDamage=int32(FMath::Min<int64>(MAX_int32,int64(AppliedDamage)+Removed));++Hits;
   auto& E=AddEvent(Result,Next,EEvent::Damage,Side,Choices[Index].Index,Moves[Index]);E.Damage=Removed;E.TypeMultiplier=Multiplier;E.HPBefore=BeforeHP;E.HPAfter=Defender.CurrentHP;
  }
  if(Multi)Notice(EEvent::HitCount,Side,Opposite,FString::Printf(TEXT("%d Treffer."),Hits),Choices[Index].Index,Moves[Index]);
  ApplyComponents(Side,Moves[Index],Choices[Index].Index,AppliedDamage,true);
  if(Fallback){const int Before=Attacker.CurrentHP;Attacker.CurrentHP=FMath::Max(0,Before-FMath::Max(1,AppliedDamage/4));auto& R=AddEvent(Result,Next,EEvent::Recoil,Side);R.Target=Side;R.TargetInstanceId=Attacker.InstanceId;R.HPBefore=Before;R.HPAfter=Attacker.CurrentHP;R.Damage=Before-Attacker.CurrentHP;}
  if(Defender.CurrentHP==0||Attacker.CurrentHP==0){Knockout(Defender.CurrentHP==0?(Index==0?ESide::B:ESide::A):Side);break;}

  BurnTick(Side);if(Next.Phase!=EPhase::AwaitingChoices)break;
	}
 for(int I=0;I<2&&Next.Phase==EPhase::AwaitingChoices;++I)if(!Moves[I])BurnTick(I==0?ESide::A:ESide::B);
 // Leech Seed is volatile, grass-immune, and drains once at round end.
 for(int I:Order)
 {
  if(Next.Phase!=EPhase::AwaitingChoices)break;
  const ESide Victim=I==0?ESide::A:ESide::B, Recipient=I==0?ESide::B:ESide::A;
  if(!(I==0?Next.bSeededA:Next.bSeededB))continue;
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
  if(C.CurrentHP>0 && C.Status==EPokeMonsterCreatureStatus::Poison)
  {
   const int Before=C.CurrentHP;C.CurrentHP=FMath::Max(0,Before-FMath::Max(1,C.GetMaxHP()/EffectRules.PoisonDenominator));auto& E=Notice(EEvent::StatusDamage,Side,Side,TEXT("Vergiftung verursacht Schaden."),INDEX_NONE,nullptr);E.HPBefore=Before;E.HPAfter=C.CurrentHP;E.Damage=Before-C.CurrentHP;if(C.CurrentHP==0)Knockout(Side);
  }
 }
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
	if (!State.TeamA.IsValidIndex(TeamIndex) || !State.TeamA[TeamIndex].ResolveMoveLearning(SlotIndex)) return false;
	if (TeamIndex == State.ActiveIndexA) State.SideA = State.TeamA[TeamIndex];
	return true;
}

bool UPokeMonsterBattleSession::ConfigureEffectRules(const FPokeMonsterBattleEffectRules& InRules)
{
 if(State.Phase!=EPhase::Uninitialized || !InRules.IsConfigured())return false;
 EffectRules=InRules;return true;
}
