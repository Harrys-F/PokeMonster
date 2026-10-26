#include "PokeMonsterCreatureRoamingComponent.h"
#include "../PokeMonsterCreatureSpeciesData.h"
#include "../../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "Engine/OverlapResult.h"
#include "EngineUtils.h"
#include "Engine/GameInstance.h"

void UPokeMonsterCreatureRoamingComponent::EndPlay(const EEndPlayReason::Type Reason)
{
 ReleaseSocial();UnbindRhythm();
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
 ActivityRemaining=ActivityTravelRemaining=ActivityElapsed=SocialCooldown=SleepCooldown=ForageCooldown=0;
 SocialInvitationRemaining=ActivityRandom.FRandRange(5.f,11.f);
 SocialDeadlineRemaining=SocialValidationRemaining=0;
 PeerQueryRemaining=ActivityRandom.FRandRange(.1f,Activities.PerceptionSeconds);
 VisibilityRemaining=0;PerceivedPeer.Reset();ForageAnchors.Reset();
 ActivityDecisions=PeerQueries=PerceptionTraces=SocialCompleted=ForageCompleted=SocialRequests=SocialDeclined=SocialInterrupted=0;
 ConfigureRhythm(Seed);
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
 auto* Peer=SocialPartner.Get();SocialPartner=nullptr;PerceivedPeer.Reset();
 SocialDeadlineRemaining=SocialValidationRemaining=0;
 if(IsValid(Peer) && Peer->SocialPartner==this)
 {
  Peer->SocialPartner=nullptr;Peer->PerceivedPeer.Reset();
  Peer->bActivityRunning=Peer->bActivityTravelling=false;
  Peer->ActivityRemaining=Peer->ActivityElapsed=Peer->SocialDeadlineRemaining=0;
  Peer->Path.Reset();Peer->CurrentSpeed=0;
  Peer->SocialCooldown=Peer->Activities.SocialCooldown;
  Peer->PauseRemaining=Peer->ActivityRandom.FRandRange(1.f,2.5f);
  Peer->BehaviorState=EPokeMonsterOverworldState::Rest;
 }
}
void UPokeMonsterCreatureRoamingComponent::FinishActivity(bool Interrupted)
{
 if(!bActivityRunning && !SocialPartner)return;
 using S=EPokeMonsterOverworldState;
 if(BehaviorState==S::Sleep)SleepCooldown=Activities.SleepCooldown;
 if(BehaviorState==S::Forage){ForageCooldown=Activities.ForageCooldown;if(!Interrupted&&!bActivityTravelling)++ForageCompleted;}
 if(SocialPartner || BehaviorState==S::Social)
 {
  SocialCooldown=Activities.SocialCooldown;
  if(Interrupted){++SocialInterrupted;if(SocialPartner)++SocialPartner->SocialInterrupted;}
  else if(!bActivityTravelling){++SocialCompleted;if(SocialPartner)++SocialPartner->SocialCompleted;}
 }
 ReleaseSocial();bActivityRunning=bActivityTravelling=false;ActivityRemaining=ActivityElapsed=0;
 Path.Reset();PauseRemaining=ActivityRandom.FRandRange(1.f,2.5f);CurrentSpeed=0;
 BehaviorState=S::Rest;
}
bool UPokeMonsterCreatureRoamingComponent::CanSocialize() const
{
 const auto* Wild=Cast<APokeMonsterVisibleWildCreatureActor>(GetOwner());
 using S=EPokeMonsterOverworldState;
 return bActivitiesEnabled && bReady && !bPaused && !bPresentationHold && IsComponentTickEnabled()
  && Wild && Wild->LifeState==EPokeMonsterWildLifeState::Active && !GetOwner()->IsHidden()
  && !bEscapingDefeat && !bActivityDistant && !SocialPartner && SocialCooldown<=0 && CooldownRemaining<=0
  && ActivityWeights().SocialWeight>0 && !IsAmbientClockPaused()
  && (BehaviorState==S::Wander || BehaviorState==S::Idle || BehaviorState==S::Rest)
  // Honour a minimum quiet period before accepting a visit. Sleep/forage and player reactions never accept.
  && (!bActivityRunning || BehaviorState!=S::Rest || ActivityElapsed>=Activities.MinimumSeconds);
}
bool UPokeMonsterCreatureRoamingComponent::TryStartSocial(UPokeMonsterCreatureRoamingComponent* Peer,const FVector& Current)
{
 using S=EPokeMonsterOverworldState;
 if(!IsValid(Peer)||Peer==this||!CanSocialize()||!Peer->CanSocialize())return false;
 const FVector PeerPosition=Peer->GetOwner()->GetActorLocation();
 const bool Same=ActivitySpecies==Peer->ActivitySpecies;
 if((!Same&&(Activities.bPreferOwnSpecies||Peer->Activities.bPreferOwnSpecies))
  || FVector::Dist2D(Current,PeerPosition)>FMath::Min(Activities.SocialRadius,Peer->Activities.SocialRadius))return false;
 ++SocialRequests;
 ++PerceptionTraces;if(!PeerVisible(Peer)){LastSocialDecision=TEXT("Obstructed");return false;}
 if(Peer->ActivityRandom.FRand()>=Peer->ActivityWeights().SocialAcceptance*(Peer->bRhythmEnabled&&Peer->BehaviorState==S::Rest?.5f:1.f))
 {
  ++Peer->SocialDeclined;Peer->LastSocialDecision=TEXT("Declined");LastSocialDecision=TEXT("Rejected");
  SocialCooldown=ActivityRandom.FRandRange(6.f,10.f);Peer->SocialCooldown=Peer->ActivityRandom.FRandRange(3.f,5.f);
  return false;
 }
 const bool Shy=Settings.Behavior.Temperament==EPokeMonsterOverworldTemperament::Shy
  || Peer->Settings.Behavior.Temperament==EPokeMonsterOverworldTemperament::Shy;
 const float Separation=BodyRadius+Peer->BodyRadius+ActivityRandom.FRandRange(65.f,95.f)+(Shy?100.f:0.f);
 const FVector PeerGround=PeerPosition-FVector(0,0,Peer->Offset);
 const FVector Direction=(Current-PeerGround).GetSafeNormal2D(SMALL_NUMBER,FVector::ForwardVector);
 const float Angle=ActivityRandom.FRandRange(-16.f,16.f);
 bool Planned=false;
 for(float Turn:{Angle,0.f,-Angle})
  if(Plan(PeerGround+Direction.RotateAngleAxis(Turn,FVector::UpVector)*Separation)){Planned=true;break;}
 if(!Planned){SocialCooldown=6.f;LastSocialDecision=TEXT("NoApproachSpace");return false;}
 // All invitations and reservations execute on the game thread. Recheck immediately before claiming.
 if(!Peer->CanSocialize()){Path.Reset();return false;}
 Peer->FinishActivity(true);
 SocialPartner=Peer;Peer->SocialPartner=this;bSocialLeader=true;Peer->bSocialLeader=false;
 const float Duration=ActivityRandom.FRandRange(Activities.MinimumSeconds+2.f,Activities.MinimumSeconds+6.f);
 for(auto* M:{this,Peer})
 {
  M->bActivityRunning=true;M->BehaviorState=S::Social;M->ActivityElapsed=0;
  M->ActivityRemaining=Duration;M->SocialDeadlineRemaining=30.f;M->SocialValidationRemaining=0;
  M->PauseRemaining=0;M->LastSocialDecision=TEXT("Accepted");
 }
 // Receiver explicitly accepts and waits, facing the bounded approach. No moving-target chase.
 Peer->bActivityTravelling=false;Peer->Path.Reset();Peer->CurrentSpeed=0;
 bActivityTravelling=true;ActivityTravelRemaining=20.f;
 return true;
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
  if(Distance>FMath::Min(Activities.SocialRadius,Peer->Activities.SocialRadius) || FMath::Abs(GetOwner()->GetActorLocation().Z-Wild->GetActorLocation().Z)>100)continue;
  const bool Same=ActivitySpecies==Peer->ActivitySpecies;
  if((Activities.bPreferOwnSpecies||Peer->Activities.bPreferOwnSpecies)&&!Same)continue;
  // Peripheral peers do not constantly distract a resting creature.
  const FVector Direction=(Wild->GetActorLocation()-GetOwner()->GetActorLocation()).GetSafeNormal2D();
  const float BehindPenalty=FVector::DotProduct(Direction,GetOwner()->GetActorForwardVector())<-.25f?100.f:0.f;
  ++PerceptionTraces;if(!PeerVisible(Peer)){LastSocialDecision=TEXT("Obstructed");continue;}
  const float Score=Distance+(Same?0:150)+BehindPenalty;
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
 // Player/threat reactions above have priority. Only ambient timers/motion follow the clock pause.
 if(IsAmbientClockPaused())
 {
  if(SocialPartner&&!IsSocialPartnerValid())FinishActivity(true);
  CurrentSpeed=0;return true;
 }
 if(bRhythmEnabled)
 {
  RhythmRefreshRemaining-=Delta;
  if(RhythmRefreshRemaining<=0)RefreshRhythm();
 }
 const auto& Weights=ActivityWeights();
 SocialCooldown=FMath::Max(0.f,SocialCooldown-Delta);SleepCooldown=FMath::Max(0.f,SleepCooldown-Delta);ForageCooldown=FMath::Max(0.f,ForageCooldown-Delta);
 PeerQueryRemaining-=Delta;SocialInvitationRemaining-=Delta;
 if(bActivityRunning)ActivityElapsed+=Delta;
 // Invitations can also occur during an established idle, rest or walk. One bounded query per interval.
 if(bActivityRunning && ActivityElapsed>=Activities.MinimumSeconds && SocialInvitationRemaining<=0 && CanSocialize())
 {
  SocialInvitationRemaining=ActivityRandom.FRandRange(8.f,13.f);
  const float Total=Weights.WanderWeight+Weights.ObserveWeight+Weights.RestWeight+Weights.ForageWeight+Weights.SocialWeight;
  if(ActivityRandom.FRand()<FMath::Min(.5f,2.f*Weights.SocialWeight/FMath::Max(1.f,Total)))
  {
   if(FindSocialPartner())TryStartSocial(PerceivedPeer.Get(),Current);
   PeerQueryRemaining=Activities.PerceptionSeconds;
  }
 }
 if(bActivityRunning)
 {
  if(BehaviorState==S::Social)
  {
   auto* Peer=SocialPartner.Get();
   SocialDeadlineRemaining-=Delta;SocialValidationRemaining-=Delta;
   if(!IsSocialPartnerValid()){FinishActivity(true);return true;}
   if(SocialValidationRemaining<=0)
   {
    SocialValidationRemaining=ActivityRandom.FRandRange(.8f,1.2f);++PerceptionTraces;
    if(!PeerVisible(Peer)){FinishActivity(true);return true;}
   }
   ActivityFocus=Peer->GetOwner()->GetActorLocation();
   // The initiator owns the dwell clock; the receiver has an independent safety deadline.
   if(!bSocialLeader){CurrentSpeed=0;FaceActivity(Delta,ActivityFocus);return true;}
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
 S Next=FPokeMonsterCreatureActivityProfile::Select(Weights,ActivityRandom,bRhythmEnabled?EPokeMonsterActivityPeriod::Day:ActivityPeriod,SleepCooldown<=0,ForageCooldown<=0,Social);
 ++ActivityDecisions;
 if(Next==S::Social)
 {
  if(TryStartSocial(PerceivedPeer.Get(),Current))return false;
  Next=S::Idle;
 }
 if(Next==S::Forage)
 {
  if(!PlanForage(Current)){ForageCooldown=Activities.ForageCooldown;Next=S::Idle;}
  else {bActivityTravelling=true;ActivityTravelRemaining=20;}
 }
 BehaviorState=Next;bActivityRunning=true;ActivityElapsed=0;
 ActivityRemaining=ActivityRandom.FRandRange(Activities.MinimumSeconds,Activities.MaximumSeconds);
 if(Next==S::Rest)ActivityRemaining=Activities.RestSeconds*ActivityRandom.FRandRange(.8f,1.2f);
 if(Next==S::Sleep)ActivityRemaining=Activities.SleepSeconds*ActivityRandom.FRandRange(.8f,1.2f);

 if(Next==S::Idle)ActivityFocus=Current+GetOwner()->GetActorForwardVector().RotateAngleAxis(ActivityRandom.FRandRange(-65,65),FVector::UpVector)*150;
 PauseRemaining=0;
 return Next!=S::Wander && !bActivityTravelling;
}

void UPokeMonsterCreatureRoamingComponent::ConfigureRhythm(int32 Seed)
{
 UnbindRhythm();RhythmRefreshes=0;RhythmOffsetMinutes=0;
 if(!bActivitiesEnabled)return;
 const auto* Config=GetDefault<UPokeMonsterCreatureRhythmSettings>();
 if(!Config->bEnableRhythms)return;
 if(bOverrideRhythm){if(!RhythmOverride.IsValid())return;Rhythm=RhythmOverride;}
 else if(!Config->Find(ActivitySpecies,Rhythm))return;
 auto* GI=GetWorld()->GetGameInstance();auto* Clock=GI?GI->GetSubsystem<UPokeMonsterWorldClock>():nullptr;
 if(!Clock)return;
 // Separate stream preserves the established movement/social random sequence.
 FRandomStream R(Seed^0x72A039);RhythmOffsetMinutes=R.FRandRange(-Rhythm.IndividualOffsetMinutes,Rhythm.IndividualOffsetMinutes);
 BindRhythm(Clock);
}
void UPokeMonsterCreatureRoamingComponent::BindRhythm(UPokeMonsterWorldClock* Clock)
{
 RhythmClock=Clock;bRhythmEnabled=Clock!=nullptr;
 if(!Clock)return;
 Clock->OnTimeSet.AddUniqueDynamic(this,&UPokeMonsterCreatureRoamingComponent::RhythmTimeSet);
 Clock->OnPhaseChanged.AddUniqueDynamic(this,&UPokeMonsterCreatureRoamingComponent::RhythmPhaseChanged);
 RefreshRhythm();
}
void UPokeMonsterCreatureRoamingComponent::UnbindRhythm()
{
 if(auto* C=RhythmClock.Get())
 {
  C->OnTimeSet.RemoveDynamic(this,&UPokeMonsterCreatureRoamingComponent::RhythmTimeSet);
  C->OnPhaseChanged.RemoveDynamic(this,&UPokeMonsterCreatureRoamingComponent::RhythmPhaseChanged);
 }
 RhythmClock.Reset();bRhythmEnabled=false;
}
void UPokeMonsterCreatureRoamingComponent::RefreshRhythm()
{
 auto* C=RhythmClock.Get();if(!bRhythmEnabled||!C)return;
 const auto* Config=GetDefault<UPokeMonsterWorldClockSettings>();if(!Config->IsValidConfiguration())return;
 RhythmActivity=Rhythm.ActivityAt(C->GetTime().SecondsOfDay,RhythmOffsetMinutes,*Config);
 RhythmActivities=Rhythm.Weight(Activities,RhythmActivity);++RhythmRefreshes;
 RhythmRefreshRemaining=FMath::Max(.5f,3.f/float(FMath::Max(1.,C->GetDebugSpeed())));
 // Existing activity, path, reservation and minimum duration deliberately survive phase/time changes.
}
void UPokeMonsterCreatureRoamingComponent::RhythmTimeSet(FPokeMonsterWorldTime){RefreshRhythm();}
void UPokeMonsterCreatureRoamingComponent::RhythmPhaseChanged(EPokeMonsterDayPhase){RefreshRhythm();}
bool UPokeMonsterCreatureRoamingComponent::IsAmbientClockPaused() const
{return bRhythmEnabled&&RhythmClock.IsValid()&&RhythmClock->IsClockPaused();}
bool UPokeMonsterCreatureRoamingComponent::IsSocialPartnerValid() const
{
 const auto* Peer=SocialPartner.Get();const auto* Wild=IsValid(Peer)?Cast<APokeMonsterVisibleWildCreatureActor>(Peer->GetOwner()):nullptr;
 return IsValid(Peer)&&Peer->SocialPartner==this&&Wild&&Wild->LifeState==EPokeMonsterWildLifeState::Active
  &&!Peer->bPaused&&!Peer->bPresentationHold&&!Peer->bEscapingDefeat&&!Peer->bActivityDistant
  &&!Peer->GetOwner()->IsHidden()&&Peer->IsComponentTickEnabled()&&SocialDeadlineRemaining>0
  &&FVector::Dist2D(GetOwner()->GetActorLocation(),Peer->GetOwner()->GetActorLocation())<=FMath::Min(Activities.SocialRadius,Peer->Activities.SocialRadius)*1.4f;
}
