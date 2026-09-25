#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Capture/PokeMonsterCaptureLibrary.h"
#include "../Capture/PokeMonsterCaptureDeviceData.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "Components/Button.h"
#include "Engine/AssetManager.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCaptureTest,
	"PokeMonster.Capture.WildBattleAndTeamTransfer",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterCaptureTest::RunTest(const FString& Parameters)
{
	using Library = FPokeMonsterCaptureLibrary;
	const float Full = Library::CalculateChance(100, 100, 120, 1.0f);
	const float Weak = Library::CalculateChance(1, 100, 120, 1.0f);
	const float Bonus = Library::CalculateChance(1, 100, 120, 1.5f);
	TestTrue(TEXT("Low HP increases capture chance"), Weak > Full);
	TestTrue(TEXT("Device bonus increases capture chance"), Bonus > Weak);
	TestEqual(TEXT("Invalid HP cannot be captured"), Library::CalculateChance(0, 100, 120, 1.0f), 0.0f);
	TestTrue(TEXT("Low deterministic roll captures"), Library::CheckCapture(0.5f, 0));
	TestFalse(TEXT("High deterministic roll fails"), Library::CheckCapture(0.5f, 9999));

	auto* Device = LoadObject<UPokeMonsterCaptureDeviceData>(nullptr,
		TEXT("/Game/Data/Capture/DA_TestCaptureDevice.DA_TestCaptureDevice"));
	auto* Grass = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Water = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	if (!TestNotNull(TEXT("Capture device asset"), Device)
		|| !TestNotNull(TEXT("Wild species asset"), Grass)
		|| !TestNotNull(TEXT("Player species asset"), Water)
		|| !TestNotNull(TEXT("Test move asset"), Move)) return false;
	TestTrue(TEXT("Device configured"), Device->IsConfigured());
	TestEqual(TEXT("Capture device scanned for cooking"),
		UAssetManager::Get().GetPrimaryAssetPath(Device->GetPrimaryAssetId()), FSoftObjectPath(Device));
	TestTrue(TEXT("Species capture rate available"), Grass->GetBaseCaptureRate() > 0);

	auto MakePlayer = [&]()
	{
		auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, 20);
		Creature.AssignMove(0, Move);
		return Creature;
	};
	auto MakeWild = [&]()
	{
		auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Grass, 5);
		Creature.AssignMove(0, Move);
		return Creature;
	};
	auto CaptureChoice = [&]()
	{
		FPokeMonsterBattleChoice Choice;
		Choice.Type = EPokeMonsterBattleChoiceType::Capture;
		Choice.CaptureDevice = Device;
		return Choice;
	};
	FPokeMonsterBattleChoice EnemyMove;
	EnemyMove.Index = 0;
	const auto Player = MakePlayer();
	const auto Wild = MakeWild();

	// A seed search uses the same FRandomStream roll as the session, without depending on a magic seed.
	const float Chance = Library::CalculateChance(Wild.CurrentHP, Wild.GetMaxHP(),
		Grass->GetBaseCaptureRate(), Device->GetCaptureBonus());
	int32 SuccessSeed = INDEX_NONE, FailureSeed = INDEX_NONE;
	for (int32 Seed = 0; Seed < 1000 && (SuccessSeed == INDEX_NONE || FailureSeed == INDEX_NONE); ++Seed)
	{
		FRandomStream Stream(Seed);
		const bool bSuccess = Library::CheckCapture(Chance, Stream.RandRange(0, 9999));
		if (bSuccess && SuccessSeed == INDEX_NONE) SuccessSeed = Seed;
		if (!bSuccess && FailureSeed == INDEX_NONE) FailureSeed = Seed;
	}
	if (!TestTrue(TEXT("Deterministic success and failure seeds found"),
		SuccessSeed != INDEX_NONE && FailureSeed != INDEX_NONE)) return false;

	auto* Forbidden = NewObject<UPokeMonsterBattleSession>();
	TestTrue(TEXT("Non-wild battle initializes"), Forbidden->Initialize(Player, Wild, SuccessSeed).bSucceeded);
	const auto Rejected = Forbidden->ResolveTurn(CaptureChoice(), EnemyMove);
	TestEqual(TEXT("Capture forbidden outside wild battles"), Rejected.Error,
		EPokeMonsterBattleError::CaptureNotAllowed);
	TestEqual(TEXT("Rejected capture costs no round"), Forbidden->GetState().RoundNumber, 0);

	auto* Success = NewObject<UPokeMonsterBattleSession>();
	TestTrue(TEXT("Wild battle initializes"), Success->InitializeTeams({Player}, {Wild}, SuccessSeed, true).bSucceeded);
	const auto Caught = Success->ResolveTurn(CaptureChoice(), EnemyMove);
	TestTrue(TEXT("Capture turn succeeds"), Caught.bSucceeded);
	TestEqual(TEXT("Capture consumes one turn"), Success->GetState().RoundNumber, 1);
	TestEqual(TEXT("Capture ends battle immediately"), Success->GetState().EndReason,
		EPokeMonsterBattleEndReason::Captured);
	TestEqual(TEXT("Captured individual identity retained"), Success->GetState().CapturedCreature.InstanceId,
		Wild.InstanceId);
	TestEqual(TEXT("Captured individual HP retained"), Success->GetState().CapturedCreature.CurrentHP,
		Wild.CurrentHP);
	TestEqual(TEXT("Captured individual PP retained"),
		Success->GetState().CapturedCreature.GetMoveSlots()[0].GetCurrentPP(),
		Wild.GetMoveSlots()[0].GetCurrentPP());
	bool bCaptureEvent = false, bEnemyAttacked = false;
	for (const auto& Event : Caught.Events)
	{
		bCaptureEvent |= Event.Type == EPokeMonsterBattleEventType::CaptureSucceeded;
		bEnemyAttacked |= Event.Type == EPokeMonsterBattleEventType::MoveExecuted
			&& Event.Source == EPokeMonsterBattleSide::B;
	}
	TestTrue(TEXT("Success event emitted"), bCaptureEvent);
	TestFalse(TEXT("No enemy move after successful capture"), bEnemyAttacked);
	FPokeMonsterEncounterStartData Start;
	Start.Kind = EPokeMonsterEncounterKind::Wild;
	const auto End = UPokeMonsterEncounterSubsystem::BuildEndData(Start, Success->GetState());
	TestEqual(TEXT("Distinct captured encounter result"), End.Outcome, EPokeMonsterEncounterOutcome::Captured);
	TestEqual(TEXT("Captured creature joins a party with room"), End.CaptureTransfer,
		EPokeMonsterCaptureTransfer::AddedToTeam);
	TestEqual(TEXT("New party size"), End.PlayerTeam.Num(), 2);
	TestEqual(TEXT("New party member is the captured individual"), End.PlayerTeam.Last().InstanceId,
		Wild.InstanceId);

	TArray<FPokeMonsterCreatureInstance> FullTeam;
	for (int32 Index = 0; Index < 6; ++Index) FullTeam.Add(MakePlayer());
	auto* FullPartySession = NewObject<UPokeMonsterBattleSession>();
	TestTrue(TEXT("Full party wild battle initializes"),
		FullPartySession->InitializeTeams(FullTeam, {Wild}, SuccessSeed, true).bSucceeded);
	TestTrue(TEXT("Full party can capture"), FullPartySession->ResolveTurn(CaptureChoice(), EnemyMove).bSucceeded);
	const auto FullEnd = UPokeMonsterEncounterSubsystem::BuildEndData(Start, FullPartySession->GetState());
	TestEqual(TEXT("Full party reports transfer handoff"), FullEnd.CaptureTransfer,
		EPokeMonsterCaptureTransfer::TeamFull);
	TestEqual(TEXT("Party stays at six"), FullEnd.PlayerTeam.Num(), 6);
	TestEqual(TEXT("Reserve handoff preserves captured individual"), FullEnd.CapturedCreature.InstanceId,
		Wild.InstanceId);

	auto* Failure = NewObject<UPokeMonsterBattleSession>();
	TestTrue(TEXT("Failed-capture battle initializes"),
		Failure->InitializeTeams({Player}, {Wild}, FailureSeed, true).bSucceeded);
	const auto Escaped = Failure->ResolveTurn(CaptureChoice(), EnemyMove);
	TestTrue(TEXT("Failed capture still resolves the turn"), Escaped.bSucceeded);
	TestEqual(TEXT("Failed capture consumes one turn"), Failure->GetState().RoundNumber, 1);
	bCaptureEvent = bEnemyAttacked = false;
	for (const auto& Event : Escaped.Events)
	{
		bCaptureEvent |= Event.Type == EPokeMonsterBattleEventType::CaptureFailed;
		bEnemyAttacked |= Event.Type == EPokeMonsterBattleEventType::MoveExecuted
			&& Event.Source == EPokeMonsterBattleSide::B;
	}
	TestTrue(TEXT("Failure event emitted"), bCaptureEvent);
	TestTrue(TEXT("Opponent acts after failed capture"), bEnemyAttacked);
	TestEqual(TEXT("Opponent PP consumed after failure"),
		Failure->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(),
		Wild.GetMoveSlots()[0].GetCurrentPP() - 1);

	auto* Presenter = NewObject<UPokeMonsterBattlePresenter>();
	TestTrue(TEXT("Wild presenter initializes"), Presenter->InitializeTeamBattle({Player}, {Wild}, SuccessSeed, true));
	TestTrue(TEXT("Capture UI action available for wild battle"), Presenter->GetView().bCaptureEnabled);
	TestTrue(TEXT("Capture UI selection locks input"), Presenter->TrySelectCapture());
	TestFalse(TEXT("Duplicate capture selection rejected"), Presenter->TrySelectCapture());
	TestTrue(TEXT("Presenter forwards capture to session"), Presenter->ResolveSelection());
	TestFalse(TEXT("Capture input stays locked during presentation"), Presenter->GetView().bCaptureEnabled);
	Presenter->FinishPresentation();
	TestTrue(TEXT("Presenter shows battle finished"), Presenter->GetView().bFinished);

	UWorld* PlayWorld = nullptr;
	for (const FWorldContext& Context : GEngine->GetWorldContexts())
		if (Context.WorldType == EWorldType::PIE) { PlayWorld = Context.World(); break; }
	if (!PlayWorld) return true;
	APlayerController* Controller = PlayWorld->GetFirstPlayerController();
	auto* WorldPlayer = Controller ? Cast<APokeMonsterPlayerCharacter>(Controller->GetPawn()) : nullptr;
	auto* Encounters = PlayWorld->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	if (!TestNotNull(TEXT("PIE player exists"), WorldPlayer)
		|| !TestNotNull(TEXT("PIE encounter subsystem exists"), Encounters)
		|| !TestFalse(TEXT("PIE starts outside battle"), Encounters->IsEncounterActive())) return false;
	APokeMonsterVisibleWildCreatureActor* VisibleActor = nullptr;
	for (TActorIterator<APokeMonsterVisibleWildCreatureActor> It(PlayWorld); It; ++It)
		if (!VisibleActor) VisibleActor = *It;
	if (!TestNotNull(TEXT("Visible wild actor exists in PIE map"), VisibleActor)) return false;
	FPokeMonsterEncounterStartData WorldStart;
	WorldStart.EncounterId = TEXT("AutomationCapture");
	WorldStart.Kind = EPokeMonsterEncounterKind::Wild;
	WorldStart.Source = EPokeMonsterEncounterSource::VisibleCreature;
	WorldStart.PlayerTeam = {MakePlayer()};
	WorldStart.OpponentTeam = {MakeWild()};
	WorldStart.RandomSeed = SuccessSeed;
	WorldStart.SourceActor = VisibleActor;
	if (!TestTrue(TEXT("Wild battle starts over PIE world"),
		Encounters->StartEncounter(WorldStart, WorldPlayer))) return false;
	TestTrue(TEXT("World input locked during capture battle"), WorldPlayer->IsOverworldInputLocked());
	UPokeMonsterBattleWidget* WorldWidget = Encounters->GetBattleWidget();
	UPokeMonsterBattlePresenter* WorldPresenter = Encounters->GetPresenter();
	if (!TestNotNull(TEXT("Battle UI is present"), WorldWidget)
		|| !TestNotNull(TEXT("Battle presenter is present"), WorldPresenter)
		|| !TestNotNull(TEXT("Capture button is present"), WorldWidget->GetCaptureButton())) return false;
	TestTrue(TEXT("Capture button enabled in wild battle"), WorldWidget->GetCaptureButton()->GetIsEnabled());
	WorldWidget->GetCaptureButton()->OnClicked.Broadcast();
	TestTrue(TEXT("UI click locks the capture choice"), WorldPresenter->GetView().bBusy);
	if (!TestTrue(TEXT("UI capture resolves"), WorldPresenter->ResolveSelection())) return false;
	TestEqual(TEXT("PIE session captures the wild creature"), WorldPresenter->GetBattleState()->EndReason,
		EPokeMonsterBattleEndReason::Captured);
	WorldPresenter->FinishPresentation();
	Encounters->CompleteEncounter();
	TestFalse(TEXT("PIE world input restored"), WorldPlayer->IsOverworldInputLocked());
	TestFalse(TEXT("PIE encounter closed"), Encounters->IsEncounterActive());
	TestEqual(TEXT("PIE result is Captured"), Encounters->GetLastResult().Outcome,
		EPokeMonsterEncounterOutcome::Captured);
	TestEqual(TEXT("PIE captured creature joins player team"), Encounters->GetPlayerParty().Num(), 2);
	TestTrue(TEXT("Visible wild actor hidden after capture"), VisibleActor->IsHidden());
	return true;
}
#endif
