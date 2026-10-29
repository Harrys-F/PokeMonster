#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../UI/PokeMonsterNameplateLayout.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../UI/PokeMonsterBattlePresentationPlan.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPopulationV4Names,"PokeMonster.PopulationV4.ScreenNameLayout",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPopulationV4Names::RunTest(const FString&)
{
 for(const FVector2D View:{FVector2D(2560,1440),FVector2D(1280,720)})
 {
  TArray<FBox2D> Occupied;
  for(int I=0;I<18;++I)
  {
   const FVector2D Size(140,23);const auto P=FPokeMonsterNameplateLayout::Place(FVector2D(500,650),Size,View,Occupied);
   const FBox2D B(P,P+Size);
   TestTrue(TEXT("All names remain inside viewport"),P.X>=0&&P.Y>=0&&P.X+Size.X<=View.X&&P.Y+Size.Y<=View.Y);
   for(const auto& Other:Occupied)TestFalse(TEXT("Names shift rather than disappear"),B.Intersect(Other));
   Occupied.Emplace(P-FVector2D(2,2),P+Size+FVector2D(2,2));
  }
  const auto Edge=FPokeMonsterNameplateLayout::Place(FVector2D(-10,-20),FVector2D(180,24),View,{});
  TestEqual(TEXT("Large visible body with offscreen head retains clamped label"),Edge,FVector2D::ZeroVector);
 }
 const auto* Settings=GetDefault<UPokeMonsterHabitatSettings>();
 TestEqual(TEXT("VisualV2 target cap"),Settings->MaximumPopulation,14);
 TestEqual(TEXT("Species diversity cap preserved"),Settings->MaximumSpecies,6);
 TestTrue(TEXT("Curated setup validates"),Settings->IsValidConfiguration());
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPopulationV4Progression,"PokeMonster.PopulationV4.RealTeamProgressionAndRewards",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPopulationV4Progression::RunTest(const FString&)
{
 const TCHAR* Names[]={TEXT("Zunderlauf"),TEXT("Garados"),TEXT("Pikachu")};const int Levels[]={15,30,11};
 for(int I=0;I<3;++I)
 {
  auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),Names[I],Names[I]));
  if(!TestNotNull(TEXT("Existing team species"),S))return false;
  auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(S,Levels[I]);C.AssignSpeciesMoves();C.CurrentHP-=3;C.ConsumeMovePP(0,2);
  const auto Id=C.InstanceId;const auto Slots=C.GetMoveSlots();const int64 Required=C.GetExperienceToNextLevel();
  TestTrue(TEXT("Actual next threshold"),Required>1);TestTrue(TEXT("Below threshold"),C.AddExperience(Required-1).bSucceeded);
  TestEqual(TEXT("No premature level"),C.Level,Levels[I]);TestTrue(TEXT("Exact threshold accepted"),C.AddExperience(1).bSucceeded);
  TestEqual(TEXT("One level"),C.Level,Levels[I]+1);TestEqual(TEXT("No healing"),C.CurrentHP,C.GetMaxHP()-3);TestEqual(TEXT("Same individual"),C.InstanceId,Id);
  TestEqual(TEXT("PP unchanged"),C.GetMoveSlots()[0].GetCurrentPP(),Slots[0].GetCurrentPP());
  auto K=C;K.CurrentHP=0;K.AddExperience(K.GetExperienceToNextLevel());TestEqual(TEXT("No KO revival"),K.CurrentHP,0);
  C.AddExperience(MAX_int64);TestEqual(TEXT("Cap remains 100"),C.Level,100);TestEqual(TEXT("No remaining XP at cap"),C.GetExperienceToNextLevel(),int64(0));
 }
 // Both a switched-out participant and the current Pokemon earn XP. The message must
 // identify the actual recipient, not stamp every award with the active Pokemon name.
 auto* AData=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 auto* BData=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Pikachu.DA_Pikachu"));
 auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(AData,15);A.AssignSpeciesMoves();auto B=FPokeMonsterCreatureInstance::CreateFromSpecies(BData,11);B.AssignSpeciesMoves();
 auto Enemy=FPokeMonsterCreatureInstance::CreateFromSpecies(AData,10);Enemy.AssignSpeciesMoves();
 auto* Scratch=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Scratch.DA_Scratch"));auto* Growl=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Growl.DA_Growl"));
 B.AssignMove(0,Scratch);Enemy.AssignMove(0,Growl);Enemy.CurrentHP=1;
 auto* P=NewObject<UPokeMonsterBattlePresenter>();TestTrue(TEXT("Existing presenter"),P->InitializeTeamBattle({A,B},{Enemy},1));
 TestTrue(TEXT("Switch participates"),P->TrySelectSwitch(1));TestTrue(TEXT("Switch resolves"),P->ResolveSelection());P->FinishPresentation();
 TestTrue(TEXT("Existing attack"),P->TrySelectMove(0));TestTrue(TEXT("KO resolves"),P->ResolveSelection());P->FinishPresentation();
 const FString Log=P->GetView().Log.ToString();
 const auto Actions=UPokeMonsterBattlePresentationPlan::BuildActions(P->GetLastResult());
 TestTrue(TEXT("Actual message for inactive recipient"),Actions.ContainsByPredicate([](const auto& X){return X.bExperienceGain&&X.Information.Contains(TEXT("Glumanda erhält"));}));
 TestTrue(TEXT("Actual message for active recipient"),Actions.ContainsByPredicate([](const auto& X){return X.bExperienceGain&&X.Information.Contains(TEXT("Pikachu erhält"));}));
 TestTrue(TEXT("Inactive recipient named"),Log.Contains(TEXT("Glumanda erhält")));TestTrue(TEXT("Active recipient named"),Log.Contains(TEXT("Pikachu erhält")));
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPopulationV4EvolutionWindow,"PokeMonster.PopulationV4.OptionalEvolutionTimeWindow",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPopulationV4EvolutionWindow::RunTest(const FString&)
{
 FPokeMonsterEvolutionData Rule;Rule.TargetSpecies=FPrimaryAssetId(TEXT("CreatureSpecies"),TEXT("FutureTarget"));Rule.MinimumLevel=16;FPokeMonsterEvolutionContext C;
 TestTrue(TEXT("Existing untimed routes unchanged"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));
 Rule.RequiredStartMinute=20*60;Rule.RequiredEndMinute=4*60;
 TestFalse(TEXT("Unknown time fails closed"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));
 for(int32 Minute:{0,239,1200,1439}){C.MinuteOfDay=Minute;TestTrue(TEXT("Wrapping night window"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));}
 for(int32 Minute:{240,1199}){C.MinuteOfDay=Minute;TestFalse(TEXT("Exclusive end and before start"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));}
 Rule.RequiredStartMinute=7*60;Rule.RequiredEndMinute=18*60;C.MinuteOfDay=420;
 TestTrue(TEXT("Inclusive day start"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));C.MinuteOfDay=1080;TestFalse(TEXT("Exclusive day end"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));
 Rule.RequiredEndMinute=-1;TestFalse(TEXT("Incomplete range rejected"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));Rule.RequiredEndMinute=420;TestFalse(TEXT("Ambiguous empty range rejected"),UPokeMonsterCreatureProgression::IsEvolutionEligible(Rule,16,C));
 return true;
}
#endif
