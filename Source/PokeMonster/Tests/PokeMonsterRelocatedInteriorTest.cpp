#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "Camera/CameraComponent.h"
#include "Camera/CameraTypes.h"
#include "Components/BoxComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputActionValue.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterRelocatedInteriorTransitionTest,
    "PokeMonster.Building.RelocatedInterior.MappingAndTransition",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterRelocatedInteriorTransitionTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
    if (!TestNotNull(TEXT("Isolated relocation world"), World)) return false;
    GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
    ON_SCOPE_EXIT { GEngine->DestroyWorldContext(World); World->DestroyWorld(false); };
    auto* Player = World->SpawnActor<APokeMonsterPlayerCharacter>(FVector(-550,0,48), FRotator::ZeroRotator);
    auto* Controller = World->SpawnActor<APlayerController>();
    World->AddController(Controller); Controller->Possess(Player);
    auto* Building = World->SpawnActor<APokeMonsterBuildingCutaway>(FVector(0,0,150), FRotator::ZeroRotator);
    TestFalse(TEXT("Relocation is disabled by default for existing buildings"), Building->bUseRelocatedInterior);
    Building->DoorThreshold->SetRelativeLocation(FVector(-450,0,-42.5));
    Building->DoorThreshold->SetBoxExtent(FVector(20,75,107.5));
    Building->bUseRelocatedInterior = true; Building->bUseInteriorCamera = true;
    Building->InteriorCameraDistance = 2400;
    const FVector Outer = Building->DoorThreshold->GetComponentLocation();
    const FVector Inner = Building->RelocatedDoorThreshold->GetComponentLocation();
    const auto* Boom = Player->FindComponentByClass<USpringArmComponent>();
    const auto LagSpeed = Boom->CameraLagSpeed;
    Building->Tick(0);
    const FVector Offsets[] = {{6,0,-59.5},{15,35,-59.5},{-8,-28,-59.5}};
    for (const FVector Offset : Offsets)
    {
        FVector Position = Outer + Offset;
        for (int32 Index=0; Index<100; ++Index)
            Position = Building->MapDoorwayPosition(Building->MapDoorwayPosition(Position,true),false);
        TestTrue(TEXT("Door-relative round trips do not accumulate positional drift"), Position.Equals(Outer+Offset,.001));
    }
    Player->SetActorLocation(Outer+FVector(6,0,-59.5));
    Building->Tick(.1);
    TestFalse(TEXT("Partial entry reversal does not relocate"), Building->IsViewerRelocated());
    Player->SetActorLocation(Outer+FVector(-6,0,-59.5)); Building->Tick(.1);
    TestEqual(TEXT("Reversal restores the original exterior state"), Building->GetCutawayAmount(),0.f);
    for (int32 Cycle=0; Cycle<10; ++Cycle)
    {
        const float Side = Cycle%2 ? 25.f : -25.f;
        Player->SetActorLocation(Outer+FVector(6,Side,-59.5));
        Player->Move(FInputActionValue(FVector2D(0,1))); Player->ConsumeMovementInputVector();
        Player->GetCharacterMovement()->Velocity=FVector(148.4924,-148.4924,0);
        const FVector Velocity=Player->GetVelocity();
        Building->Tick(.2);
        TestEqual(TEXT("Midpoint is completely masked before relocation"),Building->GetRelocationMask(),1.f);
        TestFalse(TEXT("One rendered black frame precedes the cut"),Building->IsViewerRelocated());
        Building->Tick(.01);
        TestTrue(TEXT("Midpoint relocates into the same-map interior"),Building->IsViewerRelocated());
        TestTrue(TEXT("Lateral and floor offsets remain continuous"),Player->GetActorLocation().Equals(Inner+FVector(6,Side,-59.5),.001));
        TestTrue(TEXT("Velocity is preserved at the spatial cut"),Player->GetVelocity().Equals(Velocity,.001));
        TestEqual(TEXT("Held W is preserved"),Player->GetMovementInput(),FVector2D(0,1));
        FMinimalViewInfo View, Expected;
        Player->CalcCamera(0,View); Building->GetInteriorCameraView(Expected);
        TestTrue(TEXT("No camera flight through the map separation"),View.Location.Equals(Expected.Location,.01));
        Building->Tick(.2); Player->Tick(.18);
        TestEqual(TEXT("Camera endpoint uses existing interior input mode"),Player->GetMovementBasisYaw(),0.f);
        TestEqual(TEXT("Interior endpoint unmasks the screen"),Building->GetRelocationMask(),0.f);
        Player->SetActorLocation(Inner+FVector(-6,Side,-59.5));
        Building->Tick(.2); Building->Tick(.01);
        TestFalse(TEXT("Exit returns to the exterior"),Building->IsViewerRelocated());
        TestTrue(TEXT("Exit reproduces the exterior doorway offset"),Player->GetActorLocation().Equals(Outer+FVector(-6,Side,-59.5),.001));
        Building->Tick(.2); Player->Tick(.18);
        TestEqual(TEXT("Exterior basis returns after its existing post-camera blend"),Player->GetMovementBasisYaw(),-45.f);
        TestEqual(TEXT("Completed exit is unmasked"),Building->GetRelocationMask(),0.f);
    }
    // Recovery/load into the remote room must select its view without remapping it.
    const FVector RestoredInside(20000,0,48);
    Player->SetActorLocation(RestoredInside); Building->Tick(0);
    TestTrue(TEXT("Checkpoint restore detects the remote room"),Building->IsViewerRelocated());
    TestTrue(TEXT("Checkpoint restore does not add a second spatial offset"),Player->GetActorLocation().Equals(RestoredInside));
    const FVector RestoredOutside(-900,0,48);
    Player->SetActorLocation(RestoredOutside); Building->Tick(0);
    TestFalse(TEXT("Fallback recovery clears the remote room state"),Building->IsViewerRelocated());
    TestTrue(TEXT("Fallback recovery preserves its own destination"),Player->GetActorLocation().Equals(RestoredOutside));
    TestEqual(TEXT("Fallback recovery leaves no screen mask"),Building->GetRelocationMask(),0.f);
    auto* Blocker=World->SpawnActor<AActor>();
    auto* Obstruction=NewObject<UBoxComponent>(Blocker);
    Blocker->SetRootComponent(Obstruction);
    Obstruction->SetBoxExtent(FVector(50));
    Obstruction->SetCollisionProfileName(TEXT("BlockAll"));
    Obstruction->RegisterComponent();
    Blocker->SetActorLocation(Inner+FVector(6,0,-59.5));
    Player->SetActorLocation(Outer+FVector(6,0,-59.5));
    Building->Tick(.2);
    AddExpectedError(TEXT("relocation destination blocked"),EAutomationExpectedErrorFlags::Contains,1);
    Building->Tick(.01);
    TestFalse(TEXT("Blocked destination never places player inside collision"),Building->IsViewerRelocated());
    TestEqual(TEXT("Rejected relocation removes its screen mask"),Building->GetRelocationMask(),0.f);
    Building->Tick(.2);
    TestEqual(TEXT("Rejected relocation does not loop into another blackout"),Building->GetRelocationMask(),0.f);
    Blocker->Destroy();
    Player->SetActorLocation(Outer+FVector(-10,0,-59.5)); Building->Tick(.1);
    Player->SetActorLocation(Outer+FVector(6,0,-59.5)); Building->Tick(.2); Building->Tick(.01);
    TestTrue(TEXT("A new doorway crossing can retry after obstruction is removed"),Building->IsViewerRelocated());
    TestEqual(TEXT("Movement remains 210 cm/s"),Player->GetCharacterMovement()->MaxWalkSpeed,210.f);
    TestEqual(TEXT("Exterior distance remains at the 2500 cm standard"),Boom->TargetArmLength,2500.f);
    TestTrue(TEXT("Lag remains enabled"),Boom->bEnableCameraLag);
    TestEqual(TEXT("Lag speed unchanged"),Boom->CameraLagSpeed,LagSpeed);
    TestEqual(TEXT("Interaction range unchanged"),Player->GetInteractionRange(),150.f);
    return true;
}
#endif
