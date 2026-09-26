#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterNPC.generated.h"

class UCapsuleComponent;
class UPaperSpriteComponent;
class UTextRenderComponent;
class UPokeMonsterDialogueData;

/** Placed, reusable conversation actor; visuals and dialogue content are configurable per instance. */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterNPC : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()
public:
	APokeMonsterNPC();
	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Dialogue")
	TSoftObjectPtr<UPokeMonsterDialogueData> Dialogue;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Dialogue")
	FText DisplayName;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Dialogue")
	TObjectPtr<UPaperSpriteComponent> Sprite;
	UFUNCTION(BlueprintImplementableEvent, Category="PokeMonster|Dialogue")
	void OnDialogueFollowUp(FName ActionId);
protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
	UFUNCTION() void HandleCustomAction(AActor* Source, FName ActionId);
	UPROPERTY(VisibleAnywhere) TObjectPtr<UCapsuleComponent> Body;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> NameLabel;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> PlaceholderGlyph;
};
