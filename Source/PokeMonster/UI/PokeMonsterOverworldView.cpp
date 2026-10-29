#include "PokeMonsterOverworldView.h"
#include "../Moves/PokeMonsterMoveData.h"

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
		case EPokeMonsterItemCategory::Capture: return FText::FromString(TEXT("Pokébälle"));
		case EPokeMonsterItemCategory::Healing: return FText::FromString(TEXT("Medizin"));
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
			Row.InstanceId = Creature.InstanceId;
			Row.Level = Creature.Level;
   Row.Experience=FPokeMonsterExperienceView::FromCreature(Creature);
			Row.CurrentHP = Creature.CurrentHP;
			Row.MaxHP = Creature.GetMaxHP();
			Row.bKnockedOut = Creature.CurrentHP <= 0;
   Row.bPendingLearning=!Creature.PendingMoves.IsEmpty();
   for(const auto& Slot:Creature.GetMoveSlots())Row.ActiveMoves.Add(Slot.GetMove());
   static const TCHAR* Types[]={TEXT("—"),TEXT("Normal"),TEXT("Feuer"),TEXT("Wasser"),TEXT("Elektro"),TEXT("Pflanze"),TEXT("Eis"),TEXT("Kampf"),TEXT("Gift"),TEXT("Boden"),TEXT("Flug"),TEXT("Psycho"),TEXT("Käfer"),TEXT("Gestein"),TEXT("Geist"),TEXT("Drache"),TEXT("Unlicht"),TEXT("Stahl"),TEXT("???")};
   for(const auto& Known:Creature.GetLearnedMoves())
   {
    const auto* Move=Known.GetMove().LoadSynchronous();if(!Move)continue;
    auto& M=Row.Repertoire.AddDefaulted_GetRef();M.Move=Known.GetMove();M.Name=Move->GetPlayerFacingName();
    M.Type=FText::FromString(uint8(Move->Type)<UE_ARRAY_COUNT(Types)?Types[uint8(Move->Type)]:TEXT("?"));
    M.Power=Move->BasePower;M.Accuracy=Move->Accuracy;M.CurrentPP=Known.GetCurrentPP();M.MaxPP=Known.GetMaxPP();
    M.ActiveSlot=Row.ActiveMoves.IndexOfByKey(M.Move);
    const FName Effect=Move->Effect.EffectId;
    const bool Supported=Move->IsConfigured() && (!Move->Effects.IsEmpty() || Effect==TEXT("UserLevelDamage") || Effect==NAME_None || Effect==TEXT("AttackDown") || Effect==TEXT("DefenseDown") || Effect==TEXT("DefenseUp") || Effect==TEXT("LeechSeed") || Effect==TEXT("DrainHalf") || Effect==TEXT("Burn") || Effect==TEXT("SpeedDown"));
    M.Effect=FText::FromString(!Supported || (Move->Category==EPokeMonsterMoveCategory::Status && Effect==NAME_None && Move->Effects.IsEmpty())
     ? TEXT("Wirkung noch unvollständig") : Move->Effect.Description.IsEmpty()
      ? Move->Category==EPokeMonsterMoveCategory::Status?TEXT("Statuswirkung"):TEXT("Direkter Schaden") : *Move->Effect.Description.ToString());
   }
		}
	}
	if (IsValid(Inventory))
	{
  View.Notification=Inventory->GetNotification();
		for (const FPokeMonsterInventoryStack& Stack : Inventory->GetStacks())
		{
			const UPokeMonsterItemData* Item = Stack.Item.LoadSynchronous();
			if (!IsValid(Item) || Stack.Quantity <= 0) continue;
			if(auto* Existing=View.Inventory.FindByPredicate([&](const auto& R){return R.Item==Stack.Item;})){Existing->Quantity+=Stack.Quantity;continue;}
			FPokeMonsterOverworldItemRow& Row = View.Inventory.AddDefaulted_GetRef();
			Row.Item = Stack.Item;
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
