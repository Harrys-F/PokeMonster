// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "PokeMonsterInteractable.generated.h"

class APawn;

/** Common contract for world objects that can be used by a player or another pawn. */
UINTERFACE(BlueprintType)
class POKEMONSTER_API UPokeMonsterInteractable : public UInterface
{
	GENERATED_BODY()
};

class POKEMONSTER_API IPokeMonsterInteractable
{
	GENERATED_BODY()

public:
	/** Allows an interactable to reject an otherwise valid interaction attempt. */
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "PokeMonster|Interaction")
	bool CanInteract(APawn* Interactor) const;

	/** Performs the object's interaction. Later NPC and dialogue actors can implement this event. */
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "PokeMonster|Interaction")
	void Interact(APawn* Interactor);
};
