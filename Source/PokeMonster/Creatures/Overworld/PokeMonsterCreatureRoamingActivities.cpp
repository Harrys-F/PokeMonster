#include "PokeMonsterCreatureRoamingComponent.h"
#include "../PokeMonsterCreatureSpeciesData.h"
#include "../../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "Engine/OverlapResult.h"
#include "EngineUtils.h"

void UPokeMonsterCreatureRoamingComponent::EndPlay(const EEndPlayReason::Type Reason)
{
 ReleaseSocial();
 Super::EndPlay(Reason);
}
void UPokeMonsterCreatureRoamingComponent::ConfigureActivities(const UPokeMonsterCreatureSpeciesData* Species,int32 Seed)
{
 ActivitySpecies=Species->GetInternalId();
 Activities=bOverrideActivities?ActivityOverride:FPokeMonsterCreatureActivityProfile::ForSpecies(ActivitySpecies);
 // Explicit rollout boundary. Shared species assets, other maps and companions are unchanged.
 bActivitiesEnabled=Activities.bEnabled && Activities.IsValid() && !FollowTarget.IsValid() && !BiomeHabitat
  && Cast<APokeMonsterVisibleWildCreatureActor>(GetOwner())
  && UWorld::RemovePIEPrefix(GetWorld()->GetName())==TEXT("Dev_TestMap_VisualV2");
 ActivityRandom.Initialize(Seed ^ 0x32A541);
 bActivityRunning=bActivityTravelling=bActivityDistant=false;
 ActivityRemaining=ActivityTravelRemaining=SocialCooldown=SleepCooldown=ForageCooldown=0;
 PeerQueryRemaining=ActivityRandom.FRandRange(.1f,Activities.PerceptionSeconds);
 VisibilityRemaining=0;PerceivedPeer.Reset();ForageAnchors.Reset();
 ActivityDecisions=PeerQueries=PerceptionTraces=SocialCompleted=ForageCompleted=0;
 if(!bActivitiesEnabled || !Activities.bPreferVegetation)return;
 // Cache nearby authored vegetation once. Approaches stop beside it, never inside a bush.
 const float Radius=HabitatRadiusOverride>0?HabitatRadiusOverride:Settings.RoamRadius;
 for(TActorIterator<AActor> It(GetWorld());It;++It)
 {
  TInlineComponentArray<UStaticMeshComponent*> Components(*It);
  for(const auto* Mesh:Components)
  {
   if(!Mesh->GetStaticMesh())continue;
   const FString Name=Mesh->GetStaticMesh()->GetPathName();
   if(!Name.Contains(TEXT("Grass"))&&!Name.Contains(TEXT("Fern"))&&!Name.Contains(TEXT("Bush"))&&!Name.Contains(TEXT("Shrub")))continue;
   auto Add=[&](const FTransform& T)
   {
    const FVector P=T.GetLocation();
    if(FVector::DistSquared2D(P,HabitatOrigin)<FMath::Square(Radius+100) && ForageAnchors.Num()<64)ForageAnchors.Add(P);
   };
   if(const auto* Instances=Cast<UInstancedStaticMeshComponent>(Mesh))
   {for(int32 I=0;I<Instances->GetInstanceCount();++I){FTransform T;if(Instances->GetInstanceTransform(I,T,true))Add(T);}}
   else Add(Mesh->GetComponentTransform());
  }
 }
}
void UPokeMonsterCreatureRoamingComponent::ReleaseSocial()
{
 auto* Peer=SocialPartner.Get();SocialPartner=nullptr;
 if(IsValid(Peer) && Peer->SocialPartner==this)
 {
  Peer->SocialPartner=nullptr;Peer->bActivityRunning=Peer->bActivityTravelling=false;
  Peer->ActivityRemaining=0;Peer->Path.Reset();Peer->CurrentSpeed=0;
  Peer->SocialCooldown=Peer->Activities.SocialCooldown;Peer->BehaviorState=EPokeMonsterOverworldState::Rest;
 }
}
void UPokeMonsterCreatureRoamingComponent::FinishActivity(bool Interrupted)
{
 if(!bActivityRunning && !SocialPartner)return;
 using S=EPokeMonsterOverworldState;
 if(BehaviorState==S::Sleep)SleepCooldown=Activities.SleepCooldown;
 if(BehaviorState==S::Forage){ForageCooldown=Activities.ForageCooldown;if(!Interrupted&&!bActivityTravelling)++ForageCompleted;}
 if(BehaviorState==S::Social)
 {
  SocialCooldown=Activities.SocialCooldown;
  if(!Interrupted&&!bActivityTravelling){++SocialCompleted;if(SocialPartner)++SocialPartner->SocialCompleted;}
 }
 ReleaseSocial();bActivityRunning=bActivityTravelling=false;ActivityRemaining=0;
 Path.Reset();PauseRemaining=ActivityRandom.FRandRange(1.f,2.5f);CurrentSpeed=0;
 BehaviorState=S::Rest;
}
bool UPokeMonsterCreatureRoamingComponent::CanSocialize() const
{
 const auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(GetOwner());
 return bActivitiesEnabled && bReady && !bPaused && !bPresentationHold && IsComponentTickEnabled()
  && Wild && Wild->LifeState==EPokeMonsterWildLifeState::Active && !GetOwner()->IsHidden()
  && !bEscapingDefeat && !bActivityDistant && !SocialPartner && SocialCooldown<=0 && CooldownRemaining<=0
  && (BehaviorState==EPokeMonsterOverworldState::Wander || BehaviorState==EPokeMonsterOverworldState::Rest || BehaviorState==EPokeMonsterOverworldState::Idle)
  && (!bActivityRunning || BehaviorState==EPokeMonsterOverworldState::Wander || BehaviorState==EPokeMonsterOverworldState::Idle);
}
bool UPokeMonsterCreatureRoamingComponent::PeerVisible(const UPokeMonsterCreatureRoamingComponent* Peer) const
{
 if(!IsValid(Peer)||Peer==this||!Peer->GetOwner())return false;
 FCollisionQueryParams Q=Query();Q.AddIgnoredActor(Peer->GetOwner());
 TArray<AActor*> Attached;Peer->GetOwner()->GetAttachedActors(Attached);Q.AddIgnoredActors(Attached);
 FHitResult H;
 return !GetWorld()->LineTraceSingleByChannel(H,GetOwner()->GetActorLocation()+FVector(0,0,15),Peer->GetOwner()->GetActorLocation()+FVector(0,0,15),ECC_Visibility,Q);
}
bool UPokeMonsterCreatureRoamingComponent::FindSocialPartner()
{
 PerceivedPeer.Reset();LastSocialDecision=TEXT("Unavailable");if(!CanSocialize())return false;
 LastSocialDecision=TEXT("NoNearbyPeer");
 ++PeerQueries;
 // Broadphase spatial query, not an all-actors/all-pairs scan each tick.
 TArray<FOverlapResult> Hits;
 FCollisionObjectQueryParams Objects;Objects.AddObjectTypesToQuery(ECC_WorldDynamic);Objects.AddObjectTypesToQuery(ECC_Pawn);
 GetWorld()->OverlapMultiByObjectType(Hits,GetOwner()->GetActorLocation(),FQuat::Identity,Objects,
  FCollisionShape::MakeSphere(Activities.SocialRadius),Query());
 float Best=BIG_NUMBER;int32 Checked=0,BusyPeers=0;TSet<AActor*> Seen;
 for(const auto& Hit:Hits)
 {
  auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(Hit.GetActor());
  if(!Wild||Wild==GetOwner()||Seen.Contains(Wild))continue;Seen.Add(Wild);
  if(++Checked>12)break;
  auto* Peer=Wild->OverworldMovement.Get();
  if(Peer && Peer->SocialPartner && ++BusyPeers>=4){PerceivedPeer.Reset();return false;} // At most two nearby pairs.
  if(!Peer || !Peer->CanSocialize()){LastSocialDecision=TEXT("PeerBusy");continue;}
  const float Distance=FVector::Dist2D(GetOwner()->GetActorLocation(),Wild->GetActorLocation());
  if(Distance>Activities.SocialRadius || FMath::Abs(GetOwner()->GetActorLocation().Z-Wild->GetActorLocation().Z)>100)continue;
  const bool Same=ActivitySpecies==Peer->ActivitySpecies;
  if((Activities.bPreferOwnSpecies||Peer->Activities.bPreferOwnSpecies)&&!Same)continue;
  // Peripheral peers do not constantly distract a resting creature.
  const FVector Direction=(Wild->GetActorLocation()-GetOwner()->GetActorLocation()).GetSafeNormal2D();
  if(FVector::DotProduct(Direction,GetOwner()->GetActorForwardVector())<-.25f){LastSocialDecision=TEXT("Behind");continue;}
  ++PerceptionTraces;if(!PeerVisible(Peer)){LastSocialDecision=TEXT("Obstructed");continue;}
  const float Score=Distance+(Same?0:150);
  if(Score<Best){Best=Score;PerceivedPeer=Peer;}
 }
 if(PerceivedPeer.IsValid())LastSocialDecision=TEXT("ReadyPeer");
 return PerceivedPeer.IsValid();
}
bool UPokeMonsterCreatureRoamingComponent::PlanForage(const FVector& Current)
{
 for(int32 I=0;I<8;++I)
 {
  FVector Goal;
  if(!ForageAnchors.IsEmpty())
  {
   const FVector Anchor=ForageAnchors[ActivityRandom.RandRange(0,ForageAnchors.Num()-1)];
   Goal=Anchor+(Current-Anchor).GetSafeNormal2D(SMALL_NUMBER,FVector::ForwardVector)*(BodyRadius+45.f);
  }
  else Goal=Current+FVector::ForwardVector.RotateAngleAxis(ActivityRandom.FRandRange(-180,180),FVector::UpVector)*ActivityRandom.FRandRange(90,260);
  Goal.Z=Current.Z;
  if(FVector::Dist2D(Current,Goal)<60 || FVector::Dist2D(Current,Goal)>600)continue;
  if(Plan(Goal)){ActivityFocus=Goal+GetOwner()->GetActorForwardVector()*60;return true;}
 }
 return false;
}
void UPokeMonsterCreatureRoamingComponent::FaceActivity(float Delta,const FVector& Target)
{
 const float Yaw=(Target-GetOwner()->GetActorLocation()).Rotation().Yaw;
 GetOwner()->SetActorRotation(FRotator(0,AdvanceHeading(GetOwner()->GetActorRotation().Yaw,Yaw,AngularVelocity,Settings,Delta),0));
}
bool UPokeMonsterCreatureRoamingComponent::UpdateActivities(float Delta,const FVector& Current,const APawn* Player,float& Speed)
{
 QUICK_SCOPE_CYCLE_COUNTER(STAT_PokeMonsterNaturalActivities);
 using S=EPokeMonsterOverworldState;
 if(BehaviorState==S::Approach||BehaviorState==S::Retreat||BehaviorState==S::Observe||BehaviorState==S::Warning)return false;
 SocialCooldown=FMath::Max(0.f,SocialCooldown-Delta);SleepCooldown=FMath::Max(0.f,SleepCooldown-Delta);ForageCooldown=FMath::Max(0.f,ForageCooldown-Delta);
 PeerQueryRemaining-=Delta;
 if(bActivityRunning)
 {
  if(BehaviorState==S::Social)
  {
   if(!IsValid(SocialPartner)||SocialPartner->SocialPartner!=this||SocialPartner->bPaused||SocialPartner->bEscapingDefeat||SocialPartner->GetOwner()->IsHidden()||!SocialPartner->IsComponentTickEnabled())
   {FinishActivity(true);return true;}
   ActivityFocus=SocialPartner->GetOwner()->GetActorLocation();
   // No repeated moving-target replans: one partner waits; the initiator has one bounded path.
   if(!bSocialLeader && SocialPartner->bActivityTravelling){CurrentSpeed=0;FaceActivity(Delta,ActivityFocus);return true;}
  }
  if(bActivityTravelling)
  {
   ActivityTravelRemaining-=Delta;PauseRemaining=0;
   if(Path.IsEmpty())
   {
    if(FVector::Dist2D(Current,CurrentGoal)>BodyRadius+20){FinishActivity(true);return true;}
    bActivityTravelling=false;CurrentSpeed=0;
   }
   else if(ActivityTravelRemaining<=0){FinishActivity(true);return true;}
   else {Speed*=.8f;return false;}
  }
  ActivityRemaining-=Delta;
  if(ActivityRemaining<=0 && (BehaviorState!=S::Wander||Path.IsEmpty())){FinishActivity();return true;}
  if(BehaviorState==S::Wander)return false;
  CurrentSpeed=0;Path.Reset();PauseRemaining=0;
  if(BehaviorState==S::Social||BehaviorState==S::Forage||BehaviorState==S::Idle)FaceActivity(Delta,ActivityFocus);
  return true;
 }
 if(!Path.IsEmpty()||PauseRemaining>0)return false;
 // Stagger the initial decision itself, not only perception. Otherwise a social
 // profile always picked Wander before its first neighbour query had happened.
 if(ActivityDecisions==0 && PeerQueryRemaining>0){CurrentSpeed=0;return true;}
 if(PeerQueryRemaining<=0){FindSocialPartner();PeerQueryRemaining=Activities.PerceptionSeconds*ActivityRandom.FRandRange(.8f,1.25f);}
 const bool Social=PerceivedPeer.IsValid()&&CanSocialize()&&PerceivedPeer->CanSocialize();
 S Next=FPokeMonsterCreatureActivityProfile::Select(Activities,ActivityRandom,ActivityPeriod,SleepCooldown<=0,ForageCooldown<=0,Social);
 ++ActivityDecisions;
 if(Next==S::Social)
 {
  auto* Peer=PerceivedPeer.Get();
  // Stay out of both bodies; shy creatures watch from further away.
  const float Separation=BodyRadius+Peer->BodyRadius+75.f+(Settings.Behavior.Temperament==EPokeMonsterOverworldTemperament::Shy?100.f:0.f);
  const FVector PeerGround=Peer->GetOwner()->GetActorLocation()-FVector(0,0,Peer->Offset);
  const FVector Goal=PeerGround+(Current-PeerGround).GetSafeNormal2D(SMALL_NUMBER,FVector::ForwardVector)*Separation;
  if(!PeerVisible(Peer) || !Plan(Goal)){LastSocialDecision=TEXT("NoApproachSpace");Next=S::Idle;}
  else
  {
   Peer->FinishActivity(true); // Release an ambient wander, never a combat/player reaction.
   SocialPartner=Peer;Peer->SocialPartner=this;bSocialLeader=true;Peer->bSocialLeader=false;
   Peer->bActivityRunning=true;Peer->bActivityTravelling=false;Peer->BehaviorState=S::Social;
   Peer->ActivityRemaining=Activities.MinimumSeconds+4;Peer->PauseRemaining=0;Peer->Path.Reset();Peer->CurrentSpeed=0;
   bActivityTravelling=true;ActivityTravelRemaining=20;
  }
 }
 if(Next==S::Forage)
 {
  if(!PlanForage(Current)){ForageCooldown=Activities.ForageCooldown;Next=S::Idle;}
  else {bActivityTravelling=true;ActivityTravelRemaining=20;}
 }
 BehaviorState=Next;bActivityRunning=true;
 ActivityRemaining=ActivityRandom.FRandRange(Activities.MinimumSeconds,Activities.MaximumSeconds);
 if(Next==S::Rest)ActivityRemaining=Activities.RestSeconds*ActivityRandom.FRandRange(.8f,1.2f);
 if(Next==S::Sleep)ActivityRemaining=Activities.SleepSeconds*ActivityRandom.FRandRange(.8f,1.2f);
 if(Next==S::Social)ActivityRemaining=SocialPartner->ActivityRemaining;
 if(Next==S::Idle)ActivityFocus=Current+GetOwner()->GetActorForwardVector().RotateAngleAxis(ActivityRandom.FRandRange(-65,65),FVector::UpVector)*150;
 PauseRemaining=0;
 return Next!=S::Wander && !bActivityTravelling;
}
