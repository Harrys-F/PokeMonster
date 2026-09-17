#include "PokeMonsterMoveData.h"

FPrimaryAssetId UPokeMonsterMoveData::GetPrimaryAssetId() const
{
	return FPrimaryAssetId(TEXT("CreatureMove"), InternalId.IsNone() ? GetFName() : InternalId);
}

bool UPokeMonsterMoveData::IsConfigured() const
{
	const bool bKnownType = Type >= EPokeMonsterCreatureType::Normal && Type <= EPokeMonsterCreatureType::Steel;
	const bool bValidPower = Category == EPokeMonsterMoveCategory::Status ? BasePower == 0
		: (Category == EPokeMonsterMoveCategory::Physical || Category == EPokeMonsterMoveCategory::Special) && BasePower > 0;
	return !InternalId.IsNone() && !DisplayName.IsEmpty() && bKnownType && bValidPower
		&& Accuracy >= 0 && Accuracy <= 100 && MaxPP > 0
		&& Effect.ChancePercent >= 0 && Effect.ChancePercent <= 100;
}
