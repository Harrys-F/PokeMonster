#include "PokeMonsterBattlePresentationPlan.h"

TArray<FPokeMonsterPresentationAction> UPokeMonsterBattlePresentationPlan::BuildActions(const FPokeMonsterBattleResult& Result)
{
	TArray<FPokeMonsterPresentationAction> Actions;
	if (!Result.bSucceeded) return Actions;
	for (const FPokeMonsterBattleEvent& Event : Result.Events)
	{

  if(Event.Type==EPokeMonsterBattleEventType::MoveLearned||Event.Type==EPokeMonsterBattleEventType::MoveUnavailable||Event.Type==EPokeMonsterBattleEventType::EvolutionPending||Event.Type==EPokeMonsterBattleEventType::FleeSucceeded||Event.Type==EPokeMonsterBattleEventType::FleeFailed||Event.Type==EPokeMonsterBattleEventType::SeedDamage||Event.Type==EPokeMonsterBattleEventType::SeedHeal||Event.Type==EPokeMonsterBattleEventType::Healed||Event.Type==EPokeMonsterBattleEventType::StatusDamage||Event.Type==EPokeMonsterBattleEventType::ConfusionDamage||Event.Type==EPokeMonsterBattleEventType::BurnDamage||Event.Type==EPokeMonsterBattleEventType::Recoil||Event.Type==EPokeMonsterBattleEventType::ExperienceGained||Event.Type==EPokeMonsterBattleEventType::LevelUp){
   auto& A=Actions.AddDefaulted_GetRef();A.Source=Event.Source;A.Target=Event.Target;A.TeamIndex=Event.TeamIndex;
   A.bFlee=Event.Type==EPokeMonsterBattleEventType::FleeSucceeded||Event.Type==EPokeMonsterBattleEventType::FleeFailed;A.bFleeSucceeded=Event.Type==EPokeMonsterBattleEventType::FleeSucceeded;
   A.bItem=Event.Type==EPokeMonsterBattleEventType::Healed||Event.Type==EPokeMonsterBattleEventType::SeedHeal;A.RestoredHP=Event.RestoredHP;A.HPBefore=Event.HPBefore;A.HPAfter=Event.HPAfter;A.bAffectsActiveHP=!A.bItem||Event.SourceInstanceId==Event.TargetInstanceId;
   A.bResidual=Event.Type==EPokeMonsterBattleEventType::SeedDamage||Event.Type==EPokeMonsterBattleEventType::StatusDamage||Event.Type==EPokeMonsterBattleEventType::ConfusionDamage||Event.Type==EPokeMonsterBattleEventType::BurnDamage||Event.Type==EPokeMonsterBattleEventType::Recoil;A.Damage=Event.Damage;
   A.bInformation=Event.Type==EPokeMonsterBattleEventType::MoveLearned||Event.Type==EPokeMonsterBattleEventType::MoveUnavailable||Event.Type==EPokeMonsterBattleEventType::EvolutionPending||Event.Type==EPokeMonsterBattleEventType::ExperienceGained||Event.Type==EPokeMonsterBattleEventType::LevelUp;
   A.Information=(Event.Type==EPokeMonsterBattleEventType::MoveLearned||Event.Type==EPokeMonsterBattleEventType::MoveUnavailable)?Event.Information.ToString():Event.Type==EPokeMonsterBattleEventType::EvolutionPending?TEXT("Entwicklung vorbereitet – Zielmodell/Sequenz noch offen."):A.bFlee?(A.bFleeSucceeded?TEXT("Du bist entkommen!"):TEXT("Flucht fehlgeschlagen!")):A.bItem?FString::Printf(TEXT("%d KP wiederhergestellt."),Event.RestoredHP):A.bResidual?(Event.Type==EPokeMonsterBattleEventType::SeedDamage?TEXT("Egelsamen entzieht KP."):Event.Type==EPokeMonsterBattleEventType::Recoil?TEXT("Rückstoß verursacht Schaden."):Event.Information.IsEmpty()?TEXT("Die Verbrennung verursacht Schaden."):Event.Information.ToString()):Event.Type==EPokeMonsterBattleEventType::ExperienceGained?FString::Printf(TEXT("%lld Erfahrungspunkte erhalten."),Event.ExperienceAdded):FString::Printf(TEXT("Levelaufstieg: Lv. %d → %d!"),Event.LevelBefore,Event.LevelAfter);continue;
  }
  if(Event.Type==EPokeMonsterBattleEventType::DefenseLowered||Event.Type==EPokeMonsterBattleEventType::DefenseRaised||Event.Type==EPokeMonsterBattleEventType::SpeedLowered||Event.Type==EPokeMonsterBattleEventType::Seeded)
  {
   if(!Actions.IsEmpty())Actions.Last().Information=Event.Type==EPokeMonsterBattleEventType::DefenseLowered?TEXT("Die Verteidigung des Ziels sinkt!"):Event.Type==EPokeMonsterBattleEventType::DefenseRaised?TEXT("Die eigene Verteidigung steigt!"):Event.Type==EPokeMonsterBattleEventType::SpeedLowered?TEXT("Die Initiative des Ziels sinkt!"):TEXT("Das Ziel wurde bepflanzt!");continue;
  }
  if(Event.Type==EPokeMonsterBattleEventType::StatusApplied||Event.Type==EPokeMonsterBattleEventType::StatusPrevented||Event.Type==EPokeMonsterBattleEventType::StatusRecovered||Event.Type==EPokeMonsterBattleEventType::StatChanged||Event.Type==EPokeMonsterBattleEventType::Flinched||Event.Type==EPokeMonsterBattleEventType::Confused||Event.Type==EPokeMonsterBattleEventType::Protected||Event.Type==EPokeMonsterBattleEventType::HitCount)
  {
   if(!Actions.IsEmpty() && Actions.Last().Source==Event.Source && Actions.Last().MoveId==Event.MoveId && Event.MoveId.IsValid())
   {
    auto& A=Actions.Last();
    if(A.Outcome==EPokeMonsterPresentationOutcome::Status || Event.Type==EPokeMonsterBattleEventType::Protected || Event.Type==EPokeMonsterBattleEventType::HitCount)
    {
     if(Event.Type==EPokeMonsterBattleEventType::Protected && A.Outcome==EPokeMonsterPresentationOutcome::None)A.Outcome=EPokeMonsterPresentationOutcome::Status;
     if(!A.Information.IsEmpty())A.Information+=TEXT("\n");A.Information+=Event.Information.ToString();continue;
    }
   }
   auto& A=Actions.AddDefaulted_GetRef();A.bInformation=true;A.Source=Event.Source;A.Target=Event.Target;A.Information=Event.Information.ToString();continue;
  }
  if(Event.Type==EPokeMonsterBattleEventType::AttackLowered||Event.Type==EPokeMonsterBattleEventType::EffectFailed||Event.Type==EPokeMonsterBattleEventType::Burned){if(!Actions.IsEmpty())Actions.Last().Information=Event.Type==EPokeMonsterBattleEventType::AttackLowered?TEXT("Der Angriff des Ziels sinkt!"):Event.Type==EPokeMonsterBattleEventType::EffectFailed?TEXT("Die Attacke hat keine weitere Wirkung."):TEXT("Das Ziel erleidet eine Verbrennung!");continue;}
		if (Event.Type == EPokeMonsterBattleEventType::CaptureSucceeded
			|| Event.Type == EPokeMonsterBattleEventType::CaptureFailed)
		{
			FPokeMonsterPresentationAction& Action = Actions.AddDefaulted_GetRef();
			Action.bCapture = true;
			Action.bCaptureSucceeded = Event.Type == EPokeMonsterBattleEventType::CaptureSucceeded;
			Action.CaptureDeviceId = Event.CaptureDeviceId;
			Action.Source = Event.Source;
			Action.Target = Event.Target;
			continue;
		}
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
			Action.Damage += Event.Damage;
			if(Action.HPBefore==INDEX_NONE)Action.HPBefore = Event.HPBefore;
			Action.HPAfter = Event.HPAfter;
			Action.TypeMultiplier = Event.TypeMultiplier;
			break;
		case EPokeMonsterBattleEventType::KnockedOut:
			for(int I=Actions.Num()-1;I>=0;--I)if(Actions[I].Target==Event.Target&&Actions[I].HPAfter==0){Actions[I].bKnockedOut=true;break;}
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
