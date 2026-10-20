#pragma once
#include "CoreMinimal.h"
#include "PokeMonsterBattleEnvironment.generated.h"
/** Presentation metadata, never a save identity or gameplay biome rule. */
UENUM(BlueprintType)
enum class EPokeMonsterBattleEnvironment : uint8 { Auto, Meadow, Forest, Cave, Ruins };
