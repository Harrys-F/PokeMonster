#pragma once

#include "CoreMinimal.h"
#include "Engine/BlendableInterface.h"
#include "UObject/Object.h"
#include "PokeMonsterTemporalAABlendable.generated.h"

/** A map-owned AA choice; no lighting, global CVars or gameplay state are changed. */
UCLASS(BlueprintType, EditInlineNew, DefaultToInstanced)
class POKEMONSTER_API UPokeMonsterTemporalAABlendable final : public UObject, public IBlendableInterface
{
    GENERATED_BODY()
public:
    virtual void OverrideBlendableSettings(FSceneView& View, float Weight) const override;
};
