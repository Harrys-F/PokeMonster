#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterThirdPersonFixedRigTest,"PokeMonster.Player.ThirdPersonFixedHeightAndPitch",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterThirdPersonFixedRigTest::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* P=W->SpawnActor<APokeMonsterPlayerCharacter>();P->SetActorLocation(FVector(0,0,P->GetCapsuleComponent()->GetScaledCapsuleHalfHeight()));P->SetThirdPersonCamera(true);
 P->ThirdPersonBoom->bEnableCameraLag=false;P->ThirdPersonBoom->bDoCollisionTest=false;
 auto Update=[&]{P->ThirdPersonBoom->TickComponent(1.f/60,LEVELTICK_All,nullptr);};
 for(float Wheel:{0.f,1000.f,-1000.f})
 {
  P->CameraZoom(FInputActionValue(Wheel));Update();
  TestTrue(TEXT("Actual camera socket stays at 170cm with flat capsule base at zero, including zoom extremes"),FMath::IsNearlyEqual(P->ThirdPersonCamera->GetComponentLocation().Z,170.,.01));
  TestTrue(TEXT("Actual camera component has fixed minus twelve degree pitch"),FMath::IsNearlyEqual(P->ThirdPersonCamera->GetComponentRotation().Pitch,-12.,.001));
 }
 const auto Before=P->ThirdPersonBoom->GetComponentRotation();P->RotateThirdPersonCamera(FVector2D(0,10000));P->RotateGamepadCamera(FVector2D(.1,1),1);Update();
 TestTrue(TEXT("Vertical input cannot even promote horizontal sub-deadzone noise"),P->ThirdPersonBoom->GetComponentRotation().Equals(Before,.001));
 P->RotateThirdPersonCamera(FVector2D(40000,-40000));Update();TestTrue(TEXT("Full horizontal orbit preserves actual camera pitch"),FMath::IsNearlyEqual(P->ThirdPersonCamera->GetComponentRotation().Pitch,-12.,.001));
 P->SetActorLocation(P->GetActorLocation()+FVector(0,0,80));Update();TestTrue(TEXT("Camera follows height changes rather than locking global world Z"),FMath::IsNearlyEqual(P->ThirdPersonCamera->GetComponentLocation().Z,250.,.01));
 P->SetThirdPersonCamera(false);P->SetThirdPersonCamera(true);Update();TestTrue(TEXT("2D roundtrip restores fixed camera pitch and height"),FMath::IsNearlyEqual(P->ThirdPersonCamera->GetComponentRotation().Pitch,-12.,.001)&&FMath::IsNearlyEqual(P->ThirdPersonCamera->GetComponentLocation().Z,250.,.01));
 return true;
}
#endif
