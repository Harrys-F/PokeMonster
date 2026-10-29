// Deterministic acceptance fixtures only. Neither available in packaged games nor in user storage.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "HAL/IConsoleManager.h"
#include "Misc/Paths.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
#if WITH_EDITOR
namespace InventoryV2Review
{
 UWorld* IsolatedWorld()
 {
  const FString Root=FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()/TEXT("Saved/ProjectRefinement/InventoryV2"));
  if(!FPaths::IsUnderDirectory(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir()),Root))return nullptr;
  for(const auto& Context:GEngine->GetWorldContexts())
   if((Context.WorldType==EWorldType::PIE||Context.WorldType==EWorldType::Game)&&Context.World()&&Context.World()->GetGameInstance())return Context.World();
  return nullptr;
 }
 FAutoConsoleCommand Target(TEXT("pm.InventoryReview.Target"),TEXT("Owned InventoryV2 UserDir only: slot(1-6) HP(-1 keep) poison|keep PP(-1 keep). RAM fixture, no save."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& A)
 {
  auto* W=IsolatedWorld();if(!W||A.Num()!=4||!A[0].IsNumeric()||!A[1].IsNumeric()||!A[3].IsNumeric())return;
  auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();if(!E||E->IsEncounterActive())return;
  auto Team=E->GetPlayerParty();const int32 Index=FCString::Atoi(*A[0])-1;if(!Team.IsValidIndex(Index))return;
  auto& C=Team[Index];auto Slots=C.GetMoveSlots();const int32 PP=FCString::Atoi(*A[3]);
  if(PP>=0)for(auto& Slot:Slots)if(!Slot.GetMove().IsNull())Slot.RestoreCurrentPP(FMath::Min(PP,Slot.GetMaxPP()));
  const int32 HP=FCString::Atoi(*A[1]);const auto Status=A[2]==TEXT("poison")?EPokeMonsterCreatureStatus::Poison:C.Status;
  if(A[2]!=TEXT("keep")&&A[2]!=TEXT("poison"))return;
  if(C.RestoreIndividualState(C.InstanceId,C.Level,C.Experience,HP<0?C.CurrentHP:HP,Slots,Status,Status==EPokeMonsterCreatureStatus::Sleep?C.StatusTurns:0))
   E->RestorePersistentState(Team,E->GetDefeatedTrainerIds(),E->GetCompletedEncounterIds());
 }));
 FAutoConsoleCommand Quest(TEXT("pm.InventoryReview.Quest"),TEXT("Owned InventoryV2 UserDir only: active|complete. Existing mini-slice quest RAM fixture, no new story/content, no save."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& A)
 {
  auto* W=IsolatedWorld();if(!W||A.Num()!=1||(A[0]!=TEXT("active")&&A[0]!=TEXT("complete")))return;
  auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();if(!E||E->IsEncounterActive())return;
  auto* Q=W->GetGameInstance()->GetSubsystem<UPokeMonsterQuestSubsystem>();auto* D=LoadObject<UPokeMonsterQuestData>(nullptr,TEXT("/Game/Data/Quests/DA_SliceArchiveQuest.DA_SliceArchiveQuest"));if(!Q||!D)return;
  FPokeMonsterQuestProgress Progress;Progress.QuestId=D->InternalId;
  Progress.Status=A[0]==TEXT("complete")?EPokeMonsterQuestStatus::Completed:EPokeMonsterQuestStatus::Active;
  Progress.CurrentStep=Progress.Status==EPokeMonsterQuestStatus::Completed?D->Objectives.Num():0;
  Q->RestoreProgress({Progress});
 }));
}
#endif
