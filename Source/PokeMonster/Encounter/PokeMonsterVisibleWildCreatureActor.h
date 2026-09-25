#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterEncounterProfile.h"
#include "PokeMonsterEncounterSubsystem.h"
#include "PokeMonsterVisibleWildCreatureActor.generated.h"

class UCapsuleComponent;
class USphereComponent;
class UPaperSpriteComponent;
class UTextRenderComponent;
class APokeMonsterPlayerCharacter;

/** A deliberately placed wild creature. Contact or interaction uses the shared encounter flow. */
UCLASS()
class POKEMONSTER_API APokeMonsterVisibleWildCreatureActor : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()
public:
	APokeMonsterVisibleWildCreatureActor();
	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") TSoftObjectPtr<UPokeMonsterEncounterProfile> Profile;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") FPokeMonsterEncounterContext Context;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") int32 Seed = 3817;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") bool bDeactivateAfterVictory = true;
protected:
	virtual void BeginPlay() override;
private:
	bool TryStart(APokeMonsterPlayerCharacter* Player);
	UFUNCTION() void OnContact(UPrimitiveComponent* Overlapped, AActor* OtherActor,
		UPrimitiveComponent* OtherComponent, int32 BodyIndex, bool bFromSweep, const FHitResult& Hit);
	UFUNCTION() void OnEncounterFinished(const FPokeMonsterEncounterEndData& Result);
	UPROPERTY(VisibleAnywhere) TObjectPtr<UCapsuleComponent> Body;
	UPROPERTY(VisibleAnywhere) TObjectPtr<USphereComponent> ContactRange;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UPaperSpriteComponent> Sprite;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> Label;
	bool bDeactivated = false;
};
