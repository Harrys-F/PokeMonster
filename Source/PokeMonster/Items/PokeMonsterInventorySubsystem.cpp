#include "PokeMonsterInventorySubsystem.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Engine/GameInstance.h"

void UPokeMonsterInventorySubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	// Temporary development stock, granted once per GameInstance, not per encounter.
	const auto* Item = LoadObject<UPokeMonsterItemData>(nullptr, TEXT("/Game/Data/Items/DA_TestCaptureItem.DA_TestCaptureItem"));
	if (IsValid(Item)) AddItem(Item, 5);
}

int32 UPokeMonsterInventorySubsystem::GetQuantity(const UPokeMonsterItemData* Item) const
{
	if (!IsValid(Item)) return 0;
	int64 Total = 0;
	for (const auto& Stack : Stacks)
		if (Stack.Item.ToSoftObjectPath() == FSoftObjectPath(Item)) Total += Stack.Quantity;
	return int32(FMath::Min<int64>(Total, MAX_int32));
}

bool UPokeMonsterInventorySubsystem::HasItem(const UPokeMonsterItemData* Item, int32 Quantity) const
{
	return Quantity > 0 && GetQuantity(Item) >= Quantity;
}

bool UPokeMonsterInventorySubsystem::AddItem(const UPokeMonsterItemData* Item, int32 Quantity)
{
	if (!IsValid(Item) || !Item->IsConfigured() || Quantity <= 0
		|| int64(GetQuantity(Item)) + Quantity > MAX_int32) return false;
	int32 Remaining = Quantity;
	for (auto& Stack : Stacks)
	{
		if (Stack.Item.ToSoftObjectPath() != FSoftObjectPath(Item) || Stack.Quantity >= Item->GetMaxStackSize()) continue;
		const int32 Added = FMath::Min(Remaining, Item->GetMaxStackSize() - Stack.Quantity);
		Stack.Quantity += Added;
		Remaining -= Added;
		if (Remaining == 0) return true;
	}
	while (Remaining > 0)
	{
		auto& Stack = Stacks.AddDefaulted_GetRef();
		Stack.Item = const_cast<UPokeMonsterItemData*>(Item);
		Stack.Quantity = FMath::Min(Remaining, Item->GetMaxStackSize());
		Remaining -= Stack.Quantity;
	}
	return true;
}

bool UPokeMonsterInventorySubsystem::RemoveItem(const UPokeMonsterItemData* Item, int32 Quantity)
{
	if (!HasItem(Item, Quantity)) return false;
	int32 Remaining = Quantity;
	for (int32 Index = Stacks.Num() - 1; Index >= 0 && Remaining > 0; --Index)
	{
		if (Stacks[Index].Item.ToSoftObjectPath() != FSoftObjectPath(Item)) continue;
		const int32 Taken = FMath::Min(Remaining, Stacks[Index].Quantity);
		Stacks[Index].Quantity -= Taken;
		Remaining -= Taken;
		if (Stacks[Index].Quantity == 0) Stacks.RemoveAt(Index);
	}
	return true;
}

bool UPokeMonsterInventorySubsystem::RestoreStacks(const TArray<FPokeMonsterInventoryStack>& SavedStacks)
{
	int64 Total = 0;
	for (const auto& Stack : SavedStacks)
	{
		const auto* Item = Stack.Item.LoadSynchronous();
		if (!IsValid(Item) || !Item->IsConfigured() || Stack.Quantity < 1
			|| Stack.Quantity > Item->GetMaxStackSize()) return false;
		Total += Stack.Quantity;
		if (Total > MAX_int32) return false;
	}
	Stacks = SavedStacks;
	return true;
}

bool UPokeMonsterInventorySubsystem::UseHealingItem(const UPokeMonsterItemData* Item,
	FPokeMonsterCreatureInstance& Creature)
{
	if (!IsValid(Item) || !Item->IsConfigured() || Item->GetCategory() != EPokeMonsterItemCategory::Healing
		|| !Item->CanUseInOverworld() || !Creature.IsValid() || Creature.CurrentHP <= 0
		|| Creature.CurrentHP >= Creature.GetMaxHP() || !HasItem(Item)) return false;
	if (const auto* GameInstance = GetGameInstance())
		if (const auto* Encounter = GameInstance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
			if (Encounter->IsEncounterActive()) return false;
	if (!RemoveItem(Item, 1)) return false;
	Creature.CurrentHP = int32(FMath::Min<int64>(Creature.GetMaxHP(), int64(Creature.CurrentHP) + Item->GetHealAmount()));
	return true;
}
