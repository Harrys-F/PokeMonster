#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterStoryGoal.generated.h"

class UCapsuleComponent;
class UPointLightComponent;
class UPaperSpriteComponent;
class UTextRenderComponent;
class UPokeMonsterEncounterSubsystem;
struct FPokeMonsterEncounterEndData;

UENUM(BlueprintType)
enum class EPokeMonsterStoryGoalState : uint8
{
	Locked,
	Ready,
	Completed
};

/** Small placed objective that uses the existing dialogue and persisted world flags. */
UCLASS()
class POKEMONSTER_API APokeMonsterStoryGoal : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()
public:
	APokeMonsterStoryGoal();
	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;

	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Story Goal") FText DisplayName;
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Story Goal") FName RequiredTrainerId;
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Story Goal") FName CompletionFlag;
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Story Goal", meta=(MultiLine="true")) FText LockedText;
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Story Goal", meta=(MultiLine="true")) FText ReadyText;
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Story Goal", meta=(MultiLine="true")) FText CompletedText;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Story Goal") TObjectPtr<UPaperSpriteComponent> Sprite;

	static EPokeMonsterStoryGoalState EvaluateState(const UPokeMonsterEncounterSubsystem* Encounter,
		FName TrainerId, FName GoalFlag);
	static bool CompleteGoal(UPokeMonsterEncounterSubsystem* Encounter, FName TrainerId, FName GoalFlag);

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

private:
	UFUNCTION() void HandleDialogueAction(AActor* Source, FName ActionId);
	UFUNCTION() void RefreshVisual();
	UFUNCTION() void OnEncounterFinished(const FPokeMonsterEncounterEndData& Result);
	UPROPERTY(VisibleAnywhere) TObjectPtr<UCapsuleComponent> Body;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> Label;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UPointLightComponent> CompletionLight;
};
