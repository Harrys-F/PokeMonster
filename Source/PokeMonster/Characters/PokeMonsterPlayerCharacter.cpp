// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterPlayerCharacter.h"

#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/LocalPlayer.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "InputModifiers.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PaperFlipbook.h"
#include "PaperFlipbookComponent.h"
#include "Engine/World.h"
#include "UObject/ConstructorHelpers.h"

UPaperFlipbook* FPokeMonsterDirectionalFlipbookSet::GetFlipbook(const EPokeMonsterFacingDirection Direction) const
{
	switch (Direction)
	{
	case EPokeMonsterFacingDirection::Up:
		return Up;
	case EPokeMonsterFacingDirection::Down:
		return Down;
	case EPokeMonsterFacingDirection::Left:
		return Left;
	case EPokeMonsterFacingDirection::Right:
		return Right;
	default:
		return nullptr;
	}
}

bool FPokeMonsterDirectionalFlipbookSet::HasAnyFlipbook() const
{
	return Up || Down || Left || Right;
}

APokeMonsterPlayerCharacter::APokeMonsterPlayerCharacter()
{
	PrimaryActorTick.bCanEverTick = false;

	GetCapsuleComponent()->InitCapsuleSize(28.0f, 48.0f);

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	UCharacterMovementComponent* MovementComponent = GetCharacterMovement();
	MovementComponent->bOrientRotationToMovement = false;
	MovementComponent->MaxWalkSpeed = 420.0f;
	MovementComponent->MaxAcceleration = 1800.0f;
	MovementComponent->BrakingDecelerationWalking = 1600.0f;
	MovementComponent->GroundFriction = 8.0f;

	GetSprite()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	GetSprite()->SetCastShadow(false);

	PlaceholderMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PlaceholderMesh"));
	PlaceholderMesh->SetupAttachment(GetCapsuleComponent());
	PlaceholderMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	PlaceholderMesh->SetCastShadow(false);
	PlaceholderMesh->SetRelativeScale3D(FVector(0.4f, 0.12f, 0.85f));
	PlaceholderMesh->SetRelativeRotation(FRotator(0.0f, 45.0f, 0.0f));

	FacingMarkerMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("FacingMarkerMesh"));
	FacingMarkerMesh->SetupAttachment(GetCapsuleComponent());
	FacingMarkerMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	FacingMarkerMesh->SetCastShadow(false);
	FacingMarkerMesh->SetRelativeScale3D(FVector(0.12f));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> PlaceholderMeshAsset(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (PlaceholderMeshAsset.Succeeded())
	{
		PlaceholderMesh->SetStaticMesh(PlaceholderMeshAsset.Object);
	}

	static ConstructorHelpers::FObjectFinder<UStaticMesh> FacingMarkerAsset(TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	if (FacingMarkerAsset.Succeeded())
	{
		FacingMarkerMesh->SetStaticMesh(FacingMarkerAsset.Object);
	}

	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 1400.0f;
	CameraBoom->SetRelativeRotation(FRotator(-55.0f, -45.0f, 0.0f));
	CameraBoom->bUsePawnControlRotation = false;
	CameraBoom->bInheritPitch = false;
	CameraBoom->bInheritYaw = false;
	CameraBoom->bInheritRoll = false;
	CameraBoom->bDoCollisionTest = false;
	CameraBoom->bEnableCameraLag = true;
	CameraBoom->CameraLagSpeed = 6.0f;
	CameraBoom->CameraLagMaxDistance = 180.0f;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;
	FollowCamera->FieldOfView = 35.0f;

	MoveAction = CreateDefaultSubobject<UInputAction>(TEXT("MoveAction"));
	MoveAction->ValueType = EInputActionValueType::Axis2D;

	DefaultMappingContext = CreateDefaultSubobject<UInputMappingContext>(TEXT("DefaultMappingContext"));

	auto MapDigitalKey = [this](const FKey Key, const bool bNegate, const bool bSwizzle)
	{
		FEnhancedActionKeyMapping& Mapping = DefaultMappingContext->MapKey(MoveAction, Key);

		if (bSwizzle)
		{
			UInputModifierSwizzleAxis* Swizzle = NewObject<UInputModifierSwizzleAxis>(DefaultMappingContext);
			Swizzle->Order = EInputAxisSwizzle::YXZ;
			Mapping.Modifiers.Add(Swizzle);
		}

		if (bNegate)
		{
			Mapping.Modifiers.Add(NewObject<UInputModifierNegate>(DefaultMappingContext));
		}
	};

	MapDigitalKey(EKeys::W, false, true);
	MapDigitalKey(EKeys::S, true, true);
	MapDigitalKey(EKeys::D, false, false);
	MapDigitalKey(EKeys::A, true, false);
	MapDigitalKey(EKeys::Up, false, true);
	MapDigitalKey(EKeys::Down, true, true);
	MapDigitalKey(EKeys::Right, false, false);
	MapDigitalKey(EKeys::Left, true, false);

	InteractAction = CreateDefaultSubobject<UInputAction>(TEXT("InteractAction"));
	InteractAction->ValueType = EInputActionValueType::Boolean;
	DefaultMappingContext->MapKey(InteractAction, EKeys::E);
	DefaultMappingContext->MapKey(InteractAction, EKeys::Enter);
}

void APokeMonsterPlayerCharacter::BeginPlay()
{
	Super::BeginPlay();
	RefreshCharacterVisual();
}

void APokeMonsterPlayerCharacter::PawnClientRestart()
{
	Super::PawnClientRestart();

	const APlayerController* PlayerController = Cast<APlayerController>(Controller);
	if (!PlayerController)
	{
		return;
	}

	if (UEnhancedInputLocalPlayerSubsystem* InputSubsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
	{
		InputSubsystem->RemoveMappingContext(DefaultMappingContext);
		InputSubsystem->AddMappingContext(DefaultMappingContext, 0);
	}
}

void APokeMonsterPlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	UEnhancedInputComponent* EnhancedInputComponent = CastChecked<UEnhancedInputComponent>(PlayerInputComponent);
	EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &APokeMonsterPlayerCharacter::Move);
	EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Completed, this, &APokeMonsterPlayerCharacter::StopMoving);
	EnhancedInputComponent->BindAction(InteractAction, ETriggerEvent::Started, this, &APokeMonsterPlayerCharacter::Interact);
}

void APokeMonsterPlayerCharacter::Move(const FInputActionValue& Value)
{
	FVector2D Input = Value.Get<FVector2D>();
	Input = Input.GetClampedToMaxSize(1.0f);
	UpdateMovementInput(Input);

	const FVector WorldDirection = CalculateCameraRelativeMovement(Input, FollowCamera->GetComponentRotation().Yaw);
	AddMovementInput(WorldDirection);
}

void APokeMonsterPlayerCharacter::StopMoving(const FInputActionValue& Value)
{
	UpdateMovementInput(FVector2D::ZeroVector);
}

void APokeMonsterPlayerCharacter::Interact(const FInputActionValue& Value)
{
	TryInteract();
}

FVector APokeMonsterPlayerCharacter::GetInteractionWorldDirection() const
{
	FVector2D FacingInput = FVector2D::ZeroVector;
	switch (FacingDirection)
	{
	case EPokeMonsterFacingDirection::Up:
		FacingInput.Y = 1.0f;
		break;
	case EPokeMonsterFacingDirection::Down:
		FacingInput.Y = -1.0f;
		break;
	case EPokeMonsterFacingDirection::Left:
		FacingInput.X = -1.0f;
		break;
	case EPokeMonsterFacingDirection::Right:
		FacingInput.X = 1.0f;
		break;
	}

	return CalculateCameraRelativeMovement(FacingInput, FollowCamera->GetComponentRotation().Yaw);
}

AActor* APokeMonsterPlayerCharacter::FindInteractableInRange() const
{
	const UWorld* World = GetWorld();
	if (!World)
	{
		return nullptr;
	}

	const FVector Start = GetActorLocation();
	const FVector End = Start + GetInteractionWorldDirection() * InteractionRange;
	FCollisionQueryParams QueryParams(SCENE_QUERY_STAT(PokeMonsterInteraction), false, this);
	FHitResult Hit;
	const bool bHit = World->SweepSingleByChannel(
		Hit,
		Start,
		End,
		FQuat::Identity,
		ECC_Visibility,
		FCollisionShape::MakeSphere(InteractionTraceRadius),
		QueryParams);

	AActor* HitActor = bHit ? Hit.GetActor() : nullptr;
	return HitActor && HitActor->Implements<UPokeMonsterInteractable>() ? HitActor : nullptr;
}

bool APokeMonsterPlayerCharacter::TryInteract()
{
	AActor* Target = FindInteractableInRange();
	const bool bCanInteract = Target
		&& IPokeMonsterInteractable::Execute_CanInteract(Target, this);

	if (bCanInteract)
	{
		IPokeMonsterInteractable::Execute_Interact(Target, this);
	}

	OnInteractionAttempt(Target, bCanInteract);
	return bCanInteract;
}

void APokeMonsterPlayerCharacter::UpdateMovementInput(const FVector2D NewMovementInput)
{
	const FVector2D ClampedInput = NewMovementInput.GetClampedToMaxSize(1.0f);
	const bool bInputChanged = !MovementInput.Equals(ClampedInput, KINDA_SMALL_NUMBER);
	const EPokeMonsterLocomotionState NewLocomotionState = ClampedInput.IsNearlyZero(FacingInputThreshold)
		? EPokeMonsterLocomotionState::Idle
		: EPokeMonsterLocomotionState::Walking;
	const EPokeMonsterFacingDirection NewFacingDirection = NewLocomotionState == EPokeMonsterLocomotionState::Walking
		? CalculateFacingDirection(ClampedInput, FacingDirection, FacingInputThreshold)
		: FacingDirection;
	const bool bVisualStateChanged = NewLocomotionState != LocomotionState || NewFacingDirection != FacingDirection;

	if (!bInputChanged && !bVisualStateChanged)
	{
		return;
	}

	MovementInput = ClampedInput;
	FacingDirection = NewFacingDirection;
	LocomotionState = NewLocomotionState;

	if (bInputChanged)
	{
		OnMovementInputChanged(MovementInput);
	}

	if (bVisualStateChanged)
	{
		RefreshCharacterVisual();
		OnVisualStateChanged(FacingDirection, LocomotionState);
	}
}

void APokeMonsterPlayerCharacter::RefreshCharacterVisual()
{
	UPaperFlipbookComponent* SpriteComponent = GetSprite();
	const FPokeMonsterDirectionalFlipbookSet& DesiredSet = LocomotionState == EPokeMonsterLocomotionState::Walking
		? WalkingFlipbooks
		: IdleFlipbooks;
	UPaperFlipbook* DesiredFlipbook = DesiredSet.GetFlipbook(FacingDirection);

	// A missing walking animation falls back to the matching idle pose. This makes
	// partial Blueprint setups useful while the final art is still being produced.
	if (!DesiredFlipbook && LocomotionState == EPokeMonsterLocomotionState::Walking)
	{
		DesiredFlipbook = IdleFlipbooks.GetFlipbook(FacingDirection);
	}

	const bool bUsesDirectionalSets = IdleFlipbooks.HasAnyFlipbook() || WalkingFlipbooks.HasAnyFlipbook();
	if (DesiredFlipbook || bUsesDirectionalSets)
	{
		SpriteComponent->SetFlipbook(DesiredFlipbook);
	}

	const bool bHasFlipbook = SpriteComponent->GetFlipbook() != nullptr;
	SpriteComponent->SetVisibility(bHasFlipbook, true);

	const bool bShowPlaceholder = bShowPlaceholderWithoutFlipbook && !bHasFlipbook;
	PlaceholderMesh->SetVisibility(bShowPlaceholder, true);
	FacingMarkerMesh->SetVisibility(bShowPlaceholder, true);

	float FacingYaw = 135.0f;
	switch (FacingDirection)
	{
	case EPokeMonsterFacingDirection::Up:
		FacingYaw = -45.0f;
		break;
	case EPokeMonsterFacingDirection::Down:
		FacingYaw = 135.0f;
		break;
	case EPokeMonsterFacingDirection::Left:
		FacingYaw = -135.0f;
		break;
	case EPokeMonsterFacingDirection::Right:
		FacingYaw = 45.0f;
		break;
	}

	PlaceholderMesh->SetRelativeRotation(FRotator(0.0f, FacingYaw, 0.0f));
	const FVector FacingVector = FRotationMatrix(FRotator(0.0f, FacingYaw, 0.0f)).GetUnitAxis(EAxis::X);
	FacingMarkerMesh->SetRelativeLocation(FacingVector * 28.0f + FVector(0.0f, 0.0f, 20.0f));
}

FVector APokeMonsterPlayerCharacter::CalculateCameraRelativeMovement(const FVector2D Input, const float CameraYawDegrees)
{
	const FVector2D ClampedInput = Input.GetClampedToMaxSize(1.0f);
	const FRotator CameraYaw(0.0f, CameraYawDegrees, 0.0f);
	const FVector ForwardDirection = FRotationMatrix(CameraYaw).GetUnitAxis(EAxis::X);
	const FVector RightDirection = FRotationMatrix(CameraYaw).GetUnitAxis(EAxis::Y);
	return (ForwardDirection * ClampedInput.Y + RightDirection * ClampedInput.X).GetSafeNormal();
}

EPokeMonsterFacingDirection APokeMonsterPlayerCharacter::CalculateFacingDirection(
	const FVector2D Input,
	const EPokeMonsterFacingDirection CurrentDirection,
	const float InputThreshold)
{
	if (Input.IsNearlyZero(InputThreshold))
	{
		return CurrentDirection;
	}

	const float HorizontalStrength = FMath::Abs(Input.X);
	const float VerticalStrength = FMath::Abs(Input.Y);
	const bool bCurrentDirectionIsHorizontal = CurrentDirection == EPokeMonsterFacingDirection::Left
		|| CurrentDirection == EPokeMonsterFacingDirection::Right;
	const bool bUseHorizontal = HorizontalStrength > VerticalStrength
		|| (FMath::IsNearlyEqual(HorizontalStrength, VerticalStrength) && bCurrentDirectionIsHorizontal);

	if (bUseHorizontal)
	{
		return Input.X >= 0.0f ? EPokeMonsterFacingDirection::Right : EPokeMonsterFacingDirection::Left;
	}

	return Input.Y >= 0.0f ? EPokeMonsterFacingDirection::Up : EPokeMonsterFacingDirection::Down;
}
