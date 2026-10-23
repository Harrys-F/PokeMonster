#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "UObject/StrongObjectPtr.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/GameInstance.h"
namespace CrystalMoveTests
{
using K=EPokeMonsterEffectKind;using Side=EPokeMonsterBattleSide;using Ev=EPokeMonsterBattleEventType;using Status=EPokeMonsterCreatureStatus;
struct Fixture
{
 TStrongObjectPtr<UPokeMonsterMoveData> Wait{NewObject<UPokeMonsterMoveData>()};
 FPokeMonsterCreatureInstance A,B;
 Fixture(bool Ghost=false,bool TargetGhost=false)
 {
  auto* SA=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,Ghost?TEXT("/Game/Data/Creatures/DA_Gengar.DA_Gengar"):TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
  auto* SB=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TargetGhost?TEXT("/Game/Data/Creatures/DA_Gengar.DA_Gengar"):TEXT("/Game/Data/Creatures/DA_Schiggy.DA_Schiggy"));
  A=FPokeMonsterCreatureInstance::CreateFromSpecies(SA,30);B=FPokeMonsterCreatureInstance::CreateFromSpecies(SB,30);
  Wait->InternalId=TEXT("ControlledOpponentWait");Wait->DisplayName=FText::FromString(TEXT("Kontrollierter Testgegner wartet"));Wait->Category=EPokeMonsterMoveCategory::Status;Wait->BasePower=0;Wait->MaxPP=100;
  for(auto* C:{&A,&B}){C->CurrentHP=C->CalculatedStats.MaxHP=1000;C->CalculatedStats.Attack=C->CalculatedStats.Defense=C->CalculatedStats.SpecialAttack=C->CalculatedStats.SpecialDefense=100;C->CalculatedStats.Speed=10;C->AssignMove(1,Wait.Get());}A.CalculatedStats.Speed=10000;
 }
 UPokeMonsterBattleSession* Session(int Seed=0,int Time=1)
 {
  auto* S=NewObject<UPokeMonsterBattleSession>();auto Rules=FPokeMonsterBattleEffectRules::Crystal();Rules.TimeOfDay=Time;S->ConfigureEffectRules(Rules);S->InitializeTeams({A},{B},Seed,true,true);return S;
 }
};
static bool Event(const FPokeMonsterBattleResult& R,Ev E){return R.Events.ContainsByPredicate([E](const auto& X){return X.Type==E;});}
static int DamageTo(const FPokeMonsterBattleResult& R,Side S){int D=0;for(const auto& E:R.Events)if(E.Type==Ev::Damage && E.Target==S)D+=E.Damage;return D;}
static UPokeMonsterMoveData* Move(const FString& Id){return LoadObject<UPokeMonsterMoveData>(nullptr,*(TEXT("/Game/Data/Moves/EffectsV4/DA_")+Id+TEXT(".DA_")+Id));}
static const TCHAR* Ids[]={
 TEXT("KarateChop"),
 TEXT("Bite"),
 TEXT("Disable"),
 TEXT("Acid"),
 TEXT("Submission"),
 TEXT("LowKick"),
 TEXT("Growth"),
 TEXT("RazorLeaf"),
 TEXT("SolarBeam"),
 TEXT("PoisonPowder"),
 TEXT("StunSpore"),
 TEXT("SleepPowder"),
 TEXT("PetalDance"),
 TEXT("DragonRage"),
 TEXT("FireSpin"),
 TEXT("ThunderShock"),
 TEXT("Thunderbolt"),
 TEXT("ThunderWave"),
 TEXT("Thunder"),
 TEXT("Confusion"),
 TEXT("Hypnosis"),
 TEXT("Agility"),
 TEXT("Rage"),
 TEXT("Screech"),
 TEXT("DoubleTeam"),
 TEXT("Smokescreen"),
 TEXT("ConfuseRay"),
 TEXT("LightScreen"),
 TEXT("FocusEnergy"),
 TEXT("Lick"),
 TEXT("SkullBash"),
 TEXT("DreamEater"),
 TEXT("FurySwipes"),
 TEXT("Slash"),
 TEXT("Curse"),
 TEXT("Spite"),
 TEXT("Protect"),
 TEXT("ScaryFace"),
 TEXT("Foresight"),
 TEXT("DestinyBond"),
 TEXT("MeanLook"),
 TEXT("RapidSpin"),
 TEXT("SweetScent"),
 TEXT("VitalThrow"),
 TEXT("Synthesis"),
 TEXT("Moonlight"),
 TEXT("CrossChop"),
 TEXT("RainDance"),
 TEXT("PsychUp")};
}
IMPLEMENT_COMPLEX_AUTOMATION_TEST(FPokeMonsterCrystalProductionMoves,"PokeMonster.CrystalMoves.Production",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
void FPokeMonsterCrystalProductionMoves::GetTests(TArray<FString>& Names,TArray<FString>& Commands)const
{
 for(const auto* Id:CrystalMoveTests::Ids){Names.Add(Id);Commands.Add(Id);}
}
bool FPokeMonsterCrystalProductionMoves::RunTest(const FString& Id)
{
 using namespace CrystalMoveTests;
 auto* M=Move(Id);if(!TestNotNull(TEXT("Actual production move asset exists"),M))return false;
 if(!TestTrue(TEXT("Actual production move has a complete valid effect"),M->IsConfigured()))return false;
 bool Observed=false;
 // Seed search is bounded, deterministic and exercises unmodified production probabilities.
 for(int Seed=0;Seed<256 && !Observed;++Seed)
 {
  Fixture F(Id==TEXT("Curse"),Id==TEXT("Foresight"));if(!TestTrue(TEXT("Production asset assigned by its stable identity"),F.A.AssignMove(0,M)))return false;
  if(Id==TEXT("DestinyBond")){F.A.CurrentHP=1;F.B.AssignMove(1,LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Scratch.DA_Scratch")));}
  if(Id==TEXT("DreamEater")){F.A.CurrentHP=400;F.B.Status=Status::Sleep;F.B.StatusTurns=7;}
  if(Id==TEXT("Synthesis") || Id==TEXT("Moonlight"))F.A.CurrentHP=400;
  TStrongObjectPtr<UPokeMonsterBattleSession> S(F.Session(Seed));
  if(Id==TEXT("Disable") || Id==TEXT("Spite"))S->ResolveRound(1,1);
  if(Id==TEXT("PsychUp"))
  {
   auto* Agility=Move(TEXT("Agility"));F.B.AssignMove(2,Agility);S.Reset(F.Session(Seed));S->ResolveRound(1,2);
  }
  const int BeforeA=S->GetState().SideA.CurrentHP,BeforeB=S->GetState().SideB.CurrentHP;
  const auto R=S->ResolveRound(0,1);if(!TestTrue(TEXT("Real battle resolver accepts the production move"),R.bSucceeded))return false;
  const auto& T=S->GetState();const int Damage=DamageTo(R,Side::B);
  if(Id==TEXT("KarateChop") || Id==TEXT("RazorLeaf") || Id==TEXT("Slash") || Id==TEXT("CrossChop"))Observed=Damage>0 && R.Events.ContainsByPredicate([](const auto& E){return E.Information.ToString().Contains(TEXT("Volltreffer"));});
  else if(Id==TEXT("Bite") || Id==TEXT("LowKick"))Observed=Damage>0 && Event(R,Ev::Flinched) && T.SideB.GetMoveSlots()[1].GetCurrentPP()==100;
  else if(Id==TEXT("Disable"))Observed=T.EffectsB.DisableTurns>0 && T.EffectsB.DisabledSlot==1 && !S->CanSelectMove(Side::B,1) && T.SideB.GetMoveSlots()[1].GetCurrentPP()==99;
  else if(Id==TEXT("Spite"))Observed=T.SideB.GetMoveSlots()[1].GetCurrentPP()<=96 && T.SideB.GetMoveSlots()[1].GetCurrentPP()>=93;
  else if(Id==TEXT("Acid"))Observed=Damage>0 && T.DefenseStageB==-1;
  else if(Id==TEXT("Submission"))Observed=Damage>0 && BeforeA-T.SideA.CurrentHP==FMath::Max(1,Damage/4);
  else if(Id==TEXT("Growth"))Observed=T.EffectsA.SpecialAttack==1 && T.AttackStageA==0;
  else if(Id==TEXT("SolarBeam") || Id==TEXT("SkullBash"))
  {
   const bool Charge=Damage==0 && S->ForcedMoveSlot(Side::A)==0 && T.SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1 && (Id!=TEXT("SkullBash") || T.DefenseStageA==1);
   const auto Release=S->ResolveRound(1,1);Observed=Charge && Release.bSucceeded && DamageTo(Release,Side::B)>0 && S->ForcedMoveSlot(Side::A)==INDEX_NONE && S->GetState().SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1;
  }
  else if(Id==TEXT("PoisonPowder"))Observed=T.SideB.Status==Status::Poison && T.SideB.CurrentHP<BeforeB;
  else if(Id==TEXT("StunSpore") || Id==TEXT("ThunderWave") || Id==TEXT("ThunderShock") || Id==TEXT("Thunderbolt") || Id==TEXT("Thunder") || Id==TEXT("Lick"))Observed=T.SideB.Status==Status::Paralysis;
  else if(Id==TEXT("SleepPowder") || Id==TEXT("Hypnosis"))Observed=T.SideB.Status==Status::Sleep && T.SideB.StatusTurns>0 && T.SideB.GetMoveSlots()[1].GetCurrentPP()==100;
  else if(Id==TEXT("PetalDance"))
  {
   bool Locked=Damage>0 && S->ForcedMoveSlot(Side::A)==0;int Turns=1;
   while(S->ForcedMoveSlot(Side::A)!=INDEX_NONE && Turns<4){++Turns;S->ResolveRound(1,1);}
   Observed=Locked && Turns>=2 && Turns<=3 && S->GetState().EffectsA.ConfusionTurns>=2 && S->GetState().SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1;
  }
  else if(Id==TEXT("DragonRage"))Observed=Damage==40;
  else if(Id==TEXT("FireSpin"))Observed=Damage>0 && T.EffectsB.TrapTurns>0 && !S->CanLeave(Side::B) && Event(R,Ev::StatusDamage);
  else if(Id==TEXT("Confusion") || Id==TEXT("ConfuseRay"))Observed=Event(R,Ev::Confused);
  else if(Id==TEXT("Agility"))Observed=T.SpeedStageA==2;
  else if(Id==TEXT("Rage"))
  {
   auto* Scratch=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Scratch.DA_Scratch"));F.B.AssignMove(0,Scratch);S.Reset(F.Session(Seed));auto First=S->ResolveRound(0,0);auto Second=S->ResolveRound(0,0);
   Observed=DamageTo(Second,Side::B)>DamageTo(First,Side::B) && S->GetState().EffectsA.RageCounter>=2 && S->GetState().AttackStageA==0;
  }
  else if(Id==TEXT("Screech"))Observed=T.DefenseStageB==-2;
  else if(Id==TEXT("DoubleTeam"))Observed=T.EffectsA.Evasion==1;
  else if(Id==TEXT("Smokescreen"))Observed=T.EffectsB.Accuracy==-1;
  else if(Id==TEXT("LightScreen"))Observed=T.ScreenTurnsA==4;
  else if(Id==TEXT("FocusEnergy"))Observed=T.EffectsA.FocusStage==1;
  else if(Id==TEXT("DreamEater"))Observed=Damage>0 && T.SideA.CurrentHP-BeforeA==FMath::Max(1,Damage/2);
  else if(Id==TEXT("FurySwipes")){int Hits=0;for(const auto& E:R.Events)Hits+=E.Type==Ev::Damage && E.Target==Side::B;Observed=Hits>=2 && Hits<=5 && Damage>0 && T.SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1;}
  else if(Id==TEXT("Curse"))Observed=T.EffectsB.bCursed && T.SideA.CurrentHP==500 && T.SideB.CurrentHP==750;
  else if(Id==TEXT("Protect"))Observed=T.EffectsA.bProtected && Event(R,Ev::Protected);
  else if(Id==TEXT("ScaryFace"))Observed=T.SpeedStageB==-2;
  else if(Id==TEXT("Foresight"))
  {
   auto* Scratch=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Scratch.DA_Scratch"));Observed=T.EffectsB.bIdentified && UPokeMonsterBattleLibrary::CalculateCrystalDamage(T.SideA,T.SideB,Scratch,0,0,0,0,false,255,false,false,true).Damage>0;
  }
  else if(Id==TEXT("DestinyBond"))Observed=T.SideA.CurrentHP==0 && T.SideB.CurrentHP==0 && Event(R,Ev::KnockedOut);
  else if(Id==TEXT("MeanLook"))Observed=T.EffectsB.SwitchBlockSource==T.SideA.InstanceId && !S->CanLeave(Side::B);
  else if(Id==TEXT("RapidSpin"))
  {
   auto* SeedMove=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_LeechSeed.DA_LeechSeed"));F.B.AssignMove(2,SeedMove);S.Reset(F.Session(Seed));S->ResolveRound(1,2);const bool Seeded=S->GetState().bSeededA;auto Spin=S->ResolveRound(0,1);Observed=Seeded && Spin.bSucceeded && DamageTo(Spin,Side::B)>0 && !S->GetState().bSeededA;
  }
  else if(Id==TEXT("SweetScent"))Observed=T.EffectsB.Evasion==-1;
  else if(Id==TEXT("VitalThrow")){TArray<Side> Order;for(const auto& E:R.Events)if(E.Type==Ev::MoveExecuted)Order.Add(E.Source);Observed=Damage>0 && Order.Num()==2 && Order[0]==Side::B;}
  else if(Id==TEXT("Synthesis"))Observed=T.SideA.CurrentHP==900;
  else if(Id==TEXT("Moonlight"))Observed=T.SideA.CurrentHP==650;
  else if(Id==TEXT("RainDance"))Observed=T.WeatherTurns==4;
  else if(Id==TEXT("PsychUp"))Observed=T.SpeedStageA==2 && T.SpeedStageB==2;
  if(Observed){AddInfo(FString::Printf(TEXT("Actual production effect %s observed with deterministic seed %d"),*Id,Seed));TestTrue(TEXT("Accepted attempt consumes exactly one initial AP"),T.SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1);}
 }
 return TestTrue(TEXT("Observable gameplay effect verified, not just configuration fields"),Observed);
}
#define CRYSTAL_EDGE(Class,Name) IMPLEMENT_SIMPLE_AUTOMATION_TEST(Class,"PokeMonster.CrystalMoves.Edges." Name,EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter) bool Class::RunTest(const FString&)
CRYSTAL_EDGE(FCrystalDamageRules,"DamageTypeSTABCriticalAndWeather")
{
 using namespace CrystalMoveTests;Fixture F;auto* Ember=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Ember.DA_Ember"));
 auto Hit=[&](bool Crit,int AS,int DS,int Random,bool Rain,bool Screen){return UPokeMonsterBattleLibrary::CalculateCrystalDamage(F.A,F.B,Ember,0,0,AS,DS,Crit,Random,Rain,Screen,false).Damage;};
 TestEqual(TEXT("Known base with Fire STAB and Water resistance"),Hit(false,0,0,255,false,false),9);
 TestEqual(TEXT("Critical uses Gen2 multiplier before additive constant"),Hit(true,0,0,255,false,false),18);
 TestEqual(TEXT("Critical ignores adverse equal-or-worse stages and screen"),Hit(true,-6,6,255,false,true),18);
 TestTrue(TEXT("Beneficial stages remain on critical"),Hit(true,2,0,255,false,false)>18);
 TestTrue(TEXT("Rain reduces Fire damage"),Hit(false,0,0,255,true,false)<9);
 TestTrue(TEXT("Light Screen reduces special damage"),Hit(false,0,0,255,false,true)<9);
 TestTrue(TEXT("Minimum damage random factor reduces a landed hit"),Hit(false,0,0,217,false,false)<9);
 TestEqual(TEXT("Zero accuracy remains a guaranteed failure"),UPokeMonsterBattleLibrary::CrystalAccuracy(0,6,-6,false),0);
 TestEqual(TEXT("Crystal stat table keeps rounded 66 percent, not later rational 2/3"),UPokeMonsterBattleLibrary::ApplyCrystalStage(200,-1),132);
 TestEqual(TEXT("Crystal stat maximum"),UPokeMonsterBattleLibrary::ApplyCrystalStage(999,6),999);
 TestEqual(TEXT("Crystal byte accuracy, -1"),UPokeMonsterBattleLibrary::CrystalAccuracy(100,-1,0,false),191);
 TestEqual(TEXT("Crystal stages multiply separately, not a later-gen net stage"),UPokeMonsterBattleLibrary::CrystalAccuracy(90,1,1,false),228);
 TestEqual(TEXT("Foresight cancels adverse accuracy/evasion comparison"),UPokeMonsterBattleLibrary::CrystalAccuracy(90,-2,2,true),229);
 return true;
}
CRYSTAL_EDGE(FCrystalRestraints,"BindingSwitchFleeReleaseAndRapidSpin")
{
 using namespace CrystalMoveTests;Fixture F;F.A.AssignMove(0,Move(TEXT("MeanLook")));auto A2=F.A;A2.InstanceId=FGuid::NewGuid();auto B2=F.B;B2.InstanceId=FGuid::NewGuid();
 TStrongObjectPtr<UPokeMonsterBattleSession> S(NewObject<UPokeMonsterBattleSession>());S->ConfigureEffectRules(FPokeMonsterBattleEffectRules::Crystal());S->InitializeTeams({F.A,A2},{F.B,B2},1,true,true);S->ResolveRound(0,1);
 FPokeMonsterBattleChoice Switch,Wait;Switch.Type=EPokeMonsterBattleChoiceType::Switch;Switch.Index=1;Wait.Index=1;
 TestFalse(TEXT("Trapped voluntary switch rejected atomically"),S->ResolveTurn(Wait,Switch).bSucceeded);TestEqual(TEXT("Rejected turn does not advance"),S->GetState().RoundNumber,1);
 TestTrue(TEXT("Source can switch out"),S->ResolveTurn(Switch,Wait).bSucceeded);TestTrue(TEXT("Restraint released when source leaves"),S->CanLeave(Side::B));
 F.A.AssignMove(0,Move(TEXT("FireSpin")));F.B.AssignMove(0,Move(TEXT("RapidSpin")));
 bool Saw=false;for(int Seed=0;Seed<30&&!Saw;++Seed){S.Reset(F.Session(Seed));auto R=S->ResolveRound(0,0);Saw=Event(R,Ev::StatusRecovered)&&DamageTo(R,Side::A)>0;if(Saw){TestEqual(TEXT("Rapid Spin releases partial trap"),S->GetState().EffectsB.TrapTurns,0);TestTrue(TEXT("Released target may leave"),S->CanLeave(Side::B));}}
 TestTrue(TEXT("Actual trap and Rapid Spin sequence exercised"),Saw);return true;
}
CRYSTAL_EDGE(FCrystalCurse,"CurseBranchesCapsAndSwitchReset")
{
 using namespace CrystalMoveTests;Fixture F;F.A.AssignMove(0,Move(TEXT("Curse")));TStrongObjectPtr<UPokeMonsterBattleSession>S(F.Session());
 for(int I=0;I<6;++I)TestTrue(TEXT("Non-Ghost Curse resolves"),S->ResolveRound(0,1).bSucceeded);
 TestEqual(TEXT("Non-Ghost Attack cap"),S->GetState().AttackStageA,6);TestEqual(TEXT("Non-Ghost Defense cap"),S->GetState().DefenseStageA,6);TestEqual(TEXT("Non-Ghost Speed floor"),S->GetState().SpeedStageA,-6);
 TestTrue(TEXT("Both capped makes Curse fail"),Event(S->ResolveRound(0,1),Ev::EffectFailed));TestFalse(TEXT("No Ghost curse applied by non-Ghost"),S->GetState().EffectsB.bCursed);
 Fixture G(true);G.A.AssignMove(0,Move(TEXT("Curse")));auto A2=G.A;A2.InstanceId=FGuid::NewGuid();auto B2=G.B;B2.InstanceId=FGuid::NewGuid();S.Reset(NewObject<UPokeMonsterBattleSession>());S->ConfigureEffectRules(FPokeMonsterBattleEffectRules::Crystal());S->InitializeTeams({G.A,A2},{G.B,B2},0);
 S->ResolveRound(0,1);FPokeMonsterBattleChoice Switch,Wait;Switch.Type=EPokeMonsterBattleChoiceType::Switch;Switch.Index=1;Wait.Index=1;
 S->ResolveTurn(Switch,Wait);TestTrue(TEXT("Ghost source switching does not cure victim Curse"),S->GetState().EffectsB.bCursed);
 S->ResolveTurn(Wait,Switch);TestFalse(TEXT("Victim switching removes Curse"),S->GetState().EffectsB.bCursed);return true;
}
CRYSTAL_EDGE(FCrystalWeather,"RainDurationThunderAndTimeSensitiveHealing")
{
 using namespace CrystalMoveTests;
 for(int Time:{1,2})for(bool Rain:{false,true})
 {
  Fixture F;F.A.AssignMove(0,Move(TEXT("Moonlight")));F.B.AssignMove(2,Move(TEXT("RainDance")));F.A.CurrentHP=100;
  TStrongObjectPtr<UPokeMonsterBattleSession>S(F.Session(1,Time));if(Rain)S->ResolveRound(1,2);
  TestTrue(TEXT("Moonlight actual turn resolves"),S->ResolveRound(0,1).bSucceeded);
  const int Amount=(Time==2?500:250)/(Rain?2:1);TestEqual(TEXT("Gen2 time and rain healing fraction"),S->GetState().SideA.CurrentHP,100+Amount);
 }
 Fixture F;F.A.AssignMove(0,Move(TEXT("RainDance")));F.A.AssignMove(2,Move(TEXT("Thunder")));TStrongObjectPtr<UPokeMonsterBattleSession>S(F.Session(2));S->ResolveRound(0,1);TestEqual(TEXT("Rain counts casting round"),S->GetState().WeatherTurns,4);
 for(int I=0;I<4;++I){auto R=S->ResolveRound(2,1);TestFalse(TEXT("Thunder cannot miss during rain"),R.Events.ContainsByPredicate([](const auto& E){return E.Type==Ev::Missed&&E.Source==Side::A;}));}
 TestEqual(TEXT("Rain expires after five total rounds"),S->GetState().WeatherTurns,0);return true;
}
CRYSTAL_EDGE(FCrystalFreeze,"FrozenTurnEndThawAndFireCure")
{
 using namespace CrystalMoveTests;Fixture F;F.A.Status=Status::Freeze;auto Rules=FPokeMonsterBattleEffectRules::Crystal();Rules.FreezeThawPercent=100;
 TStrongObjectPtr<UPokeMonsterBattleSession>S(NewObject<UPokeMonsterBattleSession>());S->ConfigureEffectRules(Rules);S->InitializeTeams({F.A},{F.B},1);auto R=S->ResolveRound(1,1);
 TestTrue(TEXT("Freeze prevents current action"),Event(R,Ev::StatusPrevented));TestEqual(TEXT("No AP before end-turn thaw"),S->GetState().SideA.GetMoveSlots()[1].GetCurrentPP(),100);TestEqual(TEXT("Thaws at round end rather than before acting"),S->GetState().SideA.Status,Status::None);
 TestTrue(TEXT("Next turn can act"),S->ResolveRound(1,1).bSucceeded);TestEqual(TEXT("Next turn AP consumed"),S->GetState().SideA.GetMoveSlots()[1].GetCurrentPP(),99);
 F.A.Status=Status::None;F.B.Status=Status::Freeze;F.A.AssignMove(0,LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Ember.DA_Ember")));S.Reset(F.Session(0));S->ResolveRound(0,1);TestTrue(TEXT("Landed Fire attack cures frozen target"),S->GetState().SideB.Status!=Status::Freeze);return true;
}
CRYSTAL_EDGE(FCrystalFainting,"MultihitStopsDrainAndRecoilKO")
{
 using namespace CrystalMoveTests;Fixture F;F.B.CurrentHP=1;F.A.AssignMove(0,Move(TEXT("FurySwipes")));bool Seen=false;
 for(int Seed=0;Seed<30&&!Seen;++Seed){TStrongObjectPtr<UPokeMonsterBattleSession>S(F.Session(Seed));auto R=S->ResolveRound(0,1);if(DamageTo(R,Side::B)>0){int Hits=0;for(const auto& E:R.Events)Hits+=E.Type==Ev::Damage&&E.Target==Side::B;TestEqual(TEXT("Multihit stops immediately on faint"),Hits,1);TestEqual(TEXT("No overkill HP removal"),DamageTo(R,Side::B),1);Seen=true;}}
 TestTrue(TEXT("Production multihit KO exercised"),Seen);
 F.A.AssignMove(0,Move(TEXT("Submission")));F.A.CurrentHP=1;F.B.CurrentHP=1000;Seen=false;
 for(int Seed=0;Seed<30&&!Seen;++Seed){TStrongObjectPtr<UPokeMonsterBattleSession>S(F.Session(Seed));auto R=S->ResolveRound(0,1);if(DamageTo(R,Side::B)>0){TestEqual(TEXT("Recoil can faint attacker"),S->GetState().SideA.CurrentHP,0);TestEqual(TEXT("Recoil KO ends one-member battle"),S->GetState().Phase,EPokeMonsterBattlePhase::Finished);Seen=true;}}
 TestTrue(TEXT("Actual recoil KO exercised"),Seen);return true;
}
CRYSTAL_EDGE(FCrystalBindings,"AllTenLearnlistsUseValidStableAssets")
{
 using namespace CrystalMoveTests;const TCHAR* Names[]={TEXT("Zunderlauf"),TEXT("Schiggy"),TEXT("Bisasam"),TEXT("Pikachu"),TEXT("Myrapla"),TEXT("Enton"),TEXT("Machomei"),TEXT("Nebulak"),TEXT("Gengar"),TEXT("Glurak")};int Entries=0;TSet<FName> Moves;
 for(const auto* Name:Names)
 {
  auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),Name,Name));if(!TestNotNull(TEXT("Existing species remains available"),Species))return false;
  for(const auto& E:Species->LevelUpMoves){++Entries;auto* M=E.Move.LoadSynchronous();if(!TestNotNull(TEXT("No unavailable placeholder in the ten learnlists"),M))return false;TestTrue(TEXT("Bound move effect actually configured"),M->IsConfigured());TestTrue(TEXT("No stale unavailable label"),E.UnavailableMoveName.IsEmpty()&&E.UnavailableReason.IsEmpty());Moves.Add(M->InternalId);}
 }
 TestEqual(TEXT("All 102 original learnlist entries retained"),Entries,102);TestEqual(TEXT("All 68 canonical moves bound"),Moves.Num(),68);return true;
}


CRYSTAL_EDGE(FCrystalSpiteSave,"SpitePPRepertoireSaveAndHealing")
{
 using namespace CrystalMoveTests;
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,30),B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,30);
 auto* Growl=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Growl.DA_Growl"));A.AssignMove(0,Growl);B.AssignMove(0,Move(TEXT("Spite")));A.CalculatedStats.Speed=1000;B.CalculatedStats.Speed=1;
 TStrongObjectPtr<UPokeMonsterBattleSession>Session(NewObject<UPokeMonsterBattleSession>());Session->ConfigureEffectRules(FPokeMonsterBattleEffectRules::Crystal());Session->InitializeTeams({A},{B},0);TestTrue(TEXT("Actual Spite turn"),Session->ResolveRound(0,0).bSucceeded);
 const auto C=Session->GetState().SideA;const int PP=C.GetMoveSlots()[0].GetCurrentPP();TestTrue(TEXT("Spite removes 2-5 AP beyond initial use"),PP>=Growl->MaxPP-6&&PP<=Growl->MaxPP-3);
 const auto* Remembered=C.GetLearnedMoves().FindByPredicate([Growl](const auto& S){return S.GetMove().LoadSynchronous()==Growl;});TestTrue(TEXT("Personal repertoire remembers reduced PP"),Remembered&&Remembered->GetCurrentPP()==PP);
 TStrongObjectPtr<UGameInstance>GI(NewObject<UGameInstance>());auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());TestTrue(TEXT("Existing persistence accepts battle result"),E->RestorePersistentState({C},{},{}));auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());if(!TestNotNull(TEXT("Save snapshot"),Save))return false;
 TArray<uint8>Bytes;TestTrue(TEXT("Real Unreal save serialization"),UGameplayStatics::SaveGameToMemory(Save,Bytes));auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));TestTrue(TEXT("Restore existing schema"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I));auto Out=E->GetPlayerParty()[0];TestEqual(TEXT("Same individual ID"),Out.InstanceId,A.InstanceId);TestEqual(TEXT("Reduced active AP persisted"),Out.GetMoveSlots()[0].GetCurrentPP(),PP);TestEqual(TEXT("Reduced repertoire AP persisted"),Out.GetLearnedMoves()[0].GetCurrentPP(),PP);
 TestTrue(TEXT("Existing healing remains legitimate AP restoration"),Out.RestoreFully());TestEqual(TEXT("Healing restores full AP"),Out.GetMoveSlots()[0].GetCurrentPP(),Growl->MaxPP);return true;
}
CRYSTAL_EDGE(FCrystalSunContext,"SunSolarBeamAndWeatherHealContext")
{
 using namespace CrystalMoveTests;
 Fixture F;F.A.AssignMove(0,Move(TEXT("SolarBeam")));auto Rules=FPokeMonsterBattleEffectRules::Crystal();Rules.InitialWeather=EPokeMonsterBattleWeather::Sun;TStrongObjectPtr<UPokeMonsterBattleSession>S(NewObject<UPokeMonsterBattleSession>());S->ConfigureEffectRules(Rules);S->InitializeTeams({F.A},{F.B},0);auto R=S->ResolveRound(0,1);TestTrue(TEXT("Solar Beam fires immediately in sunlight"),DamageTo(R,Side::B)>0);TestEqual(TEXT("No solar charging lock in sun"),S->ForcedMoveSlot(Side::A),INDEX_NONE);
 for(auto Weather:{EPokeMonsterBattleWeather::Sun,EPokeMonsterBattleWeather::Sand})
 {
  F.A.AssignMove(0,Move(TEXT("Synthesis")));F.A.CurrentHP=100;Rules.InitialWeather=Weather;S.Reset(NewObject<UPokeMonsterBattleSession>());S->ConfigureEffectRules(Rules);S->InitializeTeams({F.A},{F.B},0);S->ResolveRound(0,1);
  TestEqual(TEXT("Gen2 sunny full heal or sandstorm quarter heal minus sand residual"),S->GetState().SideA.CurrentHP,Weather==EPokeMonsterBattleWeather::Sun?1000:225);
 }
 return true;
}

CRYSTAL_EDGE(FCrystalProtectExceptions,"ProtectMeanLookAndChargeInputGuards")
{
 using namespace CrystalMoveTests;Fixture F;F.A.AssignMove(0,Move(TEXT("Protect")));F.B.AssignMove(0,Move(TEXT("MeanLook")));TStrongObjectPtr<UPokeMonsterBattleSession>S(F.Session(0));auto R=S->ResolveRound(0,0);
 TestTrue(TEXT("Protect first succeeds"),Event(R,Ev::Protected));TestFalse(TEXT("Crystal Mean Look bypasses Protect"),S->CanLeave(Side::A));
 F.A.AssignMove(0,Move(TEXT("SolarBeam")));F.B.AssignMove(0,F.Wait.Get());S.Reset(F.Session(0));S->ResolveRound(0,0);TestEqual(TEXT("Charging slot locked"),S->ForcedMoveSlot(Side::A),0);
 FPokeMonsterBattleChoice Item,Wait;Item.Type=EPokeMonsterBattleChoiceType::Item;Item.Index=0;Wait.Index=1;const auto Before=S->GetState().RoundNumber;
 TestFalse(TEXT("Locked move rejects foreign item action before dereferencing an item"),S->ResolveTurn(Item,Wait).bSucceeded);TestEqual(TEXT("Rejected action is atomic"),S->GetState().RoundNumber,Before);TestTrue(TEXT("Normal release still resolves"),S->ResolveRound(1,1).bSucceeded);TestEqual(TEXT("Charging consumes AP only once"),S->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(),Move(TEXT("SolarBeam"))->MaxPP-1);return true;
}

CRYSTAL_EDGE(FCrystalLearningIdentity,"LearningDoesNotRetargetOldSpiteSlot")
{
 using namespace CrystalMoveTests;
 auto* Water=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Schiggy.DA_Schiggy"));auto* Fire=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));auto* Growl=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Growl.DA_Growl"));
 bool Exercised=false;
 for(int Seed=0;Seed<20&&!Exercised;++Seed)
 {
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(Water,12);A.AssignSpeciesMoves();A.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(Water->GetGrowthRate(),13)-1;A.CalculatedStats.Speed=200;
  auto B=FPokeMonsterCreatureInstance::CreateFromSpecies(Fire,10);B.CurrentHP=1;B.AssignMove(0,Growl);auto B2=FPokeMonsterCreatureInstance::CreateFromSpecies(Fire,10);B2.AssignMove(0,Move(TEXT("Spite")));B2.CalculatedStats.Speed=300;
  TStrongObjectPtr<UPokeMonsterBattleSession>S(NewObject<UPokeMonsterBattleSession>());S->ConfigureEffectRules(FPokeMonsterBattleEffectRules::Crystal());S->InitializeTeams({A},{B,B2},Seed);auto R=S->ResolveRound(0,0);if(!Event(R,Ev::KnockedOut))continue;
  TestEqual(TEXT("Actual KO queues Water Gun"),S->GetState().SideA.PendingMoves.Num(),1);TestEqual(TEXT("Previous used slot recorded"),S->GetState().EffectsA.LastMoveSlot,0);
  TestTrue(TEXT("Actual learning replaces the last-used slot"),S->ResolveMoveLearning(0,0));TestEqual(TEXT("New attack is not considered the old used attack"),S->GetState().EffectsA.LastMoveSlot,INDEX_NONE);
  TestTrue(TEXT("Enemy force switch resumes battle"),S->ForceSwitch(Side::B,1).bSucceeded);R=S->ResolveRound(0,0);TestTrue(TEXT("Spite correctly fails before newly learned move has ever acted"),R.Events.ContainsByPredicate([](const auto& E){return E.Type==Ev::EffectFailed && E.Source==Side::B;}));TestEqual(TEXT("New Water Gun loses only its real use AP"),S->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(),24);Exercised=true;
 }
 return TestTrue(TEXT("Actual KO/learn/switch/Spite sequence exercised"),Exercised);
}

CRYSTAL_EDGE(FCrystalSleepFlinch,"SleepCounterBeforeFlinch")
{
 using namespace CrystalMoveTests;Fixture F;F.A.AssignMove(0,Move(TEXT("Bite")));F.B.Status=Status::Sleep;F.B.StatusTurns=4;bool Seen=false;
 for(int Seed=0;Seed<100&&!Seen;++Seed)
 {
  TStrongObjectPtr<UPokeMonsterBattleSession>S(F.Session(Seed));S->ResolveRound(0,1);
  if(S->GetState().EffectsB.bFlinched){TestEqual(TEXT("Flinch does not freeze a sleeping target's timer"),S->GetState().SideB.StatusTurns,3);TestEqual(TEXT("Sleeping target still spends no AP"),S->GetState().SideB.GetMoveSlots()[1].GetCurrentPP(),100);Seen=true;}
 }
 return TestTrue(TEXT("Actual sleeping Bite-flinch combination exercised"),Seen);
}
CRYSTAL_EDGE(FCrystalConfusionParalysis,"ConfusionCounterBeforeFullParalysis")
{
 using namespace CrystalMoveTests;Fixture F;F.A.Status=Status::Paralysis;F.B.AssignMove(0,Move(TEXT("ConfuseRay")));auto Rules=FPokeMonsterBattleEffectRules::Crystal();Rules.ParalysisSkipPercent=100;
 TStrongObjectPtr<UPokeMonsterBattleSession>S(NewObject<UPokeMonsterBattleSession>());S->ConfigureEffectRules(Rules);S->InitializeTeams({F.A},{F.B},0);S->ResolveRound(1,0);const int Before=S->GetState().EffectsA.ConfusionTurns;TestTrue(TEXT("Confuse Ray applies on a paralyzed target"),Before>=2);
 S->ResolveRound(1,1);TestEqual(TEXT("Confusion still advances before guaranteed full paralysis"),S->GetState().EffectsA.ConfusionTurns,Before-1);TestEqual(TEXT("Neither prevention nor confusion spends action AP"),S->GetState().SideA.GetMoveSlots()[1].GetCurrentPP(),100);return true;
}
#endif
