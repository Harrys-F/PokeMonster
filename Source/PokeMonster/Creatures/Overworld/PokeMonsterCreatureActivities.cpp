#include "PokeMonsterCreatureActivities.h"
bool FPokeMonsterCreatureActivityProfile::IsValid() const
{
 const float Values[]={WanderWeight,ObserveWeight,RestWeight,SleepWeight,ForageWeight,SocialWeight,
 MinimumSeconds,MaximumSeconds,RestSeconds,SleepSeconds,SocialCooldown,SleepCooldown,ForageCooldown,
 PerceptionSeconds,SocialRadius,ActiveDistance};
 for(float V:Values)if(!FMath::IsFinite(V)||V<0)return false;
 return WanderWeight>0 && MinimumSeconds>=3 && MaximumSeconds>=MinimumSeconds && MaximumSeconds<=60
  && RestSeconds>=MinimumSeconds && SleepSeconds>=MinimumSeconds && SleepSeconds<=120
  && SocialCooldown>=15 && SleepCooldown>=30 && ForageCooldown>=10
  && PerceptionSeconds>=.5f && PerceptionSeconds<=5 && SocialRadius>=150 && SocialRadius<=800
  && ActiveDistance>=1500 && ActiveDistance<=10000;
}
FPokeMonsterCreatureActivityProfile FPokeMonsterCreatureActivityProfile::ForSpecies(FName Species)
{
 FPokeMonsterCreatureActivityProfile P;
 if(Species==TEXT("Bisasam")){P.bEnabled=true;P.WanderWeight=3;P.RestWeight=4;P.ForageWeight=5;P.bPreferVegetation=true;}
 else if(Species==TEXT("Pikachu")){P.bEnabled=true;P.WanderWeight=7;P.RestWeight=1;P.SleepWeight=.2f;P.MinimumSeconds=4;P.MaximumSeconds=9;P.bPreferVegetation=true;}
 else if(Species==TEXT("Zunderlauf")){P.bEnabled=true;P.ObserveWeight=4;P.ForageWeight=4;P.bPreferOwnSpecies=false;}
 else if(Species==TEXT("Myrapla")){P.bEnabled=true;P.WanderWeight=2;P.RestWeight=5;P.SleepWeight=1;P.ForageWeight=5;P.RestSeconds=20;P.bPreferVegetation=true;}
 else if(Species==TEXT("Enton")){P.bEnabled=true;P.WanderWeight=4;P.ObserveWeight=4;P.SocialWeight=4;P.RestWeight=3;P.bPreferOwnSpecies=false;}
 else if(Species==TEXT("Nebulak")){P.bEnabled=true;P.ObserveWeight=5;P.SocialWeight=.5f;P.SleepWeight=.2f;P.ForageWeight=1;P.bPreferOwnSpecies=false;}
 return P;
}
EPokeMonsterOverworldState FPokeMonsterCreatureActivityProfile::Select(const FPokeMonsterCreatureActivityProfile& P,
 FRandomStream& R, EPokeMonsterActivityPeriod Period, bool Sleep, bool Forage, bool Social)
{
 using S=EPokeMonsterOverworldState;
 if(!P.IsValid())return S::Rest;
 const S States[]={S::Wander,S::Idle,S::Rest,S::Sleep,S::Forage,S::Social};
 const float Weights[]={P.WanderWeight,P.ObserveWeight,P.RestWeight,
 Sleep?P.SleepWeight*(Period==EPokeMonsterActivityPeriod::Night?4.f:Period==EPokeMonsterActivityPeriod::Evening?2.f:1.f):0.f,
 Forage?P.ForageWeight:0.f,Social?P.SocialWeight:0.f};
 float Total=0;for(float W:Weights)Total+=W;
 float Choice=R.FRand()*Total;
 for(int32 I=0;I<UE_ARRAY_COUNT(States);++I){Choice-=Weights[I];if(Choice<0)return States[I];}
 return S::Wander;
}
