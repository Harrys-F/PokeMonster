#pragma once

#include "CoreMinimal.h"
#include "PokeMonsterMoveSlot.generated.h"

class UPokeMonsterMoveData;

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterMoveSlot
{
	GENERATED_BODY()

public:
	/** Assigning a configured move fills its PP; invalid assignments leave the slot unchanged. */
	bool AssignMove(UPokeMonsterMoveData* InMove);
	bool ConsumePP(int32 Amount = 1);
	const TSoftObjectPtr<UPokeMonsterMoveData>& GetMove() const { return Move; }
	int32 GetCurrentPP() const { return CurrentPP; }
	int32 GetMaxPP() const { return MaxPP; }

private:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Move", meta = (AllowPrivateAccess = "true"))
	TSoftObjectPtr<UPokeMonsterMoveData> Move;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Move", meta = (AllowPrivateAccess = "true"))
	int32 CurrentPP = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Move", meta = (AllowPrivateAccess = "true"))
	int32 MaxPP = 0;
};
