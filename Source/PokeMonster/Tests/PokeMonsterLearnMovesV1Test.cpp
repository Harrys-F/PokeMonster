#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"
namespace LearnMovesV1Tests
{
using Kind=EPokeMonsterEffectKind;using Side=EPokeMonsterBattleSide;using Event=EPokeMonsterBattleEventType;
UPokeMonsterMoveData* Move(const FString& Id){return LoadObject<UPokeMonsterMoveData>(nullptr,*(TEXT("/Game/Data/Moves/LearnMovesV1/DA_")+Id));}
UPokeMonsterCreatureSpeciesData* Species(const FString& Id){return LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*(TEXT("/Game/Data/Creatures/DA_")+Id));}
int Damage(const FPokeMonsterBattleResult& R,Side Target){int N=0;for(const auto& E:R.Events)if(E.Type==Event::Damage&&E.Target==Target)N+=E.Damage;return N;}
bool Has(const FPokeMonsterBattleResult& R,Event Type){return R.Events.ContainsByPredicate([Type](const auto& E){return E.Type==Type;});}
struct Fixture
{
 TStrongObjectPtr<UPokeMonsterMoveData> Wait{NewObject<UPokeMonsterMoveData>()};FPokeMonsterCreatureInstance A,B;
 Fixture()
 {
  A=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(TEXT("Zunderlauf")),30);B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(TEXT("Schiggy")),30);
  Wait->InternalId=TEXT("ControlledLearnMoveWait");Wait->DisplayName=FText::FromString(TEXT("Kontrolliertes Warten"));Wait->Category=EPokeMonsterMoveCategory::Status;Wait->BasePower=0;Wait->MaxPP=100;
  for(auto* C:{&A,&B}){C->CurrentHP=C->CalculatedStats.MaxHP=1000;C->CalculatedStats.Attack=C->CalculatedStats.Defense=C->CalculatedStats.SpecialAttack=C->CalculatedStats.SpecialDefense=100;C->CalculatedStats.Speed=10;C->AssignMove(1,Wait.Get());}A.CalculatedStats.Speed=10000;
 }
 UPokeMonsterBattleSession* Session(int Seed=0,bool Wild=true,const TArray<FPokeMonsterCreatureInstance>& Reserves={})
 {
  auto* S=NewObject<UPokeMonsterBattleSession>();S->ConfigureEffectRules(FPokeMonsterBattleEffectRules::Crystal());TArray<FPokeMonsterCreatureInstance> Team={B};Team.Append(Reserves);S->InitializeTeams({A},Team,Seed,Wild,Wild,!Wild);return S;
 }
};
const TCHAR* Ids[]={TEXT("Twineedle"),TEXT("Pursuit"),TEXT("PinMissile"),TEXT("Thrash"),TEXT("Twister"),TEXT("HyperBeam"),TEXT("MirrorMove"),TEXT("DrillPeck"),TEXT("Splash"),TEXT("Flail"),TEXT("Supersonic"),TEXT("Whirlwind"),TEXT("Gust"),TEXT("Psybeam"),TEXT("Safeguard")};
}
IMPLEMENT_COMPLEX_AUTOMATION_TEST(FLearnMoveProduction,"PokeMonster.LearnMovesV1.Production",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
void FLearnMoveProduction::GetTests(TArray<FString>& N,TArray<FString>& C)const{for(auto* Id:LearnMovesV1Tests::Ids){N.Add(Id);C.Add(Id);}}
bool FLearnMoveProduction::RunTest(const FString& Id)
{
 using namespace LearnMovesV1Tests;auto* M=Move(Id);if(!TestNotNull(TEXT("Real move asset"),M)||!TestTrue(TEXT("Configured shared production effects"),M->IsConfigured()))return false;
 bool Seen=false;
 for(int Seed=0;Seed<256&&!Seen;++Seed)
 {
  Fixture F;F.A.AssignMove(0,M);TStrongObjectPtr<UPokeMonsterBattleSession> S(F.Session(Seed));
  if(Id==TEXT("MirrorMove")){F.B.AssignMove(0,Move(TEXT("Gust")));S.Reset(F.Session(Seed));S->ResolveRound(1,0);}
  const int Before=S->GetState().SideB.CurrentHP;auto R=S->ResolveRound(0,1);if(!TestTrue(TEXT("Real resolver accepts selected asset"),R.bSucceeded))return false;
  const auto& T=S->GetState();const int D=Damage(R,Side::B);
  if(Id==TEXT("Twineedle"))Seen=D>0&&Has(R,Event::HitCount)&&T.SideB.Status==EPokeMonsterCreatureStatus::Poison;
  else if(Id==TEXT("PinMissile"))Seen=D>0&&Has(R,Event::HitCount);
  else if(Id==TEXT("Thrash")){int N=1;while(S->ForcedMoveSlot(Side::A)!=INDEX_NONE&&N<4){++N;S->ResolveRound(1,1);}Seen=D>0&&N>=2&&N<=3&&S->GetState().EffectsA.ConfusionTurns>=2&&S->GetState().SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1;}
  else if(Id==TEXT("Twister"))Seen=D>0&&Has(R,Event::Flinched);
  else if(Id==TEXT("Supersonic")||Id==TEXT("Psybeam"))Seen=Has(R,Event::Confused)&&T.EffectsB.ConfusionTurns>=1;
  else if(Id==TEXT("HyperBeam")){auto Pause=S->ResolveRound(1,1);Seen=D>0&&Pause.bSucceeded&&Damage(Pause,Side::B)==0&&S->ForcedMoveSlot(Side::A)==INDEX_NONE&&S->GetState().SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1;}
  else if(Id==TEXT("Whirlwind"))Seen=T.Phase==EPokeMonsterBattlePhase::Finished&&T.EndReason==EPokeMonsterBattleEndReason::ForcedOut&&T.Winner==Side::None;
  else if(Id==TEXT("Safeguard"))Seen=T.SafeguardTurnsA==4;
  else if(Id==TEXT("Splash"))Seen=Has(R,Event::EffectFailed)&&Before==T.SideB.CurrentHP;
  else Seen=D>0;
  if(Id!=TEXT("Thrash")&&Id!=TEXT("HyperBeam"))TestEqual(TEXT("Only selected personal PP consumed once"),T.SideA.GetMoveSlots()[0].GetCurrentPP(),M->MaxPP-1);
 }
 return TestTrue(TEXT("Move's actual gameplay effect observed through shared battle resolution"),Seen);
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FLearnMoveEdges,"PokeMonster.LearnMovesV1.SharedMechanismEdges",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FLearnMoveEdges::RunTest(const FString&)
{
 using namespace LearnMovesV1Tests;
 // Pursuit hits the outgoing individual, exactly twice the same seeded normal hit.
 Fixture F;F.A.AssignMove(0,Move(TEXT("Pursuit")));auto Reserve=F.B;Reserve.InstanceId=FGuid::NewGuid();TStrongObjectPtr<UPokeMonsterBattleSession> Normal(F.Session(7)),Intercept(F.Session(7,true,{Reserve}));
 auto Baseline=Normal->ResolveRound(0,1);FPokeMonsterBattleChoice Attack,Switch;Attack.Index=0;Switch.Type=EPokeMonsterBattleChoiceType::Switch;Switch.Index=1;
 auto R=Intercept->ResolveTurn(Attack,Switch);TestTrue(TEXT("Pursuit switch accepted"),R.bSucceeded);TestEqual(TEXT("Pursuit doubles outgoing damage"),1000-Intercept->GetState().TeamB[0].CurrentHP,2*Damage(Baseline,Side::B));TestEqual(TEXT("Incoming reserve unharmed"),Intercept->GetState().SideB.CurrentHP,1000);
 F.B.CurrentHP=1;Intercept.Reset(F.Session(7,true,{Reserve}));R=Intercept->ResolveTurn(Attack,Switch);TestEqual(TEXT("Intercepted KO still brings selected reserve"),Intercept->GetState().ActiveIndexB,1);TestEqual(TEXT("Outgoing KO stays recorded"),Intercept->GetState().TeamB[0].CurrentHP,0);
 // Hyper Beam final PP still permits a recharge turn, before status processing.
 Fixture H;auto* Beam=Move(TEXT("HyperBeam"));H.A.AssignMove(0,Beam);H.A.ConsumeMovePP(0,Beam->MaxPP-1);TStrongObjectPtr<UPokeMonsterBattleSession> HS(H.Session(0));HS->ResolveRound(0,1);TestEqual(TEXT("Last PP consumed"),HS->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(),0);TestFalse(TEXT("No switching during recharge"),HS->CanLeave(Side::A));R=HS->ResolveRound(1,1);TestTrue(TEXT("Recharge allowed at zero PP"),R.bSucceeded);TestEqual(TEXT("Recharge causes no second damage"),Damage(R,Side::B),0);TestEqual(TEXT("Recharge unlocks"),HS->ForcedMoveSlot(Side::A),INDEX_NONE);
 // Mirror Move failure and copy preserve all slot definitions and copied PP.
 Fixture M;M.A.AssignMove(0,Move(TEXT("MirrorMove")));M.B.AssignMove(0,Move(TEXT("DrillPeck")));TStrongObjectPtr<UPokeMonsterBattleSession> MS(M.Session(0));R=MS->ResolveRound(0,1);TestTrue(TEXT("Mirror with no previous target fails safely"),Has(R,Event::EffectFailed));MS->ResolveRound(1,0);const int CopiedPP=MS->GetState().SideB.GetMoveSlots()[0].GetCurrentPP();R=MS->ResolveRound(0,1);TestTrue(TEXT("Mirror executes copied damage"),Damage(R,Side::B)>0);TestEqual(TEXT("Copy consumes no opponent PP"),MS->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(),CopiedPP);TestEqual(TEXT("Mirror remains original move slot"),MS->GetState().SideA.GetMoveSlots()[0].GetMove().LoadSynchronous(),Move(TEXT("MirrorMove")));
 // A copied multi-turn attack retains the definition while only Mirror Move loses PP.
 Fixture MC;MC.A.AssignMove(0,Move(TEXT("MirrorMove")));MC.B.AssignMove(0,Move(TEXT("HyperBeam")));TStrongObjectPtr<UPokeMonsterBattleSession> MCS(MC.Session(0));MCS->ResolveRound(1,0);R=MCS->ResolveRound(0,1);TestTrue(TEXT("Copied Hyper Beam damages"),Damage(R,Side::B)>0);TestEqual(TEXT("Copied Hyper Beam schedules original slot recharge"),MCS->ForcedMoveSlot(Side::A),0);const int MirrorPP=MCS->GetState().SideA.GetMoveSlots()[0].GetCurrentPP();R=MCS->ResolveRound(1,1);TestTrue(TEXT("Copied recharge resolves without consuming PP"),R.bSucceeded&&Damage(R,Side::B)==0&&MCS->GetState().SideA.GetMoveSlots()[0].GetCurrentPP()==MirrorPP);
 // A mechanical airborne charge, not a creature's decorative hover, is the bonus prerequisite.
 TStrongObjectPtr<UPokeMonsterMoveData> Air(NewObject<UPokeMonsterMoveData>());Air->InternalId=TEXT("SyntheticAirborneChargeOnly");Air->DisplayName=FText::FromString(TEXT("Technische Luftzustandsprüfung"));Air->BasePower=20;FPokeMonsterMoveEffectComponent Charge;Charge.Kind=Kind::Charge;Charge.Amount=1;Air->Effects={Charge};
 Fixture AF;AF.A.AssignMove(0,Move(TEXT("Gust")));AF.B.AssignMove(0,Air.Get());TStrongObjectPtr<UPokeMonsterBattleSession> AS(AF.Session(0));AS->ResolveRound(1,0);R=AS->ResolveRound(0,1);const int AirDamage=Damage(R,Side::B);
 Air->Effects[0].Amount=0;TStrongObjectPtr<UPokeMonsterBattleSession> Ground(AF.Session(0));Ground->ResolveRound(1,0);R=Ground->ResolveRound(0,1);TestEqual(TEXT("Wind move doubles against explicitly airborne charge only"),AirDamage,2*Damage(R,Side::B));
 // Gen-2 Flail thresholds and absence of random damage/criticals.
 Fixture L;auto* Flail=Move(TEXT("Flail"));const int HP[]={1,42,105,209,355,688,1000};const int Power[]={200,150,100,80,40,20,20};
 for(int I=0;I<7;++I){L.A.CurrentHP=HP[I];TestEqual(TEXT("Pinned Crystal HP-power bracket"),UPokeMonsterBattleLibrary::ResolveMovePower(L.A,Flail),Power[I]);}
 auto D1=UPokeMonsterBattleLibrary::CalculateCrystalDamage(L.A,L.B,Flail,0,0,0,0,true,217,false,false,false);auto D2=UPokeMonsterBattleLibrary::CalculateCrystalDamage(L.A,L.B,Flail,0,0,0,0,false,255,false,false,false);TestEqual(TEXT("Flail has no critical/variance in Gen2"),D1.Damage,D2.Damage);
 // Bodyguard blocks both incoming confusion and primary status, survives a voluntary switch.
 Fixture G;G.B.AssignMove(0,Move(TEXT("Safeguard")));G.A.AssignMove(0,Move(TEXT("Supersonic")));auto GReserve=G.B;GReserve.InstanceId=FGuid::NewGuid();TStrongObjectPtr<UPokeMonsterBattleSession> GS(G.Session(0,true,{GReserve}));GS->ResolveRound(1,0);R=GS->ResolveRound(0,1);TestEqual(TEXT("Safeguard prevents confusion"),GS->GetState().EffectsB.ConfusionTurns,0);GS->ResolveTurn(Attack,Switch);TestTrue(TEXT("Safeguard belongs to team across switch"),GS->GetState().SafeguardTurnsB>0);for(int I=0;I<3;++I)GS->ResolveRound(1,1);TestEqual(TEXT("Safeguard expires"),GS->GetState().SafeguardTurnsB,0);
 // Normal wild force-out grants no KO XP; trainer requires a living reserve and completed turn.
 Fixture W;W.A.AssignMove(0,Move(TEXT("Whirlwind")));auto WR=W.B;WR.InstanceId=FGuid::NewGuid();TStrongObjectPtr<UPokeMonsterBattleSession> WS(W.Session(0,false,{WR}));R=WS->ResolveRound(0,1);TestTrue(TEXT("Trainer force switch uses reserve"),R.bSucceeded&&WS->GetState().ActiveIndexB==1&&WS->GetState().Phase==EPokeMonsterBattlePhase::AwaitingChoices);
 WS.Reset(W.Session(0,false));R=WS->ResolveRound(0,1);TestTrue(TEXT("No trainer reserve fails"),Has(R,Event::EffectFailed)&&WS->GetState().Phase==EPokeMonsterBattlePhase::AwaitingChoices);
 return true;
}

IMPLEMENT_COMPLEX_AUTOMATION_TEST(FLearnBindingsV1,"PokeMonster.LearnMovesV1.Bindings",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
void FLearnBindingsV1::GetTests(TArray<FString>& N,TArray<FString>& C)const
{
 const TCHAR* Rows[]={
 TEXT("Karpador|1|Splash"),
 TEXT("Karpador|30|Flail"),
 TEXT("Garados|1|Thrash"),
 TEXT("Garados|35|Twister"),
 TEXT("Garados|50|HyperBeam"),
 TEXT("Smettbo|18|Supersonic"),
 TEXT("Smettbo|23|Whirlwind"),
 TEXT("Smettbo|28|Gust"),
 TEXT("Smettbo|34|Psybeam"),
 TEXT("Smettbo|40|Safeguard"),
 TEXT("Bibor|20|Twineedle"),
 TEXT("Bibor|30|Pursuit"),
 TEXT("Bibor|35|PinMissile"),
 TEXT("Habitak|25|Pursuit"),
 TEXT("Habitak|31|MirrorMove"),
 TEXT("Habitak|37|DrillPeck")};
 for(auto* Row:Rows){N.Add(Row);C.Add(Row);}
}
bool FLearnBindingsV1::RunTest(const FString& Row)
{
 using namespace LearnMovesV1Tests;TArray<FString> P;Row.ParseIntoArray(P,TEXT("|"));if(P.Num()!=3)return false;
 auto* S=Species(P[0]);auto* M=Move(P[2]);const int Level=FCString::Atoi(*P[1]);
 if(!TestNotNull(TEXT("Existing species"),S)||!TestNotNull(TEXT("New actual move"),M))return false;
 const auto* Binding=S->LevelUpMoves.FindByPredicate([&](const auto& E){return E.Level==Level&&E.Move.LoadSynchronous()==M;});
 if(!TestNotNull(TEXT("Exact original level now bound"),Binding))return false;
 TestTrue(TEXT("No unavailable placeholder remains"),Binding->UnavailableMoveName.IsEmpty()&&Binding->UnavailableReason.IsEmpty());
 auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(S,FMath::Max(1,Level-1));
 if(Level==1){TestTrue(TEXT("Level-one original move usable for newly created individual"),C.AssignSpeciesMoves());return TestTrue(TEXT("Expected starting move present"),C.GetLearnedMoves().ContainsByPredicate([M](const auto& E){return E.GetMove().LoadSynchronous()==M;}));}
 auto Free=C;auto NoNew=C;const int64 XP=C.GetExperienceToNextLevel();
 NoNew.AddExperience(FMath::Max<int64>(0,XP-1));TestTrue(TEXT("No premature learning before threshold"),NoNew.PendingMoves.IsEmpty()&&NoNew.GetLearnedMoves().IsEmpty());
 Free.AddExperience(XP);TestTrue(TEXT("Free slot learns immediately"),Free.GetLearnedMoves().ContainsByPredicate([M](const auto& E){return E.GetMove().LoadSynchronous()==M;}));
 const TCHAR* Existing[]={TEXT("/Game/Data/Moves/DA_Scratch"),TEXT("/Game/Data/Moves/DA_Growl"),TEXT("/Game/Data/Moves/DA_Ember"),TEXT("/Game/Data/Moves/DA_Tackle")};
 for(int I=0;I<4;++I){auto* Old=LoadObject<UPokeMonsterMoveData>(nullptr,Existing[I]);if(!TestNotNull(TEXT("Existing controlled full moveset"),Old))return false;C.AssignMove(I,Old);C.ConsumeMovePP(I,1);}
 C.AddExperience(XP);TestEqual(TEXT("Exactly one real offer"),C.PendingMoves.Num(),1);if(C.PendingMoves.Num()!=1)return false;TestEqual(TEXT("Exact offered move"),C.PendingMoves[0].LoadSynchronous(),M);
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
 TestTrue(TEXT("Install ordinary individual data"),E->RestorePersistentState({C},{},{}));auto* Snapshot=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());TArray<uint8> Bytes;TestTrue(TEXT("Native save encodes open offer"),UGameplayStatics::SaveGameToMemory(Snapshot,Bytes));
 auto* Decoded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));if(!TestTrue(TEXT("Existing validator restores open offer"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Decoded,E,I)))return false;
 auto Restored=E->GetPlayerParty()[0];TestEqual(TEXT("Pending offer survives"),Restored.PendingMoves.Num(),1);TestEqual(TEXT("Identity survives"),Restored.InstanceId,C.InstanceId);
 auto Declined=Restored;TestTrue(TEXT("Decline succeeds"),Declined.ResolveMoveLearning(INDEX_NONE));TestFalse(TEXT("Declined is not personally learned"),Declined.GetLearnedMoves().ContainsByPredicate([M](const auto& K){return K.GetMove().LoadSynchronous()==M;}));
 auto OldSlot=Restored.GetMoveSlots()[1];TestTrue(TEXT("Replace one of four slots"),Restored.ResolveMoveLearning(1));TestEqual(TEXT("Still exactly four active slots"),Restored.GetMoveSlots().Num(),4);
 TestTrue(TEXT("Removed old move and spent PP stay in repertoire"),Restored.GetLearnedMoves().ContainsByPredicate([&](const auto& K){return K.GetMove()==OldSlot.GetMove()&&K.GetCurrentPP()==OldSlot.GetCurrentPP();}));
 for(int Slot:{0,2,3})TestEqual(TEXT("Unrelated PP unchanged"),Restored.GetMoveSlots()[Slot].GetCurrentPP(),C.GetMoveSlots()[Slot].GetCurrentPP());
 auto Already=C;Already.PendingMoves.Reset();Already.Level=Level-1;Already.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(Already.GetExperienceGrowthRate(),Already.Level);Already.AssignMove(0,M);Already.AddExperience(Already.GetExperienceToNextLevel());TestTrue(TEXT("Already learned move not offered twice"),Already.PendingMoves.IsEmpty());
 return true;
}
#endif
