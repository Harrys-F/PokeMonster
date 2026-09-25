#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Encounter/PokeMonsterBattleEncounterActor.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "GameFramework/PlayerController.h"
#include "InputActionValue.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterEncounterIntegrationTest,
	"PokeMonster.Encounter.OverworldIntegration",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterEncounterIntegrationTest::RunTest(const FString& Parameters)
{
	TestTrue(TEXT("Encounter marker uses the existing interaction contract"),
		APokeMonsterBattleEncounterActor::StaticClass()->ImplementsInterface(UPokeMonsterInteractable::StaticClass()));
	TArray<FPokeMonsterCreatureInstance> PlayerTeam, OpponentTeam;
	if (!TestTrue(TEXT("Test encounter builds teams from existing assets"),
		UPokeMonsterEncounterSubsystem::BuildTestTeams(PlayerTeam, OpponentTeam))) return false;
	TestEqual(TEXT("Player test team has two members"), PlayerTeam.Num(), 2);
	TestEqual(TEXT("Opponent test team has two members"), OpponentTeam.Num(), 2);
	TestTrue(TEXT("Members have distinct individual IDs"), PlayerTeam[0].InstanceId != PlayerTeam[1].InstanceId);
	TestEqual(TEXT("Default party starts with full PP"), PlayerTeam[0].GetMoveSlots()[0].GetCurrentPP(),
		PlayerTeam[0].GetMoveSlots()[0].GetMaxPP());
	TestFalse(TEXT("Default player is not locked"), GetDefault<APokeMonsterPlayerCharacter>()->IsOverworldInputLocked());
	FPokeMonsterEncounterStartData Contract;
	Contract.EncounterId = TEXT("ContractVictory");
	Contract.Kind = EPokeMonsterEncounterKind::Test;
	auto WinningPlayer = PlayerTeam[0];
	WinningPlayer.CalculatedStats.Speed = 1000;
	auto LosingOpponent = OpponentTeam[0];
	LosingOpponent.CurrentHP = 1;
	LosingOpponent.CalculatedStats.Speed = 1;
	UPokeMonsterBattlePresenter* ContractPresenter = NewObject<UPokeMonsterBattlePresenter>();
	if (!TestTrue(TEXT("Contract victory battle initializes"),
		ContractPresenter->InitializeBattle(WinningPlayer, LosingOpponent, 13))) return false;
	if (!TestTrue(TEXT("Contract victory move selected"), ContractPresenter->TrySelectMove(0))) return false;
	if (!TestTrue(TEXT("Contract victory round resolves"), ContractPresenter->ResolveSelection())) return false;
	ContractPresenter->FinishPresentation();
	const FPokeMonsterBattleState* ContractState = ContractPresenter->GetBattleState();
	if (!TestTrue(TEXT("Contract victory finishes"), ContractState && ContractState->Phase == EPokeMonsterBattlePhase::Finished)) return false;
	const auto VictoryEnd = UPokeMonsterEncounterSubsystem::BuildEndData(Contract, *ContractState);
	TestEqual(TEXT("Victory result is structured"), VictoryEnd.Outcome, EPokeMonsterEncounterOutcome::Victory);
	TestEqual(TEXT("Encounter ID survives the transition"), VictoryEnd.EncounterId, Contract.EncounterId);
	TestEqual(TEXT("Winning move PP returns to overworld"), VictoryEnd.PlayerTeam[0].GetMoveSlots()[0].GetCurrentPP(),
		WinningPlayer.GetMoveSlots()[0].GetCurrentPP() - 1);
	TestEqual(TEXT("Winning creature HP returns to overworld"), VictoryEnd.PlayerTeam[0].CurrentHP,
		WinningPlayer.CurrentHP);

	Contract.EncounterId = TEXT("ContractDefeat");
	auto LosingPlayer = PlayerTeam[1];
	LosingPlayer.CurrentHP = 1;
	LosingPlayer.CalculatedStats.Speed = 1;
	auto WinningOpponent = OpponentTeam[1];
	WinningOpponent.CalculatedStats.Speed = 1000;
	ContractPresenter = NewObject<UPokeMonsterBattlePresenter>();
	if (!TestTrue(TEXT("Contract defeat battle initializes"),
		ContractPresenter->InitializeBattle(LosingPlayer, WinningOpponent, 17))) return false;
	if (!TestTrue(TEXT("Contract defeat move selected"), ContractPresenter->TrySelectMove(0))) return false;
	if (!TestTrue(TEXT("Contract defeat round resolves"), ContractPresenter->ResolveSelection())) return false;
	ContractPresenter->FinishPresentation();
	ContractState = ContractPresenter->GetBattleState();
	if (!TestTrue(TEXT("Contract defeat finishes"), ContractState && ContractState->Phase == EPokeMonsterBattlePhase::Finished)) return false;
	const auto DefeatEnd = UPokeMonsterEncounterSubsystem::BuildEndData(Contract, *ContractState);
	TestEqual(TEXT("Defeat result is structured"), DefeatEnd.Outcome, EPokeMonsterEncounterOutcome::Defeat);
	TestEqual(TEXT("Fainted HP returns to overworld"), DefeatEnd.PlayerTeam[0].CurrentHP, 0);
	TestEqual(TEXT("No PP spent after KO before turn"), DefeatEnd.PlayerTeam[0].GetMoveSlots()[0].GetCurrentPP(),
		LosingPlayer.GetMoveSlots()[0].GetCurrentPP());

	UWorld* PlayWorld = nullptr;
	for (const FWorldContext& Context : GEngine->GetWorldContexts())
		if (Context.WorldType == EWorldType::PIE) { PlayWorld = Context.World(); break; }
	if (!PlayWorld) return true; // The world contract below is also exercised during PIE.

	APlayerController* Controller = PlayWorld->GetFirstPlayerController();
	APokeMonsterPlayerCharacter* Player = Controller ? Cast<APokeMonsterPlayerCharacter>(Controller->GetPawn()) : nullptr;
	if (!TestNotNull(TEXT("Overworld PIE player exists"), Player)) return false;
	UPokeMonsterEncounterSubsystem* Encounters = PlayWorld->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	if (!TestNotNull(TEXT("Encounter coordination exists in game instance"), Encounters)) return false;
	if (!TestFalse(TEXT("No encounter is initially active"), Encounters->IsEncounterActive())) return false;
	const FVector WorldPosition = Player->GetActorLocation();

	FPokeMonsterEncounterStartData Start;
	Start.EncounterId = TEXT("AutomationVictory");
	Start.Kind = EPokeMonsterEncounterKind::Test;
	Start.PlayerTeam.Add(PlayerTeam[0]);
	OpponentTeam[0].CurrentHP = 1;
	Start.OpponentTeam.Add(OpponentTeam[0]);
	if (!TestTrue(TEXT("Battle starts from loaded overworld"), Encounters->StartEncounter(Start, Player))) return false;
	TestTrue(TEXT("Movement and interaction lock during battle"), Player->IsOverworldInputLocked());
	TestFalse(TEXT("Second encounter cannot start"), Encounters->StartEncounter(Start, Player));
	TestFalse(TEXT("World interaction blocked while battle is open"), Player->TryInteract());
	Player->Move(FInputActionValue(FVector2D(1.0f, 0.0f)));
	TestTrue(TEXT("Locked movement input stays zero"), Player->GetMovementInput().IsNearlyZero());
	TestEqual(TEXT("World position is retained"), Player->GetActorLocation(), WorldPosition);
	UPokeMonsterBattlePresenter* Presenter = Encounters->GetPresenter();
	TestNotNull(TEXT("Existing battle presenter drives encounter"), Presenter);
	TestNotNull(TEXT("Existing battle widget presents over world"), Encounters->GetBattleWidget());
	TestEqual(TEXT("Session receives player's individual ID"), Presenter->GetBattleState()->TeamA[0].InstanceId,
		Start.PlayerTeam[0].InstanceId);
	TestEqual(TEXT("Session receives opponent's individual ID"), Presenter->GetBattleState()->TeamB[0].InstanceId,
		Start.OpponentTeam[0].InstanceId);
	if (!TestTrue(TEXT("Player chooses a move"), Presenter->TrySelectMove(0))) return false;
	if (!TestTrue(TEXT("Winning round resolves"), Presenter->ResolveSelection())) return false;
	Presenter->FinishPresentation();
	TestTrue(TEXT("Victory is decided by session"), Presenter->GetView().bFinished);
	Encounters->CompleteEncounter();
	TestFalse(TEXT("Encounter ends and overworld resumes"), Encounters->IsEncounterActive());
	TestFalse(TEXT("Exploration input unlocked"), Player->IsOverworldInputLocked());
	TestEqual(TEXT("Victory returned to world"), Encounters->GetLastResult().Outcome, EPokeMonsterEncounterOutcome::Victory);
	TestEqual(TEXT("World position remains unchanged"), Player->GetActorLocation(), WorldPosition);
	TestEqual(TEXT("Player's consumed PP is retained"), Encounters->GetPlayerParty()[0].GetMoveSlots()[0].GetCurrentPP(),
		Start.PlayerTeam[0].GetMoveSlots()[0].GetCurrentPP() - 1);
	Player->Move(FInputActionValue(FVector2D(1.0f, 0.0f)));
	TestFalse(TEXT("Movement input works after return"), Player->GetMovementInput().IsNearlyZero());
	Player->StopMoving(FInputActionValue(FVector2D::ZeroVector));

	// A separate controlled one-member encounter exercises defeat and HP transfer.
	FPokeMonsterEncounterStartData Defeat;
	Defeat.EncounterId = TEXT("AutomationDefeat");
	Defeat.PlayerTeam.Add(PlayerTeam[1]);
	Defeat.PlayerTeam[0].CurrentHP = 1;
	Defeat.PlayerTeam[0].CalculatedStats.Speed = 1;
	Defeat.OpponentTeam.Add(OpponentTeam[1]);
	Defeat.OpponentTeam[0].CalculatedStats.Speed = 1000;
	if (!TestTrue(TEXT("Second encounter starts after return"), Encounters->StartEncounter(Defeat, Player))) return false;
	Presenter = Encounters->GetPresenter();
	if (!TestTrue(TEXT("Defeat round selected"), Presenter->TrySelectMove(0))) return false;
	if (!TestTrue(TEXT("Defeat round resolves"), Presenter->ResolveSelection())) return false;
	Presenter->FinishPresentation();
	TestTrue(TEXT("Defeat is decided by session"), Presenter->GetView().bFinished);
	Encounters->CompleteEncounter();
	TestEqual(TEXT("Defeat returned to world"), Encounters->GetLastResult().Outcome, EPokeMonsterEncounterOutcome::Defeat);
	TestEqual(TEXT("Fainted HP stays with player party"), Encounters->GetPlayerParty()[0].CurrentHP, 0);
	TestFalse(TEXT("Control returns after defeat"), Player->IsOverworldInputLocked());
	return true;
}
#endif
