#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequence.h"
#include "Engine/Engine.h"
#include "Engine/World.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGaradosWaterV4Shape,"PokeMonster.GaradosWaterV4.StrongerWaveAndAnchoredUprightPose",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGaradosWaterV4Shape::RunTest(const FString&)
{
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Garados.DA_Garados"));if(!TestNotNull(TEXT("Existing Garados"),S))return false;
 auto* D=S->GetVisuals().Presentation.LoadSynchronous();if(!TestNotNull(TEXT("Existing presentation"),D))return false;
 auto* Old=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/Creatures/Garados/WaterV3/Animations/A_Garados_SwimNormal_V3"));
 auto* OldObserve=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/Creatures/Garados/WaterV3/Animations/A_Garados_SwimObserve_V3"));
 if(!TestNotNull(TEXT("Retained V3 swim reference"),Old)||!TestNotNull(TEXT("Retained V3 observe reference"),OldObserve))return false;
 if(!TestTrue(TEXT("Presentation validates"),D->GetValidationErrors().IsEmpty()))return false;
 TestTrue(TEXT("V4 normal and observation bindings"),D->SwimClip->GetPathName().Contains(TEXT("/WaterV4/"))&&D->SwimObserveClip->GetPathName().Contains(TEXT("/WaterV4/")));
 TestTrue(TEXT("Unchanged quiet V3 idle"),D->SwimIdleClip->GetPathName().Contains(TEXT("/WaterV3/")));
 TestEqual(TEXT("Same skeleton, no retarget or replacement rig"),Old->GetSkeleton(),D->SwimClip->GetSkeleton());
 TestEqual(TEXT("V3 raising/lowering timing retained"),D->SwimObserveBlendSeconds,3.2f);
 TestEqual(TEXT("V3 tail-follow delay retained"),D->SwimBodyFollowSeconds,1.1f);
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* V=W->SpawnActor<APokeMonsterCreatureVisualActor>();if(!TestTrue(TEXT("Normal production species binding"),V->SetSpecies(S)))return false;V->AquaticPoseAlpha=1;V->Tick(.016f);
 struct FPose { FVector Head,Tail,Mid,Rear,Root; };
 auto Pose=[&](UAnimSequence* Clip,float Time)
 {
  V->Mesh->PlayAnimation(Clip,true);V->Mesh->SetPosition(Time,false);V->Mesh->TickAnimation(0,false);V->Mesh->RefreshBoneTransforms();
  auto Bone=[&](const TCHAR* Name){return V->Mesh->GetSocketTransform(Name,RTS_Component).GetLocation();};
  return FPose{Bone(TEXT("head")),Bone(TEXT("spine_19")),Bone(TEXT("spine_10")),Bone(TEXT("spine_14")),Bone(TEXT("root"))};
 };
 auto Sweep=[&](UAnimSequence* Clip)
 {
  TArray<FPose> P;for(int I=0;I<32;++I)P.Add(Pose(Clip,Clip->GetPlayLength()*I/32.f));FVector Sweep=FVector::ZeroVector;
  for(int I=0;I<16;++I){Sweep.X=FMath::Max(Sweep.X,FVector::DistXY(P[I].Tail,P[I+16].Tail));Sweep.Y=FMath::Max(Sweep.Y,FVector::DistXY(P[I].Mid,P[I+16].Mid));Sweep.Z=FMath::Max(Sweep.Z,FVector::DistXY(P[I].Head,P[I+16].Head));}return Sweep;
 };
 const FVector Before=Sweep(Old),After=Sweep(D->SwimClip.Get());
 TestTrue(TEXT("Clearly greater normal tail wave, not a global model rotation"),After.X>Before.X*2&&After.X>70);
 TestTrue(TEXT("Clearly greater middle-body wave"),After.Y>Before.Y*2&&After.Y>40);
 TestTrue(TEXT("Head remains calm while the tail travels"),After.Z<6&&After.X>After.Z*10);
 const FPose Flat=Pose(Old,0),Previous=Pose(OldObserve,0),Raised=Pose(D->SwimObserveClip.Get(),0);
 const float OldLift=Previous.Head.Z-Flat.Head.Z,NewLift=Raised.Head.Z-Flat.Head.Z;
 TestTrue(TEXT("Observation is substantially higher than V3"),NewLift>250&&NewLift>OldLift*2.4f);
 TestTrue(TEXT("Rear body remains at its existing water height"),FMath::Abs(Raised.Rear.Z-Flat.Rear.Z)<1&&FMath::Abs(Raised.Tail.Z-Flat.Tail.Z)<1);
 TestTrue(TEXT("No whole-model vertical translation"),Raised.Root.Equals(Flat.Root,.01));
 AddInfo(FString::Printf(TEXT("Actual V3/V4 tail sweep %.2f/%.2f cm, middle %.2f/%.2f cm; V4 head sweep %.2f cm; V3/V4 head lift %.2f/%.2f cm"),Before.X,After.X,Before.Y,After.Y,After.Z,OldLift,NewLift));
 return true;
}
#endif
