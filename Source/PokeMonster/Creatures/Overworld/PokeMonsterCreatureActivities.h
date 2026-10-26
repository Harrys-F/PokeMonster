#pragma once
#include "CoreMinimal.h"
#include "PokeMonsterCreatureBehavior.h"
#include "PokeMonsterCreatureActivities.generated.h"

/** Context supplied by a future world clock; never changes lighting or battle time. */
UENUM(BlueprintType)
enum class EPokeMonsterActivityPeriod : uint8 { Day, Evening, Night };

/** Ambient activities use the existing roaming state and collision-checked planner. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureActivityProfile
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bEnabled=false;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float WanderWeight=5.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float ObserveWeight=2.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float RestWeight=2.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float SleepWeight=.5f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float ForageWeight=3.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float SocialWeight=2.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float MinimumSeconds=5.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float MaximumSeconds=12.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float RestSeconds=15.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float SleepSeconds=22.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float SocialCooldown=35.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float SleepCooldown=90.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float ForageCooldown=20.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float PerceptionSeconds=1.5f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float SocialRadius=500.f;
 /** A valid invitation can be declined without interrupting the receiver. */
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float SocialAcceptance=.85f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) float ActiveDistance=4000.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bPreferVegetation=false;
 UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bPreferOwnSpecies=true;
 bool IsValid() const;
 static FPokeMonsterCreatureActivityProfile ForSpecies(FName Species);
 static EPokeMonsterOverworldState Select(const FPokeMonsterCreatureActivityProfile& Profile,
  FRandomStream& Random, EPokeMonsterActivityPeriod Period, bool CanSleep, bool CanForage, bool CanSocial);
};
