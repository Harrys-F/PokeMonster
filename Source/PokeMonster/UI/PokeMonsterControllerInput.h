#pragma once

#include "CoreMinimal.h"
#include "InputCoreTypes.h"

class IInputProcessor;

/** Switch labels follow the selected macOS backend, not Xbox face-button positions. */
namespace PokeMonsterControllerInput
{
 POKEMONSTER_API FKey Confirm();
 POKEMONSTER_API FKey Cancel();
 POKEMONSTER_API FKey QuickMenu();
 POKEMONSTER_API bool IsGamepadActive();
 POKEMONSTER_API void ObserveKey(FKey Key);
 POKEMONSTER_API TSharedRef<IInputProcessor> MakeObserver();
}
