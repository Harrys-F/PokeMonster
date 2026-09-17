// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "PokeMonsterCreatureInstance.generated.h"

class UPokeMonsterCreatureSpeciesData;

/** Mutable data for one concrete creature. Species-wide values remain in the referenced data asset. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureInstance
{
	GENERATED_BODY()

public:
	static FPokeMonsterCreatureInstance CreateFromSpecies(
		UPokeMonsterCreatureSpeciesData* InSpecies,
		int32 RequestedLevel = 0);

	bool IsValid() const;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Creature")
	FGuid InstanceId;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Creature")
	TSoftObjectPtr<UPokeMonsterCreatureSpeciesData> Species;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Creature", meta = (ClampMin = "1"))
	int32 Level = 1;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Creature", meta = (ClampMin = "0"))
	int32 CurrentHP = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Creature", meta = (ClampMin = "0"))
	int64 Experience = 0;
};
