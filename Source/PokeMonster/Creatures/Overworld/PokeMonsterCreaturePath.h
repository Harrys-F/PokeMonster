#pragma once
#include "CoreMinimal.h"
#include "Templates/Function.h"

/** Bounded local A*; predicates use the actual world's ground/collision, not a new NavMesh asset. */
struct POKEMONSTER_API FPokeMonsterCreaturePath
{
	static bool Find(const FVector& Start, const FVector& Goal,
		TFunctionRef<bool(const FVector&, FVector&)> Project,
		TFunctionRef<bool(const FVector&, const FVector&)> CanCross,
		TArray<FVector>& Out, float CellSize = 65.f, int32 MaximumExpanded = 512);
};
