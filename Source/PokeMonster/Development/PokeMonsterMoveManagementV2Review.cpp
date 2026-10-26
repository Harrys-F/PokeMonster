/** Explicit transient fixture: no saved NPC, region, map or implicit save write. */
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "HAL/IConsoleManager.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "Kismet/GameplayStatics.h"
#if !UE_BUILD_SHIPPING
namespace PMMoveManagementV2Review
{
static FAutoConsoleCommandWithWorldAndArgs Fixture(TEXT("pm.MoveManagementV2.Prepare"),
 TEXT("Explicit unsaved technical master fixture in existing VisualV2 PIE. Replaces only runtime party; never saves itself."),
 FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args,UWorld* W)
 {
  if(!W || !W->IsGameWorld() || !W->GetGameInstance())return;
  bool bProtectedTest=false;
#if WITH_EDITOR
  if(const auto* Save=W->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>()) bProtectedTest=Save->IsPIETestStorageActive();
#endif
  if(UGameplayStatics::DoesSaveGameExist(UPokeMonsterSaveSubsystem::DevSlotName,0) && !bProtectedTest)
  {
   UE_LOG(LogTemp,Warning,TEXT("MOVE_MANAGEMENT_V2_FIXTURE_REFUSED: developer save exists. Use Tools/MoveManagementV2/RunReview.py with its isolated test slot."));
   return;
  }
  auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();auto* PC=W->GetFirstPlayerController();auto* P=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;
  if(!E || E->IsEncounterActive() || !P || P->IsOverworldInputLocked())return;
  auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Schiggy.DA_Schiggy"));if(!S)return;
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(S,12);if(!A.AssignSpeciesMoves())return;
  A.ConsumeMovePP(0,7);A.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(S->GetGrowthRate(),13)-1;A.AddExperience(1);
  auto B=A;B.InstanceId=FGuid::NewGuid();B.ResolveMoveLearning(INDEX_NONE);
  if(!A.ResolveMoveLearning(0) || !A.ConsumeMovePP(0,5) || !E->RestorePersistentState({A,B},E->GetDefeatedTrainerIds(),E->GetCompletedEncounterIds()))return;
  FActorSpawnParameters Params;Params.ObjectFlags|=RF_Transient;Params.Name=TEXT("TechnicalTest_MasterOfMemories");Params.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
  auto* Master=W->SpawnActor<APokeMonsterNPC>(Params);if(!Master)return;
  Master->Service=EPokeMonsterNPCService::RememberMoves;Master->DisplayName=FText::FromString(TEXT("Meister der Erinnerungen · TECHNISCHER TEST"));
  Master->SetActorLocation(P->GetActorLocation()+P->GetInteractionWorldDirection()*100.f);
  UE_LOG(LogTemp,Display,TEXT("MOVE_MANAGEMENT_V2_TRANSIENT_FIXTURE %s at %s"),*Master->GetPathName(),*Master->GetActorLocation().ToString());
 }));
}
#endif
