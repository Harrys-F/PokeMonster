#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "../Creatures/PokeMonsterCreatureTypes.h"
#include "PokeMonsterMoveData.generated.h"

UENUM(BlueprintType)
enum class EPokeMonsterMoveCategory : uint8
{
	Physical,
	Special,
	Status
};

/** Declarative extension point only. No effect is executed by the battle foundation. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterMoveEffect
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Effect")
	FName EffectId = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Effect")
	FText Description;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Effect", meta = (ClampMin = "0", ClampMax = "100"))
	int32 ChancePercent = 100;
};

/** Shared design data. Runtime PP live exclusively in individual move slots. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterMoveData : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	virtual FPrimaryAssetId GetPrimaryAssetId() const override;
	bool IsConfigured() const;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Identity")
	FName InternalId = NAME_None;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Identity")
	FText DisplayName;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Move")
	EPokeMonsterCreatureType Type = EPokeMonsterCreatureType::Normal;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Move")
	EPokeMonsterMoveCategory Category = EPokeMonsterMoveCategory::Physical;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Move", meta = (ClampMin = "0"))
	int32 BasePower = 40;

	/** Percentage: zero always misses, 100 always hits for a valid roll. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Move", meta = (ClampMin = "0", ClampMax = "100"))
	int32 Accuracy = 100;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Move", meta = (ClampMin = "1"))
	int32 MaxPP = 35;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Move")
	int32 Priority = 0;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Move")
	FPokeMonsterMoveEffect Effect;
};
