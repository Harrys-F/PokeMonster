#include "PokeMonsterCreatureBehavior.h"
bool FPokeMonsterCreaturePerceptionProfile::IsValid() const
{
 const float V[]={FieldOfView,NoticeRadius,SampleSeconds,ReactionSeconds,ForgetSeconds,MaximumChaseSeconds,InvestigationSeconds};
 for(float X:V)if(!FMath::IsFinite(X))return false;
 return FieldOfView>=30&&FieldOfView<=360&&NoticeRadius>=0&&NoticeRadius<=1600
  &&SampleSeconds>=.2f&&SampleSeconds<=2&&ReactionSeconds>=0&&ReactionSeconds<=3
  &&ForgetSeconds>=.2f&&ForgetSeconds<=5&&MaximumChaseSeconds>=2&&MaximumChaseSeconds<=20
  &&InvestigationSeconds>=2&&InvestigationSeconds<=20;
}
bool FPokeMonsterCreatureBehavior::InView(const FPokeMonsterCreatureBehaviorProfile& P,const FVector& Observer,const FVector& Forward,const FVector& Target)
{
 if(Observer.ContainsNaN()||Forward.ContainsNaN()||Target.ContainsNaN())return false;
 if(!P.Perception.bEnabled||FVector::Dist2D(Observer,Target)<=P.PersonalSpace)return true;
 return FVector::DotProduct(Forward.GetSafeNormal2D(),(Target-Observer).GetSafeNormal2D())>=FMath::Cos(FMath::DegreesToRadians(P.Perception.FieldOfView*.5f));
}
bool FPokeMonsterCreatureBehavior::UpdateAwareness(const FPokeMonsterCreaturePerceptionProfile& P,float Delta,bool Sensed,bool Immediate,bool WasAware,float& Acquiring,float& Lost)
{
 if(!FMath::IsFinite(Delta)||Delta<=0)return WasAware;
 if(!P.bEnabled)return Sensed;
 if(Sensed){Acquiring+=Delta;Lost=0;return WasAware||Immediate||Acquiring>=P.ReactionSeconds;}
 Acquiring=0;Lost+=Delta;return WasAware&&Lost<P.ForgetSeconds;
}

bool FPokeMonsterCreatureBehaviorProfile::IsValid() const
{
 const float V[]={NoticeRadius,PersonalSpace,DisengageRadius,WarningSeconds,EncounterRadius,EncounterCooldown,WalkMultiplier,ReactionSpeedMultiplier,RestMultiplier};
 for(float X:V) if(!FMath::IsFinite(X))return false;
 return Perception.IsValid()&&static_cast<uint8>(Temperament)<=static_cast<uint8>(EPokeMonsterOverworldTemperament::Aggressive)
  && static_cast<uint8>(Initiation)<=static_cast<uint8>(EPokeMonsterEncounterInitiation::Disabled)
  && PersonalSpace>=100 && NoticeRadius>PersonalSpace && DisengageRadius>NoticeRadius
  && WarningSeconds>=1 && EncounterRadius>=100 && EncounterRadius<NoticeRadius && EncounterCooldown>=5
  && WalkMultiplier>0 && WalkMultiplier<=1.5f && ReactionSpeedMultiplier>=1 && ReactionSpeedMultiplier<=3
  && RestMultiplier>=.5f && RestMultiplier<=5;
}
EPokeMonsterOverworldState FPokeMonsterCreatureBehavior::Decide(const FPokeMonsterCreatureBehaviorProfile& P,
 float D,bool Visible,bool Reacting,bool Cooling)
{
 using EOverworldState = EPokeMonsterOverworldState;using EOverworldTemperament = EPokeMonsterOverworldTemperament;
 if(!P.IsValid()||!FMath::IsFinite(D)||D<0)return EOverworldState::Rest;
 if(Cooling)return EOverworldState::Cooldown;
 if(!Visible||D>(Reacting?P.DisengageRadius:P.NoticeRadius))return EOverworldState::Wander;
 switch(P.Temperament)
 {
 case EOverworldTemperament::Shy:return EOverworldState::Retreat;
 case EOverworldTemperament::Curious:return D<P.PersonalSpace?EOverworldState::Retreat:D>P.PersonalSpace+100?EOverworldState::Approach:EOverworldState::Observe;
 case EOverworldTemperament::Aggressive:return EOverworldState::Approach;
 case EOverworldTemperament::Territorial:return EOverworldState::Warning;
 default:return D<P.PersonalSpace?EOverworldState::Observe:EOverworldState::Wander;
 }
}
EPokeMonsterEncounterInitiation FPokeMonsterCreatureBehavior::InitiationFor(const FPokeMonsterCreatureBehaviorProfile& P)
{
 if(!P.IsValid()||!P.bCanInitiateEncounter)return EPokeMonsterEncounterInitiation::Disabled;
 if(P.Initiation!=EPokeMonsterEncounterInitiation::ByTemperament)return P.Initiation;
 return P.Temperament==EPokeMonsterOverworldTemperament::Territorial||P.Temperament==EPokeMonsterOverworldTemperament::Aggressive
  ? EPokeMonsterEncounterInitiation::Contact : EPokeMonsterEncounterInitiation::Challenge;
}
bool FPokeMonsterCreatureBehavior::CanInitiate(const FPokeMonsterCreatureBehaviorProfile& P,bool Contact,bool Interaction,bool Cooling)
{
 if(Cooling)return false;
 const auto Mode=InitiationFor(P);
 return (Mode==EPokeMonsterEncounterInitiation::Contact && Contact && !Interaction)
  ||(Mode==EPokeMonsterEncounterInitiation::Challenge && Interaction && !Contact);
}
