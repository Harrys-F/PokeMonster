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

#include "Misc/PackageName.h"
bool APokeMonsterGameMode::IsIntegratedRegion(const FString& WorldName)
{
    const FString ShortName = UWorld::RemovePIEPrefix(FPackageName::GetShortName(WorldName));
    return ShortName == TEXT("Dev_TestMap_VisualV2") || ShortName == TEXT("Dev_WestlandRegion");
}
