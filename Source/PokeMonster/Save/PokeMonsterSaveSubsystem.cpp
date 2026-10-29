#include "PokeMonsterSaveSubsystem.h"
#include "../Game/PokeMonsterGameMode.h"

#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "HAL/PlatformFileManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Engine/World.h"
#include "UObject/UObjectIterator.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerStart.h"
#include "EngineUtils.h"
#include "Misc/PackageName.h"
#include "Misc/ScopeLock.h"
#include "TimerManager.h"
#include "Camera/PlayerCameraManager.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterSave, Log, All);

const FString UPokeMonsterSaveSubsystem::DevSlotName = TEXT("PokeMonster_Dev");
const FString UPokeMonsterSaveSubsystem::RecoverySlotName = TEXT("PokeMonster_Recovery");

bool FPokeMonsterSavedPlayerLocation::IsValid() const
{
 return bHasPosition && MapPackage.ToString().StartsWith(TEXT("/Game/"))
  && FPackageName::IsValidLongPackageName(MapPackage.ToString())
  && !Location.ContainsNaN() && !Rotation.ContainsNaN()
  && !FacingDirection.ContainsNaN() && FMath::IsNearlyEqual(FacingDirection.SizeSquared(), 1., .01)
  && FMath::Abs(FacingDirection.Z) < .01
  && Location.GetAbsMax() < HALF_WORLD_MAX
  && FMath::Abs(Rotation.Pitch) < 36000. && FMath::Abs(Rotation.Yaw) < 36000.
  && FMath::Abs(Rotation.Roll) < 36000. && (!bRelocatedInterior || !InteriorActor.IsNone());
}

FPokeMonsterSavedPlayerLocation UPokeMonsterSaveSubsystem::CapturePlayerLocation(const UWorld* World)
{
 FPokeMonsterSavedPlayerLocation Result;
 const auto* Player = World ? Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(World, 0)) : nullptr;
 if (!Player) return Result;
 Result.bHasPosition = true;
 Result.MapPackage = UPokeMonsterCheckpointSubsystem::GetMapPackage(World);
 Result.Location = Player->GetActorLocation();
 Result.Rotation = Player->GetActorRotation();
 Result.FacingDirection = Player->GetInteractionWorldDirection().GetSafeNormal2D();
 for (TActorIterator<APokeMonsterBuildingCutaway> It(World); It; ++It)
  if (It->IsViewerInside(Result.Location))
  {
   Result.InteriorActor = It->GetFName();
   Result.bRelocatedInterior = It->IsViewerInRelocatedRoom(Result.Location);
   break;
  }
 return Result;
}

namespace
{
	template<typename T>
	T* ResolveAsset(const FPrimaryAssetId& Id, const FPrimaryAssetType& ExpectedType)
	{
		if (!Id.IsValid() || Id.PrimaryAssetType != ExpectedType)
		{
			UE_LOG(LogPokeMonsterSave, Error, TEXT("Invalid asset ID '%s'; expected type '%s'."),
				*Id.ToString(), *ExpectedType.ToString());
			return nullptr;
		}
		const FSoftObjectPath Path = UAssetManager::Get().GetPrimaryAssetPath(Id);
		T* Asset = Path.IsValid() ? Cast<T>(Path.TryLoad()) : nullptr;
		if (!IsValid(Asset) || Asset->GetPrimaryAssetId() != Id)
		{
			UE_LOG(LogPokeMonsterSave, Error, TEXT("Missing or mismatched asset '%s' at '%s'."),
				*Id.ToString(), *Path.ToString());
			return nullptr;
		}
		return Asset;
	}

	bool DecodeCreature(const FPokeMonsterSavedCreature& Saved, FPokeMonsterCreatureInstance& Out, int32 Version)
	{
		auto* Species = ResolveAsset<UPokeMonsterCreatureSpeciesData>(Saved.SpeciesId, TEXT("CreatureSpecies"));
		if(Version<7 && uint8(Saved.Status)>uint8(EPokeMonsterCreatureStatus::Burn))return false;
		if (!Species || Saved.Moves.Num() != FPokeMonsterCreatureInstance::MoveSlotCount) return false;
		Out = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, Saved.Level);
  if(Version>=8){Out.bHasExperienceGrowthOverride=Saved.bHasExperienceGrowthOverride;Out.ExperienceGrowthOverride=Saved.ExperienceGrowthOverride;
   Out.PendingEvolutionTarget=Saved.PendingEvolutionTarget;Out.LastEvolutionOfferedLevel=Saved.LastEvolutionOfferedLevel;}
  if(Version>=11)Out.PendingEvolutionItemId=Saved.PendingEvolutionItemId;
  if(!Out.ValidateEvolutionState())return false;
		TArray<FPokeMonsterMoveSlot> Slots;
		Slots.SetNum(FPokeMonsterCreatureInstance::MoveSlotCount);
		for (int32 Index = 0; Index < Slots.Num(); ++Index)
		{
			const FPokeMonsterSavedMove& Move = Saved.Moves[Index];
			if (!Move.MoveId.IsValid())
			{
				if (Move.CurrentPP != 0) return false;
				continue;
			}
			auto* Data = ResolveAsset<UPokeMonsterMoveData>(Move.MoveId, TEXT("CreatureMove"));
			if (!Data || !Slots[Index].AssignMove(Data) || !Slots[Index].RestoreCurrentPP(Move.CurrentPP)) return false;
		}
		if(!Out.RestoreIndividualState(Saved.InstanceId, Saved.Level, Saved.Experience, Saved.CurrentHP, Slots, Version>=4?Saved.Status:EPokeMonsterCreatureStatus::None,Version>=7?Saved.StatusTurns:0))return false;
  if (Version >= 6)
  {
   TArray<FPokeMonsterMoveSlot> Known;
   for (const auto& SavedMove : Saved.LearnedMoves)
   {
    auto* Move=ResolveAsset<UPokeMonsterMoveData>(SavedMove.MoveId,TEXT("CreatureMove"));
    FPokeMonsterMoveSlot Slot;
    if (!Move || !Slot.AssignMove(Move) || !Slot.RestoreCurrentPP(SavedMove.CurrentPP)) return false;
    Known.Add(Slot);
   }
   if (!Out.RestoreLearnedMoves(Known)) return false;
  } // Versions 1..5 seed only actual active moves, never the species learnlist.
  if (Version >= 5)
  {
   TArray<TSoftObjectPtr<UPokeMonsterMoveData>> Pending;
   for (const auto& Id : Saved.PendingMoves)
   {
    auto* Move = ResolveAsset<UPokeMonsterMoveData>(Id, TEXT("CreatureMove"));
    if (!Move) return false;
    Pending.Add(Move);
   }
   if (!Out.RestorePendingMoves(Pending)) return false;
  }
  return Version>=4||Out.UpgradeLegacyGlumandaMoves();
	}
}

UPokeMonsterSaveGame* UPokeMonsterSaveSubsystem::CaptureSnapshot(
	const UPokeMonsterEncounterSubsystem* Encounter, const UPokeMonsterInventorySubsystem* Inventory,
	UObject* Outer, const UPokeMonsterCheckpointSubsystem* Checkpoint, const UPokeMonsterQuestSubsystem* Quests, const UPokeMonsterWorldClock* Clock)
{
	if (!IsValid(Encounter) || !IsValid(Inventory) || Encounter->IsEncounterActive()
		|| (IsValid(Checkpoint) && Checkpoint->IsReturningFromDefeat())) return nullptr;
	if (Encounter->GetPlayerParty().Num() > 6) return nullptr;
	auto* Save = NewObject<UPokeMonsterSaveGame>(Outer ? Outer : GetTransientPackage());
	for (const FPokeMonsterCreatureInstance& Creature : Encounter->GetPlayerParty())
	{
		const auto* Species = Creature.Species.LoadSynchronous();
		FPokeMonsterCreatureInstance Validated = Creature;
		if (!Creature.IsValid() || !Creature.ValidateEvolutionState() || !IsValid(Species)
			|| !Validated.RestoreIndividualState(Creature.InstanceId, Creature.Level, Creature.Experience,
				Creature.CurrentHP, Creature.GetMoveSlots(), Creature.Status, Creature.StatusTurns)
            || !Validated.RestoreLearnedMoves(Creature.GetLearnedMoves())
            || !Validated.RestorePendingMoves(Creature.PendingMoves)) return nullptr;
		FPokeMonsterSavedCreature& Entry = Save->PlayerTeam.AddDefaulted_GetRef();
		Entry.InstanceId = Creature.InstanceId;
		Entry.SpeciesId = Species->GetPrimaryAssetId();
		Entry.Level = Creature.Level;
		Entry.Experience = Creature.Experience;
		Entry.CurrentHP = Creature.CurrentHP;
  Entry.bHasExperienceGrowthOverride=Creature.bHasExperienceGrowthOverride;Entry.ExperienceGrowthOverride=Creature.ExperienceGrowthOverride;
  Entry.PendingEvolutionTarget=Creature.PendingEvolutionTarget;Entry.LastEvolutionOfferedLevel=Creature.LastEvolutionOfferedLevel;
  Entry.PendingEvolutionItemId=Creature.PendingEvolutionItemId;
  Entry.Status=Creature.Status; Entry.StatusTurns=Creature.StatusTurns;
  for (const auto& Ref : Creature.PendingMoves)
  {
   const auto* Move = Ref.LoadSynchronous();
   if (!Move) return nullptr;
   Entry.PendingMoves.Add(Move->GetPrimaryAssetId());
  }
  for (const auto& Known : Creature.GetLearnedMoves())
  {
   const auto* Move=Known.GetMove().LoadSynchronous();
   if (!Move) return nullptr;
   FPokeMonsterSavedMove EntryMove; EntryMove.MoveId=Move->GetPrimaryAssetId(); EntryMove.CurrentPP=Known.GetCurrentPP();
   Entry.LearnedMoves.Add(EntryMove);
  }
		for (const FPokeMonsterMoveSlot& Slot : Creature.GetMoveSlots())
		{
			FPokeMonsterSavedMove& SavedMove = Entry.Moves.AddDefaulted_GetRef();
			if (!Slot.GetMove().IsNull())
			{
				const auto* Data = Slot.GetMove().LoadSynchronous();
				if (!IsValid(Data)) return nullptr;
				SavedMove.MoveId = Data->GetPrimaryAssetId();
			}
			SavedMove.CurrentPP = Slot.GetCurrentPP();
		}
	}
	for (const FPokeMonsterInventoryStack& Stack : Inventory->GetStacks())
	{
		const auto* Item = Stack.Item.LoadSynchronous();
		if (!IsValid(Item) || !Item->IsConfigured() || Stack.Quantity < 1
			|| Stack.Quantity > Item->GetMaxStackSize()) return nullptr;
		FPokeMonsterSavedItemStack& Entry = Save->InventoryStacks.AddDefaulted_GetRef();
		Entry.ItemId = Item->GetPrimaryAssetId();
		Entry.Quantity = Stack.Quantity;
	}
	Save->DefeatedTrainerIds = Encounter->GetDefeatedTrainerIds();
	Save->CompletedEncounterIds = Encounter->GetCompletedEncounterIds();
	Save->DefeatedTrainerIds.Sort(FNameLexicalLess());
	Save->CompletedEncounterIds.Sort(FNameLexicalLess());
	if (IsValid(Checkpoint)) Save->ActiveCheckpoint = Checkpoint->GetActiveCheckpoint();
 Save->PlayerLocation = CapturePlayerLocation(Encounter->GetWorld());
 if(Clock){Save->WorldTime=Clock->GetTime();Save->bHasWorldTime=true;}
	if (IsValid(Quests))
	{
		Save->QuestProgress = Quests->GetProgress();
		Save->CapturedSpeciesIds = Quests->GetCapturedSpeciesIds();
		Save->CapturedSpeciesIds.Sort(FNameLexicalLess());
	}
	return Save;
}

bool UPokeMonsterSaveSubsystem::RestoreSnapshot(const UPokeMonsterSaveGame* Save,
	UPokeMonsterEncounterSubsystem* Encounter, UPokeMonsterInventorySubsystem* Inventory,
	UPokeMonsterCheckpointSubsystem* Checkpoint, UPokeMonsterQuestSubsystem* Quests, bool bValidateOnly, UPokeMonsterWorldClock* Clock)
{
	if (!IsValid(Save) || !IsValid(Encounter) || !IsValid(Inventory) || Encounter->IsEncounterActive()
		|| (IsValid(Checkpoint) && Checkpoint->IsReturningFromDefeat())) return false;
	// Version 1 had no checkpoint. It migrates to an unset return location.
	if (Save->SaveVersion < 1 || Save->SaveVersion > UPokeMonsterSaveGame::CurrentVersion)
	{
		UE_LOG(LogPokeMonsterSave, Error, TEXT("Unsupported save version %d (supported: 1 through %d)."),
			Save->SaveVersion, UPokeMonsterSaveGame::CurrentVersion);
		return false;
	}
	FPokeMonsterCheckpointData SavedCheckpoint;
	if (Save->SaveVersion >= 2)
	{
		SavedCheckpoint = Save->ActiveCheckpoint;
		if ((!SavedCheckpoint.CheckpointId.IsNone() && !SavedCheckpoint.IsValid())
			|| (SavedCheckpoint.CheckpointId.IsNone() && (!SavedCheckpoint.MapPackage.IsNone()
				|| !SavedCheckpoint.Location.IsNearlyZero() || !SavedCheckpoint.Rotation.IsNearlyZero())))
		{
			UE_LOG(LogPokeMonsterSave, Error, TEXT("Invalid checkpoint in save."));
			return false;
		}
	}
	if (Save->PlayerTeam.Num() > 6) return false;
	TArray<FPokeMonsterCreatureInstance> Team;
	TSet<FGuid> Seen;
	for (const FPokeMonsterSavedCreature& Saved : Save->PlayerTeam)
	{
		FPokeMonsterCreatureInstance Creature;
		if (!DecodeCreature(Saved, Creature, Save->SaveVersion) || Seen.Contains(Creature.InstanceId))
		{
			UE_LOG(LogPokeMonsterSave, Error, TEXT("Invalid creature in save: %s."), *Saved.SpeciesId.ToString());
			return false;
		}
		Seen.Add(Creature.InstanceId);
		Team.Add(MoveTemp(Creature));
	}
	TArray<FPokeMonsterInventoryStack> Stacks;
	int64 TotalQuantity = 0;
	for (const FPokeMonsterSavedItemStack& Saved : Save->InventoryStacks)
	{
		auto* Item = ResolveAsset<UPokeMonsterItemData>(Saved.ItemId, TEXT("Item"));
		if (!Item || !Item->IsConfigured() || Saved.Quantity < 1
			|| Saved.Quantity > Item->GetMaxStackSize()) return false;
		TotalQuantity += Saved.Quantity;
		if (TotalQuantity > MAX_int32) return false;
		FPokeMonsterInventoryStack& Stack = Stacks.AddDefaulted_GetRef();
		Stack.Item = Item;
		Stack.Quantity = Saved.Quantity;
	}
	for (FName Id : Save->DefeatedTrainerIds) if (Id.IsNone()) return false;
	for (FName Id : Save->CompletedEncounterIds) if (Id.IsNone()) return false;
	if (Save->SaveVersion >= 3 && !Save->QuestProgress.IsEmpty()
		&& (!IsValid(Quests) || !Quests->ValidateSavedProgress(Save->QuestProgress)))
	{
		UE_LOG(LogPokeMonsterSave, Error, TEXT("Invalid quest progress in save."));
		return false;
	}
	if (Save->SaveVersion >= 3)
		for (FName Id : Save->CapturedSpeciesIds) if (Id.IsNone()) return false;
	if (bValidateOnly) return true;
 const TArray<FPokeMonsterInventoryStack> PreviousStacks = Inventory->GetStacks();
	if (!Inventory->RestoreStacks(Stacks)) return false;
	if (!Encounter->RestorePersistentState(Team, Save->DefeatedTrainerIds, Save->CompletedEncounterIds))
	{
		Inventory->RestoreStacks(PreviousStacks);
		return false;
	}
	if (IsValid(Checkpoint)) Checkpoint->RestoreCheckpoint(SavedCheckpoint);
	if (IsValid(Quests))
	{
		Quests->RestoreCapturedSpeciesIds(Save->SaveVersion >= 3 ? Save->CapturedSpeciesIds : TArray<FName>{});
		Quests->RestoreProgress(Save->SaveVersion >= 3 ? Save->QuestProgress : TArray<FPokeMonsterQuestProgress>{});
		if (Save->SaveVersion < 3) Quests->MigrateLegacyMiniSlice(Encounter);
		Quests->RefreshProgress(Encounter, Inventory);
	}
 if(Clock)Clock->RestoreTime(Save->WorldTime,Save->SaveVersion>=10&&Save->bHasWorldTime);
	return true;
}

bool UPokeMonsterSaveSubsystem::SaveSnapshotToSlot(UPokeMonsterSaveGame* Save, const FString& SlotName)
{
#if WITH_EDITOR
    // A low-level caller must not bypass an active manual PIE preview's disk protection.
    if (SlotName == DevSlotName || SlotName == RecoverySlotName)
        for (TObjectIterator<UPokeMonsterSaveSubsystem> It; It; ++It)
            if ((It->IsPIEMemoryPreviewActive() || !It->IsolatedPIESlot.IsEmpty()) && It->GetWorld()
                && It->GetWorld()->WorldType == EWorldType::PIE) return false;
#endif
	// This project targets macOS. Its physical MoveFile uses same-filesystem rename(2),
	// replacing the old destination atomically, without deleting it first.
#if PLATFORM_MAC
	if (!IsValid(Save) || SlotName.IsEmpty() || SlotName != FPaths::GetCleanFilename(SlotName)
		|| SlotName.Contains(TEXT("..")) || SlotName.Contains(TEXT(":"))) return false;
	TArray<uint8> Bytes;
	if (!UGameplayStatics::SaveGameToMemory(Save, Bytes) || Bytes.IsEmpty()) return false;
	IPlatformFile& Files = FPlatformFileManager::Get().GetPlatformPhysical();
	const FString Directory = FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir() / TEXT("SaveGames"));
	if (!Files.CreateDirectoryTree(*Directory)) return false;
	const FString Destination = Directory / (SlotName + TEXT(".sav"));
	const FString Temporary = Destination + TEXT(".") + FGuid::NewGuid().ToString(EGuidFormats::Digits) + TEXT(".pending");
	TArray<uint8> Verified;
	const bool bWritten = FFileHelper::SaveArrayToFile(Bytes, *Temporary)
		&& FFileHelper::LoadFileToArray(Verified, *Temporary) && Verified == Bytes
		&& Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Verified));
	const bool bCommitted = bWritten && Files.MoveFile(*Destination, *Temporary);
	if (!bCommitted && Files.FileExists(*Temporary)) Files.DeleteFile(*Temporary);
	return bCommitted;
#else
	return false;
#endif
}

namespace
{
 bool MapAvailable(FName Name)
 {
  return Name.ToString().StartsWith(TEXT("/Game/"))
   && FPackageName::IsValidLongPackageName(Name.ToString())
   && FPackageName::DoesPackageExist(Name.ToString());
 }
 void InteriorContext(UWorld* World, FPokeMonsterSavedPlayerLocation& Location)
 {
  Location.InteriorActor = NAME_None; Location.bRelocatedInterior = false;
  for (TActorIterator<APokeMonsterBuildingCutaway> It(World); It; ++It)
   if (It->IsViewerInside(Location.Location))
   {
    Location.InteriorActor = It->GetFName();
    Location.bRelocatedInterior = It->IsViewerInRelocatedRoom(Location.Location);
    break;
   }
 }
 bool SafeLocation(APokeMonsterPlayerCharacter* Player, const FPokeMonsterSavedPlayerLocation& Candidate)
 {
  if (!Player || !Candidate.IsValid()) return false;
  UWorld* World = Player->GetWorld();
  if (Candidate.MapPackage != UPokeMonsterCheckpointSubsystem::GetMapPackage(World)) return false;
  FPokeMonsterSavedPlayerLocation Context = Candidate; InteriorContext(World, Context);
  if (Context.InteriorActor != Candidate.InteriorActor
   || Context.bRelocatedInterior != Candidate.bRelocatedInterior) return false;
  const auto* Capsule = Player->GetCapsuleComponent();
  FCollisionQueryParams Query(SCENE_QUERY_STAT(SaveV2Position), false, Player);
  const FCollisionShape Shape = FCollisionShape::MakeCapsule(
   FMath::Max(1.f, Capsule->GetScaledCapsuleRadius() - .5f),
   FMath::Max(1.f, Capsule->GetScaledCapsuleHalfHeight() - .5f));
  if (World->OverlapBlockingTestByChannel(Candidate.Location, FQuat::Identity,
   Capsule->GetCollisionObjectType(), Shape, Query, Capsule->GetCollisionResponseToChannels())) return false;
  FHitResult Floor;
  const float HalfHeight = Capsule->GetScaledCapsuleHalfHeight();
  return World->LineTraceSingleByChannel(Floor, Candidate.Location,
   Candidate.Location - FVector(0,0,HalfHeight + 30.f), ECC_Visibility, Query)
   && Floor.bBlockingHit && Floor.ImpactNormal.Z >= Player->GetCharacterMovement()->GetWalkableFloorZ();
 }
 bool ResolvePlacement(APokeMonsterPlayerCharacter* Player, const FPokeMonsterSavedPlayerLocation& Desired,
  FPokeMonsterSavedPlayerLocation& Out)
 {
  if (SafeLocation(Player, Desired)) { Out = Desired; return true; }
  // Only a blocked location is adjusted, within 2 m; do not silently move to another room.
  for (float Radius : {40.f, 80.f, 140.f, 200.f})
   for (int32 Direction = 0; Direction < 8; ++Direction)
   {
    Out = Desired;
    const float Angle = Direction * PI / 4.f;
    Out.Location += FVector(FMath::Cos(Angle)*Radius, FMath::Sin(Angle)*Radius, 0);
    FHitResult Floor;
    FCollisionQueryParams Query(SCENE_QUERY_STAT(SaveV2Fallback), false, Player);
    if (Player->GetWorld()->LineTraceSingleByChannel(Floor, Out.Location + FVector(0,0,80),
     Out.Location - FVector(0,0,180), ECC_Visibility, Query))
     Out.Location.Z = Floor.ImpactPoint.Z + Player->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() + 2.5f;
    if (SafeLocation(Player, Out)) return true;
   }
  return false;
 }
}

void UPokeMonsterSaveSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
 Super::Initialize(Collection);
 PostLoadMapHandle = FCoreUObjectDelegates::PostLoadMapWithWorld.AddUObject(
  this, &UPokeMonsterSaveSubsystem::HandlePostLoadMap);
 if (GEngine) TravelFailureHandle = GEngine->OnTravelFailure().AddUObject(this, &UPokeMonsterSaveSubsystem::HandleTravelFailure);
}

FString UPokeMonsterSaveSubsystem::SlotName(bool bRecovery) const
{
#if WITH_EDITOR
 if (!IsolatedPIESlot.IsEmpty()) return IsolatedPIESlot + (bRecovery ? TEXT("_Recovery") : TEXT(""));
#endif
 return bRecovery ? RecoverySlotName : DevSlotName;
}

bool UPokeMonsterSaveSubsystem::UseIsolatedPIETestSlot(const FString& Name)
{
#if WITH_EDITOR
 if (!GetWorld() || GetWorld()->WorldType != EWorldType::PIE || IsLoadInProgress()
  || IsPIEMemoryPreviewActive() || bWriting || !IsolatedPIESlot.IsEmpty()
  || !Name.StartsWith(TEXT("PokeMonster_SaveV2_Test_")) || Name.Len() > 100) return false;
 for (TCHAR Char : Name) if (!FChar::IsAlnum(Char) && Char != TEXT('_')) return false;
 IsolatedPIESlot = Name;
 return true;
#else
 return false;
#endif
}

bool UPokeMonsterSaveSubsystem::CanAccessWorldState(bool bRecovery) const
{
 if (bWriting || IsLoadInProgress() || !APokeMonsterGameMode::AllowsPersistentGameplay(GetWorld())) return false;
 const auto* GI = GetGameInstance();
 const auto* E = GI ? GI->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
 const auto* C = GI ? GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>() : nullptr;
 const auto* D = GI ? GI->GetSubsystem<UPokeMonsterDialogueSubsystem>() : nullptr;
 const auto* PC = GetWorld() ? Cast<APokeMonsterOverworldPlayerController>(GetWorld()->GetFirstPlayerController()) : nullptr;
 const auto* Player = PC ? Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()) : nullptr;
 if (Player && Player->ActorHasTag(TEXT("PokemonDevelopmentTestVisit"))) return false;
 if (!E || E->IsEncounterActive() || (C && C->IsReturningFromDefeat())
  || (D && D->IsDialogueActive()) || !Player || (!bRecovery && PC && PC->GetEvolutionWidget())) return false;
 if (!bRecovery && Player->IsOverworldInputLocked() && !PC->IsMenuOpen()) return false;
 if (Player->GetCharacterMovement()->IsFalling()
  && (!bRecovery || !SafeLocation(const_cast<APokeMonsterPlayerCharacter*>(Player), CapturePlayerLocation(GetWorld())))) return false;
 for (TActorIterator<APokeMonsterBuildingCutaway> It(GetWorld()); It; ++It)
  if (It->GetRelocationMask() > .001f) return false;
 return true;
}

bool UPokeMonsterSaveSubsystem::SaveCurrentGame() { return WriteCurrentGame(false); }
bool UPokeMonsterSaveSubsystem::SaveRecoveryGame() { return WriteCurrentGame(true); }
bool UPokeMonsterSaveSubsystem::SaveProgressGame() { return WriteCurrentGame(true); }

bool UPokeMonsterSaveSubsystem::WriteCurrentGame(bool bRecovery)
{
 if (!CanAccessWorldState(bRecovery))
 {
  LastStorageMessage = TEXT("Speichern in dieser Spielsituation nicht möglich.");
  const auto* GI=GetGameInstance();const auto* W=GetWorld();
  const auto* PC=W?Cast<APokeMonsterOverworldPlayerController>(W->GetFirstPlayerController()):nullptr;
  const auto* P=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;
  UE_LOG(LogPokeMonsterSave,Display,TEXT("Save guard: automatic=%d world=%s allowed=%d pending=%d writing=%d battle=%d return=%d dialogue=%d pawn=%d falling=%d safe=%d"),
   bRecovery,*GetNameSafe(W),APokeMonsterGameMode::AllowsPersistentGameplay(W),IsLoadInProgress(),bWriting,
   GI&&GI->GetSubsystem<UPokeMonsterEncounterSubsystem>()->IsEncounterActive(),GI&&GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>()->IsReturningFromDefeat(),
   GI&&GI->GetSubsystem<UPokeMonsterDialogueSubsystem>()->IsDialogueActive(),P!=nullptr,P&&P->GetCharacterMovement()->IsFalling(),P&&SafeLocation(const_cast<APokeMonsterPlayerCharacter*>(P),CapturePlayerLocation(W)));
  for(TActorIterator<APokeMonsterBuildingCutaway> It(W);It;++It)if(It->GetRelocationMask()>.001f)UE_LOG(LogPokeMonsterSave,Display,TEXT("Save guard: transitioning building %s mask=%f"),*It->GetName(),It->GetRelocationMask());
  return false;
 }
 TGuardValue<bool> Writing(bWriting, true);
 auto* GI = GetGameInstance();
 auto* Save = CaptureSnapshot(GI->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
  GI->GetSubsystem<UPokeMonsterInventorySubsystem>(), this,
  GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>(), GI->GetSubsystem<UPokeMonsterQuestSubsystem>(), GI->GetSubsystem<UPokeMonsterWorldClock>());
 if (!Save || !Save->PlayerLocation.IsValid())
 { LastStorageMessage = TEXT("Spielerposition oder Spieldaten sind nicht speicherbar."); return false; }
#if WITH_EDITOR
 if (IsPIEMemoryPreviewActive())
 {
  TArray<uint8> Bytes;
  if (!UGameplayStatics::SaveGameToMemory(Save, Bytes) || Bytes.IsEmpty()) return false;
  (bRecovery ? PIEMemoryRecovery : PIEMemorySave) = MoveTemp(Bytes);
  LastStorageMessage = bRecovery ? TEXT("Automatischer Stand im Test-RAM gespeichert.") : TEXT("Spiel im Test-RAM gespeichert.");
  return true;
 }
#endif
 const bool Saved = SaveSnapshotToSlot(Save, SlotName(bRecovery));
 LastStorageMessage = Saved ? (bRecovery ? TEXT("Automatischer Stand gespeichert; manueller Spielstand unverändert.")
  : TEXT("Spiel gespeichert.")) : TEXT("Speichern fehlgeschlagen. Vorheriger Spielstand bleibt erhalten.");
 UE_LOG(LogPokeMonsterSave, Display, TEXT("%s [%s]"), *LastStorageMessage, *SlotName(bRecovery));
 return Saved;
}

bool UPokeMonsterSaveSubsystem::HasSlot(bool bRecovery) const
{
 if (!APokeMonsterGameMode::AllowsPersistentGameplay(GetWorld())) return false;
#if WITH_EDITOR
 if (IsPIEMemoryPreviewActive()) return !(bRecovery ? PIEMemoryRecovery : PIEMemorySave).IsEmpty();
#endif
 return UGameplayStatics::DoesSaveGameExist(SlotName(bRecovery), 0);
}
bool UPokeMonsterSaveSubsystem::HasSaveGame() const { return HasSlot(false); }
bool UPokeMonsterSaveSubsystem::HasRecoveryGame() const { return HasSlot(true); }
bool UPokeMonsterSaveSubsystem::LoadGame() { return ReadGame(false); }
bool UPokeMonsterSaveSubsystem::LoadRecoveryGame() { return ReadGame(true); }

bool UPokeMonsterSaveSubsystem::ReadGame(bool bRecovery)
{
 if (!CanAccessWorldState() || !HasSlot(bRecovery))
 { LastStorageMessage = TEXT("Laden derzeit nicht möglich oder kein Spielstand vorhanden."); return false; }
 UPokeMonsterSaveGame* Save = nullptr;
#if WITH_EDITOR
 if (IsPIEMemoryPreviewActive()) Save = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(
  bRecovery ? PIEMemoryRecovery : PIEMemorySave));
 else
#endif
 Save = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(SlotName(bRecovery), 0));
 auto* GI = GetGameInstance();
 if (!Save || !RestoreSnapshot(Save, GI->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
  GI->GetSubsystem<UPokeMonsterInventorySubsystem>(), GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>(),
  GI->GetSubsystem<UPokeMonsterQuestSubsystem>(), true))
 { LastStorageMessage = TEXT("Spielstand ungültig; laufende Daten bleiben erhalten."); return false; }
 PendingLocation = Save->SaveVersion >= 9 ? Save->PlayerLocation : FPokeMonsterSavedPlayerLocation();
 bool bFallback = !PendingLocation.IsValid() || !MapAvailable(PendingLocation.MapPackage);
 bUsingPositionFallback = bFallback;
 if (bFallback)
 {
  PendingLocation = {};
  if (Save->ActiveCheckpoint.IsValid() && MapAvailable(Save->ActiveCheckpoint.MapPackage))
  {
   PendingLocation.bHasPosition = true; PendingLocation.MapPackage = Save->ActiveCheckpoint.MapPackage;
   PendingLocation.Location = Save->ActiveCheckpoint.Location; PendingLocation.Rotation = Save->ActiveCheckpoint.Rotation;
   PendingLocation.FacingDirection = Save->ActiveCheckpoint.Rotation.Vector().GetSafeNormal2D();
   if (PendingLocation.MapPackage == UPokeMonsterCheckpointSubsystem::GetMapPackage(GetWorld()))
    InteriorContext(GetWorld(), PendingLocation);
  }
 }
 PendingLoad = Save;
 LoadAttempts = 0;
 LastStorageMessage = bFallback ? TEXT("Alte/ungültige Position: sicherer Rückkehrpunkt wird geprüft.") : TEXT("Spielstand wird geladen …");
 if (PendingLocation.IsValid() && PendingLocation.MapPackage != UPokeMonsterCheckpointSubsystem::GetMapPackage(GetWorld()))
 {
  if (auto* PC = GetWorld()->GetFirstPlayerController())
   if (auto* P = Cast<APokeMonsterPlayerCharacter>(PC->GetPawn())) P->SetOverworldInputLocked(true);
  UGameplayStatics::OpenLevel(GetWorld(), PendingLocation.MapPackage);
  return true; // Completion and input release occur only in the destination world.
 }
 return CompleteLoad(GetWorld());
}

void UPokeMonsterSaveSubsystem::SynchronizeRestoredPlayer(APokeMonsterPlayerCharacter* Player)
{
 if (!Player) return;
 auto* Move = Player->GetCharacterMovement(); Move->StopMovementImmediately(); Move->bJustTeleported = true;
 for (TActorIterator<APokeMonsterBuildingCutaway> It(Player->GetWorld()); It; ++It) It->SynchronizeViewerAfterLoad();
 if (auto* PC = Player->GetController())
 {
  PC->SetControlRotation(Player->GetActorRotation());
  if (auto* Controller = Cast<APlayerController>(PC))
  {
   Controller->SetViewTarget(Player);
   if (Controller->PlayerCameraManager) Controller->PlayerCameraManager->SetGameCameraCutThisFrame();
  }
 }
}

bool UPokeMonsterSaveSubsystem::CompleteLoad(UWorld* World)
{
 auto* GI = GetGameInstance();
 auto* PC = World ? World->GetFirstPlayerController() : nullptr;
 auto* Player = PC ? Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()) : nullptr;
 if (!PendingLoad || !GI || !Player) return false;
 FPokeMonsterSavedPlayerLocation Destination;
 bool bPlacedTarget = PendingLocation.IsValid() && ResolvePlacement(Player, PendingLocation, Destination);
 if (!bPlacedTarget && PendingLoad->ActiveCheckpoint.IsValid()
  && PendingLoad->ActiveCheckpoint.MapPackage == UPokeMonsterCheckpointSubsystem::GetMapPackage(World))
 {
  FPokeMonsterSavedPlayerLocation Fallback;
  Fallback.bHasPosition = true; Fallback.MapPackage = PendingLoad->ActiveCheckpoint.MapPackage;
  Fallback.Location = PendingLoad->ActiveCheckpoint.Location; Fallback.Rotation = PendingLoad->ActiveCheckpoint.Rotation;
  Fallback.FacingDirection = Fallback.Rotation.Vector().GetSafeNormal2D();
  InteriorContext(World, Fallback);
  bPlacedTarget = ResolvePlacement(Player, Fallback, Destination);
 }
 if (!bPlacedTarget)
 {
  for (TActorIterator<APlayerStart> It(World); It; ++It)
  {
   FPokeMonsterSavedPlayerLocation Fallback;
   Fallback.bHasPosition = true; Fallback.MapPackage = UPokeMonsterCheckpointSubsystem::GetMapPackage(World);
   Fallback.Location = It->GetActorLocation(); Fallback.Rotation = It->GetActorRotation();
   Fallback.FacingDirection = Fallback.Rotation.Vector().GetSafeNormal2D(); InteriorContext(World, Fallback);
   if (ResolvePlacement(Player, Fallback, Destination)) { bPlacedTarget = true; break; }
  }
 }
 if (!bPlacedTarget)
 { LastStorageMessage = TEXT("Kein sicherer Ladeort; Spieldaten unverändert."); ClearPendingLoad(); return false; }
 const FTransform Previous = Player->GetActorTransform();
 if (!Player->TeleportTo(Destination.Location, Destination.Rotation, false, true))
 { LastStorageMessage = TEXT("Platzieren fehlgeschlagen; Spieldaten unverändert."); ClearPendingLoad(); return false; }
 const bool Loaded = RestoreSnapshot(PendingLoad, GI->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
  GI->GetSubsystem<UPokeMonsterInventorySubsystem>(), GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>(),
  GI->GetSubsystem<UPokeMonsterQuestSubsystem>(), false, GI->GetSubsystem<UPokeMonsterWorldClock>());
 if (!Loaded) Player->SetActorTransform(Previous, false, nullptr, ETeleportType::TeleportPhysics);
 SynchronizeRestoredPlayer(Player);
 if (Loaded) Player->RestoreSavedFacing(Destination.FacingDirection);
 LastStorageMessage = Loaded ? (bUsingPositionFallback ? TEXT("Spielstand am sicheren Rückkehrpunkt geladen.") : Destination.Location.Equals(PendingLocation.Location, .01f)
  ? TEXT("Spielstand und Position geladen.") : TEXT("Spielstand an sicherem Ersatzort geladen."))
  : TEXT("Laden abgelehnt; vorherige Daten bleiben erhalten.");
 UE_LOG(LogPokeMonsterSave, Display, TEXT("%s"), *LastStorageMessage);
 ClearPendingLoad();
 return Loaded;
}

void UPokeMonsterSaveSubsystem::HandlePostLoadMap(UWorld* World)
{
 if (!PendingLoad || !World || World->GetGameInstance() != GetGameInstance()) return;
 if (PendingLocation.IsValid() && PendingLocation.MapPackage != UPokeMonsterCheckpointSubsystem::GetMapPackage(World))
 { LastStorageMessage = TEXT("Zielwelt nicht geladen; Spieldaten unverändert."); ClearPendingLoad(); return; }
 if (bUsingPositionFallback && PendingLocation.IsValid()) InteriorContext(World, PendingLocation);
 // PlayerController BeginPlay is not guaranteed to have possessed its pawn at PostLoad.
 World->GetTimerManager().SetTimer(LoadTimer, FTimerDelegate::CreateWeakLambda(this, [this, World]()
 {
  if (CompleteLoad(World)) return;
  if (!PendingLoad) return;
  if (++LoadAttempts >= 30) { LastStorageMessage = TEXT("Ladevorgang ohne Spielfigur abgebrochen."); ClearPendingLoad(); }
  else HandlePostLoadMap(World);
 }), .1f, false);
}

void UPokeMonsterSaveSubsystem::HandleTravelFailure(UWorld* World, ETravelFailure::Type, const FString& Error)
{
 if (!PendingLoad || (World && World->GetGameInstance() != GetGameInstance())) return;
 LastStorageMessage = TEXT("Weltwechsel fehlgeschlagen; laufende Spieldaten unverändert.");
 UE_LOG(LogPokeMonsterSave, Display, TEXT("Load travel rejected: %s"), *Error);
 ClearPendingLoad();
}

void UPokeMonsterSaveSubsystem::ClearPendingLoad()
{
 if (GetWorld())
 {
  GetWorld()->GetTimerManager().ClearTimer(LoadTimer);
  if (auto* PC = Cast<APokeMonsterOverworldPlayerController>(GetWorld()->GetFirstPlayerController()))
   if (auto* Player = Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()))
    Player->SetOverworldInputLocked(PC->IsMenuOpen() || PC->GetEvolutionWidget() != nullptr);
 }
 PendingLoad = nullptr; PendingLocation = {}; LoadAttempts = 0;
}

bool UPokeMonsterSaveSubsystem::DeleteDevSave()
{
    if (!APokeMonsterGameMode::AllowsPersistentGameplay(GetWorld())) return false;
#if WITH_EDITOR
    if (IsPIEMemoryPreviewActive() || !IsolatedPIESlot.IsEmpty()) return false;
#endif
	return !HasSaveGame() || UGameplayStatics::DeleteGameInSlot(DevSlotName, 0);
}

bool UPokeMonsterSaveSubsystem::RunDevRoundTripTest()
{
    if (!APokeMonsterGameMode::AllowsPersistentGameplay(GetWorld())) return false;
	if (HasSaveGame())
	{
		UE_LOG(LogPokeMonsterSave, Warning, TEXT("Round trip refused: existing Dev save would be overwritten."));
		return false;
	}
	UGameInstance* Instance = GetGameInstance();
	auto* Encounter = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	auto* Inventory = Instance ? Instance->GetSubsystem<UPokeMonsterInventorySubsystem>() : nullptr;
	if (!Encounter || !Inventory || Encounter->IsEncounterActive() || !Encounter->EnsureDevPlayerParty()) return false;
	auto* Capture = LoadObject<UPokeMonsterItemData>(nullptr,
		TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem"));
	auto* Healing = LoadObject<UPokeMonsterItemData>(nullptr,
		TEXT("/Game/Data/Items/DA_TestHealingItem.DA_TestHealingItem"));
	if (!Capture || !Healing) return false;
	TArray<FPokeMonsterCreatureInstance> Team = Encounter->GetPlayerParty();
	if (Team.IsEmpty() || !Team[0].ConsumeMovePP(0, 2)) return false;
	Team[0].CurrentHP = FMath::Max(1, Team[0].CurrentHP - 7);
	if (!Team[0].AddExperience(11).bSucceeded) return false;
	const FGuid ExpectedId = Team[0].InstanceId;
	const int32 ExpectedHP = Team[0].CurrentHP;
	const int32 ExpectedPP = Team[0].GetMoveSlots()[0].GetCurrentPP();
	const int64 ExpectedXP = Team[0].Experience;
	const int32 ExpectedLevel = Team[0].Level;
	if (!Encounter->RestorePersistentState(Team, {TEXT("Dev_SaveTrainer")}, {TEXT("Dev_VisibleWild")})) return false;
	if (!Inventory->RestoreStacks({}) || !Inventory->AddItem(Capture, 3)
		|| !Inventory->AddItem(Healing, 2) || !SaveCurrentGame()) return false;
	if (!Encounter->RestorePersistentState({}, {}, {}) || !Inventory->RestoreStacks({})) return false;
	const bool bCleared = Encounter->GetPlayerParty().IsEmpty() && Inventory->GetStacks().IsEmpty()
		&& !Encounter->IsTrainerDefeated(TEXT("Dev_SaveTrainer"));
	if (!bCleared || !LoadGame()) return false;
	const auto& LoadedTeam = Encounter->GetPlayerParty();
	const bool bPassed = LoadedTeam.Num() == Team.Num() && LoadedTeam[0].InstanceId == ExpectedId
		&& LoadedTeam[0].Level == ExpectedLevel && LoadedTeam[0].Experience == ExpectedXP
		&& LoadedTeam[0].CurrentHP == ExpectedHP
		&& LoadedTeam[0].GetMoveSlots()[0].GetCurrentPP() == ExpectedPP
		&& Inventory->GetQuantity(Capture) == 3 && Inventory->GetQuantity(Healing) == 2
		&& Encounter->IsTrainerDefeated(TEXT("Dev_SaveTrainer"))
		&& Encounter->IsEncounterCompleted(TEXT("Dev_VisibleWild"));
	UE_LOG(LogPokeMonsterSave, Display,
		TEXT("PIE save round trip %s: team=%d, HP=%d, XP=%lld, PP=%d, capture=%d, healing=%d, trainer=%s, encounter=%s"),
		bPassed ? TEXT("PASS") : TEXT("FAIL"), LoadedTeam.Num(),
		LoadedTeam.IsEmpty() ? -1 : LoadedTeam[0].CurrentHP,
		LoadedTeam.IsEmpty() ? -1LL : LoadedTeam[0].Experience,
		LoadedTeam.IsEmpty() ? -1 : LoadedTeam[0].GetMoveSlots()[0].GetCurrentPP(),
		Inventory->GetQuantity(Capture), Inventory->GetQuantity(Healing),
		Encounter->IsTrainerDefeated(TEXT("Dev_SaveTrainer")) ? TEXT("yes") : TEXT("no"),
		Encounter->IsEncounterCompleted(TEXT("Dev_VisibleWild")) ? TEXT("yes") : TEXT("no"));
	return bPassed;
}

void UPokeMonsterSaveSubsystem::Deinitialize()
{
 FCoreUObjectDelegates::PostLoadMapWithWorld.Remove(PostLoadMapHandle);
 if (GEngine) GEngine->OnTravelFailure().Remove(TravelFailureHandle);
 ClearPendingLoad();
#if WITH_EDITOR
 PIEOriginalSnapshot.Reset(); PIEMemorySave.Reset(); PIEMemoryRecovery.Reset();
 IsolatedPIESlot.Reset();
#endif
 Super::Deinitialize();
}
#if WITH_EDITOR
bool UPokeMonsterSaveSubsystem::BeginPIEMemoryPreview()
{
    if (IsPIEMemoryPreviewActive() || !IsolatedPIESlot.IsEmpty()) return false;
    auto* GI = GetGameInstance();
    if (!GI || !GetWorld() || GetWorld()->WorldType != EWorldType::PIE) return false;
    auto* Snapshot = CaptureSnapshot(GI->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
        GI->GetSubsystem<UPokeMonsterInventorySubsystem>(), this,
        GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>(), GI->GetSubsystem<UPokeMonsterQuestSubsystem>(), GI->GetSubsystem<UPokeMonsterWorldClock>());
    TArray<uint8> Bytes;
    if (!Snapshot || !UGameplayStatics::SaveGameToMemory(Snapshot, Bytes) || Bytes.IsEmpty()) return false;
    PIEOriginalSnapshot = Bytes;
    PIEMemorySave = MoveTemp(Bytes);
    return true;
}
bool UPokeMonsterSaveSubsystem::EndPIEMemoryPreview()
{
    if (!IsPIEMemoryPreviewActive() || !GetWorld() || GetWorld()->WorldType != EWorldType::PIE) return false;
    auto* GI = GetGameInstance();
    auto* Snapshot = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(PIEOriginalSnapshot));
    if (!GI || !Snapshot || !RestoreSnapshot(Snapshot, GI->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
        GI->GetSubsystem<UPokeMonsterInventorySubsystem>(), GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>(),
        GI->GetSubsystem<UPokeMonsterQuestSubsystem>(), false, GI->GetSubsystem<UPokeMonsterWorldClock>())) return false;
    // Keep protection active until the entire original session has restored successfully.
    PIEOriginalSnapshot.Reset();
    PIEMemorySave.Reset();
    PIEMemoryRecovery.Reset();
    return true;
}
#endif
