#include "PokeMonsterNPC.h"

#include "PokeMonsterDialogueData.h"
#include "PokeMonsterDialogueSubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Components/CapsuleComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "PaperSpriteComponent.h"

APokeMonsterNPC::APokeMonsterNPC()
{
	PrimaryActorTick.bCanEverTick = false;
	Body = CreateDefaultSubobject<UCapsuleComponent>(TEXT("Body"));
	SetRootComponent(Body);
	Body->InitCapsuleSize(34.f, 56.f);
	Body->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	Body->SetCollisionResponseToAllChannels(ECR_Ignore);
	Body->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
	Body->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	Sprite = CreateDefaultSubobject<UPaperSpriteComponent>(TEXT("NPCSprite"));
	Sprite->SetupAttachment(Body);
	Sprite->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Sprite->SetCastShadow(false);
	Sprite->SetRelativeLocation(FVector(0.f, 0.f, -40.f));
	NameLabel = CreateDefaultSubobject<UTextRenderComponent>(TEXT("NameLabel"));
	NameLabel->SetupAttachment(Body);
	NameLabel->SetRelativeLocation(FVector(0.f, 0.f, 110.f));
	NameLabel->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	NameLabel->SetHorizontalAlignment(EHTA_Center);
	NameLabel->SetWorldSize(12.f);
	NameLabel->SetTextRenderColor(FColor(235, 224, 195));
	NameLabel->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	PlaceholderGlyph = CreateDefaultSubobject<UTextRenderComponent>(TEXT("PlaceholderGlyph"));
	PlaceholderGlyph->SetupAttachment(Body);
	PlaceholderGlyph->SetRelativeLocation(FVector(0.f, 0.f, 20.f));
	PlaceholderGlyph->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	PlaceholderGlyph->SetHorizontalAlignment(EHTA_Center);
	PlaceholderGlyph->SetWorldSize(32.f);
	PlaceholderGlyph->SetText(FText::FromString(TEXT("?")));
	PlaceholderGlyph->SetTextRenderColor(FColor(235, 224, 195));
	PlaceholderGlyph->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	DisplayName = FText::FromString(TEXT("Dorfbewohner"));
}

void APokeMonsterNPC::BeginPlay()
{
	Super::BeginPlay();
	NameLabel->SetText(FText::Format(FText::FromString(TEXT("{0} · E")), DisplayName));
	PlaceholderGlyph->SetVisibility(!Sprite->GetSprite());
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterDialogueSubsystem* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->OnCustomAction.AddUniqueDynamic(this, &APokeMonsterNPC::HandleCustomAction);
}

void APokeMonsterNPC::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterDialogueSubsystem* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->OnCustomAction.RemoveDynamic(this, &APokeMonsterNPC::HandleCustomAction);
	Super::EndPlay(EndPlayReason);
}

bool APokeMonsterNPC::CanInteract_Implementation(APawn* Interactor) const
{
	const auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	const UGameInstance* Instance = Player ? Player->GetGameInstance() : nullptr;
	const auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* Dialogues = Instance ? Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>() : nullptr;
	return Player && Encounter && Dialogues && !Dialogue.IsNull()
		&& !Player->IsOverworldInputLocked() && !Encounter->IsEncounterActive()
		&& !Dialogues->IsDialogueActive();
}

void APokeMonsterNPC::Interact_Implementation(APawn* Interactor)
{
	auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	if (!CanInteract_Implementation(Player)) return;
	auto* Instance = Player->GetGameInstance();
	auto* Data = Dialogue.LoadSynchronous();
	if (!IsValid(Data)) return;
	Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>()->StartDialogue(Player, this, Data,
		Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>());
}

void APokeMonsterNPC::HandleCustomAction(AActor* Source, const FName ActionId)
{
	if (Source == this) OnDialogueFollowUp(ActionId);
}
