#include "PokeMonsterBuildingCutaway.h"

#include "Components/BoxComponent.h"
#include "Camera/CameraTypes.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/PrimitiveComponent.h"
#include "GameFramework/Pawn.h"
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
}

void APokeMonsterBuildingCutaway::GetInteriorCameraView(FMinimalViewInfo& OutView) const
{
	OutView.Rotation = FRotator(InteriorCameraPitch,
		DoorThreshold->GetComponentRotation().Yaw + InteriorCameraYawOffset, 0.f);
	const FVector Target = InteriorArea->GetComponentTransform().TransformPosition(InteriorCameraTarget);
	OutView.Location = Target - OutView.Rotation.Vector() * InteriorCameraDistance;
}

bool APokeMonsterBuildingCutaway::IsViewerInside(FVector WorldLocation) const
{
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
	bool bInside = false;
	if (Player)
	{
		const FVector Position = Player->GetActorLocation();
		bInside = IsViewerInside(Position);
		if (bViewerInitialized && IsViewerInDoorway(Position))
		{
			const float DoorX = DoorThreshold->GetComponentTransform().InverseTransformPosition(Position).X;
			const float Band = FMath::Clamp(ThresholdHysteresis, 0.f,
				DoorThreshold->GetUnscaledBoxExtent().X);
			// Keep the previous side while standing on, or brushing, the threshold.
			bInside = DoorX > Band ? true : DoorX < -Band ? false : bCutawayActive;
		}
	}
	bCutawayActive = bInside;
	const float Target = bInside ? 1.f : 0.f;
	const float PreviousAmount = CutawayAmount;
	if (!bViewerInitialized)
	{
		// A checkpoint/spawn already inside must not start beneath an opaque roof.
		CutawayAmount = Target;
		bViewerInitialized = true;
	}
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
