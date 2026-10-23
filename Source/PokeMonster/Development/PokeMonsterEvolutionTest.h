#pragma once
#include "CoreMinimal.h"
#include "Engine/AssetManagerTypes.h"
#if WITH_EDITOR
struct FPokeMonsterCreatureInstance;
class UWorld;
/** Editor-only adapter to the existing progression, offer, UI and save services. */
namespace PokeMonsterEvolutionTest
{
    FGuid SelectedCreature(const UWorld* World);
    bool PrepareConditions(FPokeMonsterCreatureInstance& Creature, FPrimaryAssetId& Target);
}
#endif
