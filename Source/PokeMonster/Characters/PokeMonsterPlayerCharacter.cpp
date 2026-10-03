// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterPlayerCharacter.h"

#include "Camera/CameraComponent.h"
#include "Camera/CameraTypes.h"
#include "../World/PokeMonsterBuildingCutaway.h"
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
#include "PaperSprite.h"
#include "Engine/World.h"
#include "UObject/ConstructorHelpers.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"

UPaperFlipbook* FPokeMonsterDirectionalFlipbookSet::GetFlipbook(const EPokeMonsterFacingDirection Direction) const
{
	switch (Direction)
	{
	case EPokeMonsterFacingDirection::Up:
		return Up;
	case EPokeMonsterFacingDirection::UpRight:
		return UpRight ? UpRight.Get() : (Right ? Right.Get() : Up.Get());
	case EPokeMonsterFacingDirection::Right:
		return Right;
	case EPokeMonsterFacingDirection::DownRight:
		return DownRight ? DownRight.Get() : (Right ? Right.Get() : Down.Get());
	case EPokeMonsterFacingDirection::Down:
		return Down;
	case EPokeMonsterFacingDirection::DownLeft:
		return DownLeft ? DownLeft.Get() : (Left ? Left.Get() : Down.Get());
	case EPokeMonsterFacingDirection::Left:
		return Left;
	case EPokeMonsterFacingDirection::UpLeft:
		return UpLeft ? UpLeft.Get() : (Left ? Left.Get() : Up.Get());
	default:
		return nullptr;
	}
}

bool FPokeMonsterDirectionalFlipbookSet::HasAnyFlipbook() const
{
	return Up || UpRight || Right || DownRight || Down || DownLeft || Left || UpLeft;
}

APokeMonsterPlayerCharacter::APokeMonsterPlayerCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = false;

	GetCapsuleComponent()->InitCapsuleSize(28.0f, 48.0f);

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	UCharacterMovementComponent* MovementComponent = GetCharacterMovement();
	MovementComponent->bOrientRotationToMovement = false;
	MovementComponent->MaxWalkSpeed = 210.0f;
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
	CameraBoom->TargetArmLength = 2500.0f;
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

	// Match the existing 0.25 gamepad axis deadzone with a radial 2D mapping.
	FEnhancedActionKeyMapping& StickMapping = DefaultMappingContext->MapKey(MoveAction, EKeys::Gamepad_Left2D);
	UInputModifierDeadZone* StickDeadZone = NewObject<UInputModifierDeadZone>(DefaultMappingContext);
	StickDeadZone->LowerThreshold = 0.25f;
	StickDeadZone->Type = EDeadZoneType::Radial;
	StickMapping.Modifiers.Add(StickDeadZone);

	InteractAction = CreateDefaultSubobject<UInputAction>(TEXT("InteractAction"));
	InteractAction->ValueType = EInputActionValueType::Boolean;
	DefaultMappingContext->MapKey(InteractAction, EKeys::E);
	DefaultMappingContext->MapKey(InteractAction, EKeys::Enter);

	MenuAction = CreateDefaultSubobject<UInputAction>(TEXT("MenuAction"));
	MenuAction->ValueType = EInputActionValueType::Boolean;
	DefaultMappingContext->MapKey(MenuAction, EKeys::Tab);

	// Keep the eight authored directions on the existing character class so the
	// default pawn in Dev_TestMap needs no map or GameMode override.
	auto FindPlayerFlipbook = [](const TCHAR* AssetName) -> UPaperFlipbook*
	{
		const FString Path = FString::Printf(
			TEXT("/Game/Characters/Prototype2D/Flipbooks/HobbitPlayer/%s.%s"), AssetName, AssetName);
		const ConstructorHelpers::FObjectFinder<UPaperFlipbook> Asset(*Path);
		return Asset.Succeeded() ? Asset.Object : nullptr;
	};
	IdleFlipbooks.Down = FindPlayerFlipbook(TEXT("FB_PlayerIdleDown"));
	IdleFlipbooks.DownRight = FindPlayerFlipbook(TEXT("FB_PlayerIdleDownRight"));
	IdleFlipbooks.Right = FindPlayerFlipbook(TEXT("FB_PlayerIdleRight"));
	IdleFlipbooks.UpRight = FindPlayerFlipbook(TEXT("FB_PlayerIdleUpRight"));
	IdleFlipbooks.Up = FindPlayerFlipbook(TEXT("FB_PlayerIdleUp"));
	IdleFlipbooks.UpLeft = FindPlayerFlipbook(TEXT("FB_PlayerIdleUpLeft"));
	IdleFlipbooks.Left = FindPlayerFlipbook(TEXT("FB_PlayerIdleLeft"));
	IdleFlipbooks.DownLeft = FindPlayerFlipbook(TEXT("FB_PlayerIdleDownLeft"));
	WalkingFlipbooks.Down = FindPlayerFlipbook(TEXT("FB_PlayerWalkDown"));
	WalkingFlipbooks.DownRight = FindPlayerFlipbook(TEXT("FB_PlayerWalkDownRight"));
	WalkingFlipbooks.Right = FindPlayerFlipbook(TEXT("FB_PlayerWalkRight"));
	WalkingFlipbooks.UpRight = FindPlayerFlipbook(TEXT("FB_PlayerWalkUpRight"));
	WalkingFlipbooks.Up = FindPlayerFlipbook(TEXT("FB_PlayerWalkUp"));
	WalkingFlipbooks.UpLeft = FindPlayerFlipbook(TEXT("FB_PlayerWalkUpLeft"));
	WalkingFlipbooks.Left = FindPlayerFlipbook(TEXT("FB_PlayerWalkLeft"));
	WalkingFlipbooks.DownLeft = FindPlayerFlipbook(TEXT("FB_PlayerWalkDownLeft"));
}

void APokeMonsterPlayerCharacter::BeginPlay()
{
	Super::BeginPlay();
	// Directional illustrated stand-ins remain replaceable by authored Blueprint flipbooks.
	if (!IdleFlipbooks.HasAnyFlipbook() && !WalkingFlipbooks.HasAnyFlipbook())
	{
		auto MakeStillFlipbook = [this](const TCHAR* SpritePath) -> UPaperFlipbook*
		{
			UPaperSprite* StandIn = LoadObject<UPaperSprite>(nullptr, SpritePath);
			if (!StandIn) return nullptr;
			UPaperFlipbook* StandInFlipbook = NewObject<UPaperFlipbook>(this);
			{
				FScopedFlipbookMutator FlipbookEdit(StandInFlipbook);
				FPaperFlipbookKeyFrame& Frame = FlipbookEdit.KeyFrames.AddDefaulted_GetRef();
				Frame.Sprite = StandIn;
			}
			return StandInFlipbook;
		};
		IdleFlipbooks.Down = MakeStillFlipbook(TEXT("/Game/Characters/Prototype2D/Sprites/S_PlayerDown.S_PlayerDown"));
		IdleFlipbooks.Up = MakeStillFlipbook(TEXT("/Game/Characters/Prototype2D/Sprites/S_PlayerUp.S_PlayerUp"));
		IdleFlipbooks.Left = MakeStillFlipbook(TEXT("/Game/Characters/Prototype2D/Sprites/S_PlayerLeft.S_PlayerLeft"));
		IdleFlipbooks.Right = MakeStillFlipbook(TEXT("/Game/Characters/Prototype2D/Sprites/S_PlayerRight.S_PlayerRight"));
	}
	if (IdleFlipbooks.HasAnyFlipbook() || WalkingFlipbooks.HasAnyFlipbook())
	{
		GetSprite()->SetRelativeRotation(FRotator(0.f, 45.f, 0.f));
		// Upright Paper2D geometry gives real 140 cm height and correct counter occlusion.
		// Sprite assets share a visible sole pivot and normalized body heights.
		GetSprite()->SetRelativeScale3D(FVector(0.66f, 0.66f, 140.f * 3.4f / 438.f));
		GetSprite()->SetRelativeLocation(FVector(0.f, 0.f, -GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight()));
		GetSprite()->SetSpriteColor(FLinearColor::White);
	}
	RefreshCharacterVisual();
}

float APokeMonsterPlayerCharacter::GetMovementBasisYaw() const
{
	return bMovementBasisOverride ? MovementBasisYaw : FollowCamera->GetComponentRotation().Yaw;
}

float APokeMonsterPlayerCharacter::GetPresentationCameraYaw() const
{
	const FRotator Exterior = FollowCamera->GetComponentRotation();
	const auto* Building = InteriorCameraSource.Get();
	if (!IsValid(Building) || !Building->bUseInteriorCamera) return Exterior.Yaw;
	FMinimalViewInfo Interior;
	Building->GetInteriorCameraView(Interior);
	const float Alpha = FMath::SmoothStep(0.f, 1.f, Building->GetCutawayAmount());
	return FQuat::Slerp(Exterior.Quaternion(), Interior.Rotation.Quaternion(), Alpha).Rotator().Yaw;
}

void APokeMonsterPlayerCharacter::SetInteriorCameraSource(APokeMonsterBuildingCutaway* Building)
{
	if (!bMovementBasisOverride) MovementBasisYaw = GetMovementBasisYaw();
	InteriorCameraSource = Building;
	bMovementBasisOverride = true;
	// Latch only a completed camera endpoint; a partial reversal does not switch input.
	if (Building && Building->GetCutawayAmount() >= 1.f) bInteriorMovementBasis = true;
	SetActorTickEnabled(true);
}

void APokeMonsterPlayerCharacter::ClearInteriorCameraSource(const APokeMonsterBuildingCutaway* Building)
{
	if (InteriorCameraSource.Get() != Building) return;
	InteriorCameraSource.Reset();
	bInteriorMovementBasis = false;
	// Keep ticking until the brief post-camera input blend has reached the exterior.
}

void APokeMonsterPlayerCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	const auto* Building = InteriorCameraSource.Get();
	const bool bHasBuilding = IsValid(Building) && Building->bUseInteriorCamera;
	if (!bHasBuilding) bInteriorMovementBasis = false;
	float TargetYaw = FollowCamera->GetComponentRotation().Yaw;
	if (bInteriorMovementBasis && bHasBuilding)
	{
		FMinimalViewInfo Interior;
		Building->GetInteriorCameraView(Interior);
		TargetYaw = Interior.Rotation.Yaw;
	}
	// 45 degrees in 0.18 s, only after the view has completed. Never reset held input.
	MovementBasisYaw = FRotator::NormalizeAxis(FMath::FixedTurn(MovementBasisYaw, TargetYaw, 250.f * FMath::Max(DeltaSeconds, 0.f)));
	GetSprite()->SetWorldRotation(FRotator(0.f, GetPresentationCameraYaw() + 90.f, 0.f));
	UpdateMovementInput(MovementInput);
	if (!bHasBuilding && FMath::IsNearlyZero(FMath::FindDeltaAngleDegrees(MovementBasisYaw, TargetYaw)))
	{
		bMovementBasisOverride = false;
		SetActorTickEnabled(false);
	}
}

void APokeMonsterPlayerCharacter::CalcCamera(float DeltaTime, FMinimalViewInfo& OutResult)
{
	Super::CalcCamera(DeltaTime, OutResult);
	const APokeMonsterBuildingCutaway* Building = InteriorCameraSource.Get();
	if (!IsValid(Building) || !Building->bUseInteriorCamera) return;
	const float Progress = FMath::Clamp(Building->GetCutawayAmount(), 0.f, 1.f);
	if (Progress <= 0.f) return;
	const float Alpha = FMath::SmoothStep(0.f, 1.f, Progress);
	FMinimalViewInfo InteriorView = OutResult;
	Building->GetInteriorCameraView(InteriorView);
	OutResult.Location = FMath::Lerp(OutResult.Location, InteriorView.Location, Alpha);
	OutResult.Rotation = FQuat::Slerp(OutResult.Rotation.Quaternion(),
		InteriorView.Rotation.Quaternion(), Alpha).Rotator();
	// FOV/projection stay inherited from the existing camera. Only the rendered POV
	// changes; movement switches separately, only at completed view endpoints.
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
	EnhancedInputComponent->BindAction(MenuAction, ETriggerEvent::Started, this, &APokeMonsterPlayerCharacter::ToggleOverworldMenu);
}

void APokeMonsterPlayerCharacter::Move(const FInputActionValue& Value)
{
	if (bOverworldInputLocked) return;
	FVector2D Input = Value.Get<FVector2D>();
	Input = Input.GetClampedToMaxSize(1.0f);
	UpdateMovementInput(Input);

	const FVector WorldDirection = CalculateCameraRelativeMovement(Input, GetMovementBasisYaw());
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

void APokeMonsterPlayerCharacter::ToggleOverworldMenu(const FInputActionValue& Value)
{
	if (auto* OverworldController = Cast<APokeMonsterOverworldPlayerController>(GetController()))
		OverworldController->ToggleMenu();
}

FVector APokeMonsterPlayerCharacter::GetInteractionWorldDirection() const
{
	if (bHasWorldFacing) return LastWorldFacing;
	FVector2D FacingInput = FVector2D::ZeroVector;
	switch (FacingDirection)
	{
	case EPokeMonsterFacingDirection::Up:
		FacingInput.Y = 1.0f;
		break;
	case EPokeMonsterFacingDirection::UpRight:
		FacingInput = FVector2D(1.0f, 1.0f);
		break;
	case EPokeMonsterFacingDirection::DownRight:
		FacingInput = FVector2D(1.0f, -1.0f);
		break;
	case EPokeMonsterFacingDirection::Down:
		FacingInput.Y = -1.0f;
		break;
	case EPokeMonsterFacingDirection::DownLeft:
		FacingInput = FVector2D(-1.0f, -1.0f);
		break;
	case EPokeMonsterFacingDirection::Left:
		FacingInput.X = -1.0f;
		break;
	case EPokeMonsterFacingDirection::Right:
		FacingInput.X = 1.0f;
		break;
	case EPokeMonsterFacingDirection::UpLeft:
		FacingInput = FVector2D(-1.0f, 1.0f);
		break;
	}

	return CalculateCameraRelativeMovement(FacingInput, GetMovementBasisYaw());
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
	if (bOverworldInputLocked) return false;
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

void APokeMonsterPlayerCharacter::SetOverworldInputLocked(const bool bLocked)
{
	if (bOverworldInputLocked == bLocked) return;
	bOverworldInputLocked = bLocked;
	if (bLocked)
	{
		UpdateMovementInput(FVector2D::ZeroVector);
		GetCharacterMovement()->StopMovementImmediately();
	}
}

void APokeMonsterPlayerCharacter::PMSave()
{
	if (auto* Save = GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>()) Save->SaveCurrentGame();
}

void APokeMonsterPlayerCharacter::PMLoad()
{
	if (auto* Save = GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>()) Save->LoadGame();
}

void APokeMonsterPlayerCharacter::PMHasSave()
{
	if (auto* Save = GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>())
		UE_LOG(LogTemp, Display, TEXT("PokeMonster_Dev save exists: %s"), Save->HasSaveGame() ? TEXT("yes") : TEXT("no"));
}

void APokeMonsterPlayerCharacter::PMDeleteDevSave()
{
	if (auto* Save = GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>()) Save->DeleteDevSave();
}

void APokeMonsterPlayerCharacter::PMDevSaveRoundTrip()
{
	if (auto* Save = GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>()) Save->RunDevRoundTripTest();
}

void APokeMonsterPlayerCharacter::PMDevDefeatReturn()
{
#if !UE_BUILD_SHIPPING
	auto* Encounters = GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	if (!Encounters || !Encounters->EnsureDevPlayerParty() || !Species || !Move
		|| Encounters->IsEncounterActive() || Encounters->GetPlayerParty().IsEmpty()) return;
	FPokeMonsterEncounterStartData Start;
	Start.EncounterId = TEXT("Dev_ForcedDefeat");
	Start.Kind = EPokeMonsterEncounterKind::Wild;
	Start.PlayerTeam.Add(Encounters->GetPlayerParty()[0]);
	Start.PlayerTeam[0].CurrentHP = 1;
	Start.PlayerTeam[0].CalculatedStats.Speed = 1;
	auto Opponent = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 100);
	if (!Opponent.AssignMove(0, Move)) return;
	Opponent.CalculatedStats.Attack = 1000;
	Opponent.CalculatedStats.Speed = 1000;
	Start.OpponentTeam.Add(MoveTemp(Opponent));
	if (Encounters->StartEncounter(Start, this))
		UE_LOG(LogTemp, Display, TEXT("Dev defeat battle started. Select any move to test checkpoint return."));
#endif
}

void APokeMonsterPlayerCharacter::UpdateMovementInput(const FVector2D NewMovementInput)
{
	const FVector2D ClampedInput = NewMovementInput.GetClampedToMaxSize(1.0f);
	const bool bInputChanged = !MovementInput.Equals(ClampedInput, KINDA_SMALL_NUMBER);
	const EPokeMonsterLocomotionState NewLocomotionState = ClampedInput.IsNearlyZero(FacingInputThreshold)
		? EPokeMonsterLocomotionState::Idle
		: EPokeMonsterLocomotionState::Walking;
	if (NewLocomotionState == EPokeMonsterLocomotionState::Walking)
	{
		LastWorldFacing = CalculateCameraRelativeMovement(ClampedInput, GetMovementBasisYaw());
		bHasWorldFacing = true;
	}
	const FRotationMatrix ViewAxes(FRotator(0.f, GetPresentationCameraYaw(), 0.f));
	const FVector WorldFacing = GetInteractionWorldDirection();
	const FVector2D ScreenFacing(FVector::DotProduct(WorldFacing, ViewAxes.GetUnitAxis(EAxis::Y)),
		FVector::DotProduct(WorldFacing, ViewAxes.GetUnitAxis(EAxis::X)));
	const EPokeMonsterFacingDirection NewFacingDirection = bHasWorldFacing
		? CalculateFacingDirection(ScreenFacing, FacingDirection, FacingInputThreshold)
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

	const float FacingYaw = GetInteractionWorldDirection().Rotation().Yaw;
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

	// Angle zero is screen-up; enum order then follows clockwise in 45-degree steps.
	const float Angle = FMath::Fmod(
		FMath::RadiansToDegrees(FMath::Atan2(Input.X, Input.Y)) + 360.0f, 360.0f);
	const int32 CandidateIndex = FMath::FloorToInt((Angle + 22.5f) / 45.0f) % 8;
	const int32 CurrentIndex = static_cast<int32>(CurrentDirection);
	const float CurrentCenter = CurrentIndex * 45.0f;
	const float DistanceFromCurrent = FMath::Abs(FMath::FindDeltaAngleDegrees(Angle, CurrentCenter));
	// Eight extra degrees around a sector boundary stop small stick changes flickering.
	if (CandidateIndex != CurrentIndex && DistanceFromCurrent <= 30.5f)
	{
		return CurrentDirection;
	}
	return static_cast<EPokeMonsterFacingDirection>(CandidateIndex);
}
