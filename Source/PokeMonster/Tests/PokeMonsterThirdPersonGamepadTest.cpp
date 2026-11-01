#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "GameFramework/SpringArmComponent.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "InputMappingContext.h"
#include "InputAction.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterThirdPersonGamepadTest,"PokeMonster.Player.ThirdPersonDefaultAndGamepad",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterThirdPersonGamepadTest::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* P=W->SpawnActor<APokeMonsterPlayerCharacter>();P->DispatchBeginPlay();
 TestTrue(TEXT("Actual BeginPlay activates Third Person"),P->IsThirdPersonCamera());
 auto Mapped=[&](const UInputAction* A,FKey K){return P->DefaultMappingContext->GetMappings().ContainsByPredicate([&](const auto& X){return X.Action==A&&X.Key==K;});};
 TestTrue(TEXT("Separate stick source shares movement, right stick supplies camera rate"),Mapped(P->GamepadMoveAction,EKeys::Gamepad_Left2D)&&Mapped(P->GamepadLookAction,EKeys::Gamepad_Right2D));
 TestTrue(TEXT("Mouse retained separately from rate input"),Mapped(P->CameraLookAction,EKeys::Mouse2D));
 const FRotator Initial=P->ThirdPersonBoom->GetComponentRotation();
 for(auto Noise:{FVector2D::ZeroVector,FVector2D(.1,.1),FVector2D(.15,0)})P->RotateGamepadCamera(Noise,1.f);
 TestTrue(TEXT("Neutral and radial deadzone never drift"),Initial.Equals(P->ThirdPersonBoom->GetComponentRotation(),.001f));
 for(int Rate:{30,120})
 {
  P->ThirdPersonBoom->SetWorldRotation(FRotator(0,0,0));
  for(int I=0;I<Rate;++I)P->RotateGamepadCamera(FVector2D(1,0),1.f/Rate);
  TestTrue(TEXT("Full horizontal rate is 120 degrees per second at different frame rates"),FMath::IsNearlyEqual(P->ThirdPersonBoom->GetComponentRotation().Yaw,120.,.01));
 }
 P->ThirdPersonBoom->SetWorldRotation(FRotator(0,0,0));P->RotateGamepadCamera(FVector2D(0,1),.1f);
 TestEqual(TEXT("Stick up leaves arm level"),P->ThirdPersonBoom->GetComponentRotation().Pitch,0.0);
 P->RotateGamepadCamera(FVector2D(0,1),1);P->RotateGamepadCamera(FVector2D(0,-1),2);
 TestEqual(TEXT("Both vertical stick directions remain locked"),P->ThirdPersonBoom->GetComponentRotation().Pitch,0.0);
 P->ThirdPersonBoom->SetWorldRotation(FRotator(0,0,0));P->GamepadMove(FInputActionValue(FVector2D(0,1)));const FVector Forward=P->ConsumeMovementInputVector();
 P->RotateGamepadCamera(FVector2D(1,0),.5f);P->GamepadMove(FInputActionValue(FVector2D(0,1)));
 TestTrue(TEXT("Held direction retains world movement while camera independently orbits"),P->ConsumeMovementInputVector().Equals(Forward,.001f));
 P->StopGamepadMoving(FInputActionValue(FVector2D::ZeroVector));P->GamepadMove(FInputActionValue(FVector2D(0,1)));
 TestTrue(TEXT("Re-engaging stick uses current camera yaw"),P->ConsumeMovementInputVector().GetSafeNormal().Equals(FRotator(0,60,0).Vector(),.001f));
 P->GamepadMove(FInputActionValue(FVector2D(1,1)));TestTrue(TEXT("Gamepad diagonal cannot gain speed"),P->ConsumeMovementInputVector().Size()<=1.001f);
 P->SetOverworldInputLocked(true);const FRotator Locked=P->ThirdPersonBoom->GetComponentRotation();P->RotateGamepadCamera(FVector2D(1,1),1);P->GamepadMove(FInputActionValue(FVector2D(0,1)));
 TestTrue(TEXT("Menus/dialogs/battles block stick look and movement"),P->ThirdPersonBoom->GetComponentRotation().Equals(Locked)&&P->ConsumeMovementInputVector().IsNearlyZero());P->SetOverworldInputLocked(false);
 P->SetThirdPersonCamera(false);P->RotateGamepadCamera(FVector2D(1,1),1);TestTrue(TEXT("Right stick does not rotate retained 2.5D camera"),P->ThirdPersonBoom->GetComponentRotation().Equals(Locked));
 UPokeMonsterSaveSubsystem::SynchronizeRestoredPlayer(P);TestTrue(TEXT("Existing load synchronization returns to default Third Person"),P->IsThirdPersonCamera());
 P->Move(FInputActionValue(FVector2D(0,1)));TestTrue(TEXT("Keyboard still follows current camera yaw"),P->ConsumeMovementInputVector().GetSafeNormal().Equals(FRotator(0,P->ThirdPersonBoom->GetComponentRotation().Yaw,0).Vector(),.001f));
 return true;
}
#endif
