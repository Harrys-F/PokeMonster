#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../UI/PokeMonsterOverworldView.h"
#include "../UI/PokeMonsterOverworldWidget.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"
#include "../Game/PokeMonsterGameMode.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "Blueprint/WidgetTree.h"
#include "Components/VerticalBox.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterOverworldUITest, "PokeMonster.Overworld.UI.Foundation",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterOverworldUITest::RunTest(const FString& Parameters)
{
	TestEqual(TEXT("Overworld GameMode installs its own controller"),
		GetDefault<APokeMonsterGameMode>()->PlayerControllerClass.Get(),
		APokeMonsterOverworldPlayerController::StaticClass());
	TStrongObjectPtr<UPokeMonsterOverworldWidget> Widget(NewObject<UPokeMonsterOverworldWidget>());
	Widget->TakeWidget();
	TestNotNull(TEXT("Compact HUD created"), Widget->GetWidgetFromName(TEXT("HudTeamRows")));
	TestNotNull(TEXT("Inventory menu button created"), Widget->GetWidgetFromName(TEXT("InventoryButton")));
	TestNotNull(TEXT("Team tab created"), Widget->GetWidgetFromName(TEXT("TeamTab")));
	TestNotNull(TEXT("Inventory tab created"), Widget->GetWidgetFromName(TEXT("InventoryTab")));
	TestNotNull(TEXT("Menu close button created"), Widget->GetWidgetFromName(TEXT("CloseButton")));

	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Item = LoadObject<UPokeMonsterItemData>(nullptr,
		TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem"));
	if (!TestNotNull(TEXT("Test species"), Species) || !TestNotNull(TEXT("Test item"), Item)) return false;
	TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
	auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 17);
	Creature.CurrentHP = 12;
	TestTrue(TEXT("Party prepared"), Encounter->RestorePersistentState({Creature}, {}, {}));
	TestTrue(TEXT("Inventory prepared"), Inventory->AddItem(Item, 4));
	const FPokeMonsterOverworldView View = FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory);
	TestEqual(TEXT("One team entry shown"), View.Team.Num(), 1);
	TestEqual(TEXT("Team name shown"), View.Team[0].Name.ToString(), Species->GetDisplayName().ToString());
	TestEqual(TEXT("Team level shown"), View.Team[0].Level, 17);
	TestEqual(TEXT("Team HP shown"), View.Team[0].CurrentHP, 12);
	TestEqual(TEXT("One inventory stack shown"), View.Inventory.Num(), 1);
	TestEqual(TEXT("Item name shown"), View.Inventory[0].Name.ToString(), Item->GetDisplayName().ToString());
	TestEqual(TEXT("Item quantity shown"), View.Inventory[0].Quantity, 4);
	Widget->UpdateView(View);
	Widget->SetMenuOpen(true, EPokeMonsterOverworldMenuSection::Inventory);
	TestTrue(TEXT("Menu opens"), Widget->IsMenuOpen());
	TestEqual(TEXT("Inventory view selectable"), Widget->GetSection(), EPokeMonsterOverworldMenuSection::Inventory);
	if (auto* Rows = Cast<UVerticalBox>(Widget->GetWidgetFromName(TEXT("MenuRows"))))
		TestEqual(TEXT("Inventory row rendered"), Rows->GetChildrenCount(), 1);
	else AddError(TEXT("Inventory rows widget missing"));
	Widget->SetBattleVisible(true);
	TestEqual(TEXT("Overworld UI hidden behind battle"), Widget->GetVisibility(), ESlateVisibility::Collapsed);
	Widget->SetBattleVisible(false);
	TestEqual(TEXT("Overworld UI restored after battle"), Widget->GetVisibility(), ESlateVisibility::SelfHitTestInvisible);
	Widget->SetMenuOpen(false);
	TestFalse(TEXT("Menu closes"), Widget->IsMenuOpen());
	Creature.CurrentHP = 0;
	Encounter->RestorePersistentState({Creature}, {}, {});
	TestTrue(TEXT("KO clearly represented"),
		FPokeMonsterOverworldViewBuilder::Build(Encounter, Inventory).Team[0].bKnockedOut);

	UWorld* TestWorld = nullptr;
	for (const FWorldContext& Context : GEngine->GetWorldContexts())
		if (Context.WorldType == EWorldType::Editor) { TestWorld = Context.World(); break; }
	if (!TestNotNull(TEXT("Editor test world"), TestWorld)) return false;
	FActorSpawnParameters Spawn;
	Spawn.ObjectFlags |= RF_Transient;
	Spawn.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	APokeMonsterPlayerCharacter* Player = TestWorld->SpawnActor<APokeMonsterPlayerCharacter>(Spawn);
	if (!TestNotNull(TEXT("Transient test player"), Player))
		return false;
	TestTrue(TEXT("Unencumbered player may open menu"),
		APokeMonsterOverworldPlayerController::CanOpenMenu(Player, Encounter, false));
	TestTrue(TEXT("Menu locks movement and interaction"),
		APokeMonsterOverworldPlayerController::TryLockMenu(Player, Encounter, false));
	TestTrue(TEXT("Player input is locked"), Player->IsOverworldInputLocked());
	TestFalse(TEXT("Open menu cannot open again"),
		APokeMonsterOverworldPlayerController::CanOpenMenu(Player, Encounter, true));
	APokeMonsterOverworldPlayerController::UnlockMenu(Player);
	TestFalse(TEXT("Closing returns movement and interaction"), Player->IsOverworldInputLocked());
	Encounter->bActive = true;
	TestFalse(TEXT("Battle prevents menu opening"),
		APokeMonsterOverworldPlayerController::CanOpenMenu(Player, Encounter, false));
	Encounter->bActive = false;
	TestWorld->DestroyActor(Player);
	return true;
}
#endif
