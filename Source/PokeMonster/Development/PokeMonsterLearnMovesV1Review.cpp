/** Editor-only isolated fixture for existing learning UI. No gameplay implementation, disk writes or saved actors. */
#include "CoreMinimal.h"
#include "HAL/IConsoleManager.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#if WITH_EDITOR
namespace PMLearnMovesV1Review
{
FAutoConsoleCommandWithWorldAndArgs Prepare(TEXT("pm.LearnMovesV1.Prepare"),TEXT("Editor PIE isolated save only: <Bibor|Garados|Habitak|Karpador|Smettbo> <learning level> full|free. Sets XP one below threshold; use existing XP or victory command."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args,UWorld* W)
{
 if(!W || W->WorldType!=EWorldType::PIE || Args.Num()!=3 || !Args[1].IsNumeric() || (Args[2]!=TEXT("full")&&Args[2]!=TEXT("free")))return;
 const TArray<FString> Names={TEXT("Bibor"),TEXT("Garados"),TEXT("Habitak"),TEXT("Karpador"),TEXT("Smettbo")};if(!Names.Contains(Args[0]))return;
 auto* GI=W->GetGameInstance();auto* Save=GI?GI->GetSubsystem<UPokeMonsterSaveSubsystem>():nullptr;auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 if(!Save || !Save->IsPIETestStorageActive() || !E || E->IsEncounterActive())return;
 const int32 Level=FCString::Atoi(*Args[1]);if(Level<2||Level>100)return;
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*(TEXT("/Game/Data/Creatures/DA_")+Args[0]));auto* Reserve=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Glurak"));
 if(!Species || !Reserve || !Species->LevelUpMoves.ContainsByPredicate([Level](const auto& L){return L.Level==Level&&!L.Move.IsNull();}))return;
 auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,Level-1),R=FPokeMonsterCreatureInstance::CreateFromSpecies(Reserve,36);R.AssignSpeciesMoves();
 if(Args[2]==TEXT("full"))
 {
  const TCHAR* Paths[]={TEXT("/Game/Data/Moves/DA_Scratch"),TEXT("/Game/Data/Moves/DA_Growl"),TEXT("/Game/Data/Moves/DA_Ember"),TEXT("/Game/Data/Moves/DA_Tackle")};
  for(int32 I=0;I<4;++I){auto* M=LoadObject<UPokeMonsterMoveData>(nullptr,Paths[I]);if(!M||!C.AssignMove(I,M))return;C.ConsumeMovePP(I,1);}
 }
 else C.AssignSpeciesMoves();
 C.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(C.GetExperienceGrowthRate(),Level)-1;
 if(E->RestorePersistentState({C,R},E->GetDefeatedTrainerIds(),E->GetCompletedEncounterIds()))UE_LOG(LogTemp,Display,TEXT("LEARN_MOVES_V1_ISOLATED_FIXTURE %s before level %d %s"),*Args[0],Level,*Args[2]);
}));
}
#endif
