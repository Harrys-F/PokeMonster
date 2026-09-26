#include "PokeMonsterSaveSubsystem.h"

#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Kismet/GameplayStatics.h"

DEFINE_LOG_CATEGORY_STATIC(LogPokeMonsterSave, Log, All);

const FString UPokeMonsterSaveSubsystem::DevSlotName = TEXT("PokeMonster_Dev");

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

	bool DecodeCreature(const FPokeMonsterSavedCreature& Saved, FPokeMonsterCreatureInstance& Out)
	{
		auto* Species = ResolveAsset<UPokeMonsterCreatureSpeciesData>(Saved.SpeciesId, TEXT("CreatureSpecies"));
		if (!Species || Saved.Moves.Num() != FPokeMonsterCreatureInstance::MoveSlotCount) return false;
		Out = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, Saved.Level);
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
		return Out.RestoreIndividualState(Saved.InstanceId, Saved.Level, Saved.Experience,
			Saved.CurrentHP, Slots);
	}
}

UPokeMonsterSaveGame* UPokeMonsterSaveSubsystem::CaptureSnapshot(
	const UPokeMonsterEncounterSubsystem* Encounter, const UPokeMonsterInventorySubsystem* Inventory, UObject* Outer)
{
	if (!IsValid(Encounter) || !IsValid(Inventory) || Encounter->IsEncounterActive()) return nullptr;
	if (Encounter->GetPlayerParty().Num() > 6) return nullptr;
	auto* Save = NewObject<UPokeMonsterSaveGame>(Outer ? Outer : GetTransientPackage());
	for (const FPokeMonsterCreatureInstance& Creature : Encounter->GetPlayerParty())
	{
		const auto* Species = Creature.Species.LoadSynchronous();
		FPokeMonsterCreatureInstance Validated = Creature;
		if (!Creature.IsValid() || !IsValid(Species)
			|| !Validated.RestoreIndividualState(Creature.InstanceId, Creature.Level, Creature.Experience,
				Creature.CurrentHP, Creature.GetMoveSlots())) return nullptr;
		FPokeMonsterSavedCreature& Entry = Save->PlayerTeam.AddDefaulted_GetRef();
		Entry.InstanceId = Creature.InstanceId;
		Entry.SpeciesId = Species->GetPrimaryAssetId();
		Entry.Level = Creature.Level;
		Entry.Experience = Creature.Experience;
		Entry.CurrentHP = Creature.CurrentHP;
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
	return Save;
}

bool UPokeMonsterSaveSubsystem::RestoreSnapshot(const UPokeMonsterSaveGame* Save,
	UPokeMonsterEncounterSubsystem* Encounter, UPokeMonsterInventorySubsystem* Inventory)
{
	if (!IsValid(Save) || !IsValid(Encounter) || !IsValid(Inventory) || Encounter->IsEncounterActive()) return false;
	// Version 1 is the only understood schema. Future migrations belong here before decoding.
	if (Save->SaveVersion != UPokeMonsterSaveGame::CurrentVersion)
	{
		UE_LOG(LogPokeMonsterSave, Error, TEXT("Unsupported save version %d (expected %d)."),
			Save->SaveVersion, UPokeMonsterSaveGame::CurrentVersion);
		return false;
	}
	if (Save->PlayerTeam.Num() > 6) return false;
	TArray<FPokeMonsterCreatureInstance> Team;
	TSet<FGuid> Seen;
	for (const FPokeMonsterSavedCreature& Saved : Save->PlayerTeam)
	{
		FPokeMonsterCreatureInstance Creature;
		if (!DecodeCreature(Saved, Creature) || Seen.Contains(Creature.InstanceId))
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
	const TArray<FPokeMonsterInventoryStack> PreviousStacks = Inventory->GetStacks();
	if (!Inventory->RestoreStacks(Stacks)) return false;
	if (!Encounter->RestorePersistentState(Team, Save->DefeatedTrainerIds, Save->CompletedEncounterIds))
	{
		Inventory->RestoreStacks(PreviousStacks);
		return false;
	}
	return true;
}

bool UPokeMonsterSaveSubsystem::SaveCurrentGame()
{
	UGameInstance* Instance = GetGameInstance();
	if (!Instance) return false;
	UPokeMonsterSaveGame* Save = CaptureSnapshot(Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
		Instance->GetSubsystem<UPokeMonsterInventorySubsystem>(), this);
	if (!Save) return false;
	const bool bSaved = UGameplayStatics::SaveGameToSlot(Save, DevSlotName, 0);
	if (bSaved) { UE_LOG(LogPokeMonsterSave, Display, TEXT("Save written: %s"), *DevSlotName); }
	else { UE_LOG(LogPokeMonsterSave, Error, TEXT("Save failed: %s"), *DevSlotName); }
	return bSaved;
}

bool UPokeMonsterSaveSubsystem::LoadGame()
{
	if (!HasSaveGame())
	{
		UE_LOG(LogPokeMonsterSave, Warning, TEXT("No save in slot %s."), *DevSlotName);
		return false;
	}
	UGameInstance* Instance = GetGameInstance();
	auto* Save = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(DevSlotName, 0));
	if (!Instance || !Save)
	{
		UE_LOG(LogPokeMonsterSave, Error, TEXT("Save slot %s is unreadable or has the wrong class."), *DevSlotName);
		return false;
	}
	const bool bLoaded = RestoreSnapshot(Save, Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
		Instance->GetSubsystem<UPokeMonsterInventorySubsystem>());
	if (bLoaded) { UE_LOG(LogPokeMonsterSave, Display, TEXT("Load completed: %s"), *DevSlotName); }
	else { UE_LOG(LogPokeMonsterSave, Error, TEXT("Load rejected: %s"), *DevSlotName); }
	return bLoaded;
}

bool UPokeMonsterSaveSubsystem::HasSaveGame() const
{
	return UGameplayStatics::DoesSaveGameExist(DevSlotName, 0);
}

bool UPokeMonsterSaveSubsystem::DeleteDevSave()
{
	return !HasSaveGame() || UGameplayStatics::DeleteGameInSlot(DevSlotName, 0);
}

bool UPokeMonsterSaveSubsystem::RunDevRoundTripTest()
{
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
