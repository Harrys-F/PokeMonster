#include "PokeMonsterCreaturePresentation.h"
#include "PokeMonsterCreatureSpeciesData.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimSequence.h"
#include "AnimationRuntime.h"
#include "Engine/SkeletalMesh.h"
APokeMonsterCreatureVisualActor::APokeMonsterCreatureVisualActor()
{
 PrimaryActorTick.bCanEverTick=true;
 Mesh=CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("CreatureMesh"));SetRootComponent(Mesh);
 Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);Mesh->AddTickPrerequisiteActor(this);
 Mesh->VisibilityBasedAnimTickOption=EVisibilityBasedAnimTickOption::OnlyTickPoseWhenRendered;
 Flame=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TailFlameOnly"));Flame->SetupAttachment(Mesh);
 Flame->SetCollisionEnabled(ECollisionEnabled::NoCollision);Flame->SetCastShadow(false);
 Flame->SetAbsolute(false,true,false);
}
bool APokeMonsterCreatureVisualActor::SetSpecies(const UPokeMonsterCreatureSpeciesData* Species)
{
 Presentation=Species?Species->GetVisuals().Presentation.LoadSynchronous():nullptr;
 if(!Presentation||!Presentation->Mesh){Mesh->SetSkeletalMesh(nullptr);Flame->SetVisibility(false);return false;}
 Mesh->SetSkeletalMesh(Presentation->Mesh);Mesh->SetAnimationMode(EAnimationMode::AnimationBlueprint);
 Mesh->SetAnimInstanceClass(UPokeMonsterCreatureAnimInstance::StaticClass());
 const bool bTail=Presentation->TailFlame&&Mesh->DoesSocketExist(Presentation->FlameBone);
 Flame->SetStaticMesh(bTail?Presentation->TailFlame.Get():nullptr);
 Flame->AttachToComponent(Mesh,FAttachmentTransformRules::SnapToTargetNotIncludingScale,Presentation->FlameBone);
 Flame->SetWorldRotation(FRotator::ZeroRotator);
 if(Presentation->FlameMaterial)Flame->SetMaterial(0,Presentation->FlameMaterial);
 Flame->SetVisibility(bTail);bHavePrevious=false;Reaction=EPokeMonsterCreatureClip::Idle;++ReactionSerial;
 return true;
}
float APokeMonsterCreatureVisualActor::SampleSpeed(const FVector& Delta,float Seconds,bool HasPrevious)
{
 const float Distance=Delta.Size2D();
 // Long capture/background frames are still movement. Reject actual teleports instead.
 return HasPrevious&&Seconds>SMALL_NUMBER&&Seconds<=1.f&&Distance<200.f?FMath::Min(Distance/Seconds,300.f):0.f;
}
void APokeMonsterCreatureVisualActor::Tick(float Delta)
{
 Super::Tick(Delta);const FVector P=GetActorLocation();
 MotionSpeed=SampleSpeed(P-PreviousLocation,Delta,bHavePrevious);
 PreviousLocation=P;bHavePrevious=true;
}
bool APokeMonsterCreatureVisualActor::PlayReaction(EPokeMonsterCreatureClip Clip)
{
 if(!Presentation||!Presentation->Clips.Contains(Clip)||Clip<=EPokeMonsterCreatureClip::Run)return false;
 Reaction=Clip;++ReactionSerial;return true;
}
namespace
{
struct FCreatureProxy final:FAnimInstanceProxy
{
 explicit FCreatureProxy(UAnimInstance* I):FAnimInstanceProxy(I){}
 UAnimSequence *Idle=nullptr,*Walk=nullptr,*Run=nullptr,*OneShot=nullptr;
 float IdleTime=0,Phase=0,ShotTime=0,WalkAlpha=0,RunAlpha=0,ShotAlpha=0,Rate=0;
 bool bHold=false;uint32 Serial=0;
 virtual void PreUpdate(UAnimInstance* I,float Dt)override
 {
  FAnimInstanceProxy::PreUpdate(I,Dt);auto* A=Cast<APokeMonsterCreatureVisualActor>(I->GetOwningActor());
  if(!A||!A->Presentation)return;auto* D=A->Presentation.Get();
  auto Get=[D](EPokeMonsterCreatureClip C)->UAnimSequence*{const auto* P=D->Clips.Find(C);return P?P->Get():nullptr;};
  Idle=Get(EPokeMonsterCreatureClip::Idle);Walk=Get(EPokeMonsterCreatureClip::Walk);Run=Get(EPokeMonsterCreatureClip::Run);
  const float Speed=A->MotionSpeed;
  Rate=Speed/FMath::Max(FMath::Lerp(Walk?Walk->GetPlayLength()*D->WalkSpeed:1.f,Run?Run->GetPlayLength()*D->RunSpeed:1.f,RunAlpha),1.f);
  WalkAlpha=FMath::FInterpConstantTo(WalkAlpha,Speed>2.f&&Walk?1.f:0.f,Dt,1.f/.14f);
  RunAlpha=FMath::FInterpConstantTo(RunAlpha,Run?FMath::Clamp((Speed-D->WalkSpeed)/(FMath::Max(D->RunSpeed-D->WalkSpeed,1.f)),0.f,1.f):0.f,Dt,1.f/.14f);
  if(A->ReactionSerial!=Serial){Serial=A->ReactionSerial;OneShot=A->Reaction>EPokeMonsterCreatureClip::Run?Get(A->Reaction):nullptr;ShotTime=0;ShotAlpha=0;bHold=A->Reaction==EPokeMonsterCreatureClip::Faint;}
 }
 virtual void Update(float Dt)override
 {
  if(Idle)IdleTime=FMath::Fmod(IdleTime+Dt,FMath::Max(Idle->GetPlayLength(),.01f));
  if(Walk&&WalkAlpha>0)Phase=FMath::Fmod(Phase+Dt*FMath::Max(Rate,.1f),1.f);
  if(OneShot){ShotTime+=Dt;const float End=OneShot->GetPlayLength();ShotAlpha=FMath::FInterpConstantTo(ShotAlpha,bHold||ShotTime<End-.12f?1.f:0.f,Dt,1.f/.12f);if(ShotTime>=End&&!bHold&&ShotAlpha<=0)OneShot=nullptr;}
 }
 virtual void PostUpdate(UAnimInstance* I)const override
 {
  FAnimInstanceProxy::PostUpdate(I);auto* V=CastChecked<UPokeMonsterCreatureAnimInstance>(I);
  V->WalkBlend=WalkAlpha;V->RunBlend=RunAlpha;V->ReactionBlend=ShotAlpha;
 }
 virtual bool Evaluate(FPoseContext& Out)override
 {
  Out.ResetToRefPose();if(!Idle)return true;FAnimationPoseData Result(Out);
  Idle->GetAnimationPose(Result,FAnimExtractContext(IdleTime,false));
  auto Blend=[&](UAnimSequence* Clip,float Time,float Alpha){if(!Clip||Alpha<=0)return;FPoseContext Base(Out),Other(Out);Base.Pose=Out.Pose;Base.Curve=Out.Curve;Base.CustomAttributes=Out.CustomAttributes;Other.ResetToRefPose();FAnimationPoseData A(Base),B(Other);Clip->GetAnimationPose(B,FAnimExtractContext(Time,false));FAnimationRuntime::BlendTwoPosesTogether(A,B,1.f-Alpha,Result);};
  Blend(Walk,Walk?Phase*Walk->GetPlayLength():0,WalkAlpha);
  Blend(Run,Run?Phase*Run->GetPlayLength():0,RunAlpha*WalkAlpha);
  Blend(OneShot,OneShot?FMath::Min(ShotTime,OneShot->GetPlayLength()):0,ShotAlpha);
  return true;
 }
};
}
FAnimInstanceProxy* UPokeMonsterCreatureAnimInstance::CreateAnimInstanceProxy(){return new FCreatureProxy(this);}
void UPokeMonsterCreatureAnimInstance::DestroyAnimInstanceProxy(FAnimInstanceProxy* P){delete P;}
