#include "PokeMonsterCameraVisibilityComponent.h"

#include "Camera/PlayerCameraManager.h"
#include "Components/MeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/KismetMaterialLibrary.h"
#include "Materials/Material.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialParameterCollection.h"
#include "UObject/ConstructorHelpers.h"

UPokeMonsterCameraVisibilityComponent::UPokeMonsterCameraVisibilityComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.TickGroup = TG_PostUpdateWork;
    static ConstructorHelpers::FObjectFinder<UMaterialParameterCollection> Collection(TEXT("/Game/Environment/DevTestMapVisualV2/Materials/MPC_PlayerSight.MPC_PlayerSight"));
    static ConstructorHelpers::FObjectFinder<UMaterial> Crown(TEXT("/Game/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal.M_V2_CrownReveal"));
    static ConstructorHelpers::FObjectFinder<UMaterial> Bark(TEXT("/Game/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase.M_V2_BarkRevealBase"));
    SightCollection = Collection.Object;
    CrownMaterial = Crown.Object;
    BarkMaterial = Bark.Object;
    static ConstructorHelpers::FObjectFinder<UStaticMesh> Oak(TEXT("/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3.SM_WLA_OakAncient_V3"));
    static ConstructorHelpers::FObjectFinder<UStaticMesh> Birch(TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Trees/SM_WLA_Birch_A.SM_WLA_Birch_A"));
    OakMesh = Oak.Object;
    BirchMesh = Birch.Object;
    for (const TCHAR* Suffix : {TEXT("Birch"), TEXT("LeafBirch"), TEXT("LeafDark"), TEXT("LeafLight")})
    {
        const FString OriginalPath = FString::Printf(TEXT("/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_%s.MI_WLA_%s"), Suffix, Suffix);
        const FString RevealPath = FString::Printf(TEXT("/Game/Environment/DevTestMapVisualV2/Materials/MI_V2_%sReveal.MI_V2_%sReveal"), Suffix, Suffix);
        ConstructorHelpers::FObjectFinder<UMaterialInterface> Original(*OriginalPath);
        ConstructorHelpers::FObjectFinder<UMaterialInterface> Reveal(*RevealPath);
        if (Original.Succeeded() && Reveal.Succeeded()) BirchMaterials.Add(Original.Object, Reveal.Object);
    }
}

UMaterialInterface* UPokeMonsterCameraVisibilityComponent::FindRevealMaterial(const UStaticMesh* Mesh, UMaterialInterface* Original) const
{
    if (!Mesh || !Original) return nullptr;
    if (Mesh == OakMesh && (Original->GetMaterial() == CrownMaterial || Original->GetMaterial() == BarkMaterial)) return Original;
    if (Mesh == BirchMesh)
        if (const TObjectPtr<UMaterialInterface>* Reveal = BirchMaterials.Find(Original)) return Reveal->Get();
    return nullptr;
}

void UPokeMonsterCameraVisibilityComponent::BeginPlay()
{
    Super::BeginPlay();
    if (!SightCollection || !CrownMaterial || !BarkMaterial)
    {
        SetComponentTickEnabled(false);
        return;
    }
    // Scan once. Both the tree mesh and its material must explicitly opt in.
    // A building using the same bark/leaf material still cannot be registered.
    for (TActorIterator<AActor> It(GetWorld()); It; ++It)
    {
        TArray<UMeshComponent*> Meshes;
        It->GetComponents(Meshes);
        for (UMeshComponent* Mesh : Meshes)
        {
            const UStaticMeshComponent* StaticMesh = Cast<UStaticMeshComponent>(Mesh);
            if (!StaticMesh) continue;
            FTree Tree;
            Tree.Mesh = Mesh;
            for (int32 Slot = 0; Slot < Mesh->GetNumMaterials(); ++Slot)
            {
                UMaterialInterface* Original = Mesh->GetMaterial(Slot);
                UMaterialInterface* Reveal = FindRevealMaterial(StaticMesh->GetStaticMesh(), Original);
                if (!Reveal) continue;
                if (UMaterialInstanceDynamic* MID = Mesh->CreateDynamicMaterialInstance(Slot, Reveal))
                {
                    MID->SetScalarParameterValue(TEXT("PlayerRevealStrength"), 0.f);
                    Tree.Slots.Add({Slot, Original, MID});
                    Instances.Add(MID);
                }
            }
            if (!Tree.Slots.IsEmpty()) Trees.Add(MoveTemp(Tree));
        }
    }
    if (Trees.IsEmpty()) SetComponentTickEnabled(false);
}

bool UPokeMonsterCameraVisibilityComponent::IsBetweenCameraAndTarget(const FBox& Bounds, const FVector& Camera, const FVector& Target)
{
    const FVector Direction = Target - Camera;
    if (!Bounds.IsValid || Direction.SizeSquared() < 1.f) return false;
    // A small broad-phase margin starts the temporal fade before the actual silhouette.
    // Objects wholly behind the player are rejected even after this expansion.
    const FVector Start = Camera + Direction * .06f;
    const FVector End = Camera + Direction * .995f;
    const double CentreT = FVector::DotProduct(Bounds.GetCenter() - Camera, Direction) / Direction.SizeSquared();
    const double DepthRadius = FVector::DotProduct(Bounds.GetExtent(), Direction.GetAbs()) / Direction.SizeSquared();
    if (CentreT - DepthRadius >= .995 || CentreT + DepthRadius <= .06) return false;
    return FMath::LineBoxIntersection(Bounds.ExpandBy(110.f), Start, End, End - Start);
}

float UPokeMonsterCameraVisibilityComponent::AdvanceFade(float Current, bool bOccluding, float DeltaTime, float Duration)
{
    return FMath::FInterpConstantTo(FMath::Clamp(Current, 0.f, 1.f), bOccluding ? 1.f : 0.f,
        FMath::Max(0.f, DeltaTime), 1.f / FMath::Max(.01f, Duration));
}

void UPokeMonsterCameraVisibilityComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    const APawn* Pawn = Cast<APawn>(GetOwner());
    const APlayerController* PC = Pawn ? Cast<APlayerController>(Pawn->GetController()) : nullptr;
    const bool bValidView = PC && PC->IsLocalController() && PC->PlayerCameraManager;
    const FVector Target = GetOwner()->GetActorLocation() + FVector(0, 0, 35);
    if (bValidView)
    {
        UKismetMaterialLibrary::SetVectorParameterValue(this, SightCollection, TEXT("PlayerSightTarget"), FLinearColor(Target.X, Target.Y, Target.Z, 1.f));
        const FVector Eye = PC->PlayerCameraManager->GetCameraLocation();
        UKismetMaterialLibrary::SetVectorParameterValue(this, SightCollection, TEXT("PlayerSightCamera"), FLinearColor(Eye.X, Eye.Y, Eye.Z, 1.f));
    }
    for (FTree& Tree : Trees)
    {
        UMeshComponent* Mesh = Tree.Mesh.Get();
        if (!Mesh) continue;
        const bool bOccluding = bValidView && IsBetweenCameraAndTarget(Mesh->Bounds.GetBox(), PC->PlayerCameraManager->GetCameraLocation(), Target);
        const float Next = AdvanceFade(Tree.Strength, bOccluding, DeltaTime, FadeDuration);
        if (Next == Tree.Strength) continue;
        Tree.Strength = Next;
        for (const FSlot& Slot : Tree.Slots)
            if (UMaterialInstanceDynamic* MID = Slot.Instance.Get()) MID->SetScalarParameterValue(TEXT("PlayerRevealStrength"), Next);
    }
}

void UPokeMonsterCameraVisibilityComponent::EndPlay(const EEndPlayReason::Type Reason)
{
    for (const FTree& Tree : Trees)
        if (UMeshComponent* Mesh = Tree.Mesh.Get())
            for (const FSlot& Slot : Tree.Slots)
                if (Slot.Original.IsValid() && Mesh->GetMaterial(Slot.Index) == Slot.Instance.Get()) Mesh->SetMaterial(Slot.Index, Slot.Original.Get());
    Trees.Empty();
    Instances.Empty();
    Super::EndPlay(Reason);
}
