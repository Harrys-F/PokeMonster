// Explicit development-only fixtures exercise the real encounter/presenter/UI. No save or asset writes.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "HAL/IConsoleManager.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "Components/Button.h"
#if !UE_BUILD_SHIPPING
namespace PMBattleSystemV3Review
{
static FAutoConsoleCommand Start(TEXT("pm.BattleV3.Start"),TEXT("Explicit unsaved fixture: classic|world wild|trainer|story|failflee|defeat|forced|victory|exhausted."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args){
 if(Args.Num()!=2||(Args[0]!=TEXT("classic")&&Args[0]!=TEXT("world")))return;
 const TSet<FString> Cases={TEXT("wild"),TEXT("trainer"),TEXT("story"),TEXT("failflee"),TEXT("defeat"),TEXT("forced"),TEXT("victory"),TEXT("exhausted")};if(!Cases.Contains(Args[1]))return;
 for(const auto& Context:GEngine->GetWorldContexts()){
  auto* W=Context.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;auto* PC=W->GetFirstPlayerController();auto* Player=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;if(!Player)return;
  auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();if(E->IsEncounterActive())return;
  auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));if(!Species)return;
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,10),B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,10),Reserve=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,10);if(!A.AssignSpeciesMoves()||!B.AssignSpeciesMoves()||!Reserve.AssignSpeciesMoves())return;
  A.CurrentHP-=12;Reserve.CurrentHP-=6;A.CalculatedStats.Speed=100;B.CalculatedStats.Speed=1;
  FPokeMonsterEncounterStartData D;D.EncounterId=FName(*FString::Printf(TEXT("ExplicitBattleV3_%s"),*Args[1]));D.Kind=Args[1]==TEXT("trainer")?EPokeMonsterEncounterKind::Trainer:EPokeMonsterEncounterKind::Wild;D.TrainerId=D.Kind==EPokeMonsterEncounterKind::Trainer?FName(TEXT("ExplicitBattleV3Trainer")):NAME_None;D.Source=Args[1]==TEXT("story")?EPokeMonsterEncounterSource::Scripted:EPokeMonsterEncounterSource::VisibleCreature;D.bAllowFlee=true;D.RandomSeed=17;
  D.PresentationMode=Args[0]==TEXT("classic")?EPokeMonsterBattlePresentationMode::ClassicBattle:EPokeMonsterBattlePresentationMode::WorldBattle;
  if(Args[1]==TEXT("failflee")){A.CalculatedStats.Speed=1;B.CalculatedStats.Speed=200;}
  if(Args[1]==TEXT("defeat")||Args[1]==TEXT("forced")){A.CurrentHP=1;B.CalculatedStats.Speed=200;}
  if(Args[1]==TEXT("victory")){B.CurrentHP=1;A.CalculatedStats.Speed=200;}
  if(Args[1]==TEXT("exhausted"))for(int Slot=0;Slot<3;++Slot){A.ConsumeMovePP(Slot,A.GetMoveSlots()[Slot].GetMaxPP());B.ConsumeMovePP(Slot,B.GetMoveSlots()[Slot].GetMaxPP());}
  D.PlayerTeam.Add(A);if(Args[1]!=TEXT("defeat"))D.PlayerTeam.Add(Reserve);D.OpponentTeam.Add(B);
  auto* Inventory=W->GetGameInstance()->GetSubsystem<UPokeMonsterInventorySubsystem>();auto* Item=LoadObject<UPokeMonsterItemData>(nullptr,TEXT("/Game/Data/Items/DA_TestHealingItem.DA_TestHealingItem"));if(!Inventory||!Item)return;Inventory->AddItem(Item,2);
  E->StartEncounter(D,Player);return;
 }
}));
static FAutoConsoleCommand Click(TEXT("pm.BattleV3.Click"),TEXT("Activate a real battle UMG control: command/move/team/heal index, or capture. No direct session mutation."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args){
 if(Args.IsEmpty()||Args.Num()>2)return;for(const auto& Context:GEngine->GetWorldContexts()){auto* W=Context.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();auto* UI=E?E->GetBattleWidget():nullptr;if(!UI)return;const int I=Args.Num()>1?FCString::Atoi(*Args[1]):0;UButton* B=Args[0]==TEXT("command")?UI->GetCommandButton(I):Args[0]==TEXT("move")?UI->GetAttackButton(I):Args[0]==TEXT("team")?UI->GetSwitchButton(I):Args[0]==TEXT("heal")?UI->GetHealingButton(I):Args[0]==TEXT("capture")?UI->GetCaptureButton():nullptr;if(B&&B->GetIsEnabled()&&B->IsVisible())B->OnClicked.Broadcast();return;}
}));
}
#endif
