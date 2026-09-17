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
#include "PaperFlipbookComponent.h"
#include "UObject/ConstructorHelpers.h"

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

	static ConstructorHelpers::FObjectFinder<UStaticMesh> PlaceholderMeshAsset(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (PlaceholderMeshAsset.Succeeded())
	{
		PlaceholderMesh->SetStaticMesh(PlaceholderMeshAsset.Object);
	}

	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 900.0f;
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
}

void APokeMonsterPlayerCharacter::BeginPlay()
{
	Super::BeginPlay();

	const bool bHasFlipbook = GetSprite()->GetFlipbook() != nullptr;
	PlaceholderMesh->SetVisibility(bShowPlaceholderWithoutFlipbook && !bHasFlipbook, true);
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

void APokeMonsterPlayerCharacter::UpdateMovementInput(const FVector2D NewMovementInput)
{
	if (MovementInput.Equals(NewMovementInput, KINDA_SMALL_NUMBER))
	{
		return;
	}

	MovementInput = NewMovementInput;
	OnMovementInputChanged(MovementInput);
}

FVector APokeMonsterPlayerCharacter::CalculateCameraRelativeMovement(const FVector2D Input, const float CameraYawDegrees)
{
	const FVector2D ClampedInput = Input.GetClampedToMaxSize(1.0f);
	const FRotator CameraYaw(0.0f, CameraYawDegrees, 0.0f);
	const FVector ForwardDirection = FRotationMatrix(CameraYaw).GetUnitAxis(EAxis::X);
	const FVector RightDirection = FRotationMatrix(CameraYaw).GetUnitAxis(EAxis::Y);
	return (ForwardDirection * ClampedInput.Y + RightDirection * ClampedInput.X).GetSafeNormal();
}
