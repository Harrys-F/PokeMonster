#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"

#include "../Dialogue/PokeMonsterDialogueData.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Items/PokeMonsterItemData.h"
#include "../Quest/PokeMonsterQuestData.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../UI/PokeMonsterOverworldView.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterQuestFlowTest,
	"PokeMonster.Quest.MiniSlice.FlowAndSave",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterQuestFlowTest::RunTest(const FString& Parameters)
{
	const auto* Definition = LoadObject<UPokeMonsterQuestData>(nullptr,
		TEXT("/Game/Data/Quests/DA_SliceArchiveQuest.DA_SliceArchiveQuest"));
	const auto* Guide = LoadObject<UPokeMonsterDialogueData>(nullptr,
		TEXT("/Game/Data/Dialogues/DA_SliceGuideDialogue.DA_SliceGuideDialogue"));
	if (!TestNotNull(TEXT("Quest asset loads"), Definition) || !TestNotNull(TEXT("Guide asset loads"), Guide)) return false;
	TestTrue(TEXT("Quest definition is valid"), Definition->IsConfigured());
	TestEqual(TEXT("Three ordered steps"), Definition->Objectives.Num(), 3);
	TestEqual(TEXT("Guide starts quest"), Guide->Pages[1].FollowUp, EPokeMonsterDialogueAction::StartQuest);
	TestEqual(TEXT("Guide quest ID"), Guide->Pages[1].FollowUpId, Definition->InternalId);

	TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
	auto* LookupQuests = NewObject<UPokeMonsterQuestSubsystem>(GI.Get());
	TestTrue(TEXT("Dialogue can start quest by stable ID"), LookupQuests->StartQuestById(Definition->InternalId));
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
	auto* Quests = NewObject<UPokeMonsterQuestSubsystem>(GI.Get());
	const FName QuestId = Definition->InternalId;
	TestEqual(TEXT("Initially not started"), Quests->GetStatus(QuestId), EPokeMonsterQuestStatus::NotStarted);
	if (!TestTrue(TEXT("Quest starts"), Quests->StartQuest(Definition))) return false;
	TestFalse(TEXT("Quest cannot start twice"), Quests->StartQuest(Definition));
	TestEqual(TEXT("First goal is Wanderer"), Quests->GetCurrentStep(QuestId), 0);
	auto View = FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory, Quests);
	TestEqual(TEXT("HUD quest title"), View.ActiveQuestName.ToString(), FString(TEXT("Das Siegel des Archivs")));
	TestEqual(TEXT("HUD current goal"), View.ActiveQuestObjective.ToString(), FString(TEXT("Sprich mit dem Wanderer")));
	Quests->RecordDialogue(TEXT("WrongDialogue"));
	TestEqual(TEXT("Other NPC does not progress"), Quests->GetCurrentStep(QuestId), 0);
	Quests->RecordDialogue(Guide->GetPrimaryAssetId().PrimaryAssetName);
	TestEqual(TEXT("Wanderer advances quest"), Quests->GetCurrentStep(QuestId), 1);
	FPokeMonsterDialoguePage Condition;
	Condition.Condition = EPokeMonsterDialogueCondition::QuestActive;
	Condition.ConditionId = QuestId;
	TestTrue(TEXT("Dialogue recognizes active quest"), UPokeMonsterDialogueSubsystem::IsConditionMet(Condition, Encounter, Quests));
	Encounter->MarkEncounterCompleted(TEXT("Slice_VisibleWild"));
	Quests->RefreshProgress(Encounter, Inventory);
	TestEqual(TEXT("Optional wild branch does not block or advance"), Quests->GetCurrentStep(QuestId), 1);

	auto* MidSave = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI.Get(), nullptr, Quests);
	if (!TestNotNull(TEXT("Mid-quest snapshot"), MidSave)) return false;
	TestEqual(TEXT("Save schema version"), MidSave->SaveVersion, 3);
	const FString Slot = TEXT("PokeMonster_QuestAutomation_") + FGuid::NewGuid().ToString(EGuidFormats::Digits);
	TestTrue(TEXT("Quest save written"), UGameplayStatics::SaveGameToSlot(MidSave, Slot, 0));
	auto* Loaded = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(Slot, 0));
	TestTrue(TEXT("Temporary quest save removed"), UGameplayStatics::DeleteGameInSlot(Slot, 0));
	if (!TestNotNull(TEXT("Quest save loaded"), Loaded)) return false;
	Quests->RestoreProgress({});
	TestEqual(TEXT("Runtime reset"), Quests->GetStatus(QuestId), EPokeMonsterQuestStatus::NotStarted);
	if (!TestTrue(TEXT("Quest snapshot restored"), UPokeMonsterSaveSubsystem::RestoreSnapshot(
		Loaded, Encounter, Inventory, nullptr, Quests))) return false;
	TestEqual(TEXT("Quest resumes at Liora"), Quests->GetCurrentStep(QuestId), 1);
	View = FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory, Quests);
	TestEqual(TEXT("HUD follows restored goal"), View.ActiveQuestObjective.ToString(), FString(TEXT("Bestehe Lioras Prüfung")));
	TestTrue(TEXT("Trainer victory state"), Encounter->RestorePersistentState({}, {TEXT("Slice_Liora")},
		Encounter->GetCompletedEncounterIds()));
	Quests->RefreshProgress(Encounter, Inventory);
	TestEqual(TEXT("Trainer victory advances quest"), Quests->GetCurrentStep(QuestId), 2);
	View = FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory, Quests);
	TestEqual(TEXT("HUD points to archive"), View.ActiveQuestObjective.ToString(), FString(TEXT("Untersuche den Archivstein")));
	Encounter->MarkEncounterCompleted(TEXT("Slice_ArchiveSeal"));
	Quests->RefreshProgress(Encounter, Inventory);
	TestEqual(TEXT("World flag completes quest"), Quests->GetStatus(QuestId), EPokeMonsterQuestStatus::Completed);
	Condition.Condition = EPokeMonsterDialogueCondition::QuestCompleted;
	TestTrue(TEXT("Dialogue recognizes completed quest"), UPokeMonsterDialogueSubsystem::IsConditionMet(Condition, Encounter, Quests));
	View = FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory, Quests);
	TestTrue(TEXT("HUD hides completed quest"), View.ActiveQuestName.IsEmpty());

	auto* Already = NewObject<UPokeMonsterQuestSubsystem>(GI.Get());
	TestTrue(TEXT("Already fulfilled world states"), Already->StartQuest(Definition));
	Already->RecordDialogue(Guide->GetPrimaryAssetId().PrimaryAssetName);
	Already->RefreshProgress(Encounter, Inventory);
	TestEqual(TEXT("Preexisting trainer and flag complete immediately"), Already->GetStatus(QuestId), EPokeMonsterQuestStatus::Completed);

	// The other authored objective types use their existing owners, without copying item or world state.
	auto* Item = LoadObject<UPokeMonsterItemData>(nullptr,
		TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem"));
	if (!TestNotNull(TEXT("Item definition"), Item)) return false;
	auto* Other = NewObject<UPokeMonsterQuestData>(GI.Get());
	Other->InternalId = TEXT("Quest_ObjectiveKindsTest");
	Other->DisplayName = FText::FromString(TEXT("Objective kinds"));
	for (auto Type : {EPokeMonsterQuestObjectiveType::ItemOwned,
		EPokeMonsterQuestObjectiveType::CreatureCaptured,
		EPokeMonsterQuestObjectiveType::LocationInteracted})
	{
		auto& Step = Other->Objectives.AddDefaulted_GetRef();
		Step.Type = Type;
		Step.TargetId = Type == EPokeMonsterQuestObjectiveType::ItemOwned ? Item->GetInternalId()
			: Type == EPokeMonsterQuestObjectiveType::CreatureCaptured ? FName(TEXT("TestWild")) : FName(TEXT("TestPlace"));
		Step.Description = FText::FromString(TEXT("Test objective"));
	}
	auto* OtherQuests = NewObject<UPokeMonsterQuestSubsystem>(GI.Get());
	TestTrue(TEXT("Mixed objective quest starts"), OtherQuests->StartQuest(Other));
	TestEqual(TEXT("Item goal waits"), OtherQuests->GetCurrentStep(Other->InternalId), 0);
	TestTrue(TEXT("Item added to inventory"), Inventory->AddItem(Item, 1));
	OtherQuests->RefreshProgress(Encounter, Inventory);
	TestEqual(TEXT("Item possession progresses"), OtherQuests->GetCurrentStep(Other->InternalId), 1);
	OtherQuests->RecordCapturedSpecies(TEXT("TestWild"));
	TestEqual(TEXT("Capture event progresses"), OtherQuests->GetCurrentStep(Other->InternalId), 2);
	Encounter->MarkEncounterCompleted(TEXT("TestPlace"));
	OtherQuests->RefreshProgress(Encounter, Inventory);
	TestEqual(TEXT("Location flag completes"), OtherQuests->GetStatus(Other->InternalId), EPokeMonsterQuestStatus::Completed);

	auto* Invalid = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI.Get(), nullptr, Quests);
	if (!TestNotNull(TEXT("Quest validation snapshot"), Invalid)) return false;
	Invalid->QuestProgress[0].QuestId = TEXT("MissingQuestAsset");
	AddExpectedError(TEXT("Invalid quest progress in save"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Unknown quest ID rejected before state change"),
		UPokeMonsterSaveSubsystem::RestoreSnapshot(Invalid, Encounter, Inventory, nullptr, Quests));
	TestEqual(TEXT("Quest state survives invalid save"), Quests->GetStatus(QuestId), EPokeMonsterQuestStatus::Completed);
	auto* Legacy = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI.Get(), nullptr, Quests);
	if (!TestNotNull(TEXT("Legacy migration snapshot"), Legacy)) return false;
	Legacy->SaveVersion = 2;
	Quests->RestoreProgress({});
	TestTrue(TEXT("Version 2 save migrates"), UPokeMonsterSaveSubsystem::RestoreSnapshot(
		Legacy, Encounter, Inventory, nullptr, Quests));
	TestEqual(TEXT("Old archive flag reconstructs completed quest"), Quests->GetStatus(QuestId), EPokeMonsterQuestStatus::Completed);
	return true;
}
#endif
