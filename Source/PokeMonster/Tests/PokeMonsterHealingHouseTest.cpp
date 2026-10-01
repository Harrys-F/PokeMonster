#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Interaction/PokeMonsterRestPoint.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Game/PokeMonsterGameMode.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/Level.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "GameFramework/PlayerStart.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/WorldSettings.h"
#include "Kismet/GameplayStatics.h"
#include "PaperSpriteComponent.h"
#include "UObject/StrongObjectPtr.h"
#include "Misc/ScopeExit.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterHealingHouseLayoutTest,
	"PokeMonster.Overworld.HealingHouse.Layout",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterHealingHouseLayoutTest::RunTest(const FString& Parameters)
{
	const auto* World = LoadObject<UWorld>(nullptr,
		TEXT("/Game/Maps/Dev_HealingHouseTestMap.Dev_HealingHouseTestMap"));
	if (!TestNotNull(TEXT("Healing house map loads"), World) || !World->PersistentLevel) return false;
	APokeMonsterRestPoint* Healer = nullptr;
	APokeMonsterBuildingCutaway* Cutaway = nullptr;
	AStaticMeshActor* Counter = nullptr;
	APlayerStart* Start = nullptr;
	TArray<FBox> EntranceWalls;
	for (AActor* Actor : World->PersistentLevel->Actors)
	{
		if (!Actor) continue;
		if (auto* Rest = Cast<APokeMonsterRestPoint>(Actor)) Healer = Rest;
		if (auto* Cut = Cast<APokeMonsterBuildingCutaway>(Actor)) Cutaway = Cut;
		if (Actor->ActorHasTag(TEXT("PokeMonsterSafeFallback"))) Start = Cast<APlayerStart>(Actor);
		if (Actor->ActorHasTag(TEXT("HealingHouse_Counter"))) Counter = Cast<AStaticMeshActor>(Actor);
		if (Actor->ActorHasTag(TEXT("HealingHouse_EntranceWall")))
		{
			auto* MeshActor = Cast<AStaticMeshActor>(Actor);
			if (!MeshActor) continue;
			auto* Mesh = MeshActor->GetStaticMeshComponent();
			Mesh->UpdateComponentToWorld();
			EntranceWalls.Add(Mesh->GetStaticMesh()->GetBoundingBox().TransformBy(Mesh->GetComponentTransform()));
		}
	}
	if (!TestNotNull(TEXT("Existing RestPoint serves as healer"), Healer)
		|| !TestNotNull(TEXT("Cutaway configured"), Cutaway)
		|| !TestNotNull(TEXT("Safe exterior start"), Start)
		|| !TestNotNull(TEXT("Healing counter"), Counter)) return false;
	TestEqual(TEXT("Existing overworld game mode"), World->GetWorldSettings()->DefaultGameMode.Get(),
		APokeMonsterGameMode::StaticClass());
	TestTrue(TEXT("Healer activates checkpoint"), Healer->bActivateCheckpoint);
	TestTrue(TEXT("Healer uses existing save"), Healer->bSaveAfterRest);
	TestEqual(TEXT("Stable house checkpoint identity"), Healer->CheckpointId, FName(TEXT("Dev_HealingHouse")));
	TestNotNull(TEXT("Healer has illustrated sprite"), Healer->Sprite->GetSprite());
	TestEqual(TEXT("Counter blocks walking"), Counter->GetStaticMeshComponent()->GetCollisionResponseToChannel(ECC_Pawn), ECR_Block);
	TestEqual(TEXT("Counter allows interaction trace"), Counter->GetStaticMeshComponent()->GetCollisionResponseToChannel(ECC_Visibility), ECR_Ignore);
	TestEqual(TEXT("Entrance made of two wall sections"), EntranceWalls.Num(), 2);
	if (EntranceWalls.Num() == 2)
	{
		EntranceWalls.Sort([](const FBox& A, const FBox& B) { return A.Min.Y < B.Min.Y; });
		TestTrue(TEXT("Door clearance exceeds three player capsule diameters"),
			EntranceWalls[1].Min.Y - EntranceWalls[0].Max.Y > 3.f * 56.f);
	}
	Cutaway->InteriorArea->UpdateComponentToWorld();
	TestFalse(TEXT("Roof visible at exterior spawn"), Cutaway->IsViewerInside(Start->GetActorLocation()));
	TestTrue(TEXT("Cutaway begins before the doorway"), Cutaway->IsViewerInside(FVector(-570.f, 0.f, 48.f)));
	TestTrue(TEXT("Whole main aisle is inside cutaway"), Cutaway->IsViewerInside(FVector(140.f, -80.f, 48.f)));
	TestTrue(TEXT("Healer remains inside cutaway after defeat return"), Cutaway->IsViewerInside(Healer->GetActorLocation()));
	TestTrue(TEXT("Occluding building parts configured"), Cutaway->OccludingActors.Num() > 0);
	for (AActor* Occluder : Cutaway->OccludingActors)
	{
		TestNotNull(TEXT("Cutaway references a real building part"), Occluder);
		TestTrue(TEXT("Cutaway targets only visual building meshes"), Cast<AStaticMeshActor>(Occluder) != nullptr);
		TestTrue(TEXT("Cutaway never hides healer"), Occluder != Healer);
	}
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterHealingHouseCollisionTest,
	"PokeMonster.Overworld.HealingHouse.CollisionAndCutaway",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterHealingHouseCollisionTest::RunTest(const FString& Parameters)
{
	auto* Map = LoadObject<UWorld>(nullptr, TEXT("/Game/Maps/Dev_HealingHouseTestMap.Dev_HealingHouseTestMap"));
	if (!TestNotNull(TEXT("House map for collision audit"), Map) || !Map->PersistentLevel) return false;
	// An isolated physics world copies the actual map meshes/transforms/responses; no editor assets change.
	UWorld* TestWorld = UWorld::CreateWorld(EWorldType::Game, false);
	if (!TestNotNull(TEXT("Isolated collision world"), TestWorld)) return false;
	ON_SCOPE_EXIT { TestWorld->DestroyWorld(false); };
	TArray<TObjectPtr<AActor>> FrontParts;
	for (AActor* Source : Map->PersistentLevel->Actors)
	{
		auto* MeshActor = Cast<AStaticMeshActor>(Source);
		if (!MeshActor) continue;
		auto* Original = MeshActor->GetStaticMeshComponent();
		auto* Copy = TestWorld->SpawnActor<AStaticMeshActor>(MeshActor->GetActorLocation(), MeshActor->GetActorRotation());
		Copy->SetActorScale3D(MeshActor->GetActorScale3D());
		auto* Mesh = Copy->GetStaticMeshComponent();
		Mesh->SetStaticMesh(Original->GetStaticMesh());
		Mesh->SetCollisionEnabled(Original->GetCollisionEnabled());
		Mesh->SetCollisionObjectType(Original->GetCollisionObjectType());
		Mesh->SetCollisionResponseToChannels(Original->GetCollisionResponseToChannels());
		if (Source->ActorHasTag(TEXT("HealingHouse_EntranceWall"))) FrontParts.Add(Copy);
	}
	FHitResult Hit;
	const FCollisionShape PlayerShape = FCollisionShape::MakeCapsule(28.f, 48.f);
	const FVector Route[] = { {-1000, 0, 50}, {-550, 0, 50}, {-330, 45, 50},
		{60, 0, 50}, {145, -80, 50}, {0, 220, 50}, {-280, 160, 50}, {-390, 0, 50}, {-750, 0, 50} };
	for (int32 Index = 1; Index < UE_ARRAY_COUNT(Route); ++Index)
		TestFalse(FString::Printf(TEXT("Free capsule route segment %d including diagonal door entry/exit"), Index),
			TestWorld->SweepSingleByChannel(Hit, Route[Index - 1], Route[Index], FQuat::Identity, ECC_Pawn, PlayerShape));
	TestTrue(TEXT("Counter blocks walking"), TestWorld->SweepSingleByChannel(Hit,
		FVector(145, -80, 50), FVector(330, -80, 50), FQuat::Identity, ECC_Pawn, PlayerShape));
	TestTrue(TEXT("Exterior wall blocks walking"), TestWorld->SweepSingleByChannel(Hit,
		FVector(-600, 300, 50), FVector(-300, 300, 50), FQuat::Identity, ECC_Pawn, PlayerShape));
	auto* Healer = TestWorld->SpawnActor<APokeMonsterRestPoint>(FVector(330, -80, 62), FRotator::ZeroRotator);
	TestTrue(TEXT("Short existing interaction sweep reaches healer through counter"), TestWorld->SweepSingleByChannel(Hit,
		FVector(145, -80, 50), FVector(295, -80, 50), FQuat::Identity, ECC_Visibility, FCollisionShape::MakeSphere(32.f)));
	TestEqual(TEXT("Interaction selects healer rather than furniture"), Hit.GetActor(), static_cast<AActor*>(Healer));
	auto* Viewer = TestWorld->SpawnActor<APokeMonsterPlayerCharacter>(FVector(-1000, 0, 50), FRotator::ZeroRotator);
	auto* Controller = TestWorld->SpawnActor<APlayerController>();
	// This isolated world has no BeginPlay, so register the test controller explicitly.
	TestWorld->AddController(Controller);
	Controller->Possess(Viewer);
	TestEqual(TEXT("Cutaway can resolve the possessed viewer"), UGameplayStatics::GetPlayerPawn(Controller, 0), static_cast<APawn*>(Viewer));
	auto* Cutaway = TestWorld->SpawnActor<APokeMonsterBuildingCutaway>(FVector(-40, 0, 150), FRotator::ZeroRotator);
	Cutaway->OccludingActors = FrontParts;
	Cutaway->Tick(0.1f);
	TestFalse(TEXT("Exterior does not activate cutaway"), Cutaway->IsCutawayActive());
	Viewer->SetActorLocation(FVector(0, 0, 50));
	Cutaway->Tick(0.1f);
	TestTrue(TEXT("Interior activates cutaway"), Cutaway->IsCutawayActive());
	for (AActor* Part : FrontParts) TestTrue(TEXT("Front wall becomes invisible"), Part->IsHidden());
	FCollisionQueryParams WithoutViewer;
	WithoutViewer.AddIgnoredActor(Viewer);
	TestTrue(TEXT("Invisible wall still blocks gameplay"), TestWorld->SweepSingleByChannel(Hit,
		FVector(-600, 300, 50), FVector(-300, 300, 50), FQuat::Identity, ECC_Pawn, PlayerShape, WithoutViewer));
	Viewer->SetActorLocation(FVector(-1000, 0, 50));
	Cutaway->Tick(0.1f);
	TestFalse(TEXT("Leaving deactivates cutaway"), Cutaway->IsCutawayActive());
	for (AActor* Part : FrontParts) TestFalse(TEXT("Front wall restored on exit"), Part->IsHidden());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterHealingHouseRestTest,
	"PokeMonster.Overworld.HealingHouse.RestCheckpointSaveAndDefeat",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterHealingHouseRestTest::RunTest(const FString& Parameters)
{
	auto* World = LoadObject<UWorld>(nullptr, TEXT("/Game/Maps/Dev_HealingHouseTestMap.Dev_HealingHouseTestMap"));
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	if (!TestNotNull(TEXT("House map"), World) || !TestNotNull(TEXT("Species"), Species) || !TestNotNull(TEXT("Move"), Move)) return false;
	TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
	auto* Checkpoints = NewObject<UPokeMonsterCheckpointSubsystem>(GI.Get());
	auto* Quests = NewObject<UPokeMonsterQuestSubsystem>(GI.Get());
	auto* Quest = LoadObject<UPokeMonsterQuestData>(nullptr, TEXT("/Game/Data/Quests/DA_SliceArchiveQuest.DA_SliceArchiveQuest"));
	if (!TestNotNull(TEXT("Existing quest"), Quest)) return false;
	Quests->StartQuest(Quest);
	Quests->RecordDialogue(TEXT("DA_SliceGuideDialogue"));
	auto First = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 15);
	auto Second = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 12);
	First.AssignMove(0, Move);
	Second.AssignMove(0, Move);
	First.CurrentHP = 1;
	Second.CurrentHP = 0;
	First.ConsumeMovePP(0, 3);
	Second.ConsumeMovePP(0, 5);
	Encounter->RestorePersistentState({First, Second}, {TEXT("HouseTest_ExistingTrainer")}, {TEXT("HouseTest_WorldFlag")});
	const FTransform SafePosition(FRotator(0.f, 0.f, 0.f), FVector(145.f, -80.f, 48.f));
	UPokeMonsterSaveGame* Snapshot = nullptr;
	const auto Result = APokeMonsterRestPoint::PerformRest(Encounter, true,
		[&] { Snapshot = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI.Get(), Checkpoints, Quests); return Snapshot != nullptr; },
		[&] { return Checkpoints->ActivateCheckpoint(TEXT("Dev_HealingHouse"), World, SafePosition); });
	TestEqual(TEXT("Rest and save successful"), Result.Outcome, EPokeMonsterRestOutcome::HealedAndSaved);
	TestTrue(TEXT("House checkpoint registered"), Result.bCheckpointActivated);
	if (!TestNotNull(TEXT("Snapshot after checkpoint activation"), Snapshot)) return false;
	for (const auto& Member : Encounter->GetPlayerParty())
	{
		TestEqual(TEXT("Entire team healed including fainted member"), Member.CurrentHP, Member.GetMaxHP());
		TestEqual(TEXT("Entire team PP full"), Member.GetMoveSlots()[0].GetCurrentPP(), Move->MaxPP);
	}
	const FString Slot = TEXT("PokeMonster_HouseAutomation_") + FGuid::NewGuid().ToString(EGuidFormats::Digits);
	TestTrue(TEXT("House state written to isolated test slot"), UGameplayStatics::SaveGameToSlot(Snapshot, Slot, 0));
	auto* Loaded = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(Slot, 0));
	TestTrue(TEXT("Isolated test slot removed"), UGameplayStatics::DeleteGameInSlot(Slot, 0));
	Encounter->RestorePersistentState({}, {}, {});
	Checkpoints->RestoreCheckpoint({});
	Quests->RestoreProgress({});
	if (!TestNotNull(TEXT("Disk save loaded"), Loaded) || !TestTrue(TEXT("All existing owners restored"),
		UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded, Encounter, Inventory, Checkpoints, Quests))) return false;
	TestEqual(TEXT("Checkpoint map retained"), Checkpoints->GetActiveCheckpoint().MapPackage, FName(TEXT("/Game/Maps/Dev_HealingHouseTestMap")));
	TestEqual(TEXT("Free counter approach position retained"), Checkpoints->GetActiveCheckpoint().Location, SafePosition.GetLocation());
	TestEqual(TEXT("Quest step retained"), Quests->GetCurrentStep(Quest->InternalId), 1);
	TArray<FPokeMonsterCreatureInstance> Defeated = Encounter->GetPlayerParty();
	for (auto& Member : Defeated) { Member.CurrentHP = 0; Member.ConsumeMovePP(0, 5); }
	Encounter->RestorePersistentState(Defeated, Encounter->GetDefeatedTrainerIds(), Encounter->GetCompletedEncounterIds());
	FPokeMonsterCheckpointData Target;
	TestTrue(TEXT("Defeat selects house checkpoint"), UPokeMonsterCheckpointSubsystem::ResolveReturnTarget(
		Checkpoints->GetActiveCheckpoint().MapPackage, Checkpoints->GetActiveCheckpoint(), FTransform::Identity, Target));
	TestEqual(TEXT("Defeat destination is activated house"), Target.Location, SafePosition.GetLocation());
	TestTrue(TEXT("Existing defeat mechanism heals team"), UPokeMonsterCheckpointSubsystem::RestoreTeamAfterDefeat(Encounter));
	for (const auto& Member : Encounter->GetPlayerParty())
	{
		TestEqual(TEXT("HP full after defeat"), Member.CurrentHP, Member.GetMaxHP());
		TestEqual(TEXT("PP full after defeat"), Member.GetMoveSlots()[0].GetCurrentPP(), Move->MaxPP);
	}
	TestEqual(TEXT("Individual creature retained"), Encounter->GetPlayerParty()[0].InstanceId, First.InstanceId);
	TestTrue(TEXT("Previous trainer status retained"), Encounter->IsTrainerDefeated(TEXT("HouseTest_ExistingTrainer")));
	TestFalse(TEXT("Lost trainer not marked defeated"), Encounter->IsTrainerDefeated(TEXT("HouseTest_LostTrainer")));
	TestTrue(TEXT("World flag retained"), Encounter->IsEncounterCompleted(TEXT("HouseTest_WorldFlag")));
	TestEqual(TEXT("Defeat does not reset quest"), Quests->GetCurrentStep(Quest->InternalId), 1);
	return true;
}
#endif
