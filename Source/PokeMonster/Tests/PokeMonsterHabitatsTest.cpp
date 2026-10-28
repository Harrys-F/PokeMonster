#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterProfile.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "Engine/World.h"
#include "Components/BoxComponent.h"
#include "Engine/Engine.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHabitatCatalogTest,"PokeMonster.Habitats.CuratedRulesAndExistingEncounterData",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FHabitatCatalogTest::RunTest(const FString&)
{
 const auto* S=GetDefault<UPokeMonsterHabitatSettings>();
 TestTrue(TEXT("Configuration valid"),S->IsValidConfiguration());
 TestEqual(TEXT("Existing eight plus near-start meadow and water zone"),S->VisualV2Zones.Num(),10);
 TestEqual(TEXT("Curated population, not entire 18-model catalog"),S->Rules.Num(),14);
 for(const auto& Zone:S->VisualV2Zones)if(Zone.Medium==EPokeMonsterBiomeMedium::Land)TestTrue(TEXT("Pond height must never reject ordinary land"),Zone.WaterSurfaceZ<=-2.f);
 const auto Registry=UPokeMonsterCreatureSpeciesData::GetRegisteredPlayableSpecies();
 for(const auto& R:S->Rules)
 {
  TestTrue(TEXT("Rule points to registered species"),Registry.ContainsByPredicate([&](const auto* C){return C->GetInternalId()==R.Species;}));
  const auto* P=R.Profile.LoadSynchronous();if(!TestNotNull(TEXT("Existing encounter profile"),P))continue;
  TestFalse(TEXT("Profile has actual data"),P->Entries.IsEmpty());
  for(const auto& E:P->Entries){const auto* C=E.Species.LoadSynchronous();TestTrue(TEXT("No wrong-species encounter source"),C&&C->GetInternalId()==R.Species);}
  FPokeMonsterEncounterContext Context;Context.Time=EPokeMonsterEncounterTime::Any;
  FRandomStream Random(12531);FPokeMonsterCreatureInstance Rolled;
  TestTrue(TEXT("Configured source produces a real valid encounter, not just a visual"),P->Roll(Context,Random,Rolled));
  const auto* Actual=Rolled.Species.LoadSynchronous();
  TestTrue(TEXT("Rolled individual matches habitat rule"),Rolled.IsValid()&&Actual&&Actual->GetInternalId()==R.Species);
 }
 FPokeMonsterHabitatRule Day=S->Rules[0],Night=Day;Night.Rhythm=EPokeMonsterActivityRhythm::Nocturnal;
 TestTrue(TEXT("Diurnal population preference"),Day.WeightAt(12*3600)>Day.WeightAt(0));
 TestTrue(TEXT("Nocturnal population preference"),Night.WeightAt(0)>Night.WeightAt(12*3600));
 TestTrue(TEXT("Off-hour weight remains positive"),Day.WeightAt(0)>0);
 auto Bad=S->Rules[0];Bad.MinimumPlayerDistance=0;TestFalse(TEXT("Unsafe spawn distance rejected"),Bad.IsValid());
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHabitatIdentityTest,"PokeMonster.Habitats.PersistentIdentityAndMapIsolation",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FHabitatIdentityTest::RunTest(const FString&)
{
 using H=UPokeMonsterHabitatSubsystem;
 TestTrue(TEXT("PIE exact map"),H::IsVisualV2(TEXT("UEDPIE_0_Dev_TestMap_VisualV2")));
 TestFalse(TEXT("Westland excluded"),H::IsVisualV2(TEXT("Dev_Westland_Region")));
 TestFalse(TEXT("Biome excluded"),H::IsVisualV2(TEXT("Dev_BiomeTestMap_V1")));
 const auto Id=H::PopulationId(TEXT("Forest"),0,TEXT("Pikachu"),2);
 TestEqual(TEXT("Stable across reload"),Id,H::PopulationId(TEXT("Forest"),0,TEXT("Pikachu"),2));
 TestNotEqual(TEXT("Separate individual slot"),Id,H::PopulationId(TEXT("Forest"),1,TEXT("Pikachu"),2));
 TestNotEqual(TEXT("New day replenishes"),Id,H::PopulationId(TEXT("Forest"),0,TEXT("Pikachu"),3));
 TestNotEqual(TEXT("No identity reuse across species"),Id,H::PopulationId(TEXT("Forest"),0,TEXT("Bisasam"),2));
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHabitatBoundsTest,"PokeMonster.Habitats.SharedSurfaceBoundsAndDormancy",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FHabitatBoundsTest::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);ON_SCOPE_EXIT{W->DestroyWorld(false);};
 auto* Z=W->SpawnActor<APokeMonsterHabitatZone>();Z->Bounds->SetBoxExtent(FVector(500,300,250));
 TestTrue(TEXT("Natural activities explicitly opt in"),Z->bAllowNaturalActivities);
 TestTrue(TEXT("Center safe"),Z->ContainsFootprint(FVector(0,0,0),38));
 TestFalse(TEXT("Full footprint remains inside boundary"),Z->ContainsFootprint(FVector(490,0,0),38));
 TestFalse(TEXT("Exterior rejected"),Z->ContainsFootprint(FVector(0,400,0),38));
 Z->bEllipticalBoundary=true;
 TestFalse(TEXT("Ellipse rejects rectangular corner"),Z->ContainsFootprint(FVector(400,230,0),38));
 TestTrue(TEXT("Ellipse retains central swimming space"),Z->ContainsFootprint(FVector(200,40,-100),38));
 TestFalse(TEXT("Large swimmer footprint cannot cross shore"),Z->ContainsFootprint(FVector(350,0,0),205));
 // A mixed-size pond must leave alternative large-swimmer targets after the
 // shared planner remembers its last four destinations.
 for(const auto& Layout:GetDefault<UPokeMonsterHabitatSettings>()->VisualV2Zones)if(Layout.Medium==EPokeMonsterBiomeMedium::WaterOnly)
 {
  Z->SetActorLocation(Layout.Center);Z->Bounds->SetBoxExtent(Layout.Extent);Z->bEllipticalBoundary=true;
  int32 LargeGoals=0;for(const auto& Point:Layout.TravelPoints)if(Z->ContainsFootprint(Layout.Center+Point,205.f))++LargeGoals;
  TestTrue(TEXT("Large swimmer retains choices beyond recent history and occupied goals"),LargeGoals>=6);
 }
 auto* Original=W->SpawnActor<APokeMonsterVisibleWildCreatureActor>();const FName Before=Original->EncounterId;
 Original->ConfigureHabitatBody(205.f,205.f);
 TestEqual(TEXT("No larger search range on ordinary land"),Original->GetShoreInteractionRadius(),0.f);
 Original->OverworldMovement->BiomeHabitat=Z;Z->Medium=EPokeMonsterBiomeMedium::WaterOnly;
 TestEqual(TEXT("Large swimmer exposes its real shore interaction extent"),Original->GetShoreInteractionRadius(),205.f);
 Z->Medium=EPokeMonsterBiomeMedium::Land;
 TestEqual(TEXT("Other media retain existing interaction range"),Original->GetShoreInteractionRadius(),0.f);
 Original->SuspendForHabitatPopulation();
 TestFalse(TEXT("Dormant source has no collision"),Original->GetActorEnableCollision());
 TestFalse(TEXT("Dormant AI no tick"),Original->OverworldMovement->IsComponentTickEnabled());
 TestEqual(TEXT("Original save identity retained"),Original->EncounterId,Before);
 const auto* Old=GetDefault<APokeMonsterBiomeHabitat>();TestFalse(TEXT("Biome sandbox does not opt into natural AI"),Old->bAllowNaturalActivities);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVisualV2PartyTest,"PokeMonster.Habitats.VisualV2NewPartyUsesRealSpecies",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FVisualV2PartyTest::RunTest(const FString&)
{
 TArray<FPokeMonsterCreatureInstance> Party;
 if(!TestTrue(TEXT("Existing factory and profiles build team"),UPokeMonsterEncounterSubsystem::BuildVisualV2TestParty(Party)))return false;
 TestEqual(TEXT("Three occupied, three empty slots"),Party.Num(),3);
 const FName Ids[]={TEXT("Zunderlauf"),TEXT("Garados"),TEXT("Pikachu")};const int32 Levels[]={15,30,11};
 for(int32 I=0;I<Party.Num();++I){TestEqual(TEXT("Real species"),Party[I].Species.LoadSynchronous()->GetInternalId(),Ids[I]);TestEqual(TEXT("Requested or existing profile level"),Party[I].Level,Levels[I]);TestTrue(TEXT("Valid instance with learned moves"),Party[I].IsValid()&&!Party[I].GetLearnedMoves().IsEmpty());}
 return true;
}
#endif
