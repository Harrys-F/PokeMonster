#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Development/PokeMonsterCreatureTestGround.h"
#include "../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "Engine/SkeletalMesh.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Engine/StaticMesh.h"
#include "Components/BoxComponent.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Engine/Engine.h"
#include "Engine/StaticMeshActor.h"
#include "Components/StaticMeshComponent.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FTestGroundV7Collection,"PokeMonster.Development.TestGround.V7PersistentCollectionAndEnvelopes",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FTestGroundV7Collection::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::PIE,false,FName(TEXT("Dev_TestMap_VisualV2")),CreatePackage(TEXT("/Temp/V7/Dev_TestMap_VisualV2")));
 GEngine->CreateNewWorldContext(EWorldType::PIE).SetCurrentWorld(W);ON_SCOPE_EXIT{W->DestroyWorld(false);GEngine->DestroyWorldContext(W);};auto* G=W->GetSubsystem<UPokeMonsterCreatureTestGround>();if(!TestNotNull(TEXT("Existing subsystem"),G))return false;G->OnWorldBeginPlay(*W);
 TestEqual(TEXT("Registry is authoritative"),G->Species.Num(),UPokeMonsterCreatureSpeciesData::GetRegisteredPlayableSpecies().Num());TestTrue(TEXT("All V6 imported candidates discovered without spawning one selection"),G->ImportNames.Num()>=49);
 float MinHalf=BIG_NUMBER,MaxHalf=0;TArray<FVector> Centers=G->Stations;TArray<float> Half=G->CellHalfSizes;
 for(int32 I=0;I<G->Species.Num();++I)
 {
  const auto* Presentation=G->Specimens[I]->Presentation.Get();
  if(Presentation->SwimClip)
  {
   const auto* Mesh=Presentation->SwimMesh?Presentation->SwimMesh.Get():Presentation->Mesh.Get();
   const FBox Bounds=Mesh->GetBounds().GetBox();const float Scale=Presentation->SwimMesh?Presentation->SwimBoundsScale:1.f;
   auto* Pool=G->Movements[I]->BiomeHabitat.Get();if(!TestNotNull(TEXT("Aquatic models have a real own water volume"),Pool))return false;
   // Independently sweep the actual rotated bounding box along the controlled route.
   for(int32 Goal=0;Goal<8;++Goal)for(int32 Heading=0;Heading<8;++Heading)for(int32 Corner=0;Corner<8;++Corner)
   {
    const FVector Local((Corner&1)?Bounds.Max.X:Bounds.Min.X,(Corner&2)?Bounds.Max.Y:Bounds.Min.Y,0);
    FVector Point=G->Stations[I]+FVector(G->GetMotionRadius(I),0,0).RotateAngleAxis(Goal*45.f,FVector::UpVector)+Local.RotateAngleAxis(Heading*45.f,FVector::UpVector)*Scale;
    TestTrue(TEXT("Complete water silhouette remains inside the pool, not over its boardwalk"),Pool->ContainsFootprint(Point,0));
   }
  }
  MinHalf=FMath::Min(MinHalf,Half[I]);MaxHalf=FMath::Max(MaxHalf,Half[I]);TestTrue(TEXT("Movement envelope fits in each own cell"),Half[I]>G->GetMotionRadius(I)+100);TestTrue(TEXT("Teleport stays at boardwalk height even for water specimens"),FMath::IsNearlyEqual(G->GetVisitGround(I).Z,G->Center().Z));
 }
 TestTrue(TEXT("Size-aware cells are not a uniform grid"),MaxHalf>MinHalf*3);
 for(int32 I=0;I<Centers.Num();++I)for(int32 J=I+1;J<Centers.Num();++J)TestTrue(TEXT("Actual movement/model cell envelopes cannot overlap"),FMath::Abs(Centers[I].X-Centers[J].X)>=Half[I]+Half[J]||FMath::Abs(Centers[I].Y-Centers[J].Y)>=Half[I]+Half[J]);
 G->PrepareCollection();for(int32 I=0;I<G->ImportNames.Num()+1;++I)G->Tick(.1f);
 TestTrue(TEXT("Whole physically placed collection, no rotating single model"),G->IsCollectionReady());TestEqual(TEXT("Physical count equals both registries"),G->GetPhysicalModelCount(),G->Species.Num()+G->ImportNames.Num());
 const auto* Capsule=GetDefault<APokeMonsterPlayerCharacter>()->GetCapsuleComponent();
 const float Radius=Capsule->GetScaledCapsuleRadius(),Height=Capsule->GetScaledCapsuleHalfHeight();
 const FCollisionShape PlayerShape=FCollisionShape::MakeCapsule(Radius,Height);
 for(int32 I=0;I<G->Species.Num();++I)TestFalse(TEXT("Actual player capsule has a clear safe land/boardwalk teleport"),W->OverlapBlockingTestByChannel(G->GetVisitGround(I)+FVector(0,0,Height+.5f),FQuat::Identity,ECC_Pawn,PlayerShape));
 for(int32 I=0;I<G->ImportNames.Num();++I)
 {
  const float HalfSize=FMath::Max(145.f,float(G->ImportDimensions[I].Size2D()*.5f+85.f));const FVector P=G->ImportStations[I]+FVector(0,-HalfSize-65,Height+.5f);
  TestFalse(TEXT("Every imported target also clears the real player capsule"),W->OverlapBlockingTestByChannel(P,FQuat::Identity,ECC_Pawn,PlayerShape));
 }
 for(int32 I=0;I<G->StaticSpecimens.Num();++I)
 {
  auto* A=G->StaticSpecimens[I].Get();if(!TestNotNull(TEXT("Each import has its own permanent actor"),A))continue;TestFalse(TEXT("No static model ticks"),A->IsActorTickEnabled());TestFalse(TEXT("No inspection model collision"),A->GetActorEnableCollision());TestTrue(TEXT("Original imported scale unchanged"),A->GetActorScale3D().Equals(FVector::OneVector));TestTrue(TEXT("Unique registered target position"),G->GetImportStation(G->ImportNames[I]).Equals(G->ImportStations[I]));
 }
 for(TActorIterator<AStaticMeshActor> It(W);It;++It)if(auto* A=*It;A->ActorHasTag(TEXT("PokemonDevelopmentTestGround"))&&FMath::IsNearlyEqual(A->GetActorScale3D().Z,0.7,0.001))
 {
  auto* Root=A->GetStaticMeshComponent();TestFalse(TEXT("Solid safety collider must not obscure small water models"),Root->IsVisible());TestEqual(TEXT("Both narrow visible rails exist"),Root->GetNumChildrenComponents(),2);TestTrue(TEXT("Continuous player collision remains"),Root->GetCollisionEnabled()!=ECollisionEnabled::NoCollision);
 }
 G->Tick(1.f);TestTrue(TEXT("Leaving the gallery does not remove any model"),G->IsCollectionReady());return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FKarpadorV7Water,"PokeMonster.Habitats.V7KarpadorWholeWaterSamplingAndScope",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FKarpadorV7Water::RunTest(const FString&)
{
 const auto* S=GetDefault<UPokeMonsterHabitatSettings>();int32 OptIns=0;for(const auto& Rule:S->Rules)if(Rule.bVisualV2WaterExploration){++OptIns;TestEqual(TEXT("Only Karpador opt-in"),Rule.Species,FName(TEXT("Karpador")));}TestEqual(TEXT("Exactly one explicit rule"),OptIns,1);
 const FVector Extent(860,610,600);const float Radius=50;const FTransform T(FRotator(0,31,0),FVector(720,-1800,0));int32 Sectors[8]={};float MaxX=0,MaxY=0;FRandomStream Random(1729);
 for(int32 I=0;I<4096;++I)
 {
  const float Angle=Random.FRandRange(-PI,PI);const FVector P=UPokeMonsterCreatureRoamingComponent::SampleWaterArea(T,Extent,Radius,Angle,Random.FRand()),L=T.InverseTransformPosition(P);const float E=FMath::Square(L.X/(Extent.X-Radius))+FMath::Square(L.Y/(Extent.Y-Radius));TestTrue(TEXT("Every proposal respects eroded ellipse before actual depth/path validation"),E<=1.00001f);++Sectors[FMath::Clamp(FMath::FloorToInt((Angle+PI)/(PI/4)),0,7)];MaxX=FMath::Max(MaxX,float(FMath::Abs(L.X)));MaxY=FMath::Max(MaxY,float(FMath::Abs(L.Y)));
 }
 for(int32 N:Sectors)TestTrue(TEXT("Every pond sector is proposed"),N>400);TestTrue(TEXT("Proposals can reach safe edge margins on both axes"),MaxX>(Extent.X-Radius)*.94&&MaxY>(Extent.Y-Radius)*.94);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FKarpadorV7LongSwim,"PokeMonster.Habitats.V7LongDirectWaterRouteKeepsLegacyPlannerBound",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FKarpadorV7LongSwim::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::PIE,false,FName(TEXT("WaterRouteUnit")));GEngine->CreateNewWorldContext(EWorldType::PIE).SetCurrentWorld(W);ON_SCOPE_EXIT{W->DestroyWorld(false);GEngine->DestroyWorldContext(W);};
 auto* Floor=W->SpawnActor<AStaticMeshActor>(FVector(0,0,-220),FRotator::ZeroRotator);auto* C=Floor->GetStaticMeshComponent();C->SetMobility(EComponentMobility::Movable);C->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));C->SetCollisionProfileName(TEXT("BlockAll"));Floor->SetActorScale3D(FVector(30,30,.4));
 auto* Zone=W->SpawnActor<APokeMonsterBiomeHabitat>();Zone->Medium=EPokeMonsterBiomeMedium::WaterOnly;Zone->Bounds->SetBoxExtent(FVector(860,610,600));Zone->bEllipticalBoundary=true;Zone->WaterSurfaceZ=4.2f;Zone->WaterDraftCm=43.f;
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Karpador.DA_Karpador"));auto* V=W->SpawnActor<APokeMonsterCreatureVisualActor>(FVector(-700,0,-38.8f),FRotator::ZeroRotator);if(!TestTrue(TEXT("Existing original presentation"),V->SetSpecies(Species)))return false;V->Tags.Add(TEXT("PokemonDevelopmentSpecimen"));
 auto* M=NewObject<UPokeMonsterCreatureRoamingComponent>(V);V->AddInstanceComponent(M);M->RegisterComponent();M->BiomeHabitat=Zone;M->HabitatRadiusOverride=2109;M->bControlledModelPreview=true;M->Configure(Species,0,50,90,nullptr,7919);
 const FVector End(700,0,-38.8f);TestTrue(TEXT("Real complete depth/sweep corridor is clear"),M->CanTraverse(FVector(-700,0,-38.8f),End));TestFalse(TEXT("Existing generic 12.5m planner guard remains unchanged"),M->RequestModelPreviewGoal(End));M->bExploreWholeWaterHabitat=true;TestTrue(TEXT("Only explicit whole-water profile reaches a checked 14m target without truncation"),M->RequestModelPreviewGoal(End));TestTrue(TEXT("True final goal retained across pond"),M->CurrentGoal.Equals(End,.01f));TestFalse(TEXT("Shore/outside targets stay invalid"),M->RequestModelPreviewGoal(FVector(900,0,-38.8f)));return true;
}
#endif
