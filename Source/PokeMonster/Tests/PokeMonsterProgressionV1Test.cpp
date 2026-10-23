#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"

namespace ProgressionV1
{
UPokeMonsterCreatureSpeciesData* Species(const TCHAR* Name)
{
 return LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),Name,Name));
}
FPokeMonsterCreatureInstance NearWaterGun()
{
 auto* Data=Species(TEXT("Schiggy"));auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Data,12);C.AssignSpeciesMoves();
 C.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(Data->GetGrowthRate(),13)-1;
 C.ConsumeMovePP(0,3);C.CurrentHP-=2;return C;
}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FProgressionV1Learning,"PokeMonster.ProgressionV1.LearningAndFourSlotLimit",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FProgressionV1Learning::RunTest(const FString&)
{
 using namespace ProgressionV1;auto C=NearWaterGun();const auto Id=C.InstanceId;const int PP=C.GetMoveSlots()[0].GetCurrentPP();
 const auto G=C.AddExperience(1);TestEqual(TEXT("Exactly level 13"),C.Level,13);TestEqual(TEXT("One level gained"),G.LevelsGained,1);
 TestEqual(TEXT("Missing HP retained"),C.CurrentHP,C.GetMaxHP()-2);TestEqual(TEXT("Full set is never silently overwritten"),C.GetMoveSlots()[0].GetCurrentPP(),PP);
 TestEqual(TEXT("Water Gun queued"),C.PendingMoves.Num(),1);TestEqual(TEXT("Four slots"),C.GetMoveSlots().Num(),4);
 TestFalse(TEXT("Out-of-range replacement rejected"),C.ResolveMoveLearning(4));TestFalse(TEXT("Negative invalid choice rejected"),C.ResolveMoveLearning(-2));
 TestEqual(TEXT("Rejected choice retains offer"),C.PendingMoves.Num(),1);
 auto Declined=C;TestTrue(TEXT("Decline allowed"),Declined.ResolveMoveLearning(INDEX_NONE));TestTrue(TEXT("Decline consumes only offer"),Declined.PendingMoves.IsEmpty());
 TestEqual(TEXT("Decline retains spent AP"),Declined.GetMoveSlots()[0].GetCurrentPP(),PP);
 TestTrue(TEXT("Accepted replacement"),C.ResolveMoveLearning(1));TestEqual(TEXT("Accepted move identity"),C.GetMoveSlots()[1].GetMove().LoadSynchronous()->InternalId,FName(TEXT("WaterGun")));
 TestEqual(TEXT("New move full AP"),C.GetMoveSlots()[1].GetCurrentPP(),25);TestEqual(TEXT("Other AP unchanged"),C.GetMoveSlots()[0].GetCurrentPP(),PP);TestEqual(TEXT("Same individual"),C.InstanceId,Id);
 TestFalse(TEXT("Cannot learn again after resolving"),C.ResolveMoveLearning(0));C.AddExperience(1);TestTrue(TEXT("No repeat at same level"),C.PendingMoves.IsEmpty());
 auto Many=NearWaterGun();Many.AddExperience(MAX_int64);TestEqual(TEXT("Level cap"),Many.Level,100);TestEqual(TEXT("All seven now-supported crossed levels retained"),Many.PendingMoves.Num(),7);
 TestTrue(TEXT("First offer survives large grant"),Many.PendingMoves[0].LoadSynchronous()->InternalId==TEXT("WaterGun"));TestTrue(TEXT("Later offer retained"),Many.PendingMoves.Last().LoadSynchronous()->InternalId==TEXT("HydroPump"));
 TestFalse(TEXT("Queue rejects duplicates"),Many.RestorePendingMoves({Many.PendingMoves[0],Many.PendingMoves[0]}));
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FProgressionV1Battle,"PokeMonster.ProgressionV1.BattleLearningGate",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FProgressionV1Battle::RunTest(const FString&)
{
 using namespace ProgressionV1;
 for(bool Decline:{false,true})
 {
  auto A=NearWaterGun();A.CalculatedStats.Speed=1000;auto B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(TEXT("Zunderlauf")),10);B.AssignSpeciesMoves();B.CurrentHP=1;
  auto* P=NewObject<UPokeMonsterBattlePresenter>();TestTrue(TEXT("Existing presenter initialized"),P->InitializeTeamBattle({A},{B},1));
  TestTrue(TEXT("Select normal attack"),P->TrySelectMove(0));TestTrue(TEXT("Normal KO grants XP"),P->ResolveSelection());P->FinishPresentation();
  TestTrue(TEXT("Learning gate shown before encounter closes"),P->GetView().bLearningMove);TestFalse(TEXT("No premature end"),P->GetView().bFinished);
  TestFalse(TEXT("No additional combat while learning"),P->TrySelectMove(0));TestEqual(TEXT("Learner row"),P->GetView().LearningTeamIndex,0);
  TestFalse(TEXT("Invalid choice is atomic"),P->ResolveMoveLearning(9));TestTrue(TEXT("Still learning"),P->GetView().bLearningMove);
  const int Round=P->GetBattleState()->RoundNumber;TestTrue(TEXT("Learning decision"),P->ResolveMoveLearning(Decline?INDEX_NONE:2));
  TestFalse(TEXT("Offer resolved"),P->GetView().bLearningMove);TestTrue(TEXT("Encounter can finish"),P->GetView().bFinished);TestEqual(TEXT("Learning does not spend a round"),P->GetBattleState()->RoundNumber,Round);
  TestTrue(TEXT("XP retained"),P->GetBattleState()->TeamA[0].Experience>A.Experience);
 }
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FProgressionV1Save,"PokeMonster.ProgressionV1.PendingSaveAndLegacy",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FProgressionV1Save::RunTest(const FString&)
{
 using namespace ProgressionV1;auto C=NearWaterGun();C.AddExperience(1);auto* GI=NewObject<UGameInstance>();auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI);auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI);
 TestTrue(TEXT("Party accepted"),E->RestorePersistentState({C},{},{}));auto* S=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI);if(!TestNotNull(TEXT("Snapshot"),S))return false;
 const auto Id=C.InstanceId;const FString Slot=TEXT("PokeMonster_ProgressionV1_")+FGuid::NewGuid().ToString(EGuidFormats::Digits);
 TestTrue(TEXT("Write dedicated test slot"),UGameplayStatics::SaveGameToSlot(S,Slot,0));auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromSlot(Slot,0));
 TestTrue(TEXT("Remove only this generated automation slot"),UGameplayStatics::DeleteGameInSlot(Slot,0));
 TestTrue(TEXT("Disk restore"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I));TestEqual(TEXT("Pending offer persists"),E->GetPlayerParty()[0].PendingMoves.Num(),1);
 TestEqual(TEXT("Instance ID persists"),E->GetPlayerParty()[0].InstanceId,Id);TestEqual(TEXT("XP persists"),E->GetPlayerParty()[0].Experience,C.Experience);
 TestEqual(TEXT("Spent AP persists"),E->GetPlayerParty()[0].GetMoveSlots()[0].GetCurrentPP(),C.GetMoveSlots()[0].GetCurrentPP());
 for(int Version=1;Version<=4;++Version){S->SaveVersion=Version;TestTrue(TEXT("Older versions still accepted"),UPokeMonsterSaveSubsystem::RestoreSnapshot(S,E,I));TestTrue(TEXT("Old schema has no fabricated pending offer"),E->GetPlayerParty()[0].PendingMoves.IsEmpty());TestEqual(TEXT("Old ID retained"),E->GetPlayerParty()[0].InstanceId,Id);}
 S->SaveVersion=5;const auto Duplicate=S->PlayerTeam[0].PendingMoves[0];S->PlayerTeam[0].PendingMoves.Add(Duplicate);const auto Before=E->GetPlayerParty()[0].InstanceId;
 AddExpectedError(TEXT("Invalid creature in save"),EAutomationExpectedErrorFlags::Contains,1);
 TestFalse(TEXT("Corrupt duplicated queue rejected"),UPokeMonsterSaveSubsystem::RestoreSnapshot(S,E,I));TestEqual(TEXT("Failed load preserves active party"),E->GetPlayerParty()[0].InstanceId,Before);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FProgressionV1Evolution,"PokeMonster.ProgressionV1.EvolutionMissingTarget",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FProgressionV1Evolution::RunTest(const FString&)
{
 using namespace ProgressionV1;auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(TEXT("Zunderlauf")),15);const auto Id=C.InstanceId;const auto SpeciesRef=C.Species;
 FPokeMonsterEvolutionContext Context;TestTrue(TEXT("No early level evolution"),UPokeMonsterCreatureProgression::GetEvolutionOptions(C,Context).IsEmpty());C.AddExperience(C.GetExperienceToNextLevel());
 auto Options=UPokeMonsterCreatureProgression::GetEvolutionOptions(C,Context);if(!TestEqual(TEXT("Prepared level route"),Options.Num(),1))return false;
 TestEqual(TEXT("Missing target fails closed"),Options[0].Readiness,EPokeMonsterEvolutionReadiness::MissingSpecies);TestEqual(TEXT("No placeholder substitution"),C.Species,SpeciesRef);TestEqual(TEXT("No new individual"),C.InstanceId,Id);
 auto Pikachu=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(TEXT("Pikachu")),20);Context.Trigger=EPokeMonsterEvolutionTrigger::Item;
 TestTrue(TEXT("No item means no item evolution"),UPokeMonsterCreatureProgression::GetEvolutionOptions(Pikachu,Context).IsEmpty());Context.UsedItemId=TEXT("ThunderStone");TestEqual(TEXT("Prepared stone route"),UPokeMonsterCreatureProgression::GetEvolutionOptions(Pikachu,Context).Num(),1);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FProgressionV1Distribution,"PokeMonster.ProgressionV1.ExperienceParticipants",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FProgressionV1Distribution::RunTest(const FString&)
{
 using namespace ProgressionV1;auto* SpeciesData=Species(TEXT("Zunderlauf"));
 for(bool Trainer:{false,true})
 {
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(SpeciesData,20);A.AssignSpeciesMoves();auto B=A;B.InstanceId=FGuid::NewGuid();auto Unused=A;Unused.InstanceId=FGuid::NewGuid();
  auto Enemy=FPokeMonsterCreatureInstance::CreateFromSpecies(SpeciesData,10);Enemy.AssignSpeciesMoves();Enemy.CurrentHP=1;
  // Do not assume old incomplete learnlists determine slot order. This test isolates XP distribution.
  auto* Scratch=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Scratch.DA_Scratch"));
  auto* Growl=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Growl.DA_Growl"));
  A.AssignMove(0,Scratch);B.AssignMove(0,Scratch);Unused.AssignMove(0,Scratch);Enemy.AssignMove(1,Growl);
  auto* Session=NewObject<UPokeMonsterBattleSession>();TestTrue(TEXT("Participant test starts"),Session->InitializeTeams({A,B,Unused},{Enemy},1,false,false,Trainer).bSucceeded);
  FPokeMonsterBattleChoice Switch,NoDamage;Switch.Type=EPokeMonsterBattleChoiceType::Switch;Switch.Index=1;NoDamage.Index=1;
  TestTrue(TEXT("Second member participates"),Session->ResolveTurn(Switch,NoDamage).bSucceeded);
  TestTrue(TEXT("Winning hit"),Session->ResolveRound(0,1).bSucceeded);
  int64 Expected=65*10/7/2;if(Trainer)Expected=Expected*3/2;
  TestEqual(TEXT("First participant share"),Session->GetState().TeamA[0].Experience-A.Experience,Expected);
  TestEqual(TEXT("Second participant share"),Session->GetState().TeamA[1].Experience-B.Experience,Expected);
  TestEqual(TEXT("Nonparticipant receives no XP"),Session->GetState().TeamA[2].Experience,Unused.Experience);
 }
 return true;
}

#endif
