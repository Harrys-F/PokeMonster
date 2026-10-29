#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Quest/PokeMonsterQuestSubsystem.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"

namespace EvolutionV3Tests
{
 auto* Species(const TCHAR* Name){return LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),Name,Name));}
 auto Creature(const TCHAR* Name,int32 Level){auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(Name),Level);C.AssignSpeciesMoves();return C;}
 FPrimaryAssetId Garados(){return FPrimaryAssetId(TEXT("CreatureSpecies"),TEXT("Garados"));}
 // Explicit non-production item fixture using existing models. Restore the shared source array
 // before returning; never mark it dirty or invent a real stone evolution for Karpador.
 struct FItemRouteFixture
 {
  UPokeMonsterCreatureSpeciesData* Source=Species(TEXT("Karpador"));
  TArray<FPokeMonsterEvolutionData> Original=Source->GetEvolutions();
  FItemRouteFixture(){FPokeMonsterEvolutionData Rule;Rule.TargetSpecies=Garados();Rule.Trigger=EPokeMonsterEvolutionTrigger::Item;Rule.RequiredItemId=TEXT("TestEvolutionItem");const_cast<TArray<FPokeMonsterEvolutionData>&>(Source->GetEvolutions())={Rule};}
  ~FItemRouteFixture(){const_cast<TArray<FPokeMonsterEvolutionData>&>(Source->GetEvolutions())=Original;}
 };
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionV3Karpador,"PokeMonster.EvolutionV3.KarpadorDataIdentityAndLimits",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionV3Karpador::RunTest(const FString&)
{
 using namespace EvolutionV3Tests;using P=UPokeMonsterCreatureProgression;FPokeMonsterEvolutionContext Context;
 auto C=Creature(TEXT("Karpador"),19);const auto Route=Species(TEXT("Karpador"))->GetEvolutions();
 TestEqual(TEXT("Only canonical route"),Route.Num(),1);if(Route.Num()!=1)return false;
 TestEqual(TEXT("Level20"),Route[0].MinimumLevel,20);TestEqual(TEXT("Existing target"),Route[0].TargetSpecies,Garados());
 TestFalse(TEXT("No early evolution"),P::ApplyEvolution(C,Garados(),Context));
 TestTrue(TEXT("Existing XP threshold"),C.AddExperience(C.GetExperienceToNextLevel()).bSucceeded);
 C.ConsumeMovePP(0,7);C.CurrentHP-=4;C.Status=EPokeMonsterCreatureStatus::Poison;
 const auto Before=C;const auto Other=Creature(TEXT("Garados"),30);const auto Options=P::GetEvolutionOptions(C,Context);
 TestTrue(TEXT("Real target presentation ready"),Options.ContainsByPredicate([](const auto& O){return O.TargetSpecies==Garados()&&O.Readiness==EPokeMonsterEvolutionReadiness::Ready;}));
 TestFalse(TEXT("Wrong species never used"),P::ApplyEvolution(C,FPrimaryAssetId(TEXT("CreatureSpecies"),TEXT("Glurak")),Context));
 TestTrue(TEXT("Actual existing evolution path"),P::ApplyEvolution(C,Garados(),Context));
 TestEqual(TEXT("One individual"),C.InstanceId,Before.InstanceId);TestEqual(TEXT("Same XP"),C.Experience,Before.Experience);TestEqual(TEXT("Same level"),C.Level,20);
 TestEqual(TEXT("Missing HP preserved"),C.GetMaxHP()-C.CurrentHP,4);TestEqual(TEXT("Poison retained"),C.Status,Before.Status);
 TestEqual(TEXT("No PP refill"),C.GetMoveSlots()[0].GetCurrentPP(),Before.GetMoveSlots()[0].GetCurrentPP());TestEqual(TEXT("Repertoire retained"),C.GetLearnedMoves().Num(),Before.GetLearnedMoves().Num());
 TestTrue(TEXT("Only current target-level Bite offered"),C.PendingMoves.Num()==1&&C.PendingMoves[0].ToString().Contains(TEXT("Bite")));
 TestEqual(TEXT("Four active slots"),C.GetMoveSlots().Num(),4);TestTrue(TEXT("Learning can be declined"),C.ResolveMoveLearning(INDEX_NONE));
 TestEqual(TEXT("Separate Garados not changed"),Other.Level,30);TestNotEqual(TEXT("Distinct identity"),Other.InstanceId,C.InstanceId);
 auto K=Creature(TEXT("Karpador"),20);K.CurrentHP=0;TestTrue(TEXT("Pure data transfer also preserves KO"),P::ApplyEvolution(K,Garados(),Context));TestEqual(TEXT("No resurrection"),K.CurrentHP,0);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionV3ItemSave,"PokeMonster.EvolutionV3.ItemOfferSaveAndLegacyCompatibility",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionV3ItemSave::RunTest(const FString&)
{
 using namespace EvolutionV3Tests;FItemRouteFixture ScopedFixture;
 auto* GI=NewObject<UGameInstance>();auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI);auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI);
 auto* Item=LoadObject<UPokeMonsterItemData>(nullptr,TEXT("/Game/Data/Items/DA_TestEvolutionItem"));I->AddItem(Item,2);
 auto C=Creature(TEXT("Karpador"),20);C.PendingEvolutionTarget=Garados();C.PendingEvolutionItemId=Item->GetInternalId();C.LastEvolutionOfferedLevel=C.Level;
 TestTrue(TEXT("Item-specific metadata valid"),C.ValidateEvolutionState());auto Bad=C;Bad.PendingEvolutionItemId=TEXT("WrongItem");TestFalse(TEXT("Wrong item metadata rejected"),Bad.ValidateEvolutionState());
 TestTrue(TEXT("Original party transport"),E->RestorePersistentState({C},{},{}));auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI);if(!TestNotNull(TEXT("Existing native snapshot"),Save))return false;
 TArray<uint8> Bytes;TestTrue(TEXT("Serialize pending item offer"),UGameplayStatics::SaveGameToMemory(Save,Bytes));auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));
 TestTrue(TEXT("Restore pending item offer"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I));TestEqual(TEXT("Correct selected item survives"),E->GetPlayerParty()[0].PendingEvolutionItemId,Item->GetInternalId());TestEqual(TEXT("Offer reserves no item"),I->GetQuantity(Item),2);
 TestFalse(TEXT("Missing registered save service refuses commit"),E->ResolveEvolution(C.InstanceId,Garados(),true));TestEqual(TEXT("Failed commit retains source"),E->GetPlayerParty()[0].Species,C.Species);TestEqual(TEXT("Failed commit retains stock"),I->GetQuantity(Item),2);
 TestFalse(TEXT("No valid inventory service prevents preparation"),E->PrepareItemEvolutionOffer(Item,0)!=INDEX_NONE);
 auto Old=Creature(TEXT("Zunderlauf"),16);Old.PendingEvolutionTarget=FPrimaryAssetId(TEXT("CreatureSpecies"),TEXT("Glutexo"));Old.LastEvolutionOfferedLevel=16;E->RestorePersistentState({Old},{},{});Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI);
 for(int Version=1;Version<=10;++Version)
 {
  Save->SaveVersion=Version;TestTrue(TEXT("All supported old schemas remain readable"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I));
  TestTrue(TEXT("No invented legacy item selection"),E->GetPlayerParty()[0].PendingEvolutionItemId.IsNone());
 }
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionV3Gates,"PokeMonster.EvolutionV3.ExistingQuestLocationActionAndTimeGates",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionV3Gates::RunTest(const FString&)
{
 auto* GI=NewObject<UGameInstance>();auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI);auto* Q=NewObject<UPokeMonsterQuestSubsystem>(GI);
 auto* Quest=NewObject<UPokeMonsterQuestData>();Quest->InternalId=TEXT("V3_TEST_Quest");Quest->DisplayName=FText::FromString(TEXT("Technical fixture only"));Quest->CompletionFlag=TEXT("V3_TEST_TrialDone");
 FPokeMonsterQuestObjective Step;Step.Type=EPokeMonsterQuestObjectiveType::WorldFlagSet;Step.TargetId=TEXT("V3_TEST_Action");Step.Description=FText::FromString(TEXT("Not an authored gameplay trial"));Quest->Objectives={Step};
 TestTrue(TEXT("Reuse existing quest"),Q->StartQuest(Quest));
 FPokeMonsterEvolutionData Rule;Rule.TargetSpecies=EvolutionV3Tests::Garados();Rule.Trigger=EPokeMonsterEvolutionTrigger::SpecialInteraction;
 // 42 is only a test boundary, never assigned to Kadabra/Maschock/Georok/Alpollo data.
 Rule.MinimumLevel=42;Rule.RequiredLocationId=TEXT("V3_TEST_Place");Rule.RequiredActionId=Quest->CompletionFlag;Rule.RequiredStartMinute=1200;Rule.RequiredEndMinute=240;
 FPokeMonsterEvolutionContext Context;Context.Trigger=EPokeMonsterEvolutionTrigger::SpecialInteraction;Context.LocationId=Rule.RequiredLocationId;Context.MinuteOfDay=1300;
 using P=UPokeMonsterCreatureProgression;
 TestFalse(TEXT("Uncompleted action blocks"),P::IsEvolutionEligible(Rule,42,Context));
 E->MarkEncounterCompleted(Step.TargetId);Q->RefreshProgress(E,nullptr);TestEqual(TEXT("Existing quest completion"),Q->GetStatus(Quest->InternalId),EPokeMonsterQuestStatus::Completed);
 if(E->IsEncounterCompleted(Quest->CompletionFlag))Context.ActionId=Quest->CompletionFlag;
 TestFalse(TEXT("Minimum level still required"),P::IsEvolutionEligible(Rule,41,Context));TestTrue(TEXT("Level AND place AND completed action AND time"),P::IsEvolutionEligible(Rule,42,Context));
 Context.LocationId=TEXT("Wrong");TestFalse(TEXT("Wrong place"),P::IsEvolutionEligible(Rule,42,Context));Context.LocationId=Rule.RequiredLocationId;Context.MinuteOfDay=240;TestFalse(TEXT("Time boundary"),P::IsEvolutionEligible(Rule,42,Context));
 Context.MinuteOfDay=1300;Rule.MinimumFriendship=220;TestFalse(TEXT("No invented friendship value"),P::IsEvolutionEligible(Rule,42,Context));Context.Friendship=220;TestTrue(TEXT("Existing combined friendship gate"),P::IsEvolutionEligible(Rule,42,Context));
 return true;
}
#endif
