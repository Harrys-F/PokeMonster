#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"

#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCheckpointTest,
	"PokeMonster.Overworld.Checkpoint.DefeatAndSave",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterCheckpointTest::RunTest(const FString& Parameters)
{
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	if (!TestNotNull(TEXT("Species"), Species) || !TestNotNull(TEXT("Move"), Move)) return false;
	TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
	auto* Checkpoints = NewObject<UPokeMonsterCheckpointSubsystem>(GI.Get());
	FPokeMonsterCheckpointData Site;
	Site.CheckpointId = TEXT("Dev_RestPoint_01");
	Site.MapPackage = TEXT("/Game/Maps/Dev_TestMap");
	Site.Location = FVector(-770.f, -1200.f, 100.f);
	Site.Rotation = FRotator(0.f, 30.f, 0.f);
	TestTrue(TEXT("Checkpoint activated"), Checkpoints->RestoreCheckpoint(Site));
	TestEqual(TEXT("Checkpoint ID active"), Checkpoints->GetActiveCheckpoint().CheckpointId, Site.CheckpointId);
	const FTransform Fallback(FRotator(0.f, 35.f, 0.f), FVector(-1000.f, -1100.f, 100.f));
	FPokeMonsterCheckpointData Target;
	TestTrue(TEXT("Active checkpoint selected"), UPokeMonsterCheckpointSubsystem::ResolveReturnTarget(
		Site.MapPackage, Checkpoints->GetActiveCheckpoint(), Fallback, Target));
	TestEqual(TEXT("Checkpoint position selected"), Target.Location, Site.Location);
	TestEqual(TEXT("Checkpoint rotation selected"), Target.Rotation, Site.Rotation);
	TestTrue(TEXT("Fallback without checkpoint"), UPokeMonsterCheckpointSubsystem::ResolveReturnTarget(
		Site.MapPackage, {}, Fallback, Target));
	TestEqual(TEXT("Fallback position"), Target.Location, Fallback.GetLocation());
	TestEqual(TEXT("Fallback map"), Target.MapPackage, Site.MapPackage);

	auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 20);
	if (!TestTrue(TEXT("Move assigned"), Creature.AssignMove(0, Move))) return false;
	Creature.CurrentHP = 0;
	TestTrue(TEXT("PP spent"), Creature.ConsumeMovePP(0, 5));
	const FGuid OriginalId = Creature.InstanceId;
	const int64 OriginalXP = Creature.Experience;
	TestTrue(TEXT("Defeated party installed"), Encounter->RestorePersistentState({Creature},
		{TEXT("AlreadyDefeatedTrainer")}, {TEXT("ExistingWorldFlag")}));
	TestTrue(TEXT("Return restores party"), UPokeMonsterCheckpointSubsystem::RestoreTeamAfterDefeat(Encounter));
	const auto& Restored = Encounter->GetPlayerParty()[0];
	TestEqual(TEXT("HP full after return"), Restored.CurrentHP, Restored.GetMaxHP());
	TestEqual(TEXT("PP full after return"), Restored.GetMoveSlots()[0].GetCurrentPP(), Move->MaxPP);
	TestEqual(TEXT("Identity retained"), Restored.InstanceId, OriginalId);
	TestEqual(TEXT("XP retained"), Restored.Experience, OriginalXP);
	TestTrue(TEXT("Existing defeated trainer retained"), Encounter->IsTrainerDefeated(TEXT("AlreadyDefeatedTrainer")));
	TestFalse(TEXT("Losing trainer not marked defeated"), Encounter->IsTrainerDefeated(TEXT("CurrentTrainer")));
	TestTrue(TEXT("World flag retained"), Encounter->IsEncounterCompleted(TEXT("ExistingWorldFlag")));

	TestTrue(TEXT("Checkpoint selected again"), Checkpoints->RestoreCheckpoint(Site));
	auto* Save = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI.Get(), Checkpoints);
	if (!TestNotNull(TEXT("Snapshot"), Save)) return false;
	TestEqual(TEXT("Schema upgraded"), Save->SaveVersion, UPokeMonsterSaveGame::CurrentVersion);
	TestEqual(TEXT("Checkpoint stored"), Save->ActiveCheckpoint.CheckpointId, Site.CheckpointId);
	const FString Slot = TEXT("PokeMonster_CheckpointAutomation_") + FGuid::NewGuid().ToString(EGuidFormats::Digits);
	TestTrue(TEXT("Checkpoint save written"), UGameplayStatics::SaveGameToSlot(Save, Slot, 0));
	auto* Loaded = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(Slot, 0));
	TestTrue(TEXT("Temporary save removed"), UGameplayStatics::DeleteGameInSlot(Slot, 0));
	if (!TestNotNull(TEXT("Loaded save"), Loaded)) return false;
	TestTrue(TEXT("Checkpoint cleared"), Checkpoints->RestoreCheckpoint({}));
	TestTrue(TEXT("Snapshot loaded"), UPokeMonsterSaveSubsystem::RestoreSnapshot(
		Loaded, Encounter, Inventory, Checkpoints));
	TestEqual(TEXT("Checkpoint ID loaded"), Checkpoints->GetActiveCheckpoint().CheckpointId, Site.CheckpointId);
	TestEqual(TEXT("Checkpoint map loaded"), Checkpoints->GetActiveCheckpoint().MapPackage, Site.MapPackage);
	TestEqual(TEXT("Checkpoint location loaded"), Checkpoints->GetActiveCheckpoint().Location, Site.Location);
	TestEqual(TEXT("Checkpoint rotation loaded"), Checkpoints->GetActiveCheckpoint().Rotation, Site.Rotation);

	Loaded->SaveVersion = 1;
	TestTrue(TEXT("Version 1 save migrates without checkpoint"), UPokeMonsterSaveSubsystem::RestoreSnapshot(
		Loaded, Encounter, Inventory, Checkpoints));
	TestFalse(TEXT("Legacy save clears checkpoint"), Checkpoints->HasActiveCheckpoint());
	Loaded->SaveVersion = 2;
	Loaded->ActiveCheckpoint.MapPackage = TEXT("bad map");
	AddExpectedError(TEXT("Invalid checkpoint in save"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Invalid checkpoint rejected atomically"), UPokeMonsterSaveSubsystem::RestoreSnapshot(
		Loaded, Encounter, Inventory, Checkpoints));
	TestFalse(TEXT("No checkpoint was partly installed"), Checkpoints->HasActiveCheckpoint());
	TestTrue(TEXT("Trainer flag survived invalid load"), Encounter->IsTrainerDefeated(TEXT("AlreadyDefeatedTrainer")));
	Loaded->ActiveCheckpoint = {};
	Loaded->ActiveCheckpoint.Location = FVector(1.f, 0.f, 0.f);
	AddExpectedError(TEXT("Invalid checkpoint in save"), EAutomationExpectedErrorFlags::Contains, 1);
	TestFalse(TEXT("Partial empty checkpoint rejected"), UPokeMonsterSaveSubsystem::RestoreSnapshot(
		Loaded, Encounter, Inventory, Checkpoints));
	return true;
}
#endif
