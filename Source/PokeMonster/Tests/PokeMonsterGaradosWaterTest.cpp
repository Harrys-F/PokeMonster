#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "Components/BoxComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Animation/AnimSequence.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosWaterMath,"PokeMonster.GaradosWater.ContinuousObserveAndTurn",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosWaterMath::RunTest(const FString&)
{
 using V=APokeMonsterCreatureVisualActor;float Alpha=0;
 for(int I=0;I<150;++I){float Before=Alpha;Alpha=V::AdvanceSwimObserve(Alpha,true,1.f/60,2.5f);TestTrue(TEXT("Raising has no pose jump"),Alpha>=Before&&Alpha-Before<.007f);}
 TestTrue(TEXT("Full observation in 2.5 seconds"),FMath::IsNearlyEqual(Alpha,1.f,.001f));
 TestEqual(TEXT("Pause preserves pose"),V::AdvanceSwimObserve(Alpha,false,0,2.5f),Alpha);
 for(int I=0;I<150;++I)Alpha=V::AdvanceSwimObserve(Alpha,false,1.f/60,2.5f);
 TestTrue(TEXT("Full smooth descent"),Alpha<.001f);
 TestTrue(TEXT("Yaw wraps through 180 degrees"),FMath::IsNearlyEqual(V::SwimTurnFromYaw(179,-179,.1f,35),-2.f/3.5f));
 TestEqual(TEXT("Teleport timing excluded"),V::SwimTurnFromYaw(0,180,2,35),0.f);
 TestEqual(TEXT("Turn input bounded"),V::SwimTurnFromYaw(0,-90,.1f,35),1.f);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosWaterEnvelope,"PokeMonster.GaradosWater.FullBodyBedClearance",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosWaterEnvelope::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* Cube=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));
 auto Box=[&](FVector P,FVector Scale){auto* A=W->SpawnActor<AStaticMeshActor>(P,FRotator::ZeroRotator);A->GetStaticMeshComponent()->SetStaticMesh(Cube);A->SetActorScale3D(Scale);A->GetStaticMeshComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);A->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);return A;};
 Box(FVector(0,0,-410),FVector(30,30,.2));auto* Z=W->SpawnActor<APokeMonsterBiomeHabitat>();Z->Medium=EPokeMonsterBiomeMedium::WaterOnly;Z->Bounds->SetBoxExtent(FVector(860,610,600));Z->bEllipticalBoundary=true;Z->WaterSurfaceZ=0;
 FCollisionQueryParams Q;FVector Foot;
 TestTrue(TEXT("Deep wide pond accepts full envelope"),Z->ProjectFoot(FVector::ZeroVector,380,380,Q,Foot,0,180,100));
 TestFalse(TEXT("Narrow shore rejects a long body"),Z->ProjectFoot(FVector(0,400,0),380,380,Q,Foot,0,180,100));
 Box(FVector(380,0,-55),FVector(.4,.8,.2));
 TestTrue(TEXT("Old centre-only test misses a shallow tail edge"),Z->ProjectFoot(FVector::ZeroVector,380,380,Q,Foot,0,180));
 TestFalse(TEXT("Full body probe rejects that shallow edge"),Z->ProjectFoot(FVector::ZeroVector,380,380,Q,Foot,0,180,100));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosWaterContract,"PokeMonster.GaradosWater.ProductionRigAndLandBattleIsolation",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosWaterContract::RunTest(const FString&)
{
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Garados.DA_Garados"));if(!TestNotNull(TEXT("Stable species"),S))return false;
 auto* D=S->GetVisuals().Presentation.LoadSynchronous();if(!TestNotNull(TEXT("Water-enabled existing presentation"),D))return false;
 if(!TestNotNull(TEXT("Derived swimming mesh"),D->SwimMesh.Get()))return false;
 TestTrue(TEXT("Full contract"),D->GetValidationErrors().IsEmpty());TestEqual(TEXT("Original seven land/battle roles"),D->Clips.Num(),7);
 TestTrue(TEXT("Land/battle mesh retained"),D->Mesh->GetPathName().Contains(TEXT("Garados/MeshyV1/Meshes/SK_Garados_Meshy.")));
 TestTrue(TEXT("Only water uses new skeleton"),D->SwimMesh->GetSkeleton()!=D->Mesh->GetSkeleton());
 TestTrue(TEXT("Complete horizontal envelope"),D->SwimClearanceRadiusCm>=370);
 for(const auto& Pair:D->Clips)TestEqual(TEXT("Original battle clip skeleton retained"),Pair.Value->GetSkeleton(),D->Mesh->GetSkeleton());
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* V=W->SpawnActor<APokeMonsterCreatureVisualActor>();TestTrue(TEXT("Existing species binding"),V->SetSpecies(S));auto* Component=V->Mesh.Get();
 V->AquaticPoseAlpha=1;V->Tick(.016f);TestTrue(TEXT("Water mesh selected"),V->bUsingSwimMesh);TestEqual(TEXT("One existing mesh component"),V->Mesh.Get(),Component);
 for(auto Role:{EPokeMonsterCreatureClip::Attack,EPokeMonsterCreatureClip::Hit,EPokeMonsterCreatureClip::Faint})
 {TestTrue(TEXT("Existing water reaction selected"),V->PlayReaction(Role));for(int I=0;I<90;++I){V->Mesh->TickAnimation(1.f/30,false);V->Mesh->RefreshBoneTransforms();}TestFalse(TEXT("Water head pose remains finite"),V->Mesh->GetSocketLocation(TEXT("head")).ContainsNaN());}
 V->AquaticPoseAlpha=0;V->Tick(.016f);V->Mesh->TickAnimation(.016f,false);V->Mesh->RefreshBoneTransforms();TestEqual(TEXT("Land/battle mesh restored"),V->Mesh->GetSkeletalMeshAsset(),D->Mesh.Get());TestFalse(TEXT("Land is not in swimming posture"),V->bUsingSwimMesh);for(auto Role:{EPokeMonsterCreatureClip::Attack,EPokeMonsterCreatureClip::Hit,EPokeMonsterCreatureClip::Faint})
 {TestTrue(TEXT("Existing battle reaction retained"),V->PlayReaction(Role));for(int I=0;I<90;++I){V->Mesh->TickAnimation(1.f/30,false);V->Mesh->RefreshBoneTransforms();}TestFalse(TEXT("Land/battle head pose remains finite"),V->Mesh->GetSocketLocation(TEXT("head")).ContainsNaN());}return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosWaterNatural,"PokeMonster.GaradosWater.NaturalPlannerContinuesAfterActivities",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosWaterNatural::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* Floor=W->SpawnActor<AStaticMeshActor>(FVector(0,0,-410),FRotator::ZeroRotator);Floor->GetStaticMeshComponent()->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));Floor->SetActorScale3D(FVector(30,30,.2));Floor->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);
 // Reproduce the real pond's narrow all-heading-safe centre. From its centre,
 // no valid goal reaches the old 180 cm minimum, despite adequate body clearance.
 for(const FVector P:{FVector(600,0,-65),FVector(-600,0,-65),FVector(0,490,-65),FVector(0,-490,-65)})
 {auto* Rock=W->SpawnActor<AStaticMeshActor>(P,FRotator::ZeroRotator);Rock->GetStaticMeshComponent()->SetStaticMesh(Floor->GetStaticMeshComponent()->GetStaticMesh());Rock->SetActorScale3D(FMath::Abs(P.X)>0?FVector(1,30,1.3):FVector(30,1,1.3));Rock->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);}
 auto* Z=W->SpawnActor<APokeMonsterBiomeHabitat>();Z->Medium=EPokeMonsterBiomeMedium::WaterOnly;Z->Bounds->SetBoxExtent(FVector(860,610,600));Z->bEllipticalBoundary=true;Z->WaterSurfaceZ=0;Z->TravelPoints={FVector(0,530,0),FVector(0,-530,0)};
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Garados.DA_Garados"));auto* V=W->SpawnActor<APokeMonsterCreatureVisualActor>();V->SetSpecies(S);
 auto* M=NewObject<UPokeMonsterCreatureRoamingComponent>(V);V->AddInstanceComponent(M);M->RegisterComponent();M->BiomeHabitat=Z;M->WaterDraftOverrideCm=180;M->bOverrideActivities=true;M->ActivityOverride.bEnabled=true;M->ActivityOverride.WanderWeight=4;M->ActivityOverride.ObserveWeight=4;M->ActivityOverride.RestWeight=4;M->ActivityOverride.SleepWeight=.5;M->ActivityOverride.ForageWeight=M->ActivityOverride.SocialWeight=0;
 for(int32 Seed:{817758721,31,701})
 {
  V->SetActorLocation(FVector(0,0,-180));M->Configure(S,0,205,205,nullptr,Seed);
  for(int I=0;I<2400;++I)M->TickComponent(.1f,LEVELTICK_All,nullptr);
  TestTrue(TEXT("Finite natural pauses eventually return to movement"),M->DistanceTravelled>100);TestTrue(TEXT("Long swimmer plans without exhausting two invalid old anchors"),M->SuccessfulPlans>1);
  TestTrue(TEXT("Final full body footprint stays in the pond"),M->IsInsideHabitat(V->GetActorLocation()));
 }
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosWaterPeerQueries,"PokeMonster.GaradosWater.FishAreNotTerrainButRemainPhysicalObstacles",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosWaterPeerQueries::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* H=W->GetSubsystem<UPokeMonsterHabitatSubsystem>();if(!TestNotNull(TEXT("Existing population registry"),H))return false;
 auto* Floor=W->SpawnActor<AStaticMeshActor>(FVector(0,0,-410),FRotator::ZeroRotator);Floor->GetStaticMeshComponent()->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));Floor->SetActorScale3D(FVector(30,30,.2));Floor->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);
 auto* Z=W->SpawnActor<APokeMonsterBiomeHabitat>();Z->Medium=EPokeMonsterBiomeMedium::WaterOnly;Z->Bounds->SetBoxExtent(FVector(860,610,600));Z->WaterSurfaceZ=0;
 auto* A=W->SpawnActor<APokeMonsterVisibleWildCreatureActor>(FVector(0,0,25),FRotator::ZeroRotator);A->ConfigureHabitatBody(205,205);A->OverworldMovement->BiomeHabitat=Z;A->OverworldMovement->WaterDraftOverrideCm=180;
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Garados.DA_Garados"));A->OverworldMovement->Configure(S,205,205,205);
 auto* Peer=W->SpawnActor<APokeMonsterVisibleWildCreatureActor>(FVector(350,0,0),FRotator::ZeroRotator);Peer->ConfigureHabitatBody(40,40);Peer->OverworldMovement->BiomeHabitat=Z;H->Population={A,Peer};
 FVector Foot;const FVector Start(0,0,-180),End(150,0,-180);
 Peer->SetActorLocation(FVector(350,350,0));
 TestTrue(TEXT("Spawn peer already exceeds the unchanged radius plus peer radius plus 50 cm margin"),FVector::Dist2D(Start,Peer->GetActorLocation())>490.f);
 FCollisionQueryParams SpawnTerrain;SpawnTerrain.AddIgnoredActor(A);
 TestFalse(TEXT("Unfiltered spawn envelope incorrectly treats nearby fish as terrain"),Z->ProjectFoot(Start,400,400,SpawnTerrain,Foot,0,180,130));
 H->IgnoreWaterTerrainPeers(Z,SpawnTerrain);
 TestTrue(TEXT("Production spawn terrain filter accepts the same deep water beside a fish"),Z->ProjectFoot(Start,400,400,SpawnTerrain,Foot,0,180,130));
 Peer->SetActorLocation(FVector(350,0,0));
 TestTrue(TEXT("A fish 350 cm away does not become a shallow pond bed"),A->OverworldMovement->ProjectWalkable(Start,Foot));
 TestFalse(TEXT("Original contact capsule still prevents moving into that fish"),A->OverworldMovement->CanTraverse(Start,End));
 Peer->SetActorEnableCollision(false);TestTrue(TEXT("Same static terrain supports the route without a physical obstacle"),A->OverworldMovement->CanTraverse(Start,End));Peer->SetActorEnableCollision(true);return true;
}
#endif
