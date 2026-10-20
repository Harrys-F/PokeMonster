#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Encounter/PokeMonsterClassicBattleScene.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Components/InstancedStaticMeshComponent.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterBattleEnvironmentV2Test,"PokeMonster.Encounter.ClassicBattle.EnvironmentV2",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterBattleEnvironmentV2Test::RunTest(const FString& Parameters)
{
 using Scene=APokeMonsterClassicBattleScene;using E=EPokeMonsterBattleEnvironment;
 TestEqual(TEXT("Legacy encounters select environment automatically"),FPokeMonsterEncounterStartData().BattleEnvironment,E::Auto);
 TestEqual(TEXT("Known forest region"),Scene::ThemeForRegion(TEXT("WestlandForest")),E::Forest);
 TestEqual(TEXT("Known cave region"),Scene::ThemeForRegion(TEXT("CaveEntrance")),E::Cave);
 TestEqual(TEXT("Known ruin region"),Scene::ThemeForRegion(TEXT("AncientRuins")),E::Ruins);
 TestEqual(TEXT("Unknown region is not guessed as cave"),Scene::ThemeForRegion(TEXT("Unknown")),E::Auto);
 TestEqual(TEXT("Safe unclassified fallback"),Scene::ResolveEnvironment(E::Auto,NAME_None,nullptr),E::Meadow);
 for(E Theme:{E::Meadow,E::Forest,E::Cave,E::Ruins})TestEqual(TEXT("Explicit profile overrides region"),Scene::ResolveEnvironment(Theme,TEXT("WestlandForest"),nullptr),Theme);
 const auto* D=GetDefault<Scene>();TestEqual(TEXT("All ten reusable dressing assets available"),D->DressingMeshes.Num(),10);TestEqual(TEXT("All existing ground materials available"),D->GroundMaterials.Num(),3);
 TestTrue(TEXT("Standard camera is closer than V1 before bounds padding"),D->FramingDistance<700.f);
 TestTrue(TEXT("Nintendo logical A/B profile is configurable and defaults to Switch"),GetDefault<UPokeMonsterBattleWidget>()->bNintendoButtonLayout);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterBattleEnvironmentInstancesV2Test,"PokeMonster.Encounter.ClassicBattle.InstancedLocationV2",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterBattleEnvironmentInstancesV2Test::RunTest(const FString& Parameters)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 W->InitializeActorsForPlay(FURL());W->BeginPlay();auto* Reference=W->SpawnActor<AActor>();auto* Root=NewObject<USceneComponent>(Reference);Reference->SetRootComponent(Root);Root->RegisterComponent();Reference->SetActorLocation(FVector(5000,0,0));
 auto* Group=W->SpawnActor<AActor>();auto* Trees=NewObject<UInstancedStaticMeshComponent>(Group);Group->SetRootComponent(Trees);Group->AddInstanceComponent(Trees);Trees->SetStaticMesh(GetDefault<APokeMonsterClassicBattleScene>()->DressingMeshes.FindRef(TEXT("Tree")));Trees->RegisterComponent();
 using Scene=APokeMonsterClassicBattleScene;using E=EPokeMonsterBattleEnvironment;
 Trees->AddInstance(FTransform(FVector(0,0,0)));TestEqual(TEXT("Distant instance is not forest at encounter"),Scene::ResolveEnvironment(E::Auto,NAME_None,Reference),E::Meadow);
 for(int I=0;I<3;++I)Trees->AddInstance(FTransform(FVector(5000,I*30,0)));
 TestEqual(TEXT("Nearby instance positions count even when group origin is distant"),Scene::ResolveEnvironment(E::Auto,NAME_None,Reference),E::Forest);
 TestEqual(TEXT("Explicit meadow still wins"),Scene::ResolveEnvironment(E::Meadow,NAME_None,Reference),E::Meadow);
 W->DestroyWorld(false);GEngine->DestroyWorldContext(W);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterBattleMoveLabelsV2Test,"PokeMonster.Battle.UI.ProvisionalMoveLabels",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterBattleMoveLabelsV2Test::RunTest(const FString& Parameters)
{
 auto* M=NewObject<UPokeMonsterMoveData>();M->InternalId=TEXT("TestPhysical");M->DisplayName=FText::FromString(TEXT("TestNormalPhysical"));const int Power=M->BasePower;
 TestFalse(TEXT("No technical identifier shown"),M->GetPlayerFacingName().ToString().Contains(TEXT("TestNormalPhysical")));
 TestTrue(TEXT("Provisional data explicitly labelled"),M->GetPlayerFacingName().ToString().Contains(TEXT("Test")));
 TestEqual(TEXT("No balancing change"),M->BasePower,Power);
 M->InternalId=TEXT("AuthoredMove");M->DisplayName=FText::FromString(TEXT("Freigegebener Name"));TestEqual(TEXT("Authored names preserved"),M->GetPlayerFacingName().ToString(),M->DisplayName.ToString());
 return true;
}
#endif
