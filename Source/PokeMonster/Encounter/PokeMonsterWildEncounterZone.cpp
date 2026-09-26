#include "PokeMonsterWildEncounterZone.h"

#include "PokeMonsterEncounterSubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "UObject/ConstructorHelpers.h"

APokeMonsterWildEncounterZone::APokeMonsterWildEncounterZone()
{
	PrimaryActorTick.bCanEverTick = false;
	Trigger = CreateDefaultSubobject<UBoxComponent>(TEXT("EncounterTrigger"));
	SetRootComponent(Trigger);
	Trigger->InitBoxExtent(FVector(85.f, 85.f, 65.f));
	Trigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	Trigger->SetCollisionResponseToAllChannels(ECR_Ignore);
	Trigger->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	Trigger->OnComponentBeginOverlap.AddDynamic(this, &APokeMonsterWildEncounterZone::OnEntered);
	GroundMarker = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("GroundMarker"));
	GroundMarker->SetupAttachment(Trigger);
	GroundMarker->SetRelativeLocation(FVector(0.f, 0.f, -62.f));
	GroundMarker->SetRelativeScale3D(FVector(1.7f, 1.7f, 0.008f));
	GroundMarker->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	GroundMarker->SetCastShadow(false);
	static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (Cube.Succeeded()) GroundMarker->SetStaticMesh(Cube.Object);
	static ConstructorHelpers::FObjectFinder<UMaterialInterface> Grass(TEXT("/Game/Environment/Prototype2D/Materials/M_GrassTuft.M_GrassTuft"));
	if (Grass.Succeeded()) GroundMarker->SetMaterial(0, Grass.Object);
	Label = CreateDefaultSubobject<UTextRenderComponent>(TEXT("ZoneLabel"));
	Label->SetupAttachment(Trigger);
	Label->SetRelativeLocation(FVector(0.f, 0.f, 75.f));
	Label->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	Label->SetText(FText::FromString(TEXT("Wild-Zone")));
	Label->SetHorizontalAlignment(EHTA_Center);
	Label->SetWorldSize(23.f);
	Label->SetTextRenderColor(FColor(230, 224, 183));
	Label->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Profile = TSoftObjectPtr<UPokeMonsterEncounterProfile>(FSoftObjectPath(TEXT("/Game/Data/Encounters/DA_DevWild.DA_DevWild")));
	Tags.Add(TEXT("WildEncounterZone"));
}

void APokeMonsterWildEncounterZone::BeginPlay()
{
	Super::BeginPlay();
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterEncounterSubsystem* Encounters = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounters->OnPersistentStateRestored.AddUniqueDynamic(this, &APokeMonsterWildEncounterZone::RefreshPersistentState);
			RefreshPersistentState();
		}
}

void APokeMonsterWildEncounterZone::RefreshPersistentState()
{
	const UGameInstance* Instance = GetGameInstance();
	const auto* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	bTriggered = Encounters && Encounters->IsEncounterCompleted(EncounterId);
}

void APokeMonsterWildEncounterZone::OnEntered(UPrimitiveComponent*, AActor* OtherActor,
	UPrimitiveComponent*, int32, bool, const FHitResult&)
{
	if (bTriggered) return;
	auto* Player = Cast<APokeMonsterPlayerCharacter>(OtherActor);
	if (!Player || Player->IsOverworldInputLocked()) return;
	UGameInstance* Instance = Player->GetGameInstance();
	UPokeMonsterEncounterSubsystem* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	if (!Encounters || Encounters->IsEncounterActive()) return;
	UPokeMonsterEncounterProfile* LoadedProfile = Profile.LoadSynchronous();
	if (LoadedProfile && Encounters->EnsureDevPlayerParty()
		&& Encounters->StartWildEncounter(LoadedProfile, Context, EPokeMonsterEncounterSource::Zone,
			Player, this, Seed, EncounterId))
	{
		bTriggered = true;
		Encounters->MarkEncounterCompleted(EncounterId);
	}
}
