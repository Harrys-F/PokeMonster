// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterGameMode.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"

APokeMonsterGameMode::APokeMonsterGameMode()
{
	DefaultPawnClass = APokeMonsterPlayerCharacter::StaticClass();
	PlayerControllerClass = APokeMonsterOverworldPlayerController::StaticClass();
}
