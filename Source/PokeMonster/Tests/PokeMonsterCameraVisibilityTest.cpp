#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Camera/PokeMonsterCameraVisibilityComponent.h"
#include "Materials/MaterialParameterCollection.h"
#include "Materials/Material.h"
#include "Materials/MaterialInstance.h"
#include "Engine/StaticMesh.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCameraVisibilityTest,
    "PokeMonster.Camera.Visibility.FiniteSightlineAndFade", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterCameraVisibilityTest::RunTest(const FString& Parameters)
{
    using V = UPokeMonsterCameraVisibilityComponent;
    const auto* Default=GetDefault<V>();
    TestEqual(TEXT("Inner radius doubled, not area"),Default->GetTargetRadii().X,110.0);
    TestEqual(TEXT("Outer radius doubled, not area"),Default->GetTargetRadii().Y,220.0);
    const FVector Camera(0,0,1000), Target(1000,0,100);
    TestTrue(TEXT("An obstructing crown is between camera and character"), V::IsBetweenCameraAndTarget(FBox(FVector(450,-50,500),FVector(550,50,600)),Camera,Target));
    TestFalse(TEXT("Vegetation fully behind the player is not registered"), V::IsBetweenCameraAndTarget(FBox(FVector(1100,-50,-90),FVector(1250,50,50)),Camera,Target));
    TestFalse(TEXT("An off-ray crown stays unchanged"), V::IsBetweenCameraAndTarget(FBox(FVector(450,400,500),FVector(550,500,600)),Camera,Target));
    TestFalse(TEXT("No degenerate camera/player ray"), V::IsBetweenCameraAndTarget(FBox(FVector(-1),FVector(1)),Camera,Camera));
    TestTrue(TEXT("Broad phase includes the enlarged cone"),V::IsBetweenCameraAndTarget(FBox(FVector(490,165,540),FVector(510,185,560)),Camera,Target));
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

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCameraTreeFamilyTest,
    "PokeMonster.Camera.Visibility.TreeFamiliesAndBuildingExclusion", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterCameraTreeFamilyTest::RunTest(const FString& Parameters)
{
    const auto* Visibility = GetDefault<UPokeMonsterCameraVisibilityComponent>();
    auto* Birch = LoadObject<UStaticMesh>(nullptr,TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Trees/SM_WLA_Birch_A.SM_WLA_Birch_A"));
    auto* Oak = LoadObject<UStaticMesh>(nullptr,TEXT("/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3.SM_WLA_OakAncient_V3"));
    auto* Cube = LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));
    auto* Bark = LoadObject<UMaterial>(nullptr,TEXT("/Game/Environment/DevTestMapVisualV2/Materials/M_V2_BarkRevealBase.M_V2_BarkRevealBase"));
    auto* Crown = LoadObject<UMaterial>(nullptr,TEXT("/Game/Environment/DevTestMapVisualV2/Materials/M_V2_CrownReveal.M_V2_CrownReveal"));
    TestNotNull(TEXT("Existing birch mesh loads"),Birch);
    TestNotNull(TEXT("Existing oak mesh loads"),Oak);
    TestNotNull(TEXT("Building-like mesh loads"),Cube);
    TestEqual(TEXT("Existing oak crown material is reused unchanged"),Visibility->FindRevealMaterial(Oak,Crown),static_cast<UMaterialInterface*>(Crown));
    TestNull(TEXT("A building cannot opt in even with a crown reveal material"),Visibility->FindRevealMaterial(Cube,Crown));
    TestNull(TEXT("A building cannot opt in even with a bark reveal material"),Visibility->FindRevealMaterial(Cube,Bark));
    TestNull(TEXT("Missing mesh cannot opt in"),Visibility->FindRevealMaterial(nullptr,Bark));
    TestEqual(TEXT("The established fade duration stays unchanged"),Visibility->FadeDuration,.25f);
    for (const TCHAR* Suffix : {TEXT("Birch"),TEXT("LeafBirch"),TEXT("LeafDark"),TEXT("LeafLight")})
    {
        const FString Path = FString::Printf(TEXT("/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_%s.MI_WLA_%s"),Suffix,Suffix);
        auto* Original = LoadObject<UMaterialInterface>(nullptr,*Path);
        TestNotNull(FString::Printf(TEXT("Original %s loads"),Suffix),Original);
        UMaterialInterface* Reveal = Visibility->FindRevealMaterial(Birch,Original);
        TestNotNull(FString::Printf(TEXT("Birch slot %s has a reveal instance"),Suffix),Reveal);
        TestNull(TEXT("A building sharing the original tree material is excluded"),Visibility->FindRevealMaterial(Cube,Original));
        if (!Original || !Reveal) continue;
        TestEqual(TEXT("No duplicate reveal master"),Reveal->GetMaterial(),Bark);
        UTexture* OriginalPaint = nullptr;
        UTexture* RevealPaint = nullptr;
        Original->GetTextureParameterValue(FMaterialParameterInfo(TEXT("Paint")),OriginalPaint);
        Reveal->GetTextureParameterValue(FMaterialParameterInfo(TEXT("Paint")),RevealPaint);
        TestNotNull(TEXT("Original paint texture is available"),OriginalPaint);
        TestEqual(TEXT("Birch paint texture is preserved"),RevealPaint,OriginalPaint);
        FLinearColor OriginalTint, RevealTint;
        TestTrue(TEXT("Original tint is available"),Original->GetVectorParameterValue(FMaterialParameterInfo(TEXT("Tint")),OriginalTint));
        TestTrue(TEXT("Reveal tint is available"),Reveal->GetVectorParameterValue(FMaterialParameterInfo(TEXT("Tint")),RevealTint));
        TestTrue(TEXT("Birch leaf/bark tint is preserved"),OriginalTint.Equals(RevealTint));
        TestEqual(TEXT("Original two-sided rendering is preserved"),Reveal->IsTwoSided(),Original->IsTwoSided());
    }
    return true;
}
#endif
