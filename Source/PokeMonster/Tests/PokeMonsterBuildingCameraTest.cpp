#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "Camera/CameraComponent.h"
#include "Camera/CameraTypes.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "PaperFlipbookComponent.h"
#include "InputActionValue.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Engine/Level.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterBuildingCameraTest,
    "PokeMonster.Player.BuildingInteriorCamera", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterBuildingCameraTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
    if (!TestNotNull(TEXT("Isolated camera world"), World)) return false;
    GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
    ON_SCOPE_EXIT { GEngine->DestroyWorldContext(World); World->DestroyWorld(false); };
    auto* Player = World->SpawnActor<APokeMonsterPlayerCharacter>(FVector(-400,0,48), FRotator::ZeroRotator);
    auto* Controller = World->SpawnActor<APlayerController>();
    World->AddController(Controller);
    Controller->Possess(Player);
    auto* Building = World->SpawnActor<APokeMonsterBuildingCutaway>(FVector(0,0,150), FRotator::ZeroRotator);
    Building->InteriorArea->SetBoxExtent(FVector(310,310,200));
    Building->DoorThreshold->SetRelativeLocation(FVector(-300,0,-50));
    Building->DoorThreshold->SetBoxExtent(FVector(20,65,100));
    TestFalse(TEXT("Interior camera is opt-in for all existing buildings"), Building->bUseInteriorCamera);
    Building->bUseInteriorCamera = true;
    const auto* Boom = Player->FindComponentByClass<USpringArmComponent>();
    auto* Camera = Player->FindComponentByClass<UCameraComponent>();
    Camera->Activate(true);
    const auto BoomRotation = Boom->GetRelativeRotation();
    const auto SpriteScale = Player->GetSprite()->GetRelativeScale3D();
    TestEqual(TEXT("Outside uses the unchanged exterior yaw"), Player->GetMovementBasisYaw(), -45.f);
    TestFalse(TEXT("Outside mode is exploration"), Player->IsUsingInteriorMovementBasis());
    Building->Tick(0.f);
    FMinimalViewInfo Exterior;
    Player->CalcCamera(0.f, Exterior);
    Player->SetActorLocation(FVector(-294,0,48));
    Building->Tick(.1f);
    TestTrue(TEXT("Threshold starts cutaway and camera together"), Building->IsCutawayActive());
    TestEqual(TEXT("Same quarter progress drives camera"), Building->GetCutawayAmount(), .25f);
    Player->Tick(.1f);
    TestEqual(TEXT("Entry camera transition retains exterior movement basis"), Player->GetMovementBasisYaw(), -45.f);
    TestFalse(TEXT("Entry does not latch interior before camera completion"), Player->IsUsingInteriorMovementBasis());
    FMinimalViewInfo Partial, Interior;
    Player->CalcCamera(0.f, Partial);
    Building->GetInteriorCameraView(Interior);
    TestTrue(TEXT("Camera moves continuously rather than cutting"), !Partial.Location.Equals(Exterior.Location) && !Partial.Location.Equals(Interior.Location));
    TestTrue(TEXT("Yaw rotates towards frontal orientation"), Partial.Rotation.Yaw > Exterior.Rotation.Yaw && Partial.Rotation.Yaw < Interior.Rotation.Yaw);
    Player->SetActorLocation(FVector(-300,0,48));
    Building->Tick(.05f);
    TestTrue(TEXT("Standing on threshold retains interior target"), Building->IsCutawayActive());
    Player->SetActorLocation(FVector(-306,0,48));
    Building->Tick(.04f);
    TestFalse(TEXT("Reversing doorway changes target"), Building->IsCutawayActive());
    TestTrue(TEXT("Reversal preserves partial transition"), FMath::IsNearlyEqual(Building->GetCutawayAmount(), .275f));
    Building->Tick(.2f);
    Player->Tick(.2f);
    TestFalse(TEXT("Partial reversal never latches interior movement"), Player->IsUsingInteriorMovementBasis());
    TestEqual(TEXT("Partial reversal restores original input yaw"), Player->GetMovementBasisYaw(), -45.f);
    FMinimalViewInfo Restored;
    Player->CalcCamera(0.f, Restored);
    FMinimalViewInfo ExpectedExterior;
    Camera->GetCameraView(0.f, ExpectedExterior);
    TestTrue(TEXT("Exterior POV restored exactly at current player position"), Restored.Location.Equals(ExpectedExterior.Location) && Restored.Rotation.Equals(ExpectedExterior.Rotation));
    TestEqual(TEXT("FOV unchanged"), Restored.FOV, 35.f);
    Player->SetActorLocation(FVector(-280,25,48));
    Building->Tick(.4f);
    TestTrue(TEXT("Only the completed entry latches interior input"), Player->IsUsingInteriorMovementBasis());
    TestEqual(TEXT("The input basis has not jumped on the completion frame"), Player->GetMovementBasisYaw(), -45.f);
    Player->Move(FInputActionValue(FVector2D(0,1)));
    Player->ConsumeMovementInputVector();
    Player->Tick(.01f);
    TestEqual(TEXT("Held W starts a bounded post-camera input blend"), Player->GetMovementBasisYaw(), -42.5f);
    TestEqual(TEXT("Held W is never cancelled by the basis change"), Player->GetMovementInput(), FVector2D(0,1));
    Player->Tick(.17f);
    TestEqual(TEXT("Completed input blend uses horizontal interior yaw"), Player->GetMovementBasisYaw(), 0.f);
    const FVector2D Directions[] = { {0,1},{1,1},{1,0},{1,-1},{0,-1},{-1,-1},{-1,0},{-1,1} };
    for (int32 Index = 0; Index < 8; ++Index)
    {
        Player->Move(FInputActionValue(Directions[Index]));
        const FVector Direction = Player->ConsumeMovementInputVector();
        TestTrue(TEXT("Interior directions have no diagonal speed bonus or vertical input"), FMath::IsNearlyEqual(Direction.Size2D(), 1.f) && FMath::IsNearlyZero(Direction.Z));
        TestEqual(TEXT("All eight interior keys select the corresponding view-relative flipbook"), Player->GetFacingDirection(), static_cast<EPokeMonsterFacingDirection>(Index));
        TestTrue(TEXT("Interaction follows the actual movement direction"), Player->GetInteractionWorldDirection().Equals(Direction));
        Player->StopMoving(FInputActionValue(FVector2D::ZeroVector));
        TestTrue(TEXT("Idle retains world facing for interaction"), Player->GetInteractionWorldDirection().Equals(Direction));
    }
    TestTrue(TEXT("Interior sprite plane faces the frontal camera"), Player->GetSprite()->GetComponentRotation().Equals(FRotator(0,90,0)));
    TestEqual(TEXT("Walk speed remains 210 cm/s"), Player->GetCharacterMovement()->MaxWalkSpeed, 210.f);
    TestEqual(TEXT("Interaction range remains 150 cm"), Player->GetInteractionRange(), 150.f);
    Player->CalcCamera(0.f, Interior);
    TestTrue(TEXT("Final view is frontal"), Interior.Rotation.Equals(FRotator(-50,0,0)));
    const FVector FixedLocation = Interior.Location;
    Player->SetActorLocation(FVector(180,-180,48));
    Player->CalcCamera(0.f, Interior);
    TestTrue(TEXT("Interior view stays fixed while walking diagonally"), Interior.Location.Equals(FixedLocation));
    TestEqual(TEXT("Interior FOV stays 35"), Interior.FOV, 35.f);
    TestEqual(TEXT("Overworld boom remains 2500"), Boom->TargetArmLength, 2500.f);
    TestTrue(TEXT("Overworld rotation untouched"), Boom->GetRelativeRotation().Equals(BoomRotation));

    TestTrue(TEXT("Sprite scale unchanged"), Player->GetSprite()->GetRelativeScale3D().Equals(SpriteScale));
    TestTrue(TEXT("Lag stays enabled"), Boom->bEnableCameraLag);
    TestEqual(TEXT("Lag speed unchanged"), Boom->CameraLagSpeed, 6.f);
    TestEqual(TEXT("Lag limit unchanged"), Boom->CameraLagMaxDistance, 180.f);
    Player->SetActorLocation(FVector(-306,0,48));
    Building->Tick(.1f);
    Player->Tick(.1f);
    TestTrue(TEXT("Exit transition retains completed interior mode"), Player->IsUsingInteriorMovementBasis());
    TestEqual(TEXT("Exit transition retains interior yaw"), Player->GetMovementBasisYaw(), 0.f);
    Player->SetActorLocation(FVector(-294,0,48));
    Building->Tick(.1f);
    Player->Tick(.1f);
    TestTrue(TEXT("Re-entering during exit retains the last completed interior mode"), Player->IsUsingInteriorMovementBasis());
    Player->SetActorLocation(FVector(-306,0,48));
    Building->Tick(.4f);
    TestFalse(TEXT("Only completed return unlatches interior"), Player->IsUsingInteriorMovementBasis());
    TestEqual(TEXT("Return does not abruptly jump the input yaw"), Player->GetMovementBasisYaw(), 0.f);
    Player->Tick(.01f);
    TestEqual(TEXT("Exit input blend starts after camera restoration"), Player->GetMovementBasisYaw(), -2.5f);
    Player->Tick(.17f);
    TestEqual(TEXT("Final outside input basis is exactly restored"), Player->GetMovementBasisYaw(), -45.f);
    TestFalse(TEXT("Outside no longer needs a player camera tick"), Player->IsActorTickEnabled());
    Player->SetActorLocation(FVector(-280,0,48));
    Building->Tick(.4f);
    Building->SetActorRotation(FRotator(0,90,0));
    Building->GetInteriorCameraView(Interior);
    TestTrue(TEXT("Frontal view follows building-local doorway orientation"), FMath::IsNearlyEqual(Interior.Rotation.Yaw, 90.f));
    Building->Destroy();
    Player->Tick(.5f);
    Player->CalcCamera(0.f, Restored);
    TestFalse(TEXT("Removed provider clears interior input mode"), Player->IsUsingInteriorMovementBasis());
    TestTrue(TEXT("Removed provider safely returns to exploration"), Restored.Rotation.Equals(Exterior.Rotation));
    auto* SavedMap = LoadObject<UWorld>(nullptr, TEXT("/Game/Maps/Dev_BuildingKitTestMap.Dev_BuildingKitTestMap"));
    if (TestNotNull(TEXT("Saved building test map loads"), SavedMap))
    {
        APokeMonsterBuildingCutaway* SavedCutaway = nullptr;
        for (AActor* Actor : SavedMap->PersistentLevel->Actors)
            if (Actor && Actor->GetActorLabel() == TEXT("WL_Cottage_Cutaway"))
                SavedCutaway = Cast<APokeMonsterBuildingCutaway>(Actor);
        if (TestNotNull(TEXT("Saved Cottage cutaway exists"), SavedCutaway))
        {
            TestTrue(TEXT("Only Cottage opts into the interior camera"), SavedCutaway->bUseInteriorCamera);
            TestEqual(TEXT("Cottage retains the configured 2000 cm distance"), SavedCutaway->InteriorCameraDistance, 2000.f);
            for (AActor* Actor : SavedMap->PersistentLevel->Actors)
            {
                if (!Actor) continue;
                const FString Label = Actor->GetActorLabel();
                const FVector Position = Actor->GetActorLocation();
                if (Label.StartsWith(TEXT("Cottage_Wall")) && (FMath::IsNearlyEqual(FMath::Abs(Actor->GetActorRotation().Yaw), 90.f) || Position.X >= 299.f))
                    TestFalse(TEXT("Both side walls and rear wall stay visible in the saved explicit list"), SavedCutaway->OccludingActors.Contains(Actor));
                if (Label == TEXT("Cottage_WallDoor2m_038"))
                    TestTrue(TEXT("Front door wall stays in the saved list"), SavedCutaway->OccludingActors.Contains(Actor));
                if (Label.StartsWith(TEXT("Cottage_RoofPanel")))
                    TestTrue(TEXT("Roof stays in the saved list"), SavedCutaway->OccludingActors.Contains(Actor));
            }
        }
    }
    return true;
}
#endif
