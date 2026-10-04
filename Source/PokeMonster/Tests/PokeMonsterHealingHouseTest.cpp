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
#include "PhysicsEngine/BodySetup.h"
#include "Materials/MaterialInterface.h"
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
		TestTrue(TEXT("Door clearance exceeds two player capsule diameters with 38 cm spare"),
			EntranceWalls[1].Min.Y - EntranceWalls[0].Max.Y > 2.f * 56.f);
	}
	Cutaway->InteriorArea->UpdateComponentToWorld();
	TestFalse(TEXT("Roof visible at exterior spawn"), Cutaway->IsViewerInside(Start->GetActorLocation()));
	TestFalse(TEXT("Approaching the house does not activate cutaway"), Cutaway->IsViewerInside(FVector(-570.f, 0.f, 48.f)));
	Cutaway->DoorThreshold->UpdateComponentToWorld();
	TestEqual(TEXT("Door threshold is centred on the actual doorway"), Cutaway->DoorThreshold->GetComponentLocation(), FVector(-450.f, 0.f, 107.5f));
	TestEqual(TEXT("Door threshold matches the 150 by 215 cm passage"), Cutaway->DoorThreshold->GetUnscaledBoxExtent(), FVector(20.f, 75.f, 107.5f));
	if (EntranceWalls.Num() == 2)
	{
		TestTrue(TEXT("Collision matches the narrowed 150 cm visual passage"),
			FMath::IsNearlyEqual(EntranceWalls[1].Min.Y - EntranceWalls[0].Max.Y, 150.f, 0.1f));
	}
	// The actual upper-window mesh must share the doorway axis, not an offset roof ridge.
	const auto* LoftGlass = LoadObject<UStaticMesh>(nullptr,
		TEXT("/Game/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Loft.SM_HH_V2_Glass_Loft"));
	if (TestNotNull(TEXT("Aligned round-window mesh loads"), LoftGlass))
		TestTrue(TEXT("Round window centred on doorway Y=0"),
			FMath::IsNearlyZero(LoftGlass->GetBoundingBox().GetCenter().Y, 0.1f));
	TestEqual(TEXT("Door threshold never changes gameplay collision"), Cutaway->DoorThreshold->GetCollisionEnabled(), ECollisionEnabled::NoCollision);
	TestFalse(TEXT("Forecourt is outside the small threshold"), Cutaway->IsViewerInDoorway(FVector(-570.f, 0.f, 48.f)));
	TestTrue(TEXT("Diagonal position fits doorway transition"), Cutaway->IsViewerInDoorway(FVector(-450.f, 55.f, 48.f)));
	TestFalse(TEXT("Old wide doorway edge does not trigger cutaway"), Cutaway->IsViewerInDoorway(FVector(-450.f, 80.f, 48.f)));
	TestFalse(TEXT("Facade away from door does not form a transition"), Cutaway->IsViewerInDoorway(FVector(-450.f, 300.f, 48.f)));
	TestEqual(TEXT("Fade duration is 0.4 seconds"), Cutaway->FadeDuration, 0.4f);
	TestTrue(TEXT("Whole main aisle is inside cutaway"), Cutaway->IsViewerInside(FVector(140.f, -80.f, 48.f)));
	TestTrue(TEXT("Healer remains inside cutaway after defeat return"), Cutaway->IsViewerInside(Healer->GetActorLocation()));
	TestTrue(TEXT("Expanded interior is explicitly opt-in in this prototype map"), Cutaway->bUseRelocatedInterior);
	TestTrue(TEXT("Expanded room retains existing interior camera mechanism"), Cutaway->bUseInteriorCamera);
	TestEqual(TEXT("Chosen room camera distance"), Cutaway->InteriorCameraDistance, 2600.f);
	Cutaway->RelocatedDoorThreshold->UpdateComponentToWorld();
	TestEqual(TEXT("Same-map inner door matches exterior orientation and clearance"),Cutaway->RelocatedDoorThreshold->GetComponentLocation(),FVector(19500,0,107.5));

	TestTrue(TEXT("Occluding building parts configured"), Cutaway->OccludingActors.Num() > 0);
	for (AActor* Occluder : Cutaway->OccludingActors)
	{
		TestNotNull(TEXT("Cutaway references a real building part"), Occluder);
		TestTrue(TEXT("Cutaway targets only visual building meshes"), Cast<AStaticMeshActor>(Occluder) != nullptr);
		TestTrue(TEXT("Cutaway never hides healer"), Occluder != Healer);
	}
	// Imported architecture is presentation only; the retained simple blockers
	// remain authoritative. In particular, a convex whole-house hull must never
	// seal the door or the room. Roof/front fade; side/rear walls stay visible.
	TMap<FName, AStaticMeshActor*> Imported;
	for (AActor* Actor : World->PersistentLevel->Actors)
	{
		if (!Actor || !Actor->ActorHasTag(TEXT("HealingHouse_BlenderV1"))) continue;
		auto* MeshActor = Cast<AStaticMeshActor>(Actor);
		if (!TestNotNull(TEXT("Imported architecture is a mesh actor"), MeshActor)) continue;
		Imported.Add(FName(*Actor->GetActorLabel()), MeshActor);
		TestEqual(TEXT("Imported geometry never introduces whole-house collision"),
			MeshActor->GetStaticMeshComponent()->GetCollisionEnabled(), ECollisionEnabled::NoCollision);
		TestEqual(TEXT("Imported module uses unit scale"), Actor->GetActorScale3D(), FVector::OneVector);
		TestEqual(TEXT("Imported module shares building origin"), Actor->GetActorLocation(), FVector::ZeroVector);
	}
	TestTrue(TEXT("Blender shell is installed"), Imported.Num() >= 9);
	for (const FName Name : {FName(TEXT("HH_Roof_Main")), FName(TEXT("HH_Roof_Porch")),
		FName(TEXT("HH_Walls_Front")), FName(TEXT("HH_Gable_Front"))})
	{
		auto* Module = Imported.FindRef(Name);
		if (TestNotNull(TEXT("Required removable Blender module exists"), Module))
		{
			TestTrue(TEXT("Imported roof/near facade belongs to existing cutaway"), Cutaway->OccludingActors.Contains(Module));
			for (UMaterialInterface* Material : Module->GetStaticMeshComponent()->GetMaterials())
			{
				if (!TestNotNull(TEXT("Occluding module has a material"), Material)) continue;
				TestEqual(TEXT("Cutaway uses masked rendering rather than translucency"), Material->GetBlendMode(), BLEND_Masked);
				float DefaultFade = -1.f;
				TestTrue(TEXT("Material exposes the primitive-driven fade parameter"), Material->GetScalarParameterValue(FMaterialParameterInfo(TEXT("HouseCutaway")), DefaultFade));
				TestEqual(TEXT("Material is fully visible without runtime cutaway data"), DefaultFade, 0.f);
			}
		}
	}
	int32 RetainedExpandedWalls = 0;
	int32 RemovableExpandedFrontParts = 0;
	for (AActor* Actor : World->PersistentLevel->Actors)
	{
		if (!Actor) continue;
		const FString Label = Actor->GetActorLabel();
		if (Label.Contains(TEXT("CameraSide")))
			TestFalse(TEXT("Legacy side facade is no longer a blanket occluder"), Cutaway->OccludingActors.Contains(Actor));
		if (Label.StartsWith(TEXT("HH_Expanded_Side")) || Label.StartsWith(TEXT("HH_Expanded_Rear")))
		{
			TestFalse(TEXT("Expanded side/rear wall and beam remain outside cutaway"), Cutaway->OccludingActors.Contains(Actor));
			TestFalse(TEXT("Retained expanded architecture is visible"), Actor->IsHidden());
			if (Label.Contains(TEXT("Wall"))) ++RetainedExpandedWalls;
		}
		if (Label.StartsWith(TEXT("HH_Expanded_FrontWall")) || Label.StartsWith(TEXT("HH_Expanded_DoorPost"))
			|| Label == TEXT("HH_Expanded_DoorLintel") || Label == TEXT("HH_Expanded_DoorBeam"))
		{
			TestTrue(TEXT("Camera-facing front and doorway trim are explicit occluders"), Cutaway->OccludingActors.Contains(Actor));
			++RemovableExpandedFrontParts;
		}
	}
	TestEqual(TEXT("Ten side bays and six rear bays retained"), RetainedExpandedWalls, 16);
	TestEqual(TEXT("Only the six expanded front/door parts fade"), RemovableExpandedFrontParts, 6);
	if (auto* Roof = Imported.FindRef(TEXT("HH_Roof_Main")))
	{
		const FBox Bounds = Roof->GetStaticMeshComponent()->GetStaticMesh()->GetBoundingBox();
		TestTrue(TEXT("FBX metre scale produces 6.4 metre ridge"), FMath::IsNearlyEqual(Bounds.Max.Z, 640.f, 0.3f));
	}
	// V3 dressing must never turn a small decoration into a movement/interaction
	// blocker. Fixed furniture remains visible and ignores the healer trace.
	int32 Decorations = 0;
	TMap<FName, FVector> Beds;
	for (AActor* Actor : World->PersistentLevel->Actors)
	{
		if (!Actor || !Actor->ActorHasTag(TEXT("HealingHouse_V3"))) continue;
		TArray<UPrimitiveComponent*> Primitives;
		Actor->GetComponents<UPrimitiveComponent>(Primitives);
		if (Actor->ActorHasTag(TEXT("HealingHouse_V3_Decoration")))
		{
			++Decorations;
			for (auto* Primitive : Primitives)
			{
				TestEqual(TEXT("Small V3 decoration has no gameplay collision"),
					Primitive->GetCollisionEnabled(), ECollisionEnabled::NoCollision);
				if (auto* Sprite = Cast<UPaperSpriteComponent>(Primitive))
					TestNotNull(TEXT("V3 planted sprite is assigned and renderable"), Sprite->GetSprite());
			}
		}
		if (Actor->ActorHasTag(TEXT("HealingHouse_V3_Furniture")))
			for (const auto* Primitive : Primitives)
			{
				TestTrue(TEXT("Blocking V3 furniture stays visible"), Primitive->IsVisible());
				TestEqual(TEXT("Furniture does not intercept interaction"),
					Primitive->GetCollisionResponseToChannel(ECC_Visibility), ECR_Ignore);
			}
		if (auto* MeshActor = Cast<AStaticMeshActor>(Actor))
		{
			const FString Label = Actor->GetActorLabel();
			if (Label == TEXT("HH_V3_TreatmentBedSmall") || Label == TEXT("HH_V3_TreatmentBedLarge"))
				Beds.Add(FName(*Label), MeshActor->GetStaticMeshComponent()->GetStaticMesh()->GetBoundingBox().GetSize());
			if (Cutaway->OccludingActors.Contains(Actor))
				for (const auto* Material : MeshActor->GetStaticMeshComponent()->GetMaterials())
					if (TestNotNull(TEXT("Front dressing has fade-compatible material"), Material))
						TestEqual(TEXT("New facade dressing uses the same masked fade"), Material->GetBlendMode(), BLEND_Masked);
		}
	}
	TestTrue(TEXT("V3 small props are independently placed"), Decorations > 20);
	TestEqual(TEXT("Exactly two creature bed sizes"), Beds.Num(), 2);
	if (Beds.Num() == 2)
	{
		TestTrue(TEXT("Large bed is longer than small bed"),
			Beds[TEXT("HH_V3_TreatmentBedLarge")].X > Beds[TEXT("HH_V3_TreatmentBedSmall")].X + 30.f);
		TestTrue(TEXT("Large bed is wider than small bed"),
			Beds[TEXT("HH_V3_TreatmentBedLarge")].Y > Beds[TEXT("HH_V3_TreatmentBedSmall")].Y + 15.f);
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
		if (Source->ActorHasTag(TEXT("HealingHouse_V3_Furniture")))
		{
			auto* Body = Original->GetStaticMesh()->GetBodySetup();
			TestNotNull(TEXT("V3 furniture has saved body setup"), Body);
			if (Body)
			{
				AddInfo(FString::Printf(TEXT("Saved %s: %d convex, %d boxes, physics created=%d"),
					*Source->GetActorLabel(), Body->AggGeom.ConvexElems.Num(), Body->AggGeom.BoxElems.Num(), Body->bCreatedPhysicsMeshes));
				// Imported convex data may be uncooked on a fresh/null-RHI load.
				// Prepare it before copying the mesh into the isolated physics world.
				Body->CreatePhysicsMeshes();
			}
		}
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
	const FVector ExpandedRoute[] = { {19450,0,50}, {19580,35,50}, {19750,0,50},
		{20000,0,50}, {20145,-80,50}, {20000,170,50}, {19560,20,50}, {19450,0,50} };
	for (int32 Index=1; Index<UE_ARRAY_COUNT(ExpandedRoute); ++Index)
		TestFalse(FString::Printf(TEXT("Expanded room capsule route %d"),Index),
			TestWorld->SweepSingleByChannel(Hit,ExpandedRoute[Index-1],ExpandedRoute[Index],FQuat::Identity,ECC_Pawn,PlayerShape));
	TestTrue(TEXT("Counter blocks walking"), TestWorld->SweepSingleByChannel(Hit,
		FVector(20145, -80, 50), FVector(20330, -80, 50), FQuat::Identity, ECC_Pawn, PlayerShape));
	TestTrue(TEXT("Exterior wall blocks walking"), TestWorld->SweepSingleByChannel(Hit,
		FVector(-600, 300, 50), FVector(-300, 300, 50), FQuat::Identity, ECC_Pawn, PlayerShape));
	TestTrue(TEXT("Visible V3 creature bed blocks walking"), TestWorld->SweepSingleByChannel(Hit,
		FVector(19955, 290, 50), FVector(19955, 415, 50), FQuat::Identity, ECC_Pawn, PlayerShape));
	TestTrue(TEXT("Visible V3 bookcase blocks walking"), TestWorld->SweepSingleByChannel(Hit,
		FVector(19830, -325, 50), FVector(19830, -450, 50), FQuat::Identity, ECC_Pawn, PlayerShape));
	auto* Healer = TestWorld->SpawnActor<APokeMonsterRestPoint>(FVector(20330, -80, 62), FRotator::ZeroRotator);
	TestTrue(TEXT("Short existing interaction sweep reaches healer through counter"), TestWorld->SweepSingleByChannel(Hit,
		FVector(20145, -80, 50), FVector(20295, -80, 50), FQuat::Identity, ECC_Visibility, FCollisionShape::MakeSphere(32.f)));
	TestEqual(TEXT("Interaction selects healer rather than furniture"), Hit.GetActor(), static_cast<AActor*>(Healer));
	auto* Viewer = TestWorld->SpawnActor<APokeMonsterPlayerCharacter>(FVector(-1000, 0, 50), FRotator::ZeroRotator);
	auto* Controller = TestWorld->SpawnActor<APlayerController>();
	// This isolated world has no BeginPlay, so register the test controller explicitly.
	TestWorld->AddController(Controller);
	Controller->Possess(Viewer);
	TestEqual(TEXT("Cutaway can resolve the possessed viewer"), UGameplayStatics::GetPlayerPawn(Controller, 0), static_cast<APawn*>(Viewer));
	auto* Cutaway = TestWorld->SpawnActor<APokeMonsterBuildingCutaway>(FVector(-40, 0, 150), FRotator::ZeroRotator);
	// Exercise the map-authored dimensions, not the generic class defaults.
	APokeMonsterBuildingCutaway* MapCutaway = nullptr;
	for (AActor* Actor : Map->PersistentLevel->Actors)
		if (auto* Candidate = Cast<APokeMonsterBuildingCutaway>(Actor)) MapCutaway = Candidate;
	if (!TestNotNull(TEXT("Map-authored cutaway dimensions"), MapCutaway)) return false;
	Cutaway->InteriorArea->SetBoxExtent(MapCutaway->InteriorArea->GetUnscaledBoxExtent());
	Cutaway->DoorThreshold->SetRelativeLocation(MapCutaway->DoorThreshold->GetRelativeLocation());
	Cutaway->DoorThreshold->SetBoxExtent(MapCutaway->DoorThreshold->GetUnscaledBoxExtent());
	Cutaway->OccludingActors = FrontParts;
	Cutaway->Tick(0.1f);
	TestFalse(TEXT("Exterior does not activate cutaway"), Cutaway->IsCutawayActive());
	Viewer->SetActorLocation(FVector(-570, 0, 50));
	Cutaway->Tick(0.1f);
	TestFalse(TEXT("Approach before door keeps entire roof and facade visible"), Cutaway->IsCutawayActive());
	TestEqual(TEXT("No fade in forecourt"), Cutaway->GetCutawayAmount(), 0.f);
	Viewer->SetActorLocation(FVector(-443, 60, 50));
	Cutaway->Tick(0.1f);
	TestTrue(TEXT("Crossing threshold starts the fade"), Cutaway->IsCutawayActive());
	TestTrue(TEXT("Quarter-faded after 0.1 seconds"), FMath::IsNearlyEqual(Cutaway->GetCutawayAmount(), 0.25f));
	for (AActor* Part : FrontParts)
	{
		TestFalse(TEXT("Part stays renderable during the transition"), Part->IsHidden());
		const auto* Mesh = CastChecked<AStaticMeshActor>(Part)->GetStaticMeshComponent();
		TestTrue(TEXT("Partial fade reaches actual primitive material data"), FMath::IsNearlyEqual(Mesh->GetCustomPrimitiveData().Data[0], 0.25f));
	}
	Viewer->SetActorLocation(FVector(-450, 0, 50));
	Cutaway->Tick(0.1f);
	TestTrue(TEXT("Pausing on threshold retains inside state"), Cutaway->IsCutawayActive());
	TestTrue(TEXT("Fade continues smoothly while paused"), FMath::IsNearlyEqual(Cutaway->GetCutawayAmount(), 0.5f));
	Viewer->SetActorLocation(FVector(-452, -30, 50));
	Cutaway->Tick(0.f);
	TestTrue(TEXT("Small threshold jitter does not flicker"), Cutaway->IsCutawayActive());
	Viewer->SetActorLocation(FVector(-458, -30, 50));
	Cutaway->Tick(0.04f);
	TestFalse(TEXT("Turning around across threshold changes target"), Cutaway->IsCutawayActive());
	TestTrue(TEXT("Reversal preserves continuous fade progress"), FMath::IsNearlyEqual(Cutaway->GetCutawayAmount(), 0.4f));
	Viewer->SetActorLocation(FVector(-450, -30, 50));
	Cutaway->Tick(0.f);
	TestFalse(TEXT("Paused threshold retains outside state after reversal"), Cutaway->IsCutawayActive());
	Cutaway->Tick(0.16f);
	TestTrue(TEXT("Reverse transition restores full opacity"), FMath::IsNearlyZero(Cutaway->GetCutawayAmount()));
	Viewer->SetActorLocation(FVector(-444, 60, 50));
	Cutaway->Tick(0.4f);
	TestTrue(TEXT("Diagonal threshold crossing activates cutaway"), Cutaway->IsCutawayActive());
	TestEqual(TEXT("Fully faded after 0.4 seconds"), Cutaway->GetCutawayAmount(), 1.f);
	Viewer->SetActorLocation(FVector(140, -80, 50));
	Cutaway->Tick(0.1f);
	TestTrue(TEXT("Interior keeps cutaway active"), Cutaway->IsCutawayActive());
	for (AActor* Part : FrontParts) TestTrue(TEXT("Only completed fade hides the front wall"), Part->IsHidden());
	FCollisionQueryParams WithoutViewer;
	WithoutViewer.AddIgnoredActor(Viewer);
	TestTrue(TEXT("Invisible wall still blocks gameplay"), TestWorld->SweepSingleByChannel(Hit,
		FVector(-600, 300, 50), FVector(-300, 300, 50), FQuat::Identity, ECC_Pawn, PlayerShape, WithoutViewer));
	Viewer->SetActorLocation(FVector(-460, -60, 50));
	Cutaway->Tick(0.1f);
	TestFalse(TEXT("Leaving through threshold starts restoration"), Cutaway->IsCutawayActive());
	TestTrue(TEXT("Exit fades in gradually"), FMath::IsNearlyEqual(Cutaway->GetCutawayAmount(), 0.75f));
	for (AActor* Part : FrontParts) TestFalse(TEXT("Front wall is renderable during fade-in"), Part->IsHidden());
	Viewer->SetActorLocation(FVector(-1000, 0, 50));
	Cutaway->Tick(0.31f);
	TestEqual(TEXT("Exterior restoration completes"), Cutaway->GetCutawayAmount(), 0.f);
	for (AActor* Part : FrontParts) TestFalse(TEXT("Front wall restored on exit"), Part->IsHidden());
	Viewer->SetActorLocation(FVector(140, -80, 50));
	auto* InteriorSpawnCutaway = TestWorld->SpawnActor<APokeMonsterBuildingCutaway>(FVector(-40, 0, 150), FRotator::ZeroRotator);
	InteriorSpawnCutaway->Tick(0.f);
	TestTrue(TEXT("Existing checkpoint spawn inside initializes the correct state"), InteriorSpawnCutaway->IsCutawayActive());
	TestEqual(TEXT("Existing interior spawn starts readable"), InteriorSpawnCutaway->GetCutawayAmount(), 1.f);
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
