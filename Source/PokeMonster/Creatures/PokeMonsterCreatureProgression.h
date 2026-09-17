#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "PokeMonsterCreatureInstance.h"
#include "PokeMonsterCreatureProgression.generated.h"

/** Pure progression rules; no dependency on a world, player, inventory or UI. */
UCLASS()
class POKEMONSTER_API UPokeMonsterCreatureProgression : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	static constexpr int32 MinLevel = 1;
	static constexpr int32 MaxLevel = 100;

	/** Cumulative XP threshold. Level is clamped; unknown growth groups return -1. */
	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	static int64 ExperienceForLevel(EPokeMonsterGrowthRate GrowthRate, int32 Level);

	/** Provisional base-stat/level calculation, without IVs, EVs, nature or combat modifiers. */
	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	static FPokeMonsterCreatureStats CalculateStats(const FPokeMonsterCreatureBaseStats& BaseStats, int32 Level);

	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Creature")
	static FPokeMonsterExperienceResult AddExperience(UPARAM(ref) FPokeMonsterCreatureInstance& Creature, int64 Amount);

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	static int64 ExperienceToNextLevel(const FPokeMonsterCreatureInstance& Creature);

	/** Evaluates a rule, not an evolution execution. Unsupported/malformed rules fail closed. */
	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	static bool IsEvolutionEligible(const FPokeMonsterEvolutionData& Rule, int32 Level, const FPokeMonsterEvolutionContext& Context);

	/** Checks the creature's species rules and returns unique eligible target IDs without loading targets. */
	UFUNCTION(BlueprintPure, Category = "PokeMonster|Creature")
	static TArray<FPrimaryAssetId> GetEligibleEvolutions(const FPokeMonsterCreatureInstance& Creature, const FPokeMonsterEvolutionContext& Context);
};
