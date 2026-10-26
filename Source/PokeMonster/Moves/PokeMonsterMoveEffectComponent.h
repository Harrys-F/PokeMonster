#pragma once
#include "CoreMinimal.h"
#include "../Creatures/PokeMonsterCreatureTypes.h"
#include "PokeMonsterMoveEffectComponent.generated.h"

UENUM(BlueprintType)
enum class EPokeMonsterEffectKind : uint8
{
 Stage, PrimaryStatus, Drain, Recoil, Heal, FixedDamage, MultiHit, Flinch, Confusion,
 Protect, Screen, Charge, Trap, PreventSwitch, Disable, Spite, CopyStages,
 Identify, ClearBindings, Rain, Rage, Rampage, Curse, DestinyBond, CriticalFocus,
 Recharge, LowHPPower, ForceSwitch, CopyLastMove, Safeguard, SwitchPunish, NoEffect, AirborneBonus
};
UENUM(BlueprintType)
enum class EPokeMonsterBattleStat : uint8 { Attack, Defense, SpecialAttack, SpecialDefense, Speed, Accuracy, Evasion };

/** Composable declarative effect. Durations/fractions/chances belong to reviewed move data. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterMoveEffectComponent
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadOnly) EPokeMonsterEffectKind Kind=EPokeMonsterEffectKind::Stage;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) bool bSelf=false;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) bool bSecondary=false;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) EPokeMonsterBattleStat Stat=EPokeMonsterBattleStat::Attack;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 Stages=-1;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) EPokeMonsterCreatureStatus Status=EPokeMonsterCreatureStatus::None;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 ChancePercent=100;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 MinTurns=1;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 MaxTurns=1;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 Numerator=1;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 Denominator=2;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 Amount=0;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 MinHits=2;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 MaxHits=5;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TArray<int32> HitWeights;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TArray<EPokeMonsterCreatureType> ImmuneTypes;
 bool IsConfigured()const;
};
