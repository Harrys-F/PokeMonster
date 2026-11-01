#include "PokeMonsterPlayerCharacter.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/PlayerController.h"
#include "Components/CapsuleComponent.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "HAL/IConsoleManager.h"
void APokeMonsterPlayerCharacter::SetThirdPersonCamera(bool Enabled)
{
 if(Enabled==bThirdPersonCamera)return;
 bGamepadMovementBasis=false;
 auto* PC=Cast<APlayerController>(GetController());
 if(Enabled)
 {
  bOriginalActorTick=IsActorTickEnabled();bOriginalCursor=PC?PC->bShowMouseCursor:true;
  // Preserve the current world-facing direction while the camera orbits independently.
  const FVector Facing=GetInteractionWorldDirection();
  LastWorldFacing=Facing;bHasWorldFacing=true;
  ThirdPersonBoom->SetRelativeLocation(FVector(0,0,ThirdPersonHeight-GetCapsuleComponent()->GetScaledCapsuleHalfHeight()));
  ThirdPersonBoom->TargetArmLength=FMath::Clamp(ThirdPersonDistance,ThirdPersonMinDistance,ThirdPersonMaxDistance);
  ThirdPersonBoom->SetWorldRotation(FRotator(-12,Facing.Rotation().Yaw,0));ThirdPersonCamera->FieldOfView=ThirdPersonFOV;
  ThirdPersonBoom->SetComponentTickEnabled(true);FollowCamera->Deactivate();ThirdPersonCamera->Activate();bThirdPersonCamera=true;SetActorTickEnabled(true);RefreshThirdPersonInput();
 }
 else
 {
  bThirdPersonCamera=false;ThirdPersonBoom->SetComponentTickEnabled(false);ThirdPersonCamera->Deactivate();FollowCamera->Activate();
  SetActorTickEnabled(bOriginalActorTick||InteriorCameraSource.IsValid()||bMovementBasisOverride);
  if(PC&&!IsOverworldInputLocked()){PC->SetInputMode(FInputModeGameAndUI());PC->bShowMouseCursor=bOriginalCursor;}
 }
}
void APokeMonsterPlayerCharacter::RefreshThirdPersonInput()
{
 if(auto* PC=Cast<APlayerController>(GetController());PC&&!IsOverworldInputLocked()&&PC->bShowMouseCursor)
 {PC->SetInputMode(FInputModeGameOnly());PC->bShowMouseCursor=false;}
}
void APokeMonsterPlayerCharacter::RotateThirdPersonCamera(FVector2D Delta)
{
 if(!bThirdPersonCamera||IsOverworldInputLocked()||Delta.ContainsNaN())return;
 FRotator R=ThirdPersonBoom->GetComponentRotation();R.Yaw=FRotator::NormalizeAxis(R.Yaw+Delta.X*ThirdPersonMouseSensitivity);
 R.Pitch=FMath::Clamp(R.Pitch-Delta.Y*ThirdPersonMouseSensitivity,-65.f,5.f);R.Roll=0;ThirdPersonBoom->SetWorldRotation(R);
}
void APokeMonsterPlayerCharacter::CameraLook(const FInputActionValue& Value)
{
 if(!Value.Get<FVector2D>().IsNearlyZero())bGamepadMovementBasis=false;
 RotateThirdPersonCamera(Value.Get<FVector2D>());
}
void APokeMonsterPlayerCharacter::GamepadLook(const FInputActionValue& Value)
{
 RotateGamepadCamera(Value.Get<FVector2D>(),GetWorld()->GetDeltaSeconds());
}
void APokeMonsterPlayerCharacter::RotateGamepadCamera(FVector2D Input,float DeltaSeconds)
{
 if(!bThirdPersonCamera||IsOverworldInputLocked()||Input.ContainsNaN()||!FMath::IsFinite(DeltaSeconds)||DeltaSeconds<=0.f)return;
 // Enhanced Input reads raw stick values; one radial deadzone here also covers injected input.
 const float Magnitude=FMath::Min(float(Input.Size()),1.f);
 const float DeadZone=FMath::Clamp(GamepadCameraDeadZone,0.f,.95f);
 if(Magnitude<=DeadZone)return;
 Input=Input.GetSafeNormal()*((Magnitude-DeadZone)/(1.f-DeadZone));
 FRotator Rotation=ThirdPersonBoom->GetComponentRotation();
 Rotation.Yaw=FRotator::NormalizeAxis(Rotation.Yaw+Input.X*GamepadCameraYawSpeed*DeltaSeconds);
 Rotation.Pitch=FMath::Clamp(Rotation.Pitch+Input.Y*GamepadCameraPitchSpeed*DeltaSeconds,-65.f,5.f);
 Rotation.Roll=0.f;ThirdPersonBoom->SetWorldRotation(Rotation);
}
void APokeMonsterPlayerCharacter::GamepadMove(const FInputActionValue& Value)
{
 if(IsOverworldInputLocked())return;
 if(!bThirdPersonCamera){Move(Value);return;}
 const FVector2D Input=Value.Get<FVector2D>().GetClampedToMaxSize(1.f);
 if(Input.IsNearlyZero()){StopGamepadMoving(Value);return;}
 const FVector2D Direction=Input.GetSafeNormal();
 if(!bGamepadMovementBasis||FVector2D::DotProduct(Direction,GamepadMoveDirection)<FMath::Cos(FMath::DegreesToRadians(FMath::Clamp(GamepadDirectionChangeDegrees,.1f,45.f))))
 {
  GamepadMovementYaw=ThirdPersonBoom->GetComponentRotation().Yaw;
  GamepadMoveDirection=Direction;bGamepadMovementBasis=true;
 }
 ApplyMoveInput(FInputActionValue(Input));
}
void APokeMonsterPlayerCharacter::StopGamepadMoving(const FInputActionValue& Value)
{
 bGamepadMovementBasis=false;StopMoving(Value);
}
void APokeMonsterPlayerCharacter::CameraZoom(const FInputActionValue& Value)
{
 if(bThirdPersonCamera&&!IsOverworldInputLocked())ThirdPersonBoom->TargetArmLength=FMath::Clamp(ThirdPersonBoom->TargetArmLength-Value.Get<float>()*35.f,ThirdPersonMinDistance,ThirdPersonMaxDistance);
}
static FAutoConsoleCommandWithWorldAndArgs CameraCommand(TEXT("pm.Camera"),TEXT("ThirdPerson | 2D | Status; session-only camera test, no save changes."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args,UWorld* W)
{
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(W,0));
 if(!P||Args.Num()!=1){UE_LOG(LogTemp,Display,TEXT("pm.Camera ThirdPerson | 2D | Status (active game required)"));return;}
 if(Args[0].Equals(TEXT("ThirdPerson"),ESearchCase::IgnoreCase))P->SetThirdPersonCamera(true);
 else if(Args[0].Equals(TEXT("2D"),ESearchCase::IgnoreCase))P->SetThirdPersonCamera(false);
 else if(!Args[0].Equals(TEXT("Status"),ESearchCase::IgnoreCase)){UE_LOG(LogTemp,Display,TEXT("Unknown camera mode"));return;}
 UE_LOG(LogTemp,Display,TEXT("PM_CAMERA %s"),P->IsThirdPersonCamera()?TEXT("ThirdPerson"):TEXT("2.5D"));
}));
