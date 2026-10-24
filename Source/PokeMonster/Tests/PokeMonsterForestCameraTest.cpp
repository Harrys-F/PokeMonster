#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Development/BiomeTestV1/PokeMonsterForestCameraZone.h"
#include "../Camera/PokeMonsterCameraVisibilityComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/Material.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBiomeForestCameraEnvelope,"PokeMonster.BiomeV11.ForestCamera.LocalEnvelope",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBiomeForestCameraEnvelope::RunTest(const FString& Parameters)
{
 using Z=APokeMonsterForestCameraZone;const FVector Extent(1050,650,600);
 TestEqual(TEXT("Deep forest alone requests close view"),Z::TargetAmount(FVector(0,0,50),Extent,180),1.f);
 TestEqual(TEXT("Half feather blends smoothly"),Z::TargetAmount(FVector(1140,0,50),Extent,180),.5f);
 TestEqual(TEXT("Meadow outside zone remains unchanged"),Z::TargetAmount(FVector(-1800,0,50),Extent,180),0.f);
 TestEqual(TEXT("Ruin beyond forest margin restores camera"),Z::TargetAmount(FVector(0,-1100,50),Extent,180),0.f);
 TestEqual(TEXT("A different interior elevation cannot activate"),Z::TargetAmount(FVector(0,0,1200),Extent,180),0.f);
 TestEqual(TEXT("Invalid area rejected"),Z::TargetAmount(FVector::ZeroVector,FVector::ZeroVector,180),0.f);
 TestEqual(TEXT("Transition starts at exact baseline"),Z::SmoothAmount(0),0.f);TestEqual(TEXT("Transition reaches exact candidate"),Z::SmoothAmount(1),1.f);TestEqual(TEXT("Midpoint stays continuous"),Z::SmoothAmount(.5f),.5f);
 TestTrue(TEXT("Low transition speed at entry"),Z::SmoothAmount(.1f)<.1f);TestTrue(TEXT("Low transition speed before completion"),Z::SmoothAmount(.9f)>.9f);
 const auto* V=GetDefault<UPokeMonsterCameraVisibilityComponent>();TestEqual(TEXT("Default world has no dense canopy request"),V->DenseCanopyAmount,0.f);TestEqual(TEXT("Existing outer sight radius preserved"),V->GetTargetRadii().Y,220.);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBiomeForestCameraMaterialScope,"PokeMonster.BiomeV11.ForestCamera.MaterialScope",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBiomeForestCameraMaterialScope::RunTest(const FString& Parameters)
{
 auto* M=LoadObject<UMaterial>(nullptr,TEXT("/Game/Environment/BiomeTestV1/DenseForestV11/M_V2_CrownReveal_Dense.M_V2_CrownReveal_Dense"));if(!TestNotNull(TEXT("Actual separate canopy asset"),M))return false;
 auto* Oak=LoadObject<UStaticMesh>(nullptr,TEXT("/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3.SM_WLA_OakAncient_V3"));auto* Cube=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));const auto* V=GetDefault<UPokeMonsterCameraVisibilityComponent>();
 TestEqual(TEXT("Known tree plus explicit private master opt in"),V->FindRevealMaterial(Oak,M),static_cast<UMaterialInterface*>(M));TestNull(TEXT("Architecture never joins canopy fade"),V->FindRevealMaterial(Cube,M));TestNull(TEXT("Missing tree never joins canopy fade"),V->FindRevealMaterial(nullptr,M));
 float Strength=-1;TestTrue(TEXT("Only separate shader has local parameter"),M->GetScalarParameterValue(FMaterialParameterInfo(TEXT("DenseCanopyStrength")),Strength));TestEqual(TEXT("Asset is unchanged without local request"),Strength,0.f);TestTrue(TEXT("Temporal masking preserved"),M->GetBlendMode()==BLEND_Masked);return true;
}
#endif
