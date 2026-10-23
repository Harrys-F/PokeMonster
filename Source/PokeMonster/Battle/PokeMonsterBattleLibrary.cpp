#include "PokeMonsterBattleLibrary.h"
#include "PokeMonsterTypeChart.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"

bool UPokeMonsterBattleLibrary::CheckHit(const UPokeMonsterMoveData* Move, const int32 Roll)
{
	return IsValid(Move) && Move->IsConfigured() && Roll >= 0 && Roll < 100 && (Move->bNeverMiss || Roll < Move->Accuracy);
}

FPokeMonsterDamageResult UPokeMonsterBattleLibrary::CalculateDamage(const FPokeMonsterCreatureInstance& Attacker,
	const FPokeMonsterCreatureInstance& Defender, const UPokeMonsterMoveData* Move, int32 AttackStage, int32 DefenseStage, int32 SpecialAttackStage, int32 SpecialDefenseStage)
{
	FPokeMonsterDamageResult Result;
	if (!IsValid(Move) || !Move->IsConfigured() || !Attacker.IsValid() || !Defender.IsValid()) return Result;
	const UPokeMonsterCreatureSpeciesData* AttackerSpecies = Attacker.Species.LoadSynchronous();
	const UPokeMonsterCreatureSpeciesData* DefenderSpecies = Defender.Species.LoadSynchronous();
	if (!IsValid(AttackerSpecies) || !IsValid(DefenderSpecies)) return Result;
	if (Move->Category == EPokeMonsterMoveCategory::Status)
	{
		Result.bValid = true; // BattleSession applies the supported status effects.
		return Result;
	}
	const bool bPhysical = Move->Category == EPokeMonsterMoveCategory::Physical;
	int32 Offense = bPhysical ? Attacker.CalculatedStats.Attack : Attacker.CalculatedStats.SpecialAttack;
 if(Offense<=0)return Result; // Stage clamping must not turn invalid source stats into a legal attack.
 if(!bPhysical)Offense=ApplyStage(Offense,SpecialAttackStage);
 if(bPhysical){const int S=FMath::Clamp(AttackStage,-6,6);Offense=int32(FMath::Clamp<int64>(int64(Offense)*(S>=0?2+S:2)/(S>=0?2:2-S),1,MAX_int32));if(Attacker.Status==EPokeMonsterCreatureStatus::Burn)Offense=FMath::Max(1,Offense/2);}
	const int32 Defense = bPhysical ? ApplyStage(Defender.CalculatedStats.Defense, DefenseStage) : ApplyStage(Defender.CalculatedStats.SpecialDefense,SpecialDefenseStage);
	if (Offense <= 0 || Defense <= 0) return Result;
	Result.TypeMultiplier = Move->Effect.EffectId==TEXT("Struggle")?1.f:GetTypeMultiplier(Move->Type, DefenderSpecies->GetPrimaryType(), DefenderSpecies->GetSecondaryType());
	if (Result.TypeMultiplier < 0.0f) return Result;
	Result.bValid = true;
	if (Result.TypeMultiplier == 0.0f) return Result;
	if (Move->HasEffect(EPokeMonsterEffectKind::FixedDamage))
	{
		// Night Shade / Seismic Toss: immunity applies; resistance/weakness does not.
		Result.TypeMultiplier = 1.f;
		const auto Specs=Move->GetEffectComponents();const auto* Fixed=Specs.FindByPredicate([](const auto& E){return E.Kind==EPokeMonsterEffectKind::FixedDamage;});
  Result.Damage=Fixed && Fixed->Amount>0?Fixed->Amount:Attacker.Level;
		return Result;
	}
	// Working formula only: no STAB, critical hits, random damage, abilities or complete Generation-2 arithmetic.
	// Double intermediates avoid integer overflow even for malformed/extreme positive designer values.
	const double Base = FMath::FloorToDouble((2 * Attacker.Level / 5 + 2) * static_cast<double>(Move->BasePower)
		* Offense / Defense / 50.0) + 2.0;
	Result.Damage = static_cast<int32>(FMath::Clamp(FMath::FloorToDouble(Base * Result.TypeMultiplier), 1.0, double(MAX_int32)));
	return Result;
}

float UPokeMonsterBattleLibrary::GetTypeMultiplier(const EPokeMonsterCreatureType Attack,
	const EPokeMonsterCreatureType Primary, const EPokeMonsterCreatureType Secondary)
{
	return PokeMonsterTypeChart::GetMultiplier(Attack, Primary, Secondary);
}

bool UPokeMonsterBattleLibrary::AssignMove(FPokeMonsterCreatureInstance& Creature, const int32 SlotIndex, UPokeMonsterMoveData* Move)
{
	return Creature.IsValid() && Creature.AssignMove(SlotIndex, Move);
}

bool UPokeMonsterBattleLibrary::ConsumeMovePP(FPokeMonsterCreatureInstance& Creature, const int32 SlotIndex, const int32 Amount)
{
	return Creature.IsValid() && Creature.ConsumeMovePP(SlotIndex, Amount);
}

int32 UPokeMonsterBattleLibrary::ApplyStage(int32 Value,int32 Stage)
{
 if(Value<=0)return 0;
 const int S=FMath::Clamp(Stage,-6,6);
 return int32(FMath::Clamp<int64>(int64(Value)*(S>=0?2+S:2)/(S>=0?2:2-S),1,MAX_int32));
}

int32 UPokeMonsterBattleLibrary::AccuracyAtStages(int32 BaseAccuracy,int32 AccuracyStage,int32 EvasionStage)
{
 const int32 S=FMath::Clamp(FMath::Clamp(AccuracyStage,-6,6)-FMath::Clamp(EvasionStage,-6,6),-6,6);
 return int32(FMath::Clamp<int64>(int64(FMath::Clamp(BaseAccuracy,0,100))*(S>=0?3+S:3)/(S>=0?3:3-S),0,100));
}
FText UPokeMonsterBattleLibrary::StatusLabel(EPokeMonsterCreatureStatus Status)
{
 static const TCHAR* Labels[]={TEXT(""),TEXT("BRN"),TEXT("PAR"),TEXT("SLP"),TEXT("PSN"),TEXT("FRZ")};
 return FText::FromString(uint8(Status)<UE_ARRAY_COUNT(Labels)?Labels[uint8(Status)]:TEXT("?"));
}


FPokeMonsterDamageResult UPokeMonsterBattleLibrary::CalculateCrystalDamage(const FPokeMonsterCreatureInstance& A,
 const FPokeMonsterCreatureInstance& D,const UPokeMonsterMoveData* M,int32 AS,int32 DS,int32 SAS,int32 SDS,
 bool Critical,int32 RandomFactor,bool Rain,bool Screen,bool Identified,bool Sunny,bool Sand,int32 DamageMultiplier)
{
 FPokeMonsterDamageResult R;
 if(!M || !M->IsConfigured() || !A.IsValid() || !D.IsValid() || RandomFactor<217 || RandomFactor>255)return R;
 const auto* SA=A.Species.LoadSynchronous();const auto* SD=D.Species.LoadSynchronous();if(!SA || !SD)return R;
 if(M->Category==EPokeMonsterMoveCategory::Status){R.bValid=true;return R;}
 const bool Struggle=M->Effect.EffectId==TEXT("Struggle");
 auto Factor=[&](EPokeMonsterCreatureType T){if(Identified && T==EPokeMonsterCreatureType::Ghost && (M->Type==EPokeMonsterCreatureType::Normal || M->Type==EPokeMonsterCreatureType::Fighting))return 1.f;return GetTypeMultiplier(M->Type,T);};
 R.TypeMultiplier=Struggle?1.f:Factor(SD->GetPrimaryType())*((SD->GetSecondaryType()==EPokeMonsterCreatureType::None || SD->GetSecondaryType()==SD->GetPrimaryType())?1.f:Factor(SD->GetSecondaryType()));
 if(R.TypeMultiplier<0)return R;R.bValid=true;if(R.TypeMultiplier==0)return R;
 if(M->HasEffect(EPokeMonsterEffectKind::FixedDamage))
 {
  const auto Effects=M->GetEffectComponents();const auto* Fixed=Effects.FindByPredicate([](const auto& E){return E.Kind==EPokeMonsterEffectKind::FixedDamage;});
  R.Damage=Fixed->Amount>0?Fixed->Amount:A.Level;R.TypeMultiplier=1;return R;
 }
 // In Gen 2 the elemental type, not an individual move flag, selects offensive stats.
 const auto Type=M->Type;const bool Special=Type==EPokeMonsterCreatureType::Fire || Type==EPokeMonsterCreatureType::Water || Type==EPokeMonsterCreatureType::Electric || Type==EPokeMonsterCreatureType::Grass || Type==EPokeMonsterCreatureType::Ice || Type==EPokeMonsterCreatureType::Psychic || Type==EPokeMonsterCreatureType::Dragon || Type==EPokeMonsterCreatureType::Dark;
 const int OStage=Special?SAS:AS,DStage=Special?SDS:DS;
 const bool Ignore=Critical && OStage<=DStage;
 int64 Offense=Special?A.CalculatedStats.SpecialAttack:A.CalculatedStats.Attack,Defense=Special?D.CalculatedStats.SpecialDefense:D.CalculatedStats.Defense;
 if(Offense<=0 || Defense<=0){R.bValid=false;return R;}
 if(!Ignore){Offense=ApplyCrystalStage(int32(Offense),OStage);Defense=ApplyCrystalStage(int32(Defense),DStage);if(!Special && A.Status==EPokeMonsterCreatureStatus::Burn)Offense=FMath::Max<int64>(1,Offense/2);if(Special && Screen)Defense*=2;}
 // Crystal truncates the two stats together when either exceeds 255; deliberately no overflow bugs.
 while(Offense>255 || Defense>255){Offense=FMath::Max<int64>(1,Offense/4);Defense=FMath::Max<int64>(1,Defense/4);}
 int64 Damage=(2*A.Level/5+2)*int64(M->BasePower)*Offense/Defense/50;
 if(Critical)Damage*=2;Damage=FMath::Min<int64>(997,Damage)+2;
 if(Rain){if(Type==EPokeMonsterCreatureType::Water)Damage=Damage*3/2;else if(Type==EPokeMonsterCreatureType::Fire)Damage/=2;}
 if(Sunny){if(Type==EPokeMonsterCreatureType::Fire)Damage=Damage*3/2;else if(Type==EPokeMonsterCreatureType::Water)Damage/=2;}
 if((Rain || Sand) && M->InternalId==TEXT("SolarBeam"))Damage/=2;
 if(!Struggle && (SA->GetPrimaryType()==Type || SA->GetSecondaryType()==Type))Damage+=Damage/2;
 Damage=int64(Damage*R.TypeMultiplier);Damage*=FMath::Clamp(DamageMultiplier,1,256);Damage=Damage*RandomFactor/255;
 R.Damage=int32(FMath::Clamp<int64>(Damage,1,MAX_int32));return R;
}

int32 UPokeMonsterBattleLibrary::CrystalAccuracy(int32 Base,int32 Accuracy,int32 Evasion,bool Identified)
{
 if(Base<=0)return 0;
 const int32 N[]={33,36,43,50,60,75,1,133,166,2,233,133,3};
 const int32 D[]={100,100,100,100,100,100,1,100,100,1,100,50,1};
 Accuracy=FMath::Clamp(Accuracy,-6,6);Evasion=FMath::Clamp(Evasion,-6,6);
 int64 Threshold=FMath::Clamp(Base,0,100)*255/100;
 if(Identified && Evasion>=Accuracy)return int32(Threshold);
 Threshold=FMath::Max<int64>(1,Threshold*N[Accuracy+6]/D[Accuracy+6]);
 Threshold=FMath::Max<int64>(1,Threshold*N[6-Evasion]/D[6-Evasion]);
 return int32(FMath::Min<int64>(255,Threshold));
}

int32 UPokeMonsterBattleLibrary::ApplyCrystalStage(int32 Value,int32 Stage)
{
 if(Value<=0)return 0;
 const int N[]={25,28,33,40,50,66,1,15,2,25,3,35,4};
 const int D[]={100,100,100,100,100,100,1,10,1,10,1,10,1};
 const int I=FMath::Clamp(Stage,-6,6)+6;
 return int32(FMath::Clamp<int64>(int64(Value)*N[I]/D[I],1,999));
}
