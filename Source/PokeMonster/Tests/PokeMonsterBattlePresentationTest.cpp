#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../UI/PokeMonsterBattlePresentationPlan.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterBattlePresentationEventsTest,
	"PokeMonster.Battle.Presentation.EventSequence",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterBattlePresentationEventsTest::RunTest(const FString& Parameters)
{
	FPokeMonsterBattleResult Round;
	Round.bSucceeded = true;
	FPokeMonsterBattleEvent Chosen;
	Chosen.Type = EPokeMonsterBattleEventType::MoveChosen;
	Chosen.Source = EPokeMonsterBattleSide::B;
	Round.Events.Add(Chosen);
	Chosen.Source = EPokeMonsterBattleSide::A;
	Round.Events.Add(Chosen);

	FPokeMonsterBattleEvent Executed;
	Executed.Type = EPokeMonsterBattleEventType::MoveExecuted;
	Executed.Source = EPokeMonsterBattleSide::B;
	Executed.Target = EPokeMonsterBattleSide::A;
	Executed.Category = EPokeMonsterMoveCategory::Special;
	Executed.PPAfter = 24;
	Round.Events.Add(Executed);
	FPokeMonsterBattleEvent Damage = Executed;
	Damage.Type = EPokeMonsterBattleEventType::SuperEffective;
	Damage.TypeMultiplier = 2.0f;
	Round.Events.Add(Damage);
	Damage.Type = EPokeMonsterBattleEventType::Damage;
	Damage.Damage = 12;
	Damage.HPBefore = 52;
	Damage.HPAfter = 40;
	Round.Events.Add(Damage);

	Executed.Source = EPokeMonsterBattleSide::A;
	Executed.Target = EPokeMonsterBattleSide::B;
	Executed.Category = EPokeMonsterMoveCategory::Physical;
	Round.Events.Add(Executed);
	FPokeMonsterBattleEvent Miss = Executed;
	Miss.Type = EPokeMonsterBattleEventType::Missed;
	Round.Events.Add(Miss);
	const auto Actions = UPokeMonsterBattlePresentationPlan::BuildActions(Round);
	TestEqual(TEXT("Chosen events do not create phantom actions"), Actions.Num(), 2);
	if (Actions.Num() != 2) return false;
	TestEqual(TEXT("Actual execution order leads presentation"), Actions[0].Source, EPokeMonsterBattleSide::B);
	TestEqual(TEXT("First action is a hit"), Actions[0].Outcome, EPokeMonsterPresentationOutcome::Hit);
	TestEqual(TEXT("First damage retains event values"), Actions[0].Damage, 12);
	TestEqual(TEXT("HP before retained"), Actions[0].HPBefore, 52);
	TestEqual(TEXT("HP after retained"), Actions[0].HPAfter, 40);
	TestEqual(TEXT("PP retained"), Actions[0].PPAfter, 24);
	TestEqual(TEXT("Multiplier retained"), Actions[0].TypeMultiplier, 2.0f);
	TestEqual(TEXT("Miss remains a separate second action"), Actions[1].Outcome, EPokeMonsterPresentationOutcome::Miss);
	TestEqual(TEXT("Miss never creates damage"), Actions[1].Damage, 0);

	Round.Events.Reset();
	Executed.Source = EPokeMonsterBattleSide::A;
	Executed.Category = EPokeMonsterMoveCategory::Status;
	Round.Events.Add(Executed);
	Executed.Source = EPokeMonsterBattleSide::B;
	Executed.Category = EPokeMonsterMoveCategory::Physical;
	Round.Events.Add(Executed);
	FPokeMonsterBattleEvent Immune = Executed;
	Immune.Type = EPokeMonsterBattleEventType::Immune;
	Round.Events.Add(Immune);
	const auto NoDamage = UPokeMonsterBattlePresentationPlan::BuildActions(Round);
	TestEqual(TEXT("Status is still an executed presentation action"), NoDamage.Num(), 2);
	if (NoDamage.Num() != 2) return false;
	TestEqual(TEXT("Status has no HP impact"), NoDamage[0].Outcome, EPokeMonsterPresentationOutcome::Status);
	TestEqual(TEXT("Immunity has separate feedback"), NoDamage[1].Outcome, EPokeMonsterPresentationOutcome::Immune);
	TestEqual(TEXT("Immunity has no HP impact"), NoDamage[1].Damage, 0);

	Round.Events.Reset();
	Round.Events.Add(Chosen); // A selected action can be cancelled by KO before execution.
	Round.Events.Add(Executed);
	Damage = Executed;
	Damage.Type = EPokeMonsterBattleEventType::Damage;
	Damage.Damage = 7;
	Damage.HPBefore = 7;
	Damage.HPAfter = 0;
	Round.Events.Add(Damage);
	FPokeMonsterBattleEvent KO = Damage;
	KO.Type = EPokeMonsterBattleEventType::KnockedOut;
	Round.Events.Add(KO);
	KO.Type = EPokeMonsterBattleEventType::BattleEnded;
	Round.Events.Add(KO);
	const auto Finish = UPokeMonsterBattlePresentationPlan::BuildActions(Round);
	TestEqual(TEXT("KO leaves no invented second action"), Finish.Num(), 1);
	if (Finish.Num() == 1)
	{
		TestTrue(TEXT("KO cue retained"), Finish[0].bKnockedOut);
		TestTrue(TEXT("Battle end cue retained"), Finish[0].bBattleEnded);
	}
	Round.bSucceeded = false;
	TestEqual(TEXT("Rejected rounds have no presentation actions"),
		UPokeMonsterBattlePresentationPlan::BuildActions(Round).Num(), 0);
	Round.bSucceeded = true;
	Round.Events.Reset();
	FPokeMonsterBattleEvent Switched;
	Switched.Type = EPokeMonsterBattleEventType::SwitchedIn;
	Switched.Source = EPokeMonsterBattleSide::A;
	Switched.TeamIndex = 2;
	Switched.HPBefore = Switched.HPAfter = 27;
	Round.Events.Add(Switched);
	Round.Events.Add(Executed);
	const auto WithSwitch = UPokeMonsterBattlePresentationPlan::BuildActions(Round);
	TestEqual(TEXT("Switch is presented before opponent attack"), WithSwitch.Num(), 2);
	if (WithSwitch.Num() == 2)
	{
		TestTrue(TEXT("First cue is the switch"), WithSwitch[0].bSwitch);
		TestEqual(TEXT("Switch target index retained"), WithSwitch[0].TeamIndex, 2);
		TestEqual(TEXT("Incoming HP retained"), WithSwitch[0].HPBefore, 27);
		TestFalse(TEXT("Second cue is an attack"), WithSwitch[1].bSwitch);
	}
	return true;
}
#endif
