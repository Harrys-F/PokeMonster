#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/GameInstance.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSaveSnapshotTest, "PokeMonster.Save.SnapshotAndDisk",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterSaveSnapshotTest::RunTest(const FString& Parameters)
{
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	auto* Item = LoadObject<UPokeMonsterItemData>(nullptr,
		TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem"));
	if (!TestNotNull(TEXT("Species"), Species) || !TestNotNull(TEXT("Move"), Move)
		|| !TestNotNull(TEXT("Item"), Item)) return false;
	auto* GI = NewObject<UGameInstance>();
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI);
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI);
	auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 20);
	TestTrue(TEXT("Move assigned"), Creature.AssignMove(0, Move));
	TestTrue(TEXT("PP spent"), Creature.ConsumeMovePP(0, 4));
	Creature.CurrentHP -= 9;
	TestTrue(TEXT("Experience gained"), Creature.AddExperience(19).bSucceeded);
	const FGuid Id = Creature.InstanceId;
	const int32 HP = Creature.CurrentHP;
	const int32 PP = Creature.GetMoveSlots()[0].GetCurrentPP();
	const int64 XP = Creature.Experience;
	TestTrue(TEXT("Party set"), Encounter->RestorePersistentState({Creature},
		{TEXT("DevTrainer_SaveTest")}, {TEXT("Dev_VisibleWild")}));
	TestTrue(TEXT("Inventory set"), Inventory->AddItem(Item, 7));
	auto* Save = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI);
	if (!TestNotNull(TEXT("Snapshot captured"), Save)) return false;
	TestEqual(TEXT("Save schema version"), Save->SaveVersion, UPokeMonsterSaveGame::CurrentVersion);
	TestEqual(TEXT("Species stored as ID"), Save->PlayerTeam[0].SpeciesId, Species->GetPrimaryAssetId());
	TestEqual(TEXT("Move stored as ID"), Save->PlayerTeam[0].Moves[0].MoveId, Move->GetPrimaryAssetId());
	TestEqual(TEXT("Item stored as ID"), Save->InventoryStacks[0].ItemId, Item->GetPrimaryAssetId());

	const FString Slot = TEXT("PokeMonster_SaveAutomation_") + FGuid::NewGuid().ToString(EGuidFormats::Digits);
	TestFalse(TEXT("Missing save reported"), UGameplayStatics::DoesSaveGameExist(Slot, 0));
	TestTrue(TEXT("Save file created"), UGameplayStatics::SaveGameToSlot(Save, Slot, 0));
	TestTrue(TEXT("Save file exists"), UGameplayStatics::DoesSaveGameExist(Slot, 0));
	auto* Loaded = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(Slot, 0));
	TestTrue(TEXT("Temporary test save removed"), UGameplayStatics::DeleteGameInSlot(Slot, 0));
	if (!TestNotNull(TEXT("Save file decoded"), Loaded)) return false;
	TestEqual(TEXT("On-disk save version"), Loaded->SaveVersion, UPokeMonsterSaveGame::CurrentVersion);
	TestTrue(TEXT("Party cleared"), Encounter->RestorePersistentState({}, {}, {}));
	TestTrue(TEXT("Inventory cleared"), Inventory->RestoreStacks({}));
	TestTrue(TEXT("Snapshot restored"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded, Encounter, Inventory));
	const auto& Team = Encounter->GetPlayerParty();
	if (!TestEqual(TEXT("Team count restored"), Team.Num(), 1)) return false;
	TestEqual(TEXT("Instance identity restored"), Team[0].InstanceId, Id);
	TestEqual(TEXT("Level restored"), Team[0].Level, 20);
	TestEqual(TEXT("HP restored"), Team[0].CurrentHP, HP);
	TestEqual(TEXT("XP restored"), Team[0].Experience, XP);
	TestEqual(TEXT("PP restored"), Team[0].GetMoveSlots()[0].GetCurrentPP(), PP);
	TestEqual(TEXT("Inventory restored"), Inventory->GetQuantity(Item), 7);
	TestTrue(TEXT("Trainer defeat restored"), Encounter->IsTrainerDefeated(TEXT("DevTrainer_SaveTest")));
	TestTrue(TEXT("World flag restored"), Encounter->IsEncounterCompleted(TEXT("Dev_VisibleWild")));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSaveRejectTest, "PokeMonster.Save.RejectInvalidData",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterSaveRejectTest::RunTest(const FString& Parameters)
{
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Item = LoadObject<UPokeMonsterItemData>(nullptr,
		TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	if (!TestNotNull(TEXT("Species"), Species) || !TestNotNull(TEXT("Item"), Item)
		|| !TestNotNull(TEXT("Move"), Move)) return false;
	auto* GI = NewObject<UGameInstance>();
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI);
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI);
	auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 10);
	TestTrue(TEXT("Move assigned"), Creature.AssignMove(0, Move));
	TestTrue(TEXT("Initial team"), Encounter->RestorePersistentState({Creature}, {TEXT("SafeTrainer")}, {}));
	TestTrue(TEXT("Initial inventory"), Inventory->AddItem(Item, 2));
	auto* Save = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI);
	if (!TestNotNull(TEXT("Baseline snapshot"), Save)) return false;
	Save->SaveVersion = UPokeMonsterSaveGame::CurrentVersion + 1;
	AddExpectedError(TEXT("Unsupported save version"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Future schema rejected"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Save, Encounter, Inventory));
	Save->SaveVersion = 0;
	AddExpectedError(TEXT("Unsupported save version"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Old schema without migration rejected"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Save, Encounter, Inventory));
	Save->SaveVersion = UPokeMonsterSaveGame::CurrentVersion;
	Save->PlayerTeam[0].SpeciesId = FPrimaryAssetId(TEXT("CreatureSpecies"), TEXT("MissingSaveSpecies"));
	AddExpectedError(TEXT("Missing or mismatched asset"), EAutomationExpectedErrorFlags::Contains, 1);
	AddExpectedError(TEXT("Invalid creature in save"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Unknown species rejected"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Save, Encounter, Inventory));
	Save->PlayerTeam[0].SpeciesId = Species->GetPrimaryAssetId();
	Save->PlayerTeam[0].Moves[0].MoveId = FPrimaryAssetId(TEXT("CreatureMove"), TEXT("MissingSaveMove"));
	AddExpectedError(TEXT("Missing or mismatched asset"), EAutomationExpectedErrorFlags::Contains, 1);
	AddExpectedError(TEXT("Invalid creature in save"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Unknown move rejected"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Save, Encounter, Inventory));
	Save->PlayerTeam[0].Moves[0].MoveId = Move->GetPrimaryAssetId();
	Save->InventoryStacks[0].ItemId = FPrimaryAssetId(TEXT("Item"), TEXT("MissingSaveItem"));
	AddExpectedError(TEXT("Missing or mismatched asset"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Unknown item rejected"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Save, Encounter, Inventory));
	Save->InventoryStacks[0].ItemId = Item->GetPrimaryAssetId();
	Save->PlayerTeam[0].Moves[0].CurrentPP = Move->MaxPP + 1;
	AddExpectedError(TEXT("Invalid creature in save"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Invalid PP rejected"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Save, Encounter, Inventory));
	TestEqual(TEXT("Team unchanged after rejection"), Encounter->GetPlayerParty()[0].InstanceId, Creature.InstanceId);
	TestEqual(TEXT("Inventory unchanged after rejection"), Inventory->GetQuantity(Item), 2);
	TestTrue(TEXT("Trainer state unchanged"), Encounter->IsTrainerDefeated(TEXT("SafeTrainer")));
	return true;
}
#endif
