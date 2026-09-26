#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Dialogue/PokeMonsterDialogueData.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../UI/PokeMonsterDialogueWidget.h"
#include "Blueprint/WidgetTree.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterDialogueTest, "PokeMonster.Dialogue.PagesAndState",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterDialogueTest::RunTest(const FString& Parameters)
{
	TStrongObjectPtr<UPokeMonsterDialogueWidget> Widget(NewObject<UPokeMonsterDialogueWidget>());
	Widget->TakeWidget();
	TestNotNull(TEXT("Dialogue box speaker label"), Widget->GetWidgetFromName(TEXT("SpeakerName")));
	TestNotNull(TEXT("Dialogue box text label"), Widget->GetWidgetFromName(TEXT("DialogueText")));
	TestNotNull(TEXT("Dialogue box next button"), Widget->GetWidgetFromName(TEXT("AdvanceButton")));
	TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
	auto* Dialogues = NewObject<UPokeMonsterDialogueSubsystem>(GI.Get());
	TStrongObjectPtr<UPokeMonsterDialogueData> Pages(NewObject<UPokeMonsterDialogueData>());
	FPokeMonsterDialoguePage First;
	First.SpeakerName = FText::FromString(TEXT("Wanderer"));
	First.Text = FText::FromString(TEXT("Ein erster Satz."));
	Pages->Pages.Add(First);
	FPokeMonsterDialoguePage Second = First;
	Second.Text = FText::FromString(TEXT("Ein zweiter Satz."));
	Pages->Pages.Add(Second);
	TestEqual(TEXT("Two eligible pages"),
		UPokeMonsterDialogueSubsystem::SelectPages(Pages.Get(), Encounter).Num(), 2);

	UWorld* World = nullptr;
	for (const FWorldContext& Context : GEngine->GetWorldContexts())
		if (Context.WorldType == EWorldType::Editor) { World = Context.World(); break; }
	if (!TestNotNull(TEXT("Editor test world"), World)) return false;
	FActorSpawnParameters Spawn;
	Spawn.ObjectFlags |= RF_Transient;
	Spawn.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	auto* Player = World->SpawnActor<APokeMonsterPlayerCharacter>(Spawn);
	auto* NPC = World->SpawnActor<APokeMonsterNPC>(Spawn);
	if (!TestNotNull(TEXT("Test player"), Player) || !TestNotNull(TEXT("Reusable NPC"), NPC))
	{
		if (Player) World->DestroyActor(Player);
		if (NPC) World->DestroyActor(NPC);
		return false;
	}
	TestTrue(TEXT("NPC uses common interaction interface"), NPC->Implements<UPokeMonsterInteractable>());
	TestTrue(TEXT("Dialogue starts"), Dialogues->StartDialogue(Player, NPC, Pages.Get(), Encounter));
	TestTrue(TEXT("Movement and world interaction locked"), Player->IsOverworldInputLocked());
	TestFalse(TEXT("A second dialogue cannot interrupt"), Dialogues->StartDialogue(Player, NPC, Pages.Get(), Encounter));
	TestEqual(TEXT("First page selected"), Dialogues->GetPageIndex(), 0);
	TestTrue(TEXT("Next page works"), Dialogues->AdvanceDialogue());
	TestEqual(TEXT("Second page selected"), Dialogues->GetPageIndex(), 1);
	TestEqual(TEXT("Second page text"), Dialogues->GetCurrentPage()->Text.ToString(),
		FString(TEXT("Ein zweiter Satz.")));
	TestTrue(TEXT("Last page closes"), Dialogues->AdvanceDialogue());
	TestFalse(TEXT("Dialogue inactive after final page"), Dialogues->IsDialogueActive());
	TestFalse(TEXT("Movement and interaction restored"), Player->IsOverworldInputLocked());

	TStrongObjectPtr<UPokeMonsterDialogueData> StatePages(NewObject<UPokeMonsterDialogueData>());
	FPokeMonsterDialoguePage Before;
	Before.SpeakerName = First.SpeakerName;
	Before.Text = FText::FromString(TEXT("Wir kennen uns noch nicht."));
	Before.Condition = EPokeMonsterDialogueCondition::WorldFlagUnset;
	Before.ConditionId = TEXT("Dev_NPCMet");
	Before.FollowUp = EPokeMonsterDialogueAction::SetWorldFlag;
	Before.FollowUpId = TEXT("Dev_NPCMet");
	StatePages->Pages.Add(Before);
	FPokeMonsterDialoguePage After = Before;
	After.Text = FText::FromString(TEXT("Schön, dich wiederzusehen."));
	After.Condition = EPokeMonsterDialogueCondition::WorldFlagSet;
	After.FollowUp = EPokeMonsterDialogueAction::None;
	After.FollowUpId = NAME_None;
	StatePages->Pages.Add(After);
	TestTrue(TEXT("First stateful conversation starts"),
		Dialogues->StartDialogue(Player, NPC, StatePages.Get(), Encounter));
	TestEqual(TEXT("Unset flag text shown"), Dialogues->GetCurrentPage()->Text.ToString(),
		Before.Text.ToString());
	Dialogues->AdvanceDialogue();
	TestTrue(TEXT("Follow-up writes existing persistent world flag"),
		Encounter->IsEncounterCompleted(TEXT("Dev_NPCMet")));
	TestTrue(TEXT("Stateful NPC can be addressed again"),
		Dialogues->StartDialogue(Player, NPC, StatePages.Get(), Encounter));
	TestEqual(TEXT("Set flag text shown"), Dialogues->GetCurrentPage()->Text.ToString(),
		After.Text.ToString());
	Dialogues->CloseDialogue();
	TestFalse(TEXT("Manual close restores input"), Player->IsOverworldInputLocked());
	Player->SetOverworldInputLocked(true);
	TestFalse(TEXT("Locked Overworld rejects dialogue start"),
		Dialogues->StartDialogue(Player, NPC, Pages.Get(), Encounter));
	Player->SetOverworldInputLocked(false);
	World->DestroyActor(NPC);
	World->DestroyActor(Player);
	return true;
}
#endif
