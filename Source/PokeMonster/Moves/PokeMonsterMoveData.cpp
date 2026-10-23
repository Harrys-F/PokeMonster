#include "PokeMonsterMoveData.h"

FPrimaryAssetId UPokeMonsterMoveData::GetPrimaryAssetId() const
{
	return FPrimaryAssetId(TEXT("CreatureMove"), InternalId.IsNone() ? GetFName() : InternalId);
}

bool UPokeMonsterMoveData::IsConfigured() const
{
	const bool bKnownType = Type >= EPokeMonsterCreatureType::Normal && Type <= EPokeMonsterCreatureType::Steel;
	const bool bValidPower = Category == EPokeMonsterMoveCategory::Status ? BasePower == 0
		: (Category == EPokeMonsterMoveCategory::Physical || Category == EPokeMonsterMoveCategory::Special) && (BasePower > 0 || (BasePower == 0 && HasEffect(EPokeMonsterEffectKind::FixedDamage)));
 int32 Fixed=0,Multi=0;
 for(const auto& E:Effects){Fixed+=E.Kind==EPokeMonsterEffectKind::FixedDamage;Multi+=E.Kind==EPokeMonsterEffectKind::MultiHit;}
 if(Fixed>1 || Multi>1 || (Category==EPokeMonsterMoveCategory::Status && (Fixed || Multi)))return false;
	return !InternalId.IsNone() && !DisplayName.IsEmpty() && bKnownType && bValidPower
		&& Accuracy >= 0 && Accuracy <= 100 && MaxPP > 0
		&& Effect.ChancePercent >= 0 && Effect.ChancePercent <= 100
  && CriticalStageBonus==0
  && !Effects.ContainsByPredicate([](const auto& E){return !E.IsConfigured();});
}

FText UPokeMonsterMoveData::GetPlayerFacingName()const
{
 if(InternalId.ToString().StartsWith(TEXT("Test"))||DisplayName.ToString().StartsWith(TEXT("Test")))return FText::FromString(Category==EPokeMonsterMoveCategory::Status?TEXT("Statusversuch · Test"):Category==EPokeMonsterMoveCategory::Physical?TEXT("Körperangriff · Test"):TEXT("Elementangriff · Test"));
 return DisplayName;
}

bool FPokeMonsterMoveEffectComponent::IsConfigured()const
{
 if(uint8(Kind)>uint8(EPokeMonsterEffectKind::CriticalFocus) || uint8(Stat)>uint8(EPokeMonsterBattleStat::Evasion)
  || ChancePercent<0 || ChancePercent>100 || MinTurns<1 || MaxTurns<MinTurns || MaxTurns>15
  || Numerator<0 || Denominator<1 || Amount<0)return false;
 if(Kind==EPokeMonsterEffectKind::Stage && (Stages==0 || Stages < -6 || Stages>6))return false;
 if(Kind==EPokeMonsterEffectKind::PrimaryStatus && (Status==EPokeMonsterCreatureStatus::None || uint8(Status)>uint8(EPokeMonsterCreatureStatus::Freeze)))return false;
 if((Kind==EPokeMonsterEffectKind::Drain || Kind==EPokeMonsterEffectKind::Recoil || Kind==EPokeMonsterEffectKind::Heal || Kind==EPokeMonsterEffectKind::Protect) && (Numerator<=0 || Numerator>Denominator || !bSelf))return false;
 if((Kind==EPokeMonsterEffectKind::FixedDamage || Kind==EPokeMonsterEffectKind::MultiHit) && (ChancePercent!=100 || bSelf || bSecondary))return false;
 if(Kind==EPokeMonsterEffectKind::Screen && !bSelf)return false;
 if(Kind==EPokeMonsterEffectKind::MultiHit)
 {
  if(MinHits<2 || MaxHits<MinHits || MaxHits>10 || HitWeights.Num()!=MaxHits-MinHits+1)return false;
  int64 Total=0;for(int32 W:HitWeights){if(W<0)return false;Total+=W;}if(Total<=0 || Total>MAX_int32)return false;
 }
 // Unimplemented component kinds fail validation instead of silently becoming playable placeholders.
 switch(Kind){case EPokeMonsterEffectKind::Stage:case EPokeMonsterEffectKind::PrimaryStatus:case EPokeMonsterEffectKind::Drain:case EPokeMonsterEffectKind::Recoil:case EPokeMonsterEffectKind::Heal:case EPokeMonsterEffectKind::FixedDamage:case EPokeMonsterEffectKind::MultiHit:case EPokeMonsterEffectKind::Flinch:case EPokeMonsterEffectKind::Confusion:case EPokeMonsterEffectKind::Protect:case EPokeMonsterEffectKind::Screen:break;default:return false;}
 return true;
}

TArray<FPokeMonsterMoveEffectComponent> UPokeMonsterMoveData::GetEffectComponents()const
{
 if(!Effects.IsEmpty())return Effects;
 TArray<FPokeMonsterMoveEffectComponent> Out;
 FPokeMonsterMoveEffectComponent E;E.ChancePercent=Effect.ChancePercent;
 const auto Id=Effect.EffectId;
 if(Id==TEXT("AttackDown")){E.Kind=EPokeMonsterEffectKind::Stage;E.Stat=EPokeMonsterBattleStat::Attack;}
 else if(Id==TEXT("DefenseDown")){E.Kind=EPokeMonsterEffectKind::Stage;E.Stat=EPokeMonsterBattleStat::Defense;}
 else if(Id==TEXT("DefenseUp")){E.Kind=EPokeMonsterEffectKind::Stage;E.Stat=EPokeMonsterBattleStat::Defense;E.Stages=1;E.bSelf=true;}
 else if(Id==TEXT("SpeedDown")){E.Kind=EPokeMonsterEffectKind::Stage;E.Stat=EPokeMonsterBattleStat::Speed;E.bSecondary=true;}
 else if(Id==TEXT("Burn")){E.Kind=EPokeMonsterEffectKind::PrimaryStatus;E.Status=EPokeMonsterCreatureStatus::Burn;E.bSecondary=true;E.ImmuneTypes={EPokeMonsterCreatureType::Fire};}
 else if(Id==TEXT("DrainHalf")){E.Kind=EPokeMonsterEffectKind::Drain;E.bSelf=true;}
 else if(Id==TEXT("UserLevelDamage")){E.Kind=EPokeMonsterEffectKind::FixedDamage;}
 else return Out; // Legacy Leech Seed/Struggle keep their existing lifecycle; no guessed conversion.
 // Only legacy burn/speed effects used the old chance field. Preserve guaranteed legacy stages/drain/fixed damage.
 if(!E.bSecondary)E.ChancePercent=100;
 Out.Add(E);return Out;
}

bool UPokeMonsterMoveData::HasEffect(EPokeMonsterEffectKind Kind)const
{
 return GetEffectComponents().ContainsByPredicate([Kind](const auto& E){return E.Kind==Kind;});
}
