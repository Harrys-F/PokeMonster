#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "Engine/Level.h"
#include "Engine/StaticMesh.h"
#include "Components/HierarchicalInstancedStaticMeshComponent.h"
#include "Materials/MaterialInterface.h"
#include "PhysicsEngine/BodySetup.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterWestlandVisualUpgradeTest,
    "PokeMonster.WestlandVisualUpgrade.SavedSheetReplacementAndCollision",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterWestlandVisualUpgradeTest::RunTest(const FString&)
{
    const auto* W=LoadObject<UWorld>(nullptr,TEXT("/Game/Maps/Dev_WestlandRegion.Dev_WestlandRegion"));
    if(!TestNotNull(TEXT("Existing region loads"),W))return false;
    int32 Trees=0,Bushes=0,DetailGrass=0,OldSheets=0,Trunks=0,Rivers=0;
    TSet<FString> Variants;
    for(const AActor* A:W->PersistentLevel->Actors)
    {
        if(!A)continue;
        const FString Label=A->GetActorLabel();
        TArray<UHierarchicalInstancedStaticMeshComponent*> Groups;
        A->GetComponents(Groups);
        for(const auto* C:Groups)
        {
            if(Label.StartsWith(TEXT("WVU_Trees_")))
            {
                Trees+=C->GetInstanceCount();if(C->GetStaticMesh())Variants.Add(C->GetStaticMesh()->GetPathName());
                TestEqual(TEXT("Existing authored trunk collision is active"),C->GetCollisionEnabled(),ECollisionEnabled::QueryAndPhysics);
                TestEqual(TEXT("Pawn blocked by authored model hull"),C->GetCollisionResponseToChannel(ECC_Pawn),ECR_Block);
                TestEqual(TEXT("Ground planner still traces terrain"),C->GetCollisionResponseToChannel(ECC_Visibility),ECR_Ignore);
                const auto* Body=C->GetStaticMesh()?C->GetStaticMesh()->GetBodySetup():nullptr;
                TestTrue(TEXT("Existing simple trunk hull, no leaf triangle collision"),Body&&Body->AggGeom.GetElementCount()>0&&Body->CollisionTraceFlag!=CTF_UseComplexAsSimple);
                TestTrue(TEXT("Real 3D tree geometry"),C->GetStaticMesh()&&!C->GetStaticMesh()->GetName().Contains(TEXT("Card")));
            }
            if(Label.StartsWith(TEXT("WVU_Bush_")))Bushes+=C->GetInstanceCount();
            if(Label.StartsWith(TEXT("WVU_DetailGrass_")))
            {
                DetailGrass+=C->GetInstanceCount();
                TestEqual(TEXT("Ground cover leaves movement clear"),C->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
                TestFalse(TEXT("No additional fine grass shadow pass"),C->CastShadow);
            }
            if(Label==TEXT("WR_Oak")||Label==TEXT("WR_Bush"))OldSheets+=C->GetInstanceCount();
            if(Label==TEXT("WR_TrunkCollision"))
            {
                Trunks=C->GetInstanceCount();TestFalse(TEXT("Old cylinder debug geometry hidden"),C->IsVisible());
                TestEqual(TEXT("No duplicate obsolete cylinder obstacle"),C->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
            }
        }
        if(Label==TEXT("WR_WindingRiver"))
        {
            ++Rivers;const auto* C=A->FindComponentByClass<UStaticMeshComponent>();
            if(TestNotNull(TEXT("Existing water component retained"),C))
            {
                TestTrue(TEXT("Existing river topology uses Westland-only reshaped derivative"),C->GetStaticMesh()&&C->GetStaticMesh()->GetName()==TEXT("SM_WEP_River"));
                TestEqual(TEXT("Water surface collision unchanged"),C->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
                const auto* M=C->GetMaterial(0);
                TestTrue(TEXT("Westland-local physically lit Single Layer Water"),M&&M->GetName()==TEXT("M_WEP_FlowingRiver")&&M->GetBlendMode()==BLEND_Opaque&&M->GetShadingModels().HasShadingModel(MSM_SingleLayerWater));
            }
        }
    }
    TestEqual(TEXT("All original tree positions have a 3D replacement"),Trees,1710);
    TestEqual(TEXT("All old bush sheets replaced"),Bushes,6668);
    TestEqual(TEXT("No legacy tree/bush sheet geometry remains"),OldSheets,0);
    TestEqual(TEXT("Seven existing tree variations"),Variants.Num(),7);
    TestEqual(TEXT("Legacy placements retained without duplicate obstacles"),Trunks,1710);
    TestTrue(TEXT("Grounded detail pockets present"),DetailGrass>20000);
    TestEqual(TEXT("No duplicate river"),Rivers,1);
    return true;
}
#endif
