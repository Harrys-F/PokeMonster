#include "PokeMonsterCreaturePresentation.h"
#include "Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "../Time/PokeMonsterWorldClock.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
void FPokeMonsterSwimHeadingHistory::Reset(float Yaw)
{
 Time=0;NextSample=1.0/60.0;PreviousYaw=FMath::IsFinite(Yaw)?Yaw:0.f;UnwrappedYaw=PreviousYaw;
 Samples.Reset();Samples.Emplace(0,UnwrappedYaw);Offsets.Init(0.f,20);
}
void FPokeMonsterSwimHeadingHistory::Advance(float Yaw,float Delta,float FollowSeconds,float LimitDegrees)
{
 if(!FMath::IsFinite(Yaw)||!FMath::IsFinite(Delta)||Delta<=0)return;
 if(Samples.IsEmpty()||Delta>1.f||!FMath::IsFinite(FollowSeconds)||FollowSeconds<=0||!FMath::IsFinite(LimitDegrees)||LimitDegrees<=0)
 {Reset(Yaw);return;}
 FollowSeconds=FMath::Clamp(FollowSeconds,0.f,2.f);LimitDegrees=FMath::Min(LimitDegrees,45.f);
 const double Before=Time,OldYaw=UnwrappedYaw;Time+=Delta;
 UnwrappedYaw+=FMath::FindDeltaAngleDegrees(PreviousYaw,Yaw);PreviousYaw=Yaw;
 while(NextSample<=Time)
 {Samples.Emplace(NextSample,FMath::Lerp(OldYaw,UnwrappedYaw,(NextSample-Before)/Delta));NextSample+=1.0/60.0;}
 // Keep the sample preceding the oldest needed instant, not an unbounded per-frame log.
 while(Samples.Num()>2&&Samples[1].X<Time-FollowSeconds-.04)Samples.RemoveAt(0,1,EAllowShrinking::No);
 for(int32 I=0;I<20;++I)
 {
  const double Wanted=Time-FollowSeconds*I/19.;double Heading=Samples[0].Y;
  if(Wanted>=Samples.Last().X)
   Heading=FMath::Lerp(Samples.Last().Y,UnwrappedYaw,FMath::Clamp((Wanted-Samples.Last().X)/FMath::Max(Time-Samples.Last().X,1.e-9),0.,1.));
  else for(int32 J=1;J<Samples.Num();++J)if(Samples[J].X>=Wanted)
   {Heading=FMath::Lerp(Samples[J-1].Y,Samples[J].Y,FMath::Clamp((Wanted-Samples[J-1].X)/(Samples[J].X-Samples[J-1].X),0.,1.));break;}
  Offsets[I]=I==0?0.f:FMath::Clamp(float(Heading-UnwrappedYaw),-LimitDegrees,LimitDegrees);
 }
}
float APokeMonsterCreatureVisualActor::SmoothSwimValue(float Current,float Target,float Delta,float Seconds)
{
 if(!FMath::IsFinite(Current))Current=0;
 if(!FMath::IsFinite(Target)||!FMath::IsFinite(Delta)||!FMath::IsFinite(Seconds)||Delta<=0||Seconds<=0)return Current;
 return FMath::Lerp(Current,Target,1.f-FMath::Exp(-Delta/Seconds));
}
float APokeMonsterCreatureVisualActor::AdvanceSwimObserve(float Current,bool Requested,float Delta,float Seconds)
{
 if(!FMath::IsFinite(Current)||!FMath::IsFinite(Delta)||!FMath::IsFinite(Seconds)||Delta<=0||Seconds<=0)return FMath::Clamp(FMath::IsFinite(Current)?Current:0.f,0.f,1.f);
 return FMath::FInterpConstantTo(FMath::Clamp(Current,0.f,1.f),Requested?1.f:0.f,Delta,1.f/Seconds);
}
float APokeMonsterCreatureVisualActor::SwimTurnFromYaw(float Previous,float Current,float Delta,float MaximumRate)
{
 if(!FMath::IsFinite(Previous)||!FMath::IsFinite(Current)||!FMath::IsFinite(Delta)||!FMath::IsFinite(MaximumRate)||Delta<=0||Delta>1.f||MaximumRate<=0)return 0.f;
 return FMath::Clamp(-FMath::FindDeltaAngleDegrees(Previous,Current)/(Delta*MaximumRate),-1.f,1.f);
}
void APokeMonsterCreatureVisualActor::UpdateSwimming(float Delta)
{
 if(!Presentation||!Presentation->SwimMesh)return;
 const bool Aquatic=AquaticPoseAlpha>.5f;
 if(Aquatic!=bUsingSwimMesh)
 {
  bUsingSwimMesh=Aquatic;Reaction=EPokeMonsterCreatureClip::Idle;++ReactionSerial;
  Mesh->SetSkeletalMesh(Aquatic?Presentation->SwimMesh.Get():Presentation->Mesh.Get());
  Mesh->SetAnimInstanceClass(UPokeMonsterCreatureAnimInstance::StaticClass());
  SwimObserveAlpha=SwimObserveHold=SwimObserveProgress=SwimTurnInput=0.f;PreviousSwimYaw=GetActorRotation().Yaw;SwimHeadingHistory.Reset(PreviousSwimYaw);SwimBodyYawOffsets=SwimHeadingHistory.Offsets;
 }
 auto* Context=HoverContext.Get();
 if(!Aquatic){SwimBodyYawOffsets.Reset();if(Context)Context->SetSwimPresentationWeight(0.f);return;}
 bool Observing=false;
 if(Context&&!Context->bControlledModelPreview)
 {
  using S=EPokeMonsterOverworldState;const S State=Context->BehaviorState;
  Observing=State==S::Idle||State==S::Observe||State==S::Alert||State==S::Warning||State==S::Curious||State==S::Social;
 }
 const auto* Clock=GetGameInstance()?GetGameInstance()->GetSubsystem<UPokeMonsterWorldClock>():nullptr;
 const float Dt=Clock&&Clock->IsClockPaused()?0.f:FMath::Max(0.f,Delta);
 if(Observing)SwimObserveHold=3.f;else SwimObserveHold=FMath::Max(0.f,SwimObserveHold-Dt);
 const bool Raise=SwimObserveHold>0.f&&MotionSpeed<FMath::Max(5.f,Presentation->SwimSlowSpeed*.3f);
 SwimObserveProgress=AdvanceSwimObserve(SwimObserveProgress,Raise,Dt,Presentation->SwimObserveBlendSeconds);
 SwimObserveAlpha=FMath::SmoothStep(0.f,1.f,SwimObserveProgress);
 SwimHeadingHistory.Advance(GetActorRotation().Yaw,Dt,Presentation->SwimBodyFollowSeconds,Presentation->SwimBodyFollowLimitDegrees);
 SwimBodyYawOffsets=SwimHeadingHistory.Offsets;
 const float Turn=SwimTurnFromYaw(PreviousSwimYaw,GetActorRotation().Yaw,Delta,Presentation->SwimTurnDegreesPerSecond);
 PreviousSwimYaw=GetActorRotation().Yaw;SwimTurnInput=SmoothSwimValue(SwimTurnInput,Turn,Dt,.5f);
 if(Context)
 {
  Context->SetSwimPresentationWeight(SwimObserveAlpha);
  if(Context->bControlledModelPreview&&(!Context->BiomeHabitat||Context->BiomeHabitat->Medium!=EPokeMonsterBiomeMedium::WaterOnly))Mesh->SetRelativeLocation(Mesh->GetRelativeLocation()-FVector(0,0,Presentation->SwimPreviewOffsetCm));
 }
}
