#pragma once
#include "PokeMonsterNPCAnimInstance.h"
#include "PokeMonsterNPCMotionV3AnimInstance.generated.h"
/** V3-only presentation. V2 proxy and all existing actors remain unchanged. */
UCLASS(Transient, Blueprintable)
class POKEMONSTER_API UPokeMonsterNPCMotionV3AnimInstance : public UPokeMonsterNPCAnimInstance
{
 GENERATED_BODY()
public:
 UPROPERTY(BlueprintReadOnly, Category="NPC Motion V3") float PlantCorrectionCm=0.f;
 virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
 virtual void DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy) override;
};
