// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "PokeMonsterGameMode.generated.h"

/** Minimal game mode for exploration and movement tests. */
UCLASS()
class POKEMONSTER_API APokeMonsterGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	APokeMonsterGameMode();
    /** Explicit sandbox opt-out. Existing maps keep all persistent gameplay enabled. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Development") bool bEnablePersistentGameplay = true;
    static bool AllowsPersistentGameplay(const UWorld* World);
};
