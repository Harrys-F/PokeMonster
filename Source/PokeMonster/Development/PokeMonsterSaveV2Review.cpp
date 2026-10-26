// Editor-only fixtures for the existing save transport. Never targets a user slot.
#include "CoreMinimal.h"
#if WITH_EDITOR
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "EngineUtils.h"
#include "HAL/IConsoleManager.h"

struct FPokeMonsterSaveV2TestAccess
{
 static bool Write(UPokeMonsterSaveSubsystem* S, const FString& Kind)
 {
  if (!S || !S->GetWorld() || S->GetWorld()->WorldType != EWorldType::PIE
   || !S->IsolatedPIESlot.StartsWith(TEXT("PokeMonster_SaveV2_Test_")) || S->IsPIEMemoryPreviewActive()) return false;
  const TSet<FString> Cases={TEXT("legacy"),TEXT("missing-map"),TEXT("invalid-position"),TEXT("blocked"),TEXT("crossmap"),TEXT("missing-checkpoint")};
  if (!Cases.Contains(Kind)) return false;
  auto* GI=S->GetGameInstance();
  auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(GI->GetSubsystem<UPokeMonsterEncounterSubsystem>(),
   GI->GetSubsystem<UPokeMonsterInventorySubsystem>(),S,GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>(),GI->GetSubsystem<UPokeMonsterQuestSubsystem>());
  if (!Save || !Save->PlayerLocation.IsValid()) return false;
  // Explicit technical checkpoint, only in this isolated snapshot; never activates a world source.
  Save->ActiveCheckpoint.CheckpointId=TEXT("SaveV2_EdgeFixture");
  Save->ActiveCheckpoint.MapPackage=Save->PlayerLocation.MapPackage;
  Save->ActiveCheckpoint.Location=Save->PlayerLocation.Location;
  Save->ActiveCheckpoint.Rotation=Save->PlayerLocation.Rotation;
  if (Kind==TEXT("legacy")) { Save->SaveVersion=8; Save->PlayerLocation={}; }
  else if (Kind==TEXT("missing-map")) Save->PlayerLocation.MapPackage=TEXT("/Game/Maps/SaveV2_MissingMap_DoNotCreate");
  else if (Kind==TEXT("invalid-position")) Save->PlayerLocation.Location.X=HALF_WORLD_MAX*2.;
  else if (Kind==TEXT("blocked"))
  {
   AActor* Rock=nullptr;
   for (TActorIterator<AActor> It(S->GetWorld());It;++It)
    if(It->GetActorLabel()==TEXT("VS_BoundaryRock_0")){Rock=*It;break;}
   if(!Rock)return false;
   FVector Extent;Rock->GetActorBounds(true,Save->PlayerLocation.Location,Extent);
   Save->PlayerLocation.Location.Z=50.15;
  }
  else if (Kind==TEXT("missing-checkpoint")) Save->ActiveCheckpoint.MapPackage=TEXT("/Game/Maps/SaveV2_MissingCheckpoint_DoNotCreate");
  else if (Kind==TEXT("crossmap"))
  {
   Save->PlayerLocation.MapPackage=TEXT("/Game/Maps/Dev_TestMap");
   Save->PlayerLocation.Location=FVector(-1000,-1100,50.15);
   Save->PlayerLocation.Rotation=FRotator(0,123,0);
   Save->PlayerLocation.FacingDirection=Save->PlayerLocation.Rotation.Vector();
   Save->PlayerLocation.InteriorActor=NAME_None;Save->PlayerLocation.bRelocatedInterior=false;
  }
  return UPokeMonsterSaveSubsystem::SaveSnapshotToSlot(Save,S->SlotName(false));
 }
};
namespace
{
 FAutoConsoleCommand SaveV2ReviewFixtureCommand(TEXT("pm.SaveV2Review.Fixture"),
  TEXT("Editor PIE, isolated SaveV2 test slot required: legacy|missing-map|invalid-position|blocked|crossmap|missing-checkpoint. Never a user save."),
  FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
 {
  if(Args.Num()!=1)return;
  for(const auto& Context:GEngine->GetWorldContexts())
   if(Context.WorldType==EWorldType::PIE&&Context.World()&&Context.World()->GetGameInstance())
   {
    const bool Written=FPokeMonsterSaveV2TestAccess::Write(Context.World()->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>(),Args[0]);
    UE_LOG(LogTemp,Display,TEXT("SAVE_V2_ISOLATED_FIXTURE %s written=%d"),*Args[0],Written);return;
   }
 }));
}
#endif
