#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Animation/AnimSequence.h"
#include "Animation/Skeleton.h"
#include "Engine/SkeletalMesh.h"
#include "../Characters/PokeMonsterNPCMotionV3VisualActor.h"
#include "../Characters/PokeMonsterNPCMotionV3AnimInstance.h"
#include "Components/SkeletalMeshComponent.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPMNPCMotionV3Test,"PokeMonster.NPC.MotionV3.AnatomicalLegAxes",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPMNPCMotionV3Test::RunTest(const FString&)
{
 auto* M=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/NPCs/RangerMotionV3/Meshes/SK_Ranger_AQV3"));
 auto* Walk=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/NPCs/RangerMotionV3/Animations/A_Ranger_Walk_AQV3"));
 if(!TestNotNull(TEXT("Independent V3 mesh"),M)||!TestNotNull(TEXT("Independent V3 walk"),Walk))return false;
 const auto& Ref=Walk->GetSkeleton()->GetReferenceSkeleton();
 TestTrue(TEXT("V3 skeleton matches mesh"),M->GetSkeleton()==Walk->GetSkeleton());
 TestFalse(TEXT("In-place animation"),Walk->bEnableRootMotion);
 TestTrue(TEXT("150 cm/s with a 120 cm stride pair"),FMath::IsNearlyEqual(Walk->GetPlayLength(),.8,.0001));
 for(int32 Frame=0;Frame<=48;++Frame)
 {
  TArray<FTransform> CS;CS.SetNum(Ref.GetNum());
  for(int32 I=0;I<CS.Num();++I)
  {
   FTransform Local;Walk->GetBoneTransform(Local,FSkeletonPoseBoneIndex(I),FAnimExtractContext(Frame/60.,false),true);
   const int32 Parent=Ref.GetParentIndex(I);CS[I]=Parent<0?Local:Local*CS[Parent];
  }
  for(const TCHAR* Side:{TEXT("l"),TEXT("r")})
  {
   const FVector Hip=CS[Ref.FindBoneIndex(FName(FString(TEXT("thigh_"))+Side))].GetTranslation();
   const FVector Knee=CS[Ref.FindBoneIndex(FName(FString(TEXT("shin_"))+Side))].GetTranslation();
   const FVector Foot=CS[Ref.FindBoneIndex(FName(FString(TEXT("foot_"))+Side))].GetTranslation();
   const FVector Axis=(Foot-Hip).GetSafeNormal();
   const FVector Pole=(FVector::XAxisVector-Axis*FVector::DotProduct(FVector::XAxisVector,Axis)).GetSafeNormal();
   TestTrue(TEXT("Knee bends toward real UE forward +X, never backward"),FVector::DotProduct(Knee-Hip,Pole)>0.1);
   TestTrue(TEXT("Foot stays in its sagittal track"),FMath::Abs(Foot.Y)<15.6);
  }
 }
 const auto* Default=GetDefault<APokeMonsterNPCMotionV3VisualActor>();
 TestTrue(TEXT("V3-only animation class"),Default->Visual->GetAnimClass()==UPokeMonsterNPCMotionV3AnimInstance::StaticClass());
 TestEqual(TEXT("No gameplay collision added"),Default->Visual->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
 return true;
}
#endif
