#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Development/PokeMonsterCreatureTestGround.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "EngineUtils.h"
#include "Components/SkeletalMeshComponent.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPermanentGroundGateTest,"PokeMonster.Development.TestGround.OrdinaryPIEOnly",
 EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPermanentGroundGateTest::RunTest(const FString& Parameters)
{
 using G=UPokeMonsterCreatureTestGround;
 TestTrue(TEXT("Ordinary VisualV2 PIE eligible without any review command"),G::IsSupportedMap(TEXT("UEDPIE_0_Dev_TestMap_VisualV2"),EWorldType::PIE));
 TestFalse(TEXT("Other development maps untouched"),G::IsSupportedMap(TEXT("Dev_TestMap_VisualV2EnvironmentQualityV1"),EWorldType::PIE));
 TestFalse(TEXT("Packaged game excluded"),G::IsSupportedMap(TEXT("Dev_TestMap_VisualV2"),EWorldType::Game));
 TestFalse(TEXT("Editor authored level excluded"),G::IsSupportedMap(TEXT("Dev_TestMap_VisualV2"),EWorldType::Editor));
 for(int32 I=0;I<10;++I)for(int32 J=I+1;J<10;++J)
  TestTrue(TEXT("Independent 8.6m movement regions never overlap"),FVector::Dist2D(G::Station(I),G::Station(J))>=1000.f);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPermanentGroundIsolationTest,"PokeMonster.Development.TestGround.RealVisualIsolationAndGround",
 EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPermanentGroundIsolationTest::RunTest(const FString& Parameters)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::PIE,false,FName(TEXT("Dev_TestMap_VisualV2")),CreatePackage(TEXT("/Temp/Automation/Dev_TestMap_VisualV2")));
 GEngine->CreateNewWorldContext(EWorldType::PIE).SetCurrentWorld(W);
 ON_SCOPE_EXIT{W->DestroyWorld(false);GEngine->DestroyWorldContext(W);};
 auto* G=W->GetSubsystem<UPokeMonsterCreatureTestGround>();
 if(!TestNotNull(TEXT("World owns initialized subsystem"),G))return false;
 G->OnWorldBeginPlay(*W);
 TestEqual(TEXT("All ten actual species available without a review fixture"),G->Specimens.Num(),10);
 if(G->Specimens.Num()!=10)return false;
 for(int32 I=0;I<10;++I)
 {
  const auto* V=G->Specimens[I].Get();const auto* M=G->Movements[I].Get();FVector Ground;
  TestTrue(TEXT("Distinct development tag"),V->ActorHasTag(TEXT("PokemonDevelopmentSpecimen")));
  TestFalse(TEXT("No interaction target"),V->Implements<UPokeMonsterInteractable>());
  TestFalse(TEXT("Never a capturable wild actor"),V->IsA<APokeMonsterVisibleWildCreatureActor>());
  TestEqual(TEXT("No blocking creature collider"),V->Mesh->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
  TestTrue(TEXT("Own floor is genuinely walkable"),M->ProjectWalkable(UPokeMonsterCreatureTestGround::Station(I),Ground));
  TestTrue(TEXT("Wide free routes use existing collision planner"),M->CanTraverse(UPokeMonsterCreatureTestGround::Station(I),UPokeMonsterCreatureTestGround::Station(I)+FVector(220,170,0)));
  TestEqual(TEXT("Existing seven animation roles retained"),V->Presentation->Clips.Num(),7);
  TestEqual(TEXT("Encounter disabled on specimen only"),M->GetBehaviorProfile().Initiation,EPokeMonsterEncounterInitiation::Disabled);
 }
 TestFalse(TEXT("Cannot teleport without a player"),G->Visit());
 TestFalse(TEXT("No fabricated return anchor"),G->ReturnToWorld());
 TestFalse(TEXT("Invalid mode rejected"),G->SetMode(TEXT("flight")));
 TestTrue(TEXT("Existing run role selected"),G->SetMode(TEXT("run")));
 G->Tick(.1f);
 for(int32 I : {1,3})
 {
  const TCHAR* Name=I==1?TEXT("Schiggy"):TEXT("Pikachu");
  const FString Path=FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),Name,Name);
  const auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*Path);
  const auto* Visual=G->Specimens[I].Get();
  const float Expected=Species->Overworld.RunSpeedOverride>0.f?Species->Overworld.RunSpeedOverride:Visual->Presentation->RunSpeed;
  TestEqual(TEXT("Test ground uses real species fast speed, not only clip reference"),G->Movements[I]->Settings.WalkSpeedOverride,Expected);
 }

 TestFalse(TEXT("Invalid reaction rejected"),G->React(TEXT("unknown")));
 return true;
}
#endif
