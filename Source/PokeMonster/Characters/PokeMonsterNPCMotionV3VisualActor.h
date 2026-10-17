#pragma once
#include "PokeMonsterNPCVisualActor.h"
#include "PokeMonsterNPCMotionV3VisualActor.generated.h"
/** Isolated V3 test presentation. No new gameplay identity or movement. */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterNPCMotionV3VisualActor : public APokeMonsterNPCVisualActor
{
 GENERATED_BODY()
public:
 APokeMonsterNPCMotionV3VisualActor();
};
