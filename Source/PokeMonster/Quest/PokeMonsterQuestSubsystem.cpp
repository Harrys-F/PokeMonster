#include "PokeMonsterQuestSubsystem.h"

#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Engine/AssetManager.h"
#include "Engine/GameInstance.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterQuest, Log, All);

void UPokeMonsterQuestSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	Collection.InitializeDependency<UPokeMonsterEncounterSubsystem>();
	if (auto* Encounter = GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>())
	{
		Encounter->OnEncounterEnded.AddUniqueDynamic(this, &UPokeMonsterQuestSubsystem::HandleEncounterEnded);
	}
}

void UPokeMonsterQuestSubsystem::HandleEncounterEnded(const FPokeMonsterEncounterEndData& Result)
{
	if (Result.Outcome == EPokeMonsterEncounterOutcome::Captured)
		if (const auto* Species = Result.CapturedCreature.Species.LoadSynchronous())
			RecordCapturedSpecies(Species->GetInternalId());
	HandlePersistentStateRestored();
}

void UPokeMonsterQuestSubsystem::HandlePersistentStateRestored()
{
	if (UGameInstance* GI = GetGameInstance())
		RefreshProgress(GI->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
			GI->GetSubsystem<UPokeMonsterInventorySubsystem>());
}

const UPokeMonsterQuestData* UPokeMonsterQuestSubsystem::ResolveDefinition(FName QuestId) const
{
	for (const UPokeMonsterQuestData* Data : RuntimeDefinitions)
		if (IsValid(Data) && Data->InternalId == QuestId) return Data;
	TArray<FPrimaryAssetId> Ids;
	UAssetManager::Get().GetPrimaryAssetIdList(TEXT("Quest"), Ids);
	for (const FPrimaryAssetId& Id : Ids)
	{
		const FSoftObjectPath Path = UAssetManager::Get().GetPrimaryAssetPath(Id);
		const auto* Data = Path.IsValid() ? Cast<UPokeMonsterQuestData>(Path.TryLoad()) : nullptr;
		if (IsValid(Data) && Data->InternalId == QuestId) return Data;
	}
	return nullptr;
}

const UPokeMonsterQuestData* UPokeMonsterQuestSubsystem::GetDefinition(FName QuestId) const
{
	return ResolveDefinition(QuestId);
}

bool UPokeMonsterQuestSubsystem::StartQuestById(FName QuestId)
{
	return StartQuest(ResolveDefinition(QuestId));
}

bool UPokeMonsterQuestSubsystem::StartQuest(const UPokeMonsterQuestData* Definition)
{
	if (!IsValid(Definition) || !Definition->IsConfigured() || GetStatus(Definition->InternalId) != EPokeMonsterQuestStatus::NotStarted)
		return false;
	for (FName Prerequisite : Definition->PrerequisiteQuestIds)
		if (GetStatus(Prerequisite) != EPokeMonsterQuestStatus::Completed) return false;
	RuntimeDefinitions.AddUnique(const_cast<UPokeMonsterQuestData*>(Definition));
	FPokeMonsterQuestProgress& State = Progress.AddDefaulted_GetRef();
	State.QuestId = Definition->InternalId;
	State.Status = EPokeMonsterQuestStatus::Active;
	RefreshProgress(GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr,
		GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterInventorySubsystem>() : nullptr);
	return true;
}

EPokeMonsterQuestStatus UPokeMonsterQuestSubsystem::GetStatus(FName QuestId) const
{
	for (const auto& State : Progress) if (State.QuestId == QuestId) return State.Status;
	return EPokeMonsterQuestStatus::NotStarted;
}

int32 UPokeMonsterQuestSubsystem::GetCurrentStep(FName QuestId) const
{
	for (const auto& State : Progress) if (State.QuestId == QuestId) return State.CurrentStep;
	return 0;
}

const UPokeMonsterQuestData* UPokeMonsterQuestSubsystem::GetActiveMainQuest() const
{
	for (const auto& State : Progress)
		if (State.Status == EPokeMonsterQuestStatus::Active)
			if (const auto* Data = ResolveDefinition(State.QuestId))
				if (Data->QuestType == EPokeMonsterQuestType::MainStory) return Data;
	return nullptr;
}

bool UPokeMonsterQuestSubsystem::IsSatisfied(const FPokeMonsterQuestObjective& Objective,
	const UPokeMonsterEncounterSubsystem* Encounter, const UPokeMonsterInventorySubsystem* Inventory) const
{
	switch (Objective.Type)
	{
	case EPokeMonsterQuestObjectiveType::TrainerDefeated:
		return Encounter && Encounter->IsTrainerDefeated(Objective.TargetId);
	case EPokeMonsterQuestObjectiveType::WorldFlagSet:
	case EPokeMonsterQuestObjectiveType::LocationInteracted:
		return Encounter && Encounter->IsEncounterCompleted(Objective.TargetId);
	case EPokeMonsterQuestObjectiveType::CreatureCaptured:
		return CapturedSpeciesIds.Contains(Objective.TargetId);
	case EPokeMonsterQuestObjectiveType::ItemOwned:
		if (Inventory)
			for (const auto& Stack : Inventory->GetStacks())
				if (const auto* Item = Stack.Item.LoadSynchronous())
					if (Item->GetInternalId() == Objective.TargetId && Stack.Quantity > 0) return true;
		return false;
	default: return false;
	}
}

void UPokeMonsterQuestSubsystem::Advance(UPokeMonsterEncounterSubsystem* Encounter)
{
	for (auto& State : Progress)
	{
		if (State.Status != EPokeMonsterQuestStatus::Active) continue;
		const auto* Data = ResolveDefinition(State.QuestId);
		if (!Data || State.CurrentStep < Data->Objectives.Num()) continue;
		State.Status = EPokeMonsterQuestStatus::Completed;
		if (Encounter && !Data->CompletionFlag.IsNone()) Encounter->MarkEncounterCompleted(Data->CompletionFlag);
		UE_LOG(LogPokeMonsterQuest, Display, TEXT("Quest completed: %s"), *State.QuestId.ToString());
	}
}

void UPokeMonsterQuestSubsystem::RefreshProgress(UPokeMonsterEncounterSubsystem* Encounter,
	const UPokeMonsterInventorySubsystem* Inventory)
{
	for (auto& State : Progress)
	{
		if (State.Status != EPokeMonsterQuestStatus::Active) continue;
		const auto* Data = ResolveDefinition(State.QuestId);
		if (!Data) continue;
		while (Data->Objectives.IsValidIndex(State.CurrentStep)
			&& IsSatisfied(Data->Objectives[State.CurrentStep], Encounter, Inventory)) ++State.CurrentStep;
	}
	Advance(Encounter);
}

void UPokeMonsterQuestSubsystem::RecordDialogue(FName DialogueId)
{
	if (DialogueId.IsNone()) return;
	for (auto& State : Progress)
	{
		const auto* Data = ResolveDefinition(State.QuestId);
		if (State.Status == EPokeMonsterQuestStatus::Active && Data && Data->Objectives.IsValidIndex(State.CurrentStep))
		{
			const auto& Step = Data->Objectives[State.CurrentStep];
			if (Step.Type == EPokeMonsterQuestObjectiveType::TalkToNPC && Step.TargetId == DialogueId) ++State.CurrentStep;
		}
	}
	RefreshProgress(GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr,
		GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterInventorySubsystem>() : nullptr);
}

void UPokeMonsterQuestSubsystem::RecordCapturedSpecies(FName SpeciesId)
{
	if (SpeciesId.IsNone()) return;
	CapturedSpeciesIds.Add(SpeciesId);
	RefreshProgress(GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr,
		GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterInventorySubsystem>() : nullptr);
}

bool UPokeMonsterQuestSubsystem::ValidateSavedProgress(const TArray<FPokeMonsterQuestProgress>& Saved) const
{
	TSet<FName> Seen;
	for (const auto& State : Saved)
	{
		const auto* Data = ResolveDefinition(State.QuestId);
		if (!Data || !Data->IsConfigured() || Seen.Contains(State.QuestId)
			|| (State.Status != EPokeMonsterQuestStatus::Active && State.Status != EPokeMonsterQuestStatus::Completed)
			|| State.CurrentStep < 0 || State.CurrentStep > Data->Objectives.Num()
			|| (State.Status == EPokeMonsterQuestStatus::Completed) != (State.CurrentStep == Data->Objectives.Num()))
			return false;
		Seen.Add(State.QuestId);
	}
	return true;
}

void UPokeMonsterQuestSubsystem::RestoreProgress(const TArray<FPokeMonsterQuestProgress>& Saved)
{
	Progress = Saved;
}

void UPokeMonsterQuestSubsystem::MigrateLegacyMiniSlice(const UPokeMonsterEncounterSubsystem* Encounter)
{
	if (!Encounter) return;
	const bool bSeal = Encounter->IsEncounterCompleted(TEXT("Slice_ArchiveSeal"));
	const bool bLiora = Encounter->IsTrainerDefeated(TEXT("Slice_Liora"));
	if (!bSeal && !bLiora) return;
	const auto* Data = ResolveDefinition(TEXT("Slice_ArchiveQuest"));
	if (!Data || Data->Objectives.Num() != 3) return;
	FPokeMonsterQuestProgress& State = Progress.AddDefaulted_GetRef();
	State.QuestId = Data->InternalId;
	State.CurrentStep = bSeal ? Data->Objectives.Num() : 2;
	State.Status = bSeal ? EPokeMonsterQuestStatus::Completed : EPokeMonsterQuestStatus::Active;
}

void UPokeMonsterQuestSubsystem::Deinitialize()
{
	if (UGameInstance* GI = GetGameInstance())
		if (auto* Encounter = GI->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounter->OnEncounterEnded.RemoveDynamic(this, &UPokeMonsterQuestSubsystem::HandleEncounterEnded);
		}
	Progress.Reset(); RuntimeDefinitions.Reset(); CapturedSpeciesIds.Reset();
	Super::Deinitialize();
}
