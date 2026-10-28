#pragma once
#include "CoreMinimal.h"
#include "PokeMonsterCreatureBehavior.generated.h"

UENUM(BlueprintType)
enum class EPokeMonsterOverworldTemperament : uint8 { Curious, Shy, Territorial, Calm, Aggressive };
UENUM(BlueprintType)
enum class EPokeMonsterEncounterInitiation : uint8 { ByTemperament, Contact, Challenge, Disabled };
UENUM(BlueprintType)
enum class EPokeMonsterOverworldState : uint8 { Rest, Wander, Observe, Approach, Retreat, Warning, Cooldown, Follow, Idle, Sleep, Forage, Social, Alert, Curious, Chase, Group, Battle };

/** Optional senses for managed wild creatures; legacy species/companions retain their defaults. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreaturePerceptionProfile
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite) bool bEnabled=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float FieldOfView=220.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float NoticeRadius=0.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float SampleSeconds=.5f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ReactionSeconds=.35f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ForgetSeconds=1.2f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float MaximumChaseSeconds=6.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float InvestigationSeconds=7.f;
 bool IsValid() const;
};

/** Overworld tuning only. Does not change battle stats, species identity or save data. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureBehaviorProfile
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FPokeMonsterCreaturePerceptionProfile Perception;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) EPokeMonsterOverworldTemperament Temperament=EPokeMonsterOverworldTemperament::Calm;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) EPokeMonsterEncounterInitiation Initiation=EPokeMonsterEncounterInitiation::ByTemperament;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float NoticeRadius=550.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float PersonalSpace=170.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float DisengageRadius=750.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float WarningSeconds=2.5f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float EncounterRadius=160.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float EncounterCooldown=30.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) bool bCanInitiateEncounter=true;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float WalkMultiplier=.75f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ReactionSpeedMultiplier=1.35f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float RestMultiplier=1.5f;
 bool IsValid() const;
};

/** Shared decision policy; runtime owns timers, perception and collision-checked paths. */
struct POKEMONSTER_API FPokeMonsterCreatureBehavior
{
 static bool InView(const FPokeMonsterCreatureBehaviorProfile& Profile,const FVector& Observer,const FVector& Forward,const FVector& Target);
 static bool UpdateAwareness(const FPokeMonsterCreaturePerceptionProfile& Profile,float Delta,bool Sensed,bool Immediate,bool WasAware,float& Acquiring,float& Lost);
 static EPokeMonsterOverworldState Decide(const FPokeMonsterCreatureBehaviorProfile& Profile,
  float PlayerDistance,bool bVisible,bool bPreviouslyReacting,bool bCoolingDown);
 static EPokeMonsterEncounterInitiation InitiationFor(const FPokeMonsterCreatureBehaviorProfile& Profile);
 static bool CanInitiate(const FPokeMonsterCreatureBehaviorProfile& Profile,bool bActualContact,bool bInteraction,bool bCoolingDown);
};
