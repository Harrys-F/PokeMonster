#include "PokeMonsterBattlePresentationPlan.h"

TArray<FPokeMonsterPresentationAction> UPokeMonsterBattlePresentationPlan::BuildActions(const FPokeMonsterBattleResult& Result)
{
	TArray<FPokeMonsterPresentationAction> Actions;
	if (!Result.bSucceeded) return Actions;
	for (const FPokeMonsterBattleEvent& Event : Result.Events)
	{
		if (Event.Type == EPokeMonsterBattleEventType::SwitchedIn)
		{
			FPokeMonsterPresentationAction& Action = Actions.AddDefaulted_GetRef();
			Action.bSwitch = true;
			Action.Source = Event.Source;
			Action.Target = Event.Source;
			Action.TeamIndex = Event.TeamIndex;
			Action.HPBefore = Event.HPBefore;
			Action.HPAfter = Event.HPAfter;
			continue;
		}
		if (Event.Type == EPokeMonsterBattleEventType::MoveExecuted)
		{
			FPokeMonsterPresentationAction& Action = Actions.AddDefaulted_GetRef();
			Action.Source = Event.Source;
			Action.Target = Event.Target;
			Action.Category = Event.Category;
			Action.MoveId = Event.MoveId;
			Action.SlotIndex = Event.SlotIndex;
			Action.PPAfter = Event.PPAfter;
			if (Event.Category == EPokeMonsterMoveCategory::Status)
				Action.Outcome = EPokeMonsterPresentationOutcome::Status;
			continue;
		}
		if (Actions.IsEmpty()) continue; // MoveChosen events precede execution.
		FPokeMonsterPresentationAction& Action = Actions.Last();
		switch (Event.Type)
		{
		case EPokeMonsterBattleEventType::Missed:
			Action.Outcome = EPokeMonsterPresentationOutcome::Miss;
			break;
		case EPokeMonsterBattleEventType::Immune:
			Action.Outcome = EPokeMonsterPresentationOutcome::Immune;
			Action.TypeMultiplier = 0.0f;
			break;
		case EPokeMonsterBattleEventType::SuperEffective:
		case EPokeMonsterBattleEventType::NotVeryEffective:
			Action.TypeMultiplier = Event.TypeMultiplier;
			break;
		case EPokeMonsterBattleEventType::Damage:
			Action.Outcome = EPokeMonsterPresentationOutcome::Hit;
			Action.Damage = Event.Damage;
			Action.HPBefore = Event.HPBefore;
			Action.HPAfter = Event.HPAfter;
			Action.TypeMultiplier = Event.TypeMultiplier;
			break;
		case EPokeMonsterBattleEventType::KnockedOut:
			Action.bKnockedOut = true;
			break;
		case EPokeMonsterBattleEventType::BattleEnded:
			Action.bBattleEnded = true;
			break;
		default:
			break;
		}
	}
	return Actions;
}
