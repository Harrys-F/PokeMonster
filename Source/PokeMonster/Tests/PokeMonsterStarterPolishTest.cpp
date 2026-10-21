#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../UI/PokeMonsterBattlePresentationPlan.h"
#include "UObject/StrongObjectPtr.h"
namespace StarterPolishTests
{
struct Fixture
{
 TStrongObjectPtr<UPokeMonsterCreatureSpeciesData> Species{NewObject<UPokeMonsterCreatureSpeciesData>()};
 TStrongObjectPtr<UPokeMonsterMoveData> Strike{NewObject<UPokeMonsterMoveData>()};
 FPokeMonsterCreatureInstance A,B;
 Fixture(){Strike->InternalId=TEXT("PolishFixture");Strike->DisplayName=FText::FromString(TEXT("Fixture"));Strike->BasePower=20;Strike->MaxPP=100;A=FPokeMonsterCreatureInstance::CreateFromSpecies(Species.Get(),10);B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species.Get(),10);for(auto* C:{&A,&B}){C->CurrentHP=C->CalculatedStats.MaxHP=500;C->CalculatedStats.Attack=C->CalculatedStats.Defense=C->CalculatedStats.SpecialAttack=C->CalculatedStats.SpecialDefense=100;C->CalculatedStats.Speed=50;C->AssignMove(0,Strike.Get());}}
 UPokeMonsterBattleSession* Session(int Seed=17){auto* S=NewObject<UPokeMonsterBattleSession>();S->InitializeTeams({A},{B},Seed);return S;}
};
UPokeMonsterMoveData* Move(const TCHAR* Name){return LoadObject<UPokeMonsterMoveData>(nullptr,*FString::Printf(TEXT("/Game/Data/Moves/DA_%s.DA_%s"),Name,Name));}
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStarterDefenseEffects,"PokeMonster.Battle.Starters.DefenseAndSpeedEffects",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FStarterDefenseEffects::RunTest(const FString& Parameters)
{
 using namespace StarterPolishTests;Fixture F;auto* Tail=Move(TEXT("TailWhip"));auto* Withdraw=Move(TEXT("Withdraw"));auto* Bubble=Move(TEXT("Bubble"));if(!Tail||!Withdraw||!Bubble){AddError(TEXT("Missing verified starter move assets"));return false;}
 F.A.AssignMove(1,Tail);F.A.AssignMove(2,Withdraw);F.A.CalculatedStats.Speed=100;
 auto* S=F.Session();auto R=S->ResolveRound(1,0);TestTrue(TEXT("Tail Whip accepted"),R.bSucceeded);TestEqual(TEXT("Defense lowered"),S->GetState().DefenseStageB,-1);
 TestTrue(TEXT("Physical damage increases"),UPokeMonsterBattleLibrary::CalculateDamage(F.A,F.B,F.Strike.Get(),0,-1).Damage>UPokeMonsterBattleLibrary::CalculateDamage(F.A,F.B,F.Strike.Get()).Damage);
 R=S->ResolveRound(2,0);TestEqual(TEXT("Withdraw raises own defense"),S->GetState().DefenseStageA,1);
 TestFalse(TEXT("Withdraw is not an attacking hit"),R.Events.ContainsByPredicate([](const auto& E){return E.Type==EPokeMonsterBattleEventType::Damage&&E.Source==EPokeMonsterBattleSide::A;}));
 auto* Special=NewObject<UPokeMonsterMoveData>();Special->InternalId=TEXT("SpecialFixture");Special->Category=EPokeMonsterMoveCategory::Special;
 TestEqual(TEXT("Physical defense stage leaves special damage unchanged"),UPokeMonsterBattleLibrary::CalculateDamage(F.A,F.B,Special,0,6).Damage,UPokeMonsterBattleLibrary::CalculateDamage(F.A,F.B,Special).Damage);
 for(int I=0;I<7;++I)S->ResolveRound(2,0);TestEqual(TEXT("Positive stage capped"),S->GetState().DefenseStageA,6);
 // Exercise actual 10% asset across deterministic seeds, without changing its chance.
 int Applied=0;
 for(int Seed=0;Seed<100;++Seed){F.A.AssignMove(3,Bubble);auto* T=F.Session(Seed);T->ResolveRound(3,0);Applied+=T->GetState().SpeedStageB==-1;}
 TestTrue(TEXT("Bubble secondary effect sometimes applies, not guaranteed"),Applied>0&&Applied<35);
 TestEqual(TEXT("Speed stage changes effective initiative"),UPokeMonsterBattleLibrary::ApplyStage(90,-1),60);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStarterSeedEffects,"PokeMonster.Battle.Starters.LeechSeedAndSwitch",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FStarterSeedEffects::RunTest(const FString& Parameters)
{
 using namespace StarterPolishTests;Fixture F;auto* Seed=Move(TEXT("LeechSeed"));if(!TestNotNull(TEXT("Leech Seed"),Seed))return false;F.A.AssignMove(1,Seed);F.A.CurrentHP=250;
 UPokeMonsterBattleSession* S=nullptr;FPokeMonsterBattleResult R;
 for(int I=0;I<100;++I){S=F.Session(I);R=S->ResolveRound(1,0);if(S->GetState().bSeededB)break;}
 TestTrue(TEXT("Seed applied"),S->GetState().bSeededB);
 const auto* D=R.Events.FindByPredicate([](const auto& E){return E.Type==EPokeMonsterBattleEventType::SeedDamage;});
 TestTrue(TEXT("Once-per-round eighth of max HP"),D&&D->Damage==62&&D->Target==EPokeMonsterBattleSide::B);
 TestTrue(TEXT("Recipient heals without invented excess HP"),S->GetState().SideA.CurrentHP>F.A.CurrentHP&&S->GetState().SideA.CurrentHP<=F.A.GetMaxHP());
 const auto Actions=UPokeMonsterBattlePresentationPlan::BuildActions(R);
 TestTrue(TEXT("Drain has separate HP presentation"),Actions.ContainsByPredicate([](const auto& A){return A.bResidual&&A.Target==EPokeMonsterBattleSide::B;}));
 TestTrue(TEXT("Recovery uses existing animated HP path"),Actions.ContainsByPredicate([](const auto& A){return A.bItem&&A.bAffectsActiveHP&&A.Target==EPokeMonsterBattleSide::A;}));
 auto Reserve=F.B;Reserve.InstanceId=FGuid::NewGuid();S=NewObject<UPokeMonsterBattleSession>();S->InitializeTeams({F.A},{F.B,Reserve},17);
 for(int I=0;I<6&&!S->GetState().bSeededB;++I)S->ResolveRound(1,0);
 TestTrue(TEXT("Switch fixture seeded"),S->GetState().bSeededB);
 FPokeMonsterBattleChoice Attack,Switch;Attack.Index=0;Switch.Type=EPokeMonsterBattleChoiceType::Switch;Switch.Index=1;
 R=S->ResolveTurn(Attack,Switch);TestTrue(TEXT("Switch works"),R.bSucceeded);TestFalse(TEXT("Switch clears volatile seed"),S->GetState().bSeededB);
 auto* Grass=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Bisasam.DA_Bisasam"));auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Grass,10);C.AssignMove(0,F.Strike.Get());S=NewObject<UPokeMonsterBattleSession>();S->InitializeTeams({F.A},{C},17);S->ResolveRound(1,0);TestFalse(TEXT("Grass is immune to Leech Seed"),S->GetState().bSeededB);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStarterLearnsetData,"PokeMonster.Battle.Starters.VerifiedGen2Learnsets",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FStarterLearnsetData::RunTest(const FString& Parameters)
{
 using namespace StarterPolishTests;
 auto* SG=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Schiggy.DA_Schiggy"));auto* B=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Bisasam.DA_Bisasam"));if(!SG||!B)return false;
 const auto Moves=SG->MovesForLevel(13);TestEqual(TEXT("Only last four learned moves on new level-13 individuals"),Moves.Num(),4);
 const TCHAR* Ids[]={TEXT("TailWhip"),TEXT("Bubble"),TEXT("Withdraw"),TEXT("WaterGun")};for(int I=0;I<Moves.Num();++I)TestEqual(TEXT("Chronological learning"),Moves[I]->InternalId,FName(Ids[I]));
 TestEqual(TEXT("Bubble is Gen2 power 20, not later-gen 40"),Move(TEXT("Bubble"))->BasePower,20);TestEqual(TEXT("Bubble PP"),Move(TEXT("Bubble"))->MaxPP,30);TestEqual(TEXT("Seed accuracy"),Move(TEXT("LeechSeed"))->Accuracy,90);
 TestEqual(TEXT("Bulbasaur learns seed at 7"),B->MovesForLevel(7).Num(),3);TestEqual(TEXT("Four moves at 10"),B->MovesForLevel(10).Num(),4);
 auto Old=FPokeMonsterCreatureInstance::CreateFromSpecies(SG,13);Old.AssignMove(0,Move(TEXT("Tackle")));Old.ConsumeMovePP(0,3);const auto Id=Old.InstanceId;auto Restored=FPokeMonsterCreatureInstance::CreateFromSpecies(SG,13);TestTrue(TEXT("Existing individual slots restore"),Restored.RestoreIndividualState(Old.InstanceId,Old.Level,Old.Experience,Old.CurrentHP,Old.GetMoveSlots()));Old=Restored;
 TestEqual(TEXT("Existing move never overwritten by expanded learnset"),Old.GetMoveSlots()[0].GetMove().Get(),Move(TEXT("Tackle")));TestEqual(TEXT("Spent PP retained"),Old.GetMoveSlots()[0].GetCurrentPP(),Move(TEXT("Tackle"))->MaxPP-3);TestEqual(TEXT("Individual identity retained"),Old.InstanceId,Id);
 return true;
}
#endif
