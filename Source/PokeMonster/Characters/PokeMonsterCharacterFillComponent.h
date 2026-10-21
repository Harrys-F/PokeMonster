#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PokeMonsterCharacterFillComponent.generated.h"
class UPointLightComponent;
class USkeletalMeshComponent;
class UStaticMeshComponent;
class UDirectionalLightComponent;

/** Conservative canopy-core estimate, not a renderer shadow-buffer readback. */
UCLASS(ClassGroup=(PokeMonster))
class POKEMONSTER_API UPokeMonsterCharacterFillComponent : public UActorComponent
{
 GENERATED_BODY()
public:
 UPokeMonsterCharacterFillComponent();
 virtual void BeginPlay() override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 virtual void TickComponent(float Delta,ELevelTick Type,FActorComponentTickFunction* Function) override;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) float EstimatedShade=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) float FillLumens=0;
 static float CanopyOcclusion(const FVector& Point,const FVector& Sunward,const FBox& TreeBounds);
private:
 UPROPERTY(Transient) TObjectPtr<UPointLightComponent> Fill;
 UPROPERTY(Transient) TObjectPtr<USkeletalMeshComponent> Mesh;
 TArray<TWeakObjectPtr<UStaticMeshComponent>> Trees;
 TWeakObjectPtr<UDirectionalLightComponent> Sun;
 bool bOriginallyChannel2=false;
 float SampleRemaining=0;
};
