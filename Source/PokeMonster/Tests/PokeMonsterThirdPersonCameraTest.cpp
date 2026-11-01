#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Camera/CameraComponent.h"
#include "Camera/CameraTypes.h"
#include "GameFramework/SpringArmComponent.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterThirdPersonCameraTest,"PokeMonster.Player.ThirdPersonCamera",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterThirdPersonCameraTest::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* P=W->SpawnActor<APokeMonsterPlayerCharacter>();const auto Location=P->GetActorLocation();const auto Rot=P->CameraBoom->GetRelativeRotation();const auto Offset=P->CameraBoom->TargetOffset;const float Length=P->CameraBoom->TargetArmLength,FOV=P->FollowCamera->FieldOfView;const float Yaw=P->GetMovementBasisYaw();
 TestFalse(TEXT("Default is retained 2.5D"),P->IsThirdPersonCamera());
 for(int I=0;I<10;++I)
 {
  const FVector Facing=P->GetInteractionWorldDirection();
  P->SetThirdPersonCamera(true);P->SetThirdPersonCamera(true);
  TestTrue(TEXT("Initial camera looks in the player's current facing direction"),P->ThirdPersonBoom->GetForwardVector().GetSafeNormal2D().Equals(Facing.GetSafeNormal2D(),.001f));
  TestTrue(TEXT("Switch preserves world-facing direction"),P->GetInteractionWorldDirection().Equals(Facing,.001f));TestTrue(TEXT("Third person camera active"),P->ThirdPersonCamera->IsActive());TestTrue(TEXT("Probe collision enabled"),P->ThirdPersonBoom->bDoCollisionTest);
  P->RotateThirdPersonCamera(FVector2D(750,-10000));TestEqual(TEXT("Pitch cannot flip above player"),P->ThirdPersonBoom->GetComponentRotation().Pitch,5.0);
  P->Move(FInputActionValue(FVector2D(1,1)));auto D=P->ConsumeMovementInputVector();TestTrue(TEXT("Diagonal input never exceeds unit length"),D.Size()<=1.001f);
  P->Move(FInputActionValue(FVector2D(0,1)));D=P->ConsumeMovementInputVector();TestTrue(TEXT("Forward follows horizontal orbit yaw"),D.GetSafeNormal().Equals(FRotator(0,P->GetMovementBasisYaw(),0).Vector(),.001f));
  P->SetOverworldInputLocked(true);const auto Before=P->ThirdPersonBoom->GetComponentRotation();P->RotateThirdPersonCamera(FVector2D(800,800));TestTrue(TEXT("UI/battle input lock also blocks look"),P->ThirdPersonBoom->GetComponentRotation().Equals(Before));P->SetOverworldInputLocked(false);
  P->SetThirdPersonCamera(false);TestTrue(TEXT("Original camera active"),P->FollowCamera->IsActive());TestFalse(TEXT("Third person no longer active"),P->ThirdPersonCamera->IsActive());TestTrue(TEXT("No teleport during mode switch"),P->GetActorLocation().Equals(Location));
  TestTrue(TEXT("Original arm rotation untouched"),P->CameraBoom->GetRelativeRotation().Equals(Rot));TestTrue(TEXT("Original target offset untouched"),P->CameraBoom->TargetOffset.Equals(Offset));TestEqual(TEXT("Original distance unchanged"),P->CameraBoom->TargetArmLength,Length);TestEqual(TEXT("Original FOV unchanged"),P->FollowCamera->FieldOfView,FOV);TestEqual(TEXT("Original movement basis restored"),P->GetMovementBasisYaw(),Yaw);
 }
 return true;
}
#endif
