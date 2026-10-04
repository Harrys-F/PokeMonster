#include "PokeMonsterBuildingCutaway.h"

#include "Components/BoxComponent.h"
#include "Camera/CameraTypes.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/PrimitiveComponent.h"
#include "Components/CapsuleComponent.h"
#include "Engine/World.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/PlayerCameraManager.h"
#include "Kismet/GameplayStatics.h"

namespace
{
	// The house's masked materials reserve this float for their dither mask.
	constexpr int32 CutawayDataIndex = 0;
}

APokeMonsterBuildingCutaway::APokeMonsterBuildingCutaway()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.TickInterval = 0.02f;
	InteriorArea = CreateDefaultSubobject<UBoxComponent>(TEXT("InteriorArea"));
	SetRootComponent(InteriorArea);
	InteriorArea->SetBoxExtent(FVector(490.f, 500.f, 250.f));
	InteriorArea->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	InteriorArea->SetGenerateOverlapEvents(false);

	DoorThreshold = CreateDefaultSubobject<UBoxComponent>(TEXT("DoorThreshold"));
	DoorThreshold->SetupAttachment(InteriorArea);
	DoorThreshold->SetRelativeLocation(FVector(-410.f, 0.f, -35.f));
	DoorThreshold->SetBoxExtent(FVector(20.f, 120.f, 115.f));
	DoorThreshold->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	DoorThreshold->SetGenerateOverlapEvents(false);

	RelocatedInteriorArea = CreateDefaultSubobject<UBoxComponent>(TEXT("RelocatedInteriorArea"));
	RelocatedInteriorArea->SetupAttachment(InteriorArea);
	RelocatedInteriorArea->SetRelativeLocation(FVector(20000.f, 0.f, 0.f));
	RelocatedInteriorArea->SetBoxExtent(FVector(600.f, 550.f, 250.f));
	RelocatedInteriorArea->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	RelocatedInteriorArea->SetGenerateOverlapEvents(false);
	RelocatedDoorThreshold = CreateDefaultSubobject<UBoxComponent>(TEXT("RelocatedDoorThreshold"));
	RelocatedDoorThreshold->SetupAttachment(RelocatedInteriorArea);
	RelocatedDoorThreshold->SetRelativeLocation(FVector(-600.f, 0.f, -42.5f));
	RelocatedDoorThreshold->SetBoxExtent(FVector(20.f, 75.f, 107.5f));
	RelocatedDoorThreshold->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	RelocatedDoorThreshold->SetGenerateOverlapEvents(false);
}

void APokeMonsterBuildingCutaway::GetInteriorCameraView(FMinimalViewInfo& OutView) const
{
	OutView.Rotation = FRotator(InteriorCameraPitch,
		DoorThreshold->GetComponentRotation().Yaw + InteriorCameraYawOffset, 0.f);
	const FVector Target = bUseRelocatedInterior
		? RelocatedInteriorArea->GetComponentTransform().TransformPosition(RelocatedCameraTarget)
		: InteriorArea->GetComponentTransform().TransformPosition(InteriorCameraTarget);
	OutView.Location = Target - OutView.Rotation.Vector() * InteriorCameraDistance;
}

bool APokeMonsterBuildingCutaway::IsViewerInside(FVector WorldLocation) const
{
	if (IsViewerInRelocatedRoom(WorldLocation)) return true;
	const FVector Local = InteriorArea->GetComponentTransform().InverseTransformPosition(WorldLocation);
	const FVector Extent = InteriorArea->GetUnscaledBoxExtent();
	const FVector DoorLocal = DoorThreshold->GetComponentTransform().InverseTransformPosition(WorldLocation);
	if (DoorLocal.X < 0.f) return false;
	if (InteriorRegions.IsEmpty())
		return FMath::Abs(Local.X) <= Extent.X && FMath::Abs(Local.Y) <= Extent.Y
			&& FMath::Abs(Local.Z) <= Extent.Z;
	for (const FPokeMonsterBuildingInteriorRegion& Region : InteriorRegions)
	{
		const FVector Offset = Local - Region.Center;
		if (Region.Extent.X > 0.f && Region.Extent.Y > 0.f && Region.Extent.Z > 0.f
			&& FMath::Abs(Offset.X) <= Region.Extent.X && FMath::Abs(Offset.Y) <= Region.Extent.Y
			&& FMath::Abs(Offset.Z) <= Region.Extent.Z) return true;
	}
	return false;
}

bool APokeMonsterBuildingCutaway::IsViewerInRelocatedRoom(FVector WorldLocation) const
{
	if (!bUseRelocatedInterior) return false;
	const FVector Local = RelocatedInteriorArea->GetComponentTransform().InverseTransformPosition(WorldLocation);
	const FVector Extent = RelocatedInteriorArea->GetUnscaledBoxExtent();
	return FMath::Abs(Local.X) <= Extent.X && FMath::Abs(Local.Y) <= Extent.Y
		&& FMath::Abs(Local.Z) <= Extent.Z;
}

FVector APokeMonsterBuildingCutaway::MapDoorwayPosition(FVector WorldLocation, bool bEntering) const
{
	const FTransform From = (bEntering ? DoorThreshold : RelocatedDoorThreshold)->GetComponentTransform();
	const FTransform To = (bEntering ? RelocatedDoorThreshold : DoorThreshold)->GetComponentTransform();
	return To.TransformPosition(From.InverseTransformPosition(WorldLocation));
}

float APokeMonsterBuildingCutaway::GetRelocationMask() const
{
	if (!bUseRelocatedInterior) return 0.f;
	const float Width = FMath::Clamp(RelocationMaskHalfWidth, .05f, .5f);
	return FMath::SmoothStep(0.f, 1.f, FMath::Clamp(1.f - FMath::Abs(CutawayAmount - .5f) / Width, 0.f, 1.f));
}

void APokeMonsterBuildingCutaway::ApplyRelocationMask(APawn* Player)
{
	const auto* Controller = Cast<APlayerController>(Player->GetController());
	if (!Controller || !Controller->PlayerCameraManager) return;
	const float Mask = GetRelocationMask();
	if (Mask > 0.f)
	{
		Controller->PlayerCameraManager->SetManualCameraFade(Mask, FLinearColor::Black, false);
		bOwnsCameraMask = true;
	}
	else if (bOwnsCameraMask)
	{
		Controller->PlayerCameraManager->StopCameraFade();
		bOwnsCameraMask = false;
	}
}

void APokeMonsterBuildingCutaway::UpdateRelocation(APawn* Player, bool bInside, float DeltaSeconds)
{
	const float Target = bInside ? 1.f : 0.f;
	const float Next = FMath::FInterpConstantTo(CutawayAmount, Target,
		FMath::Max(DeltaSeconds, 0.f), 1.f / FMath::Max(FadeDuration, .05f));
	if (bMidpointArmed)
	{
		bMidpointArmed = false;
		if (bInside != bViewerRelocated)
		{
			// One fully masked frame precedes the relocation. Held input is never cleared.
			const FVector Velocity = Player->GetVelocity();
			const FVector Destination = MapDoorwayPosition(Player->GetActorLocation(), bInside);
			FHitResult Hit;
			const auto* Character = Cast<ACharacter>(Player);
			const auto* Capsule = Character ? Character->GetCapsuleComponent() : nullptr;
			FCollisionQueryParams Query(SCENE_QUERY_STAT(BuildingRelocation), false, Player);
			const FCollisionShape Shape = Capsule
				? FCollisionShape::MakeCapsule(Capsule->GetScaledCapsuleRadius(), Capsule->GetScaledCapsuleHalfHeight())
				: FCollisionShape::MakeSphere(28.f);
			const bool bBlocked = GetWorld()->SweepSingleByChannel(Hit, Destination, Destination,
				FQuat::Identity, ECC_Pawn, Shape, Query);
			if (!bBlocked && Player->SetActorLocation(Destination, false, nullptr, ETeleportType::TeleportPhysics))
			{
				bViewerRelocated = bInside;
				if (auto* MovingCharacter = Cast<ACharacter>(Player))
				{
					MovingCharacter->GetCharacterMovement()->Velocity = Velocity;
					MovingCharacter->GetCharacterMovement()->bJustTeleported = true;
				}
				// Reset only the lag history at the hidden spatial cut, keeping its configuration.
				if (auto* Boom = Player->FindComponentByClass<USpringArmComponent>())
				{
					const bool bLag = Boom->bEnableCameraLag;
					Boom->bEnableCameraLag = false;
					Boom->TickComponent(0.f, LEVELTICK_All, nullptr);
					Boom->bEnableCameraLag = bLag;
				}
			}
			else
			{
				UE_LOG(LogTemp, Warning, TEXT("Building %s: relocation destination blocked; remaining on current side."), *GetName());
				bCutawayActive = bViewerRelocated;
				bRelocationRejected = true;
				CutawayAmount = bViewerRelocated ? 1.f : 0.f;
			}
		}
	}
	else if (bInside != bViewerRelocated && ((CutawayAmount <= .5f && Next >= .5f)
		|| (CutawayAmount >= .5f && Next <= .5f)))
	{
		CutawayAmount = .5f;
		bMidpointArmed = true;
	}
	else CutawayAmount = Next;
	ApplyRelocationMask(Player);
}

bool APokeMonsterBuildingCutaway::IsViewerInDoorway(FVector WorldLocation) const
{
	const FVector Local = DoorThreshold->GetComponentTransform().InverseTransformPosition(WorldLocation);
	const FVector Extent = DoorThreshold->GetUnscaledBoxExtent();
	return FMath::Abs(Local.X) <= Extent.X && FMath::Abs(Local.Y) <= Extent.Y
		&& FMath::Abs(Local.Z) <= Extent.Z;
}

void APokeMonsterBuildingCutaway::BeginPlay()
{
	Super::BeginPlay();
	if (bUseRelocatedInterior && (!bUseInteriorCamera
		|| !DoorThreshold->GetComponentRotation().Equals(RelocatedDoorThreshold->GetComponentRotation(), .1f)))
	{
		UE_LOG(LogTemp, Error, TEXT("Building %s: relocated interior requires an interior camera and aligned door axes."), *GetName());
		bUseRelocatedInterior = false;
	}
	if (bUseInteriorCamera) PrimaryActorTick.TickInterval = 0.f;
	RefreshVisibility(0.f);
}

void APokeMonsterBuildingCutaway::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	RefreshVisibility(DeltaSeconds);
}

void APokeMonsterBuildingCutaway::RefreshVisibility(float DeltaSeconds)
{
	APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	if (!Player) return;
	const float PreviousAmount = CutawayAmount;
	bool bInside = false;
	if (Player)
	{
		const FVector Position = Player->GetActorLocation();
		if (bUseRelocatedInterior && bViewerInitialized)
		{
			const bool bInRoom = IsViewerInRelocatedRoom(Position);
			const UBoxComponent* PreviousDoor = bViewerRelocated ? RelocatedDoorThreshold : DoorThreshold;
			// A checkpoint recovery or load may restore the pawn directly on either side.
			// Do not remap that independent world relocation as another doorway crossing.
			if (bInRoom != bViewerRelocated
				&& FVector::DistSquared(Position, PreviousDoor->GetComponentLocation()) > FMath::Square(500.f))
			{
				bViewerRelocated = bInRoom;
				CutawayAmount = bInRoom ? 1.f : 0.f;
				bMidpointArmed = bRelocationRejected = false;
				ApplyRelocationMask(Player);
			}
		}
		bInside = IsViewerInside(Position);
		const UBoxComponent* ActiveDoor = bUseRelocatedInterior && bViewerRelocated ? RelocatedDoorThreshold : DoorThreshold;
		const FVector DoorLocal = ActiveDoor->GetComponentTransform().InverseTransformPosition(Position);
		const FVector DoorExtent = ActiveDoor->GetUnscaledBoxExtent();
		const bool bInActiveDoor = FMath::Abs(DoorLocal.X) <= DoorExtent.X
			&& FMath::Abs(DoorLocal.Y) <= DoorExtent.Y && FMath::Abs(DoorLocal.Z) <= DoorExtent.Z;
		if (bUseRelocatedInterior && bViewerRelocated) bInside = IsViewerInRelocatedRoom(Position) && DoorLocal.X >= 0.f;
		if (bViewerInitialized && bInActiveDoor)
		{
			const float DoorX = DoorLocal.X;
			const float Band = FMath::Clamp(ThresholdHysteresis, 0.f,
				DoorThreshold->GetUnscaledBoxExtent().X);
			// Keep the previous side while standing on, or brushing, the threshold.
			bInside = DoorX > Band ? true : DoorX < -Band ? false : bCutawayActive;
		}
		if (bRelocationRejected)
		{
			if (bInside == bViewerRelocated) bRelocationRejected = false;
			else bInside = bViewerRelocated;
		}
	}
	bCutawayActive = bInside;
	const float Target = bInside ? 1.f : 0.f;
	if (!bViewerInitialized)
	{
		// A checkpoint/spawn already inside must not start beneath an opaque roof.
		CutawayAmount = Target;
		bViewerRelocated = IsViewerInRelocatedRoom(Player->GetActorLocation());
		bViewerInitialized = true;
	}
	else if (bUseRelocatedInterior) UpdateRelocation(Player, bInside, DeltaSeconds);
	else
	{
		CutawayAmount = FMath::FInterpConstantTo(CutawayAmount, Target,
			FMath::Max(DeltaSeconds, 0.f), 1.f / FMath::Max(FadeDuration, 0.05f));
		if (FMath::IsNearlyEqual(CutawayAmount, Target, KINDA_SMALL_NUMBER)) CutawayAmount = Target;
	}
	if (bUseInteriorCamera && (bCutawayActive || CutawayAmount > 0.f))
	{
		auto* Viewer = Cast<APokeMonsterPlayerCharacter>(Player);
		if (CameraViewer.Get() != Viewer)
			if (auto* PreviousViewer = CameraViewer.Get()) PreviousViewer->ClearInteriorCameraSource(this);
		CameraViewer = Viewer;
		if (Viewer) Viewer->SetInteriorCameraSource(this);
	}
	else if (auto* Viewer = CameraViewer.Get())
	{
		Viewer->ClearInteriorCameraSource(this);
		CameraViewer.Reset();
	}
	if (OriginalHiddenStates.IsEmpty() || PreviousAmount != CutawayAmount)
		ApplyVisibility();
}

void APokeMonsterBuildingCutaway::ApplyVisibility()
{
	for (AActor* Actor : OccludingActors)
	{
		if (!IsValid(Actor)) continue;
		const TWeakObjectPtr<AActor> Key(Actor);
		if (!OriginalHiddenStates.Contains(Key)) OriginalHiddenStates.Add(Key, Actor->IsHidden());
		TInlineComponentArray<UPrimitiveComponent*> Components(Actor);
		for (UPrimitiveComponent* Component : Components)
		{
			const TWeakObjectPtr<UPrimitiveComponent> ComponentKey(Component);
			if (!OriginalFadeData.Contains(ComponentKey))
			{
				const TArray<float>& Data = Component->GetCustomPrimitiveData().Data;
				OriginalFadeData.Add(ComponentKey, Data.IsValidIndex(CutawayDataIndex) ? Data[CutawayDataIndex] : 0.f);
			}
			Component->SetCustomPrimitiveDataFloat(CutawayDataIndex, CutawayAmount);
		}
		// Dither covers the entire transition; only its fully hidden endpoint skips rendering.
		Actor->SetActorHiddenInGame(CutawayAmount >= 1.f || OriginalHiddenStates.FindChecked(Key));
	}
}

void APokeMonsterBuildingCutaway::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (bOwnsCameraMask)
		if (auto* Viewer = CameraViewer.Get())
			if (auto* Controller = Cast<APlayerController>(Viewer->GetController()))
				if (Controller->PlayerCameraManager) Controller->PlayerCameraManager->StopCameraFade();
	if (auto* Viewer = CameraViewer.Get()) Viewer->ClearInteriorCameraSource(this);
	CameraViewer.Reset();
	for (const auto& Data : OriginalFadeData)
		if (UPrimitiveComponent* Component = Data.Key.Get())
			Component->SetCustomPrimitiveDataFloat(CutawayDataIndex, Data.Value);
	for (const auto& State : OriginalHiddenStates)
		if (AActor* Actor = State.Key.Get()) Actor->SetActorHiddenInGame(State.Value);
	OriginalFadeData.Reset();
	OriginalHiddenStates.Reset();
	Super::EndPlay(EndPlayReason);
}
