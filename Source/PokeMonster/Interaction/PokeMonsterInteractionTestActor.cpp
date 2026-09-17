// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterInteractionTestActor.h"

#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/Pawn.h"
#include "UObject/ConstructorHelpers.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterInteraction, Log, All);

APokeMonsterInteractionTestActor::APokeMonsterInteractionTestActor()
{
	PrimaryActorTick.bCanEverTick = false;

	Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
	SetRootComponent(Mesh);
	Mesh->SetCollisionProfileName(TEXT("BlockAll"));
	Mesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.85f));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeAsset(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (CubeAsset.Succeeded())
	{
		Mesh->SetStaticMesh(CubeAsset.Object);
	}

	InteractionLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("InteractionLight"));
	InteractionLight->SetupAttachment(Mesh);
	InteractionLight->SetRelativeLocation(FVector(0.0f, 0.0f, 85.0f));
	InteractionLight->SetLightColor(FLinearColor(0.2f, 1.0f, 0.25f));
	InteractionLight->SetIntensity(2500.0f);
	InteractionLight->SetAttenuationRadius(240.0f);
	InteractionLight->SetVisibility(false);

	Tags.Add(TEXT("InteractionTest"));
}

bool APokeMonsterInteractionTestActor::CanInteract_Implementation(APawn* Interactor) const
{
	return IsValid(Interactor);
}

void APokeMonsterInteractionTestActor::Interact_Implementation(APawn* Interactor)
{
	++InteractionCount;
	bInteractionActive = !bInteractionActive;
	InteractionLight->SetVisibility(bInteractionActive);
	Mesh->SetRelativeScale3D(bInteractionActive
		? FVector(0.65f, 0.65f, 1.0f)
		: FVector(0.55f, 0.55f, 0.85f));

	UE_LOG(LogPokeMonsterInteraction, Display,
		TEXT("Interaction test actor '%s' used by '%s' (count: %d, active: %s)."),
		*GetName(),
		Interactor ? *Interactor->GetName() : TEXT("None"),
		InteractionCount,
		bInteractionActive ? TEXT("true") : TEXT("false"));
}
