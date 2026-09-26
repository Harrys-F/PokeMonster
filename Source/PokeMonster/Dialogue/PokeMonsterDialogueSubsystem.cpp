#include "PokeMonsterDialogueSubsystem.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"

bool UPokeMonsterDialogueSubsystem::IsConditionMet(const FPokeMonsterDialoguePage& Page,
	const UPokeMonsterEncounterSubsystem* Encounter)
{
	switch (Page.Condition)
	{
	case EPokeMonsterDialogueCondition::Always: return true;
	case EPokeMonsterDialogueCondition::WorldFlagSet:
		return Encounter && !Page.ConditionId.IsNone()
			&& Encounter->IsEncounterCompleted(Page.ConditionId);
	case EPokeMonsterDialogueCondition::WorldFlagUnset:
		return Encounter && !Page.ConditionId.IsNone()
			&& !Encounter->IsEncounterCompleted(Page.ConditionId);
	case EPokeMonsterDialogueCondition::TrainerDefeated:
		return Encounter && Encounter->IsTrainerDefeated(Page.ConditionId);
	case EPokeMonsterDialogueCondition::TrainerNotDefeated:
		return Encounter && !Page.ConditionId.IsNone()
			&& !Encounter->IsTrainerDefeated(Page.ConditionId);
	default: return false;
	}
}

TArray<FPokeMonsterDialoguePage> UPokeMonsterDialogueSubsystem::SelectPages(
	const UPokeMonsterDialogueData* Data, const UPokeMonsterEncounterSubsystem* Encounter)
{
	TArray<FPokeMonsterDialoguePage> Selected;
	if (!IsValid(Data)) return Selected;
	for (const FPokeMonsterDialoguePage& Page : Data->Pages)
		if (!Page.Text.IsEmpty() && IsConditionMet(Page, Encounter)) Selected.Add(Page);
	return Selected;
}

bool UPokeMonsterDialogueSubsystem::StartDialogue(APokeMonsterPlayerCharacter* Player,
	AActor* Source, const UPokeMonsterDialogueData* Data, UPokeMonsterEncounterSubsystem* Encounter)
{
	if (bActive || !IsValid(Player) || !IsValid(Source) || !IsValid(Encounter)
		|| Encounter->IsEncounterActive() || Player->IsOverworldInputLocked()) return false;
	TArray<FPokeMonsterDialoguePage> Pages = SelectPages(Data, Encounter);
	if (Pages.IsEmpty()) return false;
	ActivePages = MoveTemp(Pages);
	ActivePlayer = Player;
	ActiveSource = Source;
	ActiveEncounter = Encounter;
	PageIndex = 0;
	bActive = true;
	Player->SetOverworldInputLocked(true);
	OnDialogueChanged.Broadcast();
	return true;
}

const FPokeMonsterDialoguePage* UPokeMonsterDialogueSubsystem::GetCurrentPage() const
{
	return bActive && ActivePages.IsValidIndex(PageIndex) ? &ActivePages[PageIndex] : nullptr;
}

bool UPokeMonsterDialogueSubsystem::AdvanceDialogue()
{
	const FPokeMonsterDialoguePage* Current = GetCurrentPage();
	if (!Current) return false;
	const FPokeMonsterDialoguePage CompletedPage = *Current;
	AActor* Source = ActiveSource.Get();
	UPokeMonsterEncounterSubsystem* Encounter = ActiveEncounter.Get();
	const bool bLastPage = PageIndex + 1 >= ActivePages.Num();
	if (bLastPage) CloseDialogue();
	else { ++PageIndex; OnDialogueChanged.Broadcast(); }
	RunFollowUp(CompletedPage, Source, Encounter);
	return true;
}

void UPokeMonsterDialogueSubsystem::RunFollowUp(const FPokeMonsterDialoguePage& Page,
	AActor* Source, UPokeMonsterEncounterSubsystem* Encounter)
{
	if (Page.FollowUpId.IsNone()) return;
	if (Page.FollowUp == EPokeMonsterDialogueAction::SetWorldFlag && IsValid(Encounter))
		Encounter->MarkEncounterCompleted(Page.FollowUpId);
	else if (Page.FollowUp == EPokeMonsterDialogueAction::Custom && IsValid(Source))
		OnCustomAction.Broadcast(Source, Page.FollowUpId);
}

void UPokeMonsterDialogueSubsystem::CloseDialogue()
{
	if (!bActive) return;
	bActive = false;
	if (APokeMonsterPlayerCharacter* Player = ActivePlayer.Get())
		Player->SetOverworldInputLocked(false);
	ActivePlayer.Reset();
	ActiveSource.Reset();
	ActiveEncounter.Reset();
	ActivePages.Reset();
	PageIndex = 0;
	OnDialogueChanged.Broadcast();
}

void UPokeMonsterDialogueSubsystem::Deinitialize()
{
	CloseDialogue();
	Super::Deinitialize();
}
