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

/** Experience curves implemented by UPokeMonsterCreatureProgression. */
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

/** One evolution route. Populated requirements are ANDed, separate routes are alternatives. */
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

	/** Legacy RequirementId still applies to Item, Location or SpecialInteraction triggers. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution")
	FName RequiredItemId = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution")
	FName RequiredLocationId = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution")
	FName RequiredActionId = NAME_None;

	/** Zero disables the extra friendship gate; Friendship routes require a positive threshold. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Evolution", meta = (ClampMin = "0", ClampMax = "255"))
	int32 MinimumFriendship = 0;
};

/** Supplied by the caller at the event being evaluated. Does not consume items or execute actions. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterEvolutionContext
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Evolution")
	EPokeMonsterEvolutionTrigger Trigger = EPokeMonsterEvolutionTrigger::Level;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Evolution")
	FName UsedItemId = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Evolution")
	FName LocationId = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Evolution")
	FName ActionId = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Evolution", meta = (ClampMin = "0", ClampMax = "255"))
	int32 Friendship = 0;
};

/** Calculated per-instance values, distinct from immutable species base stats. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureStats
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 MaxHP = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 Attack = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 Defense = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 SpecialAttack = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 SpecialDefense = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 Speed = 0;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterExperienceResult
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression")
	bool bSucceeded = false;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression")
	int64 ExperienceAdded = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression")
	int32 LevelsGained = 0;
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
