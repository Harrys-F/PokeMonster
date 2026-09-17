// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterCreatureSpeciesData.h"

namespace PokeMonsterCreatureAssetTypes
{
	const FPrimaryAssetType CreatureSpecies(TEXT("CreatureSpecies"));
}

FPrimaryAssetId UPokeMonsterCreatureSpeciesData::GetPrimaryAssetId() const
{
	const FName AssetName = InternalId.IsNone() ? GetFName() : InternalId;
	return FPrimaryAssetId(PokeMonsterCreatureAssetTypes::CreatureSpecies, AssetName);
}
