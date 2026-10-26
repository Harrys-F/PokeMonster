#include "PokeMonsterCreatureRhythm.h"
#include "../../Time/PokeMonsterWorldClock.h"
bool FPokeMonsterCreatureRhythm::IsValid() const
{
 const float Values[]={ActiveWander,QuietWander,ActiveForage,QuietForage,ActiveSocial,QuietSocial,ActiveRest,QuietRest,ActiveSleep,QuietSleep,QuietAcceptance};
 for(float V:Values)if(!FMath::IsFinite(V)||V<0||V>12)return false;
 if(!FMath::IsFinite(IndividualOffsetMinutes)||IndividualOffsetMinutes<0||IndividualOffsetMinutes>120)return false;
 return uint8(Rhythm)<=uint8(EPokeMonsterActivityRhythm::Flexible)&&QuietAcceptance<=1&&ActiveWander>0&&QuietWander>0;
}
float FPokeMonsterCreatureRhythm::ActivityAt(double Seconds,float Offset,const UPokeMonsterWorldClockSettings& C) const
{
 auto Smooth=[](double A,double B,double H){const double T=FMath::Clamp((H-A)/FMath::Max(.01,B-A),0.,1.);return float(T*T*(3-2*T));};
 const double H=FMath::Fmod(Seconds/3600.+Offset/60.+48.,24.);
 const double Early=C.PhaseStartMinutes[0]/60.,Dawn=C.PhaseStartMinutes[1]/60.,Day=C.PhaseStartMinutes[2]/60.,Dusk=C.PhaseStartMinutes[3]/60.,Night=C.PhaseStartMinutes[4]/60.;
 const float Sun=Smooth(Dawn,Day,H)*(1-Smooth(Dusk,Night,H));
 switch(Rhythm)
 {
 case EPokeMonsterActivityRhythm::Diurnal:return Sun;
 case EPokeMonsterActivityRhythm::Nocturnal:return 1-Sun;
 case EPokeMonsterActivityRhythm::Crepuscular:return FMath::Max(Smooth(Early,Dawn,H)*(1-Smooth(Day,Day+1,H)),Smooth(Dusk-1,Dusk,H)*(1-Smooth(Night,Night+1,H)));
 default:return .75f+.1f*Sun;
 }
}
FPokeMonsterCreatureActivityProfile FPokeMonsterCreatureRhythm::Weight(const FPokeMonsterCreatureActivityProfile& Base,float A) const
{
 auto P=Base;A=FMath::Clamp(A,0.f,1.f);
 P.WanderWeight*=FMath::Lerp(QuietWander,ActiveWander,A);
 P.ForageWeight*=FMath::Lerp(QuietForage,ActiveForage,A);
 P.SocialWeight*=FMath::Lerp(QuietSocial,ActiveSocial,A);
 P.RestWeight*=FMath::Lerp(QuietRest,ActiveRest,A);
 P.SleepWeight*=FMath::Lerp(QuietSleep,ActiveSleep,A);
 P.SocialAcceptance*=FMath::Lerp(QuietAcceptance,1.f,A);
 return P;
}
bool UPokeMonsterCreatureRhythmSettings::Find(FName Id,FPokeMonsterCreatureRhythm& Result) const
{
 if(!bEnableRhythms)return false;
 const FPokeMonsterSpeciesRhythm* Found=nullptr;
 for(const auto& Row:SpeciesProfiles)if(Row.Species==Id){if(Found||!Row.Profile.IsValid())return false;Found=&Row;}
 if(!Found)return false;Result=Found->Profile;return true;
}
