#include "PokeMonsterRestPoint.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Dialogue/PokeMonsterDialogueData.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "Materials/MaterialInterface.h"
#include "PaperSpriteComponent.h"
#include "UObject/ConstructorHelpers.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterRestPoint, Log, All);

namespace
{
	const FName RestActionId(TEXT("RestorePartyAtRestPoint"));
}

APokeMonsterRestPoint::APokeMonsterRestPoint()
{
	PrimaryActorTick.bCanEverTick = false;
	Body = CreateDefaultSubobject<UCapsuleComponent>(TEXT("Body"));
	SetRootComponent(Body);
	Body->InitCapsuleSize(48.f, 62.f);
	Body->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	Body->SetCollisionResponseToAllChannels(ECR_Ignore);
	Body->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
	Body->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);

	Pedestal = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Pedestal"));
	Pedestal->SetupAttachment(Body);
	Pedestal->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Pedestal->SetCastShadow(false);
	Pedestal->SetRelativeLocation(FVector(0.f, 0.f, -44.f));
	Pedestal->SetRelativeScale3D(FVector(0.85f, 0.85f, 0.20f));
	Crystal = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Crystal"));
	Crystal->SetupAttachment(Body);
	Crystal->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Crystal->SetCastShadow(false);
	Crystal->SetRelativeLocation(FVector(0.f, 0.f, 2.f));
	Crystal->SetRelativeRotation(FRotator(0.f, 45.f, 45.f));
	Crystal->SetRelativeScale3D(FVector(0.34f, 0.34f, 0.55f));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMesh(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (CubeMesh.Succeeded())
	{
		Pedestal->SetStaticMesh(CubeMesh.Object);
		Crystal->SetStaticMesh(CubeMesh.Object);
	}
	static ConstructorHelpers::FObjectFinder<UMaterialInterface> StoneMaterial(
		TEXT("/Game/Environment/Prototype/Materials/MI_Slice_Stone.MI_Slice_Stone"));
	if (StoneMaterial.Succeeded()) Pedestal->SetMaterial(0, StoneMaterial.Object);
	static ConstructorHelpers::FObjectFinder<UMaterialInterface> WaterMaterial(
		TEXT("/Game/Environment/Prototype/Materials/MI_Slice_Water.MI_Slice_Water"));
	if (WaterMaterial.Succeeded()) Crystal->SetMaterial(0, WaterMaterial.Object);

	Sprite = CreateDefaultSubobject<UPaperSpriteComponent>(TEXT("RestPointSprite"));
	Sprite->SetupAttachment(Body);
	Sprite->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Sprite->SetCastShadow(false);
	NameLabel = CreateDefaultSubobject<UTextRenderComponent>(TEXT("NameLabel"));
	NameLabel->SetupAttachment(Body);
	NameLabel->SetRelativeLocation(FVector(0.f, 0.f, 118.f));
	NameLabel->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	NameLabel->SetHorizontalAlignment(EHTA_Center);
	NameLabel->SetWorldSize(14.f);
	NameLabel->SetTextRenderColor(FColor(218, 237, 220));
	NameLabel->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	DisplayName = FText::FromString(TEXT("Ruhepunkt"));
	IntroText = FText::FromString(TEXT("Ein stiller Schrein lädt dich zum Ausruhen ein. Weiter: Team vollständig heilen."));
}

void APokeMonsterRestPoint::BeginPlay()
{
	Super::BeginPlay();
	NameLabel->SetText(FText::Format(FText::FromString(TEXT("{0} · E")), DisplayName));
	const bool bHasSprite = Sprite->GetSprite() != nullptr;
	Pedestal->SetVisibility(!bHasSprite);
	Crystal->SetVisibility(!bHasSprite);
	if (UGameInstance* Instance = GetGameInstance())
		if (auto* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->OnCustomAction.AddUniqueDynamic(this, &APokeMonsterRestPoint::HandleDialogueAction);
}

void APokeMonsterRestPoint::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (UGameInstance* Instance = GetGameInstance())
		if (auto* Dialogues = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>())
			Dialogues->OnCustomAction.RemoveDynamic(this, &APokeMonsterRestPoint::HandleDialogueAction);
	Super::EndPlay(EndPlayReason);
}

bool APokeMonsterRestPoint::CanInteract_Implementation(APawn* Interactor) const
{
	const auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	const UGameInstance* Instance = Player ? Player->GetGameInstance() : nullptr;
	const auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* Dialogues = Instance ? Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>() : nullptr;
	return Player && Encounter && Dialogues && !Player->IsOverworldInputLocked()
		&& !Encounter->IsEncounterActive() && !Dialogues->IsDialogueActive();
}

void APokeMonsterRestPoint::Interact_Implementation(APawn* Interactor)
{
	auto* Player = Cast<APokeMonsterPlayerCharacter>(Interactor);
	if (!CanInteract_Implementation(Player)) return;
	const FText Prompt = bSaveAfterRest
		? FText::Format(FText::FromString(TEXT("{0} Anschließend wird der Dev-Spielstand gespeichert.")), IntroText)
		: IntroText;
	if (ShowMessage(Player, Prompt, true)) ActivePlayer = Player;
}

bool APokeMonsterRestPoint::ShowMessage(APokeMonsterPlayerCharacter* Player,
	const FText& Text, const bool bStartRest)
{
	if (!IsValid(Player)) return false;
	UGameInstance* Instance = Player->GetGameInstance();
	if (!Instance) return false;
	auto* Dialogue = Instance->GetSubsystem<UPokeMonsterDialogueSubsystem>();
	auto* Encounter = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	if (!Dialogue || !Encounter) return false;
	auto* Data = NewObject<UPokeMonsterDialogueData>(this);
	FPokeMonsterDialoguePage& Page = Data->Pages.AddDefaulted_GetRef();
	Page.SpeakerName = DisplayName;
	Page.Text = Text;
	if (bStartRest)
	{
		Page.FollowUp = EPokeMonsterDialogueAction::Custom;
		Page.FollowUpId = RestActionId;
	}
	return Dialogue->StartDialogue(Player, this, Data, Encounter);
}

FPokeMonsterRestResult APokeMonsterRestPoint::PerformRest(
	UPokeMonsterEncounterSubsystem* Encounter, const bool bSaveAfterRest,
	TFunctionRef<bool()> AttemptSave)
{
	FPokeMonsterRestResult Result;
	if (!IsValid(Encounter) || Encounter->IsEncounterActive()) return Result;
	Result.TeamCount = Encounter->GetPlayerParty().Num();
	if (Result.TeamCount == 0)
	{
		Result.Outcome = EPokeMonsterRestOutcome::NoTeam;
		return Result;
	}
	if (!Encounter->RestorePlayerPartyAtRestPoint())
	{
		Result.Outcome = EPokeMonsterRestOutcome::RestoreFailed;
		return Result;
	}
	Result.Outcome = EPokeMonsterRestOutcome::Healed;
	if (bSaveAfterRest)
		Result.Outcome = AttemptSave() ? EPokeMonsterRestOutcome::HealedAndSaved
			: EPokeMonsterRestOutcome::HealedSaveFailed;
	return Result;
}

FText APokeMonsterRestPoint::MessageForOutcome(const EPokeMonsterRestOutcome Outcome)
{
	switch (Outcome)
	{
	case EPokeMonsterRestOutcome::NoTeam:
		return FText::FromString(TEXT("Dein Team ist leer. Es gibt noch niemanden zu heilen."));
	case EPokeMonsterRestOutcome::RestoreFailed:
		return FText::FromString(TEXT("Die Heilung konnte nicht abgeschlossen werden. Dein Team blieb unverändert."));
	case EPokeMonsterRestOutcome::Healed:
		return FText::FromString(TEXT("Dein gesamtes Team wurde geheilt. HP und PP sind wieder vollständig."));
	case EPokeMonsterRestOutcome::HealedAndSaved:
		return FText::FromString(TEXT("Dein Team wurde vollständig geheilt. Der Spielstand wurde gespeichert."));
	case EPokeMonsterRestOutcome::HealedSaveFailed:
		return FText::FromString(TEXT("Dein Team wurde vollständig geheilt, aber das Speichern ist fehlgeschlagen. Die Heilung bleibt erhalten."));
	default:
		return FText::FromString(TEXT("Der Ruhepunkt ist gerade nicht verfügbar."));
	}
}

void APokeMonsterRestPoint::HandleDialogueAction(AActor* Source, const FName ActionId)
{
	if (Source != this || ActionId != RestActionId) return;
	APokeMonsterPlayerCharacter* Player = ActivePlayer.Get();
	ActivePlayer.Reset();
	if (!IsValid(Player)) return;
	UGameInstance* Instance = Player->GetGameInstance();
	auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	auto* Save = Instance ? Instance->GetSubsystem<UPokeMonsterSaveSubsystem>() : nullptr;
	const FPokeMonsterRestResult Result = PerformRest(Encounter, bSaveAfterRest,
		[Save] { return IsValid(Save) && Save->SaveCurrentGame(); });
	if (Result.Outcome == EPokeMonsterRestOutcome::HealedSaveFailed)
		UE_LOG(LogPokeMonsterRestPoint, Error, TEXT("Party healed, but the Dev save failed."));
	if (!ShowMessage(Player, MessageForOutcome(Result.Outcome), false))
		UE_LOG(LogPokeMonsterRestPoint, Warning, TEXT("Could not display rest result: %d"),
			static_cast<int32>(Result.Outcome));
}
