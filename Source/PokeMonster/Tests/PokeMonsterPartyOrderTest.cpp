#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Save/PokeMonsterSaveGame.h"
#include "../UI/PokeMonsterOverworldView.h"
#include "Engine/GameInstance.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterPartyOrderTest, "PokeMonster.Overworld.Team.ReorderPreservesInstances",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterPartyOrderTest::RunTest(const FString& Parameters)
{
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
 auto* E = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
 auto* I = NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
 auto* S = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 if (!TestNotNull(TEXT("Existing species"),S)) return false;
 TArray<FPokeMonsterCreatureInstance> Team;
 for (int32 Index=0;Index<6;++Index)
 {
  auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(S,10+Index);
  if(!C.AssignSpeciesMoves())return false;
  C.CurrentHP=Index+1;
  C.Status=Index%2 ? EPokeMonsterCreatureStatus::Burn : EPokeMonsterCreatureStatus::None;
  Team.Add(C);
 }
 TestTrue(TEXT("Existing persistent team initialized"),E->RestorePersistentState(Team,{},{}));
 const auto Same=[](const auto& A,const auto& B){return FPokeMonsterCreatureInstance::StaticStruct()->CompareScriptStruct(&A,&B,0);};
 TestTrue(TEXT("Fifth to first swaps"),E->ReorderParty(Team[4].InstanceId,0));
 TestTrue(TEXT("First is exact fifth instance"),Same(E->GetPlayerParty()[0],Team[4]));
 TestTrue(TEXT("Fifth is exact first instance"),Same(E->GetPlayerParty()[4],Team[0]));
 for(const auto& Original:Team)
 {
  const auto* Found=E->GetPlayerParty().FindByPredicate([&](const auto& C){return C.InstanceId==Original.InstanceId;});
  TestTrue(TEXT("All fields including moves, HP, XP, level and status preserved"),Found&&Same(*Found,Original));
 }
 auto* Snapshot=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());
 TestNotNull(TEXT("Reordered party can be saved"),Snapshot);
 if(Snapshot)
 {
  TestEqual(TEXT("Saved order begins with fifth"),Snapshot->PlayerTeam[0].InstanceId,Team[4].InstanceId);
  TestTrue(TEXT("Save restores with existing schema"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Snapshot,E,I));
  TestTrue(TEXT("Restored first is bytewise-equivalent reflected state"),Same(E->GetPlayerParty()[0],Team[4]));
 }
 E->bActive=true;
 TestFalse(TEXT("Battle blocks reordering"),E->ReorderParty(Team[4].InstanceId,2));E->bActive=false;
 TestFalse(TEXT("Stale selection cannot reorder"),E->ReorderParty(FGuid::NewGuid(),0));
 TestFalse(TEXT("Negative target rejected"),E->ReorderParty(Team[4].InstanceId,-1));
 TestFalse(TEXT("Target outside six slots rejected"),E->ReorderParty(Team[4].InstanceId,6));
 TestTrue(TEXT("Partial team restored"),E->RestorePersistentState({Team[0],Team[1],Team[2]}, {}, {}));
 TestTrue(TEXT("Free slot moves instead of duplicating"),E->ReorderParty(Team[0].InstanceId,5));
 TestEqual(TEXT("No empty saved creatures or duplication"),E->GetPlayerParty().Num(),3);
 TestTrue(TEXT("First compacted correctly"),Same(E->GetPlayerParty()[0],Team[1]));
 TestTrue(TEXT("Moved member appended intact"),Same(E->GetPlayerParty()[2],Team[0]));
 TestEqual(TEXT("UI carries identity even for identical species"),FPokeMonsterOverworldViewBuilder::Build(E,I).Team[2].InstanceId,Team[0].InstanceId);
 return true;
}
#endif
