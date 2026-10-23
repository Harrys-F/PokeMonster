/** Explicit unsaved fixtures use the real encounter, XP award and existing UMG. */
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "HAL/IConsoleManager.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#if !UE_BUILD_SHIPPING
namespace PMProgressionV1Review
{
static FAutoConsoleCommand Start(TEXT("pm.ProgressionV1.Start"),TEXT("Unsaved explicit progression fixture: classic|world replace|free|evolution. Uses normal XP/UMG; no asset/map/save writes."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=2||(Args[0]!=TEXT("classic")&&Args[0]!=TEXT("world"))||(Args[1]!=TEXT("replace")&&Args[1]!=TEXT("free")&&Args[1]!=TEXT("evolution")))return;
 for(const auto& Context:GEngine->GetWorldContexts())
 {
  auto* W=Context.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;
  auto* PC=W->GetFirstPlayerController();auto* Player=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;
  auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();if(!Player||!E||E->IsEncounterActive())return;
  const bool Water=Args[1]==TEXT("replace");const int Level=Water?12:Args[1]==TEXT("free")?6:15;
  auto* Data=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,Water?TEXT("/Game/Data/Creatures/DA_Schiggy.DA_Schiggy"):TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
  auto* Other=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));if(!Data||!Other)return;
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(Data,Level),B=FPokeMonsterCreatureInstance::CreateFromSpecies(Other,10);
  if(!A.AssignSpeciesMoves()||!B.AssignSpeciesMoves())return;
  A.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(),Level+1)-1;A.CurrentHP-=2;A.CalculatedStats.Speed=1000;B.CurrentHP=1;
  FPokeMonsterEncounterStartData D;D.EncounterId=FName(*FString::Printf(TEXT("ExplicitProgressionV1_%s"),*Args[1]));D.Kind=EPokeMonsterEncounterKind::Wild;D.Source=EPokeMonsterEncounterSource::VisibleCreature;
  D.PresentationMode=Args[0]==TEXT("classic")?EPokeMonsterBattlePresentationMode::ClassicBattle:EPokeMonsterBattlePresentationMode::WorldBattle;
  D.RandomSeed=1;D.PlayerTeam={A};D.OpponentTeam={B};E->StartEncounter(D,Player);return;
 }
}));
}
#endif
