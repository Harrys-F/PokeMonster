#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "Engine/GameInstance.h"
#include "HAL/PlatformFileManager.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Misc/ScopeExit.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCheckpointSaveGuardTest,
	"PokeMonster.Save.DefeatTransitionGuard",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterCheckpointSaveGuardTest::RunTest(const FString& Parameters)
{
	auto* GI = NewObject<UGameInstance>();
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI);
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI);
	auto* Checkpoint = NewObject<UPokeMonsterCheckpointSubsystem>(GI);
	TestFalse(TEXT("No false saved status"), Checkpoint->WasLastRecoverySaved());
	Checkpoint->bReturning = true;
	TestNull(TEXT("Unfinished defeat cannot be saved"), UPokeMonsterSaveSubsystem::CaptureSnapshot(
		Encounter, Inventory, GI, Checkpoint));
	TestFalse(TEXT("Checkpoint cannot change during return"), Checkpoint->RestoreCheckpoint({}));
	Checkpoint->bReturning = false;
	TestNotNull(TEXT("Finished return allows snapshot"), UPokeMonsterSaveSubsystem::CaptureSnapshot(
		Encounter, Inventory, GI, Checkpoint));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterAtomicSaveTest,
	"PokeMonster.Save.VerifiedAtomicReplacement",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterAtomicSaveTest::RunTest(const FString& Parameters)
{
	const FString Slot = TEXT("PokeMonster_AtomicAutomation_") + FGuid::NewGuid().ToString(EGuidFormats::Digits);
	const FString Path = FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir() / TEXT("SaveGames") / (Slot + TEXT(".sav")));
	const FString BlockedSlot = Slot + TEXT("_Blocked");
	const FString BlockedPath = FPaths::GetPath(Path) / (BlockedSlot + TEXT(".sav"));
	IPlatformFile& Files = FPlatformFileManager::Get().GetPlatformPhysical();
	ON_SCOPE_EXIT { Files.DeleteFile(*Path); Files.DeleteDirectory(*BlockedPath); };
	auto* Save = NewObject<UPokeMonsterSaveGame>();
	Save->CompletedEncounterIds = {TEXT("Before")};
	TestTrue(TEXT("Initial write"), UPokeMonsterSaveSubsystem::SaveSnapshotToSlot(Save, Slot));
	TArray<uint8> Before, After;
	TestTrue(TEXT("Read original"), FFileHelper::LoadFileToArray(Before, *Path));
	TestFalse(TEXT("Null snapshot rejected"), UPokeMonsterSaveSubsystem::SaveSnapshotToSlot(nullptr, Slot));
	TestFalse(TEXT("Traversal rejected"), UPokeMonsterSaveSubsystem::SaveSnapshotToSlot(Save, TEXT("../") + Slot));
	TestTrue(TEXT("Read after rejected write"), FFileHelper::LoadFileToArray(After, *Path));
	TestTrue(TEXT("Existing save remains byte-identical after failure"), Before == After);
	TestTrue(TEXT("Create blocked destination"), Files.CreateDirectory(*BlockedPath));
	TestFalse(TEXT("Failed promotion reported"), UPokeMonsterSaveSubsystem::SaveSnapshotToSlot(Save, BlockedSlot));
	TestTrue(TEXT("Blocking destination preserved"), Files.DirectoryExists(*BlockedPath));
	TArray<FString> Pending;
	IFileManager::Get().FindFiles(Pending, *(FPaths::GetPath(Path) / (BlockedSlot + TEXT(".sav.*.pending"))), true, false);
	TestTrue(TEXT("Failed staging file removed"), Pending.IsEmpty());
	Save->CompletedEncounterIds = {TEXT("AfterReturn")};
	TestTrue(TEXT("Atomic overwrite existing slot"), UPokeMonsterSaveSubsystem::SaveSnapshotToSlot(Save, Slot));
	auto* Loaded = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(Slot, 0));
	if (!TestNotNull(TEXT("Existing loader decodes atomic write"), Loaded)) return false;
	TestTrue(TEXT("Completed state persisted"), Loaded->CompletedEncounterIds.Contains(TEXT("AfterReturn")));
	TestEqual(TEXT("Save schema unchanged"), Loaded->SaveVersion, UPokeMonsterSaveGame::CurrentVersion);
	return true;
}
#endif
