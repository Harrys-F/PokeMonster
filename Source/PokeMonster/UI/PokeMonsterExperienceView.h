#pragma once
#include "CoreMinimal.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "PokeMonsterExperienceView.generated.h"

/** Derived, read-only presentation data. Never serialized into a save or used to award XP. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterExperienceView
{
 GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly) bool bValid=false;
 UPROPERTY(BlueprintReadOnly) bool bMaximumLevel=false;
 UPROPERTY(BlueprintReadOnly) int32 Level=0;
 UPROPERTY(BlueprintReadOnly) int64 Total=0;
 UPROPERTY(BlueprintReadOnly) int64 LevelStart=0;
 UPROPERTY(BlueprintReadOnly) int64 NextLevelStart=0;
 UPROPERTY(BlueprintReadOnly) int64 Earned=0;
 UPROPERTY(BlueprintReadOnly) int64 Required=0;
 UPROPERTY(BlueprintReadOnly) int64 Remaining=0;
 UPROPERTY(BlueprintReadOnly) float Fraction=0;
 UPROPERTY(BlueprintReadOnly) EPokeMonsterGrowthRate Growth=EPokeMonsterGrowthRate::MediumFast;
 static FPokeMonsterExperienceView FromCreature(const FPokeMonsterCreatureInstance& Creature);
 static FPokeMonsterExperienceView Calculate(EPokeMonsterGrowthRate Growth,int32 Level,int64 Total);
 /** UI-only interpolation across the actual curve boundaries, including multiple levels. */
 static FPokeMonsterExperienceView Interpolate(const FPokeMonsterExperienceView& Before,const FPokeMonsterExperienceView& After,float Alpha);
 FText ProgressText() const;
 FText RemainingText() const;
};
