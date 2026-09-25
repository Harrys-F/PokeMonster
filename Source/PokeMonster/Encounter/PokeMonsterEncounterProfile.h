#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "PokeMonsterEncounterProfile.generated.h"

class UPokeMonsterCreatureSpeciesData;
class UPokeMonsterMoveData;

UENUM(BlueprintType)
enum class EPokeMonsterEncounterTime : uint8 { Any, Morning, Day, Evening, Night };

/** The optional fields describe the conditions at the moment of the encounter. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterEncounterContext
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") EPokeMonsterEncounterTime Time = EPokeMonsterEncounterTime::Day;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") FName RegionId;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") TArray<FName> ActiveConditions;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterWildEncounterEntry
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter") TSoftObjectPtr<UPokeMonsterCreatureSpeciesData> Species;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter", meta=(ClampMin="1", ClampMax="100")) int32 MinLevel = 1;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter", meta=(ClampMin="1", ClampMax="100")) int32 MaxLevel = 1;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter", meta=(ClampMin="0")) int32 Weight = 1;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter") EPokeMonsterEncounterTime Time = EPokeMonsterEncounterTime::Any;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter") FName RegionId;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter") FName RequiredCondition;
	/** At most four initial moves; PP belongs to the rolled creature, not this profile. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter") TArray<TSoftObjectPtr<UPokeMonsterMoveData>> Moves;

	bool Matches(const FPokeMonsterEncounterContext& Context) const;
};

/** Shared encounter pool for visible actors, zones, and later scripted/random sources. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterEncounterProfile : public UPrimaryDataAsset
{
	GENERATED_BODY()
public:
	virtual FPrimaryAssetId GetPrimaryAssetId() const override;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Encounter") TArray<FPokeMonsterWildEncounterEntry> Entries;
	/** A seeded stream makes test encounters reproducible. Invalid entries are ignored. */
	bool Roll(const FPokeMonsterEncounterContext& Context, FRandomStream& Random,
		FPokeMonsterCreatureInstance& OutCreature, int32* OutEntryIndex = nullptr) const;
};
