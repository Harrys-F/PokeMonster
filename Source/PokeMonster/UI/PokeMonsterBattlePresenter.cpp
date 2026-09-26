#include "PokeMonsterBattlePresenter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Items/PokeMonsterItemData.h"

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

bool UPokeMonsterBattlePresenter::StartTeamDemo()
{
	if (bBusy) return false;
	auto* Water = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Grass = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Normal = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	auto* Fire = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestFireSpecial.DA_TestFireSpecial"));
	auto* Status = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestStatus.DA_TestStatus"));
	if (!Water || !Grass || !Normal || !Fire || !Status)
	{
		Problem = TEXT("Testdaten fehlen. Team-Battle kann nicht gestartet werden.");
		Session = nullptr; Refresh(); return false;
	}
	TArray<FPokeMonsterCreatureInstance> Player, Opponent;
	for (const int32 Level : {20, 18})
	{
		auto A = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, Level);
		auto B = FPokeMonsterCreatureInstance::CreateFromSpecies(Grass, Level);
		UPokeMonsterMoveData* AMoves[] = {Normal, Fire, Status, Normal};
		UPokeMonsterMoveData* BMoves[] = {Normal, Status, Fire, Normal};
		for (int32 Slot = 0; Slot < 4; ++Slot)
			if (!A.AssignMove(Slot, AMoves[Slot]) || !B.AssignMove(Slot, BMoves[Slot]))
			{
				Problem = TEXT("Ungültige Team-Attackendaten."); Session = nullptr; Refresh(); return false;
			}
		Player.Add(MoveTemp(A)); Opponent.Add(MoveTemp(B));
	}
	return InitializeTeamBattle(Player, Opponent, 2026);
}

bool UPokeMonsterBattlePresenter::InitializeBattle(const FPokeMonsterCreatureInstance& Player,
	const FPokeMonsterCreatureInstance& Opponent, const int32 Seed)
{
	return InitializeTeamBattle({Player}, {Opponent}, Seed);
}

bool UPokeMonsterBattlePresenter::InitializeTeamBattle(const TArray<FPokeMonsterCreatureInstance>& Player,
	const TArray<FPokeMonsterCreatureInstance>& Opponent, const int32 Seed, bool bAllowCapture,
	UPokeMonsterInventorySubsystem* InInventory)
{
	if (bBusy) return false;
	Inventory = InInventory;
	CaptureItem = bAllowCapture ? LoadObject<UPokeMonsterItemData>(nullptr,
		TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem")) : nullptr;
	TestCaptureDevice = CaptureItem ? CaptureItem->GetCaptureDevice() : nullptr;
	if (bAllowCapture && (!TestCaptureDevice || !TestCaptureDevice->IsConfigured()
		|| !CaptureItem || !CaptureItem->IsConfigured()
		|| CaptureItem->GetCategory() != EPokeMonsterItemCategory::Capture))
	{
		Problem = TEXT("Test-Fangitem fehlt oder ist ungültig.");
		Refresh();
		return false;
	}
	Session = NewObject<UPokeMonsterBattleSession>(this);
	LastResult = Session->InitializeTeams(Player, Opponent, Seed, bAllowCapture);
	PendingSlot = INDEX_NONE;
	bPendingSwitch = false;
	bPendingCapture = false;
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

int32 UPokeMonsterBattlePresenter::NextOpponentSwitch() const
{
	if (!Session) return INDEX_NONE;
	const auto& State = Session->GetState();
	for (int32 Index = 0; Index < State.TeamB.Num(); ++Index)
		if (Index != State.ActiveIndexB && State.TeamB[Index].CurrentHP > 0) return Index;
	return INDEX_NONE;
}

bool UPokeMonsterBattlePresenter::TrySelectMove(const int32 Slot)
{
	if (bBusy || !Session || Session->GetState().Phase != EPokeMonsterBattlePhase::AwaitingChoices
		|| !CanUse(Session->GetState().SideA, Slot) || ChooseOpponentMove() == INDEX_NONE) return false;
	PendingSlot = Slot;
	bPendingSwitch = false;
	bPendingCapture = false;
	bBusy = true;
	bResolved = false;
	Refresh(); // Close the input gate before the controller schedules presentation.
	return true;
}

bool UPokeMonsterBattlePresenter::TrySelectCapture()
{
	if (bBusy || !Session || !TestCaptureDevice || !TestCaptureDevice->IsConfigured()
		|| !Inventory || !CaptureItem || !Inventory->HasItem(CaptureItem)
		|| !Session->GetState().bCaptureAllowed
		|| Session->GetState().Phase != EPokeMonsterBattlePhase::AwaitingChoices
		|| ChooseOpponentMove() == INDEX_NONE) return false;
	PendingSlot = 0;
	bPendingCapture = true;
	bPendingSwitch = false;
	bBusy = true;
	bResolved = false;
	Refresh();
	return true;
}

bool UPokeMonsterBattlePresenter::TrySelectSwitch(const int32 TeamIndex)
{
	if (bBusy || !Session) return false;
	const auto& State = Session->GetState();
	if (!State.TeamA.IsValidIndex(TeamIndex) || TeamIndex == State.ActiveIndexA
		|| State.TeamA[TeamIndex].CurrentHP <= 0 || State.Phase == EPokeMonsterBattlePhase::Finished)
		return false;
	const bool bForced = State.Phase == EPokeMonsterBattlePhase::AwaitingSwitch && State.SideA.CurrentHP == 0;
	if (!bForced && (State.Phase != EPokeMonsterBattlePhase::AwaitingChoices || ChooseOpponentMove() == INDEX_NONE))
		return false;
	PendingSlot = TeamIndex;
	bPendingSwitch = true;
	bPendingCapture = false;
	bBusy = true;
	bResolved = false;
	Refresh();
	return true;
}

bool UPokeMonsterBattlePresenter::ResolveSelection()
{
	if (!bBusy || bResolved || !Session || PendingSlot == INDEX_NONE) return false;
	bResolved = true; // Reject re-entry from callbacks and duplicate resolution.
	if (bPendingCapture)
	{
		if (!Inventory || !Inventory->RemoveItem(CaptureItem, 1))
		{
			Problem = TEXT("Kein Fangitem mehr im Inventar.");
			bBusy = false; bResolved = false; PendingSlot = INDEX_NONE; bPendingCapture = false;
			Refresh();
			return false;
		}
		FPokeMonsterBattleChoice A, B;
		A.Type = EPokeMonsterBattleChoiceType::Capture;
		A.CaptureDevice = TestCaptureDevice;
		B.Index = ChooseOpponentMove();
		LastResult = Session->ResolveTurn(A, B);
		if (!LastResult.bSucceeded) Inventory->AddItem(CaptureItem, 1);
	}
	else if (bPendingSwitch)
	{
		if (Session->GetState().Phase == EPokeMonsterBattlePhase::AwaitingSwitch)
			LastResult = Session->ForceSwitch(EPokeMonsterBattleSide::A, PendingSlot);
		else
		{
			FPokeMonsterBattleChoice A, B;
			A.Type = EPokeMonsterBattleChoiceType::Switch; A.Index = PendingSlot;
			B.Index = ChooseOpponentMove();
			LastResult = Session->ResolveTurn(A, B);
		}
	}
	else LastResult = Session->ResolveRound(PendingSlot, ChooseOpponentMove());
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
	if (Session && Session->GetState().Phase == EPokeMonsterBattlePhase::AwaitingSwitch
		&& Session->GetState().SideB.CurrentHP == 0)
	{
		const int32 Index = NextOpponentSwitch();
		if (Index != INDEX_NONE)
		{
			LastResult = Session->ForceSwitch(EPokeMonsterBattleSide::B, Index);
			if (LastResult.bSucceeded)
			{
				AppendEvents(LastResult);
				Refresh();
				OnRoundResolved.Broadcast(LastResult);
				return; // The automatic switch has its own presentation and keeps input locked.
			}
		}
	}
	bBusy = false;
	PendingSlot = INDEX_NONE;
	bPendingSwitch = false;
	bPendingCapture = false;
	Refresh();
}

void UPokeMonsterBattlePresenter::Refresh()
{
	View = FPokeMonsterBattleView();
	View.Moves.SetNum(4);
	View.bBusy = bBusy;
	View.bPresentationPending = bBusy && bResolved;
	View.Status = FText::FromString(Problem);
	if (Session)
	{
		const auto& State = Session->GetState();
		View.Player = CreatureView(State.SideA);
		View.Opponent = CreatureView(State.SideB);
		View.Round = State.RoundNumber;
		View.bFinished = State.Phase == EPokeMonsterBattlePhase::Finished;
		View.bCaptured = State.EndReason == EPokeMonsterBattleEndReason::Captured;
		View.bCaptureEnabled = State.bCaptureAllowed && TestCaptureDevice && CaptureItem
			&& Inventory && Inventory->HasItem(CaptureItem) && !bBusy
			&& !View.bFinished && State.Phase == EPokeMonsterBattlePhase::AwaitingChoices
			&& ChooseOpponentMove() != INDEX_NONE;
		View.CaptureDeviceName = CaptureItem ? CaptureItem->GetDisplayName() : FText::GetEmpty();
		View.bMustSwitch = State.Phase == EPokeMonsterBattlePhase::AwaitingSwitch && State.SideA.CurrentHP == 0;
		for (int32 SideIndex = 0; SideIndex < 2; ++SideIndex)
		{
			const auto& Team = SideIndex == 0 ? State.TeamA : State.TeamB;
			auto& Out = SideIndex == 0 ? View.PlayerTeam : View.OpponentTeam;
			const int32 Active = SideIndex == 0 ? State.ActiveIndexA : State.ActiveIndexB;
			for (int32 Index = 0; Index < Team.Num(); ++Index)
			{
				const auto Creature = CreatureView(Team[Index]);
				auto& Member = Out.AddDefaulted_GetRef();
				Member.Name = Creature.Name;
				Member.Level = Creature.Level;
				Member.CurrentHP = Creature.CurrentHP;
				Member.MaxHP = Creature.MaxHP;
				Member.bKO = Creature.bKO;
				Member.bActive = Index == Active;
				Member.bCanSwitch = SideIndex == 0 && Index != Active && !Creature.bKO
					&& !bBusy && !View.bFinished;
			}
		}
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
			MoveView.bEnabled = bUsable && bEnemyReady && !bBusy && !View.bFinished && !View.bMustSwitch;
		}
		if (View.bFinished) View.Status = FText::FromString(State.EndReason == EPokeMonsterBattleEndReason::Captured
			? TEXT("Gefangen! Der Kampf ist beendet.")
			: State.Winner == EPokeMonsterBattleSide::A ? TEXT("Gewonnen! Der Kampf ist beendet.") : TEXT("Besiegt. Der Kampf ist beendet."));
		else if (bBusy) View.Status = FText::FromString(TEXT("Runde wird aufgelöst …"));
		else if (View.bMustSwitch) View.Status = FText::FromString(TEXT("K.O. – wähle ein kampffähiges Teammitglied."));
		else if (!bEnemyReady || !bAnyPlayerMove) View.Status = FText::FromString(TEXT("Keine gültige Attacke mehr verfügbar. Test neu starten."));
		else if (Problem.IsEmpty()) View.Status = FText::FromString(State.bCaptureAllowed
			? TEXT("Wähle eine Aktion.") : TEXT("Wähle eine Attacke."));
	}
	if (LogLines.Num() > 80) LogLines.RemoveAt(0, LogLines.Num() - 80);
	View.Log = FText::FromString(FString::Join(LogLines, TEXT("\n")));
	OnChanged.Broadcast();
}

void UPokeMonsterBattlePresenter::AppendEvents(const FPokeMonsterBattleResult& Result)
{
	bool bNewRound = false;
	for (const auto& Event : Result.Events)
		bNewRound |= Event.Type == EPokeMonsterBattleEventType::MoveChosen
			|| Event.Type == EPokeMonsterBattleEventType::SwitchChosen
			|| Event.Type == EPokeMonsterBattleEventType::CaptureChosen;
	if (bNewRound) LogLines.Add(FString::Printf(TEXT("— Runde %d —"), Result.RoundNumber));
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
		case EPokeMonsterBattleEventType::SwitchChosen: break;
		case EPokeMonsterBattleEventType::CaptureChosen: LogLines.Add(TEXT("Fangversuch gestartet.")); break;
		case EPokeMonsterBattleEventType::CaptureSucceeded: LogLines.Add(Other + TEXT(" wurde gefangen!")); break;
		case EPokeMonsterBattleEventType::CaptureFailed: LogLines.Add(TEXT("Die wilde Kreatur entkommt!")); break;
		case EPokeMonsterBattleEventType::SwitchedIn:
			LogLines.Add(Who + TEXT(" wird eingewechselt."));
			break;
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
		case EPokeMonsterBattleEventType::BattleEnded: LogLines.Add(State.EndReason == EPokeMonsterBattleEndReason::Captured
			? TEXT("Gefangen! Kampf beendet.") : Event.Source == EPokeMonsterBattleSide::A
				? TEXT("Gewonnen! Kampf beendet.") : TEXT("Besiegt. Kampf beendet.")); break;
		}
	}
}
