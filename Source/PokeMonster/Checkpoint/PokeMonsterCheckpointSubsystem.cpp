#include "PokeMonsterCheckpointSubsystem.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../UI/PokeMonsterDefeatWidget.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "Blueprint/UserWidget.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/CharacterMovementComponent.h"
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
 if (GEngine) TravelFailureHandle = GEngine->OnTravelFailure().AddUObject(this, &UPokeMonsterCheckpointSubsystem::HandleTravelFailure);
}

void UPokeMonsterCheckpointSubsystem::Deinitialize()
{
	FCoreUObjectDelegates::PostLoadMapWithWorld.Remove(PostLoadMapHandle);
 if (GEngine) GEngine->OnTravelFailure().Remove(TravelFailureHandle);
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
 const bool bUsableCheckpoint = ActiveCheckpoint.IsValid() && FPackageName::DoesPackageExist(ActiveCheckpoint.MapPackage.ToString());
 if (bReturning || PendingTarget.IsValid() || !World || !IsValid(Controller)
		|| (!bUsableCheckpoint && !FindFallback(World, Fallback))
		|| !ResolveReturnTarget(GetMapPackage(World), bUsableCheckpoint ? ActiveCheckpoint : FPokeMonsterCheckpointData{}, Fallback, PendingTarget)) return false;
	bReturning = true;
	bLastRecoverySaved = false;
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

void UPokeMonsterCheckpointSubsystem::HandleTravelFailure(UWorld* World, ETravelFailure::Type, const FString& Error)
{
 if (!bReturning || (World && World->GetGameInstance() != GetGameInstance())) return;
 UWorld* Current = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr;
 FTransform Fallback;
 UE_LOG(LogPokeMonsterCheckpoint, Display, TEXT("Recovery travel failed; checking current-world fallback: %s"), *Error);
 if (Current && FindFallback(Current, Fallback)
  && ResolveReturnTarget(GetMapPackage(Current), {}, Fallback, PendingTarget)) FinishReturn(Current);
 else UnlockAfterReturn();
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
	bool bPlaced = false;
	FPokeMonsterCheckpointData ActualTarget = PendingTarget;
	if (IsValid(Player) && GetMapPackage(World) == PendingTarget.MapPackage)
	{
		Player->SetOverworldInputLocked(true);
		bPlaced = Player->TeleportTo(PendingTarget.Location, PendingTarget.Rotation, false, false);
		if (!bPlaced)
		{
			FTransform Fallback;
			if (FindFallback(World, Fallback))
			{
				bPlaced = Player->TeleportTo(Fallback.GetLocation(), Fallback.Rotator(), false, false);
				if (bPlaced) ResolveReturnTarget(GetMapPackage(World), {}, Fallback, ActualTarget);
			}
			UE_LOG(LogPokeMonsterCheckpoint, Warning, TEXT("Checkpoint blocked; checked fallback placement: %s."),
				bPlaced ? TEXT("succeeded") : TEXT("failed"));
		}
		if (bPlaced)
  {
   if (IsValid(Controller)) Controller->SetControlRotation(ActualTarget.Rotation);
   UPokeMonsterSaveSubsystem::SynchronizeRestoredPlayer(Player);
   Player->RestoreSavedFacing(ActualTarget.Rotation.Vector());
  }
	}
	const bool bHealed = bPlaced && RestoreTeamAfterDefeat(GetGameInstance()
		? GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr);
 if (bPlaced && bHealed)
 {
  ReturnAttempts=0;
  // A newly possessed pawn still reports Falling for its first movement tick.
  // Keep recovery/input locked until it has actually settled, then snapshot once.
  World->GetTimerManager().SetTimer(TransitionTimer,this,
   &UPokeMonsterCheckpointSubsystem::SaveSettledReturn,.1f,false);
  return;
 }

	UE_LOG(LogPokeMonsterCheckpoint, Display,
		TEXT("Defeat return '%s': placed=%d healed=%d autosaved=%d."),
		*ActualTarget.CheckpointId.ToString(), bPlaced, bHealed, bLastRecoverySaved);
	ShowOverlay(Controller, FText::FromString(!bPlaced
		? TEXT("Rückkehr fehlgeschlagen. Dein bisheriger Spielstand wurde nicht verändert.")
		: !bHealed ? TEXT("Teamheilung fehlgeschlagen. Es wurde nicht gespeichert.")
		: bLastRecoverySaved ? TEXT("Dein Team ist wieder fit. Rettungsstand gespeichert; manueller Spielstand bleibt erhalten.")
		: TEXT("Dein Team ist wieder fit. Speichern fehlgeschlagen – bitte erneut speichern.")));
	World->GetTimerManager().SetTimer(TransitionTimer, this,
		&UPokeMonsterCheckpointSubsystem::UnlockAfterReturn, 1.0f, false);
}

void UPokeMonsterCheckpointSubsystem::SaveSettledReturn()
{
 UWorld* World=GetWorld();auto* PC=World?World->GetFirstPlayerController():nullptr;
 auto* Player=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;
 if(!bReturning || !World)return;
 if((!Player || Player->GetCharacterMovement()->IsFalling()) && ++ReturnAttempts<20)
 {
  World->GetTimerManager().SetTimer(TransitionTimer,this,&UPokeMonsterCheckpointSubsystem::SaveSettledReturn,.1f,false);
  return;
 }
 bReturning=false;
 auto* Saves=GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>();
 bLastRecoverySaved=Player && !Player->GetCharacterMovement()->IsFalling() && Saves && Saves->SaveRecoveryGame();
 UE_LOG(LogPokeMonsterCheckpoint,Display,TEXT("Settled defeat return: autosaved=%d."),bLastRecoverySaved);
 ShowOverlay(PC,FText::FromString(bLastRecoverySaved
  ? TEXT("Dein Team ist wieder fit. Automatischer Stand gespeichert; manueller Spielstand bleibt erhalten.")
  : TEXT("Dein Team ist wieder fit. Automatisches Speichern fehlgeschlagen – bitte erneut speichern.")));
 World->GetTimerManager().SetTimer(TransitionTimer,this,&UPokeMonsterCheckpointSubsystem::UnlockAfterReturn,1.f,false);
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
