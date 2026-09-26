// Copyright Epic Games, Inc. All Rights Reserved.

#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Game/PokeMonsterGameMode.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "../Interaction/PokeMonsterInteractionTestActor.h"
#include "Camera/CameraComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/Engine.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "EngineUtils.h"
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
	TestNotNull(TEXT("The interaction input action exists"), Character->InteractAction.Get());
	TestNotNull(TEXT("The overworld menu input action exists"), Character->MenuAction.Get());
	TestEqual(TEXT("The move action uses a two-dimensional value"), Character->MoveAction->ValueType, EInputActionValueType::Axis2D);
	TestEqual(TEXT("The interaction action uses a boolean value"), Character->InteractAction->ValueType, EInputActionValueType::Boolean);
	TestEqual(TEXT("Movement, interaction and menu provide eleven mappings"), Character->DefaultMappingContext->GetMappings().Num(), 11);

	bool bHasEInteraction = false;
	bool bHasEnterInteraction = false;
	bool bHasTabMenu = false;
	for (const FEnhancedActionKeyMapping& Mapping : Character->DefaultMappingContext->GetMappings())
	{
		if (Mapping.Action == Character->InteractAction)
		{
			bHasEInteraction |= Mapping.Key == EKeys::E;
			bHasEnterInteraction |= Mapping.Key == EKeys::Enter;
		}
		if (Mapping.Action == Character->MenuAction)
			bHasTabMenu |= Mapping.Key == EKeys::Tab;
	}
	TestTrue(TEXT("E triggers the interaction action"), bHasEInteraction);
	TestTrue(TEXT("Enter triggers the interaction action"), bHasEnterInteraction);
	TestTrue(TEXT("Tab triggers the overworld menu"), bHasTabMenu);
	TestTrue(TEXT("The interaction range remains short"), Character->InteractionRange > 0.0f && Character->InteractionRange <= 250.0f);
	TestTrue(TEXT("The interaction trace has a useful radius"), Character->InteractionTraceRadius > 0.0f);
	TestTrue(TEXT("The test actor implements the generic interaction interface"),
		APokeMonsterInteractionTestActor::StaticClass()->ImplementsInterface(UPokeMonsterInteractable::StaticClass()));

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
	TestNotNull(TEXT("The character owns a Paper2D flipbook component"), Character->GetCharacterFlipbookComponent());
	TestEqual(TEXT("The default visual state is idle"), Character->GetLocomotionState(), EPokeMonsterLocomotionState::Idle);
	TestEqual(TEXT("The default facing direction is down"), Character->GetFacingDirection(), EPokeMonsterFacingDirection::Down);

	TestEqual(TEXT("A vertical-dominant diagonal faces up"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(FVector2D(0.4f, 1.0f), EPokeMonsterFacingDirection::Left, 0.1f),
		EPokeMonsterFacingDirection::Up);
	TestEqual(TEXT("A horizontal-dominant diagonal faces left"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(FVector2D(-1.0f, 0.4f), EPokeMonsterFacingDirection::Up, 0.1f),
		EPokeMonsterFacingDirection::Left);
	TestEqual(TEXT("A rightward input faces right"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(FVector2D(1.0f, 0.0f), EPokeMonsterFacingDirection::Down, 0.1f),
		EPokeMonsterFacingDirection::Right);
	TestEqual(TEXT("A downward input faces down"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(FVector2D(0.0f, -1.0f), EPokeMonsterFacingDirection::Up, 0.1f),
		EPokeMonsterFacingDirection::Down);
	TestEqual(TEXT("An equal diagonal keeps the current horizontal axis"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(FVector2D(1.0f, 1.0f), EPokeMonsterFacingDirection::Left, 0.1f),
		EPokeMonsterFacingDirection::Right);

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

			LiveCharacter->Move(FInputActionValue(FVector2D(0.4f, 1.0f)));
			TestTrue(TEXT("PIE movement input reaches the character movement pipeline"),
				!LiveCharacter->GetPendingMovementInputVector().IsNearlyZero());
			TestEqual(TEXT("Movement changes the visual state to walking"),
				LiveCharacter->GetLocomotionState(), EPokeMonsterLocomotionState::Walking);
			TestEqual(TEXT("A vertical-dominant PIE input faces up"),
				LiveCharacter->GetFacingDirection(), EPokeMonsterFacingDirection::Up);
			LiveCharacter->ConsumeMovementInputVector();

			LiveCharacter->StopMoving(FInputActionValue(FVector2D::ZeroVector));
			TestTrue(TEXT("Stopping input resets the exposed movement input"),
				LiveCharacter->GetMovementInput().IsNearlyZero());
			TestEqual(TEXT("Stopping changes the visual state to idle"),
				LiveCharacter->GetLocomotionState(), EPokeMonsterLocomotionState::Idle);
			TestEqual(TEXT("Idle retains the last relevant facing direction"),
				LiveCharacter->GetFacingDirection(), EPokeMonsterFacingDirection::Up);

			LiveCharacter->Move(FInputActionValue(FVector2D(-1.0f, 0.25f)));
			TestEqual(TEXT("A horizontal-dominant PIE input faces left"),
				LiveCharacter->GetFacingDirection(), EPokeMonsterFacingDirection::Left);
			LiveCharacter->ConsumeMovementInputVector();
			LiveCharacter->StopMoving(FInputActionValue(FVector2D::ZeroVector));

			APokeMonsterInteractionTestActor* InteractionTarget = nullptr;
			TActorIterator<APokeMonsterInteractionTestActor> InteractionActorIt(PlayWorld);
			if (InteractionActorIt)
			{
				InteractionTarget = *InteractionActorIt;
			}

			if (TestNotNull(TEXT("Dev_TestMap contains the interaction test actor"), InteractionTarget))
			{
				const FTransform OriginalTransform = InteractionTarget->GetActorTransform();
				const FVector FacingDirection = LiveCharacter->GetInteractionWorldDirection();
				const int32 InitialInteractionCount = InteractionTarget->GetInteractionCount();

				InteractionTarget->SetActorLocation(
					LiveCharacter->GetActorLocation() + FacingDirection * 105.0f,
					false,
					nullptr,
					ETeleportType::TeleportPhysics);
				TestEqual(TEXT("The trace selects an interactable directly in front"),
					LiveCharacter->FindInteractableInRange(), static_cast<AActor*>(InteractionTarget));
				TestTrue(TEXT("A nearby target in front can be interacted with"), LiveCharacter->TryInteract());
				TestEqual(TEXT("The interaction reaches the target exactly once"),
					InteractionTarget->GetInteractionCount(), InitialInteractionCount + 1);

				InteractionTarget->SetActorLocation(
					LiveCharacter->GetActorLocation() + FacingDirection * (LiveCharacter->GetInteractionRange() + 150.0f),
					false,
					nullptr,
					ETeleportType::TeleportPhysics);
				TestFalse(TEXT("A target outside the configured range cannot be interacted with"), LiveCharacter->TryInteract());
				TestEqual(TEXT("An out-of-range attempt does not reach the target"),
					InteractionTarget->GetInteractionCount(), InitialInteractionCount + 1);

				InteractionTarget->SetActorLocation(
					LiveCharacter->GetActorLocation() - FacingDirection * 105.0f,
					false,
					nullptr,
					ETeleportType::TeleportPhysics);
				TestFalse(TEXT("A nearby target behind the player cannot be interacted with"), LiveCharacter->TryInteract());
				TestEqual(TEXT("A behind-the-player attempt does not reach the target"),
					InteractionTarget->GetInteractionCount(), InitialInteractionCount + 1);

				InteractionTarget->SetActorTransform(OriginalTransform, false, nullptr, ETeleportType::TeleportPhysics);
			}
		}
	}

	return true;
}

#endif
