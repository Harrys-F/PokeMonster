#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "PokeMonsterTrainerProfile.generated.h"

class UPokeMonsterCreatureSpeciesData;
class UPokeMonsterMoveData;

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterTrainerTeamEntry
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Trainer") TSoftObjectPtr<UPokeMonsterCreatureSpeciesData> Species;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Trainer", meta=(ClampMin="1", ClampMax="100")) int32 Level = 1;
	/** One to four starting moves. Each generated creature owns its own PP. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Trainer") TArray<TSoftObjectPtr<UPokeMonsterMoveData>> StartingMoves;
};

/** Shared trainer definition; defeated state lives in the GameInstance encounter subsystem. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterTrainerProfile : public UPrimaryDataAsset
{
	GENERATED_BODY()
public:
	virtual FPrimaryAssetId GetPrimaryAssetId() const override;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Identity") FName InternalId;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Identity") FText DisplayName;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Identity") FText TrainerClass;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Team") TArray<FPokeMonsterTrainerTeamEntry> Team;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Dialogue") FText BeforeBattle;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Dialogue") FText AfterPlayerVictory;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Dialogue") FText AfterPlayerDefeat;

	bool BuildTeam(TArray<FPokeMonsterCreatureInstance>& OutTeam) const;
};
