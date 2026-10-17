#include "PokeMonsterNPCAnimInstance.h"
#include "PokeMonsterNPCVisualActor.h"
#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimSequence.h"
#include "AnimationRuntime.h"
#include "BoneContainer.h"
namespace
{
struct FPresentationSpring
{
 float Angle=0.f, Velocity=0.f;
 void Step(float Target,float Delta,float Limit)
 {
  float Remaining=FMath::Clamp(Delta,0.f,.1f);
  while(Remaining>0.f)
  {
   const float Dt=FMath::Min(Remaining,1.f/120.f);
   Velocity+=((Target-Angle)*90.f-Velocity*15.f)*Dt;Angle+=Velocity*Dt;
   const float Clamped=FMath::Clamp(Angle,-Limit,Limit);if(Clamped!=Angle)Velocity=0.f;
   Angle=Clamped;Remaining-=Dt;
  }
 }
};
struct FNPCPresentationProxy final : FAnimInstanceProxy
{
 explicit FNPCPresentationProxy(UAnimInstance* Instance):FAnimInstanceProxy(Instance){}
 UAnimSequence *Idle=nullptr,*Talk=nullptr,*Walk=nullptr,*TurnLeft=nullptr,*TurnRight=nullptr;
 float Alpha=0.f,IdleTime=0.f,TalkTime=0.f,WalkTime=0.f,TurnTime=0.f,WalkAlpha=0.f,Rate=0.f,TurnAlpha=0.f;
 float PreviousYaw=0.f,PreviousSpeed=0.f,AngularSpeed=0.f;bool bPrevious=false,bAccessories=false;
 FName CapeUpper,CapeLower,CapeLeft,CapeRight,Bag;
 FPresentationSpring CapePitch,CapeSwing,BagSwing;
 virtual void PreUpdate(UAnimInstance* Instance,float Delta) override
 {
  FAnimInstanceProxy::PreUpdate(Instance,Delta);
  auto* Actor=Cast<APokeMonsterNPCVisualActor>(Instance->GetOwningActor());if(!Actor)return;
  Actor->SampleMotion(Delta);
  Idle=Actor->IdleAnimation;Talk=Actor->ConversationAnimation;
  Walk=Actor->bEnableMotionPresentation?Actor->WalkAnimation.Get():nullptr;
  TurnLeft=Actor->bEnableMotionPresentation?Actor->TurnLeftAnimation.Get():nullptr;
  TurnRight=Actor->bEnableMotionPresentation?Actor->TurnRightAnimation.Get():nullptr;
  const float Blend=FMath::Max(Actor->MotionBlendSeconds,.05f);
  Alpha=FMath::FInterpConstantTo(Alpha,Actor->IsConversing()&&Talk?1.f:0.f,Delta,1.f/.18f);
  const float Speed=Actor->PresentationSpeed;
  Rate=Walk&&Speed>3.f?FMath::Clamp(Speed/FMath::Max(Actor->AuthoredWalkSpeed,1.f),.05f,3.f):0.f;
  WalkAlpha=FMath::FInterpConstantTo(WalkAlpha,Rate>0.f&&!Actor->IsConversing()?1.f:0.f,Delta,1.f/Blend);
  const float Yaw=Actor->GetActorRotation().Yaw,Dt=FMath::Max(Delta,.001f);
  AngularSpeed=bPrevious&&Delta<.25f?FMath::Clamp(FMath::FindDeltaAngleDegrees(PreviousYaw,Yaw)/Dt,-360.f,360.f):0.f;
  const float TurnTarget=Speed<3.f&&!Actor->IsConversing()&&(TurnLeft||TurnRight)?FMath::Clamp(FMath::Abs(AngularSpeed)/90.f,0.f,1.f):0.f;
  TurnAlpha=FMath::FInterpConstantTo(TurnAlpha,TurnTarget,Delta,1.f/Blend);
  const float Acceleration=bPrevious&&Delta<.25f?FMath::Clamp((Speed-PreviousSpeed)/Dt,-600.f,600.f):0.f;
  bAccessories=Actor->bEnableAccessoryMotion;
  CapeUpper=Actor->CapeUpperBone;CapeLower=Actor->CapeLowerBone;CapeLeft=Actor->CapeLeftBone;CapeRight=Actor->CapeRightBone;Bag=Actor->BagBone;
  CapePitch.Step(bAccessories?FMath::Clamp(Speed/FMath::Max(Actor->AuthoredWalkSpeed,1.f)*2.f+Acceleration*.003f,-1.f,5.f):0.f,Delta,6.f);
  CapeSwing.Step(bAccessories?-AngularSpeed*.012f:0.f,Delta,5.f);
  BagSwing.Step(bAccessories?AngularSpeed*.008f+Acceleration*.002f:0.f,Delta,4.f);
  PreviousYaw=Yaw;PreviousSpeed=Speed;bPrevious=true;
 }
 virtual void Update(float Delta) override
 {
  if(Idle)IdleTime=FMath::Fmod(IdleTime+Delta,FMath::Max(Idle->GetPlayLength(),.01f));
  if(Talk)TalkTime=FMath::Fmod(TalkTime+Delta,FMath::Max(Talk->GetPlayLength(),.01f));
  // Keep phase through stops. While blending out, continue slowly instead of freezing one airborne foot.
  if(Walk&&WalkAlpha>0.f)WalkTime=FMath::Fmod(WalkTime+Delta*FMath::Max(Rate,.15f*WalkAlpha),FMath::Max(Walk->GetPlayLength(),.01f));
  UAnimSequence* Turn=AngularSpeed>=0.f?TurnLeft:TurnRight;
  if(Turn&&TurnAlpha>0.f)TurnTime=FMath::Fmod(TurnTime+Delta*FMath::Max(FMath::Abs(AngularSpeed)/90.f,.15f),FMath::Max(Turn->GetPlayLength(),.01f));
 }
 virtual bool Evaluate(FPoseContext& Output) override
 {
  Output.ResetToRefPose();if(!Idle)return true;
  FPoseContext Base(Output);Base.ResetToRefPose();FAnimationPoseData A(Base),Result(Output);
  Idle->GetAnimationPose(A,FAnimExtractContext(IdleTime,false));
  if(Walk&&WalkAlpha>0.f)
  {
   FPoseContext Moving(Output);Moving.ResetToRefPose();FAnimationPoseData B(Moving);
   Walk->GetAnimationPose(B,FAnimExtractContext(WalkTime,false));FAnimationRuntime::BlendTwoPosesTogether(A,B,1.f-WalkAlpha,Result);
  }
  else
  {
   UAnimSequence* Turn=AngularSpeed>=0.f?TurnLeft:TurnRight;
   if(Turn&&TurnAlpha>0.f)
   {
    FPoseContext Turning(Output);Turning.ResetToRefPose();FAnimationPoseData B(Turning);
    Turn->GetAnimationPose(B,FAnimExtractContext(TurnTime,false));FAnimationRuntime::BlendTwoPosesTogether(A,B,1.f-TurnAlpha,Result);
   }
   else Idle->GetAnimationPose(Result,FAnimExtractContext(IdleTime,false));
  }
  if(Talk&&Alpha>0.f)
  {
   FPoseContext Current(Output),Talking(Output);Current.Pose=Output.Pose;Current.Curve=Output.Curve;Current.CustomAttributes=Output.CustomAttributes;Talking.ResetToRefPose();
   FAnimationPoseData B(Talking),C(Current);Talk->GetAnimationPose(B,FAnimExtractContext(TalkTime,false));FAnimationRuntime::BlendTwoPosesTogether(C,B,1.f-Alpha,Result);
  }
  if(bAccessories)
  {
   const FBoneContainer& Bones=Output.Pose.GetBoneContainer();
   auto Offset=[&](FName Name,float Pitch,float Swing)
   {
    const int32 SkeletonIndex=Bones.GetReferenceSkeleton().FindBoneIndex(Name);if(SkeletonIndex==INDEX_NONE)return;
    const auto Index=Bones.MakeCompactPoseIndex(FMeshPoseBoneIndex(SkeletonIndex));if(Index.GetInt()==INDEX_NONE)return;
    FQuat ParentRotation=FQuat::Identity;auto Parent=Bones.GetParentBoneIndex(Index);
    while(Parent.GetInt()!=INDEX_NONE){ParentRotation=Output.Pose[Parent].GetRotation()*ParentRotation;Parent=Bones.GetParentBoneIndex(Parent);}
    const FQuat Delta=FQuat(FVector::YAxisVector,FMath::DegreesToRadians(Pitch))*FQuat(FVector::XAxisVector,FMath::DegreesToRadians(Swing));
    auto& T=Output.Pose[Index];T.SetRotation((ParentRotation.Inverse()*Delta*ParentRotation*T.GetRotation()).GetNormalized());
   };
   Offset(CapeUpper,CapePitch.Angle,CapeSwing.Angle*.3f);Offset(CapeLower,CapePitch.Angle*.3f,CapeSwing.Angle*.4f);
   Offset(CapeLeft,CapePitch.Angle*.25f,CapeSwing.Angle*.5f);Offset(CapeRight,CapePitch.Angle*.25f,CapeSwing.Angle*.5f);
   Offset(Bag,BagSwing.Angle,BagSwing.Angle*.25f);Output.Pose.NormalizeRotations();
  }
  return true;
 }
 virtual void PostUpdate(UAnimInstance* Instance) const override
 {
  FAnimInstanceProxy::PostUpdate(Instance);auto* V=CastChecked<UPokeMonsterNPCAnimInstance>(Instance);
  V->ConversationAlpha=Alpha;V->WalkAlpha=WalkAlpha;V->WalkPlayRate=Rate;V->TurnAlpha=TurnAlpha;V->CapePitch=CapePitch.Angle;V->CapeSwing=CapeSwing.Angle;V->BagSwing=BagSwing.Angle;
 }
};
}
FAnimInstanceProxy* UPokeMonsterNPCAnimInstance::CreateAnimInstanceProxy(){return new FNPCPresentationProxy(this);}
void UPokeMonsterNPCAnimInstance::DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy){delete Proxy;}
