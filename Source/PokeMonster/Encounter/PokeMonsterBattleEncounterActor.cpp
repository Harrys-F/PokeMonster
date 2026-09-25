#include "PokeMonsterBattleEncounterActor.h"

#include "PokeMonsterEncounterSubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Components/SceneComponent.h"
#include "Engine/GameInstance.h"
#include "UObject/ConstructorHelpers.h"

APokeMonsterBattleEncounterActor::APokeMonsterBattleEncounterActor()
{
	PrimaryActorTick.bCanEverTick = false;
	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	SetRootComponent(SceneRoot);
	Marker = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("EncounterMarker"));
	Marker->SetupAttachment(SceneRoot);
	Marker->SetCollisionProfileName(TEXT("BlockAll"));
	Marker->SetRelativeScale3D(FVector(0.42f, 0.18f, 0.75f));
	Marker->SetCastShadow(false);
	static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (Cube.Succeeded()) Marker->SetStaticMesh(Cube.Object);
	static ConstructorHelpers::FObjectFinder<UMaterialInterface> Wood(TEXT("/Game/Environment/Prototype2D/Materials/M_WeatheredWood.M_WeatheredWood"));
	if (Wood.Succeeded()) Marker->SetMaterial(0, Wood.Object);
	Label = CreateDefaultSubobject<UTextRenderComponent>(TEXT("EncounterLabel"));
	Label->SetupAttachment(SceneRoot);
	Label->SetRelativeLocation(FVector(0.0f, 0.0f, 105.0f));
	Label->SetRelativeRotation(FRotator(0.0f, 180.0f, 0.0f));
	Label->SetText(FText::FromString(TEXT("Kampf · E")));
	Label->SetHorizontalAlignment(EHTA_Center);
	Label->SetWorldSize(30.0f);
	Label->SetTextRenderColor(FColor(238, 228, 186));
	Label->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Tags.Add(TEXT("BattleEncounterTest"));
}

bool APokeMonsterBattleEncounterActor::CanInteract_Implementation(APawn* Interactor) const
{
	const APokeMonsterPlayerCharacter* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	const UGameInstance* Instance = Player ? Player->GetGameInstance() : nullptr;
	const UPokeMonsterEncounterSubsystem* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	return Encounters && !Encounters->IsEncounterActive() && !Player->IsOverworldInputLocked();
}

void APokeMonsterBattleEncounterActor::Interact_Implementation(APawn* Interactor)
{
	APokeMonsterPlayerCharacter* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	UGameInstance* Instance = Player ? Player->GetGameInstance() : nullptr;
	if (UPokeMonsterEncounterSubsystem* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr)
		Encounters->StartTestEncounter(Player, this);
}
