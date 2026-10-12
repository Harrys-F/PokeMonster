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
    static ConstructorHelpers::FObjectFinder<UAnimSequence> Idle(TEXT("/Game/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Idle_V2.A_Player_Meshy_Idle_V2"));
    static ConstructorHelpers::FObjectFinder<UAnimSequence> Walk(TEXT("/Game/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Walk_V2.A_Player_Meshy_Walk_V2"));
    if (Mesh.Succeeded()) SetSkeletalMesh(Mesh.Object);
    IdleAnimation = Idle.Object;
    WalkAnimation = Walk.Object;
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

void UPokeMonsterMeshyVisualComponent::UpdatePresentation()
{
    auto* Player = Cast<APokeMonsterPlayerCharacter>(GetOwner());
    if (!Player) return;
    const bool bActive = IsMeshyActive();
    SetVisibility(bActive, true);
    Player->GetCharacterFlipbookComponent()->SetVisibility(!bActive && Player->GetCharacterFlipbookComponent()->GetFlipbook() != nullptr, true);
    if (!bActive) return;
    SetRelativeLocation(FVector(0, 0, -Player->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight()));
    // Rotate only the visual; interaction retains the player's existing world-facing direction.
    SetWorldRotation(FRotator(0, Player->GetInteractionWorldDirection().Rotation().Yaw + ForwardYawOffset, 0));

}

void UPokeMonsterMeshyVisualComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    UpdatePresentation();
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}
