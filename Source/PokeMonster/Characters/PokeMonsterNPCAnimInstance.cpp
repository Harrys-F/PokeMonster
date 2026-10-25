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
 UAnimSequence *Idle=nullptr,*Talk=nullptr,*Walk=nullptr,*TurnLeft=nullptr,*TurnRight=nullptr,*Run=nullptr,*Greeting=nullptr;
 float Alpha=0.f,IdleTime=0.f,TalkTime=0.f,WalkTime=0.f,TurnTime=0.f,WalkAlpha=0.f,Rate=0.f,TurnAlpha=0.f;
 float PreviousYaw=0.f,PreviousSpeed=0.f,AngularSpeed=0.f;bool bPrevious=false,bAccessories=false;
 float RunAlpha=0.f,LocomotionPhase=0.f,GreetingTime=1000.f,GreetingWeight=0.f,MaxFootCorrection=0.f;
 int32 GreetingSerial=0;bool bContacts=false,bUpperConversation=false;
 FTransform ComponentWorld=FTransform::Identity;
 struct FPlant {bool Active=false;FTransform World=FTransform::Identity;} Plants[2];
 FName CapeUpper,CapeLower,CapeLeft,CapeRight,Bag;
 FPresentationSpring CapePitch,CapeSwing,BagSwing;
 virtual void PreUpdate(UAnimInstance* Instance,float Delta) override
 {
  FAnimInstanceProxy::PreUpdate(Instance,Delta);
  auto* Actor=Cast<APokeMonsterNPCVisualActor>(Instance->GetOwningActor());if(!Actor)return;
  Actor->SampleMotion(Delta);
  Idle=Actor->IdleAnimation;Talk=Actor->ConversationAnimation;
  Run=Actor->bEnableMotionPresentation?Actor->RunAnimation.Get():nullptr;Greeting=Actor->GreetingAnimation;
  bContacts=Actor->bEnableFootContacts;bUpperConversation=Actor->bUpperBodyConversation;
  ComponentWorld=Actor->Visual->GetComponentTransform();
  if(Actor->GreetingSerial!=GreetingSerial){GreetingSerial=Actor->GreetingSerial;GreetingTime=0.f;}
  Walk=Actor->bEnableMotionPresentation?Actor->WalkAnimation.Get():nullptr;
  TurnLeft=Actor->bEnableMotionPresentation?Actor->TurnLeftAnimation.Get():nullptr;
  TurnRight=Actor->bEnableMotionPresentation?Actor->TurnRightAnimation.Get():nullptr;
  const float Blend=FMath::Max(Actor->MotionBlendSeconds,.05f);
  Alpha=FMath::FInterpConstantTo(Alpha,Actor->IsConversing()&&Talk?1.f:0.f,Delta,1.f/.18f);
  const float Speed=Actor->PresentationSpeed;
  const float RunTarget=Run?FMath::Clamp((Speed-Actor->AuthoredWalkSpeed*.95f)/FMath::Max(Actor->AuthoredRunSpeed-Actor->AuthoredWalkSpeed*.95f,1.f),0.f,1.f):0.f;
  RunAlpha=FMath::FInterpConstantTo(RunAlpha,RunTarget,Delta,1.f/Blend);
  const float ReferenceSpeed=FMath::Lerp(Actor->AuthoredWalkSpeed,Actor->AuthoredRunSpeed,RunAlpha);
  Rate=Walk&&Speed>3.f?FMath::Clamp(Speed/FMath::Max(ReferenceSpeed,1.f),.05f,3.f):0.f;
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
  if(Greeting)GreetingTime+=Delta;
  const float GreetingLength=Greeting?Greeting->GetPlayLength():0.f;
  GreetingWeight=Greeting&&GreetingTime<GreetingLength?FMath::Min(FMath::Clamp(GreetingTime/.18f,0.f,1.f),FMath::Clamp((GreetingLength-GreetingTime)/.20f,0.f,1.f)):0.f;
  // Keep phase through stops. While blending out, continue slowly instead of freezing one airborne foot.
  if(Walk&&WalkAlpha>0.f)
  {
   const float Duration=FMath::Lerp(Walk->GetPlayLength(),Run?Run->GetPlayLength():Walk->GetPlayLength(),RunAlpha);
   LocomotionPhase=FMath::Fmod(LocomotionPhase+Delta*FMath::Max(Rate,.15f*WalkAlpha)/FMath::Max(Duration,.01f),1.f);
   WalkTime=LocomotionPhase*Walk->GetPlayLength();
  }
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
   Walk->GetAnimationPose(B,FAnimExtractContext(WalkTime,false));
   if(Run&&RunAlpha>0.f)
   {
    FPoseContext Running(Output),Blended(Output);Running.ResetToRefPose();Blended.ResetToRefPose();FAnimationPoseData R(Running),Combined(Blended);
    Run->GetAnimationPose(R,FAnimExtractContext(LocomotionPhase*Run->GetPlayLength(),false));
    FAnimationRuntime::BlendTwoPosesTogether(B,R,1.f-RunAlpha,Combined);
    FAnimationRuntime::BlendTwoPosesTogether(A,Combined,1.f-WalkAlpha,Result);
   }
   else FAnimationRuntime::BlendTwoPosesTogether(A,B,1.f-WalkAlpha,Result);
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
   if(bUpperConversation)BlendUpper(Output,Current,Talking,Alpha);
   else FAnimationRuntime::BlendTwoPosesTogether(C,B,1.f-Alpha,Result);
  }
  if(Greeting&&GreetingWeight>0.f)
  {
   FPoseContext Current(Output),Gesture(Output);Current.Pose=Output.Pose;Current.Curve=Output.Curve;Current.CustomAttributes=Output.CustomAttributes;Gesture.ResetToRefPose();FAnimationPoseData G(Gesture);
   Greeting->GetAnimationPose(G,FAnimExtractContext(GreetingTime,false));BlendUpper(Output,Current,Gesture,GreetingWeight);
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
  if(bContacts)LockFeet(Output);
  return true;
 }
 void BlendUpper(FPoseContext& Output,const FPoseContext& Current,const FPoseContext& Other,float Weight)
 {
  const FBoneContainer& BC=Output.Pose.GetBoneContainer();int32 Spine=BC.GetReferenceSkeleton().FindBoneIndex(TEXT("spine"));if(Spine==INDEX_NONE)Spine=BC.GetReferenceSkeleton().FindBoneIndex(TEXT("chest"));
  for(FCompactPoseBoneIndex I:Output.Pose.ForEachBoneIndex())
  {
   int32 S=BC.GetSkeletonIndex(I);bool Upper=false;
   while(S!=INDEX_NONE){if(S==Spine){Upper=true;break;}S=BC.GetReferenceSkeleton().GetParentIndex(S);}
   if(Upper){FTransform T;T.Blend(Current.Pose[I],Other.Pose[I],Weight);Output.Pose[I]=T;}
  }
 }
 void LockFeet(FPoseContext& Output)
 {
  FCSPose<FCompactPose> CSP;CSP.InitPose(Output.Pose);const FBoneContainer& BC=Output.Pose.GetBoneContainer();MaxFootCorrection=0.f;
  UAnimSequence* Turn=AngularSpeed>=0.f?TurnLeft:TurnRight;
  const float TurnPhase=Turn?TurnTime/FMath::Max(Turn->GetPlayLength(),.01f):0.f;
  for(int32 Side=0;Side<2;++Side)
  {
   auto Index=[&](const TCHAR* N){return BC.MakeCompactPoseIndex(FMeshPoseBoneIndex(BC.GetReferenceSkeleton().FindBoneIndex(FName(FString(N)+(Side==0?TEXT("_l"):TEXT("_r"))))));};
   const auto Hip=Index(TEXT("thigh")),Knee=Index(TEXT("shin")),Foot=Index(TEXT("foot"));if(Hip.GetInt()<0||Knee.GetInt()<0||Foot.GetInt()<0)continue;
   FTransform H=CSP.GetComponentSpaceTransform(Hip),K=CSP.GetComponentSpaceTransform(Knee),F=CSP.GetComponentSpaceTransform(Foot);
   const bool Moving=Rate>0.f||FMath::Abs(AngularSpeed)>3.f;
   const float Phase=FMath::Fmod((Rate>0.f?LocomotionPhase:TurnPhase)+Side*.5f,1.f);
   FPlant& Plant=Plants[Side];if(Moving&&Phase>=.5f){Plant.Active=false;continue;}
   if(!Plant.Active){Plant.World=F*ComponentWorld;Plant.Active=true;}
   FTransform Goal=Plant.World.GetRelativeTransform(ComponentWorld);FVector Target=Goal.GetTranslation();
   const FVector HP=H.GetTranslation(),KP=K.GetTranslation(),FP=F.GetTranslation();const double A=(KP-HP).Size(),B=(FP-KP).Size();
   FVector D=Target-HP;double Length=D.Size();
   if((Target-FP).Size()>25.||Length<.01){Plant.World=F*ComponentWorld;continue;}
   Length=FMath::Clamp(Length,FMath::Abs(A-B)+.01,A+B-.01);const FVector Dir=D.GetSafeNormal();Target=HP+Dir*Length;
   const double Along=(A*A-B*B+Length*Length)/(2*Length);const FVector Pole=FVector::XAxisVector;
   const FVector Bend=(Pole-Dir*FVector::DotProduct(Pole,Dir)).GetSafeNormal();const FVector NewKnee=HP+Dir*Along+Bend*FMath::Sqrt(FMath::Max(0.,A*A-Along*Along));
   H.SetRotation((FQuat::FindBetweenNormals((KP-HP).GetSafeNormal(),(NewKnee-HP).GetSafeNormal())*H.GetRotation()).GetNormalized());
   K.SetRotation((FQuat::FindBetweenNormals((FP-KP).GetSafeNormal(),(Target-NewKnee).GetSafeNormal())*K.GetRotation()).GetNormalized());
   K.SetTranslation(NewKnee);F.SetTranslation(Target);F.SetRotation(Goal.GetRotation());MaxFootCorrection=FMath::Max(MaxFootCorrection,static_cast<float>((Target-FP).Size()));
   CSP.SetComponentSpaceTransform(Hip,H);CSP.SetComponentSpaceTransform(Knee,K);CSP.SetComponentSpaceTransform(Foot,F);
  }
  FCSPose<FCompactPose>::ConvertComponentPosesToLocalPoses(CSP,Output.Pose);Output.Pose.NormalizeRotations();
 }
 virtual void PostUpdate(UAnimInstance* Instance) const override
 {
  FAnimInstanceProxy::PostUpdate(Instance);auto* V=CastChecked<UPokeMonsterNPCAnimInstance>(Instance);
  V->RunAlpha=RunAlpha;V->GreetingAlpha=GreetingWeight;V->FootCorrectionCm=MaxFootCorrection;V->ConversationAlpha=Alpha;V->WalkAlpha=WalkAlpha;V->WalkPlayRate=Rate;V->TurnAlpha=TurnAlpha;V->CapePitch=CapePitch.Angle;V->CapeSwing=CapeSwing.Angle;V->BagSwing=BagSwing.Angle;
 }
};
}
FAnimInstanceProxy* UPokeMonsterNPCAnimInstance::CreateAnimInstanceProxy(){return new FNPCPresentationProxy(this);}
void UPokeMonsterNPCAnimInstance::DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy){delete Proxy;}
