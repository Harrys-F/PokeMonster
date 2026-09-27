#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"

#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Dialogue/PokeMonsterDialogueData.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Encounter/PokeMonsterTrainerProfile.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Story/PokeMonsterStoryGoal.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterMiniSliceTest,
	"PokeMonster.Overworld.MiniSlice.ProgressAndSave",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterMiniSliceTest::RunTest(const FString& Parameters)
{
	const auto* Guide = LoadObject<UPokeMonsterDialogueData>(nullptr,
		TEXT("/Game/Data/Dialogues/DA_SliceGuideDialogue.DA_SliceGuideDialogue"));
	const auto* Archivist = LoadObject<UPokeMonsterDialogueData>(nullptr,
		TEXT("/Game/Data/Dialogues/DA_SliceArchivistDialogue.DA_SliceArchivistDialogue"));
	const auto* Trainer = LoadObject<UPokeMonsterTrainerProfile>(nullptr,
		TEXT("/Game/Data/Trainers/DA_SliceGuardian.DA_SliceGuardian"));
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	if (!TestNotNull(TEXT("Guide dialogue"), Guide) || !TestNotNull(TEXT("Archivist dialogue"), Archivist)
		|| !TestNotNull(TEXT("Guardian profile"), Trainer) || !TestNotNull(TEXT("Player species"), Species)) return false;
	TestEqual(TEXT("Guardian identity"), Trainer->InternalId, FName(TEXT("Slice_Liora")));
	TArray<FPokeMonsterCreatureInstance> GuardianTeam;
	TestTrue(TEXT("Guardian team is playable"), Trainer->BuildTeam(GuardianTeam));
	TestEqual(TEXT("Guardian team size"), GuardianTeam.Num(), 2);

	TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
	const FPokeMonsterCreatureInstance PlayerCreature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 20);
	if (!TestTrue(TEXT("Initial team installed"), Encounter->RestorePersistentState({PlayerCreature}, {}, {}))) return false;
	const FName GuardianId(TEXT("Slice_Liora"));
	const FName GoalFlag(TEXT("Slice_ArchiveSeal"));
	TestTrue(TEXT("Initial goal locked"), APokeMonsterStoryGoal::EvaluateState(Encounter, GuardianId, GoalFlag)
		== EPokeMonsterStoryGoalState::Locked);
	TestFalse(TEXT("Goal cannot be completed early"), APokeMonsterStoryGoal::CompleteGoal(Encounter, GuardianId, GoalFlag));
	TestEqual(TEXT("Guide before completion has two pages"),
		UPokeMonsterDialogueSubsystem::SelectPages(Guide, Encounter).Num(), 2);
	TestEqual(TEXT("Archivist before completion has two pages"),
		UPokeMonsterDialogueSubsystem::SelectPages(Archivist, Encounter).Num(), 2);

	TestTrue(TEXT("Guardian victory state installed"), Encounter->RestorePersistentState(
		{PlayerCreature}, {GuardianId}, {}));
	TestTrue(TEXT("Trainer victory unlocks goal"), APokeMonsterStoryGoal::EvaluateState(Encounter, GuardianId, GoalFlag)
		== EPokeMonsterStoryGoalState::Ready);
	TestTrue(TEXT("Goal sets world flag"), APokeMonsterStoryGoal::CompleteGoal(Encounter, GuardianId, GoalFlag));
	TestTrue(TEXT("Goal complete"), Encounter->IsEncounterCompleted(GoalFlag));
	TestFalse(TEXT("Goal does not complete twice"), APokeMonsterStoryGoal::CompleteGoal(Encounter, GuardianId, GoalFlag));
	const auto GuideAfter = UPokeMonsterDialogueSubsystem::SelectPages(Guide, Encounter);
	const auto ArchivistAfter = UPokeMonsterDialogueSubsystem::SelectPages(Archivist, Encounter);
	TestEqual(TEXT("Guide after completion has one page"), GuideAfter.Num(), 1);
	TestEqual(TEXT("Archivist after completion has one page"), ArchivistAfter.Num(), 1);
	if (GuideAfter.Num() == 1) TestTrue(TEXT("Guide reacts to success"),
		GuideAfter[0].Text.ToString().Contains(TEXT("leuchtet")));
	if (ArchivistAfter.Num() == 1) TestTrue(TEXT("Archivist reacts to success"),
		ArchivistAfter[0].Text.ToString().Contains(TEXT("lesbar")));

	auto* Save = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI.Get());
	if (!TestNotNull(TEXT("Progress snapshot"), Save)) return false;
	const FString Slot = TEXT("PokeMonster_MiniSliceAutomation_") + FGuid::NewGuid().ToString(EGuidFormats::Digits);
	TestTrue(TEXT("Progress written to disk"), UGameplayStatics::SaveGameToSlot(Save, Slot, 0));
	auto* Loaded = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(Slot, 0));
	TestTrue(TEXT("Temporary save removed"), UGameplayStatics::DeleteGameInSlot(Slot, 0));
	if (!TestNotNull(TEXT("Progress loaded from disk"), Loaded)) return false;
	TestTrue(TEXT("Runtime progress cleared"), Encounter->RestorePersistentState({PlayerCreature}, {}, {}));
	TestFalse(TEXT("Guardian cleared"), Encounter->IsTrainerDefeated(GuardianId));
	TestFalse(TEXT("Goal flag cleared"), Encounter->IsEncounterCompleted(GoalFlag));
	TestTrue(TEXT("Progress restored"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded, Encounter, Inventory));
	TestTrue(TEXT("Guardian victory restored"), Encounter->IsTrainerDefeated(GuardianId));
	TestTrue(TEXT("Goal flag restored"), Encounter->IsEncounterCompleted(GoalFlag));
	TestEqual(TEXT("Guide keeps changed dialogue after load"),
		UPokeMonsterDialogueSubsystem::SelectPages(Guide, Encounter).Num(), 1);
	return true;
}
#endif
