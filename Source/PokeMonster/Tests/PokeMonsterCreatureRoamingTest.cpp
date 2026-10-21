#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Creatures/Overworld/PokeMonsterCreaturePath.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/Engine.h"
#include "Engine/World.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCreatureHabitatPathTest, "PokeMonster.Creatures.Overworld.BoundedObstaclePath",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FCreatureHabitatPathTest::RunTest(const FString& Parameters)
{
	const FBox Wall(FVector(100,-180,-10), FVector(220,180,10));
	auto Project = [&Wall](const FVector& P, FVector& G)
	{
		G = FVector(P.X,P.Y,0);
		return G.Size2D() < 700 && !Wall.IsInside(G);
	};
	auto Cross = [&Project](const FVector& A, const FVector& B)
	{
		for (int I=0;I<=40;++I) { FVector G; if(!Project(FMath::Lerp(A,B,I/40.f),G)) return false; }
		return true;
	};
	TArray<FVector> Route;
	const FVector Start(0,0,0), Goal(390,0,0);
	TestFalse(TEXT("Straight route actually blocked"), Cross(Start,Goal));
	TestTrue(TEXT("Finds route around wall"), FPokeMonsterCreaturePath::Find(Start,Goal,Project,Cross,Route));
	TestTrue(TEXT("More than one straight segment"), Route.Num()>1);
	FVector Last = Start; float Length = 0;
	for(const FVector& P:Route) { TestTrue(TEXT("Each segment collision-free"),Cross(Last,P)); Length+=FVector::Dist(Last,P); Last=P; }
	TestTrue(TEXT("Route reaches destination"),Last.Equals(Goal,.01f));
	TestTrue(TEXT("Detour actually measured"),Length>FVector::Dist(Start,Goal));
	auto Sealed = [](const FVector&,const FVector&){return false;};
	TestFalse(TEXT("Sealed terrain fails safely"),FPokeMonsterCreaturePath::Find(Start,Goal,Project,Sealed,Route));
	TestTrue(TEXT("No misleading partial path"),Route.IsEmpty());
	TestFalse(TEXT("Out of active planner range rejected"),FPokeMonsterCreaturePath::Find(Start,FVector(5000,0,0),Project,Cross,Route));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCreatureGroundCollisionTest, "PokeMonster.Creatures.Overworld.RealGroundAndWater",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FCreatureGroundCollisionTest::RunTest(const FString& Parameters)
{
	UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);
	GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
	ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
	auto* Cube=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));
	auto Box=[&](const FVector& P,const FVector& Scale)
	{
		auto* A=W->SpawnActor<AStaticMeshActor>(P,FRotator::ZeroRotator);
		A->GetStaticMeshComponent()->SetStaticMesh(Cube);A->SetActorScale3D(Scale);
		A->GetStaticMeshComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		A->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);return A;
	};
	Box(FVector(0,0,-10),FVector(12,12,.2));
	Box(FVector(150,0,100),FVector(1,1,2));
	auto* Water=Box(FVector(-200,0,5),FVector(1,1,.1));Water->Tags.Add(TEXT("Water"));
	auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
	auto* Visual=W->SpawnActor<APokeMonsterCreatureVisualActor>(FVector(0,0,0),FRotator::ZeroRotator);
	auto* M=NewObject<UPokeMonsterCreatureRoamingComponent>(Visual);Visual->AddInstanceComponent(M);M->RegisterComponent();M->Configure(Species,0,20,30);
	FVector Ground;
	TestTrue(TEXT("Real floor found"),M->ProjectWalkable(FVector(0,0,0),Ground));
	TestTrue(TEXT("Measured floor height"),FMath::Abs(Ground.Z)<.1);
	TestFalse(TEXT("Building/trunk blocks movement"),M->CanTraverse(FVector(0,0,0),FVector(300,0,0)));
	TestFalse(TEXT("Water surface not walkable"),M->ProjectWalkable(FVector(-200,0,0),Ground));
	TestFalse(TEXT("Crossing water rejected"),M->CanTraverse(FVector(-100,0,0),FVector(-300,0,0)));
	TestFalse(TEXT("Outside habitat rejected"),M->ProjectWalkable(FVector(900,0,0),Ground));
	TestFalse(TEXT("No ground means no walking"),M->ProjectWalkable(FVector(0,620,0),Ground));
	Box(FVector(0,300,12),FVector(1.7,2.1,.24));
	TestTrue(TEXT("24 cm bridge lip is a supported step, not an obstacle halo"),M->CanTraverse(FVector(0,150,0),FVector(0,450,0)));
	TestTrue(TEXT("Original small movement disk replaced"),M->IsInsideHabitat(FVector(500,0,0)));
	TestTrue(TEXT("Companion visual has no player collider"),Visual->Mesh->GetCollisionEnabled()==ECollisionEnabled::NoCollision);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCreatureMovementConfigTest, "PokeMonster.Creatures.Overworld.ConfigurationAndSpeed",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FCreatureMovementConfigTest::RunTest(const FString& Parameters)
{
	FPokeMonsterCreatureOverworldSettings S;
	TestTrue(TEXT("Default species settings valid"),S.IsValid());
	S.RoamRadius=45;TestFalse(TEXT("Tiny invalid habitat rejected"),S.IsValid());S.RoamRadius=650;
	S.PauseMaximum=.1;TestFalse(TEXT("Invalid pause ordering rejected"),S.IsValid());S.PauseMaximum=3.8;
	S.RecallDistance=S.CompanionRoamRadius;TestFalse(TEXT("Recall hysteresis required"),S.IsValid());
	TestEqual(TEXT("Sprint speed measured without 300 cm/s clipping"),APokeMonsterCreatureVisualActor::SampleSpeed(FVector(38.5,0,0),.1,true),385.f);
	TestEqual(TEXT("Actual teleport still ignored"),APokeMonsterCreatureVisualActor::SampleSpeed(FVector(210,0,0),.1,true),0.f);
	return true;
}
#endif
