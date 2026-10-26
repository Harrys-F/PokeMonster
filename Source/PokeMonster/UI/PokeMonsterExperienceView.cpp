#include "PokeMonsterExperienceView.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"

FPokeMonsterExperienceView FPokeMonsterExperienceView::FromCreature(const FPokeMonsterCreatureInstance& C)
{
 return IsValid(C.Species.LoadSynchronous())?Calculate(C.GetExperienceGrowthRate(),C.Level,C.Experience):FPokeMonsterExperienceView();
}
FPokeMonsterExperienceView FPokeMonsterExperienceView::Calculate(EPokeMonsterGrowthRate Rate,int32 L,int64 XP)
{
 FPokeMonsterExperienceView V;
 using P=UPokeMonsterCreatureProgression;
 if(L<P::MinLevel||L>P::MaxLevel||XP<0)return V;
 const int64 Floor=P::ExperienceForLevel(Rate,L);
 const int64 Next=P::ExperienceForLevel(Rate,L<P::MaxLevel?L+1:L);
 if(Floor<0||Next<Floor||XP<Floor||(L<P::MaxLevel&&XP>=Next)||(L==P::MaxLevel&&XP!=Floor))return V;
 V.bValid=true;V.Growth=Rate;V.Level=L;V.Total=XP;V.LevelStart=Floor;V.NextLevelStart=Next;V.bMaximumLevel=L==P::MaxLevel;
 if(V.bMaximumLevel){V.Fraction=1;return V;}
 V.Required=Next-Floor;V.Earned=XP-Floor;V.Remaining=Next-XP;
 V.Fraction=V.Required>0?FMath::Clamp(float(double(V.Earned)/double(V.Required)),0.f,1.f):0.f;
 return V;
}
FPokeMonsterExperienceView FPokeMonsterExperienceView::Interpolate(const FPokeMonsterExperienceView& Before,const FPokeMonsterExperienceView& After,float Alpha)
{
 if(!Before.bValid||!After.bValid||Before.Growth!=After.Growth||After.Total<Before.Total)return After;
 if(!FMath::IsFinite(Alpha))return Before;
 const int64 XP=Before.Total+FMath::RoundToInt64(double(After.Total-Before.Total)*FMath::Clamp(Alpha,0.f,1.f));
 int32 Level=Before.Level;
 while(Level<UPokeMonsterCreatureProgression::MaxLevel&&XP>=UPokeMonsterCreatureProgression::ExperienceForLevel(Before.Growth,Level+1))++Level;
 return Calculate(Before.Growth,Level,XP);
}
FText FPokeMonsterExperienceView::ProgressText() const
{
 if(!bValid)return FText::FromString(TEXT("EP · nicht verfügbar"));
 if(bMaximumLevel)return FText::FromString(TEXT("EP · MAX"));
 return FText::Format(NSLOCTEXT("PokeMonster","XPProgress","EP: {0} / {1}"),FText::AsNumber(Earned),FText::AsNumber(Required));
}
FText FPokeMonsterExperienceView::RemainingText() const
{
 if(!bValid)return FText::FromString(TEXT("Erfahrungsdaten prüfen"));
 if(bMaximumLevel)return FText::Format(NSLOCTEXT("PokeMonster","XPMax","Höchstlevel {0} erreicht"),FText::AsNumber(Level));
 return FText::Format(NSLOCTEXT("PokeMonster","XPRemaining","Bis Level {0}: {1} EP"),FText::AsNumber(Level+1),FText::AsNumber(Remaining));
}
