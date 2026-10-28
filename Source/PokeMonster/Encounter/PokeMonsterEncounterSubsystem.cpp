#include "PokeMonsterEncounterSubsystem.h"
#include "../Game/PokeMonsterGameMode.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "PokeMonsterClassicBattleScene.h"
#include "PokeMonsterEncounterProfile.h"
#include "PokeMonsterVisibleWildCreatureActor.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "PokeMonsterTrainerProfile.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "Blueprint/UserWidget.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Camera/PlayerCameraManager.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/PlayerController.h"
#include "TimerManager.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterEncounter, Log, All);

bool UPokeMonsterEncounterSubsystem::BuildTestTeams(TArray<FPokeMonsterCreatureInstance>& Player,
	TArray<FPokeMonsterCreatureInstance>& Opponent)
{
	auto* Water = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Grass = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Normal = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	auto* Fire = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestFireSpecial.DA_TestFireSpecial"));
	auto* Status = LoadObject<UPokeMonsterMoveData>(nullptr, TEXT("/Game/Data/Moves/DA_TestStatus.DA_TestStatus"));
	if (!Water || !Grass || !Normal || !Fire || !Status) return false;
	for (const int32 Level : {20, 18})
	{
		auto A = FPokeMonsterCreatureInstance::CreateFromSpecies(Water, Level);
		auto B = FPokeMonsterCreatureInstance::CreateFromSpecies(Grass, Level);
		UPokeMonsterMoveData* AMoves[] = {Normal, Fire, Status, Normal};
		UPokeMonsterMoveData* BMoves[] = {Normal, Status, Fire, Normal};
		for (int32 Slot = 0; Slot < 4; ++Slot)
			if (!A.AssignMove(Slot, AMoves[Slot]) || !B.AssignMove(Slot, BMoves[Slot])) return false;
		Player.Add(MoveTemp(A));
		Opponent.Add(MoveTemp(B));
	}
	return true;
}

bool UPokeMonsterEncounterSubsystem::StartTestEncounter(APokeMonsterPlayerCharacter* Player, AActor* SourceActor)
{
	TArray<FPokeMonsterCreatureInstance> InitialParty, Opponents;
	if (!BuildTestTeams(InitialParty, Opponents))
	{
		UE_LOG(LogPokeMonsterEncounter, Error, TEXT("Test encounter assets are missing or invalid."));
		return false;
	}
	FPokeMonsterEncounterStartData Start;
	Start.EncounterId = TEXT("Dev_TestEncounter");
	Start.Kind = EPokeMonsterEncounterKind::Test;
	Start.PlayerTeam = PlayerParty.IsEmpty() ? MoveTemp(InitialParty) : PlayerParty;
	Start.OpponentTeam = MoveTemp(Opponents);
	Start.SourceActor = SourceActor;
	return StartEncounter(Start, Player);
}

bool UPokeMonsterEncounterSubsystem::BuildVisualV2TestParty(TArray<FPokeMonsterCreatureInstance>& OutParty)
{
 auto* Fire=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 if(!Fire)return false;
 TArray<FPokeMonsterCreatureInstance> NewParty;auto Starter=FPokeMonsterCreatureInstance::CreateFromSpecies(Fire,15);
 if(!Starter.AssignSpeciesMoves())return false;NewParty.Add(MoveTemp(Starter));
 for(const TCHAR* Path:{TEXT("/Game/Data/Encounters/DA_Garados_Wild.DA_Garados_Wild"),TEXT("/Game/Data/Encounters/DA_Pikachu_Wild.DA_Pikachu_Wild")})
 {
  const auto* Profile=LoadObject<UPokeMonsterEncounterProfile>(nullptr,Path);FPokeMonsterCreatureInstance Member;
  FPokeMonsterEncounterContext Context;Context.Time=EPokeMonsterEncounterTime::Any;FRandomStream Random(3817);
  if(!Profile||!Profile->Roll(Context,Random,Member))return false;NewParty.Add(MoveTemp(Member));
 }
 for(const auto& Member:NewParty)if(!Member.IsValid())return false;
 OutParty=MoveTemp(NewParty);return true;
}

bool UPokeMonsterEncounterSubsystem::EnsureDevPlayerParty()
{
	if (!PlayerParty.IsEmpty()) return true;
#if !UE_BUILD_SHIPPING
 if(GetWorld()&&UWorld::RemovePIEPrefix(GetWorld()->GetName())==TEXT("Dev_TestMap_VisualV2"))return BuildVisualV2TestParty(PlayerParty);
#endif
	TArray<FPokeMonsterCreatureInstance> InitialParty, UnusedOpponents;
	if (!BuildTestTeams(InitialParty, UnusedOpponents)) return false;
	PlayerParty = MoveTemp(InitialParty);
	return true;
}

bool UPokeMonsterEncounterSubsystem::UseHealingItemOnPartyMember(const UPokeMonsterItemData* Item, int32 TeamIndex)
{
	if (bActive || !PlayerParty.IsValidIndex(TeamIndex) || !GetGameInstance()) return false;
	UPokeMonsterInventorySubsystem* Inventory = GetGameInstance()->GetSubsystem<UPokeMonsterInventorySubsystem>();
	return Inventory && Inventory->UseHealingItem(Item, PlayerParty[TeamIndex]);
}

bool UPokeMonsterEncounterSubsystem::RestorePlayerPartyAtRestPoint()
{
	if (bActive || PlayerParty.IsEmpty()) return false;
	TArray<FPokeMonsterCreatureInstance> RestoredParty = PlayerParty;
	for (FPokeMonsterCreatureInstance& Creature : RestoredParty)
		if (!Creature.RestoreFully()) return false;
	PlayerParty = MoveTemp(RestoredParty);
	return true;
}

bool UPokeMonsterEncounterSubsystem::ReorderParty(const FGuid SourceInstanceId, const int32 TargetIndex)
{
	if (bActive || !SourceInstanceId.IsValid() || TargetIndex < 0 || TargetIndex >= 6) return false;
	const auto* Checkpoint = GetGameInstance() ? GetGameInstance()->GetSubsystem<UPokeMonsterCheckpointSubsystem>() : nullptr;
	if (Checkpoint && Checkpoint->IsReturningFromDefeat()) return false;
	TSet<FGuid> Seen;
	for (const auto& Member : PlayerParty)
	{
		if (!Member.IsValid() || Seen.Contains(Member.InstanceId)) return false;
		Seen.Add(Member.InstanceId);
	}
	const int32 Source = PlayerParty.IndexOfByPredicate([&](const auto& Member) { return Member.InstanceId == SourceInstanceId; });
	if (Source == INDEX_NONE) return false;
	if (PlayerParty.IsValidIndex(TargetIndex)) PlayerParty.Swap(Source, TargetIndex);
	else
	{
		FPokeMonsterCreatureInstance Member = PlayerParty[Source];
		PlayerParty.RemoveAt(Source);
		PlayerParty.Add(MoveTemp(Member));
	}
	return true;
}

bool UPokeMonsterEncounterSubsystem::PrepareWildEncounter(const UPokeMonsterEncounterProfile* Profile,
	const FPokeMonsterEncounterContext& Context, EPokeMonsterEncounterSource Source,
	AActor* SourceActor, int32 Seed, FName EncounterId, FPokeMonsterEncounterStartData& OutStart)
{
	OutStart = FPokeMonsterEncounterStartData();
	if (!IsValid(Profile)) return false;
	FRandomStream Random(Seed);
	FPokeMonsterCreatureInstance WildCreature;
	if (!Profile->Roll(Context, Random, WildCreature)) return false;
	OutStart.PresentationMode=Profile->PresentationMode;
 OutStart.BattleEnvironment=Profile->BattleEnvironment;
	OutStart.EncounterId = EncounterId;
	OutStart.Kind = EPokeMonsterEncounterKind::Wild;
 OutStart.bAllowFlee=Profile->bAllowFlee&&Source!=EPokeMonsterEncounterSource::Scripted;
	OutStart.Source = Source;
 OutStart.BattleRegion=Context.RegionId;
	OutStart.OpponentTeam.Add(MoveTemp(WildCreature));
	OutStart.RandomSeed = Seed;
	OutStart.SourceActor = SourceActor;
	return true;
}

bool UPokeMonsterEncounterSubsystem::StartWildEncounter(const UPokeMonsterEncounterProfile* Profile,
	const FPokeMonsterEncounterContext& Context, EPokeMonsterEncounterSource Source,
	APokeMonsterPlayerCharacter* Player, AActor* SourceActor, int32 Seed, FName EncounterId)
{
	FPokeMonsterEncounterStartData Start;
	if (!PrepareWildEncounter(Profile, Context, Source, SourceActor, Seed, EncounterId, Start))
	{
		UE_LOG(LogPokeMonsterEncounter, Warning, TEXT("Wild encounter '%s' has no valid profile entry."), *EncounterId.ToString());
		return false;
	}
	return StartEncounter(Start, Player);
}

bool UPokeMonsterEncounterSubsystem::PrepareTrainerEncounter(const UPokeMonsterTrainerProfile* Profile,
	AActor* SourceActor, int32 Seed, FPokeMonsterEncounterStartData& OutStart)
{
	OutStart = FPokeMonsterEncounterStartData();
	if (!IsValid(Profile) || !Profile->BuildTeam(OutStart.OpponentTeam)) return false;
	OutStart.PresentationMode=Profile->PresentationMode;
 OutStart.BattleEnvironment=Profile->BattleEnvironment;
	OutStart.EncounterId = Profile->InternalId;
	OutStart.TrainerId = Profile->InternalId;
	OutStart.Kind = EPokeMonsterEncounterKind::Trainer;
	OutStart.Source = EPokeMonsterEncounterSource::Scripted;
	OutStart.RandomSeed = Seed;
	OutStart.SourceActor = SourceActor;
	return true;
}

bool UPokeMonsterEncounterSubsystem::StartTrainerEncounter(const UPokeMonsterTrainerProfile* Profile,
	APokeMonsterPlayerCharacter* Player, AActor* SourceActor, int32 Seed)
{
	FPokeMonsterEncounterStartData Start;
	if (!PrepareTrainerEncounter(Profile, SourceActor, Seed, Start)
		|| IsTrainerDefeated(Start.TrainerId) || !EnsureDevPlayerParty()) return false;
	return StartEncounter(Start, Player);
}

void UPokeMonsterEncounterSubsystem::RestoreDefeatedTrainerIds(const TArray<FName>& TrainerIds)
{
	DefeatedTrainerIds.Reset();
	for (FName Id : TrainerIds) if (!Id.IsNone()) DefeatedTrainerIds.Add(Id);
}

bool UPokeMonsterEncounterSubsystem::RestorePersistentState(
	const TArray<FPokeMonsterCreatureInstance>& Team, const TArray<FName>& TrainerIds,
	const TArray<FName>& EncounterIds)
{
	if (bActive || Team.Num() > 6) return false;
	TSet<FGuid> Seen;
	for (const FPokeMonsterCreatureInstance& Creature : Team)
	{
		if (!Creature.IsValid() || Seen.Contains(Creature.InstanceId)) return false;
		Seen.Add(Creature.InstanceId);
	}
	PlayerParty = Team;
	RestoreDefeatedTrainerIds(TrainerIds);
	CompletedEncounterIds.Reset();
	for (FName Id : EncounterIds) if (!Id.IsNone()) CompletedEncounterIds.Add(Id);
	OnPersistentStateRestored.Broadcast();
	return true;
}

void UPokeMonsterEncounterSubsystem::RecordTrainerOutcome(const FPokeMonsterEncounterEndData& Result)
{
	if (Result.Kind == EPokeMonsterEncounterKind::Trainer && !Result.TrainerId.IsNone()
		&& Result.Outcome == EPokeMonsterEncounterOutcome::Victory)
		DefeatedTrainerIds.Add(Result.TrainerId);
}

bool UPokeMonsterEncounterSubsystem::StartEncounter(const FPokeMonsterEncounterStartData& Start,
	APokeMonsterPlayerCharacter* Player)
{
    if (!APokeMonsterGameMode::AllowsPersistentGameplay(GetWorld())) return false;
	if (bActive || !IsValid(Player) || Player->IsOverworldInputLocked()) return false;
 if(uint8(Start.BattleEnvironment)>uint8(EPokeMonsterBattleEnvironment::Ruins))return false;
	if(Start.PresentationMode!=EPokeMonsterBattlePresentationMode::ClassicBattle && Start.PresentationMode!=EPokeMonsterBattlePresentationMode::WorldBattle)return false;
	if (Start.Kind == EPokeMonsterEncounterKind::Trainer
		&& (Start.TrainerId.IsNone() || IsTrainerDefeated(Start.TrainerId))) return false;
	APlayerController* Controller = Cast<APlayerController>(Player->GetController());
	UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr;
	if (!Controller || !Controller->IsLocalController() || !World || Player->GetWorld() != World) return false;

	const TArray<FPokeMonsterCreatureInstance>& Team = Start.PlayerTeam.IsEmpty() ? PlayerParty : Start.PlayerTeam;
	UPokeMonsterBattlePresenter* NewPresenter = NewObject<UPokeMonsterBattlePresenter>(this);
	UPokeMonsterInventorySubsystem* Inventory = GetGameInstance()->GetSubsystem<UPokeMonsterInventorySubsystem>();
	if (!NewPresenter->InitializeTeamBattle(Team, Start.OpponentTeam, Start.RandomSeed,
		Start.Kind == EPokeMonsterEncounterKind::Wild, Inventory, Start.bAllowFlee&&Start.Kind==EPokeMonsterEncounterKind::Wild&&Start.Source!=EPokeMonsterEncounterSource::Scripted, Start.Kind==EPokeMonsterEncounterKind::Trainer, Start.EffectRules)) return false;
	UPokeMonsterBattleWidget* NewWidget = CreateWidget<UPokeMonsterBattleWidget>(Controller, UPokeMonsterBattleWidget::StaticClass());
	if (!NewWidget) return false;

	Presenter = NewPresenter;
	BattleWidget = NewWidget;
	ActiveStart = Start;
	ActivePlayer = Player;
	ActiveController = Controller;
	bPreviousMouseCursor = Controller->bShowMouseCursor;
	bActive = true;
	PlayerParty = Team;
	Player->SetOverworldInputLocked(true);
	NewWidget->SetEncounterOverlay(true);
	CreatePresentation();
	NewWidget->OnWorldPresentationStep.AddUniqueDynamic(this,&UPokeMonsterEncounterSubsystem::HandleWorldPresentationStep);
	NewWidget->SetPresenter(NewPresenter);
	NewWidget->SetIsFocusable(true);
	NewWidget->AddToViewport(100);
	NewPresenter->OnChanged.AddUniqueDynamic(this, &UPokeMonsterEncounterSubsystem::HandlePresenterChanged);
	FInputModeUIOnly Input;
	Input.SetWidgetToFocus(NewWidget->TakeWidget());
	Controller->SetInputMode(Input);
	Controller->bShowMouseCursor = true;
	UE_LOG(LogPokeMonsterEncounter, Display, TEXT("Encounter '%s' started in %s."),
		*Start.EncounterId.ToString(), *World->GetName());
	OnEncounterStarted.Broadcast();
	return true;
}

void UPokeMonsterEncounterSubsystem::HandlePresenterChanged()
{
	if (!bActive || !Presenter || !Presenter->GetView().bFinished || Presenter->GetView().bBusy) return;
	if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
		if (!World->GetTimerManager().IsTimerActive(CompletionTimer))
			World->GetTimerManager().SetTimer(CompletionTimer, this,
				&UPokeMonsterEncounterSubsystem::CompleteEncounter, (PlayerVisual||OpponentVisual)?1.15f:.75f, false);
}

void UPokeMonsterEncounterSubsystem::CompleteEncounter()
{
	if (!bActive || !Presenter) return;
	const FPokeMonsterBattleState* State = Presenter->GetBattleState();
	if (!State || State->Phase != EPokeMonsterBattlePhase::Finished) return;
	LastResult = BuildEndData(ActiveStart, *State);
	PlayerParty = LastResult.PlayerTeam;
 // A distinct later victory is another safe retry event, including at level 100.
 if(LastResult.Outcome==EPokeMonsterEncounterOutcome::Victory)for(auto& C:PlayerParty)if(!C.PendingEvolutionTarget.IsValid())C.LastEvolutionOfferedLevel=0;
	RecordTrainerOutcome(LastResult);
	if (LastResult.Kind == EPokeMonsterEncounterKind::Wild
		&& LastResult.Source == EPokeMonsterEncounterSource::VisibleCreature
		&& !LastResult.EncounterId.IsNone()
		&& (LastResult.Outcome == EPokeMonsterEncounterOutcome::Victory
			|| LastResult.Outcome == EPokeMonsterEncounterOutcome::Captured))
		CompletedEncounterIds.Add(LastResult.EncounterId);
	const bool bDefeated = LastResult.Outcome == EPokeMonsterEncounterOutcome::Defeat;
	APokeMonsterPlayerCharacter* Player = ActivePlayer.Get();
	APlayerController* Controller = ActiveController.Get();
	ReleaseOverworld(bDefeated);
	if (bDefeated)
	{
		auto* Checkpoints = GetGameInstance()
			? GetGameInstance()->GetSubsystem<UPokeMonsterCheckpointSubsystem>() : nullptr;
		if (!Checkpoints || !Checkpoints->BeginDefeatRecovery(Player, Controller))
		{
			UE_LOG(LogPokeMonsterEncounter, Error, TEXT("Defeat recovery could not start; releasing input."));
			if (IsValid(Player)) Player->SetOverworldInputLocked(false);
			if (IsValid(Controller)) Controller->SetInputMode(FInputModeGameAndUI());
		}
	}
	UE_LOG(LogPokeMonsterEncounter, Display, TEXT("Encounter '%s' ended: %s, rounds: %d, party: %d."),
		*LastResult.EncounterId.ToString(),
		LastResult.Outcome==EPokeMonsterEncounterOutcome::Fled?TEXT("Fled"):LastResult.Outcome == EPokeMonsterEncounterOutcome::Captured ? TEXT("Captured")
			: LastResult.Outcome == EPokeMonsterEncounterOutcome::Victory ? TEXT("Victory") : TEXT("Defeat"),
		LastResult.Rounds, PlayerParty.Num());
	OnEncounterEnded.Broadcast(LastResult);
}

FPokeMonsterEncounterEndData UPokeMonsterEncounterSubsystem::BuildEndData(
	const FPokeMonsterEncounterStartData& Start, const FPokeMonsterBattleState& State)
{
	FPokeMonsterEncounterEndData End;
 End.PresentationMode=Start.PresentationMode;
	End.EncounterId = Start.EncounterId;
	End.TrainerId = Start.TrainerId;
	End.Kind = Start.Kind;
	End.Source = Start.Source;
	End.Outcome = (State.EndReason==EPokeMonsterBattleEndReason::Escaped || State.EndReason==EPokeMonsterBattleEndReason::ForcedOut)?EPokeMonsterEncounterOutcome::Fled:State.EndReason == EPokeMonsterBattleEndReason::Captured
		&& Start.Kind == EPokeMonsterEncounterKind::Wild
		? EPokeMonsterEncounterOutcome::Captured
		: State.Winner == EPokeMonsterBattleSide::A
			? EPokeMonsterEncounterOutcome::Victory : EPokeMonsterEncounterOutcome::Defeat;
	End.PlayerTeam = State.TeamA;
	End.OpponentTeam = State.TeamB;
	if (End.Outcome == EPokeMonsterEncounterOutcome::Captured)
	{
		End.CapturedCreature = State.CapturedCreature;
		if (End.PlayerTeam.Num() < 6)
		{
			End.PlayerTeam.Add(End.CapturedCreature);
			End.CaptureTransfer = EPokeMonsterCaptureTransfer::AddedToTeam;
		}
		else End.CaptureTransfer = EPokeMonsterCaptureTransfer::TeamFull;
	}
	End.Rounds = State.RoundNumber;
	End.SourceActor = Start.SourceActor;
	return End;
}

void UPokeMonsterEncounterSubsystem::ReleaseOverworld(const bool bKeepInputLocked)
{
	if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
		World->GetTimerManager().ClearTimer(CompletionTimer);
	if (Presenter) Presenter->OnChanged.RemoveDynamic(this, &UPokeMonsterEncounterSubsystem::HandlePresenterChanged);
	if (BattleWidget){BattleWidget->OnWorldPresentationStep.RemoveDynamic(this,&UPokeMonsterEncounterSubsystem::HandleWorldPresentationStep);BattleWidget->RemoveFromParent();}
 if(ClassicScene){ClassicScene->Destroy();ClassicScene=nullptr;}
 if(IsValid(PlayerVisual))PlayerVisual->Destroy();PlayerVisual=nullptr;
 if(IsValid(OpponentVisual))OpponentVisual->Destroy();OpponentVisual=nullptr;
 if(auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(ActiveStart.SourceActor))Wild->SuppressPresentation(false);
	if (!bKeepInputLocked)
		if (APokeMonsterPlayerCharacter* Player = ActivePlayer.Get()) Player->SetOverworldInputLocked(false);
	if (APlayerController* Controller = ActiveController.Get())
	{
		if (!bKeepInputLocked)
		{
			Controller->SetInputMode(FInputModeGameOnly());
			Controller->bShowMouseCursor = bPreviousMouseCursor;
		}
	}
	BattleWidget = nullptr;
	Presenter = nullptr;
	ActiveStart = FPokeMonsterEncounterStartData();
	ActivePlayer.Reset();
	ActiveController.Reset();
	bActive = false;
}

void UPokeMonsterEncounterSubsystem::Deinitialize()
{
	if (bActive) ReleaseOverworld();
	Super::Deinitialize();
}

void UPokeMonsterEncounterSubsystem::CreatePresentation()
{
 if(ActiveStart.PresentationMode==EPokeMonsterBattlePresentationMode::WorldBattle){CreateWorldPresentation();if(BattleWidget)BattleWidget->SetWorldPresentation(IsValid(PlayerVisual),IsValid(OpponentVisual));return;}
 const auto* State=Presenter?Presenter->GetBattleState():nullptr;auto* Player=ActivePlayer.Get();if(!State||!Player)return;
 if(!ClassicScene)ClassicScene=Player->GetWorld()->SpawnActor<APokeMonsterClassicBattleScene>(FVector(0,0,10000),FRotator::ZeroRotator);
 if(ClassicScene){
  const auto* A=State->TeamA.IsValidIndex(State->ActiveIndexA)?State->TeamA[State->ActiveIndexA].Species.LoadSynchronous():nullptr;
  const auto* B=State->TeamB.IsValidIndex(State->ActiveIndexB)?State->TeamB[State->ActiveIndexB].Species.LoadSynchronous():nullptr;
  ClassicScene->Configure(A,B,Player,ActiveStart.BattleEnvironment,ActiveStart.BattleRegion,ActiveStart.SourceActor);PlayerVisual=ClassicScene->PlayerVisual;OpponentVisual=ClassicScene->OpponentVisual;
 }
 if(BattleWidget){BattleWidget->SetClassicPresentation(ClassicScene?ClassicScene->Target.Get():nullptr,IsValid(PlayerVisual),IsValid(OpponentVisual));if(ClassicScene){BattleWidget->SetBattleAnchors(ClassicScene->ScreenAnchor(true),ClassicScene->ScreenAnchor(false));BattleWidget->SetBattleGroundAnchors(ClassicScene->ScreenAnchor(true,true),ClassicScene->ScreenAnchor(false,true));}}
 if(auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(ActiveStart.SourceActor))Wild->SuppressPresentation(true);
}
void UPokeMonsterEncounterSubsystem::CreateWorldPresentation()
{
 const auto* State=Presenter?Presenter->GetBattleState():nullptr;auto* Player=ActivePlayer.Get();if(!State||!Player)return;
 const float PlayerGround=Player->GetActorLocation().Z-Player->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
 auto Spawn=[&](const TArray<FPokeMonsterCreatureInstance>& Team,int32 Index,const FVector& Centre,const FVector& Forward,const FVector& Right,float Side)->APokeMonsterCreatureVisualActor*
 {
  if(!Team.IsValidIndex(Index))return nullptr;auto* Species=Team[Index].Species.LoadSynchronous();
  auto* Data=Species?Species->GetVisuals().Presentation.LoadSynchronous():nullptr;if(!Data||!Data->Mesh)return nullptr;
  for(float Across:{50.f,65.f,80.f})for(float Ahead:{45.f,70.f,20.f,90.f})
  {
   FVector Location=Centre+Forward*Ahead+Right*(Side*Across);FHitResult Hit;
   FCollisionQueryParams Ground(SCENE_QUERY_STAT(CreaturePresentationGround),true);Ground.AddIgnoredActor(Player);if(ActiveStart.SourceActor)Ground.AddIgnoredActor(ActiveStart.SourceActor);
   if(!Player->GetWorld()->LineTraceSingleByChannel(Hit,Location+FVector(0,0,150),Location-FVector(0,0,250),ECC_Visibility,Ground))continue;
   if(Hit.ImpactNormal.Z<.7f||FMath::Abs(Hit.ImpactPoint.Z-PlayerGround)>15.f)continue;
   FCollisionQueryParams Space(SCENE_QUERY_STAT(CreaturePresentationSpace),false);Space.AddIgnoredActor(Player);
   if(Player->GetWorld()->OverlapBlockingTestByChannel(Hit.ImpactPoint+FVector(0,0,32),FQuat::Identity,ECC_Visibility,FCollisionShape::MakeSphere(22.f),Space))continue;
   Location.Z=Hit.ImpactPoint.Z-Data->GroundOffsetCm;
   auto* V=Player->GetWorld()->SpawnActor<APokeMonsterCreatureVisualActor>(Location,FRotator::ZeroRotator);
   if(V&&!V->SetSpecies(Species)){V->Destroy();return nullptr;}return V;
  }
  return nullptr; // Keep the existing UI fallback when no safe ground location is available.
 };
 // Keep short creatures within the existing player sight-cone. No camera or tree material changes.
 const auto* Controller=ActiveController.Get();
 const float Yaw=Controller&&Controller->PlayerCameraManager?Controller->PlayerCameraManager->GetCameraRotation().Yaw:Player->GetActorRotation().Yaw;
 const FRotationMatrix View(FRotator(0,Yaw,0));const FVector Forward=View.GetUnitAxis(EAxis::X),Right=View.GetUnitAxis(EAxis::Y);
 const FVector Centre=Player->GetActorLocation();
 const FVector Direction=Right;
 PlayerVisual=Spawn(State->TeamA,State->ActiveIndexA,Centre,Forward,Right,-1.f);
 OpponentVisual=Spawn(State->TeamB,State->ActiveIndexB,Centre,Forward,Right,1.f);
 if(PlayerVisual)PlayerVisual->SetActorRotation(Direction.Rotation());
 if(OpponentVisual){OpponentVisual->SetActorRotation((-Direction).Rotation());if(auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(ActiveStart.SourceActor))Wild->SuppressPresentation(true);}
}
void UPokeMonsterEncounterSubsystem::UpdateWorldSpecies()
{
 if(ClassicScene){ClassicScene->Destroy();ClassicScene=nullptr;}
 if(IsValid(PlayerVisual))PlayerVisual->Destroy();PlayerVisual=nullptr;
 if(IsValid(OpponentVisual))OpponentVisual->Destroy();OpponentVisual=nullptr;
 if(auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(ActiveStart.SourceActor))Wild->SuppressPresentation(false);
 CreatePresentation();
}
void UPokeMonsterEncounterSubsystem::HandleWorldPresentationStep(const FPokeMonsterPresentationAction& A,FName Step)
{
 if(ClassicScene&&!A.bFlee&&!A.bItem&&!A.bInformation&&!A.bResidual)ClassicScene->React(A.Source==EPokeMonsterBattleSide::A,Step,A.Damage);
 auto* Source=A.Source==EPokeMonsterBattleSide::A?PlayerVisual.Get():OpponentVisual.Get();
 auto* Target=A.Target==EPokeMonsterBattleSide::A?PlayerVisual.Get():OpponentVisual.Get();
 if(A.bSwitch&&Step==TEXT("Impact")){UpdateWorldSpecies();return;}
 if(Step==TEXT("Windup")&&!A.bSwitch&&!A.bCapture&&!A.bFlee&&!A.bItem&&!A.bInformation&&!A.bResidual&&Source)Source->PlayReaction(EPokeMonsterCreatureClip::Attack);
 if(Step==TEXT("Impact")&&A.Outcome==EPokeMonsterPresentationOutcome::Hit&&A.Damage>0&&Target)Target->PlayReaction(EPokeMonsterCreatureClip::Hit);
 if(Step==TEXT("KO")&&A.bKnockedOut&&Target)Target->PlayReaction(EPokeMonsterCreatureClip::Faint);
 if(Step==TEXT("KO")&&A.bCaptureSucceeded&&OpponentVisual)OpponentVisual->SetActorHiddenInGame(true);
 if(Step==TEXT("Complete")&&A.bBattleEnded&&Source&&!A.bCapture&&!A.bFlee)Source->PlayReaction(EPokeMonsterCreatureClip::Happy);
}

bool UPokeMonsterEncounterSubsystem::CommitRememberedMoves(APokeMonsterNPC* Master,
 APokeMonsterPlayerCharacter* Player, const FPokeMonsterCreatureInstance& Expected,
 const TArray<TSoftObjectPtr<UPokeMonsterMoveData>>& Moves)
{
 if (bActive || !IsValid(Master) || !Master->CanProvideMoveService(Player)
  || !Player->IsOverworldInputLocked() || Player->GetGameInstance()!=GetGameInstance()) return false;
 const int32 Index=PlayerParty.IndexOfByPredicate([&](const auto& C) { return C.InstanceId==Expected.InstanceId; });
 if (Index==INDEX_NONE) return false;
 const auto& Current=PlayerParty[Index];
 auto SameSlots=[](const auto& A,const auto& B)
 {
  if(A.Num()!=B.Num())return false;
  for(int32 I=0;I<A.Num();++I)if(A[I].GetMove()!=B[I].GetMove() || A[I].GetCurrentPP()!=B[I].GetCurrentPP() || A[I].GetMaxPP()!=B[I].GetMaxPP())return false;
  return true;
 };
 if(Current.Species!=Expected.Species || Current.Level!=Expected.Level || Current.Experience!=Expected.Experience
  || Current.CurrentHP!=Expected.CurrentHP || Current.Status!=Expected.Status || Current.StatusTurns!=Expected.StatusTurns || !Current.PendingMoves.IsEmpty()
  || !SameSlots(Current.GetMoveSlots(),Expected.GetMoveSlots()) || !SameSlots(Current.GetLearnedMoves(),Expected.GetLearnedMoves()))return false;
 auto Next=Current;
 if(!Next.SetActiveLearnedMoves(Moves))return false;
 auto* Save=GetGameInstance()?GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>():nullptr;
 if(!Save)return false;
 const auto Previous=Current;
 PlayerParty[Index]=Next;
 if(!Save->SaveProgressGame()) { PlayerParty[Index]=Previous; return false; }
 return true;
}

// Evolution is a transaction on the existing party, never a second creature roster.
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"

int32 UPokeMonsterEncounterSubsystem::PrepareEvolutionOffer(FGuid OnlyCreatureId)
{
 if(IsEncounterActive())return INDEX_NONE;
 if(auto* C=GetGameInstance()->GetSubsystem<UPokeMonsterCheckpointSubsystem>();C&&C->IsReturningFromDefeat())return INDEX_NONE;
 for(int32 I=0;I<PlayerParty.Num();++I)
 {
  auto& C=PlayerParty[I];if(OnlyCreatureId.IsValid()&&C.InstanceId!=OnlyCreatureId)continue;if(C.CurrentHP<=0||!C.PendingMoves.IsEmpty())continue;
  FPokeMonsterEvolutionContext Context;
  for(const auto& O:UPokeMonsterCreatureProgression::GetEvolutionOptions(C,Context))if(O.Readiness==EPokeMonsterEvolutionReadiness::Ready)
  {
   if(C.PendingEvolutionTarget.IsValid()) {if(C.PendingEvolutionTarget==O.TargetSpecies)return I;continue;}
   if(C.LastEvolutionOfferedLevel>=C.Level)continue;
   const auto Old=C;C.PendingEvolutionTarget=O.TargetSpecies;C.LastEvolutionOfferedLevel=C.Level;
   auto* Save=GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>();
   if(!Save||!Save->SaveProgressGame()){C=Old;return INDEX_NONE;}
   return I;
  }
 }
 return INDEX_NONE;
}
bool UPokeMonsterEncounterSubsystem::ResolveEvolution(FGuid Id,FPrimaryAssetId Target,bool Accept)
{
 if(IsEncounterActive())return false;
 if(auto* Recovery=GetGameInstance()->GetSubsystem<UPokeMonsterCheckpointSubsystem>();Recovery&&Recovery->IsReturningFromDefeat())return false;
 auto* C=PlayerParty.FindByPredicate([Id](const auto& X){return X.InstanceId==Id;});
 if(!C||C->PendingEvolutionTarget!=Target||!Target.IsValid()||!C->ValidateEvolutionState()||!C->PendingMoves.IsEmpty())return false;
 const auto Old=*C;auto Candidate=Old;
 if(Accept){FPokeMonsterEvolutionContext Context;if(!UPokeMonsterCreatureProgression::ApplyEvolution(Candidate,Target,Context))return false;}
 else Candidate.PendingEvolutionTarget=FPrimaryAssetId();
 *C=Candidate;
 auto* Q=GetGameInstance()->GetSubsystem<UPokeMonsterQuestSubsystem>();const auto OldDex=Q?Q->GetCapturedSpeciesIds():TArray<FName>();
 const auto OldProgress=Q?Q->GetProgress():TArray<FPokeMonsterQuestProgress>();const auto OldFlags=CompletedEncounterIds;
 if(Accept&&Q)if(auto* S=C->Species.LoadSynchronous())Q->RecordCapturedSpecies(S->GetInternalId());
 auto* Save=GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>();
 if(!Save||!Save->SaveProgressGame()){*C=Old;CompletedEncounterIds=OldFlags;if(Q){Q->RestoreCapturedSpeciesIds(OldDex);Q->RestoreProgress(OldProgress);}return false;}
 OnPersistentStateRestored.Broadcast();return true;
}
bool UPokeMonsterEncounterSubsystem::ResolveEvolutionLearning(FGuid Id,int32 Slot)
{
 if(IsEncounterActive())return false;
 if(auto* Recovery=GetGameInstance()->GetSubsystem<UPokeMonsterCheckpointSubsystem>();Recovery&&Recovery->IsReturningFromDefeat())return false;
 auto* C=PlayerParty.FindByPredicate([Id](const auto& X){return X.InstanceId==Id;});
 if(!C||C->PendingMoves.IsEmpty())return false;
 const auto Old=*C;auto Copy=Old;if(!Copy.ResolveMoveLearning(Slot))return false;*C=Copy;
 auto* Save=GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>();
 if(!Save||!Save->SaveProgressGame()){*C=Old;return false;}
 OnPersistentStateRestored.Broadcast();return true;
}
