#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Engine/GameInstance.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Save/PokeMonsterSaveGame.h"
#include "../Moves/PokeMonsterMoveData.h"
namespace EvolutionV2Tests
{
 auto* Species(const TCHAR* N){return LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),N,N));}
 FPrimaryAssetId Target(const TCHAR* N){return FPrimaryAssetId(TEXT("CreatureSpecies"),N);}
 FPokeMonsterCreatureInstance Creature(const TCHAR* N,int L){auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(N),L);C.AssignSpeciesMoves();return C;}
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionV2Chain,"PokeMonster.EvolutionV2.ChainIdentityMovesAndPP",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionV2Chain::RunTest(const FString&)
{
 using namespace EvolutionV2Tests;using P=UPokeMonsterCreatureProgression;FPokeMonsterEvolutionContext Context;
 auto C=Creature(TEXT("Zunderlauf"),15);auto Separate=Creature(TEXT("Glurak"),36);const auto SeparateId=Separate.InstanceId;const auto SeparateHP=Separate.CurrentHP;
 TestFalse(TEXT("No early evolution"),P::ApplyEvolution(C,Target(TEXT("Glutexo")),Context));
 C.AddExperience(C.GetExperienceToNextLevel());const auto Id=C.InstanceId;const auto XP=C.Experience;const auto Curve=C.GetExperienceGrowthRate();
 C.ConsumeMovePP(0,3);C.CurrentHP-=5;C.Status=EPokeMonsterCreatureStatus::Burn;const auto OldMax=C.GetMaxHP();const auto HP=C.CurrentHP;const auto Slots=C.GetMoveSlots();const auto Known=C.GetLearnedMoves();
 TestFalse(TEXT("Cannot skip middle evolution"),P::ApplyEvolution(C,Target(TEXT("Glurak")),Context));
 TestTrue(TEXT("Glumanda to Glutexo"),P::ApplyEvolution(C,Target(TEXT("Glutexo")),Context));
 TestEqual(TEXT("Same individual"),C.InstanceId,Id);TestEqual(TEXT("Same XP"),C.Experience,XP);TestEqual(TEXT("Historical XP curve retained"),C.GetExperienceGrowthRate(),Curve);
 TestEqual(TEXT("Level retained"),C.Level,16);TestEqual(TEXT("Missing HP retained"),C.GetMaxHP()-C.CurrentHP,OldMax-HP);TestEqual(TEXT("Persistent status retained"),C.Status,EPokeMonsterCreatureStatus::Burn);
 TestEqual(TEXT("Repertoire count retained"),C.GetLearnedMoves().Num(),Known.Num());
 for(int I=0;I<4;++I){TestEqual(TEXT("Active move unchanged"),C.GetMoveSlots()[I].GetMove(),Slots[I].GetMove());TestEqual(TEXT("No free PP"),C.GetMoveSlots()[I].GetCurrentPP(),Slots[I].GetCurrentPP());}
 auto Validated=C;TestTrue(TEXT("Evolved historical XP state restores"),Validated.RestoreIndividualState(C.InstanceId,C.Level,C.Experience,C.CurrentHP,C.GetMoveSlots(),C.Status,C.StatusTurns));
 TestFalse(TEXT("No early Glurak"),P::ApplyEvolution(C,Target(TEXT("Glurak")),Context));
 auto Gain=C.AddExperience(P::ExperienceForLevel(C.GetExperienceGrowthRate(),36)-C.Experience);TestTrue(TEXT("Multiple levels retain valid progression"),Gain.bSucceeded);TestEqual(TEXT("Reached exact second threshold"),C.Level,36);
 while(!C.PendingMoves.IsEmpty())TestTrue(TEXT("Explicitly decline pending level offers before evolution"),C.ResolveMoveLearning(INDEX_NONE));
 TestTrue(TEXT("Glutexo to existing Glurak"),P::ApplyEvolution(C,Target(TEXT("Glurak")),Context));TestEqual(TEXT("Still same individual"),C.InstanceId,Id);
 TestEqual(TEXT("Independent Glurak identity untouched"),Separate.InstanceId,SeparateId);TestEqual(TEXT("Independent Glurak HP untouched"),Separate.CurrentHP,SeparateHP);
 TestEqual(TEXT("Evolution level move offered, not granted"),C.PendingMoves.Num(),1);TestEqual(TEXT("Only four active moves"),C.GetMoveSlots().Num(),4);
 TestTrue(TEXT("Evolution-time learning can be declined"),C.ResolveMoveLearning(INDEX_NONE));TestEqual(TEXT("Decline preserves active PP"),C.GetMoveSlots()[0].GetCurrentPP(),Slots[0].GetCurrentPP());
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionV2Save,"PokeMonster.EvolutionV2.PendingAndEvolvedSaveCompatibility",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionV2Save::RunTest(const FString&)
{
 using namespace EvolutionV2Tests;auto C=Creature(TEXT("Zunderlauf"),16);C.PendingEvolutionTarget=Target(TEXT("Glutexo"));C.LastEvolutionOfferedLevel=16;C.ConsumeMovePP(0,2);
 auto* GI=NewObject<UGameInstance>();auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI);auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI);TestTrue(TEXT("Existing party transport"),E->RestorePersistentState({C},{},{}));
 auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,E);if(!TestNotNull(TEXT("Pending offer snapshot"),Save))return false;
 TestTrue(TEXT("Pending snapshot restores"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I));TestEqual(TEXT("Pending target survives"),E->GetPlayerParty()[0].PendingEvolutionTarget,C.PendingEvolutionTarget);
 TestEqual(TEXT("Offer level survives"),E->GetPlayerParty()[0].LastEvolutionOfferedLevel,16);
 FPokeMonsterEvolutionContext Context;TestTrue(TEXT("Evolution before second snapshot"),UPokeMonsterCreatureProgression::ApplyEvolution(C,Target(TEXT("Glutexo")),Context));
 TestTrue(TEXT("Evolved party"),E->RestorePersistentState({C},{},{}));Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,E);if(!TestNotNull(TEXT("Evolved snapshot"),Save))return false;
 TestTrue(TEXT("Evolved historical XP curve restores"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I));TestEqual(TEXT("XP retained after save"),E->GetPlayerParty()[0].Experience,C.Experience);TestEqual(TEXT("Spent PP retained after save"),E->GetPlayerParty()[0].GetMoveSlots()[0].GetCurrentPP(),C.GetMoveSlots()[0].GetCurrentPP());
 // All supported older schemas still decode a genuine old-species state, with no fabricated offers.
 auto Old=Creature(TEXT("Zunderlauf"),10);E->RestorePersistentState({Old},{},{});Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,E);
 for(int Version=1;Version<=7;++Version){Save->SaveVersion=Version;TestTrue(TEXT("Old schema accepted"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I));TestFalse(TEXT("Old save fabricates no pending evolution"),E->GetPlayerParty()[0].PendingEvolutionTarget.IsValid());}
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionV2Missing,"PokeMonster.EvolutionV2.MissingModelAndCancellationMetadata",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionV2Missing::RunTest(const FString&)
{
 using namespace EvolutionV2Tests;auto C=Creature(TEXT("Bisasam"),16);const auto Id=C.InstanceId;const auto S=C.Species;FPokeMonsterEvolutionContext Context;
 TestFalse(TEXT("Missing target refuses atomic mutation"),UPokeMonsterCreatureProgression::ApplyEvolution(C,Target(TEXT("Bisaknosp")),Context));TestEqual(TEXT("Original model identity retained"),C.Species,S);TestEqual(TEXT("Original individual retained"),C.InstanceId,Id);
 auto Fire=Creature(TEXT("Zunderlauf"),16);Fire.LastEvolutionOfferedLevel=16;Fire.PendingEvolutionTarget=Target(TEXT("Glutexo"));TestTrue(TEXT("Saved pending level offer valid"),Fire.ValidateEvolutionState());Fire.PendingEvolutionTarget=FPrimaryAssetId();TestTrue(TEXT("Declined state valid, same level retry suppressed"),Fire.ValidateEvolutionState());
 Fire.PendingEvolutionTarget=Target(TEXT("Glurak"));TestFalse(TEXT("Corrupt shortcut offer rejected"),Fire.ValidateEvolutionState());
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionV2Rollback,"PokeMonster.EvolutionV2.MissingSaveServiceRollsBack",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionV2Rollback::RunTest(const FString&)
{
 using namespace EvolutionV2Tests;auto* GI=NewObject<UGameInstance>();auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI);
 auto C=Creature(TEXT("Zunderlauf"),16);C.PendingEvolutionTarget=Target(TEXT("Glutexo"));C.LastEvolutionOfferedLevel=16;C.ConsumeMovePP(0,4);C.CurrentHP-=3;
 TestTrue(TEXT("Known original pending party"),E->RestorePersistentState({C},{},{}));
 TestFalse(TEXT("No mutation without successful persistence"),E->ResolveEvolution(C.InstanceId,C.PendingEvolutionTarget,true));
 const auto& Restored=E->GetPlayerParty()[0];TestEqual(TEXT("Old species restored"),Restored.Species,C.Species);TestEqual(TEXT("Individual retained"),Restored.InstanceId,C.InstanceId);TestEqual(TEXT("HP retained"),Restored.CurrentHP,C.CurrentHP);TestEqual(TEXT("Pending offer retained for retry"),Restored.PendingEvolutionTarget,C.PendingEvolutionTarget);TestEqual(TEXT("PP retained"),Restored.GetMoveSlots()[0].GetCurrentPP(),C.GetMoveSlots()[0].GetCurrentPP());
 TestFalse(TEXT("Cancellation also rolls back when persistence unavailable"),E->ResolveEvolution(C.InstanceId,C.PendingEvolutionTarget,false));TestEqual(TEXT("Failed cancel retains offer"),E->GetPlayerParty()[0].PendingEvolutionTarget,C.PendingEvolutionTarget);
 return true;
}
#endif
