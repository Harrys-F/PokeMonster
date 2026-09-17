// Copyright Epic Games, Inc. All Rights Reserved.

#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Game/PokeMonsterGameMode.h"
#include "Camera/CameraComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/Engine.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputAction.h"
#include "InputMappingContext.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPokeMonsterPlayerFoundationTest,
	"PokeMonster.Player.Foundation",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterPlayerFoundationTest::RunTest(const FString& Parameters)
{
	const APokeMonsterPlayerCharacter* Character = GetDefault<APokeMonsterPlayerCharacter>();
	if (!TestNotNull(TEXT("The player character defaults exist"), Character))
	{
		return false;
	}

	TestNotNull(TEXT("The runtime input mapping context exists"), Character->DefaultMappingContext.Get());
	TestNotNull(TEXT("The 2D move input action exists"), Character->MoveAction.Get());
	TestEqual(TEXT("The move action uses a two-dimensional value"), Character->MoveAction->ValueType, EInputActionValueType::Axis2D);
	TestEqual(TEXT("WASD and arrow keys provide eight mappings"), Character->DefaultMappingContext->GetMappings().Num(), 8);

	const FVector DiagonalMovement = APokeMonsterPlayerCharacter::CalculateCameraRelativeMovement(FVector2D(1.0f, 1.0f), -45.0f);
	TestTrue(TEXT("Diagonal input produces a movement direction"), !DiagonalMovement.IsNearlyZero());
	TestTrue(TEXT("Diagonal movement is normalized"), FMath::IsNearlyEqual(DiagonalMovement.Size2D(), 1.0f, 0.01f));

	const FVector ForwardMovement = APokeMonsterPlayerCharacter::CalculateCameraRelativeMovement(FVector2D(0.0f, 1.0f), -45.0f);
	const FVector RightMovement = APokeMonsterPlayerCharacter::CalculateCameraRelativeMovement(FVector2D(1.0f, 0.0f), -45.0f);
	TestTrue(TEXT("Camera-relative axes remain perpendicular"), FMath::IsNearlyZero(FVector::DotProduct(ForwardMovement, RightMovement), 0.01f));

	TestTrue(TEXT("Camera position lag is enabled"), Character->CameraBoom->bEnableCameraLag);
	TestTrue(TEXT("Camera does not use a vertical top-down pitch"), Character->CameraBoom->GetRelativeRotation().Pitch > -80.0f);
	TestTrue(TEXT("Camera uses an angled yaw"), !FMath::IsNearlyZero(Character->CameraBoom->GetRelativeRotation().Yaw));
	TestTrue(TEXT("Camera boom keeps visible distance from the player"), Character->CameraBoom->TargetArmLength >= 500.0f);
	TestNotNull(TEXT("The character owns a perspective follow camera"), Character->FollowCamera.Get());

	const APokeMonsterGameMode* GameModeDefaults = GetDefault<APokeMonsterGameMode>();
	TestEqual(TEXT("The game mode selects the player character as default pawn"),
		GameModeDefaults->DefaultPawnClass.Get(),
		APokeMonsterPlayerCharacter::StaticClass());

	UWorld* PlayWorld = nullptr;
	for (const FWorldContext& WorldContext : GEngine->GetWorldContexts())
	{
		if (WorldContext.WorldType == EWorldType::PIE)
		{
			PlayWorld = WorldContext.World();
			break;
		}
	}

	if (PlayWorld)
	{
		APlayerController* PlayerController = PlayWorld->GetFirstPlayerController();
		APokeMonsterPlayerCharacter* LiveCharacter = PlayerController
			? Cast<APokeMonsterPlayerCharacter>(PlayerController->GetPawn())
			: nullptr;

		if (TestNotNull(TEXT("PIE possesses the PokeMonster player character"), LiveCharacter))
		{
			const UEnhancedInputLocalPlayerSubsystem* InputSubsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer());
			TestTrue(TEXT("PIE has the movement mapping context active"),
				InputSubsystem && InputSubsystem->HasMappingContext(LiveCharacter->DefaultMappingContext));

			LiveCharacter->Move(FInputActionValue(FVector2D(1.0f, 1.0f)));
			TestTrue(TEXT("PIE movement input reaches the character movement pipeline"),
				!LiveCharacter->GetPendingMovementInputVector().IsNearlyZero());
			LiveCharacter->ConsumeMovementInputVector();

			LiveCharacter->StopMoving(FInputActionValue(FVector2D::ZeroVector));
			TestTrue(TEXT("Stopping input resets the exposed animation direction"),
				LiveCharacter->GetMovementInput().IsNearlyZero());
		}
	}

	return true;
}

#endif
