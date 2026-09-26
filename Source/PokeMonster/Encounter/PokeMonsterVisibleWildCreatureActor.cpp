#include "PokeMonsterVisibleWildCreatureActor.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Components/SphereComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "PaperSprite.h"
#include "PaperSpriteComponent.h"
#include "UObject/ConstructorHelpers.h"

APokeMonsterVisibleWildCreatureActor::APokeMonsterVisibleWildCreatureActor()
{
	PrimaryActorTick.bCanEverTick = false;
	Body = CreateDefaultSubobject<UCapsuleComponent>(TEXT("Body"));
	SetRootComponent(Body);
	Body->InitCapsuleSize(38.f, 60.f);
	Body->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	Body->SetCollisionResponseToAllChannels(ECR_Ignore);
	Body->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
	Body->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	ContactRange = CreateDefaultSubobject<USphereComponent>(TEXT("ContactRange"));
	ContactRange->SetupAttachment(Body);
	ContactRange->InitSphereRadius(68.f);
	ContactRange->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	ContactRange->SetCollisionResponseToAllChannels(ECR_Ignore);
	ContactRange->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	Sprite = CreateDefaultSubobject<UPaperSpriteComponent>(TEXT("CreatureSprite"));
	Sprite->SetupAttachment(Body);
	Sprite->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Sprite->SetCastShadow(false);
	Sprite->SetRelativeLocation(FVector(0.f, 0.f, -45.f));
	static ConstructorHelpers::FObjectFinder<UPaperSprite> Placeholder(TEXT("/Game/Environment/Prototype2D/Sprites/S_Bush.S_Bush"));
	if (Placeholder.Succeeded()) Sprite->SetSprite(Placeholder.Object);
	Label = CreateDefaultSubobject<UTextRenderComponent>(TEXT("WildLabel"));
	Label->SetupAttachment(Body);
	Label->SetRelativeLocation(FVector(0.f, 0.f, 85.f));
	Label->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	Label->SetText(FText::FromString(TEXT("Wild · E")));
	Label->SetHorizontalAlignment(EHTA_Center);
	Label->SetWorldSize(24.f);
	Label->SetTextRenderColor(FColor(235, 228, 187));
	Label->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Profile = TSoftObjectPtr<UPokeMonsterEncounterProfile>(FSoftObjectPath(TEXT("/Game/Data/Encounters/DA_DevWild.DA_DevWild")));
	Tags.Add(TEXT("VisibleWildEncounter"));
}

void APokeMonsterVisibleWildCreatureActor::BeginPlay()
{
	Super::BeginPlay();
	ContactRange->OnComponentBeginOverlap.AddDynamic(this, &APokeMonsterVisibleWildCreatureActor::OnContact);
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterEncounterSubsystem* Encounters = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounters->OnEncounterEnded.AddUniqueDynamic(this, &APokeMonsterVisibleWildCreatureActor::OnEncounterFinished);
			Encounters->OnPersistentStateRestored.AddUniqueDynamic(this, &APokeMonsterVisibleWildCreatureActor::RefreshPersistentState);
			RefreshPersistentState();
		}
}

void APokeMonsterVisibleWildCreatureActor::RefreshPersistentState()
{
	const UGameInstance* Instance = GetGameInstance();
	const auto* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	bDeactivated = bDeactivateAfterVictory && Encounters && Encounters->IsEncounterCompleted(EncounterId);
	SetActorHiddenInGame(bDeactivated);
	SetActorEnableCollision(!bDeactivated);
}

bool APokeMonsterVisibleWildCreatureActor::CanInteract_Implementation(APawn* Interactor) const
{
	const auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	const UGameInstance* Instance = Player ? Player->GetGameInstance() : nullptr;
	const auto* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	return !bDeactivated && Player && Encounters && !Encounters->IsEncounterActive()
		&& !Player->IsOverworldInputLocked() && !Profile.IsNull();
}

void APokeMonsterVisibleWildCreatureActor::Interact_Implementation(APawn* Interactor)
{
	TryStart(Cast<APokeMonsterPlayerCharacter>(Interactor));
}

void APokeMonsterVisibleWildCreatureActor::OnContact(UPrimitiveComponent*, AActor* OtherActor,
	UPrimitiveComponent*, int32, bool, const FHitResult&)
{
	TryStart(Cast<APokeMonsterPlayerCharacter>(OtherActor));
}

bool APokeMonsterVisibleWildCreatureActor::TryStart(APokeMonsterPlayerCharacter* Player)
{
	if (!Player || !CanInteract_Implementation(Player)) return false;
	UPokeMonsterEncounterSubsystem* Encounters = Player->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	UPokeMonsterEncounterProfile* LoadedProfile = Profile.LoadSynchronous();
	return LoadedProfile && Encounters->EnsureDevPlayerParty()
		&& Encounters->StartWildEncounter(LoadedProfile, Context, EPokeMonsterEncounterSource::VisibleCreature,
			Player, this, Seed, EncounterId);
}

void APokeMonsterVisibleWildCreatureActor::OnEncounterFinished(const FPokeMonsterEncounterEndData& Result)
{
	if (Result.SourceActor != this || !bDeactivateAfterVictory
		|| (Result.Outcome != EPokeMonsterEncounterOutcome::Victory
			&& Result.Outcome != EPokeMonsterEncounterOutcome::Captured)) return;
	bDeactivated = true;
	SetActorHiddenInGame(true);
	SetActorEnableCollision(false);
}
