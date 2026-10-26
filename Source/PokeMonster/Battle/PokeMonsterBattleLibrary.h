#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "PokeMonsterBattleLibrary.generated.h"

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterDamageResult
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	bool bValid = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 Damage = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	float TypeMultiplier = 1.0f;
};

/** Stateless combat primitives. Does not run turns, apply damage or execute effects. */
UCLASS()
class POKEMONSTER_API UPokeMonsterBattleLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/** Caller supplies a uniform integer roll in [0,99]; invalid rolls/data always fail. */
	UFUNCTION(BlueprintPure, Category = "PokeMonster|Battle")
	static bool CheckHit(const UPokeMonsterMoveData* Move, int32 Roll);

	/** Evaluate an already landed hit. Uses physical/special stats and species types without mutation. */
	UFUNCTION(BlueprintPure, Category = "PokeMonster|Battle")
	static FPokeMonsterDamageResult CalculateDamage(const FPokeMonsterCreatureInstance& Attacker,
		const FPokeMonsterCreatureInstance& Defender, const UPokeMonsterMoveData* Move, int32 AttackStage = 0, int32 DefenseStage = 0, int32 SpecialAttackStage = 0, int32 SpecialDefenseStage = 0);
 static FPokeMonsterDamageResult CalculateCrystalDamage(const FPokeMonsterCreatureInstance& Attacker,
  const FPokeMonsterCreatureInstance& Defender,const UPokeMonsterMoveData* Move,int32 AttackStage,int32 DefenseStage,
  int32 SpecialAttackStage,int32 SpecialDefenseStage,bool bCritical,int32 RandomFactor,bool bRain,bool bScreen,bool bIdentified,bool bSunny=false,bool bSand=false,int32 DamageMultiplier=1);
 static int32 ResolveMovePower(const FPokeMonsterCreatureInstance& Attacker,const UPokeMonsterMoveData* Move);
 static int32 ApplyStage(int32 Value, int32 Stage);
 static int32 ApplyCrystalStage(int32 Value,int32 Stage);
 static int32 AccuracyAtStages(int32 BaseAccuracy,int32 AccuracyStage,int32 EvasionStage);
 static int32 CrystalAccuracy(int32 BaseAccuracy,int32 AccuracyStage,int32 EvasionStage,bool bIdentified);
 static FText StatusLabel(EPokeMonsterCreatureStatus Status);

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Battle")
	static float GetTypeMultiplier(EPokeMonsterCreatureType Attack, EPokeMonsterCreatureType Primary,
		EPokeMonsterCreatureType Secondary = EPokeMonsterCreatureType::None);

	/** Administrative assignment, fills PP. Not a learning or in-battle replacement rule. */
	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Moves")
	static bool AssignMove(UPARAM(ref) FPokeMonsterCreatureInstance& Creature, int32 SlotIndex, UPokeMonsterMoveData* Move);

	/** Consume once per accepted attempt, including a miss or immunity; future turn logic owns that decision. */
	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Moves")
	static bool ConsumeMovePP(UPARAM(ref) FPokeMonsterCreatureInstance& Creature, int32 SlotIndex, int32 Amount = 1);
};
