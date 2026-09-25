#include "PokeMonsterEncounterSubsystem.h"
#include "PokeMonsterEncounterProfile.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "Blueprint/UserWidget.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "TimerManager.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterEncounter, Log, All);

bool UPokeMonsterEncounterSubsystem::BuildTestTeams(TArray<FPokeMonsterCreatureInstance>& Player,
	TArray<FPokeMonsterCreatureInstance>& Opponent)
{
	auto* Water = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Grass = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Normal = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	auto* Fire = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestFireSpecial.DA_TestFireSpecial"));
	auto* Status = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestStatus.DA_TestStatus"));
	if (!Water || !Grass || !Normal || !Fire || !Status) return false;
	for (const int32 Level : {20, 18})
	{
		auto A = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, Level);
		auto B = FPokeMonsterCreatureInstance::CreateFromSpecies(Grass, Level);
		UPokeMonsterMoveData* AMoves[] = {Normal, Fire, Status, Normal};
		UPokeMonsterMoveData* BMoves[] = {Normal, Status, Fire, Normal};
		for (int32 Slot = 0; Slot < 4; ++Slot)
			if (!A.AssignMove(Slot, AMoves[Slot]) || !B.AssignMove(Slot, BMoves[Slot])) return false;
		Player.Add(MoveTemp(A));
		Opponent.Add(MoveTemp(B));
	}
	return true;
}

bool UPokeMonsterEncounterSubsystem::StartTestEncounter(APokeMonsterPlayerCharacter* Player, AActor* SourceActor)
{
	TArray<FPokeMonsterCreatureInstance> InitialParty, Opponents;
	if (!BuildTestTeams(InitialParty, Opponents))
	{
		UE_LOG(LogPokeMonsterEncounter, Error, TEXT("Test encounter assets are missing or invalid."));
		return false;
	}
	FPokeMonsterEncounterStartData Start;
	Start.EncounterId = TEXT("Dev_TestEncounter");
	Start.Kind = EPokeMonsterEncounterKind::Test;
	Start.PlayerTeam = PlayerParty.IsEmpty() ? MoveTemp(InitialParty) : PlayerParty;
	Start.OpponentTeam = MoveTemp(Opponents);
	Start.SourceActor = SourceActor;
	return StartEncounter(Start, Player);
}

bool UPokeMonsterEncounterSubsystem::EnsureDevPlayerParty()
{
	if (!PlayerParty.IsEmpty()) return true;
	TArray<FPokeMonsterCreatureInstance> InitialParty, UnusedOpponents;
	if (!BuildTestTeams(InitialParty, UnusedOpponents)) return false;
	PlayerParty = MoveTemp(InitialParty);
	return true;
}

bool UPokeMonsterEncounterSubsystem::PrepareWildEncounter(const UPokeMonsterEncounterProfile* Profile,
	const FPokeMonsterEncounterContext& Context, EPokeMonsterEncounterSource Source,
	AActor* SourceActor, int32 Seed, FName EncounterId, FPokeMonsterEncounterStartData& OutStart)
{
	OutStart = FPokeMonsterEncounterStartData();
	if (!IsValid(Profile)) return false;
	FRandomStream Random(Seed);
	FPokeMonsterCreatureInstance WildCreature;
	if (!Profile->Roll(Context, Random, WildCreature)) return false;
	OutStart.EncounterId = EncounterId;
	OutStart.Kind = EPokeMonsterEncounterKind::Wild;
	OutStart.Source = Source;
	OutStart.OpponentTeam.Add(MoveTemp(WildCreature));
	OutStart.RandomSeed = Seed;
	OutStart.SourceActor = SourceActor;
	return true;
}

bool UPokeMonsterEncounterSubsystem::StartWildEncounter(const UPokeMonsterEncounterProfile* Profile,
	const FPokeMonsterEncounterContext& Context, EPokeMonsterEncounterSource Source,
	APokeMonsterPlayerCharacter* Player, AActor* SourceActor, int32 Seed, FName EncounterId)
{
	FPokeMonsterEncounterStartData Start;
	if (!PrepareWildEncounter(Profile, Context, Source, SourceActor, Seed, EncounterId, Start))
	{
		UE_LOG(LogPokeMonsterEncounter, Warning, TEXT("Wild encounter '%s' has no valid profile entry."), *EncounterId.ToString());
		return false;
	}
	return StartEncounter(Start, Player);
}

bool UPokeMonsterEncounterSubsystem::StartEncounter(const FPokeMonsterEncounterStartData& Start,
	APokeMonsterPlayerCharacter* Player)
{
	if (bActive || !IsValid(Player) || Player->IsOverworldInputLocked()) return false;
	APlayerController* Controller = Cast<APlayerController>(Player->GetController());
	UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr;
	if (!Controller || !Controller->IsLocalController() || !World || Player->GetWorld() != World) return false;

	const TArray<FPokeMonsterCreatureInstance>& Team = Start.PlayerTeam.IsEmpty() ? PlayerParty : Start.PlayerTeam;
	UPokeMonsterBattlePresenter* NewPresenter = NewObject<UPokeMonsterBattlePresenter>(this);
	if (!NewPresenter->InitializeTeamBattle(Team, Start.OpponentTeam, Start.RandomSeed,
		Start.Kind == EPokeMonsterEncounterKind::Wild)) return false;
	UPokeMonsterBattleWidget* NewWidget = CreateWidget<UPokeMonsterBattleWidget>(Controller, UPokeMonsterBattleWidget::StaticClass());
	if (!NewWidget) return false;

	Presenter = NewPresenter;
	BattleWidget = NewWidget;
	ActiveStart = Start;
	ActivePlayer = Player;
	ActiveController = Controller;
	bPreviousMouseCursor = Controller->bShowMouseCursor;
	bActive = true;
	PlayerParty = Team;
	Player->SetOverworldInputLocked(true);
	NewWidget->SetEncounterOverlay(true);
	NewWidget->SetPresenter(NewPresenter);
	NewWidget->SetIsFocusable(true);
	NewWidget->AddToViewport(100);
	NewPresenter->OnChanged.AddUniqueDynamic(this, &UPokeMonsterEncounterSubsystem::HandlePresenterChanged);
	FInputModeUIOnly Input;
	Input.SetWidgetToFocus(NewWidget->TakeWidget());
	Controller->SetInputMode(Input);
	Controller->bShowMouseCursor = true;
	UE_LOG(LogPokeMonsterEncounter, Display, TEXT("Encounter '%s' started in %s."),
		*Start.EncounterId.ToString(), *World->GetName());
	return true;
}

void UPokeMonsterEncounterSubsystem::HandlePresenterChanged()
{
	if (!bActive || !Presenter || !Presenter->GetView().bFinished || Presenter->GetView().bBusy) return;
	if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
		if (!World->GetTimerManager().IsTimerActive(CompletionTimer))
			World->GetTimerManager().SetTimer(CompletionTimer, this,
				&UPokeMonsterEncounterSubsystem::CompleteEncounter, 0.75f, false);
}

void UPokeMonsterEncounterSubsystem::CompleteEncounter()
{
	if (!bActive || !Presenter) return;
	const FPokeMonsterBattleState* State = Presenter->GetBattleState();
	if (!State || State->Phase != EPokeMonsterBattlePhase::Finished) return;
	LastResult = BuildEndData(ActiveStart, *State);
	PlayerParty = LastResult.PlayerTeam;
	ReleaseOverworld();
	UE_LOG(LogPokeMonsterEncounter, Display, TEXT("Encounter '%s' ended: %s, rounds: %d, party: %d."),
		*LastResult.EncounterId.ToString(),
		LastResult.Outcome == EPokeMonsterEncounterOutcome::Captured ? TEXT("Captured")
			: LastResult.Outcome == EPokeMonsterEncounterOutcome::Victory ? TEXT("Victory") : TEXT("Defeat"),
		LastResult.Rounds, PlayerParty.Num());
	OnEncounterEnded.Broadcast(LastResult);
}

FPokeMonsterEncounterEndData UPokeMonsterEncounterSubsystem::BuildEndData(
	const FPokeMonsterEncounterStartData& Start, const FPokeMonsterBattleState& State)
{
	FPokeMonsterEncounterEndData End;
	End.EncounterId = Start.EncounterId;
	End.Kind = Start.Kind;
	End.Source = Start.Source;
	End.Outcome = State.EndReason == EPokeMonsterBattleEndReason::Captured
		&& Start.Kind == EPokeMonsterEncounterKind::Wild
		? EPokeMonsterEncounterOutcome::Captured
		: State.Winner == EPokeMonsterBattleSide::A
			? EPokeMonsterEncounterOutcome::Victory : EPokeMonsterEncounterOutcome::Defeat;
	End.PlayerTeam = State.TeamA;
	End.OpponentTeam = State.TeamB;
	if (End.Outcome == EPokeMonsterEncounterOutcome::Captured)
	{
		End.CapturedCreature = State.CapturedCreature;
		if (End.PlayerTeam.Num() < 6)
		{
			End.PlayerTeam.Add(End.CapturedCreature);
			End.CaptureTransfer = EPokeMonsterCaptureTransfer::AddedToTeam;
		}
		else End.CaptureTransfer = EPokeMonsterCaptureTransfer::TeamFull;
	}
	End.Rounds = State.RoundNumber;
	End.SourceActor = Start.SourceActor;
	return End;
}

void UPokeMonsterEncounterSubsystem::ReleaseOverworld()
{
	if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
		World->GetTimerManager().ClearTimer(CompletionTimer);
	if (Presenter) Presenter->OnChanged.RemoveDynamic(this, &UPokeMonsterEncounterSubsystem::HandlePresenterChanged);
	if (BattleWidget) BattleWidget->RemoveFromParent();
	if (APokeMonsterPlayerCharacter* Player = ActivePlayer.Get()) Player->SetOverworldInputLocked(false);
	if (APlayerController* Controller = ActiveController.Get())
	{
		Controller->SetInputMode(FInputModeGameOnly());
		Controller->bShowMouseCursor = bPreviousMouseCursor;
	}
	BattleWidget = nullptr;
	Presenter = nullptr;
	ActiveStart = FPokeMonsterEncounterStartData();
	ActivePlayer.Reset();
	ActiveController.Reset();
	bActive = false;
}

void UPokeMonsterEncounterSubsystem::Deinitialize()
{
	if (bActive) ReleaseOverworld();
	Super::Deinitialize();
}
