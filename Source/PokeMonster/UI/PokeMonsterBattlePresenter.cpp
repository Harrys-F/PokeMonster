#include "PokeMonsterBattlePresenter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"

namespace
{
	FPokeMonsterBattleCreatureView CreatureView(const FPokeMonsterCreatureInstance& Creature)
	{
		FPokeMonsterBattleCreatureView View;
		const auto* Species = Creature.Species.LoadSynchronous();
		View.Name = Species ? Species->GetDisplayName() : FText::FromString(TEXT("Fehlende Spezies"));
		View.Level = Creature.Level;
		View.CurrentHP = Creature.CurrentHP;
		View.MaxHP = Creature.GetMaxHP();
		View.bKO = Creature.CurrentHP <= 0;
		return View;
	}
	FText TypeName(EPokeMonsterCreatureType Type)
	{
		static const TCHAR* Names[] = {TEXT("—"), TEXT("Normal"), TEXT("Feuer"), TEXT("Wasser"), TEXT("Elektro"),
			TEXT("Pflanze"), TEXT("Eis"), TEXT("Kampf"), TEXT("Gift"), TEXT("Boden"), TEXT("Flug"), TEXT("Psycho"),
			TEXT("Käfer"), TEXT("Gestein"), TEXT("Geist"), TEXT("Drache"), TEXT("Unlicht"), TEXT("Stahl")};
		return FText::FromString(uint8(Type) < UE_ARRAY_COUNT(Names) ? Names[uint8(Type)] : TEXT("?"));
	}
}

bool UPokeMonsterBattlePresenter::StartDemo()
{
	if (bBusy) return false;
	auto* Water = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Grass = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Normal = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	auto* Fire = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestFireSpecial.DA_TestFireSpecial"));
	auto* Status = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestStatus.DA_TestStatus"));
	if (!Water || !Grass || !Normal || !Fire || !Status)
	{
		Problem = TEXT("Testdaten fehlen. Battle kann nicht gestartet werden.");
		Session = nullptr;
		Refresh();
		return false;
	}
	auto Player = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, 20);
	auto Opponent = FPokeMonsterCreatureInstance::CreateFromSpecies(Grass, 20);
	UPokeMonsterMoveData* PlayerMoves[] = {Normal, Fire, Status, Normal};
	UPokeMonsterMoveData* OpponentMoves[] = {Normal, Status, Fire, Normal};
	for (int32 Slot = 0; Slot < 4; ++Slot)
	{
		if (!Player.AssignMove(Slot, PlayerMoves[Slot]) || !Opponent.AssignMove(Slot, OpponentMoves[Slot]))
		{
			Problem = TEXT("Ungültige Attackendaten."); Session = nullptr; Refresh(); return false;
		}
	}
	return InitializeBattle(Player, Opponent, 2026);
}

bool UPokeMonsterBattlePresenter::InitializeBattle(const FPokeMonsterCreatureInstance& Player,
	const FPokeMonsterCreatureInstance& Opponent, const int32 Seed)
{
	if (bBusy) return false;
	Session = NewObject<UPokeMonsterBattleSession>(this);
	LastResult = Session->Initialize(Player, Opponent, Seed);
	PendingSlot = INDEX_NONE;
	bResolved = false;
	LogLines.Reset();
	Problem.Reset();
	if (!LastResult.bSucceeded)
	{
		Problem = FString::Printf(TEXT("Battle-Start fehlgeschlagen: %s"), *StaticEnum<EPokeMonsterBattleError>()->GetNameStringByValue(int64(LastResult.Error)));
		Session = nullptr;
	}
	else LogLines.Add(TEXT("Der Kampf beginnt. Wähle eine Attacke."));
	Refresh();
	return LastResult.bSucceeded;
}

bool UPokeMonsterBattlePresenter::CanUse(const FPokeMonsterCreatureInstance& Creature, const int32 Slot)
{
	if (Creature.CurrentHP <= 0 || Slot < 0 || Slot >= 4 || !Creature.GetMoveSlots().IsValidIndex(Slot)) return false;
	const auto& MoveSlot = Creature.GetMoveSlots()[Slot];
	const auto* Move = MoveSlot.GetMove().LoadSynchronous();
	return Move && Move->IsConfigured() && MoveSlot.GetCurrentPP() > 0
		&& MoveSlot.GetCurrentPP() <= MoveSlot.GetMaxPP() && MoveSlot.GetMaxPP() == Move->MaxPP;
}

int32 UPokeMonsterBattlePresenter::ChooseOpponentMove() const
{
	if (Session) for (int32 Slot = 0; Slot < 4; ++Slot) if (CanUse(Session->GetState().SideB, Slot)) return Slot;
	return INDEX_NONE;
}

bool UPokeMonsterBattlePresenter::TrySelectMove(const int32 Slot)
{
	if (bBusy || !Session || Session->GetState().Phase != EPokeMonsterBattlePhase::AwaitingChoices
		|| !CanUse(Session->GetState().SideA, Slot) || ChooseOpponentMove() == INDEX_NONE) return false;
	PendingSlot = Slot;
	bBusy = true;
	bResolved = false;
	Refresh(); // Close the input gate before the controller schedules presentation.
	return true;
}

bool UPokeMonsterBattlePresenter::ResolveSelection()
{
	if (!bBusy || bResolved || !Session || PendingSlot == INDEX_NONE) return false;
	bResolved = true; // Reject re-entry from callbacks and duplicate resolution.
	LastResult = Session->ResolveRound(PendingSlot, ChooseOpponentMove());
	if (LastResult.bSucceeded) AppendEvents(LastResult);
	else
	{
		Problem = FString::Printf(TEXT("Runde abgewiesen: %s"), *StaticEnum<EPokeMonsterBattleError>()->GetNameStringByValue(int64(LastResult.Error)));
		LogLines.Add(Problem);
	}
	Refresh();
	OnRoundResolved.Broadcast(LastResult);
	return LastResult.bSucceeded;
}

void UPokeMonsterBattlePresenter::FinishPresentation()
{
	if (!bBusy || !bResolved) return;
	bBusy = false;
	PendingSlot = INDEX_NONE;
	Refresh();
}

void UPokeMonsterBattlePresenter::Refresh()
{
	View = FPokeMonsterBattleView();
	View.Moves.SetNum(4);
	View.bBusy = bBusy;
	View.Status = FText::FromString(Problem);
	if (Session)
	{
		const auto& State = Session->GetState();
		View.Player = CreatureView(State.SideA);
		View.Opponent = CreatureView(State.SideB);
		View.Round = State.RoundNumber;
		View.bFinished = State.Phase == EPokeMonsterBattlePhase::Finished;
		const bool bEnemyReady = ChooseOpponentMove() != INDEX_NONE;
		bool bAnyPlayerMove = false;
		for (int32 Slot = 0; Slot < 4; ++Slot)
		{
			const auto& Data = State.SideA.GetMoveSlots()[Slot];
			auto& MoveView = View.Moves[Slot];
			const auto* Move = Data.GetMove().LoadSynchronous();
			MoveView.Name = Move ? Move->DisplayName : FText::FromString(TEXT("Leerer Slot"));
			MoveView.Type = Move ? TypeName(Move->Type) : FText::GetEmpty();
			MoveView.CurrentPP = Data.GetCurrentPP(); MoveView.MaxPP = Data.GetMaxPP();
			const bool bUsable = CanUse(State.SideA, Slot);
			bAnyPlayerMove |= bUsable;
			MoveView.bEnabled = bUsable && bEnemyReady && !bBusy && !View.bFinished;
		}
		if (View.bFinished) View.Status = FText::FromString(State.Winner == EPokeMonsterBattleSide::A ? TEXT("Gewonnen! Der Kampf ist beendet.") : TEXT("Besiegt. Der Kampf ist beendet."));
		else if (bBusy) View.Status = FText::FromString(TEXT("Runde wird aufgelöst …"));
		else if (!bEnemyReady || !bAnyPlayerMove) View.Status = FText::FromString(TEXT("Keine gültige Attacke mehr verfügbar. Test neu starten."));
		else if (Problem.IsEmpty()) View.Status = FText::FromString(TEXT("Wähle eine Attacke."));
	}
	if (LogLines.Num() > 80) LogLines.RemoveAt(0, LogLines.Num() - 80);
	View.Log = FText::FromString(FString::Join(LogLines, TEXT("\n")));
	OnChanged.Broadcast();
}

void UPokeMonsterBattlePresenter::AppendEvents(const FPokeMonsterBattleResult& Result)
{
	LogLines.Add(FString::Printf(TEXT("— Runde %d —"), Result.RoundNumber));
	const auto& State = Session->GetState();
	for (int32 EventIndex = 0; EventIndex < Result.Events.Num(); ++EventIndex)
	{
		const auto& Event = Result.Events[EventIndex];
		const auto& Source = Event.Source == EPokeMonsterBattleSide::A ? State.SideA : State.SideB;
		const auto& Target = Event.Target == EPokeMonsterBattleSide::A ? State.SideA : State.SideB;
		const FString Who = CreatureView(Source).Name.ToString();
		const FString Other = CreatureView(Target).Name.ToString();
		FString MoveName = Event.MoveId.PrimaryAssetName.ToString();
		if (Source.GetMoveSlots().IsValidIndex(Event.SlotIndex))
			if (const auto* Move = Source.GetMoveSlots()[Event.SlotIndex].GetMove().Get()) MoveName = Move->DisplayName.ToString();
		switch (Event.Type)
		{
		case EPokeMonsterBattleEventType::MoveChosen: break; // Execution describes the choice in the compact log.
		case EPokeMonsterBattleEventType::MoveExecuted:
			LogLines.Add(Who + TEXT(" setzt ") + MoveName + TEXT(" ein."));
			// A missed status move has no effect; the following Missed event explains it instead.
			if (Event.Category == EPokeMonsterMoveCategory::Status
				&& !(Result.Events.IsValidIndex(EventIndex + 1)
					&& Result.Events[EventIndex + 1].Type == EPokeMonsterBattleEventType::Missed))
				LogLines.Add(TEXT("Status-Platzhalter: noch ohne Effekt."));
			break;
		case EPokeMonsterBattleEventType::Missed: LogLines.Add(TEXT("Die Attacke verfehlt ihr Ziel.")); break;
		case EPokeMonsterBattleEventType::Damage: LogLines.Add(FString::Printf(TEXT("%s verliert %d HP."), *Other, Event.Damage)); break;
		case EPokeMonsterBattleEventType::SuperEffective: LogLines.Add(TEXT("Sehr effektiv!")); break;
		case EPokeMonsterBattleEventType::NotVeryEffective: LogLines.Add(TEXT("Nicht sehr effektiv.")); break;
		case EPokeMonsterBattleEventType::Immune: LogLines.Add(Other + TEXT(" ist immun.")); break;
		case EPokeMonsterBattleEventType::KnockedOut: LogLines.Add(Other + TEXT(" ist K.O.!")); break;
		case EPokeMonsterBattleEventType::BattleEnded: LogLines.Add(Event.Source == EPokeMonsterBattleSide::A ? TEXT("Gewonnen! Kampf beendet.") : TEXT("Besiegt. Kampf beendet.")); break;
		}
	}
}
