#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Game/PokeMonsterGameMode.h"
#include "../Lighting/PokeMonsterDayNight.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"
#include "../Characters/PokeMonsterNPCVisualActor.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Interaction/PokeMonsterRestPoint.h"
#include "../Items/PokeMonsterWorldItem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Rendering/PokeMonsterTemporalAABlendable.h"
#include "Components/BoxComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/DirectionalLight.h"
#include "Engine/Level.h"
#include "Engine/PostProcessVolume.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/World.h"
#include "GameFramework/PlayerStart.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWestlandRollout,"PokeMonster.Westland.RolloutAndExistingInitialParty",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWestlandRollout::RunTest(const FString&)
{
 for(const TCHAR* Name:{TEXT("Dev_WestlandRegion"),TEXT("/Game/Maps/Dev_WestlandRegion"),TEXT("/Game/Maps/UEDPIE_3_Dev_WestlandRegion"),TEXT("UEDPIE_0_Dev_TestMap_VisualV2")})
  TestTrue(TEXT("Exact main-region rollout including PIE"),APokeMonsterGameMode::IsIntegratedRegion(Name));
 for(const TCHAR* Name:{TEXT("Dev_Westland_Region"),TEXT("Dev_WestlandVillage"),TEXT("Dev_WestlandAssetLibrary"),TEXT("Dev_BiomeTestMap_V1"),TEXT("Dev_TestMap_VisualV2GPUBottleneckV1")})
  TestFalse(TEXT("No broad name matching or unintended map opt-in"),APokeMonsterGameMode::IsIntegratedRegion(Name));
 TestTrue(TEXT("Existing day/night controller supports region"),UPokeMonsterDayNightSubsystem::IsTargetMap(TEXT("/Game/Maps/Dev_WestlandRegion")));
 TestEqual(TEXT("Shared population cap unchanged"),GetDefault<UPokeMonsterHabitatSettings>()->MaximumPopulation,14);
 TArray<FPokeMonsterCreatureInstance> Party;
 TestTrue(TEXT("Existing current development party remains buildable"),UPokeMonsterEncounterSubsystem::BuildVisualV2TestParty(Party));
 TestEqual(TEXT("No invented new regional balance"),Party.Num(),3);
 for(const auto& C:Party){const auto* S=C.Species.LoadSynchronous();TestTrue(TEXT("Valid real individual with registered visual"),C.IsValid()&&S&&!S->GetVisuals().Presentation.IsNull());}
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWestlandSavedBindings,"PokeMonster.Westland.SavedRegionBindingsAndIsolation",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWestlandSavedBindings::RunTest(const FString&)
{
 const auto* W=LoadObject<UWorld>(nullptr,TEXT("/Game/Maps/Dev_WestlandRegion.Dev_WestlandRegion"));if(!TestNotNull(TEXT("Existing region, no new map"),W)||!TestNotNull(TEXT("Saved persistent level"),W->PersistentLevel.Get()))return false;
 int32 NPCs=0,Healers=0,Starts=0,Zones=0,Water=0,Finds=0,Ground=0,Suns=0,Fills=0,AA=0,Visuals=0;TSet<const AActor*> Sources;TSet<FName> Ids;
 for(const AActor* A:W->PersistentLevel->Actors)
 {
  if(!A)continue;
  NPCs+=A->IsA<APokeMonsterNPC>();Healers+=A->IsA<APokeMonsterRestPoint>();Starts+=A->IsA<APlayerStart>();
  if(const auto* V=Cast<APokeMonsterNPCVisualActor>(A))
  {
   ++Visuals;TestNotNull(TEXT("Existing source interaction"),V->SourceActor.Get());TestFalse(TEXT("One presentation per source"),Sources.Contains(V->SourceActor));Sources.Add(V->SourceActor);
   TestTrue(TEXT("Real animated library mesh and idle"),V->Visual->GetSkeletalMeshAsset()&&V->IdleAnimation);TestEqual(TEXT("No second visual collision"),V->Visual->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
  }
  if(const auto* Z=Cast<APokeMonsterHabitatZone>(A))
  {
   ++Zones;TestFalse(TEXT("Unique regional population identities"),Ids.Contains(Z->ZoneId));Ids.Add(Z->ZoneId);TestTrue(TEXT("No VisualV2 identity collision"),Z->ZoneId.ToString().StartsWith(TEXT("Westland_")));
   TestTrue(TEXT("Natural activities opt in through existing zone"),Z->bAllowNaturalActivities);
   if(Z->Medium==EPokeMonsterBiomeMedium::WaterOnly){++Water;TestTrue(TEXT("Existing narrow river cannot admit 400cm Garados footprint"),Z->Bounds->GetScaledBoxExtent().Y<400.f);}
  }
  if(const auto* F=Cast<APokeMonsterWorldItem>(A)){++Finds;TestTrue(TEXT("Stable regional find ID"),F->PickupId.ToString().StartsWith(TEXT("Pickup.Westland.")));TestFalse(TEXT("Existing item data"),F->Item.IsNull());}
  if(const auto* M=Cast<AStaticMeshActor>(A))if(A->GetActorLabel().StartsWith(TEXT("WR_Terrain_")))
  {++Ground;TestEqual(TEXT("Existing shared planner can find the terrain"),M->GetStaticMeshComponent()->GetCollisionResponseToChannel(ECC_Visibility),ECR_Block);TestEqual(TEXT("Pawn collision retained"),M->GetStaticMeshComponent()->GetCollisionResponseToChannel(ECC_Pawn),ECR_Block);}
  if(A->IsA<ADirectionalLight>()){Suns+=A->ActorHasTag(TEXT("PokeMonsterSun"));Fills+=A->ActorHasTag(TEXT("PokeMonsterSkyFill"));}
  if(const auto* P=Cast<APostProcessVolume>(A))for(const auto& B:P->Settings.WeightedBlendables.Array)AA+=B.Weight==1.f&&B.Object&&B.Object->IsA<UPokeMonsterTemporalAABlendable>();
 }
 TestEqual(TEXT("Original three dialogue NPCs retained"),NPCs,3);TestEqual(TEXT("Original healer retained"),Healers,1);TestEqual(TEXT("Single player start"),Starts,1);TestEqual(TEXT("Four source-bound NPC models"),Visuals,4);
 TestEqual(TEXT("Authored habitat zones"),Zones,16);TestEqual(TEXT("Three measured shallow river sections"),Water,3);TestEqual(TEXT("Few ordinary item finds"),Finds,3);TestEqual(TEXT("All original terrain tiles retained"),Ground,80);
 TestEqual(TEXT("Single tagged existing sun"),Suns,1);TestEqual(TEXT("Single tagged shadowless fill"),Fills,1);TestEqual(TEXT("Existing TAA choice transferred once"),AA,1);
 return true;
}
#endif
