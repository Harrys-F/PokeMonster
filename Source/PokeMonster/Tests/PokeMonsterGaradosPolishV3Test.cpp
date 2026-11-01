#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequence.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Rendering/SkeletalMeshRenderData.h"
#include "Rendering/SkinWeightVertexBuffer.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosPolishHeading,"PokeMonster.GaradosPolishV3.DelayedHeadingWrapPauseAndFrameRates",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosPolishHeading::RunTest(const FString&)
{
 FPokeMonsterSwimHeadingHistory A,B;A.Reset(170);B.Reset(170);
 for(int I=1;I<=120;++I)A.Advance(FRotator::NormalizeAxis(170+30.f*I/60),1.f/60,1.1f,32);
 for(int I=1;I<=40;++I)B.Advance(FRotator::NormalizeAxis(170+30.f*I/20),1.f/20,1.1f,32);
 TestEqual(TEXT("Head leads at current heading"),A.Offsets[0],0.f);
 TestTrue(TEXT("Mid-body follows a past heading"),A.Offsets[10]<-15&&A.Offsets[10]>-19);
 TestTrue(TEXT("Tail is last and bounded"),A.Offsets[19]<=-31.9f&&A.Offsets[19]>=-32.f);
 for(int I=0;I<20;++I)TestTrue(TEXT("Equivalent turning across variable frame rates"),FMath::IsNearlyEqual(A.Offsets[I],B.Offsets[I],.05f));
 const auto Before=A.Offsets;A.Advance(-100,0,1.1f,32);TestTrue(TEXT("Pause does not age heading history"),A.Offsets==Before);
 for(int I=0;I<150;++I)A.Advance(-130,1.f/60,1.1f,32);
 TestTrue(TEXT("After settling all segments follow final heading"),A.Offsets.ContainsByPredicate([](float X){return FMath::Abs(X)>.01f;})==false);
 A.Advance(90,2.f,1.1f,32);TestTrue(TEXT("Teleport/timing reset cannot leave a bent tail"),A.Offsets.ContainsByPredicate([](float X){return X!=0;})==false);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosPolishDamping,"PokeMonster.GaradosPolishV3.FrameIndependentPoseDamping",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosPolishDamping::RunTest(const FString&)
{
 using V=APokeMonsterCreatureVisualActor;float A=0,B=0;
 for(int I=0;I<60;++I){const float P=A;A=V::SmoothSwimValue(A,1,1.f/60,.55f);TestTrue(TEXT("No overshoot or pose snap"),A>=P&&A-P<.031f);}
 for(int I=0;I<20;++I)B=V::SmoothSwimValue(B,1,1.f/20,.55f);
 TestTrue(TEXT("Same pose after equal elapsed time"),FMath::IsNearlyEqual(A,B,.00001f));TestEqual(TEXT("Pause holds filtered pose"),V::SmoothSwimValue(A,0,0,.55f),A);
 TestTrue(TEXT("Long frame remains within pose endpoints"),V::SmoothSwimValue(A,0,.6f,.55f)>0&&V::SmoothSwimValue(A,0,.6f,.55f)<A);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosPolishEvaluated,"PokeMonster.GaradosPolishV3.EvaluatedPoseBoundsAndLandIsolation",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosPolishEvaluated::RunTest(const FString&)
{
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Garados.DA_Garados"));if(!TestNotNull(TEXT("Existing species"),S))return false;
 auto* D=S->GetVisuals().Presentation.LoadSynchronous();if(!TestNotNull(TEXT("Presentation"),D)||!TestNotNull(TEXT("Water mesh"),D->SwimMesh.Get()))return false;
 TestTrue(TEXT("New data validates"),D->GetValidationErrors().IsEmpty());TestTrue(TEXT("Following is explicitly enabled on Garados only"),D->SwimBodyFollowSeconds>0);
 for(const auto* C:{D->SwimIdleClip.Get(),D->SwimClip.Get(),D->SwimSlowClip.Get(),D->SwimFastClip.Get(),D->SwimObserveClip.Get(),D->SwimTurnLeftClip.Get(),D->SwimTurnRightClip.Get()})
 {if(!TestNotNull(TEXT("Polished water clip"),C))return false;TestTrue(TEXT("Only V3 swim references changed"),C->GetPathName().Contains(TEXT("/WaterV3/")));TestTrue(TEXT("All looping poses share a cycle"),FMath::IsNearlyEqual(C->GetPlayLength(),2.8f,.001f));TestEqual(TEXT("Existing exact water skeleton"),C->GetSkeleton(),D->SwimMesh->GetSkeleton());}
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* V=W->SpawnActor<APokeMonsterCreatureVisualActor>();TestTrue(TEXT("Normal species binding"),V->SetSpecies(S));V->AquaticPoseAlpha=1;V->Tick(1.f/60);V->Mesh->bPauseAnims=false;TArray<FVector3f> Vertices;TArray<FMatrix44f> RefToLocal;float MaxRadius=0,InitialHeadZ=0;FVector LastHead=FVector::ZeroVector;bool HaveHead=false;
 for(int I=0;I<480;++I)
 {
  const float T=I/60.f,Speed=T<1?0:T<2?35:T<4?125:T<5?70:0;
  const float Yaw=T<2?0:T<4?(T-2)*35:T<6?70-(T-4)*35:0;
  V->SetActorLocation(V->GetActorLocation()+FVector(Speed/60,0,0));V->SetActorRotation(FRotator(0,Yaw,0));V->Tick(1.f/60);
  const float Observe=FMath::SmoothStep(0.f,1.f,FMath::Clamp((T-5)/2.f,0.f,1.f));V->SwimObserveAlpha=Observe;
  V->Mesh->TickAnimation(1.f/60,false);V->Mesh->RefreshBoneTransforms();
  const FVector Head=V->Mesh->GetSocketTransform(TEXT("head"),RTS_Component).GetLocation();TestFalse(TEXT("Actual evaluated head is finite"),Head.ContainsNaN());
  if(HaveHead)TestTrue(TEXT("No head jump while speeding, turning or raising"),FVector::Dist(LastHead,Head)<12.f);else InitialHeadZ=Head.Z;LastHead=Head;HaveHead=true;
  if(I%30==0)
  {
   V->Mesh->GetCurrentRefToLocalMatrices(RefToLocal,0);const auto& LOD=D->SwimMesh->GetResourceForRendering()->LODRenderData[0];USkinnedMeshComponent::ComputeSkinnedPositions(V->Mesh,Vertices,RefToLocal,LOD,LOD.SkinWeightVertexBuffer);if(!TestTrue(TEXT("Actual full surface evaluated"),Vertices.Num()>20000))return false;
   for(const auto& P:Vertices){const FVector Point(P);TestFalse(TEXT("Skin remains finite"),Point.ContainsNaN());MaxRadius=FMath::Max(MaxRadius,float(FVector2D(Point).Size()));}
  }
 }
 AddInfo(FString::Printf(TEXT("Actual evaluated skin radius %.2f cm; head rise %.2f cm"),MaxRadius,LastHead.Z-InitialHeadZ));
 TestTrue(TEXT("Full mesh evaluation is not a zero pose"),MaxRadius>300);TestTrue(TEXT("Actual observation lifts the head"),LastHead.Z-InitialHeadZ>60);
 TestTrue(FString::Printf(TEXT("Complete deformed surface stays in unchanged 400cm envelope: %.2f"),MaxRadius),MaxRadius<=D->SwimClearanceRadiusCm);
 V->AquaticPoseAlpha=0;V->Tick(.016f);V->Mesh->TickAnimation(.016f,false);V->Mesh->RefreshBoneTransforms();TestEqual(TEXT("Original land/battle mesh restored"),V->Mesh->GetSkeletalMeshAsset(),D->Mesh.Get());TestTrue(TEXT("No water heading correction persists on land"),V->SwimBodyYawOffsets.IsEmpty());TestEqual(TEXT("Original seven land/battle clips retained"),D->Clips.Num(),7);return true;
}
#endif
