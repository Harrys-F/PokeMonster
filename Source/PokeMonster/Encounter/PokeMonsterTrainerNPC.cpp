#include "PokeMonsterTrainerNPC.h"

#include "PokeMonsterTrainerProfile.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "PaperSpriteComponent.h"
#include "TimerManager.h"

APokeMonsterTrainerNPC::APokeMonsterTrainerNPC()
{
	PrimaryActorTick.bCanEverTick = false;
	Body = CreateDefaultSubobject<UCapsuleComponent>(TEXT("Body"));
	SetRootComponent(Body);
	Body->InitCapsuleSize(38.f, 58.f);
	Body->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	Body->SetCollisionResponseToAllChannels(ECR_Ignore);
	Body->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
	Body->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	Sprite = CreateDefaultSubobject<UPaperSpriteComponent>(TEXT("TrainerSprite"));
	Sprite->SetupAttachment(Body);
	Sprite->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Sprite->SetCastShadow(false);
	Sprite->SetRelativeLocation(FVector(0.f, 0.f, -45.f));
	NameLabel = CreateDefaultSubobject<UTextRenderComponent>(TEXT("TrainerLabel"));
	NameLabel->SetupAttachment(Body);
	NameLabel->SetRelativeLocation(FVector(0.f, 0.f, 110.f));
	NameLabel->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	NameLabel->SetText(FText::FromString(TEXT("Trainer · E")));
	NameLabel->SetHorizontalAlignment(EHTA_Center);
	NameLabel->SetWorldSize(25.f);
	NameLabel->SetTextRenderColor(FColor(234, 221, 182));
	NameLabel->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	DialogueLabel = CreateDefaultSubobject<UTextRenderComponent>(TEXT("DialoguePlaceholder"));
	DialogueLabel->SetupAttachment(Body);
	DialogueLabel->SetRelativeLocation(FVector(0.f, 0.f, 155.f));
	DialogueLabel->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	DialogueLabel->SetHorizontalAlignment(EHTA_Center);
	DialogueLabel->SetWorldSize(25.f);
	DialogueLabel->SetTextRenderColor(FColor(251, 239, 205));
	DialogueLabel->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	DialogueLabel->SetVisibility(false);
	Profile = TSoftObjectPtr<UPokeMonsterTrainerProfile>(FSoftObjectPath(TEXT("/Game/Data/Trainers/DA_DevTrainer.DA_DevTrainer")));
	Tags.Add(TEXT("TrainerEncounterTest"));
}

void APokeMonsterTrainerNPC::BeginPlay()
{
	Super::BeginPlay();
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterEncounterSubsystem* Encounters = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounters->OnEncounterEnded.AddUniqueDynamic(this, &APokeMonsterTrainerNPC::OnEncounterFinished);
			Encounters->OnPersistentStateRestored.AddUniqueDynamic(this, &APokeMonsterTrainerNPC::RefreshPersistentState);
			RefreshPersistentState();
		}
}

void APokeMonsterTrainerNPC::RefreshPersistentState()
{
	const UGameInstance* Instance = GetGameInstance();
	const auto* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* Loaded = Profile.LoadSynchronous();
	NameLabel->SetText(FText::FromString(Encounters && Loaded && Encounters->IsTrainerDefeated(Loaded->InternalId)
		? TEXT("Besiegt · E") : TEXT("Trainer · E")));
}

void APokeMonsterTrainerNPC::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	GetWorldTimerManager().ClearTimer(DialogueTimer);
	if (APokeMonsterPlayerCharacter* Player = PendingPlayer.Get()) Player->SetOverworldInputLocked(false);
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterEncounterSubsystem* Encounters = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
			Encounters->OnEncounterEnded.RemoveDynamic(this, &APokeMonsterTrainerNPC::OnEncounterFinished);
	Super::EndPlay(EndPlayReason);
}

bool APokeMonsterTrainerNPC::CanInteract_Implementation(APawn* Interactor) const
{
	const auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	const UGameInstance* Instance = Player ? Player->GetGameInstance() : nullptr;
	const auto* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	return !bBattlePending && Player && Encounters && !Encounters->IsEncounterActive()
		&& !Player->IsOverworldInputLocked() && !Profile.IsNull();
}

void APokeMonsterTrainerNPC::Interact_Implementation(APawn* Interactor)
{
	auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	if (!CanInteract_Implementation(Player)) return;
	UPokeMonsterTrainerProfile* Loaded = Profile.LoadSynchronous();
	auto* Encounters = Player->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	if (!IsValid(Loaded) || !Encounters) return;
	GetWorldTimerManager().ClearTimer(DialogueTimer);
	if (Encounters->IsTrainerDefeated(Loaded->InternalId))
	{
		ShowDialogue(Loaded->AfterPlayerVictory.IsEmpty()
			? FText::FromString(TEXT("Ein guter Kampf. Ich bin schon besiegt.")) : Loaded->AfterPlayerVictory);
		return;
	}
	TArray<FPokeMonsterCreatureInstance> Team;
	if (!Loaded->BuildTeam(Team)) return;
	ShowDialogue(Loaded->BeforeBattle.IsEmpty()
		? FText::FromString(TEXT("Zeig mir, was dein Team kann!")) : Loaded->BeforeBattle);
	bBattlePending = true;
	PendingPlayer = Player;
	Player->SetOverworldInputLocked(true);
	GetWorldTimerManager().SetTimer(DialogueTimer, this, &APokeMonsterTrainerNPC::StartPendingBattle,
		FMath::Max(0.1f, DialogueSeconds), false);
}

void APokeMonsterTrainerNPC::ShowDialogue(const FText& Text)
{
	DialogueLabel->SetText(Text);
	DialogueLabel->SetVisibility(true);
}

void APokeMonsterTrainerNPC::StartPendingBattle()
{
	bBattlePending = false;
	APokeMonsterPlayerCharacter* Player = PendingPlayer.Get();
	PendingPlayer.Reset();
	if (!IsValid(Player)) return;
	Player->SetOverworldInputLocked(false);
	UPokeMonsterTrainerProfile* Loaded = Profile.LoadSynchronous();
	auto* Encounters = Player->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	if (!IsValid(Loaded) || !Encounters || !Encounters->StartTrainerEncounter(Loaded, Player, this, BattleSeed))
		ShowDialogue(FText::FromString(TEXT("Der Kampf kann gerade nicht starten.")));
	else DialogueLabel->SetVisibility(false);
}

void APokeMonsterTrainerNPC::OnEncounterFinished(const FPokeMonsterEncounterEndData& Result)
{
	if (Result.SourceActor != this || Result.Kind != EPokeMonsterEncounterKind::Trainer) return;
	const UPokeMonsterTrainerProfile* Loaded = Profile.LoadSynchronous();
	if (Result.Outcome == EPokeMonsterEncounterOutcome::Victory)
	{
		NameLabel->SetText(FText::FromString(TEXT("Besiegt · E")));
		ShowDialogue(Loaded && !Loaded->AfterPlayerVictory.IsEmpty()
			? Loaded->AfterPlayerVictory : FText::FromString(TEXT("Ein guter Kampf!")));
	}
	else if (Result.Outcome == EPokeMonsterEncounterOutcome::Defeat)
		ShowDialogue(Loaded && !Loaded->AfterPlayerDefeat.IsEmpty()
			? Loaded->AfterPlayerDefeat : FText::FromString(TEXT("Fordere mich erneut heraus.")));
}
