#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterBattleEncounterActor.generated.h"

class UStaticMeshComponent;
class UTextRenderComponent;
class USceneComponent;

/** One deliberately placed encounter for Dev_TestMap; no random encounters or NPC logic. */
UCLASS()
class POKEMONSTER_API APokeMonsterBattleEncounterActor : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()
public:
	APokeMonsterBattleEncounterActor();
	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;
private:
	UPROPERTY(VisibleAnywhere) TObjectPtr<USceneComponent> SceneRoot;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> Marker;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> Label;
};
