#pragma once

#include "CoreMinimal.h"

/** One roll in [0, 9999] makes tests and scripted encounters reproducible. */
struct POKEMONSTER_API FPokeMonsterCaptureLibrary
{
	static float CalculateChance(int32 CurrentHP, int32 MaxHP, int32 BaseRate, float ItemBonus);
	static bool CheckCapture(float Chance, int32 Roll);
};
