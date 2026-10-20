#pragma once
#include "CoreMinimal.h"
#include "PokeMonsterBattlePresentationMode.generated.h"
/** Presentation only; both modes share BattleSession, party and persistence. */
UENUM(BlueprintType)
enum class EPokeMonsterBattlePresentationMode : uint8 { ClassicBattle, WorldBattle };
