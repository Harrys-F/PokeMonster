#include "PokeMonsterCreaturePresentation.h"
#include "Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "../Time/PokeMonsterWorldClock.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
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
  SwimObserveAlpha=SwimObserveHold=SwimTurnInput=0.f;PreviousSwimYaw=GetActorRotation().Yaw;
 }
 auto* Context=HoverContext.Get();
 if(!Aquatic){if(Context)Context->SetSwimPresentationWeight(0.f);return;}
 bool Observing=false;
 if(Context&&!Context->bControlledModelPreview)
 {
  using S=EPokeMonsterOverworldState;const S State=Context->BehaviorState;
  Observing=State==S::Idle||State==S::Observe||State==S::Alert||State==S::Warning||State==S::Curious||State==S::Social;
 }
 const auto* Clock=GetGameInstance()?GetGameInstance()->GetSubsystem<UPokeMonsterWorldClock>():nullptr;
 const float Dt=Clock&&Clock->IsClockPaused()?0.f:FMath::Max(0.f,Delta);
 if(Observing)SwimObserveHold=3.f;else SwimObserveHold=FMath::Max(0.f,SwimObserveHold-Dt);
 SwimObserveAlpha=AdvanceSwimObserve(SwimObserveAlpha,SwimObserveHold>0.f,Dt,Presentation->SwimObserveBlendSeconds);
 const float Turn=SwimTurnFromYaw(PreviousSwimYaw,GetActorRotation().Yaw,Delta,Presentation->SwimTurnDegreesPerSecond);
 PreviousSwimYaw=GetActorRotation().Yaw;SwimTurnInput=FMath::FInterpTo(SwimTurnInput,Turn,Dt,2.f);
 if(Context)
 {
  Context->SetSwimPresentationWeight(SwimObserveAlpha);
  if(Context->bControlledModelPreview&&(!Context->BiomeHabitat||Context->BiomeHabitat->Medium!=EPokeMonsterBiomeMedium::WaterOnly))Mesh->SetRelativeLocation(Mesh->GetRelativeLocation()-FVector(0,0,Presentation->SwimPreviewOffsetCm));
 }
}
