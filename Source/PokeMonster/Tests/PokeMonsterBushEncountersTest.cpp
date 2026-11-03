#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Encounter/PokeMonsterWildEncounterZone.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
struct FPokeMonsterBushTestAccess
{
 static void Finish(UPokeMonsterHabitatSubsystem* H){H->HandleBushEncounterFinished(FPokeMonsterEncounterEndData());}
};
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBushTravelTest,"PokeMonster.Encounter.Bush.DistanceAndPause",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBushTravelTest::RunTest(const FString&)
{
 auto* S=NewObject<UPokeMonsterBushEncounterSettings>();S->StepDistanceCm=250;
 for(int32 Partition:{10,25,50})
 {
  FPokeMonsterBushTravel T;float D;int32 Checks=0;T.Advance(FVector::ZeroVector,true,*S,D);
  for(int32 X=Partition;X<=1000;X+=Partition)Checks+=T.Advance(FVector(X,0,0),true,*S,D)?1:0;
  TestEqual(TEXT("Distance, not frame/sample count, controls checks"),Checks,4);
  for(int32 I=0;I<100;++I)TestFalse(TEXT("Standing still never rolls"),T.Advance(FVector(1000,0,0),true,*S,D));
  TestFalse(TEXT("Locked/dialogue/menu sample resets travel"),T.Advance(FVector(1250,0,0),false,*S,D));
  TestFalse(TEXT("Resuming establishes a fresh anchor"),T.Advance(FVector(1500,0,0),true,*S,D));
  TestFalse(TEXT("Map/load teleport is not travelled distance"),T.Advance(FVector(20000,0,0),true,*S,D));TestEqual(TEXT("Teleport contributes no travel"),D,0.f);
  TestFalse(TEXT("Vertical motion alone is not a walking step"),T.Advance(FVector(20000,0,100),true,*S,D));
  TestTrue(TEXT("Valid walking resumes after the teleport"),T.Advance(FVector(20250,0,100),true,*S,D));
 }
 S->ChancePerStep=NAN;FPokeMonsterBushTravel T;float D=1;TestFalse(TEXT("Invalid settings fail safely"),T.Advance(FVector::ZeroVector,true,*S,D));TestEqual(TEXT("Invalid settings contribute no travel"),D,0.f);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBushCatalogTest,"PokeMonster.Encounter.Bush.CentralSettingsAndHabitatProfiles",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBushCatalogTest::RunTest(const FString&)
{
 const auto* S=GetDefault<UPokeMonsterBushEncounterSettings>();const auto* H=GetDefault<UPokeMonsterHabitatSettings>();TestTrue(TEXT("Central settings load and validate"),S->IsValidConfiguration());TestFalse(TEXT("Water is not a land-bush habitat"),S->AllowedHabitats.Contains(TEXT("Water")));TestEqual(TEXT("Visible population limit remains 14"),H->MaximumPopulation,14);
 TestFalse(TEXT("Old maps retain the one-shot zone by default"),GetDefault<APokeMonsterWildEncounterZone>()->bDistanceBasedBushEncounters);TestFalse(TEXT("No new permanent actor tick"),GetDefault<APokeMonsterWildEncounterZone>()->PrimaryActorTick.bCanEverTick);
 for(FName Type:S->AllowedHabitats)
 {
  int32 Count=0;
  for(const auto& Rule:H->Rules)if(Rule.Allows(Type))
  {
   ++Count;const auto* Profile=Rule.Profile.LoadSynchronous();if(!TestNotNull(TEXT("Reuse an existing habitat profile"),Profile))continue;
   FPokeMonsterEncounterContext Context;Context.RegionId=Type;Context.Time=EPokeMonsterEncounterTime::Day;FRandomStream Stream(1531);FPokeMonsterCreatureInstance Creature;
   TestTrue(TEXT("Existing habitat source produces an actual valid individual"),Profile->Roll(Context,Stream,Creature));
   TestTrue(TEXT("Species and level remain those of the existing profile"),Creature.IsValid()&&Creature.Species.LoadSynchronous()->GetInternalId()==Rule.Species);
  }
  TestTrue(TEXT("Every allowed habitat has an existing data source"),Count>0);
 }
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBushCooldownTest,"PokeMonster.Encounter.Bush.SharedCooldownAndTravel",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBushCooldownTest::RunTest(const FString&)
{
 auto* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* H=NewObject<UPokeMonsterHabitatSubsystem>(W);const auto* S=GetDefault<UPokeMonsterBushEncounterSettings>();TestFalse(TEXT("No player means no encounter"),H->CanCheckBushEncounters(nullptr));
 FPokeMonsterBushTestAccess::Finish(H);TestEqual(TEXT("Cooldown begins after the shared battle end"),H->GetBushCooldownRemaining(),double(S->CooldownSeconds));TestEqual(TEXT("All fields share one minimum travel budget"),H->GetBushTravelRemaining(),S->MinimumTravelBetweenEncountersCm);
 H->AdvanceBushTravel(S->MinimumTravelBetweenEncountersCm-1);TestEqual(TEXT("Walking consumes the shared budget"),H->GetBushTravelRemaining(),1.f);H->AdvanceBushTravel(-50);TestEqual(TEXT("Bad distance cannot increase or satisfy the budget"),H->GetBushTravelRemaining(),1.f);H->AdvanceBushTravel(2);TestEqual(TEXT("No negative remaining distance"),H->GetBushTravelRemaining(),0.f);TestTrue(TEXT("Travel alone does not release the time cooldown"),H->GetBushCooldownRemaining()>0);return true;
}
#endif
