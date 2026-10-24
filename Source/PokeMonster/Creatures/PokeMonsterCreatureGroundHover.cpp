#include "PokeMonsterCreaturePresentation.h"
#include "Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Engine/GameInstance.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimSequence.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/World.h"

void APokeMonsterCreatureVisualActor::SetGroundHoverContext(UPokeMonsterCreatureRoamingComponent* Context)
{
 if (HoverContext.Get()==Context) return;
 if (HoverContext.IsValid()) { HoverContext->SetPresentationHold(false);HoverContext->SetPresentationHoverClearance(0.f,FBox(ForceInit)); }
 HoverContext=Context;bBoundFlightBattlePause=false;HoverState=EHoverState::Grounded;HoverStateTime=HoverHeight=HoverPoseAlpha=0.f;
 GroundWait=6.f+FMath::Fmod(GetUniqueID()*.137f,7.f);HoverCheckRemaining=0.f;bHoverClear=false;
 ActiveHoverClip=nullptr;Mesh->SetRelativeLocation(FVector::ZeroVector);
}
FString APokeMonsterCreatureVisualActor::GetGroundHoverState() const
{
 switch (HoverState)
 {
 case EHoverState::Takeoff:return TEXT("Takeoff");
 case EHoverState::Hover:return TEXT("Hover");
 case EHoverState::Landing:return TEXT("Landing");
 default:return TEXT("Grounded");
 }
}
void APokeMonsterCreatureVisualActor::UpdateGroundHover(float Delta)
{
 auto* Context=HoverContext.Get();const auto* GI=GetGameInstance();
 const auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 const bool Battle=E&&E->IsEncounterActive();
 // Explicit bounded overflight may be above a low obstacle: never descend through it on battle start.
 const bool Bounded=Context&&Context->BiomeHabitat&&Context->BiomeHabitat->bAllowGroundFlightOverObstacles;
 if(Battle&&Bounded&&HoverHeight>0.f)
 {
  bBoundFlightBattlePause=true;Context->SetPresentationHold(true);
  if(ActiveHoverClip)HoverClipTime=FMath::Fmod(HoverClipTime+FMath::Max(0.f,Delta),FMath::Max(.01f,ActiveHoverClip->GetPlayLength()));
  Mesh->SetRelativeLocation(FVector(0,0,HoverHeight));return;
 }
 if(bBoundFlightBattlePause)
 {
  bBoundFlightBattlePause=false;HoverCheckRemaining=0.f;
  if(Context)Context->SetPresentationHold(HoverState==EHoverState::Takeoff||HoverState==EHoverState::Landing);
 }

 // No effect on collision, logical ground height, or the separate ClassicBattle actors.
 if (Context&&Presentation&&Presentation->OverworldFloatAmplitudeCm>0.f&&!IsHidden()&&!Battle)
 {
  Context->SetPresentationHold(false);Context->SetPresentationHoverClearance(0.f,FBox(ForceInit));
  const float Phase=GetWorld()->GetTimeSeconds()*1.5f+IdlePhaseOffset*2.f*PI;
  const float Amplitude=Presentation->OverworldFloatAmplitudeCm;
  HoverHeight=Amplitude*(1.35f+FMath::Sin(Phase));
  Mesh->SetRelativeLocation(FVector(0,0,HoverHeight));
  Mesh->SetRelativeRotation(FRotator(1.4f*FMath::Sin(Phase*.73f),1.8f*FMath::Sin(Phase*.51f),.9f*FMath::Sin(Phase*.87f)));
  HoverState=EHoverState::Grounded;HoverPoseAlpha=0.f;ActiveHoverClip=nullptr;bUsingAmbientFloat=true;return;
 }
 if (bUsingAmbientFloat) {Mesh->SetRelativeRotation(FRotator::ZeroRotator);bUsingAmbientFloat=false;}

 if (!Context || !Presentation || !Presentation->bAllowGroundHover || IsHidden() || Battle)
 {
  if (Context) { Context->SetPresentationHold(false);Context->SetPresentationHoverClearance(0.f,FBox(ForceInit)); }
  // Hidden ClassicBattle sources reset immediately. Visible WorldBattle keeps a short descent,
  // but always gives its original combat animation sole ownership of the pose.
  HoverHeight=IsHidden()?0.f:FMath::FInterpConstantTo(HoverHeight,0.f,Delta,300.f);
  HoverState=EHoverState::Grounded;HoverStateTime=HoverPoseAlpha=0.f;ActiveHoverClip=nullptr;
  Mesh->SetRelativeLocation(FVector(0,0,HoverHeight));return;
 }
 // Analytic height curves use real game time, including capture/load hitches.
 const float Dt=FMath::IsFinite(Delta)?FMath::Max(Delta,0.f):0.f;HoverStateTime+=Dt;HoverCheckRemaining-=Dt;
 if (HoverCheckRemaining<=0.f)
 {
  HoverCheckRemaining=.10f;bHoverClear=Context->CanGroundHover(FMath::Min(150.f,Presentation->HoverHeightCm+5.f),Presentation->Mesh->GetBounds().GetBox());
 }
 auto Enter=[&](EHoverState Next){HoverState=Next;HoverStateTime=0.f;};
 auto Smooth=[](float T){T=FMath::Clamp(T,0.f,1.f);return T*T*(3.f-2.f*T);};
 if (HoverState==EHoverState::Grounded)
 {
  HoverHeight=HoverPoseAlpha=0.f;ActiveHoverClip=nullptr;
  if (HoverStateTime>=GroundWait && bHoverClear && MotionSpeed<Presentation->RunSpeed*.8f) Enter(EHoverState::Takeoff);
 }
 if ((HoverState==EHoverState::Takeoff || HoverState==EHoverState::Hover) && !bHoverClear)
 { LandingHeight=HoverHeight;Enter(EHoverState::Landing); }
 if (HoverState==EHoverState::Takeoff)
 {
  ActiveHoverClip=Presentation->TakeoffClip;HoverClipTime=FMath::Min(HoverStateTime,ActiveHoverClip->GetPlayLength());
  HoverPoseAlpha=Smooth(HoverStateTime/.20f);HoverHeight=Presentation->HoverHeightCm*Smooth((HoverStateTime-.35f)/1.25f);
  if (HoverStateTime>=1.6f) Enter(EHoverState::Hover);
 }
 else if (HoverState==EHoverState::Hover)
 {
  ActiveHoverClip=Presentation->HoverClip;HoverPoseAlpha=1.f;HoverClipTime=FMath::Fmod(HoverStateTime,ActiveHoverClip->GetPlayLength());
  HoverHeight=FMath::Clamp(Presentation->HoverHeightCm+4.f*FMath::Sin(HoverStateTime*2.f),50.f,150.f);
  if (HoverStateTime>=7.f && Context->CanGroundHover(FMath::Min(150.f,Presentation->HoverHeightCm+5.f),Presentation->Mesh->GetBounds().GetBox(),true)) { LandingHeight=HoverHeight;Enter(EHoverState::Landing); }
 }
 else if (HoverState==EHoverState::Landing)
 {
  ActiveHoverClip=Presentation->LandClip;HoverClipTime=FMath::Min(HoverStateTime,ActiveHoverClip->GetPlayLength());
  HoverHeight=LandingHeight*(1.f-Smooth(HoverStateTime/1.25f));HoverPoseAlpha=1.f-Smooth((HoverStateTime-1.1f)/.3f);
  if (HoverStateTime>=1.4f) {Enter(EHoverState::Grounded);GroundWait=28.f+FMath::Fmod(GetUniqueID()*.317f,17.f);HoverHeight=HoverPoseAlpha=0.f;ActiveHoverClip=nullptr;}
 }
 Context->SetPresentationHoverClearance(HoverHeight>0.f?FMath::Min(150.f,Presentation->HoverHeightCm+5.f):0.f,Presentation->Mesh->GetBounds().GetBox());
 Context->SetPresentationHold(HoverState==EHoverState::Takeoff || HoverState==EHoverState::Landing);
 Mesh->SetRelativeLocation(FVector(0,0,HoverHeight));
}
