#include "PokeMonsterInventorySubsystem.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Engine/GameInstance.h"
#include "../Save/PokeMonsterSaveSubsystem.h"

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
		|| int64(GetQuantity(Item)) + Quantity > MAX_int32 || MaxStackSlots<0) return false;
 int64 Total=Quantity;for(const auto& S:Stacks)Total+=S.Quantity;if(Total>MAX_int32)return false;
	int64 Space=0;for(const auto& Stack:Stacks)if(Stack.Item.ToSoftObjectPath()==FSoftObjectPath(Item))Space+=Item->GetMaxStackSize()-Stack.Quantity;
 const int64 Needed=FMath::DivideAndRoundUp(FMath::Max<int64>(0,int64(Quantity)-Space),int64(Item->GetMaxStackSize()));
 // A single malformed/absurd grant must not allocate millions of stacks. This is a
 // transaction allocation guard, not a new gameplay capacity or a save migration.
 constexpr int64 MaxNewStacksPerOperation=65536;
 if(Needed>MaxNewStacksPerOperation || Needed>MAX_int32-Stacks.Num() || (MaxStackSlots>0 && Needed>FMath::Max(0,MaxStackSlots-Stacks.Num())))return false;
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
 FPokeMonsterCreatureInstance& Creature,int32 MoveSlot)
{
 if(!IsValid(Item)||!Item->CanUseInOverworld()||!HasItem(Item))return false;
 if(GetGameInstance())if(auto* E=GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>())if(E->IsEncounterActive())return false;
 auto Preview=Creature;if(!Item->ApplyMedicine(Preview,MoveSlot))return false;
 if(Item->IsConsumedOnUse()&&!RemoveItem(Item,1))return false;
 Creature=MoveTemp(Preview);return true;
}

FText UPokeMonsterInventorySubsystem::GetNotification() const
{ return FPlatformTime::Seconds()<NotificationUntil?Notification:FText::GetEmpty(); }
void UPokeMonsterInventorySubsystem::Notify(const FString& Message)
{ Notification=FText::FromString(Message);NotificationUntil=FPlatformTime::Seconds()+6.; }

bool UPokeMonsterInventorySubsystem::DiscardItem(const UPokeMonsterItemData* Item,int32 Quantity)
{
 auto* GI=GetGameInstance();auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 auto* Save=GI?GI->GetSubsystem<UPokeMonsterSaveSubsystem>():nullptr;
 if(bTransactionActive||!E||E->IsEncounterActive()||!Save||!Item||!Item->CanDiscard()||!HasItem(Item,Quantity))return false;
 TGuardValue<bool> Guard(bTransactionActive,true);const auto Before=Stacks;
 if(!RemoveItem(Item,Quantity))return false;
 if(!Save->SaveProgressGame()){Stacks=Before;Notify(TEXT("Speicherfehler · nichts weggeworfen"));return false;}
 Notify(FString::Printf(TEXT("%s × %d weggeworfen"),*Item->GetDisplayName().ToString(),Quantity));return true;
}

bool UPokeMonsterInventorySubsystem::CollectItem(const UPokeMonsterItemData* Item,int32 Quantity,FName SourceId)
{
 auto* GI=GetGameInstance();auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 auto* Save=GI?GI->GetSubsystem<UPokeMonsterSaveSubsystem>():nullptr;
 if(bTransactionActive||!E||E->IsEncounterActive()||!Save||SourceId.IsNone()||E->IsEncounterCompleted(SourceId))return false;
 TGuardValue<bool> Guard(bTransactionActive,true);const auto Before=Stacks;
 if(!AddItem(Item,Quantity)){Notify(TEXT("Gegenstand nicht aufgenommen · Inventar voll oder ungültig"));return false;}
 E->MarkEncounterCompleted(SourceId);
 if(!Save->SaveProgressGame()){Stacks=Before;E->UnmarkEncounterCompleted(SourceId);Notify(TEXT("Speicherfehler · Gegenstand bleibt erhalten"));return false;}
 Notify(FString::Printf(TEXT("%s × %d erhalten!"),*Item->GetDisplayName().ToString(),Quantity));return true;
}
