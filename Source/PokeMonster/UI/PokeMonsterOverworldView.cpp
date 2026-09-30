#include "PokeMonsterOverworldView.h"

#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"

namespace
{
	FText CategoryName(const EPokeMonsterItemCategory Category)
	{
		switch (Category)
		{
		case EPokeMonsterItemCategory::Capture: return FText::FromString(TEXT("Fangen"));
		case EPokeMonsterItemCategory::Healing: return FText::FromString(TEXT("Heilung"));
		case EPokeMonsterItemCategory::Battle: return FText::FromString(TEXT("Kampf"));
		case EPokeMonsterItemCategory::Evolution: return FText::FromString(TEXT("Entwicklung"));
		case EPokeMonsterItemCategory::KeyItem: return FText::FromString(TEXT("Wichtig"));
		default: return FText::FromString(TEXT("Sonstiges"));
		}
	}
}

FPokeMonsterOverworldView FPokeMonsterOverworldViewBuilder::Build(
	const UPokeMonsterEncounterSubsystem* Encounter, const UPokeMonsterInventorySubsystem* Inventory,
	const UPokeMonsterQuestSubsystem* Quests)
{
	FPokeMonsterOverworldView View;
	if (IsValid(Encounter))
	{
		for (const FPokeMonsterCreatureInstance& Creature : Encounter->GetPlayerParty())
		{
			if (View.Team.Num() == 6) break;
			FPokeMonsterOverworldTeamRow& Row = View.Team.AddDefaulted_GetRef();
			const UPokeMonsterCreatureSpeciesData* Species = Creature.Species.LoadSynchronous();
			Row.Name = IsValid(Species) ? Species->GetDisplayName() : FText::FromString(TEXT("Unbekannte Kreatur"));
			Row.Level = Creature.Level;
			Row.CurrentHP = Creature.CurrentHP;
			Row.MaxHP = Creature.GetMaxHP();
			Row.bKnockedOut = Creature.CurrentHP <= 0;
		}
	}
	if (IsValid(Inventory))
	{
		for (const FPokeMonsterInventoryStack& Stack : Inventory->GetStacks())
		{
			const UPokeMonsterItemData* Item = Stack.Item.LoadSynchronous();
			if (!IsValid(Item) || Stack.Quantity <= 0) continue;
			FPokeMonsterOverworldItemRow& Row = View.Inventory.AddDefaulted_GetRef();
			Row.Name = Item->GetDisplayName();
			Row.Category = CategoryName(Item->GetCategory());
			Row.Quantity = Stack.Quantity;
		}
	}
	if (IsValid(Quests))
		if (const auto* Quest = Quests->GetActiveMainQuest())
		{
			const int32 Step = Quests->GetCurrentStep(Quest->InternalId);
			if (Quest->Objectives.IsValidIndex(Step))
			{
				View.ActiveQuestName = Quest->DisplayName;
				View.ActiveQuestObjective = Quest->Objectives[Step].Description;
			}
		}
	return View;
}
