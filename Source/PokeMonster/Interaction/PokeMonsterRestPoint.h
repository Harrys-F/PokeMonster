#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Templates/Function.h"
#include "PokeMonsterInteractable.h"
#include "PokeMonsterRestPoint.generated.h"

class APokeMonsterPlayerCharacter;
class UCapsuleComponent;
class UPaperSpriteComponent;
class UStaticMeshComponent;
class UTextRenderComponent;
class UPokeMonsterEncounterSubsystem;
class UPokeMonsterDialogueSubsystem;

UENUM(BlueprintType)
enum class EPokeMonsterRestOutcome : uint8
{
	Unavailable,
	NoTeam,
	RestoreFailed,
	Healed,
	HealedAndSaved,
	HealedSaveFailed
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterRestResult
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly, Category="Rest Point")
	EPokeMonsterRestOutcome Outcome = EPokeMonsterRestOutcome::Unavailable;
	UPROPERTY(BlueprintReadOnly, Category="Rest Point")
	int32 TeamCount = 0;
};

/** Configurable Overworld rest point using the common interaction and dialogue flow. */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterRestPoint : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()
public:
	APokeMonsterRestPoint();
	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;

	/** The save callback is invoked only after a successful heal and only when enabled. */
	static FPokeMonsterRestResult PerformRest(UPokeMonsterEncounterSubsystem* Encounter,
		bool bSaveAfterRest, TFunctionRef<bool()> AttemptSave);

	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Rest Point")
	FText DisplayName;
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Rest Point", meta=(MultiLine="true"))
	FText IntroText;
	/** Off by default so a development visit cannot overwrite an existing save unexpectedly. */
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Rest Point|Save")
	bool bSaveAfterRest = false;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Rest Point")
	TObjectPtr<UPaperSpriteComponent> Sprite;

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

private:
	bool ShowMessage(APokeMonsterPlayerCharacter* Player, const FText& Text, bool bStartRest);
	UFUNCTION() void HandleDialogueAction(AActor* Source, FName ActionId);
	static FText MessageForOutcome(EPokeMonsterRestOutcome Outcome);

	UPROPERTY(VisibleAnywhere) TObjectPtr<UCapsuleComponent> Body;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> Pedestal;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> Crystal;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> NameLabel;
	TWeakObjectPtr<APokeMonsterPlayerCharacter> ActivePlayer;
};
