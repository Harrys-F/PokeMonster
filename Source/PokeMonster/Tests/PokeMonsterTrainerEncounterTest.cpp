#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Encounter/PokeMonsterTrainerProfile.h"
#include "../Encounter/PokeMonsterTrainerNPC.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Capture/PokeMonsterCaptureDeviceData.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "Engine/AssetManager.h"
#include "Engine/GameInstance.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterTrainerEncounterTest,
	"PokeMonster.Encounter.TrainerProfileAndDefeatState",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterTrainerEncounterTest::RunTest(const FString& Parameters)
{
	auto* Profile = LoadObject<UPokeMonsterTrainerProfile>(nullptr,
		TEXT("/Game/Data/Trainers/DA_DevTrainer.DA_DevTrainer"));
	auto* Water = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	auto* Device = LoadObject<UPokeMonsterCaptureDeviceData>(nullptr,
		TEXT("/Game/Data/Capture/DA_TestCaptureDevice.DA_TestCaptureDevice"));
	if (!TestNotNull(TEXT("Trainer profile loads"), Profile)
		|| !TestNotNull(TEXT("Player species loads"), Water)
		|| !TestNotNull(TEXT("Test move loads"), Move)
		|| !TestNotNull(TEXT("Capture device loads"), Device)) return false;
	TestTrue(TEXT("Trainer profile is scanned for cooking"),
		UAssetManager::Get().GetPrimaryAssetPath(Profile->GetPrimaryAssetId()) == FSoftObjectPath(Profile));
	TestTrue(TEXT("Trainer has a stable identity and display fields"),
		!Profile->InternalId.IsNone() && !Profile->DisplayName.IsEmpty() && !Profile->TrainerClass.IsEmpty());
	TestTrue(TEXT("Trainer NPC implements the shared interaction interface"),
		APokeMonsterTrainerNPC::StaticClass()->ImplementsInterface(UPokeMonsterInteractable::StaticClass()));

	TArray<FPokeMonsterCreatureInstance> TrainerTeam, SecondTeam;
	if (!TestTrue(TEXT("Profile builds its own team"), Profile->BuildTeam(TrainerTeam))
		|| !TestTrue(TEXT("Profile can build a fresh team"), Profile->BuildTeam(SecondTeam))) return false;
	TestEqual(TEXT("Profile team size"), TrainerTeam.Num(), Profile->Team.Num());
	TestTrue(TEXT("Trainer team has multiple members"), TrainerTeam.Num() >= 2);
	for (int32 Index = 0; Index < TrainerTeam.Num(); ++Index)
	{
		TestEqual(TEXT("Configured level is applied"), TrainerTeam[Index].Level, Profile->Team[Index].Level);
		TestFalse(TEXT("Starting attack is assigned"), TrainerTeam[Index].GetMoveSlots()[0].GetMove().IsNull());
		TestEqual(TEXT("New battle gets new individual identity"),
			TrainerTeam[Index].InstanceId == SecondTeam[Index].InstanceId, false);
	}
	FPokeMonsterEncounterStartData Start;
	if (!TestTrue(TEXT("Trainer profile prepares encounter"),
		UPokeMonsterEncounterSubsystem::PrepareTrainerEncounter(Profile, nullptr, 802, Start))) return false;
	TestEqual(TEXT("Trainer battle kind"), Start.Kind, EPokeMonsterEncounterKind::Trainer);
	TestEqual(TEXT("Trainer ID travels with start data"), Start.TrainerId, Profile->InternalId);
	TestEqual(TEXT("Trainer battle receives configured team"), Start.OpponentTeam.Num(), Profile->Team.Num());
	TestEqual(TEXT("Trainer seed is retained"), Start.RandomSeed, 802);

	auto Player = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, 30);
	if (!TestTrue(TEXT("Player move assigned"), Player.AssignMove(0, Move))) return false;
	auto* Forbidden = NewObject<UPokeMonsterBattleSession>();
	if (!TestTrue(TEXT("Trainer session initializes"),
		Forbidden->InitializeTeams({Player}, {TrainerTeam[0]}, 802, false).bSucceeded)) return false;
	FPokeMonsterBattleChoice Capture;
	Capture.Type = EPokeMonsterBattleChoiceType::Capture;
	Capture.CaptureDevice = Device;
	FPokeMonsterBattleChoice EnemyMove;
	EnemyMove.Index = 0;
	const auto Rejected = Forbidden->ResolveTurn(Capture, EnemyMove);
	TestEqual(TEXT("Trainer capture is forbidden"), Rejected.Error, EPokeMonsterBattleError::CaptureNotAllowed);
	TestEqual(TEXT("Rejected capture spends no turn"), Forbidden->GetState().RoundNumber, 0);
	auto* Presenter = NewObject<UPokeMonsterBattlePresenter>();
	TestTrue(TEXT("Trainer presenter uses existing team battle"),
		Presenter->InitializeTeamBattle({Player}, TrainerTeam, 802, false));
	TestFalse(TEXT("Capture button disabled for trainer"), Presenter->GetView().bCaptureEnabled);
	TestFalse(TEXT("Capture choice rejected by presenter"), Presenter->TrySelectCapture());

	auto* TestGameInstance = NewObject<UGameInstance>();
	auto* Progress = NewObject<UPokeMonsterEncounterSubsystem>(TestGameInstance);
	TestFalse(TEXT("Trainer starts undefeated"), Progress->IsTrainerDefeated(Profile->InternalId));
	FPokeMonsterEncounterEndData Defeat;
	Defeat.Kind = EPokeMonsterEncounterKind::Trainer;
	Defeat.TrainerId = Profile->InternalId;
	Defeat.Outcome = EPokeMonsterEncounterOutcome::Defeat;
	Progress->RecordTrainerOutcome(Defeat);
	TestFalse(TEXT("Player loss leaves trainer available"), Progress->IsTrainerDefeated(Profile->InternalId));
	FPokeMonsterEncounterEndData Victory = Defeat;
	Victory.Outcome = EPokeMonsterEncounterOutcome::Victory;
	Progress->RecordTrainerOutcome(Victory);
	TestTrue(TEXT("Player win marks trainer defeated"), Progress->IsTrainerDefeated(Profile->InternalId));
	TestEqual(TEXT("Defeated ID is exposed for savegame handoff"),
		Progress->GetDefeatedTrainerIds().Num(), 1);
	auto* Restored = NewObject<UPokeMonsterEncounterSubsystem>(TestGameInstance);
	Restored->RestoreDefeatedTrainerIds(Progress->GetDefeatedTrainerIds());
	TestTrue(TEXT("Defeat state can be restored in a new subsystem"), Restored->IsTrainerDefeated(Profile->InternalId));
	return true;
}
#endif
