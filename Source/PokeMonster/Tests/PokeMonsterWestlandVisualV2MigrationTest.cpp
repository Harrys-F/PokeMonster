#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"
#include "../Encounter/PokeMonsterWildEncounterZone.h"
#include "../Development/PokeMonsterCreatureTestGround.h"
#include "Components/BoxComponent.h"
#include "Components/HierarchicalInstancedStaticMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/Level.h"
#include "Engine/World.h"
#include "Materials/MaterialInterface.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWestlandV7Room,"PokeMonster.Westland.VisualV2Migration.HealerRoomAndOriginalAnchors",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWestlandV7Room::RunTest(const FString&)
{
 const auto* W=LoadObject<UWorld>(nullptr,TEXT("/Game/Maps/Dev_WestlandRegion.Dev_WestlandRegion"));if(!TestNotNull(TEXT("Existing saved region"),W))return false;
 const APokeMonsterBuildingCutaway* Healer=nullptr;int32 Rooms=0,Walls=0,Details=0;
 for(const AActor* A:W->PersistentLevel->Actors)if(A)
 {
  if(const auto* C=Cast<APokeMonsterBuildingCutaway>(A)){++Rooms;if(A->GetActorLabel()==TEXT("HouseCutaway"))Healer=C;}
  Details+=A->GetActorLabel().StartsWith(TEXT("WVI_Healer_V6_Interior_"));
 }
 if(!TestNotNull(TEXT("Original healer controller retained"),Healer))return false;
 TestEqual(TEXT("All original room controllers retained"),Rooms,12);TestEqual(TEXT("Exactly the seven existing V6 decoration groups, no room duplication"),Details,7);
 TestTrue(TEXT("Existing stable doorway reused"),Healer->bStableDoorwayTransition);TestTrue(TEXT("Room-only Third Person clamp"),Healer->bConstrainThirdPersonToRoom);TestTrue(TEXT("Existing interior lighting opt-in"),Healer->bUseShadowlessInteriorLighting);
 TestTrue(TEXT("Original regional entrance, not VisualV2 coordinates"),Healer->DoorThreshold->GetComponentLocation().Equals(FVector(-7742.819254,-36097.80118,1107.5),.02));
 TestTrue(TEXT("Original remote room dimensions"),Healer->RelocatedInteriorArea->GetUnscaledBoxExtent().Equals(FVector(520,610,250),.01));
 for(const AActor* A:W->PersistentLevel->Actors)if(A)
 {
  const FString L=A->GetActorLabel();
  if(L.StartsWith(TEXT("HH_Expanded_FrontWall"))||L.StartsWith(TEXT("HH_Expanded_RearWall"))||L.StartsWith(TEXT("HH_Expanded_SideWall")))
  {
   ++Walls;TestFalse(TEXT("No wall actor hidden"),A->IsHidden());TestFalse(TEXT("All four room sides excluded from cutaway"),Healer->OccludingActors.ContainsByPredicate([&](const TObjectPtr<AActor>& V){return V.Get()==A;}));
   TInlineComponentArray<UStaticMeshComponent*> Components(A);for(const auto* C:Components)TestTrue(TEXT("Room wall remains fully visible"),C->IsVisible()&&!C->bHiddenInGame);
  }
 }
 TestEqual(TEXT("All 18 original wall segments retained"),Walls,18);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWestlandBushMigration,"PokeMonster.Westland.VisualV2Migration.RegionalBushFieldsAndSharedRules",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWestlandBushMigration::RunTest(const FString&)
{
 const auto* W=LoadObject<UWorld>(nullptr,TEXT("/Game/Maps/Dev_WestlandRegion.Dev_WestlandRegion"));if(!TestNotNull(TEXT("Existing saved region"),W))return false;
 TMap<FName,const APokeMonsterHabitatZone*> Zones;for(const AActor* A:W->PersistentLevel->Actors)if(const auto* Z=Cast<APokeMonsterHabitatZone>(A))Zones.Add(Z->ZoneId,Z);
 TestEqual(TEXT("Existing 16 habitat identities retained"),Zones.Num(),16);TSet<FName> Fields;
 for(const AActor* A:W->PersistentLevel->Actors)if(const auto* F=Cast<APokeMonsterWildEncounterZone>(A))if(F->bDistanceBasedBushEncounters)
 {
  TestFalse(TEXT("One field per selected existing habitat"),Fields.Contains(F->HabitatZoneId));Fields.Add(F->HabitatZoneId);const auto* const* Found=Zones.Find(F->HabitatZoneId);
  if(!TestTrue(TEXT("Every field binds an actual existing regional habitat"),Found!=nullptr))continue;const auto* Z=*Found;const auto* Box=F->FindComponentByClass<UBoxComponent>();if(!TestNotNull(TEXT("Existing distance trigger"),Box))continue;
  for(int32 I=0;I<4;++I)
  {
   const FVector E=Box->GetUnscaledBoxExtent(),P=Box->GetComponentTransform().TransformPosition(FVector((I&1)?E.X:-E.X,(I&2)?E.Y:-E.Y,0));const FVector L=Z->Bounds->GetComponentTransform().InverseTransformPosition(P),ZE=Z->Bounds->GetUnscaledBoxExtent();TestTrue(TEXT("Whole field footprint stays within its actual habitat"),FMath::Abs(L.X)<=ZE.X&&FMath::Abs(L.Y)<=ZE.Y);
  }
 }
 TestEqual(TEXT("Four modest fields, no copied VisualV2 coordinates"),Fields.Num(),4);const auto* S=GetDefault<UPokeMonsterBushEncounterSettings>();TestTrue(TEXT("Existing chance unchanged"),FMath::IsNearlyEqual(S->ChancePerStep,.18f));TestEqual(TEXT("Existing step distance unchanged"),S->StepDistanceCm,250.f);TestEqual(TEXT("Existing cooldown unchanged"),S->CooldownSeconds,12.f);TestEqual(TEXT("Existing population cap"),GetDefault<UPokeMonsterHabitatSettings>()->MaximumPopulation,14);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWestlandSurfaceMigration,"PokeMonster.Westland.VisualV2Migration.GroundAndBridgeCollisionContract",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWestlandSurfaceMigration::RunTest(const FString&)
{
 const auto* W=LoadObject<UWorld>(nullptr,TEXT("/Game/Maps/Dev_WestlandRegion.Dev_WestlandRegion"));if(!TestNotNull(TEXT("Existing saved region"),W))return false;int32 Ground=0,Road=0,Planks=0;const UStaticMeshComponent* Deck=nullptr;const UHierarchicalInstancedStaticMeshComponent* Boards=nullptr;
 for(const AActor* A:W->PersistentLevel->Actors)if(A)
 {
  const FString L=A->GetActorLabel();const auto* C=A->FindComponentByClass<UStaticMeshComponent>();
  if(C&&L.StartsWith(TEXT("WR_Terrain_"))){++Ground;TestTrue(TEXT("Regional PBR ground, original geometry retained"),C->GetMaterial(0)&&C->GetMaterial(0)->GetName()==TEXT("M_WI_RegionalGround"));TestEqual(TEXT("Terrain still supports gameplay"),C->GetCollisionResponseToChannel(ECC_Pawn),ECR_Block);}
  if(C&&L.StartsWith(TEXT("WR_Path_"))){++Road;TestFalse(TEXT("Ordinary road geometry no longer double renders terrain"),C->IsVisible());}
  if(L==TEXT("WR_Holzbruecke_Deck"))Deck=C;
  if(L==TEXT("WVI_Bridge_DeckBoards"))Boards=A->FindComponentByClass<UHierarchicalInstancedStaticMeshComponent>();
 }
 TestEqual(TEXT("All 80 existing terrain tiles"),Ground,80);TestEqual(TEXT("All six routes and eleven accesses retained"),Road,17);
 if(TestNotNull(TEXT("Original bridge collider"),Deck)&&TestNotNull(TEXT("Existing wood modules form visual planks"),Boards))
 {
  TestEqual(TEXT("Original deck still blocks player"),Deck->GetCollisionResponseToChannel(ECC_Pawn),ECR_Block);TestEqual(TEXT("No duplicate plank collision"),Boards->GetCollisionEnabled(),ECollisionEnabled::NoCollision);Planks=Boards->GetInstanceCount();AddInfo(FString::Printf(TEXT("Bridge measurement deck=%s scale=%s group=%s boundsMin=%s boundsMax=%s"),*Deck->GetComponentLocation().ToString(),*Deck->GetComponentScale().ToString(),*Boards->GetComponentLocation().ToString(),*Boards->GetStaticMesh()->GetBoundingBox().Min.ToString(),*Boards->GetStaticMesh()->GetBoundingBox().Max.ToString()));TestTrue(TEXT("Continuous full-span deck"),Planks>=70);const float Floor=Deck->GetComponentLocation().Z+Deck->GetComponentScale().Z*50.f;
  for(int32 I=0;I<Planks;++I){FTransform T;Boards->GetInstanceTransform(I,T,true);if(I==0)AddInfo(FString::Printf(TEXT("First board transform=%s top=%.6f floor=%.6f"),*T.ToString(),T.TransformPosition(Boards->GetStaticMesh()->GetBoundingBox().Max).Z,double(Floor)));TestTrue(TEXT("Visual plank top matches original collision floor"),FMath::IsNearlyEqual(T.TransformPosition(Boards->GetStaticMesh()->GetBoundingBox().Max).Z,double(Floor),.05));}
 }
 TestFalse(TEXT("No development gallery in the main region"),UPokeMonsterCreatureTestGround::IsSupportedMap(TEXT("Dev_WestlandRegion"),EWorldType::Game));TestTrue(TEXT("Reference gallery remains available"),UPokeMonsterCreatureTestGround::IsSupportedMap(TEXT("Dev_TestMap_VisualV2"),EWorldType::Game));return true;
}
#endif
