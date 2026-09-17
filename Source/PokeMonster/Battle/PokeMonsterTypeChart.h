#pragma once

#include "CoreMinimal.h"
#include "../Creatures/PokeMonsterCreatureTypes.h"

/** Central generation-two type table; independent of worlds, assets and creature state. */
namespace PokeMonsterTypeChart
{
	POKEMONSTER_API bool IsValidType(EPokeMonsterCreatureType Type);
	/** Primary must be a real type. None is allowed only for Secondary. Invalid input returns -1. */
	POKEMONSTER_API float GetMultiplier(EPokeMonsterCreatureType Attack, EPokeMonsterCreatureType Primary,
		EPokeMonsterCreatureType Secondary = EPokeMonsterCreatureType::None);
}
