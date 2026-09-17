// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterInteractable.h"
#include "PokeMonsterInteractionTestActor.generated.h"

class UPointLightComponent;
class UStaticMeshComponent;

/** Minimal engine-only interaction target used by Dev_TestMap and automated tests. */
UCLASS()
class POKEMONSTER_API APokeMonsterInteractionTestActor : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()

public:
	APokeMonsterInteractionTestActor();

	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Interaction")
	int32 GetInteractionCount() const { return InteractionCount; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Interaction")
	bool IsInteractionActive() const { return bInteractionActive; }

protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "PokeMonster|Interaction")
	TObjectPtr<UStaticMeshComponent> Mesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "PokeMonster|Interaction")
	TObjectPtr<UPointLightComponent> InteractionLight;

private:
	UPROPERTY(VisibleInstanceOnly, Category = "PokeMonster|Interaction")
	int32 InteractionCount = 0;

	UPROPERTY(VisibleInstanceOnly, Category = "PokeMonster|Interaction")
	bool bInteractionActive = false;
};
