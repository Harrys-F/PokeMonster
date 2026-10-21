#include "PokeMonsterCreatureBehavior.h"
bool FPokeMonsterCreatureBehaviorProfile::IsValid() const
{
 const float V[]={NoticeRadius,PersonalSpace,DisengageRadius,WarningSeconds,EncounterRadius,EncounterCooldown,WalkMultiplier,ReactionSpeedMultiplier,RestMultiplier};
 for(float X:V) if(!FMath::IsFinite(X))return false;
 return static_cast<uint8>(Temperament)<=static_cast<uint8>(EPokeMonsterOverworldTemperament::Calm)
  && PersonalSpace>=100 && NoticeRadius>PersonalSpace && DisengageRadius>NoticeRadius
  && WarningSeconds>=1 && EncounterRadius>=100 && EncounterRadius<NoticeRadius && EncounterCooldown>=5
  && WalkMultiplier>0 && WalkMultiplier<=1.5f && ReactionSpeedMultiplier>=1 && ReactionSpeedMultiplier<=3
  && RestMultiplier>=.5f && RestMultiplier<=5;
}
EPokeMonsterOverworldState FPokeMonsterCreatureBehavior::Decide(const FPokeMonsterCreatureBehaviorProfile& P,
 float D,bool Visible,bool Reacting,bool Cooling)
{
 using S=EPokeMonsterOverworldState;using T=EPokeMonsterOverworldTemperament;
 if(!P.IsValid()||!FMath::IsFinite(D)||D<0)return S::Rest;
 if(Cooling)return S::Cooldown;
 if(!Visible||D>(Reacting?P.DisengageRadius:P.NoticeRadius))return S::Wander;
 switch(P.Temperament)
 {
 case T::Shy:return S::Retreat;
 case T::Curious:return D<P.PersonalSpace?S::Retreat:D>P.PersonalSpace+100?S::Approach:S::Observe;
 case T::Territorial:return S::Warning;
 default:return D<P.PersonalSpace?S::Observe:S::Wander;
 }
}
bool FPokeMonsterCreatureBehavior::CanInitiate(const FPokeMonsterCreatureBehaviorProfile& P,float D,
 float Elapsed,bool Visible,bool Armed,bool Cooling)
{
 return P.IsValid()&&P.Temperament==EPokeMonsterOverworldTemperament::Territorial&&P.bCanInitiateEncounter
  &&FMath::IsFinite(D)&&D>=0&&D<=P.EncounterRadius&&FMath::IsFinite(Elapsed)&&Elapsed>=P.WarningSeconds
  &&Visible&&Armed&&!Cooling;
}
