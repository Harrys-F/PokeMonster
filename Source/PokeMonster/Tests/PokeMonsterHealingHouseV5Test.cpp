#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Camera/CameraTypes.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"
#include "Engine/Engine.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStableHouseTest,"PokeMonster.Building.StableDoorway.VelocityLoadAndSpeedFactors",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FStableHouseTest::RunTest(const FString&)
{
 auto* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* P=W->SpawnActor<APokeMonsterPlayerCharacter>(FVector(-650,0,50),FRotator(0,30,0));auto* PC=W->SpawnActor<APlayerController>();W->AddController(PC);PC->Possess(P);auto* B=W->SpawnActor<APokeMonsterBuildingCutaway>(FVector(0,0,150),FRotator::ZeroRotator);auto* M=P->GetCharacterMovement();
 TestFalse(TEXT("Existing maps do not opt in"),B->bStableDoorwayTransition);B->bUseRelocatedInterior=true;B->bUseInteriorCamera=true;B->bStableDoorwayTransition=true;B->Tick(0);const FVector Outer=B->DoorThreshold->GetComponentLocation(),Inner=B->RelocatedDoorThreshold->GetComponentLocation();
 for(int32 Speed:{1,2,3})
 {
  M->SetMovementMode(MOVE_Walking);M->Velocity=FVector(210*Speed,0,0);P->SetActorLocation(Outer+FVector(6,0,-57.5));P->Move(FInputActionValue(FVector2D(0,1)));const auto Facing=P->GetActorRotation();
  B->Tick(.1);TestTrue(TEXT("Doorway displacement freezes during the mask"),M->MovementMode==MOVE_None);TestTrue(TEXT("Transition is exposed to save/encounter guards"),B->IsDoorwayTransitionActive());B->Tick(.2);B->Tick(.01);
  TestTrue(TEXT("Landing is safely beyond the entrance camera boundary"),P->GetActorLocation().Equals(Inner+FVector(B->DoorwayLandingDistance,0,-57.5),.01));B->Tick(.21);
  TestTrue(TEXT("Movement resumes at every test speed"),M->MovementMode==MOVE_Walking);TestTrue(TEXT("Velocity restored after the mask"),M->Velocity.Equals(FVector(210*Speed,0,0)));TestTrue(TEXT("No forced player rotation"),P->GetActorRotation().Equals(Facing));TestEqual(TEXT("Held direction survives"),P->GetMovementInput(),FVector2D(0,1));
  P->SetActorLocation(Inner+FVector(-6,0,-57.5));M->Velocity=FVector(-210*Speed,0,0);B->Tick(.2);B->Tick(.01);B->Tick(.21);TestTrue(TEXT("Exit lands outside without remaining inside the threshold"),P->GetActorLocation().Equals(Outer+FVector(-B->DoorwayLandingDistance,0,-57.5),.01));TestFalse(TEXT("Completed exit releases transition guards"),B->IsDoorwayTransitionActive());
 }
 P->SetActorLocation(Outer+FVector(6,0,-57.5));B->Tick(.1);P->SetActorLocation(FVector(20000,0,50));B->SynchronizeViewerAfterLoad();TestTrue(TEXT("Loading restores movement even during an interrupted doorway"),M->MovementMode==MOVE_Walking);TestTrue(TEXT("Load keeps the exact independent saved position"),P->GetActorLocation().Equals(FVector(20000,0,50)));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHouseCameraTest,"PokeMonster.Building.StableDoorway.RoomCameraBoundsAndBlockedLanding",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FHouseCameraTest::RunTest(const FString&)
{
 auto* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};auto* P=W->SpawnActor<APokeMonsterPlayerCharacter>(FVector(20000,0,50),FRotator::ZeroRotator);auto* PC=W->SpawnActor<APlayerController>();W->AddController(PC);PC->Possess(P);auto* B=W->SpawnActor<APokeMonsterBuildingCutaway>(FVector(0,0,150),FRotator::ZeroRotator);B->bUseRelocatedInterior=true;B->bUseInteriorCamera=true;B->bConstrainThirdPersonToRoom=true;B->bStableDoorwayTransition=true;B->Tick(0);
 FMinimalViewInfo V;V.Location=FVector(19000,-2000,172);V.Rotation=FRotator(-12,135,0);V.FOV=75;B->ConstrainThirdPersonView(V);TestTrue(TEXT("Camera stays within four opaque room walls"),V.Location.X>=19485&&V.Location.Y>=-465);TestEqual(TEXT("Camera ground height unchanged"),V.Location.Z,172.);TestEqual(TEXT("Fixed third-person pitch unchanged"),V.Rotation.Pitch,-12.);TestEqual(TEXT("Yaw and FOV unchanged"),V.FOV,75.f);
 const FVector Outer=B->DoorThreshold->GetComponentLocation(),Inner=B->RelocatedDoorThreshold->GetComponentLocation();P->SetActorLocation(Outer+FVector(-160,0,-57.5));B->SynchronizeViewerAfterLoad();auto* Blocker=W->SpawnActor<AActor>();auto* Box=NewObject<UBoxComponent>(Blocker);Blocker->SetRootComponent(Box);Box->SetBoxExtent(FVector(55));Box->SetCollisionProfileName(TEXT("BlockAll"));Box->RegisterComponent();Blocker->SetActorLocation(Inner+FVector(B->DoorwayLandingDistance,0,-57.5));P->GetCharacterMovement()->SetMovementMode(MOVE_Walking);P->SetActorLocation(Outer+FVector(6,0,-57.5));B->Tick(.2);AddExpectedError(TEXT("relocation destination blocked"),EAutomationExpectedErrorFlags::Contains,1);B->Tick(.01);TestFalse(TEXT("A blocked landing never relocates"),B->IsViewerRelocated());TestTrue(TEXT("A rejected transition cannot leave movement frozen"),P->GetCharacterMovement()->MovementMode==MOVE_Walking);return true;
}
#endif
