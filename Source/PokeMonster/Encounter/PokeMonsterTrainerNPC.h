#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterEncounterSubsystem.h"
#include "PokeMonsterTrainerNPC.generated.h"

class UCapsuleComponent;
class UPaperSpriteComponent;
class UTextRenderComponent;
class UPokeMonsterTrainerProfile;
class APokeMonsterPlayerCharacter;

/** Simple placed trainer: dialogue placeholder, then the shared overworld battle overlay. */
UCLASS()
class POKEMONSTER_API APokeMonsterTrainerNPC : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()
public:
	APokeMonsterTrainerNPC();
	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Trainer") TSoftObjectPtr<UPokeMonsterTrainerProfile> Profile;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Trainer") int32 BattleSeed = 2581;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Trainer", meta=(ClampMin="0.1")) float DialogueSeconds = 1.5f;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Trainer") TObjectPtr<UPaperSpriteComponent> Sprite;
	UFUNCTION(BlueprintPure, Category="PokeMonster|Trainer") bool IsBattlePending() const { return bBattlePending; }
protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
	void ShowDialogue(const FText& Text);
	void StartPendingBattle();
	UFUNCTION() void OnEncounterFinished(const FPokeMonsterEncounterEndData& Result);
	UFUNCTION() void RefreshPersistentState();
	UPROPERTY(VisibleAnywhere) TObjectPtr<UCapsuleComponent> Body;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> NameLabel;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> DialogueLabel;
	UPROPERTY(Transient) TWeakObjectPtr<APokeMonsterPlayerCharacter> PendingPlayer;
	FTimerHandle DialogueTimer;
	bool bBattlePending = false;
};
