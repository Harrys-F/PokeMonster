#include "PokeMonsterOverworldPlayerController.h"

#include "PokeMonsterOverworldView.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "Blueprint/UserWidget.h"
#include "Engine/GameInstance.h"
#include "TimerManager.h"

bool APokeMonsterOverworldPlayerController::CanOpenMenu(
	const APokeMonsterPlayerCharacter* Player, const UPokeMonsterEncounterSubsystem* Encounter,
	const bool bAlreadyOpen)
{
	return IsValid(Player) && IsValid(Encounter) && !bAlreadyOpen
		&& !Encounter->IsEncounterActive() && !Player->IsOverworldInputLocked();
}

bool APokeMonsterOverworldPlayerController::TryLockMenu(
	APokeMonsterPlayerCharacter* Player, const UPokeMonsterEncounterSubsystem* Encounter,
	const bool bAlreadyOpen)
{
	if (!CanOpenMenu(Player, Encounter, bAlreadyOpen)) return false;
	Player->SetOverworldInputLocked(true);
	return true;
}

void APokeMonsterOverworldPlayerController::UnlockMenu(APokeMonsterPlayerCharacter* Player)
{
	if (IsValid(Player)) Player->SetOverworldInputLocked(false);
}

void APokeMonsterOverworldPlayerController::BeginPlay()
{
	Super::BeginPlay();
	if (!IsLocalController()) return;
	OverworldWidget = CreateWidget<UPokeMonsterOverworldWidget>(this,
		UPokeMonsterOverworldWidget::StaticClass());
	if (!OverworldWidget) return;
	OverworldWidget->SetOwnerController(this);
	OverworldWidget->AddToViewport(20);
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterEncounterSubsystem* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounter->EnsureDevPlayerParty();
			Encounter->OnEncounterStarted.AddUniqueDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterStarted);
			Encounter->OnEncounterEnded.AddUniqueDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterEnded);
		}
	bShowMouseCursor = true;
	SetInputMode(FInputModeGameAndUI());
	GetWorldTimerManager().SetTimer(RefreshTimer, this,
		&APokeMonsterOverworldPlayerController::RefreshHUD, 0.25f, true);
	RefreshHUD();
}

void APokeMonsterOverworldPlayerController::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	GetWorldTimerManager().ClearTimer(RefreshTimer);
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterEncounterSubsystem* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounter->OnEncounterStarted.RemoveDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterStarted);
			Encounter->OnEncounterEnded.RemoveDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterEnded);
		}
	if (bMenuOpen) UnlockMenu(Cast<APokeMonsterPlayerCharacter>(GetPawn()));
	if (OverworldWidget) OverworldWidget->RemoveFromParent();
	Super::EndPlay(EndPlayReason);
}

bool APokeMonsterOverworldPlayerController::OpenMenu(const EPokeMonsterOverworldMenuSection InitialSection)
{
	if (!OverworldWidget) return false;
	auto* Player = Cast<APokeMonsterPlayerCharacter>(GetPawn());
	const UGameInstance* Instance = GetGameInstance();
	const auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	if (!TryLockMenu(Player, Encounter, bMenuOpen)) return false;
	bMenuOpen = true;
	RefreshHUD();
	OverworldWidget->SetMenuOpen(true, InitialSection);
	FInputModeUIOnly Input;
	Input.SetWidgetToFocus(OverworldWidget->TakeWidget());
	SetInputMode(Input);
	bShowMouseCursor = true;
	OverworldWidget->SetKeyboardFocus();
	return true;
}

bool APokeMonsterOverworldPlayerController::CloseMenu()
{
	if (!bMenuOpen) return false;
	bMenuOpen = false;
	if (OverworldWidget) OverworldWidget->SetMenuOpen(false);
	UnlockMenu(Cast<APokeMonsterPlayerCharacter>(GetPawn()));
	SetInputMode(FInputModeGameAndUI());
	bShowMouseCursor = true;
	RefreshHUD();
	return true;
}

void APokeMonsterOverworldPlayerController::ToggleMenu()
{
	if (bMenuOpen) CloseMenu();
	else OpenMenu();
}

void APokeMonsterOverworldPlayerController::RefreshHUD()
{
	if (!OverworldWidget) return;
	const UGameInstance* Instance = GetGameInstance();
	const auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* Inventory = Instance ? Instance->GetSubsystem<UPokeMonsterInventorySubsystem>() : nullptr;
	OverworldWidget->SetBattleVisible(Encounter && Encounter->IsEncounterActive());
	OverworldWidget->UpdateView(FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory));
	auto* Player = Cast<APokeMonsterPlayerCharacter>(GetPawn());
	AActor* Target = Player && !bMenuOpen && !(Encounter && Encounter->IsEncounterActive())
		? Player->FindInteractableInRange() : nullptr;
	OverworldWidget->SetInteractionAvailable(Target &&
		IPokeMonsterInteractable::Execute_CanInteract(Target, Player));
}

void APokeMonsterOverworldPlayerController::OnEncounterStarted()
{
	bMenuOpen = false;
	if (OverworldWidget)
	{
		OverworldWidget->SetMenuOpen(false);
		OverworldWidget->SetBattleVisible(true);
	}
}

void APokeMonsterOverworldPlayerController::OnEncounterEnded(const FPokeMonsterEncounterEndData& Result)
{
	if (OverworldWidget) OverworldWidget->SetBattleVisible(false);
	SetInputMode(FInputModeGameAndUI());
	bShowMouseCursor = true;
	RefreshHUD();
}
