#include "PokeMonsterMeshyVisualComponent.h"
#include "PokeMonsterPlayerCharacter.h"
#include "Animation/AnimSequence.h"
#include "PokeMonsterMeshyAnimInstance.h"
#include "Components/CapsuleComponent.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "PaperFlipbookComponent.h"
#include "UObject/ConstructorHelpers.h"

UPokeMonsterMeshyVisualComponent::UPokeMonsterMeshyVisualComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    SetCollisionEnabled(ECollisionEnabled::NoCollision);
    SetGenerateOverlapEvents(false);
    SetCanEverAffectNavigation(false);
    SetAnimInstanceClass(UPokeMonsterMeshyAnimInstance::StaticClass());
    VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickPoseWhenRendered;
    static ConstructorHelpers::FObjectFinder<USkeletalMesh> Mesh(TEXT("/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2.SK_Player_Meshy_V2"));
    static ConstructorHelpers::FObjectFinder<UAnimSequence> Idle(TEXT("/Game/Characters/YoungTrainer/AnimationV6/A_Player_Idle_V6.A_Player_Idle_V6"));
    static ConstructorHelpers::FObjectFinder<UAnimSequence> Walk(TEXT("/Game/Characters/YoungTrainer/AnimationV6/A_Player_Walk_V6.A_Player_Walk_V6"));
    if (Mesh.Succeeded()) SetSkeletalMesh(Mesh.Object);
    IdleAnimation = Idle.Object;
    WalkAnimation = Walk.Object;
    static ConstructorHelpers::FObjectFinder<UAnimSequence> Run(TEXT("/Game/Characters/YoungTrainer/AnimationV6/A_Player_Run_V6.A_Player_Run_V6"));
    RunAnimation = Run.Object;
}

bool UPokeMonsterMeshyVisualComponent::IsMeshyActive() const
{
    return bUseMeshyVisual && GetSkeletalMeshAsset() && IdleAnimation && WalkAnimation;
}

void UPokeMonsterMeshyVisualComponent::BeginPlay()
{
    Super::BeginPlay();
    if (const auto* Player = Cast<APokeMonsterPlayerCharacter>(GetOwner()))
        AddTickPrerequisiteComponent(Player->GetCharacterMovement());
    UpdatePresentation();
}

void UPokeMonsterMeshyVisualComponent::SetMeshyEnabled(bool bEnabled)
{
    bUseMeshyVisual = bEnabled;
    UpdatePresentation();
}

void UPokeMonsterMeshyVisualComponent::UpdatePresentation(float DeltaTime)
{
    auto* Player = Cast<APokeMonsterPlayerCharacter>(GetOwner());
    if (!Player) return;
    const bool bActive = IsMeshyActive();
    SetVisibility(bActive, true);
    Player->GetCharacterFlipbookComponent()->SetVisibility(!bActive && Player->GetCharacterFlipbookComponent()->GetFlipbook() != nullptr, true);
    if (!bActive) return;
    SetRelativeLocation(FVector(0, 0, -Player->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight()));
    // Rotate only the visual; interaction retains the player's existing world-facing direction.
    const float TargetYaw=Player->GetInteractionWorldDirection().Rotation().Yaw+ForwardYawOffset;
    float Yaw=GetComponentRotation().Yaw;
    if (!bHaveVisualFacing || DeltaTime<=0.f) { Yaw=TargetYaw;VisualAngularVelocity=0.f;bHaveVisualFacing=true; }
    else
    {
        Yaw=AdvanceVisualYaw(Yaw,TargetYaw,VisualAngularVelocity,DeltaTime);
    }
    SetWorldRotation(FRotator(0,Yaw,0));

}

void UPokeMonsterMeshyVisualComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    UpdatePresentation(DeltaTime);
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}


float UPokeMonsterMeshyVisualComponent::AdvanceVisualYaw(float Current,float Target,float& Velocity,float Delta)
{
 if (!FMath::IsFinite(Current)||!FMath::IsFinite(Target)||!FMath::IsFinite(Delta)||Delta<=0.f) return Current;
 const float Difference=FMath::FindDeltaAngleDegrees(Current,Target);
 const float Desired=FMath::Clamp(Difference/FMath::Max(Delta,.001f),-720.f,720.f);
 Velocity=FMath::FInterpConstantTo(Velocity,Desired,Delta,4800.f);
 const float Step=Velocity*Delta;
 if (FMath::Abs(Step)>=FMath::Abs(Difference) && Step*Difference>=0.f) { Velocity=0.f;return Target; }
 return Current+Step;
}
