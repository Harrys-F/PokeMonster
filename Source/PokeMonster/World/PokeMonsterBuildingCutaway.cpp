#include "PokeMonsterBuildingCutaway.h"

#include "Components/BoxComponent.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"

APokeMonsterBuildingCutaway::APokeMonsterBuildingCutaway()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.TickInterval = 0.1f;
	InteriorArea = CreateDefaultSubobject<UBoxComponent>(TEXT("InteriorArea"));
	SetRootComponent(InteriorArea);
	InteriorArea->SetBoxExtent(FVector(570.f, 580.f, 250.f));
	InteriorArea->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	InteriorArea->SetGenerateOverlapEvents(false);
}

bool APokeMonsterBuildingCutaway::IsViewerInside(FVector WorldLocation) const
{
	const FVector Local = InteriorArea->GetComponentTransform().InverseTransformPosition(WorldLocation);
	const FVector Extent = InteriorArea->GetUnscaledBoxExtent();
	return FMath::Abs(Local.X) <= Extent.X && FMath::Abs(Local.Y) <= Extent.Y
		&& FMath::Abs(Local.Z) <= Extent.Z;
}

void APokeMonsterBuildingCutaway::BeginPlay()
{
	Super::BeginPlay();
	RefreshVisibility();
}

void APokeMonsterBuildingCutaway::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	RefreshVisibility();
}

void APokeMonsterBuildingCutaway::RefreshVisibility()
{
	const APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	ApplyVisibility(Player && IsViewerInside(Player->GetActorLocation()));
}

void APokeMonsterBuildingCutaway::ApplyVisibility(bool bInside)
{
	bCutawayActive = bInside;
	for (AActor* Actor : OccludingActors)
	{
		if (!IsValid(Actor)) continue;
		const TWeakObjectPtr<AActor> Key(Actor);
		if (!OriginalHiddenStates.Contains(Key)) OriginalHiddenStates.Add(Key, Actor->IsHidden());
		Actor->SetActorHiddenInGame(bInside || OriginalHiddenStates.FindChecked(Key));
	}
}

void APokeMonsterBuildingCutaway::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	for (const auto& State : OriginalHiddenStates)
	{
		if (AActor* Actor = State.Key.Get()) Actor->SetActorHiddenInGame(State.Value);
	}
	OriginalHiddenStates.Reset();
	Super::EndPlay(EndPlayReason);
}
