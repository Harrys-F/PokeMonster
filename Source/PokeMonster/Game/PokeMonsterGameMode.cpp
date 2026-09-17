// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterGameMode.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"

APokeMonsterGameMode::APokeMonsterGameMode()
{
	DefaultPawnClass = APokeMonsterPlayerCharacter::StaticClass();
}
