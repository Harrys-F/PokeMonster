#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterTeamBattleTest, "PokeMonster.Battle.Team.SwitchAndKO",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterTeamBattleTest::RunTest(const FString& Parameters)
{
	using TeamSide = EPokeMonsterBattleSide;
	using TeamEvent = EPokeMonsterBattleEventType;
	TStrongObjectPtr<UPokeMonsterCreatureSpeciesData> Species(NewObject<UPokeMonsterCreatureSpeciesData>());
	TStrongObjectPtr<UPokeMonsterMoveData> Move(NewObject<UPokeMonsterMoveData>());
	Move->InternalId = TEXT("TeamTest");
	Move->DisplayName = FText::FromString(TEXT("Team test"));
	Move->MaxPP = 10;
	const auto Make = [&](int32 HP, int32 Speed)
	{
		auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species.Get(), 20);
		Creature.CurrentHP = HP < 0 ? Creature.GetMaxHP() : HP;
		Creature.CalculatedStats.Speed = Speed;
		Creature.AssignMove(0, Move.Get());
		return Creature;
	};
	const auto Count = [](const FPokeMonsterBattleResult& Result, TeamEvent Type)
	{
		int32 Total = 0;
		for (const auto& Event : Result.Events) if (Event.Type == Type) ++Total;
		return Total;
	};
	auto A0 = Make(-1, 100);
	auto A1 = Make(-1, 100);
	auto B0 = Make(-1, 20);
	auto B1 = Make(-1, 20);
	TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());
	TestEqual(TEXT("Empty team rejected"), Session->InitializeTeams({}, {B0}).Error, EPokeMonsterBattleError::InvalidTeam);
	TArray<FPokeMonsterCreatureInstance> TooMany;
	for (int32 Index = 0; Index < 7; ++Index) TooMany.Add(Make(-1, 100));
	TestEqual(TEXT("More than six rejected"), Session->InitializeTeams(TooMany, {B0}).Error, EPokeMonsterBattleError::InvalidTeam);
	TestEqual(TEXT("Duplicate instance rejected"), Session->InitializeTeams({A0, A0}, {B0}).Error, EPokeMonsterBattleError::DuplicateCreature);
	if (!TestTrue(TEXT("Two teams initialize"), Session->InitializeTeams({A0, A1}, {B0, B1}, 2026).bSucceeded)) return false;
	TestEqual(TEXT("Player team size"), Session->GetState().TeamA.Num(), 2);
	TestEqual(TEXT("Opponent team size"), Session->GetState().TeamB.Num(), 2);
	TestEqual(TEXT("First player active"), Session->GetState().ActiveIndexA, 0);
	TestEqual(TEXT("First opponent active"), Session->GetState().ActiveIndexB, 0);

	FPokeMonsterBattleChoice Switch, Attack;
	Switch.Type = EPokeMonsterBattleChoiceType::Switch; Switch.Index = 1;
	Attack.Index = 0;
	const auto Changed = Session->ResolveTurn(Switch, Attack);
	TestTrue(TEXT("Manual switch succeeds"), Changed.bSucceeded);
	TestEqual(TEXT("Switch takes one round"), Session->GetState().RoundNumber, 1);
	TestEqual(TEXT("Incoming member active"), Session->GetState().ActiveIndexA, 1);
	TestEqual(TEXT("Switch event emitted"), Count(Changed, TeamEvent::SwitchedIn), 1);
	TestEqual(TEXT("Switching member does not attack"), Count(Changed, TeamEvent::MoveExecuted), 1);
	TestEqual(TEXT("Opponent spends PP on switch turn"), Session->GetState().TeamB[0].GetMoveSlots()[0].GetCurrentPP(), 9);
	TestEqual(TEXT("Benched player's PP unchanged"), Session->GetState().TeamA[0].GetMoveSlots()[0].GetCurrentPP(), 10);
	TestEqual(TEXT("Benched player's HP unchanged"), Session->GetState().TeamA[0].CurrentHP, A0.CurrentHP);
	TestTrue(TEXT("Incoming member receives opponent attack"), Session->GetState().TeamA[1].CurrentHP < A1.CurrentHP);
	const int32 InjuredHP = Session->GetState().TeamA[1].CurrentHP;
	Switch.Index = 0;
	TestTrue(TEXT("Switch back succeeds"), Session->ResolveTurn(Switch, Attack).bSucceeded);
	TestEqual(TEXT("Second switch costs another turn"), Session->GetState().RoundNumber, 2);
	TestEqual(TEXT("Previously injured member keeps HP on bench"), Session->GetState().TeamA[1].CurrentHP, InjuredHP);

	TStrongObjectPtr<UPokeMonsterBattleSession> ForcedPlayer(NewObject<UPokeMonsterBattleSession>());
	auto FrailA = Make(1, 1);
	auto FastB = Make(-1, 1000);
	if (!TestTrue(TEXT("Forced-player battle starts"), ForcedPlayer->InitializeTeams({FrailA, A1}, {FastB}, 5).bSucceeded)) return false;
	const auto PlayerKO = ForcedPlayer->ResolveRound(0, 0);
	TestEqual(TEXT("Faint awaits mandatory switch"), ForcedPlayer->GetState().Phase, EPokeMonsterBattlePhase::AwaitingSwitch);
	TestEqual(TEXT("Team still has no winner"), ForcedPlayer->GetState().Winner, TeamSide::None);
	TestEqual(TEXT("No premature battle end event"), Count(PlayerKO, TeamEvent::BattleEnded), 0);
	TestEqual(TEXT("Cannot continue before switch"), ForcedPlayer->ResolveRound(0, 0).Error, EPokeMonsterBattleError::SwitchRequired);
	TestEqual(TEXT("Cannot switch to fainted member"), ForcedPlayer->ForceSwitch(TeamSide::A, 0).Error, EPokeMonsterBattleError::InvalidSwitch);
	const auto Forced = ForcedPlayer->ForceSwitch(TeamSide::A, 1);
	TestTrue(TEXT("Mandatory switch succeeds"), Forced.bSucceeded);
	TestEqual(TEXT("Mandatory switch costs no extra round"), ForcedPlayer->GetState().RoundNumber, 1);
	TestEqual(TEXT("Battle resumes after mandatory switch"), ForcedPlayer->GetState().Phase, EPokeMonsterBattlePhase::AwaitingChoices);
	TestEqual(TEXT("Fainted member stays fainted"), ForcedPlayer->GetState().TeamA[0].CurrentHP, 0);

	TStrongObjectPtr<UPokeMonsterBattleSession> ForcedOpponent(NewObject<UPokeMonsterBattleSession>());
	auto FrailB0 = Make(1, 1);
	auto FrailB1 = Make(1, 1);
	if (!TestTrue(TEXT("Opponent-team battle starts"), ForcedOpponent->InitializeTeams({A0}, {FrailB0, FrailB1}, 7).bSucceeded)) return false;
	const auto FirstKO = ForcedOpponent->ResolveRound(0, 0);
	TestEqual(TEXT("First opponent KO does not finish team battle"), ForcedOpponent->GetState().Phase, EPokeMonsterBattlePhase::AwaitingSwitch);
	TestEqual(TEXT("No first-KO battle end"), Count(FirstKO, TeamEvent::BattleEnded), 0);
	TestTrue(TEXT("Opponent replacement succeeds"), ForcedOpponent->ForceSwitch(TeamSide::B, 1).bSucceeded);
	TestEqual(TEXT("Next opponent active"), ForcedOpponent->GetState().ActiveIndexB, 1);
	const auto FinalKO = ForcedOpponent->ResolveRound(0, 0);
	TestEqual(TEXT("All opponent members KO ends battle"), ForcedOpponent->GetState().Phase, EPokeMonsterBattlePhase::Finished);
	TestEqual(TEXT("Player wins only after whole team KO"), ForcedOpponent->GetState().Winner, TeamSide::A);
	TestEqual(TEXT("Final end event"), Count(FinalKO, TeamEvent::BattleEnded), 1);
	TestEqual(TEXT("Both opponent members retain KO state"), ForcedOpponent->GetState().TeamB[0].CurrentHP + ForcedOpponent->GetState().TeamB[1].CurrentHP, 0);

	TStrongObjectPtr<UPokeMonsterBattlePresenter> Presenter(NewObject<UPokeMonsterBattlePresenter>());
	if (!TestTrue(TEXT("Team presenter initializes"), Presenter->InitializeTeamBattle({A0}, {FrailB0, FrailB1}, 7))) return false;
	TestEqual(TEXT("Presenter exposes opposing team"), Presenter->GetView().OpponentTeam.Num(), 2);
	TestTrue(TEXT("Presenter attack selected"), Presenter->TrySelectMove(0));
	TestTrue(TEXT("Presenter round resolved"), Presenter->ResolveSelection());
	TestTrue(TEXT("KO presentation locks input"), Presenter->GetView().bBusy);
	Presenter->FinishPresentation();
	TestTrue(TEXT("Automatic opponent switch keeps input locked"), Presenter->GetView().bBusy);
	TestTrue(TEXT("Next opponent is active"), Presenter->GetView().OpponentTeam[1].bActive);
	Presenter->FinishPresentation();
	TestFalse(TEXT("Input reopens after switch presentation"), Presenter->GetView().bBusy);

	TStrongObjectPtr<UPokeMonsterBattlePresenter> PlayerPresenter(NewObject<UPokeMonsterBattlePresenter>());
	if (!TestTrue(TEXT("Player replacement presenter initializes"), PlayerPresenter->InitializeTeamBattle({FrailA, A1}, {FastB}, 5))) return false;
	TestTrue(TEXT("Player attack selected"), PlayerPresenter->TrySelectMove(0));
	TestTrue(TEXT("Player KO resolved"), PlayerPresenter->ResolveSelection());
	PlayerPresenter->FinishPresentation();
	TestTrue(TEXT("Player must switch after faint"), PlayerPresenter->GetView().bMustSwitch);
	TestFalse(TEXT("Attack blocked until replacement"), PlayerPresenter->TrySelectMove(0));
	TestTrue(TEXT("Healthy bench member selectable"), PlayerPresenter->TrySelectSwitch(1));
	TestTrue(TEXT("Mandatory switch resolves"), PlayerPresenter->ResolveSelection());
	PlayerPresenter->FinishPresentation();
	TestTrue(TEXT("Player replacement active"), PlayerPresenter->GetView().PlayerTeam[1].bActive);
	return true;
}
#endif
