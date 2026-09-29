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
#include "InputModifiers.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "PaperFlipbook.h"
#include "PaperFlipbookComponent.h"

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
	TestEqual(TEXT("Movement, interaction and menu provide twelve mappings"), Character->DefaultMappingContext->GetMappings().Num(), 12);

	bool bHasEInteraction = false;
	bool bHasEnterInteraction = false;
	bool bHasTabMenu = false;
	bool bHasDeadZonedLeftStick = false;
	for (const FEnhancedActionKeyMapping& Mapping : Character->DefaultMappingContext->GetMappings())
	{
		if (Mapping.Action == Character->InteractAction)
		{
			bHasEInteraction |= Mapping.Key == EKeys::E;
			bHasEnterInteraction |= Mapping.Key == EKeys::Enter;
		}
		if (Mapping.Action == Character->MenuAction)
			bHasTabMenu |= Mapping.Key == EKeys::Tab;
		if (Mapping.Action == Character->MoveAction && Mapping.Key == EKeys::Gamepad_Left2D)
		{
			for (const UInputModifier* Modifier : Mapping.Modifiers)
			{
				const UInputModifierDeadZone* DeadZone = Cast<UInputModifierDeadZone>(Modifier);
				bHasDeadZonedLeftStick |= DeadZone
					&& DeadZone->Type == EDeadZoneType::Radial
					&& FMath::IsNearlyEqual(DeadZone->LowerThreshold, 0.25f);
			}
		}
	}
	TestTrue(TEXT("E triggers the interaction action"), bHasEInteraction);
	TestTrue(TEXT("Enter triggers the interaction action"), bHasEnterInteraction);
	TestTrue(TEXT("Tab triggers the overworld menu"), bHasTabMenu);
	TestTrue(TEXT("The left stick uses the configured radial deadzone"), bHasDeadZonedLeftStick);
	TestEqual(TEXT("The runtime walk speed is exactly half of 420 cm/s"),
		Character->GetCharacterMovement()->MaxWalkSpeed, 210.0f);
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

	const struct { FVector2D Input; EPokeMonsterFacingDirection Expected; } Directions[] =
	{
		{ FVector2D(0, 1), EPokeMonsterFacingDirection::Up },
		{ FVector2D(1, 1), EPokeMonsterFacingDirection::UpRight },
		{ FVector2D(1, 0), EPokeMonsterFacingDirection::Right },
		{ FVector2D(1, -1), EPokeMonsterFacingDirection::DownRight },
		{ FVector2D(0, -1), EPokeMonsterFacingDirection::Down },
		{ FVector2D(-1, -1), EPokeMonsterFacingDirection::DownLeft },
		{ FVector2D(-1, 0), EPokeMonsterFacingDirection::Left },
		{ FVector2D(-1, 1), EPokeMonsterFacingDirection::UpLeft }
	};
	for (const auto& Direction : Directions)
	{
		TestEqual(TEXT("Each of the eight input sectors selects its facing"),
			APokeMonsterPlayerCharacter::CalculateFacingDirection(
				Direction.Input, EPokeMonsterFacingDirection::Down, 0.1f), Direction.Expected);
		const UPaperFlipbook* WalkFlipbook = Character->WalkingFlipbooks.GetFlipbook(Direction.Expected);
		const UPaperFlipbook* IdleFlipbook = Character->IdleFlipbooks.GetFlipbook(Direction.Expected);
		if (TestNotNull(TEXT("Every direction has a walking flipbook"), WalkFlipbook))
		{
			TestEqual(TEXT("Every walking flipbook alternates two frames"), WalkFlipbook->GetNumFrames(), 2);
			TestEqual(TEXT("Walking flipbooks play at eight frames per second"), WalkFlipbook->GetFramesPerSecond(), 8.0f);
			TestTrue(TEXT("Each walking pair uses distinct sprites"),
				WalkFlipbook->GetSpriteAtFrame(0) != WalkFlipbook->GetSpriteAtFrame(1));
		}
		if (TestNotNull(TEXT("Every direction has an idle flipbook"), IdleFlipbook))
		{
			TestEqual(TEXT("Idle flipbooks hold one frame"), IdleFlipbook->GetNumFrames(), 1);
		}
	}
	TestEqual(TEXT("Stick noise inside the facing threshold retains the last direction"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(
			FVector2D(0.04f, 0.03f), EPokeMonsterFacingDirection::UpLeft, 0.1f),
		EPokeMonsterFacingDirection::UpLeft);
	TestEqual(TEXT("Small angular changes at a sector boundary retain the last direction"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(
			FVector2D(FMath::Sin(FMath::DegreesToRadians(24.0f)),
				FMath::Cos(FMath::DegreesToRadians(24.0f))), EPokeMonsterFacingDirection::Up, 0.1f),
		EPokeMonsterFacingDirection::Up);
	TestEqual(TEXT("A clear angular change crosses the hysteresis band"),
		APokeMonsterPlayerCharacter::CalculateFacingDirection(
			FVector2D(FMath::Sin(FMath::DegreesToRadians(32.0f)),
				FMath::Cos(FMath::DegreesToRadians(32.0f))), EPokeMonsterFacingDirection::Up, 0.1f),
		EPokeMonsterFacingDirection::UpRight);

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
			TestEqual(TEXT("PIE uses the reduced walk speed"),
				LiveCharacter->GetCharacterMovement()->MaxWalkSpeed, 210.0f);

			for (const auto& Direction : Directions)
			{
				LiveCharacter->Move(FInputActionValue(Direction.Input));
				TestEqual(TEXT("PIE walking faces each of the eight directions"),
					LiveCharacter->GetFacingDirection(), Direction.Expected);
				TestEqual(TEXT("PIE movement enters walking state"),
					LiveCharacter->GetLocomotionState(), EPokeMonsterLocomotionState::Walking);
				const UPaperFlipbook* WalkFlipbook = LiveCharacter->GetCharacterFlipbookComponent()->GetFlipbook();
				if (TestNotNull(TEXT("Each PIE direction has a walking flipbook"), WalkFlipbook))
				{
					TestEqual(TEXT("Each walking flipbook has two frames"), WalkFlipbook->GetNumFrames(), 2);
					TestEqual(TEXT("Walking playback uses eight frames per second"), WalkFlipbook->GetFramesPerSecond(), 8.0f);
					TestTrue(TEXT("Walking frames are visually distinct sprite assets"),
						WalkFlipbook->GetSpriteAtFrame(0) != WalkFlipbook->GetSpriteAtFrame(1));
				}
				TestTrue(TEXT("PIE movement input has unit length, including diagonals"),
					FMath::IsNearlyEqual(LiveCharacter->GetPendingMovementInputVector().Size2D(), 1.0f, 0.01f));
				LiveCharacter->ConsumeMovementInputVector();
				LiveCharacter->StopMoving(FInputActionValue(FVector2D::ZeroVector));
				TestEqual(TEXT("PIE idle retains the last direction"),
					LiveCharacter->GetFacingDirection(), Direction.Expected);
				TestEqual(TEXT("PIE input release enters idle state"),
					LiveCharacter->GetLocomotionState(), EPokeMonsterLocomotionState::Idle);
				const UPaperFlipbook* IdleFlipbook = LiveCharacter->GetCharacterFlipbookComponent()->GetFlipbook();
				if (TestNotNull(TEXT("Each PIE direction has an idle flipbook"), IdleFlipbook))
				{
					TestEqual(TEXT("Idle holds a single frame"), IdleFlipbook->GetNumFrames(), 1);
					TestTrue(TEXT("Idle replaces the walking flipbook"), IdleFlipbook != WalkFlipbook);
				}
			}

			LiveCharacter->Move(FInputActionValue(FVector2D(0.6f, 1.0f)));
			TestTrue(TEXT("PIE movement input reaches the character movement pipeline"),
				!LiveCharacter->GetPendingMovementInputVector().IsNearlyZero());
			TestEqual(TEXT("Movement changes the visual state to walking"),
				LiveCharacter->GetLocomotionState(), EPokeMonsterLocomotionState::Walking);
			TestEqual(TEXT("An angled PIE input faces up-right"),
				LiveCharacter->GetFacingDirection(), EPokeMonsterFacingDirection::UpRight);
			LiveCharacter->ConsumeMovementInputVector();

			LiveCharacter->StopMoving(FInputActionValue(FVector2D::ZeroVector));
			TestTrue(TEXT("Stopping input resets the exposed movement input"),
				LiveCharacter->GetMovementInput().IsNearlyZero());
			TestEqual(TEXT("Stopping changes the visual state to idle"),
				LiveCharacter->GetLocomotionState(), EPokeMonsterLocomotionState::Idle);
			TestEqual(TEXT("Idle retains the last relevant facing direction"),
				LiveCharacter->GetFacingDirection(), EPokeMonsterFacingDirection::UpRight);

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
