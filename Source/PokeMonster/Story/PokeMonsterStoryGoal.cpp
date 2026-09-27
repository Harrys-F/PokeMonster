#include "PokeMonsterStoryGoal.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Dialogue/PokeMonsterDialogueData.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Components/CapsuleComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "PaperSprite.h"
#include "PaperSpriteComponent.h"
#include "UObject/ConstructorHelpers.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterStoryGoal, Log, All);

APokeMonsterStoryGoal::APokeMonsterStoryGoal()
{
	PrimaryActorTick.bCanEverTick = false;
	Body = CreateDefaultSubobject<UCapsuleComponent>(TEXT("Body"));
	SetRootComponent(Body);
	Body->InitCapsuleSize(45.f, 58.f);
	Body->SetCollisionResponseToAllChannels(ECR_Ignore);
	Body->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
	Body->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	Sprite = CreateDefaultSubobject<UPaperSpriteComponent>(TEXT("GoalSprite"));
	Sprite->SetupAttachment(Body);
	Sprite->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Sprite->SetCastShadow(false);
	Sprite->SetRelativeLocation(FVector(0.f, 0.f, -45.f));
	Sprite->SetRelativeScale3D(FVector(1.35f));
	static ConstructorHelpers::FObjectFinder<UPaperSprite> Rock(TEXT("/Game/Environment/Prototype2D/Sprites/S_Rock.S_Rock"));
	if (Rock.Succeeded()) Sprite->SetSprite(Rock.Object);
	Label = CreateDefaultSubobject<UTextRenderComponent>(TEXT("GoalLabel"));
	Label->SetupAttachment(Body);
	Label->SetRelativeLocation(FVector(0.f, 0.f, 115.f));
	Label->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	Label->SetHorizontalAlignment(EHTA_Center);
	Label->SetWorldSize(18.f);
	Label->SetTextRenderColor(FColor(231, 224, 193));
	Label->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	CompletionLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("CompletionLight"));
	CompletionLight->SetupAttachment(Body);
	CompletionLight->SetRelativeLocation(FVector(0.f, 0.f, 45.f));
	CompletionLight->SetLightColor(FLinearColor(0.38f, 0.76f, 0.62f));
	CompletionLight->SetIntensity(280.f);
	CompletionLight->SetAttenuationRadius(210.f);
	CompletionLight->SetCastShadows(false);
	CompletionLight->SetVisibility(false);
	DisplayName = FText::FromString(TEXT("Archivstein"));
	LockedText = FText::FromString(TEXT("Liora bewacht den Weg. Bestehe zuerst ihre Prüfung."));
	ReadyText = FText::FromString(TEXT("Die alten Zeichen erwachen. Du hast den Archivstein gefunden – Abschnitt abgeschlossen!"));
	CompletedText = FText::FromString(TEXT("Die Zeichen am Archivstein leuchten noch immer. Dein Weg ist hier vorerst zu Ende."));
}

EPokeMonsterStoryGoalState APokeMonsterStoryGoal::EvaluateState(
	const UPokeMonsterEncounterSubsystem* Encounter, FName TrainerId, FName GoalFlag)
{
	if (!IsValid(Encounter) || TrainerId.IsNone() || GoalFlag.IsNone()) return EPokeMonsterStoryGoalState::Locked;
	if (Encounter->IsEncounterCompleted(GoalFlag)) return EPokeMonsterStoryGoalState::Completed;
	return Encounter->IsTrainerDefeated(TrainerId)
		? EPokeMonsterStoryGoalState::Ready : EPokeMonsterStoryGoalState::Locked;
}

bool APokeMonsterStoryGoal::CompleteGoal(UPokeMonsterEncounterSubsystem* Encounter,
	FName TrainerId, FName GoalFlag)
{
	if (EvaluateState(Encounter, TrainerId, GoalFlag) != EPokeMonsterStoryGoalState::Ready) return false;
	Encounter->MarkEncounterCompleted(GoalFlag);
	return Encounter->IsEncounterCompleted(GoalFlag);
}

void APokeMonsterStoryGoal::BeginPlay()
{
	Super::BeginPlay();
	if (UGameInstance* Instance = GetGameInstance())
	{
		if (auto* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->OnCustomAction.AddUniqueDynamic(this, &APokeMonsterStoryGoal::HandleDialogueAction);
		if (auto* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounter->OnPersistentStateRestored.AddUniqueDynamic(this, &APokeMonsterStoryGoal::RefreshVisual);
			Encounter->OnEncounterEnded.AddUniqueDynamic(this, &APokeMonsterStoryGoal::OnEncounterFinished);
		}
	}
	RefreshVisual();
}

void APokeMonsterStoryGoal::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (UGameInstance* Instance = GetGameInstance())
	{
		if (auto* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->OnCustomAction.RemoveDynamic(this, &APokeMonsterStoryGoal::HandleDialogueAction);
		if (auto* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounter->OnPersistentStateRestored.RemoveDynamic(this, &APokeMonsterStoryGoal::RefreshVisual);
			Encounter->OnEncounterEnded.RemoveDynamic(this, &APokeMonsterStoryGoal::OnEncounterFinished);
		}
	}
	Super::EndPlay(EndPlayReason);
}

bool APokeMonsterStoryGoal::CanInteract_Implementation(APawn* Interactor) const
{
	const auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	const UGameInstance* Instance = Player ? Player->GetGameInstance() : nullptr;
	const auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* Dialogues = Instance ? Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>() : nullptr;
	return Player && Encounter && Dialogues && !Player->IsOverworldInputLocked()
		&& !Encounter->IsEncounterActive() && !Dialogues->IsDialogueActive();
}

void APokeMonsterStoryGoal::Interact_Implementation(APawn* Interactor)
{
	auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	if (!CanInteract_Implementation(Player)) return;
	UGameInstance* Instance = Player->GetGameInstance();
	auto* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	auto* Dialogue = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>();
	const auto State = EvaluateState(Encounter, RequiredTrainerId, CompletionFlag);
	auto* Data = NewObject<UPokeMonsterDialogueData>(this);
	auto& Page = Data->Pages.AddDefaulted_GetRef();
	Page.SpeakerName = DisplayName;
	Page.Text = State == EPokeMonsterStoryGoalState::Completed ? CompletedText
		: State == EPokeMonsterStoryGoalState::Ready ? ReadyText : LockedText;
	if (State == EPokeMonsterStoryGoalState::Ready)
	{
		Page.FollowUp = EPokeMonsterDialogueAction::Custom;
		Page.FollowUpId = CompletionFlag;
	}
	Dialogue->StartDialogue(Player, this, Data, Encounter);
}

void APokeMonsterStoryGoal::HandleDialogueAction(AActor* Source, FName ActionId)
{
	if (Source != this || ActionId != CompletionFlag) return;
	auto* Encounter = GetGameInstance()
		? GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	if (CompleteGoal(Encounter, RequiredTrainerId, CompletionFlag))
	{
		RefreshVisual();
		UE_LOG(LogPokeMonsterStoryGoal, Display, TEXT("Story goal '%s' completed."), *CompletionFlag.ToString());
	}
}

void APokeMonsterStoryGoal::RefreshVisual()
{
	const UGameInstance* Instance = GetGameInstance();
	const auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const bool bDone = EvaluateState(Encounter, RequiredTrainerId, CompletionFlag)
		== EPokeMonsterStoryGoalState::Completed;
	Label->SetText(FText::Format(FText::FromString(bDone ? TEXT("{0} · Erforscht") : TEXT("{0} · E")), DisplayName));
	Sprite->SetSpriteColor(bDone ? FLinearColor(0.80f, 1.f, 0.87f) : FLinearColor(0.90f, 0.92f, 0.86f));
	CompletionLight->SetVisibility(bDone);
}

void APokeMonsterStoryGoal::OnEncounterFinished(const FPokeMonsterEncounterEndData& Result)
{
	RefreshVisual();
}
