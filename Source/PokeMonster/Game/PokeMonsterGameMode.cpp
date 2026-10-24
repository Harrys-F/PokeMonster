// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterGameMode.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"

APokeMonsterGameMode::APokeMonsterGameMode()
{
	DefaultPawnClass = APokeMonsterPlayerCharacter::StaticClass();
	PlayerControllerClass = APokeMonsterOverworldPlayerController::StaticClass();
}

#include "Engine/World.h"
bool APokeMonsterGameMode::AllowsPersistentGameplay(const UWorld* World)
{
    const auto* Mode = World ? Cast<APokeMonsterGameMode>(World->GetAuthGameMode()) : nullptr;
    return !Mode || Mode->bEnablePersistentGameplay;
}
