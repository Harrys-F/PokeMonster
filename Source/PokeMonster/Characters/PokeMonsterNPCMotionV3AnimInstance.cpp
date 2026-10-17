#include "PokeMonsterNPCMotionV3AnimInstance.h"
#include "PokeMonsterNPCVisualActor.h"
#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimSequence.h"
#include "AnimationRuntime.h"
#include "BoneContainer.h"
#include "Components/SkeletalMeshComponent.h"
namespace
{
struct FNPCMotionV3PresentationSpring
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
struct FNPCMotionV3Proxy final : FAnimInstanceProxy
{
 explicit FNPCMotionV3Proxy(UAnimInstance* Instance):FAnimInstanceProxy(Instance){}
 UAnimSequence *Idle=nullptr,*Talk=nullptr,*Walk=nullptr,*TurnLeft=nullptr,*TurnRight=nullptr;
 float Alpha=0.f,IdleTime=0.f,TalkTime=0.f,WalkTime=0.f,TurnTime=0.f,WalkAlpha=0.f,Rate=0.f,TurnAlpha=0.f;
 float PreviousYaw=0.f,PreviousSpeed=0.f,AngularSpeed=0.f;bool bPrevious=false,bAccessories=false;
 FName CapeUpper,CapeLower,CapeLeft,CapeRight,Bag;
 FNPCMotionV3PresentationSpring CapePitch,CapeSwing,BagSwing;
 FTransform ComponentWorld=FTransform::Identity;
 struct FPlant { bool Active=false; FTransform World=FTransform::Identity; } Plants[2];
 bool bWasWalking=false; float SpeedSample=0.f;
 float MaxPlantCorrection=0.f;
 virtual void PreUpdate(UAnimInstance* Instance,float Delta) override
 {
  FAnimInstanceProxy::PreUpdate(Instance,Delta);
  auto* Actor=Cast<APokeMonsterNPCVisualActor>(Instance->GetOwningActor());if(!Actor)return;
  Actor->SampleMotion(Delta);
  ComponentWorld=Actor->Visual->GetComponentTransform();
  Idle=Actor->IdleAnimation;Talk=Actor->ConversationAnimation;
  Walk=Actor->bEnableMotionPresentation?Actor->WalkAnimation.Get():nullptr;
  TurnLeft=Actor->bEnableMotionPresentation?Actor->TurnLeftAnimation.Get():nullptr;
  TurnRight=Actor->bEnableMotionPresentation?Actor->TurnRightAnimation.Get():nullptr;
  const float Blend=FMath::Max(Actor->MotionBlendSeconds,.05f);
  Alpha=FMath::FInterpConstantTo(Alpha,Actor->IsConversing()&&Talk?1.f:0.f,Delta,1.f/.18f);
  const float Speed=Actor->PresentationSpeed;SpeedSample=Speed;
  Rate=Walk&&Speed>3.f?FMath::Clamp(Speed/FMath::Max(Actor->AuthoredWalkSpeed,1.f),.05f,3.f):0.f;
  WalkAlpha=FMath::FInterpConstantTo(WalkAlpha,Rate>0.f&&!Actor->IsConversing()?1.f:0.f,Delta,1.f/Blend);
  const float Yaw=Actor->GetActorRotation().Yaw,Dt=FMath::Max(Delta,.001f);
  AngularSpeed=bPrevious&&Delta<.25f?FMath::Clamp(FMath::FindDeltaAngleDegrees(PreviousYaw,Yaw)/Dt,-360.f,360.f):0.f;
  const float TurnTarget=Speed<3.f&&(TurnLeft||TurnRight)?FMath::Clamp(FMath::Abs(AngularSpeed)/90.f,0.f,1.f):0.f;
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
   FAnimationPoseData B(Talking),C(Current);Talk->GetAnimationPose(B,FAnimExtractContext(TalkTime,false));
   // Conversation affects upper body only. Keep the locomotion/pivot leg contacts.
   const FBoneContainer& BC=Output.Pose.GetBoneContainer();
   const int32 Spine=BC.GetReferenceSkeleton().FindBoneIndex(TEXT("spine"));
   for(FCompactPoseBoneIndex I:Output.Pose.ForEachBoneIndex())
   {
    int32 S=BC.GetSkeletonIndex(I);bool Upper=false;
    while(S!=INDEX_NONE){if(S==Spine){Upper=true;break;}S=BC.GetReferenceSkeleton().GetParentIndex(S);}
    if(Upper){FTransform T;T.Blend(Current.Pose[I],Talking.Pose[I],Alpha);Output.Pose[I]=T;}
   }
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
  LockFeet(Output);
  return true;
 }
 void LockFeet(FPoseContext& Output)
 {
  // Flat-ground contact stabilization only. No world queries, gameplay motion,
  // terrain IK, new collision, or UObject access from the animation worker.
  FCSPose<FCompactPose> CSP;CSP.InitPose(Output.Pose);
  const FBoneContainer& BC=Output.Pose.GetBoneContainer();MaxPlantCorrection=0.f;
  const float WalkPhase=Walk?WalkTime/FMath::Max(Walk->GetPlayLength(),.01f):0.f;
  UAnimSequence* Turn=AngularSpeed>=0?TurnLeft:TurnRight;
  const float TurnPhase=Turn?TurnTime/FMath::Max(Turn->GetPlayLength(),.01f):0.f;
  for(int32 Side=0;Side<2;++Side)
  {
   const FString Suffix=Side==0?TEXT("_l"):TEXT("_r");
   auto Index=[&](const TCHAR* N){return BC.MakeCompactPoseIndex(FMeshPoseBoneIndex(BC.GetReferenceSkeleton().FindBoneIndex(FName(FString(N)+Suffix))));};
   auto Hip=Index(TEXT("thigh")),Knee=Index(TEXT("shin")),Foot=Index(TEXT("foot"));
   if(Hip.GetInt()<0||Knee.GetInt()<0||Foot.GetInt()<0)continue;
   FTransform H=CSP.GetComponentSpaceTransform(Hip),K=CSP.GetComponentSpaceTransform(Knee),F=CSP.GetComponentSpaceTransform(Foot);
   const float Phase=FMath::Fmod((SpeedSample>3.f?WalkPhase:TurnPhase)+Side*.5f,1.f);
   const bool Moving=SpeedSample>3.f||FMath::Abs(AngularSpeed)>3.f;
   const bool Stance=!Moving||Phase<.5f;
   FPlant& Plant=Plants[Side];
   if(!Stance){Plant.Active=false;continue;}
   if(!Plant.Active){Plant.World=F*ComponentWorld;Plant.Active=true;}
   FTransform Goal=Plant.World.GetRelativeTransform(ComponentWorld);
   FVector Target=Goal.GetTranslation();
   const FVector HP=H.GetTranslation(),KP=K.GetTranslation(),FP=F.GetTranslation();
   const double A=(KP-HP).Size(),B=(FP-KP).Size();
   FVector D=Target-HP;double Len=D.Size();
   // Drop stale pins after relocation or a large unavailable movement step.
   if((Target-FP).Size()>25.||Len<.01){Plant.World=F*ComponentWorld;continue;}
   Len=FMath::Clamp(Len,FMath::Abs(A-B)+.01,A+B-.01);const FVector Dir=D.GetSafeNormal();Target=HP+Dir*Len;
   const double Along=(A*A-B*B+Len*Len)/(2*Len);
   const FVector Pole=FVector::XAxisVector;
   const FVector Bend=(Pole-Dir*FVector::DotProduct(Pole,Dir)).GetSafeNormal();
   const FVector NewKnee=HP+Dir*Along+Bend*FMath::Sqrt(FMath::Max(0.,A*A-Along*Along));
   H.SetRotation((FQuat::FindBetweenNormals((KP-HP).GetSafeNormal(),(NewKnee-HP).GetSafeNormal())*H.GetRotation()).GetNormalized());
   K.SetRotation((FQuat::FindBetweenNormals((FP-KP).GetSafeNormal(),(Target-NewKnee).GetSafeNormal())*K.GetRotation()).GetNormalized());
   K.SetTranslation(NewKnee);F.SetTranslation(Target);F.SetRotation(Goal.GetRotation());
   MaxPlantCorrection=FMath::Max(MaxPlantCorrection,static_cast<float>((Target-FP).Size()));
   CSP.SetComponentSpaceTransform(Hip,H);CSP.SetComponentSpaceTransform(Knee,K);CSP.SetComponentSpaceTransform(Foot,F);
  }
  FCSPose<FCompactPose>::ConvertComponentPosesToLocalPoses(CSP,Output.Pose);Output.Pose.NormalizeRotations();
 }
 virtual void PostUpdate(UAnimInstance* Instance) const override
 {
  FAnimInstanceProxy::PostUpdate(Instance);auto* V=CastChecked<UPokeMonsterNPCMotionV3AnimInstance>(Instance);
  V->ConversationAlpha=Alpha;V->WalkAlpha=WalkAlpha;V->WalkPlayRate=Rate;V->TurnAlpha=TurnAlpha;V->CapePitch=CapePitch.Angle;V->CapeSwing=CapeSwing.Angle;V->BagSwing=BagSwing.Angle;V->PlantCorrectionCm=MaxPlantCorrection;
 }
};
}
FAnimInstanceProxy* UPokeMonsterNPCMotionV3AnimInstance::CreateAnimInstanceProxy(){return new FNPCMotionV3Proxy(this);}
void UPokeMonsterNPCMotionV3AnimInstance::DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy){delete Proxy;}
