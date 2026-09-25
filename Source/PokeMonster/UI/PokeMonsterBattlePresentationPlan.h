#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "PokeMonsterBattlePresentationPlan.generated.h"

UENUM(BlueprintType)
enum class EPokeMonsterPresentationOutcome : uint8
{
	None, Hit, Miss, Immune, Status
};

/** One actually executed action, distilled from the ordered BattleEvents. Presentation only. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterPresentationAction
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") EPokeMonsterBattleSide Source = EPokeMonsterBattleSide::None;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") EPokeMonsterBattleSide Target = EPokeMonsterBattleSide::None;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") EPokeMonsterMoveCategory Category = EPokeMonsterMoveCategory::Physical;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") FPrimaryAssetId MoveId;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") int32 SlotIndex = INDEX_NONE;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") int32 PPAfter = INDEX_NONE;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") EPokeMonsterPresentationOutcome Outcome = EPokeMonsterPresentationOutcome::None;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") float TypeMultiplier = 1.0f;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") int32 Damage = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") int32 HPBefore = INDEX_NONE;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") int32 HPAfter = INDEX_NONE;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") bool bKnockedOut = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle Presentation") bool bBattleEnded = false;
};

/** Converts a finished round into visual actions without changing battle state or rules. */
UCLASS()
class POKEMONSTER_API UPokeMonsterBattlePresentationPlan : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintPure, Category="Battle Presentation")
	static TArray<FPokeMonsterPresentationAction> BuildActions(const FPokeMonsterBattleResult& Result);
};
