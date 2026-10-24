#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Algo/Find.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/GameInstance.h"
#include "UObject/StrongObjectPtr.h"
namespace BiomeV11QA
{
struct SpeciesCase {const TCHAR* Name;int32 Dex;float Size;};
static const SpeciesCase SpeciesCases[]={{TEXT("Karpador"),129,90},{TEXT("Garados"),130,650},{TEXT("Raupy"),10,30},{TEXT("Hornliu"),13,30},{TEXT("Smettbo"),12,110},{TEXT("Bibor"),15,100},{TEXT("Habitak"),21,30}};
static UPokeMonsterCreatureSpeciesData* Species(const FString& Name)
{return LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*(TEXT("/Game/Data/Creatures/DA_")+Name+TEXT(".DA_")+Name));}
}
IMPLEMENT_COMPLEX_AUTOMATION_TEST(FBiomeV11SpeciesPersistence,"PokeMonster.BiomeV11.SpeciesPersistence",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
void FBiomeV11SpeciesPersistence::GetTests(TArray<FString>& Names,TArray<FString>& Commands)const
{for(const auto& Row:BiomeV11QA::SpeciesCases){Names.Add(Row.Name);Commands.Add(Row.Name);}}
bool FBiomeV11SpeciesPersistence::RunTest(const FString& Name)
{
 using namespace BiomeV11QA;
 const auto* Row=Algo::FindByPredicate(SpeciesCases,[&](const auto& R){return Name==R.Name;});if(!Row)return false;
 auto* S=Species(Name);if(!TestNotNull(TEXT("Actual imported species"),S))return false;
 TestEqual(TEXT("Stable species identity"),S->GetInternalId(),FName(Row->Name));TestEqual(TEXT("National catalogue number"),S->GetPokedexNumber(),Row->Dex);
 auto* V=S->GetVisuals().Presentation.LoadSynchronous();if(!TestNotNull(TEXT("Own actual presentation"),V))return false;
 TestTrue(TEXT("Actual skeleton/material/clip contract"),V->GetValidationErrors().IsEmpty());TestEqual(TEXT("Original catalogue size"),V->ReferenceSizeCm,Row->Size);TestEqual(TEXT("Seven standard roles"),V->Clips.Num(),7);
 auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(S),B=FPokeMonsterCreatureInstance::CreateFromSpecies(S);TestTrue(TEXT("Existing species learnlist binding"),A.AssignSpeciesMoves()&&B.AssignSpeciesMoves());TestTrue(TEXT("Two individuals remain distinct"),A.InstanceId!=B.InstanceId);
 bool HasDamage=false;for(const auto& Slot:A.GetMoveSlots())if(auto* M=Slot.GetMove().LoadSynchronous())HasDamage|=M->IsConfigured()&&M->Category!=EPokeMonsterMoveCategory::Status&&Slot.GetCurrentPP()>0;
 TestTrue(TEXT("At least one verified playable damaging move at authored test level"),HasDamage);TestEqual(TEXT("Existing four-slot limit"),A.GetMoveSlots().Num(),4);
 const int32 PP=A.GetMoveSlots()[0].GetCurrentPP();TestTrue(TEXT("Existing AP consumption"),A.ConsumeMovePP(0));
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());if(!TestTrue(TEXT("Existing party transport"),E->RestorePersistentState({A,B},{},{})))return false;
 auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());if(!TestNotNull(TEXT("Existing versioned snapshot"),Save))return false;
 TArray<uint8> Bytes;TestTrue(TEXT("Real Unreal memory serialization, no disk writes"),UGameplayStatics::SaveGameToMemory(Save,Bytes));auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));if(!TestTrue(TEXT("Existing save schema accepts new identities"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I)))return false;
 const auto Out=E->GetPlayerParty();if(!TestEqual(TEXT("Both party members preserved"),Out.Num(),2))return false;
 TestEqual(TEXT("Identity survives save/load"),Out[0].InstanceId,A.InstanceId);TestEqual(TEXT("Other identity survives"),Out[1].InstanceId,B.InstanceId);TestEqual(TEXT("AP not refilled"),Out[0].GetMoveSlots()[0].GetCurrentPP(),PP-1);TestEqual(TEXT("Other individual's AP untouched"),Out[1].GetMoveSlots()[0].GetCurrentPP(),PP);
 TestEqual(TEXT("Personal repertoire preserved"),Out[0].GetLearnedMoves().Num(),A.GetLearnedMoves().Num());TestEqual(TEXT("Species binding retained"),Out[0].Species.LoadSynchronous()->GetInternalId(),FName(Row->Name));return true;
}
IMPLEMENT_COMPLEX_AUTOMATION_TEST(FBiomeV11MoveBindings,"PokeMonster.BiomeV11.ProductionMoves",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
void FBiomeV11MoveBindings::GetTests(TArray<FString>& Names,TArray<FString>& Commands)const
{for(const auto* Id:{TEXT("PoisonSting"),TEXT("FuryAttack"),TEXT("Peck"),TEXT("StringShot")}){Names.Add(Id);Commands.Add(Id);}}
bool FBiomeV11MoveBindings::RunTest(const FString& Id)
{
 auto* M=LoadObject<UPokeMonsterMoveData>(nullptr,*(TEXT("/Game/Data/Moves/BiomeV11/DA_")+Id+TEXT(".DA_")+Id));if(!TestNotNull(TEXT("Actual new production move"),M)||!TestTrue(TEXT("Shared effect contract"),M->IsConfigured()))return false;
 TStrongObjectPtr<UPokeMonsterMoveData> Wait(NewObject<UPokeMonsterMoveData>());Wait->InternalId=TEXT("ExplicitBiomeOpponentWait");Wait->DisplayName=FText::FromString(TEXT("Technischer Testgegner wartet"));Wait->Category=EPokeMonsterMoveCategory::Status;Wait->BasePower=0;Wait->MaxPP=100;
 bool Observed=false;
 for(int32 Seed=0;Seed<128&&!Observed;++Seed)
 {
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(BiomeV11QA::Species(TEXT("Habitak")),30),B=FPokeMonsterCreatureInstance::CreateFromSpecies(BiomeV11QA::Species(TEXT("Schiggy")),30);
  A.CurrentHP=A.CalculatedStats.MaxHP=B.CurrentHP=B.CalculatedStats.MaxHP=1000;A.CalculatedStats.Speed=1000;B.CalculatedStats.Speed=1;A.AssignMove(0,M);B.AssignMove(1,Wait.Get());
  TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());Session->ConfigureEffectRules(FPokeMonsterBattleEffectRules::Crystal());Session->InitializeTeams({A},{B},Seed);
  const auto Result=Session->ResolveRound(0,1);if(!TestTrue(TEXT("Existing actual combat resolver"),Result.bSucceeded))return false;int32 Hits=0;for(const auto& Event:Result.Events)Hits+=Event.Type==EPokeMonsterBattleEventType::Damage&&Event.Target==EPokeMonsterBattleSide::B;
  const auto& T=Session->GetState();const bool PP=T.SideA.GetMoveSlots()[0].GetCurrentPP()==M->MaxPP-1;
  if(Id==TEXT("PoisonSting"))Observed=Hits>0&&T.SideB.Status==EPokeMonsterCreatureStatus::Poison&&PP;
  else if(Id==TEXT("FuryAttack"))Observed=Hits>=2&&Hits<=5&&PP;
  else if(Id==TEXT("StringShot"))Observed=Hits==0&&T.SpeedStageB==-1&&PP;
  else Observed=Hits==1&&T.SideB.CurrentHP<1000&&PP;
 }
 TestTrue(TEXT("Actual original-probability effect observed with bounded deterministic seed search"),Observed);return true;
}
#endif
