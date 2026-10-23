#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../UI/PokeMonsterBattlePresentationPlan.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"
namespace MoveEffectsV4Tests
{
using K=EPokeMonsterEffectKind;using Stat=EPokeMonsterBattleStat;using Status=EPokeMonsterCreatureStatus;using Ev=EPokeMonsterBattleEventType;using Side=EPokeMonsterBattleSide;
struct Fixture
{
 TStrongObjectPtr<UPokeMonsterCreatureSpeciesData> Species{NewObject<UPokeMonsterCreatureSpeciesData>()};
 TStrongObjectPtr<UPokeMonsterMoveData> Strike{NewObject<UPokeMonsterMoveData>()},Wait{NewObject<UPokeMonsterMoveData>()};
 TArray<TStrongObjectPtr<UPokeMonsterMoveData>> Held;
 FPokeMonsterCreatureInstance A,B;
 Fixture()
 {
  Strike->InternalId=TEXT("V4Strike");Strike->DisplayName=FText::FromString(TEXT("Prüfangriff"));Strike->BasePower=40;Strike->MaxPP=100;
  Wait->InternalId=TEXT("V4Wait");Wait->DisplayName=FText::FromString(TEXT("Warten · technischer Test"));Wait->Category=EPokeMonsterMoveCategory::Status;Wait->BasePower=0;Wait->MaxPP=100;
  A=FPokeMonsterCreatureInstance::CreateFromSpecies(Species.Get(),10);B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species.Get(),10);
  for(auto* C:{&A,&B}){C->CurrentHP=C->CalculatedStats.MaxHP=500;C->CalculatedStats.Attack=C->CalculatedStats.Defense=C->CalculatedStats.SpecialAttack=C->CalculatedStats.SpecialDefense=100;C->CalculatedStats.Speed=50;C->AssignMove(0,Strike.Get());C->AssignMove(1,Wait.Get());}A.CalculatedStats.Speed=100;
 }
 UPokeMonsterMoveData* Move(K Kind,bool Self=false,bool Damaging=false)
 {
  auto* M=NewObject<UPokeMonsterMoveData>();Held.Emplace(M);M->InternalId=FName(*FString::Printf(TEXT("V4_%d_%d"),uint8(Kind),Held.Num()));M->DisplayName=FText::FromString(TEXT("Effektprüfung"));M->MaxPP=100;M->Category=Damaging?EPokeMonsterMoveCategory::Physical:EPokeMonsterMoveCategory::Status;M->BasePower=Damaging?40:0;
  FPokeMonsterMoveEffectComponent C;C.Kind=Kind;C.bSelf=Self;M->Effects={C};return M;
 }
 UPokeMonsterBattleSession* Session(int Seed=17,bool Extended=false)
 {
  auto* S=NewObject<UPokeMonsterBattleSession>();FPokeMonsterBattleEffectRules R;R.bExtendedStatus=Extended;S->ConfigureEffectRules(R);S->InitializeTeams({A},{B},Seed);return S;
 }
};
bool Has(const FPokeMonsterBattleResult& R,Ev E){return R.Events.ContainsByPredicate([E](const auto& X){return X.Type==E;});}
}
#define V4_TEST(Class,Name) IMPLEMENT_SIMPLE_AUTOMATION_TEST(Class,"PokeMonster.MoveEffectsV4." Name,EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter) bool Class::RunTest(const FString&)
V4_TEST(FMoveEffectsV4Configuration,"ConfigurationRejectsIncompleteEffects")
{
 using namespace MoveEffectsV4Tests;Fixture F;
 auto* M=F.Move(K::Heal,true);TestTrue(TEXT("Fractional heal configured"),M->IsConfigured());M->Effects[0].Denominator=0;TestFalse(TEXT("Zero denominator rejected"),M->IsConfigured());M->Effects[0].Denominator=2;M->Effects[0].Numerator=0;TestFalse(TEXT("Zero fraction does not secretly heal one"),M->IsConfigured());
 M=F.Move(K::MultiHit,false,true);TestFalse(TEXT("Missing weighted distribution rejected"),M->IsConfigured());M->Effects[0].HitWeights={3,3,1,1};TestTrue(TEXT("Explicit distribution accepted"),M->IsConfigured());const auto Duplicate=M->Effects[0];M->Effects.Add(Duplicate);TestFalse(TEXT("Duplicate hit controllers rejected instead of silently ignoring one"),M->IsConfigured());M->Effects.RemoveAt(1);M->Effects[0].HitWeights[0]=-1;TestFalse(TEXT("Negative weight rejected"),M->IsConfigured());
 M=F.Move(K::Charge);M->Effects[0].bSecondary=true;TestFalse(TEXT("Charge cannot be a secondary controller"),M->IsConfigured());M=F.Move(K::Stage);M->CriticalStageBonus=3;TestFalse(TEXT("Unsupported critical bonus rejected"),M->IsConfigured());
 return true;
}
V4_TEST(FMoveEffectsV4Stages,"SevenStagesLimitsAndSpecialDamage")
{
 using namespace MoveEffectsV4Tests;Fixture F;auto* M=F.Move(K::Stage,true);
 M->Effects.Reset();for(uint8 I=0;I<7;++I){FPokeMonsterMoveEffectComponent C;C.Kind=K::Stage;C.bSelf=true;C.Stat=Stat(I);C.Stages=2;M->Effects.Add(C);}F.A.AssignMove(2,M);auto* S=F.Session();
 for(int I=0;I<4;++I)TestTrue(TEXT("Composable stages resolve"),S->ResolveRound(2,1).bSucceeded);
 const auto& T=S->GetState();TestEqual(TEXT("Attack capped"),T.AttackStageA,6);TestEqual(TEXT("Defense capped"),T.DefenseStageA,6);TestEqual(TEXT("Speed capped"),T.SpeedStageA,6);TestEqual(TEXT("Special attack capped"),T.EffectsA.SpecialAttack,6);TestEqual(TEXT("Special defense capped"),T.EffectsA.SpecialDefense,6);TestEqual(TEXT("Accuracy capped"),T.EffectsA.Accuracy,6);TestEqual(TEXT("Evasion capped"),T.EffectsA.Evasion,6);
 TestTrue(TEXT("Limit produces useful failure"),Has(S->ResolveRound(2,1),Ev::EffectFailed));
 Fixture Display;auto* Boost=Display.Move(K::Stage,true);Boost->Effects[0].Stages=1;Display.A.AssignMove(2,Boost);const auto Actions=UPokeMonsterBattlePresentationPlan::BuildActions(Display.Session()->ResolveRound(2,1));TestTrue(TEXT("Working status move has real feedback instead of false no-effect placeholder"),Actions.ContainsByPredicate([](const auto& A){return A.Outcome==EPokeMonsterPresentationOutcome::Status&&!A.Information.IsEmpty();}));
 auto* Special=F.Strike.Get();Special->Category=EPokeMonsterMoveCategory::Special;const int Base=UPokeMonsterBattleLibrary::CalculateDamage(F.A,F.B,Special).Damage;
 TestTrue(TEXT("Special attack now affects actual damage"),UPokeMonsterBattleLibrary::CalculateDamage(F.A,F.B,Special,0,0,2,0).Damage>Base);TestTrue(TEXT("Special defense now affects actual damage"),UPokeMonsterBattleLibrary::CalculateDamage(F.A,F.B,Special,0,0,0,2).Damage<Base);
 TestEqual(TEXT("Accuracy minimum ratio"),UPokeMonsterBattleLibrary::AccuracyAtStages(90,-6,6),30);TestEqual(TEXT("Extreme stage inputs are safely clamped"),UPokeMonsterBattleLibrary::AccuracyAtStages(90,MIN_int32,MAX_int32),30);TestEqual(TEXT("Accuracy maximum clamps to 100"),UPokeMonsterBattleLibrary::AccuracyAtStages(90,6,-6),100);
 for(auto& C:M->Effects)C.Stages=-6;S->ResolveRound(2,1);S->ResolveRound(2,1);S->ResolveRound(2,1);TestEqual(TEXT("Negative cap"),S->GetState().EffectsA.Evasion,-6);
 return true;
}
V4_TEST(FMoveEffectsV4Chance,"StatusChanceImmunityAndLegacyRNG")
{
 using namespace MoveEffectsV4Tests;Fixture F;auto* M=F.Move(K::PrimaryStatus,false,true);M->Effects[0].bSecondary=true;M->Effects[0].Status=Status::Burn;M->Effects[0].ChancePercent=0;F.A.AssignMove(2,M);auto* S=F.Session();S->ResolveRound(2,1);TestEqual(TEXT("0 percent never applies"),S->GetState().SideB.Status,Status::None);
 M->Effects[0].ChancePercent=100;S=F.Session();S->ResolveRound(2,1);TestEqual(TEXT("100 percent applies"),S->GetState().SideB.Status,Status::Burn);
 M->Effects[0].ImmuneTypes={F.Species->GetPrimaryType()};S=F.Session();S->ResolveRound(2,1);TestEqual(TEXT("Configured immunity wins at 100 percent"),S->GetState().SideB.Status,Status::None);
 // Ineligible legacy burns must not advance the old random stream.
 auto* Old=NewObject<UPokeMonsterMoveData>();Old->InternalId=TEXT("LegacyBurn");Old->DisplayName=FText::FromString(TEXT("Verbrennung"));Old->BasePower=40;Old->MaxPP=100;Old->Effect.EffectId=TEXT("Burn");Old->Effect.ChancePercent=10;
 F.A.AssignMove(2,Old);F.B.Status=Status::Burn;auto* Legacy=F.Session(123);auto R=Legacy->ResolveRound(2,0);FRandomStream Expected(123);const int First=Expected.RandRange(0,99),Second=Expected.RandRange(0,99);TArray<int> Rolls;for(const auto& E:R.Events)if(E.Type==Ev::MoveExecuted)Rolls.Add(E.HitRoll);TestTrue(TEXT("Two expected accuracy draws only"),Rolls.Num()==2&&Rolls[0]==First&&Rolls[1]==Second);
 auto* Guaranteed=NewObject<UPokeMonsterMoveData>();Guaranteed->InternalId=TEXT("LegacyGuaranteedStage");Guaranteed->DisplayName=FText::FromString(TEXT("Alter garantierter Statuseffekt"));Guaranteed->Category=EPokeMonsterMoveCategory::Status;Guaranteed->BasePower=0;Guaranteed->MaxPP=100;Guaranteed->Effect.EffectId=TEXT("AttackDown");Guaranteed->Effect.ChancePercent=0;F.A.AssignMove(2,Guaranteed);F.B.Status=Status::None;S=F.Session(123);R=S->ResolveRound(2,0);TestEqual(TEXT("Legacy primary stage ignores historically unused probability field"),S->GetState().AttackStageB,-1);Rolls.Reset();for(const auto& E:R.Events)if(E.Type==Ev::MoveExecuted)Rolls.Add(E.HitRoll);TestTrue(TEXT("Guaranteed legacy stage adds no random draw"),Rolls.Num()==2&&Rolls[0]==First&&Rolls[1]==Second);
 return true;
}
V4_TEST(FMoveEffectsV4Primary,"OptInPrimaryStatusActionAndPersistenceRules")
{
 using namespace MoveEffectsV4Tests;Fixture F;auto* M=F.Move(K::PrimaryStatus);M->Effects[0].Status=Status::Sleep;M->Effects[0].MinTurns=M->Effects[0].MaxTurns=3;F.A.AssignMove(2,M);
 auto* S=F.Session();TestFalse(TEXT("Unapproved extended rule profile fails closed"),S->ResolveRound(2,0).bSucceeded);S=F.Session(17,true);auto R=S->ResolveRound(2,0);TestTrue(TEXT("Sleep applied"),Has(R,Ev::StatusApplied));TestEqual(TEXT("Asleep target spent no AP"),S->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(),100);TestEqual(TEXT("Sleep timer on individual"),S->GetState().SideB.StatusTurns,2);
 R=S->ResolveRound(1,0);TestTrue(TEXT("Sleep prevents action"),Has(R,Ev::StatusPrevented));R=S->ResolveRound(1,0);TestTrue(TEXT("Wake-up announced"),Has(R,Ev::StatusRecovered));TestEqual(TEXT("Wake-up action permitted by opt-in profile"),S->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(),99);
 F.A.Status=Status::Paralysis;S=NewObject<UPokeMonsterBattleSession>();FPokeMonsterBattleEffectRules Rules;Rules.bExtendedStatus=true;Rules.ParalysisSkipPercent=100;S->ConfigureEffectRules(Rules);S->InitializeTeams({F.A},{F.B},18);R=S->ResolveRound(0,1);TestEqual(TEXT("Paralysis prevents AP spend"),S->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(),100);
 F.A.Status=Status::Freeze;S=NewObject<UPokeMonsterBattleSession>();Rules.FreezeThawPercent=100;S->ConfigureEffectRules(Rules);S->InitializeTeams({F.A},{F.B},18);R=S->ResolveRound(0,1);TestEqual(TEXT("Configured thaw probability honored"),S->GetState().SideA.Status,Status::None);
 F.A.Status=Status::Poison;S=F.Session(18,true);R=S->ResolveRound(1,1);TestEqual(TEXT("Poison residual is configured eighth"),S->GetState().SideA.CurrentHP,438);TestTrue(TEXT("Residual presentation exists"),UPokeMonsterBattlePresentationPlan::BuildActions(R).ContainsByPredicate([](const auto& A){return A.bResidual&&A.Damage==62;}));
 return true;
}
V4_TEST(FMoveEffectsV4Fractions,"HealDrainRecoilAndFainting")
{
 using namespace MoveEffectsV4Tests;Fixture F;F.A.CurrentHP=100;auto* M=F.Move(K::Heal,true);F.A.AssignMove(2,M);auto* S=F.Session();auto R=S->ResolveRound(2,1);TestEqual(TEXT("Self healing fraction"),S->GetState().SideA.CurrentHP,350);
 M=F.Move(K::Drain,true,true);F.A.AssignMove(2,M);S=F.Session();R=S->ResolveRound(2,1);const int Actual=500-S->GetState().SideB.CurrentHP;TestEqual(TEXT("Drain based on actual removed HP"),S->GetState().SideA.CurrentHP,100+FMath::Max(1,Actual/2));
 F.B.CurrentHP=1;S=F.Session();R=S->ResolveRound(2,1);TestEqual(TEXT("No overkill drain"),S->GetState().SideA.CurrentHP,101);
 F.B.CurrentHP=500;F.A.CurrentHP=1;M=F.Move(K::Recoil,true,true);F.A.AssignMove(2,M);S=F.Session();R=S->ResolveRound(2,1);TestEqual(TEXT("Recoil can faint attacker"),S->GetState().SideA.CurrentHP,0);TestEqual(TEXT("Opponent wins after recoil faint"),S->GetState().Winner,Side::B);TestTrue(TEXT("Recoil HP animation"),UPokeMonsterBattlePresentationPlan::BuildActions(R).ContainsByPredicate([](const auto& A){return A.bResidual&&A.Target==Side::A&&A.HPAfter==0;}));
 return true;
}
V4_TEST(FMoveEffectsV4Hits,"MultiHitFixedDamageAndSleepingPrerequisite")
{
 using namespace MoveEffectsV4Tests;Fixture F;auto* M=F.Move(K::MultiHit,false,true);M->Effects[0].MinHits=2;M->Effects[0].MaxHits=5;M->Effects[0].HitWeights={0,0,0,1};F.A.AssignMove(2,M);auto* S=F.Session();auto R=S->ResolveRound(2,1);int Hits=0;for(const auto& E:R.Events)Hits+=E.Type==Ev::Damage;TestEqual(TEXT("Explicit five-hit sequence"),Hits,5);TestEqual(TEXT("Only one AP per sequence"),S->GetState().SideA.GetMoveSlots()[2].GetCurrentPP(),99);
 const auto Plan=UPokeMonsterBattlePresentationPlan::BuildActions(R);const auto* Action=Plan.FindByPredicate([](const auto& A){return A.Source==Side::A&&!A.bInformation;});TestTrue(TEXT("HP presentation covers full sequence"),Action&&Action->HPBefore==500&&Action->HPAfter==S->GetState().SideB.CurrentHP&&Action->Damage==500-S->GetState().SideB.CurrentHP);
 F.B.CurrentHP=1;S=F.Session();R=S->ResolveRound(2,1);Hits=0;for(const auto& E:R.Events)Hits+=E.Type==Ev::Damage;TestEqual(TEXT("Sequence stops immediately at faint"),Hits,1);
 F.B.CurrentHP=500;M=F.Move(K::FixedDamage,false,true);M->BasePower=0;M->Effects[0].Amount=40;F.A.AssignMove(2,M);S=F.Session();R=S->ResolveRound(2,1);TestEqual(TEXT("Fixed amount"),S->GetState().SideB.CurrentHP,460);
 M->bRequiresSleepingTarget=true;S=F.Session();R=S->ResolveRound(2,1);TestEqual(TEXT("Prerequisite failure deals no damage"),S->GetState().SideB.CurrentHP,500);TestEqual(TEXT("Failed condition still costs AP"),S->GetState().SideA.GetMoveSlots()[2].GetCurrentPP(),99);TestTrue(TEXT("Prerequisite failure explained"),Has(R,Ev::EffectFailed));
 M->bRequiresSleepingTarget=false;M->Accuracy=0;M->bNeverMiss=true;TestTrue(TEXT("Shared hit helper respects explicit never-miss flag"),UPokeMonsterBattleLibrary::CheckHit(M,99));S=F.Session();S->ResolveRound(2,1);TestEqual(TEXT("Runtime never-miss agrees with helper"),S->GetState().SideB.CurrentHP,460);
 return true;
}
V4_TEST(FMoveEffectsV4Volatile,"ProtectFlinchConfusionAndSwitchReset")
{
 using namespace MoveEffectsV4Tests;Fixture F;auto* M=F.Move(K::Protect,true);M->Priority=4;F.A.AssignMove(2,M);auto* S=F.Session();auto R=S->ResolveRound(2,0);TestEqual(TEXT("Protect blocks direct damage"),S->GetState().SideA.CurrentHP,500);R=S->ResolveRound(1,0);TestTrue(TEXT("Protect lasts one round"),S->GetState().SideA.CurrentHP<500);
 M=F.Move(K::Flinch,false,true);M->Effects[0].bSecondary=true;F.A.AssignMove(2,M);S=F.Session();R=S->ResolveRound(2,0);TestTrue(TEXT("Flinch prevents slower action"),Has(R,Ev::Flinched));TestEqual(TEXT("Flinched opponent no AP spent"),S->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(),100);R=S->ResolveRound(1,0);TestEqual(TEXT("Flinch cleared next round"),S->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(),99);
 M=F.Move(K::Confusion);M->Effects[0].MinTurns=M->Effects[0].MaxTurns=4;F.A.AssignMove(2,M);auto Reserve=F.B;Reserve.InstanceId=FGuid::NewGuid();S=NewObject<UPokeMonsterBattleSession>();S->InitializeTeams({F.A},{F.B,Reserve},17);R=S->ResolveRound(2,1);TestTrue(TEXT("Confusion stored battle-locally"),S->GetState().EffectsB.ConfusionTurns>0);
 FPokeMonsterBattleChoice Wait,Switch;Wait.Index=1;Switch.Type=EPokeMonsterBattleChoiceType::Switch;Switch.Index=1;TestTrue(TEXT("Switch accepted"),S->ResolveTurn(Wait,Switch).bSucceeded);TestEqual(TEXT("Switch clears confusion"),S->GetState().EffectsB.ConfusionTurns,0);TestEqual(TEXT("No persistent confusion status invented"),S->GetState().SideB.Status,Status::None);
 // A self-hit followed by the existing burn tick may end the battle before the opponent acts.
 Fixture Burn;Burn.A.Status=Status::Burn;Burn.A.CurrentHP=130;auto* Confuse=Burn.Move(K::Confusion);Confuse->Effects[0].MinTurns=Confuse->Effects[0].MaxTurns=4;Burn.B.AssignMove(2,Confuse);bool Exercised=false;
 for(int Seed=0;Seed<64 && !Exercised;++Seed){auto* T=Burn.Session(Seed);T->ResolveRound(1,2);auto End=T->ResolveRound(1,0);if(Has(End,Ev::ConfusionDamage) && T->GetState().SideA.CurrentHP==0){Exercised=true;TestEqual(TEXT("Burn after confusion finishes battle"),T->GetState().Phase,EPokeMonsterBattlePhase::Finished);TestFalse(TEXT("No opponent action after residual knockout"),End.Events.ContainsByPredicate([](const auto& E){return E.Type==Ev::MoveExecuted&&E.Source==Side::B;}));}}
 TestTrue(TEXT("Deterministic confusion/burn boundary exercised"),Exercised);
 return true;
}
V4_TEST(FMoveEffectsV4Screen,"TeamScreenDurationAndSpecialDamage")
{
 using namespace MoveEffectsV4Tests;Fixture F;auto* M=F.Move(K::Screen,true);M->Effects[0].MaxTurns=3;F.A.AssignMove(2,M);F.Strike->Category=EPokeMonsterMoveCategory::Special;auto* S=F.Session();auto R=S->ResolveRound(2,0);const int Normal=UPokeMonsterBattleLibrary::CalculateDamage(F.B,F.A,F.Strike.Get()).Damage;TestEqual(TEXT("Special screen halves damage"),500-S->GetState().SideA.CurrentHP,FMath::Max(1,Normal/2));TestEqual(TEXT("Screen duration decremented at round end"),S->GetState().ScreenTurnsA,2);R=S->ResolveRound(2,1);TestTrue(TEXT("Existing screen does not silently refresh"),Has(R,Ev::EffectFailed));R=S->ResolveRound(1,1);TestEqual(TEXT("Screen expires"),S->GetState().ScreenTurnsA,0);
 return true;
}
V4_TEST(FMoveEffectsV4Atomic,"RejectedRoundLeavesAPAndSeedUntouched")
{
 using namespace MoveEffectsV4Tests;Fixture F;auto* M=F.Move(K::PrimaryStatus,false,true);M->Effects[0].Status=Status::Burn;M->Effects[0].ChancePercent=37;M->Effects[0].bSecondary=true;F.A.AssignMove(2,M);auto* A=F.Session(812);auto* B=F.Session(812);
 TestFalse(TEXT("Invalid slot rejected"),A->ResolveRound(8,0).bSucceeded);TestEqual(TEXT("Rejected round no AP consumption"),A->GetState().SideA.GetMoveSlots()[2].GetCurrentPP(),100);TestEqual(TEXT("Rejected round no progression"),A->GetState().RoundNumber,0);
 auto RA=A->ResolveRound(2,0),RB=B->ResolveRound(2,0);TestEqual(TEXT("Controlled random stream gives same status"),A->GetState().SideB.Status,B->GetState().SideB.Status);TestEqual(TEXT("Same event count"),RA.Events.Num(),RB.Events.Num());for(int I=0;I<FMath::Min(RA.Events.Num(),RB.Events.Num());++I){TestEqual(TEXT("Same random rolls"),RA.Events[I].HitRoll,RB.Events[I].HitRoll);TestEqual(TEXT("Same event kind"),RA.Events[I].Type,RB.Events[I].Type);}
 return true;
}
V4_TEST(FMoveEffectsV4Save,"PrimaryStatusSave7AndOldSchemaMigration")
{
 using namespace MoveEffectsV4Tests;TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,10);C.AssignSpeciesMoves();C.ConsumeMovePP(0,3);const auto Id=C.InstanceId;
 for(Status S:{Status::Burn,Status::Paralysis,Status::Sleep,Status::Poison,Status::Freeze})
 {
  C.Status=S;C.StatusTurns=S==Status::Sleep?3:0;TestTrue(TEXT("Status individual accepted"),E->RestorePersistentState({C},{},{}));auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());if(!TestNotNull(TEXT("Status save captured"),Save))return false;
  TArray<uint8> Bytes;TestTrue(TEXT("Unreal serialization"),UGameplayStatics::SaveGameToMemory(Save,Bytes));auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));TestTrue(TEXT("Status restore"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I));const auto& Out=E->GetPlayerParty()[0];TestEqual(TEXT("Persistent status"),Out.Status,S);TestEqual(TEXT("Sleep turns persist"),Out.StatusTurns,C.StatusTurns);TestEqual(TEXT("Identity unchanged"),Out.InstanceId,Id);TestEqual(TEXT("AP retained"),Out.GetMoveSlots()[0].GetCurrentPP(),C.GetMoveSlots()[0].GetCurrentPP());
 }
 C.Status=Status::Burn;C.StatusTurns=0;E->RestorePersistentState({C},{},{});auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());for(int V=1;V<=6;++V){Save->SaveVersion=V;TestTrue(TEXT("Old schema accepted"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I));TestEqual(TEXT("Existing burn preserved"),E->GetPlayerParty()[0].Status,V>=4?Status::Burn:Status::None);}
 C.Status=Status::Sleep;C.StatusTurns=0;TestFalse(TEXT("Malformed sleep timer rejected"),C.RestoreIndividualState(Id,C.Level,C.Experience,C.CurrentHP,C.GetMoveSlots(),Status::Sleep,0));C.Status=Status::Freeze;C.StatusTurns=0;TestTrue(TEXT("Existing full healing clears ailment"),C.RestoreFully());TestEqual(TEXT("Healed status"),C.Status,Status::None);TestEqual(TEXT("Healed timer"),C.StatusTurns,0);
 return true;
}
#undef V4_TEST
#endif
