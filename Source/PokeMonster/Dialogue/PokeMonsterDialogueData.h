#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PokeMonsterDialogueData.generated.h"

class UTexture2D;

UENUM(BlueprintType)
enum class EPokeMonsterDialogueCondition : uint8
{
	Always,
	WorldFlagSet,
	WorldFlagUnset,
	TrainerDefeated,
	TrainerNotDefeated
};

UENUM(BlueprintType)
enum class EPokeMonsterDialogueAction : uint8
{
	None,
	SetWorldFlag,
	Custom
};

/** A page is shown only when its optional condition matches the current session state. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterDialoguePage
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Dialogue") FText SpeakerName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Dialogue", meta=(MultiLine="true")) FText Text;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Dialogue") TSoftObjectPtr<UTexture2D> Portrait;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Dialogue|Condition")
	EPokeMonsterDialogueCondition Condition = EPokeMonsterDialogueCondition::Always;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Dialogue|Condition") FName ConditionId;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Dialogue|Action")
	EPokeMonsterDialogueAction FollowUp = EPokeMonsterDialogueAction::None;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Dialogue|Action") FName FollowUpId;
};

/** Reusable ordered dialogue; the UI is independent of these authored pages. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterDialogueData : public UPrimaryDataAsset
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Dialogue") TArray<FPokeMonsterDialoguePage> Pages;
	virtual FPrimaryAssetId GetPrimaryAssetId() const override
	{
		return FPrimaryAssetId(TEXT("Dialogue"), GetFName());
	}
};
