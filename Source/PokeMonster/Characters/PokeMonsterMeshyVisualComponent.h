#pragma once

#include "CoreMinimal.h"
#include "Components/SkeletalMeshComponent.h"
#include "PokeMonsterMeshyVisualComponent.generated.h"

class UAnimSequence;

/** Presentation only. The Paper2D player, movement and camera remain the owner. */
UCLASS(ClassGroup=(PokeMonster), meta=(BlueprintSpawnableComponent))
class POKEMONSTER_API UPokeMonsterMeshyVisualComponent : public USkeletalMeshComponent
{
    GENERATED_BODY()
public:
    UPokeMonsterMeshyVisualComponent();
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Player Presentation")
    bool bUseMeshyVisual = true;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Player Presentation")
    TObjectPtr<UAnimSequence> IdleAnimation;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Player Presentation")
    TObjectPtr<UAnimSequence> WalkAnimation;
    /** Imported model faces +X; an alternate mesh may require an offset. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Player Presentation")
    float ForwardYawOffset = 0.f;
    /** Reference gameplay speed for proportional in-place animation playback. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Player Presentation", meta=(ClampMin="1"))
    float AuthoredWalkSpeed = 210.f;

    UFUNCTION(BlueprintPure, Category="Player Presentation")
    bool IsMeshyActive() const;
    UFUNCTION(BlueprintCallable, Category="Player Presentation")
    void SetMeshyEnabled(bool bEnabled);
    void UpdatePresentation();

};
