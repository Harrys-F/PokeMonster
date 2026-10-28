// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PokeMonsterCreatureTypes.h"
#include "Overworld/PokeMonsterCreatureOverworldSettings.h"
#include "PokeMonsterCreatureSpeciesData.generated.h"

class UPokeMonsterMoveData;
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterLevelMove
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 Level=1;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TSoftObjectPtr<UPokeMonsterMoveData> Move;
 /** A verified learnset entry may lack an implemented move. Keep its level/name explicit. */
 UPROPERTY(EditAnywhere,BlueprintReadOnly) FText UnavailableMoveName;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) FText UnavailableReason;
};

/** Shared, immutable design data for one creature species. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterCreatureSpeciesData : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
 /** Existing AssetManager registry, filtered by usable presentation; never an independently maintained list. */
 UFUNCTION(BlueprintCallable, Category="PokeMonster|Creature")
 static TArray<UPokeMonsterCreatureSpeciesData*> GetRegisteredPlayableSpecies();
	virtual FPrimaryAssetId GetPrimaryAssetId() const override;

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	FName GetInternalId() const { return InternalId; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	FText GetDisplayName() const { return DisplayName; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	int32 GetPokedexNumber() const { return PokedexNumber; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	int32 GetBaseCaptureRate() const { return BaseCaptureRate; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	EPokeMonsterCreatureType GetPrimaryType() const { return PrimaryType; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	EPokeMonsterCreatureType GetSecondaryType() const { return SecondaryType; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	const FPokeMonsterCreatureBaseStats& GetBaseStats() const { return BaseStats; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	const FPokeMonsterGenderData& GetGenderData() const { return Gender; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	int32 GetStartingLevel() const { return StartingLevel; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	EPokeMonsterGrowthRate GetGrowthRate() const { return GrowthRate; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	const TArray<FPokeMonsterEvolutionData>& GetEvolutions() const { return Evolutions; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	const FPokeMonsterCreatureVisuals& GetVisuals() const { return Visuals; }

 UFUNCTION(BlueprintPure) int32 GetBaseExperienceYield()const{return BaseExperienceYield;}
 TArray<UPokeMonsterMoveData*> MovesForLevel(int32 Level)const;
 UPROPERTY(EditDefaultsOnly,BlueprintReadOnly,Category="Moves") TArray<FPokeMonsterLevelMove> LevelUpMoves;
 UPROPERTY(EditDefaultsOnly,BlueprintReadOnly,Category="Overworld") FPokeMonsterCreatureOverworldSettings Overworld;
private:
 UPROPERTY(EditDefaultsOnly,Category="Growth",meta=(ClampMin="0")) int32 BaseExperienceYield=0;
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Identity", meta = (AllowPrivateAccess = "true"))
	FName InternalId = NAME_None;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Identity", meta = (AllowPrivateAccess = "true"))
	FText DisplayName;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Identity", meta = (AllowPrivateAccess = "true", ClampMin = "1"))
	int32 PokedexNumber = 1;

	/** Prototype capture rate (1-255); species-wide, never stored on an individual creature. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Capture", meta = (AllowPrivateAccess = "true", ClampMin = "1", ClampMax = "255"))
	int32 BaseCaptureRate = 120;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Typing", meta = (AllowPrivateAccess = "true"))
	EPokeMonsterCreatureType PrimaryType = EPokeMonsterCreatureType::Normal;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Typing", meta = (AllowPrivateAccess = "true"))
	EPokeMonsterCreatureType SecondaryType = EPokeMonsterCreatureType::None;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Stats", meta = (AllowPrivateAccess = "true"))
	FPokeMonsterCreatureBaseStats BaseStats;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Gender", meta = (AllowPrivateAccess = "true"))
	FPokeMonsterGenderData Gender;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Growth", meta = (AllowPrivateAccess = "true", ClampMin = "1", ClampMax = "100"))
	int32 StartingLevel = 1;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Growth", meta = (AllowPrivateAccess = "true"))
	EPokeMonsterGrowthRate GrowthRate = EPokeMonsterGrowthRate::MediumFast;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Evolution", meta = (AllowPrivateAccess = "true"))
	TArray<FPokeMonsterEvolutionData> Evolutions;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Visuals", meta = (AllowPrivateAccess = "true"))
	FPokeMonsterCreatureVisuals Visuals;
};
