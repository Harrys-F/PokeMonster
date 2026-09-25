#include "PokeMonsterCaptureLibrary.h"

float FPokeMonsterCaptureLibrary::CalculateChance(int32 CurrentHP, int32 MaxHP, int32 BaseRate, float ItemBonus)
{
	if (MaxHP <= 0 || CurrentHP <= 0 || CurrentHP > MaxHP || BaseRate <= 0 || BaseRate > 255
		|| !FMath::IsFinite(ItemBonus) || ItemBonus <= 0.0f) return 0.0f;
	const float HealthFactor = (3.0f * MaxHP - 2.0f * CurrentHP) / (3.0f * MaxHP);
	return FMath::Clamp((float(BaseRate) / 255.0f) * HealthFactor * ItemBonus, 0.0f, 1.0f);
}

bool FPokeMonsterCaptureLibrary::CheckCapture(float Chance, int32 Roll)
{
	return FMath::IsFinite(Chance) && Roll >= 0 && Roll < 10000
		&& float(Roll) < FMath::Clamp(Chance, 0.0f, 1.0f) * 10000.0f;
}
