// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Engine/AssetManagerTypes.h"
#include "PokeMonsterCreatureTypes.generated.h"

class UPaperFlipbook;

/** All elemental types used by generation 1 and 2 species. None is reserved for an absent secondary type. */
UENUM(BlueprintType)
enum class EPokeMonsterCreatureType : uint8
{
	None,
	Normal,
	Fire,
	Water,
	Electric,
	Grass,
	Ice,
	Fighting,
	Poison,
	Ground,
	Flying,
	Psychic,
	Bug,
	Rock,
	Ghost,
	Dragon,
	Dark,
	Steel
};

UENUM(BlueprintType)
enum class EPokeMonsterGenderSystem : uint8
{
	Genderless,
	Mixed,
	MaleOnly,
	FemaleOnly
};

/** Growth categories are data labels only; experience formulas will be added with progression gameplay. */
UENUM(BlueprintType)
enum class EPokeMonsterGrowthRate : uint8
{
	Fast,
	MediumFast,
	MediumSlow,
	Slow,
	Erratic,
	Fluctuating
};

UENUM(BlueprintType)
enum class EPokeMonsterEvolutionTrigger : uint8
{
	Level,
	Item,
	Friendship,
	Location,
	SpecialInteraction,
	Custom
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureBaseStats
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats", meta = (ClampMin = "1"))
	int32 HP = 10;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats", meta = (ClampMin = "1"))
	int32 Attack = 10;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats", meta = (ClampMin = "1"))
	int32 Defense = 10;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats", meta = (ClampMin = "1"))
	int32 SpecialAttack = 10;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats", meta = (ClampMin = "1"))
	int32 SpecialDefense = 10;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats", meta = (ClampMin = "1"))
	int32 Speed = 10;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterGenderData
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Gender")
	EPokeMonsterGenderSystem System = EPokeMonsterGenderSystem::Mixed;

	/** Used only by Mixed. A value of 0.5 represents an even distribution. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Gender", meta = (ClampMin = "0.0", ClampMax = "1.0", EditCondition = "System == EPokeMonsterGenderSystem::Mixed", EditConditionHides))
	float FemaleRatio = 0.5f;
};

/** One possible future evolution. RequirementId can name an item, place, event, or other rule later. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterEvolutionData
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution")
	FPrimaryAssetId TargetSpecies;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution")
	EPokeMonsterEvolutionTrigger Trigger = EPokeMonsterEvolutionTrigger::Level;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution", meta = (ClampMin = "1"))
	int32 MinimumLevel = 1;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution")
	FName RequirementId = NAME_None;
};

/** Soft references keep the species catalog lightweight until its visuals are actually needed. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureVisuals
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Visuals")
	TSoftObjectPtr<UPaperFlipbook> FrontFlipbook;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Visuals")
	TSoftObjectPtr<UPaperFlipbook> BackFlipbook;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Visuals")
	TSoftObjectPtr<UPaperFlipbook> OverworldFlipbook;
};
