#include "PokeMonsterOverworldPlayerController.h"
#include "PokeMonsterControllerInput.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "Framework/Application/SlateApplication.h"
#include "Blueprint/WidgetBlueprintLibrary.h"

#include "PokeMonsterOverworldView.h"
#include "PokeMonsterDialogueWidget.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
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
 if (FSlateApplication::IsInitialized())
 {
  InputObserver = PokeMonsterControllerInput::MakeObserver();
  FSlateApplication::Get().RegisterInputPreProcessor(InputObserver, 0);
 }
	OverworldWidget = CreateWidget<UPokeMonsterOverworldWidget>(this,
		UPokeMonsterOverworldWidget::StaticClass());
	if (!OverworldWidget) return;
	OverworldWidget->SetOwnerController(this);
	OverworldWidget->AddToViewport(20);
	DialogueWidget = CreateWidget<UPokeMonsterDialogueWidget>(this,
		UPokeMonsterDialogueWidget::StaticClass());
	if (DialogueWidget)
	{
		DialogueWidget->SetOwnerController(this);
		DialogueWidget->AddToViewport(30);
	}
	if (UGameInstance* Instance = GetGameInstance())
	{
		if (UPokeMonsterEncounterSubsystem* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounter->EnsureDevPlayerParty();
			Encounter->OnEncounterStarted.AddUniqueDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterStarted);
			Encounter->OnEncounterEnded.AddUniqueDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterEnded);
		}
		if (UPokeMonsterDialogueSubsystem* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->OnDialogueChanged.AddUniqueDynamic(this,
				&APokeMonsterOverworldPlayerController::OnDialogueChanged);
	}
	bShowMouseCursor = true;
	SetInputMode(FInputModeGameAndUI());
 UWidgetBlueprintLibrary::SetFocusToGameViewport();
	GetWorldTimerManager().SetTimer(RefreshTimer, this,
		&APokeMonsterOverworldPlayerController::RefreshHUD, 0.25f, true);
	RefreshHUD();
	OnDialogueChanged();
}

void APokeMonsterOverworldPlayerController::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	GetWorldTimerManager().ClearTimer(RefreshTimer);
 if (InputObserver.IsValid() && FSlateApplication::IsInitialized())
  FSlateApplication::Get().UnregisterInputPreProcessor(InputObserver);
 InputObserver.Reset();
	if (UGameInstance* Instance = GetGameInstance())
	{
		if (UPokeMonsterEncounterSubsystem* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounter->OnEncounterStarted.RemoveDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterStarted);
			Encounter->OnEncounterEnded.RemoveDynamic(this,
				&APokeMonsterOverworldPlayerController::OnEncounterEnded);
		}
		if (UPokeMonsterDialogueSubsystem* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
		{
			Dialogues->OnDialogueChanged.RemoveDynamic(this,
				&APokeMonsterOverworldPlayerController::OnDialogueChanged);
			Dialogues->CloseDialogue();
		}
	}
	if (bMenuOpen) UnlockMenu(Cast<APokeMonsterPlayerCharacter>(GetPawn()));
	if (OverworldWidget) OverworldWidget->RemoveFromParent();
	if (DialogueWidget) DialogueWidget->RemoveFromParent();
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
 MoveMaster.Reset(); MasterPartySnapshot.Reset();
	if (OverworldWidget) OverworldWidget->SetMenuOpen(false);
	UnlockMenu(Cast<APokeMonsterPlayerCharacter>(GetPawn()));
	SetInputMode(FInputModeGameAndUI());
 UWidgetBlueprintLibrary::SetFocusToGameViewport();
	bShowMouseCursor = true;
	RefreshHUD();
	return true;
}

bool APokeMonsterOverworldPlayerController::UseMenuHealingItem(UPokeMonsterItemData* Item, int32 TeamIndex)
{
 if (!bMenuOpen || !OverworldWidget || OverworldWidget->GetSection()!=EPokeMonsterOverworldMenuSection::Team) return false;
 auto* Encounter=GetGameInstance()?GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 const bool bUsed=Encounter && Encounter->UseHealingItemOnPartyMember(Item,TeamIndex);
 if (bUsed) RefreshHUD();
 return bUsed;
}

bool APokeMonsterOverworldPlayerController::ReorderParty(const FGuid SourceInstanceId, const int32 TargetIndex)
{
	if (!bMenuOpen || !OverworldWidget || OverworldWidget->GetSection() != EPokeMonsterOverworldMenuSection::Team) return false;
	auto* Encounter = GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	if (!Encounter || !Encounter->ReorderParty(SourceInstanceId, TargetIndex)) return false;
	RefreshHUD();
	return true;
}

void APokeMonsterOverworldPlayerController::ToggleMainMenu()
{
 if (bMenuOpen) CloseMenu();
 else OpenMenu(EPokeMonsterOverworldMenuSection::Main);
}

void APokeMonsterOverworldPlayerController::ToggleMenu()
{
	if (bMenuOpen) CloseMenu();
	else OpenMenu();
}

bool APokeMonsterOverworldPlayerController::AdvanceDialogue()
{
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterDialogueSubsystem* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			return Dialogues->AdvanceDialogue();
	return false;
}

void APokeMonsterOverworldPlayerController::CloseDialogue()
{
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterDialogueSubsystem* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->CloseDialogue();
}

void APokeMonsterOverworldPlayerController::OnDialogueChanged()
{
	if (!DialogueWidget) return;
	const UGameInstance* Instance = GetGameInstance();
	const auto* Dialogues = Instance ? Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>() : nullptr;
	const auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const FPokeMonsterDialoguePage* Page = Dialogues ? Dialogues->GetCurrentPage() : nullptr;
	if (Page)
	{
		DialogueWidget->ShowPage(*Page, Dialogues->GetPageIndex(), Dialogues->GetPageCount());
		FInputModeUIOnly Input;
		Input.SetWidgetToFocus(DialogueWidget->TakeWidget());
		SetInputMode(Input);
		bShowMouseCursor = true;
		DialogueWidget->SetKeyboardFocus();
	}
	else
	{
		DialogueWidget->HideDialogue();
		if (!bMenuOpen && !(Encounter && Encounter->IsEncounterActive()))
		{
			SetInputMode(FInputModeGameAndUI());
 UWidgetBlueprintLibrary::SetFocusToGameViewport();
			bShowMouseCursor = true;
		}
	}
	RefreshHUD();
}

void APokeMonsterOverworldPlayerController::RefreshHUD()
{
	if (!OverworldWidget) return;
 if (MoveMaster.IsStale() || (MoveMaster.IsValid() && !IsMoveMasterActive())) { CloseMenu(); return; }
	UGameInstance* Instance = GetGameInstance();
	auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* Inventory = Instance ? Instance->GetSubsystem<UPokeMonsterInventorySubsystem>() : nullptr;
	auto* Quests = Instance ? Instance->GetSubsystem<UPokeMonsterQuestSubsystem>() : nullptr;
	if (Quests) Quests->RefreshProgress(Encounter, Inventory);
	OverworldWidget->SetBattleVisible(Encounter && Encounter->IsEncounterActive());
	OverworldWidget->UpdateView(FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory, Quests));
	auto* Player = Cast<APokeMonsterPlayerCharacter>(GetPawn());
	AActor* Target = Player && !Player->IsOverworldInputLocked() && !bMenuOpen
		&& !(Encounter && Encounter->IsEncounterActive())
		? Player->FindInteractableInRange() : nullptr;
	auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(Target);
 if(FocusedWild.IsValid()&&FocusedWild.Get()!=Wild)FocusedWild->SetChallengeFocused(false);
 FocusedWild=Wild;if(Wild)Wild->SetChallengeFocused(true);
 OverworldWidget->SetInteractionAvailable(Target &&
		IPokeMonsterInteractable::Execute_CanInteract(Target, Player),Wild?FString::Printf(TEXT("Interagieren · %s herausfordern"),*Wild->GetChallengeName()):FString());
}

void APokeMonsterOverworldPlayerController::OnEncounterStarted()
{
	bMenuOpen = false;
 MoveMaster.Reset(); MasterPartySnapshot.Reset();
	if (OverworldWidget)
	{
		OverworldWidget->SetMenuOpen(false);
		OverworldWidget->SetBattleVisible(true);
	}
}

void APokeMonsterOverworldPlayerController::OnEncounterEnded(const FPokeMonsterEncounterEndData& Result)
{
	if (OverworldWidget) OverworldWidget->SetBattleVisible(false);
	if (Result.Outcome != EPokeMonsterEncounterOutcome::Defeat)
	{
		SetInputMode(FInputModeGameAndUI());
 UWidgetBlueprintLibrary::SetFocusToGameViewport();
		bShowMouseCursor = true;
	}
	RefreshHUD();
}

bool APokeMonsterOverworldPlayerController::OpenMoveMaster(APokeMonsterNPC* Master)
{
 auto* Player=Cast<APokeMonsterPlayerCharacter>(GetPawn());
 if(!IsValid(Master) || !Master->CanProvideMoveService(Player) || !Master->CanInteract_Implementation(Player))return false;
 if(!OpenMenu(EPokeMonsterOverworldMenuSection::Moves))return false;
 MoveMaster=Master;
 MasterPartySnapshot=GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>()->GetPlayerParty();
 OverworldWidget->SetMoveMasterMode(true);
 return true;
}

bool APokeMonsterOverworldPlayerController::IsMoveMasterActive() const
{
 const auto* E=GetGameInstance()?GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 return bMenuOpen && MoveMaster.IsValid() && MoveMaster->CanProvideMoveService(GetPawn()) && E && !E->IsEncounterActive();
}

bool APokeMonsterOverworldPlayerController::CommitMoveMaster(FGuid CreatureId,const TArray<TSoftObjectPtr<UPokeMonsterMoveData>>& Moves)
{
 if(!IsMoveMasterActive())return false;
 const auto* Expected=MasterPartySnapshot.FindByPredicate([&](const auto& C){return C.InstanceId==CreatureId;});
 auto* E=GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
 if(!Expected || !E->CommitRememberedMoves(MoveMaster.Get(),Cast<APokeMonsterPlayerCharacter>(GetPawn()),*Expected,Moves))return false;
 CloseMenu();
 return true;
}
