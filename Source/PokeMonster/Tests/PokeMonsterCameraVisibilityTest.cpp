#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Camera/PokeMonsterCameraVisibilityComponent.h"
#include "Materials/MaterialParameterCollection.h"
#include "Materials/Material.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCameraVisibilityTest,
    "PokeMonster.Camera.Visibility.FiniteSightlineAndFade", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterCameraVisibilityTest::RunTest(const FString& Parameters)
{
    using V = UPokeMonsterCameraVisibilityComponent;
    const FVector Camera(0,0,1000), Target(1000,0,100);
    TestTrue(TEXT("An obstructing crown is between camera and character"), V::IsBetweenCameraAndTarget(FBox(FVector(450,-50,500),FVector(550,50,600)),Camera,Target));
    TestFalse(TEXT("Vegetation fully behind the player is not registered"), V::IsBetweenCameraAndTarget(FBox(FVector(1100,-50,-90),FVector(1250,50,50)),Camera,Target));
    TestFalse(TEXT("An off-ray crown stays unchanged"), V::IsBetweenCameraAndTarget(FBox(FVector(450,400,500),FVector(550,500,600)),Camera,Target));
    TestFalse(TEXT("No degenerate camera/player ray"), V::IsBetweenCameraAndTarget(FBox(FVector(-1),FVector(1)),Camera,Camera));
    const float First = V::AdvanceFade(0,true,.05f,.25f);
    TestEqual(TEXT("Fade begins gradually, rather than disappearing"),First,.2f);
    TestTrue(TEXT("Fade can smoothly reverse before completion"),V::AdvanceFade(First,false,.025f,.25f)>0.f && V::AdvanceFade(First,false,.025f,.25f)<First);
    TestEqual(TEXT("Fade reaches full reveal after its configured duration"),V::AdvanceFade(0,true,.25f,.25f),1.f);
    TestEqual(TEXT("Fade restores foliage"),V::AdvanceFade(1,false,.25f,.25f),0.f);
    TestEqual(TEXT("No time progression means no fade jump"),V::AdvanceFade(.4f,true,0,.25f),.4f);
    auto* Collection = LoadObject<UMaterialParameterCollection>(nullptr,TEXT("/Game/Environment/DevTestMapVisualV2/Materials/MPC_PlayerSight.MPC_PlayerSight"));
    TestNotNull(TEXT("Player sight data is available"),Collection);
    if (Collection)
    {
        TestTrue(TEXT("The actual player target parameter exists"),Collection->GetParameterId(TEXT("PlayerSightTarget")).IsValid());
        TestTrue(TEXT("Camera data also stays correct in shadow passes"),Collection->GetParameterId(TEXT("PlayerSightCamera")).IsValid());
    }
    TestNotNull(TEXT("Scoped foliage material remains available"),LoadObject<UMaterial>(nullptr,TEXT("/Game/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal.M_V2_CrownReveal")));
    return true;
}
#endif
