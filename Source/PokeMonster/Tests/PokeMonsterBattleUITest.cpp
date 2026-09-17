#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterBattleUIBindingTest, "PokeMonster.Battle.UI.BindingAndInputLock",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterBattleUIBindingTest::RunTest(const FString& Parameters)
{
	TStrongObjectPtr<UPokeMonsterBattlePresenter> Presenter(NewObject<UPokeMonsterBattlePresenter>());
	if (!TestTrue(TEXT("Existing test assets start the demo"), Presenter->StartDemo())) return false;
	const auto Initial = Presenter->GetView();
	TestEqual(TEXT("Four move buttons receive data"), Initial.Moves.Num(), 4);
	TestEqual(TEXT("Player starts at level twenty"), Initial.Player.Level, 20);
	TestEqual(TEXT("Opponent starts at level twenty"), Initial.Opponent.Level, 20);
	TestEqual(TEXT("Initial player HP are full"), Initial.Player.CurrentHP, Initial.Player.MaxHP);
	TestEqual(TEXT("Initial opponent HP are full"), Initial.Opponent.CurrentHP, Initial.Opponent.MaxHP);
	TestFalse(TEXT("Player name exists"), Initial.Player.Name.IsEmpty());
	TestFalse(TEXT("Opponent name exists"), Initial.Opponent.Name.IsEmpty());
	for (const auto& Move : Initial.Moves)
	{
		TestTrue(TEXT("All four test slots are selectable"), Move.bEnabled);
		TestFalse(TEXT("Move name provided"), Move.Name.IsEmpty());
		TestFalse(TEXT("Move type provided"), Move.Type.IsEmpty());
		TestEqual(TEXT("Each slot starts at full PP"), Move.CurrentPP, Move.MaxPP);
	}
	TestFalse(TEXT("Negative slot rejected"), Presenter->TrySelectMove(-1));
	TestFalse(TEXT("Fifth slot rejected"), Presenter->TrySelectMove(4));
	TestTrue(TEXT("Valid click is accepted"), Presenter->TrySelectMove(0));
	TestTrue(TEXT("Input locks immediately"), Presenter->GetView().bBusy);
	for(const auto& Move:Presenter->GetView().Moves) TestFalse(TEXT("Every attack is disabled during resolution"),Move.bEnabled);
	TestFalse(TEXT("Double click rejected"), Presenter->TrySelectMove(1));
	TestFalse(TEXT("Restart cannot interrupt a pending round"), Presenter->StartDemo());
	Presenter->FinishPresentation();
	TestTrue(TEXT("Premature presentation completion cannot release input"), Presenter->GetView().bBusy);
	TestTrue(TEXT("Queued selection resolves"), Presenter->ResolveSelection());
	TestFalse(TEXT("Duplicate resolution rejected"), Presenter->ResolveSelection());
	TestEqual(TEXT("One accepted click produces exactly one round"), Presenter->GetView().Round, 1);
	TestEqual(TEXT("Selected slot loses one PP"), Presenter->GetView().Moves[0].CurrentPP, Initial.Moves[0].CurrentPP-1);
	TestEqual(TEXT("Duplicate move in fourth slot has independent PP"), Presenter->GetView().Moves[3].CurrentPP, Initial.Moves[3].CurrentPP);
	TestTrue(TEXT("View reports damage to target"), Presenter->GetView().Opponent.CurrentHP < Initial.Opponent.CurrentHP);
	TestTrue(TEXT("Opponent automatically performs a valid move"), Presenter->GetView().Player.CurrentHP < Initial.Player.CurrentHP);
	TestTrue(TEXT("Log renders damage events"), Presenter->GetView().Log.ToString().Contains(TEXT("verliert")));
	TestTrue(TEXT("Animation completion still owns the lock"), Presenter->GetView().bBusy);
	Presenter->FinishPresentation();
	TestTrue(TEXT("Input reopens after presentation"), Presenter->GetView().Moves[0].bEnabled);
	const int32 BeforeStatus = Presenter->GetView().Opponent.CurrentHP;
	Presenter->TrySelectMove(2); Presenter->ResolveSelection(); Presenter->FinishPresentation();
	TestEqual(TEXT("Status placeholder causes no damage"), Presenter->GetView().Opponent.CurrentHP, BeforeStatus);
	TestTrue(TEXT("Placeholder explained in log"), Presenter->GetView().Log.ToString().Contains(TEXT("Status-Platzhalter")));
	for(int32 Round=0;Round<20 && !Presenter->GetView().bFinished;++Round)
	{
		if(!Presenter->TrySelectMove(0)) { AddError(TEXT("An unfinished demo lost all usable moves unexpectedly")); break; }
		Presenter->ResolveSelection(); Presenter->FinishPresentation();
	}
	TestTrue(TEXT("Demo reaches battle end"),Presenter->GetView().bFinished);
	TestTrue(TEXT("One creature is visibly KO"),Presenter->GetView().Player.bKO || Presenter->GetView().Opponent.bKO);
	TestTrue(TEXT("KO appears in log"),Presenter->GetView().Log.ToString().Contains(TEXT("K.O.")));
	TestTrue(TEXT("Battle end appears in log"),Presenter->GetView().Log.ToString().Contains(TEXT("Kampf beendet")));
	for(const auto& Move:Presenter->GetView().Moves) TestFalse(TEXT("Finished battle disables all attacks"),Move.bEnabled);
	TestFalse(TEXT("Post-battle input rejected"),Presenter->TrySelectMove(0));
	TestTrue(TEXT("New test uses a new session"),Presenter->StartDemo());
	TestEqual(TEXT("Restart resets round"),Presenter->GetView().Round,0);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterBattleUIInvalidTest, "PokeMonster.Battle.UI.UnavailableMoves",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterBattleUIInvalidTest::RunTest(const FString& Parameters)
{
	TStrongObjectPtr<UPokeMonsterCreatureSpeciesData> Species(NewObject<UPokeMonsterCreatureSpeciesData>());
	TStrongObjectPtr<UPokeMonsterMoveData> Move(NewObject<UPokeMonsterMoveData>());
	Move->InternalId=TEXT("UITest"); Move->DisplayName=FText::FromString(TEXT("UI test")); Move->MaxPP=1;
	auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(Species.Get(),20);
	auto B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species.Get(),20);
	A.AssignMove(0,Move.Get()); B.AssignMove(0,Move.Get()); B.ConsumeMovePP(0);
	B.AssignMove(2,Move.Get()); // Simple opponent choice must skip the exhausted first slot.
	TStrongObjectPtr<UPokeMonsterBattlePresenter> Presenter(NewObject<UPokeMonsterBattlePresenter>());
	TestTrue(TEXT("Custom test battle initializes"),Presenter->InitializeBattle(A,B,1));
	TestFalse(TEXT("Empty player slot is disabled"),Presenter->GetView().Moves[1].bEnabled);
	TestTrue(TEXT("Opponent can find a later usable slot"),Presenter->TrySelectMove(0));
	TestTrue(TEXT("Fallback opponent selection resolves"),Presenter->ResolveSelection());
	Presenter->FinishPresentation();
	bool bChoseSlot2=false;
	for(const auto& Event:Presenter->GetLastResult().Events)
		bChoseSlot2 |= Event.Type==EPokeMonsterBattleEventType::MoveChosen && Event.Source==EPokeMonsterBattleSide::B && Event.SlotIndex==2;
	TestTrue(TEXT("Opponent chose its valid slot"),bChoseSlot2);
	TestFalse(TEXT("Exhausted player slot disabled"),Presenter->GetView().Moves[0].bEnabled);
	TestTrue(TEXT("No-move condition is explained"),Presenter->GetView().Status.ToString().Contains(TEXT("Keine gültige Attacke")));
	A.Species.Reset();
	TestFalse(TEXT("Missing species fails safely"),Presenter->InitializeBattle(A,B,1));
	TestFalse(TEXT("Initialization error is visible"),Presenter->GetView().Status.IsEmpty());
	for(const auto& Item:Presenter->GetView().Moves) TestFalse(TEXT("Failed initialization enables no attack"),Item.bEnabled);
	return true;
}
#endif
