#include "PokeMonsterCreaturePresentation.h"
#include "PokeMonsterCreatureSpeciesData.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimSequence.h"
#include "AnimationRuntime.h"
#include "Engine/SkeletalMesh.h"
TArray<FString> UPokeMonsterCreaturePresentationData::GetValidationErrors() const
{
 TArray<FString> Errors;
 if(!Mesh || !Mesh->GetSkeleton()){Errors.Add(TEXT("Mesh and skeleton are required"));return Errors;}
 for(const auto& Slot:Mesh->GetMaterials())if(!Slot.MaterialInterface)Errors.Add(TEXT("Mesh material slot is unassigned"));
 if(!Clips.FindRef(EPokeMonsterCreatureClip::Idle))Errors.Add(TEXT("Idle clip is required"));
 for(const auto& Pair:Clips)
 {
  const UAnimSequence* Clip=Pair.Value;
  if(static_cast<uint8>(Pair.Key)>static_cast<uint8>(EPokeMonsterCreatureClip::Happy))Errors.Add(TEXT("Unknown clip role"));
  if(!Clip){Errors.Add(TEXT("Null animation entry"));continue;}
  if(Clip->GetSkeleton()!=Mesh->GetSkeleton())Errors.Add(TEXT("Animation must use this mesh's exact skeleton; retarget first"));
  if(!FMath::IsFinite(Clip->GetPlayLength())||Clip->GetPlayLength()<=0.f)Errors.Add(TEXT("Animation must have positive duration"));
  if(Clip->bEnableRootMotion)Errors.Add(TEXT("Presentation requires in-place animation, not root-motion extraction"));
 }
 if(!FMath::IsFinite(WalkSpeed)||WalkSpeed<=0.f||!FMath::IsFinite(RunSpeed)||RunSpeed<WalkSpeed)Errors.Add(TEXT("Speeds must be finite, positive and Run >= Walk"));
 if(!FMath::IsFinite(GroundOffsetCm))Errors.Add(TEXT("Ground offset must be finite"));
 if(!FMath::IsFinite(ReferenceSizeCm)||ReferenceSizeCm<0.f)Errors.Add(TEXT("Reference size must be zero (unknown) or positive centimetres"));
 if(ReferenceSizeCm>0.f&&SizeSource.IsEmpty())Errors.Add(TEXT("Reference size requires its source"));
 auto HasAnchor=[this](FName Name){return !Name.IsNone()&&(Mesh->FindSocket(Name)||Mesh->GetRefSkeleton().FindBoneIndex(Name)!=INDEX_NONE);};
 if(TailFlame&&!HasAnchor(FlameBone))Errors.Add(TEXT("Legacy tail flame anchor is missing"));
 TSet<FName> Ids;
 for(const auto& A:EffectAnchors)
 {
  if(A.Id.IsNone()||Ids.Contains(A.Id))Errors.Add(TEXT("Effect anchor IDs must be present and unique"));
  Ids.Add(A.Id);
  if(!A.Mesh||!HasAnchor(A.Socket))Errors.Add(TEXT("Effect requires a mesh and an existing bone or socket"));
  const FVector Scale=A.Offset.GetScale3D();
  if(A.Offset.ContainsNaN()||Scale.GetMin()<=0.f||!A.Offset.GetRotation().IsNormalized())Errors.Add(TEXT("Effect offset must be finite with positive scale and normalized rotation"));
  if(TailFlame&&A.Mesh==TailFlame&&A.Socket==FlameBone)Errors.Add(TEXT("Duplicate legacy tail flame; use one effect binding"));
 }
 return Errors;
}
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
 return SetPresentation(Species?Species->GetVisuals().Presentation.LoadSynchronous():nullptr);
}
bool APokeMonsterCreatureVisualActor::SetPresentation(UPokeMonsterCreaturePresentationData* Candidate)
{
 if(!Candidate||!Candidate->GetValidationErrors().IsEmpty())return false;
 for(const auto& Component:EffectComponents)if(Component)Component->DestroyComponent();
 EffectComponents.Reset();Presentation=Candidate;MotionSpeed=0.f;
 Mesh->SetSkeletalMesh(Presentation->Mesh);Mesh->SetAnimationMode(EAnimationMode::AnimationBlueprint);
 Mesh->SetAnimInstanceClass(UPokeMonsterCreatureAnimInstance::StaticClass());
 const bool bTail=Presentation->TailFlame&&Mesh->DoesSocketExist(Presentation->FlameBone);
 Flame->SetStaticMesh(bTail?Presentation->TailFlame.Get():nullptr);
 Flame->AttachToComponent(Mesh,FAttachmentTransformRules::SnapToTargetNotIncludingScale,bTail?Presentation->FlameBone:NAME_None);
 Flame->SetWorldRotation(FRotator::ZeroRotator);
 Flame->SetMaterial(0,Presentation->FlameMaterial);
 Flame->SetVisibility(bTail);
 for(const auto& A:Presentation->EffectAnchors)
 {
  auto* Component=NewObject<UStaticMeshComponent>(this);
  AddInstanceComponent(Component);Component->SetStaticMesh(A.Mesh);
  Component->SetCollisionEnabled(ECollisionEnabled::NoCollision);Component->SetCastShadow(false);
  Component->AttachToComponent(Mesh,FAttachmentTransformRules::SnapToTargetNotIncludingScale,A.Socket);
  Component->SetRelativeTransform(A.Offset);Component->SetAbsolute(false,A.bWorldUpright,false);
  if(A.bWorldUpright)Component->SetWorldRotation(A.Offset.Rotator());
  if(A.Material)Component->SetMaterial(0,A.Material);
  Component->RegisterComponent();EffectComponents.Add(Component);
 }
 bHavePrevious=false;Reaction=EPokeMonsterCreatureClip::Idle;++ReactionSerial;
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
