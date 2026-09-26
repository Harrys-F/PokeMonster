#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "Engine/AssetManager.h"
#include "Engine/GameInstance.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterInventoryTest, "PokeMonster.Items.InventoryAndUsage",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterInventoryTest::RunTest(const FString& Parameters)
{
	auto* Capture = LoadObject<UPokeMonsterItemData>(nullptr, TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem"));
	auto* Healing = LoadObject<UPokeMonsterItemData>(nullptr, TEXT("/Game/Data/Items/DA_TestHealingItem.DA_TestHealingItem"));
	auto* Evolution = LoadObject<UPokeMonsterItemData>(nullptr, TEXT("/Game/Data/Items/DA_TestEvolutionItem.DA_TestEvolutionItem"));
	auto* Water = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Grass = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	if (!TestNotNull(TEXT("Capture item loads"), Capture) || !TestNotNull(TEXT("Healing item loads"), Healing)
		|| !TestNotNull(TEXT("Evolution item loads"), Evolution) || !TestNotNull(TEXT("Water loads"), Water)
		|| !TestNotNull(TEXT("Grass loads"), Grass) || !TestNotNull(TEXT("Move loads"), Move)) return false;
	for (const auto* Item : {Capture, Healing, Evolution})
	{
		TestTrue(TEXT("Item configured"), Item->IsConfigured());
		TestEqual(TEXT("Item scanned for cooking"), UAssetManager::Get().GetPrimaryAssetPath(Item->GetPrimaryAssetId()), FSoftObjectPath(Item));
		TestFalse(TEXT("Item has description"), Item->GetDescription().IsEmpty());
	}
	TestEqual(TEXT("Capture category"), Capture->GetCategory(), EPokeMonsterItemCategory::Capture);
	TestEqual(TEXT("Healing category"), Healing->GetCategory(), EPokeMonsterItemCategory::Healing);
	TestEqual(TEXT("Evolution category"), Evolution->GetCategory(), EPokeMonsterItemCategory::Evolution);
	TestTrue(TEXT("Capture has original device"), Capture->GetCaptureDevice() != nullptr);

	auto* GameInstance = NewObject<UGameInstance>();
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GameInstance);
	const int32 StackLimit = Capture->GetMaxStackSize();
	TestFalse(TEXT("Negative add rejected"), Inventory->AddItem(Capture, -1));
	TestTrue(TEXT("Add crosses stack boundary"), Inventory->AddItem(Capture, StackLimit + 3));
	TestEqual(TEXT("Total quantity counted"), Inventory->GetQuantity(Capture), StackLimit + 3);
	TestEqual(TEXT("Multiple stacks created"), Inventory->GetStacks().Num(), 2);
	for (const auto& Stack : Inventory->GetStacks())
		TestTrue(TEXT("Every stack respects item limit"), Stack.Quantity > 0 && Stack.Quantity <= StackLimit);
	TestFalse(TEXT("Over-removal rejected atomically"), Inventory->RemoveItem(Capture, StackLimit + 4));
	TestEqual(TEXT("Rejected removal keeps stock"), Inventory->GetQuantity(Capture), StackLimit + 3);
	TestTrue(TEXT("Remove across stacks"), Inventory->RemoveItem(Capture, 4));
	TestEqual(TEXT("Removal adjusts count"), Inventory->GetQuantity(Capture), StackLimit - 1);
	TestTrue(TEXT("Remove remaining stock"), Inventory->RemoveItem(Capture, StackLimit - 1));
	TestFalse(TEXT("Empty inventory has no capture item"), Inventory->HasItem(Capture));

	auto Player = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, 20);
	auto Wild = FPokeMonsterCreatureInstance::CreateFromSpecies(Grass, 5);
	Player.AssignMove(0, Move); Wild.AssignMove(0, Move);
	auto* Presenter = NewObject<UPokeMonsterBattlePresenter>();
	TestTrue(TEXT("Wild battle starts with empty inventory"), Presenter->InitializeTeamBattle({Player}, {Wild}, 1, true, Inventory));
	TestFalse(TEXT("No capture action without item"), Presenter->GetView().bCaptureEnabled);
	TestFalse(TEXT("No-item capture selection rejected"), Presenter->TrySelectCapture());
	TestEqual(TEXT("Rejected capture does not advance battle"), Presenter->GetBattleState()->RoundNumber, 0);
	TestTrue(TEXT("One capture item added"), Inventory->AddItem(Capture, 1));
	TestTrue(TEXT("Same session can select stocked capture"), Presenter->TrySelectCapture());
	TestTrue(TEXT("Capture attempt resolves"), Presenter->ResolveSelection());
	TestEqual(TEXT("Exactly one item consumed"), Inventory->GetQuantity(Capture), 0);
	Presenter->FinishPresentation();
	TestTrue(TEXT("Second encounter starts with same inventory"), Presenter->InitializeTeamBattle({Player}, {Wild}, 2, true, Inventory));
	TestFalse(TEXT("Second encounter cannot capture without restock"), Presenter->TrySelectCapture());
	TestTrue(TEXT("Stock can be restored through a savegame handoff"), Inventory->AddItem(Capture, 2));
	auto* Restored = NewObject<UPokeMonsterInventorySubsystem>(GameInstance);
	TestTrue(TEXT("Inventory snapshot restores"), Restored->RestoreStacks(Inventory->GetStacks()));
	TestEqual(TEXT("Restored capture quantity"), Restored->GetQuantity(Capture), 2);

	auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, 20);
	Creature.CurrentHP = Creature.GetMaxHP() - 12;
	TestTrue(TEXT("Healing item added"), Inventory->AddItem(Healing, 1));
	TestTrue(TEXT("Overworld healing succeeds"), Inventory->UseHealingItem(Healing, Creature));
	TestEqual(TEXT("Healing clamps at maximum HP"), Creature.CurrentHP, Creature.GetMaxHP());
	TestEqual(TEXT("Healing consumes one item"), Inventory->GetQuantity(Healing), 0);
	TestTrue(TEXT("Another healing item added"), Inventory->AddItem(Healing, 1));
	TestFalse(TEXT("Full HP cannot waste healing item"), Inventory->UseHealingItem(Healing, Creature));
	TestEqual(TEXT("Unused healing item retained"), Inventory->GetQuantity(Healing), 1);

	FPokeMonsterEvolutionData Rule;
	Rule.TargetSpecies = Grass->GetPrimaryAssetId();
	Rule.Trigger = EPokeMonsterEvolutionTrigger::Item;
	Rule.RequiredItemId = Evolution->GetInternalId();
	FPokeMonsterEvolutionContext Context;
	Context.Trigger = EPokeMonsterEvolutionTrigger::Item;
	Context.UsedItemId = Evolution->GetInternalId();
	TestTrue(TEXT("Evolution item ID satisfies existing eligibility check"),
		UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule, Creature.Level, Context));
	Context.UsedItemId = Capture->GetInternalId();
	TestFalse(TEXT("Wrong item does not satisfy evolution"),
		UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule, Creature.Level, Context));
	return true;
}
#endif
