#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PokeMonsterCameraVisibilityComponent.generated.h"

class UMaterial;
class UMaterialInterface;
class UMaterialInstanceDynamic;
class UMaterialParameterCollection;
class UMeshComponent;

/** Visual-only finite camera/player sight cone for the existing scoped tree materials. */
UCLASS(ClassGroup=(Camera), meta=(BlueprintSpawnableComponent))
class POKEMONSTER_API UPokeMonsterCameraVisibilityComponent : public UActorComponent
{
    GENERATED_BODY()
public:
    UPokeMonsterCameraVisibilityComponent();
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type Reason) override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Camera Visibility", meta=(ClampMin="0.01"))
    float FadeDuration = .25f;

    /** Broad phase only; the shader clips the exact finite perspective cone per fragment. */
    static bool IsBetweenCameraAndTarget(const FBox& Bounds, const FVector& Camera, const FVector& Target);
    static float AdvanceFade(float Current, bool bOccluding, float DeltaTime, float Duration);

private:
    struct FSlot
    {
        int32 Index = 0;
        TWeakObjectPtr<UMaterialInterface> Original;
        TWeakObjectPtr<UMaterialInstanceDynamic> Instance;
    };
    struct FTree
    {
        TWeakObjectPtr<UMeshComponent> Mesh;
        TArray<FSlot> Slots;
        float Strength = 0.f;
    };
    TArray<FTree> Trees;
    UPROPERTY(Transient) TArray<TObjectPtr<UMaterialInstanceDynamic>> Instances;
    UPROPERTY() TObjectPtr<UMaterialParameterCollection> SightCollection;
    UPROPERTY() TObjectPtr<UMaterial> CrownMaterial;
    UPROPERTY() TObjectPtr<UMaterial> BarkMaterial;
};
