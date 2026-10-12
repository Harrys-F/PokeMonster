#pragma once
#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "PokeMonsterMeshyAnimInstance.generated.h"

/** Two in-place clips plus bounded accessory springs. Never drives gameplay motion. */
UCLASS(Transient, Blueprintable)
class POKEMONSTER_API UPokeMonsterMeshyAnimInstance : public UAnimInstance
{
    GENERATED_BODY()
public:
    UPROPERTY(BlueprintReadOnly, Category="Player Presentation") float WalkAlpha = 0.f;
    UPROPERTY(BlueprintReadOnly, Category="Player Presentation") float WalkPlayRate = 0.f;
    UPROPERTY(BlueprintReadOnly, Category="Player Presentation") float WalkTime = 0.f;
    UPROPERTY(BlueprintReadOnly, Category="Player Presentation") float CapePitch = 0.f;
    UPROPERTY(BlueprintReadOnly, Category="Player Presentation") float CapeSwing = 0.f;
    UPROPERTY(BlueprintReadOnly, Category="Player Presentation") float BagSwing = 0.f;
protected:
    virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
    virtual void DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy) override;
};
