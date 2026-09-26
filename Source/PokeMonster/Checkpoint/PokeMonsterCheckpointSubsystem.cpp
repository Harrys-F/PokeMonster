#include "PokeMonsterCheckpointSubsystem.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../UI/PokeMonsterDefeatWidget.h"
#include "Blueprint/UserWidget.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/PackageName.h"
#include "TimerManager.h"
#include "UObject/UObjectGlobals.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterCheckpoint, Log, All);

bool FPokeMonsterCheckpointData::IsValid() const
{
	return !CheckpointId.IsNone() && !MapPackage.IsNone()
		&& FPackageName::IsValidLongPackageName(MapPackage.ToString())
		&& !Location.ContainsNaN() && !Rotation.ContainsNaN();
}

void UPokeMonsterCheckpointSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	PostLoadMapHandle = FCoreUObjectDelegates::PostLoadMapWithWorld.AddUObject(
		this, &UPokeMonsterCheckpointSubsystem::HandlePostLoadMap);
}

void UPokeMonsterCheckpointSubsystem::Deinitialize()
{
	FCoreUObjectDelegates::PostLoadMapWithWorld.Remove(PostLoadMapHandle);
	if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
		World->GetTimerManager().ClearTimer(TransitionTimer);
	ClearOverlay();
	Super::Deinitialize();
}

FName UPokeMonsterCheckpointSubsystem::GetMapPackage(const UWorld* World)
{
	if (!World || !World->GetOutermost()) return NAME_None;
	const FString LongPath = FPackageName::GetLongPackagePath(World->GetOutermost()->GetName());
	const FString ShortName = UGameplayStatics::GetCurrentLevelName(World, true);
	return LongPath.IsEmpty() || ShortName.IsEmpty()
		? NAME_None : FName(*(LongPath / ShortName));
}

bool UPokeMonsterCheckpointSubsystem::ActivateCheckpoint(
	const FName Id, const UWorld* World, const FTransform& SafePlayerTransform)
{
	FPokeMonsterCheckpointData Data;
	Data.CheckpointId = Id;
	Data.MapPackage = GetMapPackage(World);
	Data.Location = SafePlayerTransform.GetLocation();
	Data.Rotation = SafePlayerTransform.Rotator();
	return !bReturning && RestoreCheckpoint(Data);
}

bool UPokeMonsterCheckpointSubsystem::RestoreCheckpoint(const FPokeMonsterCheckpointData& Data)
{
	if (bReturning || (!Data.CheckpointId.IsNone() && !Data.IsValid())
		|| (Data.CheckpointId.IsNone() && (!Data.MapPackage.IsNone()
			|| !Data.Location.IsNearlyZero() || !Data.Rotation.IsNearlyZero()))) return false;
	ActiveCheckpoint = Data;
	return true;
}

bool UPokeMonsterCheckpointSubsystem::ResolveReturnTarget(const FName CurrentMap,
	const FPokeMonsterCheckpointData& Active, const FTransform& Fallback,
	FPokeMonsterCheckpointData& OutTarget)
{
	if (Active.IsValid()) { OutTarget = Active; return true; }
	if (CurrentMap.IsNone() || Fallback.GetLocation().ContainsNaN()
		|| Fallback.Rotator().ContainsNaN()) return false;
	OutTarget = FPokeMonsterCheckpointData();
	OutTarget.CheckpointId = TEXT("Fallback_PlayerStart");
	OutTarget.MapPackage = CurrentMap;
	OutTarget.Location = Fallback.GetLocation();
	OutTarget.Rotation = Fallback.Rotator();
	return OutTarget.IsValid();
}

bool UPokeMonsterCheckpointSubsystem::FindFallback(UWorld* World, FTransform& OutTransform)
{
	if (!World) return false;
	APlayerStart* FirstStart = nullptr;
	for (TActorIterator<APlayerStart> It(World); It; ++It)
	{
		if (!FirstStart) FirstStart = *It;
		if (It->ActorHasTag(TEXT("PokeMonsterSafeFallback")))
		{
			OutTransform = It->GetActorTransform();
			return true;
		}
	}
	if (FirstStart) { OutTransform = FirstStart->GetActorTransform(); return true; }
	if (GetMapPackage(World) == TEXT("/Game/Maps/Dev_TestMap"))
	{
		OutTransform = FTransform(FRotator(0.f, 35.f, 0.f), FVector(-1000.f, -1100.f, 100.f));
		return true;
	}
	return false;
}

bool UPokeMonsterCheckpointSubsystem::RestoreTeamAfterDefeat(UPokeMonsterEncounterSubsystem* Encounter)
{
	return IsValid(Encounter) && Encounter->RestorePlayerPartyAtRestPoint();
}

void UPokeMonsterCheckpointSubsystem::ShowOverlay(APlayerController* Controller, const FText& Message)
{
	if (!IsValid(Controller) || !Controller->IsLocalController()) return;
	if (!DefeatWidget)
	{
		DefeatWidget = CreateWidget<UPokeMonsterDefeatWidget>(Controller, UPokeMonsterDefeatWidget::StaticClass());
		if (DefeatWidget) DefeatWidget->AddToViewport(200);
	}
	if (DefeatWidget) DefeatWidget->SetMessage(Message);
	Controller->SetInputMode(FInputModeUIOnly());
	Controller->bShowMouseCursor = false;
}

void UPokeMonsterCheckpointSubsystem::ClearOverlay()
{
	if (DefeatWidget) DefeatWidget->RemoveFromParent();
	DefeatWidget = nullptr;
}

bool UPokeMonsterCheckpointSubsystem::BeginDefeatRecovery(
	APokeMonsterPlayerCharacter* Player, APlayerController* Controller)
{
	UWorld* World = IsValid(Player) ? Player->GetWorld() : nullptr;
	FTransform Fallback;
	if (bReturning || !World || !IsValid(Controller)
		|| (!ActiveCheckpoint.IsValid() && !FindFallback(World, Fallback))
		|| !ResolveReturnTarget(GetMapPackage(World), ActiveCheckpoint, Fallback, PendingTarget)) return false;
	bReturning = true;
	ReturningPlayer = Player;
	ReturningController = Controller;
	ReturnAttempts = 0;
	Player->SetOverworldInputLocked(true);
	ShowOverlay(Controller, FText::FromString(TEXT("Dein Team ist kampfunfähig …")));
	World->GetTimerManager().SetTimer(TransitionTimer, this,
		&UPokeMonsterCheckpointSubsystem::PerformReturn, 1.0f, false);
	return true;
}

void UPokeMonsterCheckpointSubsystem::PerformReturn()
{
	UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr;
	if (!World || !PendingTarget.IsValid()) { UnlockAfterReturn(); return; }
	if (PendingTarget.MapPackage != GetMapPackage(World))
	{
		ClearOverlay();
		UGameplayStatics::OpenLevel(World, PendingTarget.MapPackage);
		return;
	}
	FinishReturn(World);
}

void UPokeMonsterCheckpointSubsystem::HandlePostLoadMap(UWorld* World)
{
	if (!bReturning || !World || World->GetGameInstance() != GetGameInstance()
		|| GetMapPackage(World) != PendingTarget.MapPackage) return;
	World->GetTimerManager().SetTimer(TransitionTimer, FTimerDelegate::CreateUObject(
		this, &UPokeMonsterCheckpointSubsystem::FinishReturn, World), 0.1f, false);
}

void UPokeMonsterCheckpointSubsystem::FinishReturn(UWorld* World)
{
	if (!bReturning || !World) return;
	APlayerController* Controller = World->GetFirstPlayerController();
	APokeMonsterPlayerCharacter* Player = Controller
		? Cast<APokeMonsterPlayerCharacter>(Controller->GetPawn()) : nullptr;
	if (!Player && ReturningPlayer.IsValid() && ReturningPlayer->GetWorld() == World)
		Player = ReturningPlayer.Get();
	if (!Controller) Controller = ReturningController.Get();
	if (!Player && ReturnAttempts++ < 20)
	{
		World->GetTimerManager().SetTimer(TransitionTimer, FTimerDelegate::CreateUObject(
			this, &UPokeMonsterCheckpointSubsystem::FinishReturn, World), 0.1f, false);
		return;
	}
	if (IsValid(Player))
	{
		Player->SetOverworldInputLocked(true);
		if (!Player->TeleportTo(PendingTarget.Location, PendingTarget.Rotation, false, false))
		{
			FTransform Fallback;
			if (FindFallback(World, Fallback))
				Player->TeleportTo(Fallback.GetLocation(), Fallback.Rotator(), false, true);
			UE_LOG(LogPokeMonsterCheckpoint, Warning, TEXT("Checkpoint location blocked; used map fallback."));
		}
		if (IsValid(Controller)) Controller->SetControlRotation(PendingTarget.Rotation);
	}
	const bool bHealed = RestoreTeamAfterDefeat(GetGameInstance()
		? GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr);
	UE_LOG(LogPokeMonsterCheckpoint, Display,
		TEXT("Defeat return to '%s' in '%s': team restore %s."),
		*PendingTarget.CheckpointId.ToString(), *PendingTarget.MapPackage.ToString(),
		bHealed ? TEXT("succeeded") : TEXT("failed"));
	ShowOverlay(Controller, FText::FromString(bHealed
		? TEXT("Du bist am Ruhepunkt erwacht. Dein Team ist wieder fit.")
		: TEXT("Du bist zurückgekehrt. Die Teamheilung ist fehlgeschlagen.")));
	World->GetTimerManager().SetTimer(TransitionTimer, this,
		&UPokeMonsterCheckpointSubsystem::UnlockAfterReturn, 1.0f, false);
}

void UPokeMonsterCheckpointSubsystem::UnlockAfterReturn()
{
	ClearOverlay();
	UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr;
	APlayerController* Controller = World ? World->GetFirstPlayerController() : ReturningController.Get();
	APokeMonsterPlayerCharacter* Player = Controller
		? Cast<APokeMonsterPlayerCharacter>(Controller->GetPawn()) : ReturningPlayer.Get();
	if (IsValid(Player)) Player->SetOverworldInputLocked(false);
	if (IsValid(Controller))
	{
		Controller->SetInputMode(FInputModeGameAndUI());
		Controller->bShowMouseCursor = true;
	}
	ReturningPlayer.Reset();
	ReturningController.Reset();
	ReturnAttempts = 0;
	PendingTarget = FPokeMonsterCheckpointData();
	bReturning = false;
}
