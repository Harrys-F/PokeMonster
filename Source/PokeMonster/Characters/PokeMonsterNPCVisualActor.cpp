#include "PokeMonsterNPCVisualActor.h"
#include "PokeMonsterNPCAnimInstance.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "Animation/AnimSequence.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "PaperSpriteComponent.h"
APokeMonsterNPCVisualActor::APokeMonsterNPCVisualActor()
{
 PrimaryActorTick.bCanEverTick = true;
 PrimaryActorTick.bStartWithTickEnabled = false;
 Visual = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("NPCVisual"));
 SetRootComponent(Visual);
 Visual->SetCollisionEnabled(ECollisionEnabled::NoCollision);
 Visual->SetGenerateOverlapEvents(false);
 Visual->SetCanEverAffectNavigation(false);
 Visual->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickPoseWhenRendered;
 Visual->bEnableUpdateRateOptimizations = true;
 Visual->SetAnimInstanceClass(UPokeMonsterNPCAnimInstance::StaticClass());
}
void APokeMonsterNPCVisualActor::RefreshPresentation()
{
 const bool bReady = bUseVisual && SourceActor && Visual->GetSkeletalMeshAsset() && IdleAnimation;
 Visual->SetVisibility(bReady, true);
 if (SourceActor)
 {
  auto* Sprite = SourceActor->FindComponentByClass<UPaperSpriteComponent>();
  if (Sprite && FallbackSprite != Sprite)
  {
   if (FallbackSprite) FallbackSprite->SetVisibility(bFallbackWasVisible);
   FallbackSprite = Sprite; bFallbackWasVisible = Sprite->IsVisible();
  }
 }
 if (FallbackSprite) FallbackSprite->SetVisibility(bReady ? false : bFallbackWasVisible);
}
void APokeMonsterNPCVisualActor::OnConstruction(const FTransform& Transform)
{
 Super::OnConstruction(Transform); RefreshPresentation();
}
void APokeMonsterNPCVisualActor::BeginPlay()
{
 Super::BeginPlay();
 if (!SourceActor) SourceActor = GetAttachParentActor();
 RefreshPresentation();
 if (auto* GI = GetGameInstance())
  if (auto* Dialogue = GI->GetSubsystem<UPokeMonsterDialogueSubsystem>())
   Dialogue->OnDialogueChanged.AddUniqueDynamic(this, &APokeMonsterNPCVisualActor::HandleDialogueChanged);
 HandleDialogueChanged();
}
void APokeMonsterNPCVisualActor::HandleDialogueChanged()
{
 auto* GI = GetGameInstance(); auto* Dialogue = GI ? GI->GetSubsystem<UPokeMonsterDialogueSubsystem>() : nullptr;
 bConversing = bUseVisual && Dialogue && Dialogue->IsDialogueActive() && Dialogue->GetActiveSource() == SourceActor;
 if (bConversing)
  if (const auto* Player = UGameplayStatics::GetPlayerPawn(this, 0))
  {
   const FVector Direction = Player->GetActorLocation() - GetActorLocation();
   DesiredRotation = FRotator(0, Direction.Rotation().Yaw, 0); SetActorTickEnabled(true);
  }
}
void APokeMonsterNPCVisualActor::SampleMotion(float DeltaSeconds)
{
 if (!SourceActor || !bEnableMotionPresentation || !bUseVisual) { bHaveSourceSample = false; PresentationSpeed = 0.f; return; }
 const double Now = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.;
 const float SampleDelta = GetWorld() && GetWorld()->HasBegunPlay() && bHaveSourceSample
  ? static_cast<float>(Now - PreviousSourceSampleTime) : DeltaSeconds;
 if (bHaveSourceSample && SampleDelta <= SMALL_NUMBER) return;
 const FVector Location = SourceActor->GetActorLocation();
 FVector Velocity = SourceActor->GetVelocity();
 // Also support an existing source moved by a path/transform controller, without adding movement logic here.
 if (Velocity.IsNearlyZero() && bHaveSourceSample && SampleDelta > SMALL_NUMBER && SampleDelta < .25f)
 {
  const FVector Displacement = Location - PreviousSourceLocation;
  if (Displacement.Size2D() < 600.f * SampleDelta) Velocity = Displacement / SampleDelta;
 }
 PreviousSourceLocation = Location; PreviousSourceSampleTime = Now; bHaveSourceSample = true;
 PresentationSpeed = Velocity.Size2D();
 if (!bConversing && PresentationSpeed > 3.f)
 {
  const float TargetYaw = Velocity.Rotation().Yaw + ForwardYawOffset;
  FRotator Rotation = GetActorRotation();
  Rotation.Yaw = FMath::FixedTurn(Rotation.Yaw, TargetYaw, FacingDegreesPerSecond * FMath::Min(DeltaSeconds, .1f));
  SetActorRotation(Rotation); // The source NPC's gameplay transform is never changed.
 }
}
void APokeMonsterNPCVisualActor::Tick(float DeltaSeconds)
{
 Super::Tick(DeltaSeconds);
 const FRotator Next = FMath::RInterpTo(GetActorRotation(), DesiredRotation, DeltaSeconds, 8.f);
 SetActorRotation(Next);
 if (Next.Equals(DesiredRotation, .2f)) SetActorTickEnabled(false);
}
void APokeMonsterNPCVisualActor::EndPlay(const EEndPlayReason::Type Reason)
{
 if (auto* GI = GetGameInstance())
  if (auto* Dialogue = GI->GetSubsystem<UPokeMonsterDialogueSubsystem>())
   Dialogue->OnDialogueChanged.RemoveDynamic(this, &APokeMonsterNPCVisualActor::HandleDialogueChanged);
 if (FallbackSprite) FallbackSprite->SetVisibility(bFallbackWasVisible);
 Super::EndPlay(Reason);
}
