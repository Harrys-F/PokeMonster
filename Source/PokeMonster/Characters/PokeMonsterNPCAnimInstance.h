#pragma once
#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "PokeMonsterNPCAnimInstance.generated.h"
/** Configurable presentation only. Source NPC retains movement, interaction and story state. */
UCLASS(Transient, Blueprintable)
class POKEMONSTER_API UPokeMonsterNPCAnimInstance : public UAnimInstance
{
 GENERATED_BODY()
public:
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float ConversationAlpha = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float WalkAlpha = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float RunAlpha = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float GreetingAlpha = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float FootCorrectionCm = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float WalkPlayRate = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float TurnAlpha = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float CapePitch = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float CapeSwing = 0.f;
 UPROPERTY(BlueprintReadOnly, Category="NPC Presentation") float BagSwing = 0.f;
 virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
 virtual void DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy) override;
};
