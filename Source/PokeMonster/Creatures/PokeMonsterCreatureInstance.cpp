// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterCreatureInstance.h"

#include "PokeMonsterCreatureSpeciesData.h"

FPokeMonsterCreatureInstance FPokeMonsterCreatureInstance::CreateFromSpecies(
	UPokeMonsterCreatureSpeciesData* InSpecies,
	const int32 RequestedLevel)
{
	FPokeMonsterCreatureInstance Instance;
	if (!::IsValid(InSpecies))
	{
		return Instance;
	}

	Instance.InstanceId = FGuid::NewGuid();
	Instance.Species = InSpecies;
	Instance.Level = RequestedLevel > 0 ? RequestedLevel : InSpecies->GetStartingLevel();
	Instance.CurrentHP = InSpecies->GetBaseStats().HP;
	return Instance;
}

bool FPokeMonsterCreatureInstance::IsValid() const
{
	return InstanceId.IsValid() && !Species.IsNull() && Level > 0;
}
