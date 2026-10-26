#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../UI/PokeMonsterExperienceView.h"
#include "../UI/PokeMonsterOverworldWidget.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "../UI/PokeMonsterControllerInput.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "Components/ProgressBar.h"
#include "Components/TextBlock.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"
namespace ExperienceViewTests
{
 using P=UPokeMonsterCreatureProgression;using V=FPokeMonsterExperienceView;
 UPokeMonsterCreatureSpeciesData* Species(const TCHAR* Id){return LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),Id,Id));}
 FPokeMonsterCreatureInstance Creature(int32 Level=15){auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(Species(TEXT("Zunderlauf")),Level);C.AssignSpeciesMoves();return C;}
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FExperienceBoundariesTest,"PokeMonster.UI.Experience.AllCurveBoundaries",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FExperienceBoundariesTest::RunTest(const FString&)
{
 using namespace ExperienceViewTests;
 for(auto Rate:{EPokeMonsterGrowthRate::Fast,EPokeMonsterGrowthRate::MediumFast,EPokeMonsterGrowthRate::MediumSlow,EPokeMonsterGrowthRate::Slow,EPokeMonsterGrowthRate::Erratic,EPokeMonsterGrowthRate::Fluctuating})
 {
  for(int32 Level:{1,15,99})
  {
   const int64 Floor=P::ExperienceForLevel(Rate,Level),Next=P::ExperienceForLevel(Rate,Level+1),Need=Next-Floor;
   for(int64 Offset:{int64(0),Need/2,Need-1})
   {
    const auto X=V::Calculate(Rate,Level,Floor+Offset);TestTrue(TEXT("Valid actual curve"),X.bValid);
    TestEqual(TEXT("Total is not mistaken for per-level progress"),X.Earned,Offset);TestEqual(TEXT("Required is difference of thresholds"),X.Required,Need);
    TestEqual(TEXT("Missing experience"),X.Remaining,Need-Offset);TestTrue(TEXT("Finite bounded bar"),FMath::IsFinite(X.Fraction)&&X.Fraction>=0&&X.Fraction<1);
   }
  }
  auto Max=V::Calculate(Rate,P::MaxLevel,P::ExperienceForLevel(Rate,P::MaxLevel));
  TestTrue(TEXT("Configured maximum level"),Max.bValid&&Max.bMaximumLevel);TestEqual(TEXT("Full MAX bar"),Max.Fraction,1.f);TestEqual(TEXT("No negative remaining or division by zero"),Max.Remaining,int64(0));TestTrue(TEXT("MAX text"),Max.ProgressText().ToString().Contains(TEXT("MAX")));
 }
 TestFalse(TEXT("Unknown curve explicit unavailable"),V::Calculate(static_cast<EPokeMonsterGrowthRate>(255),15,1000).bValid);
 TestFalse(TEXT("Inconsistent total not silently displayed as valid"),V::Calculate(EPokeMonsterGrowthRate::MediumFast,15,2).bValid);
 TestFalse(TEXT("No level 101 threshold"),V::Calculate(EPokeMonsterGrowthRate::MediumFast,101,1000000).bValid);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FExperienceProgressionTest,"PokeMonster.UI.Experience.MultilevelLearningAndEvolution",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FExperienceProgressionTest::RunTest(const FString&)
{
 using namespace ExperienceViewTests;auto C=Creature();C.Experience=P::ExperienceForLevel(C.GetExperienceGrowthRate(),16)-1;
 const auto Before=V::FromCreature(C);C.AddExperience(P::ExperienceForLevel(C.GetExperienceGrowthRate(),36)+123-C.Experience);
 const auto After=V::FromCreature(C);TestEqual(TEXT("Multiple level-up target"),After.Level,36);TestEqual(TEXT("Remainder retained"),After.Earned,int64(123));TestTrue(TEXT("Move learning remains pending"),!C.PendingMoves.IsEmpty());
 for(int I=0;I<=100;++I){auto X=V::Interpolate(Before,After,I/100.f);TestTrue(TEXT("Every animation sample respects actual curve boundaries"),X.bValid&&X.Total>=Before.Total&&X.Total<=After.Total&&X.Remaining>=0);}
 TestEqual(TEXT("Exact final level and total"),V::Interpolate(Before,After,1).Total,C.Experience);
 // Existing evolution transaction keeps the individual's growth override and spent PP.
 while(!C.PendingMoves.IsEmpty())C.ResolveMoveLearning(INDEX_NONE);
 const int PP=C.GetMoveSlots()[0].GetCurrentPP();const int64 XP=C.Experience;
 TestTrue(TEXT("Existing evolution route"),P::ApplyEvolution(C,FPrimaryAssetId(TEXT("CreatureSpecies"),TEXT("Glutexo")),FPokeMonsterEvolutionContext()));
 TestEqual(TEXT("Evolution preserves display total"),V::FromCreature(C).Total,XP);TestEqual(TEXT("Evolution preserves growth curve"),V::FromCreature(C).Growth,Before.Growth);TestEqual(TEXT("No PP refill"),C.GetMoveSlots()[0].GetCurrentPP(),PP);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FExperienceSaveTest,"PokeMonster.UI.Experience.ExistingSaveRoundTrip",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FExperienceSaveTest::RunTest(const FString&)
{
 using namespace ExperienceViewTests;TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
 auto C=Creature();C.AddExperience(C.GetExperienceToNextLevel()/2);const auto Before=V::FromCreature(C);
 TestTrue(TEXT("Existing persistent party"),E->RestorePersistentState({C,Creature(30)},{},{}));auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());
 TArray<uint8> Bytes;TestTrue(TEXT("Existing schema serialized in memory"),UGameplayStatics::SaveGameToMemory(Save,Bytes));
 auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));TestTrue(TEXT("Existing schema restores without new XP fields"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I));
 auto After=V::FromCreature(E->GetPlayerParty()[0]);TestEqual(TEXT("Same cumulative XP"),Before.Total,After.Total);TestEqual(TEXT("Same in-level XP"),Before.Earned,After.Earned);TestEqual(TEXT("Same missing XP"),Before.Remaining,After.Remaining);TestEqual(TEXT("Same bar"),Before.Fraction,After.Fraction);
 E->ReorderParty(C.InstanceId,1);TestEqual(TEXT("XP follows individual after team sort"),V::FromCreature(E->GetPlayerParty()[1]).Total,Before.Total);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FExperienceInfoWidgetTest,"PokeMonster.UI.Experience.InfoReadOnlyRefreshAndInput",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FExperienceInfoWidgetTest::RunTest(const FString&)
{
 using namespace ExperienceViewTests;TStrongObjectPtr<UPokeMonsterOverworldWidget> W(NewObject<UPokeMonsterOverworldWidget>());W->TakeWidget();FPokeMonsterOverworldView View;
 auto C=Creature();auto& Row=View.Team.AddDefaulted_GetRef();Row.InstanceId=C.InstanceId;Row.Name=FText::FromString(TEXT("Glumanda"));Row.Level=C.Level;Row.Experience=V::FromCreature(C);
 auto& Other=View.Team.AddDefaulted_GetRef();Other.InstanceId=FGuid::NewGuid();Other.Name=FText::FromString(TEXT("Reserve"));Other.Level=100;Other.Experience=V::Calculate(C.GetExperienceGrowthRate(),100,P::ExperienceForLevel(C.GetExperienceGrowthRate(),100));
 W->UpdateView(View);W->SetMenuOpen(true,EPokeMonsterOverworldMenuSection::Moves);
 auto Press=[&](FKey K){return W->NativeOnPreviewKeyDown(FGeometry(),FKeyEvent(K,FModifierKeysState(),0,false,0,0)).IsEventHandled();};
 TestTrue(TEXT("Existing B selects status creature"),Press(PokeMonsterControllerInput::Confirm()));TestNotNull(TEXT("Existing info screen contains XP bar"),W->ExperienceBar.Get());
 C.AddExperience(C.GetExperienceToNextLevel()/2);View.Team[0].Experience=V::FromCreature(C);W->UpdateView(View);
 TestEqual(TEXT("Same-level XP invalidates render cache"),W->ExperienceBar->GetPercent(),View.Team[0].Experience.Fraction);
 Press(PokeMonsterControllerInput::Cancel());Press(EKeys::Gamepad_DPad_Down);Press(PokeMonsterControllerInput::Confirm());TestEqual(TEXT("Selecting another individual updates MAX bar"),W->ExperienceBar->GetPercent(),1.f);
 TestFalse(TEXT("Status remains read-only"),W->bMoveMasterMode);W->SetBattleVisible(true);TestFalse(TEXT("Battle blocks status input"),Press(PokeMonsterControllerInput::Confirm()));
 PokeMonsterControllerInput::ObserveKey(EKeys::E);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FExperienceBattleWidgetTest,"PokeMonster.UI.Experience.BattleAwardPresentationAndSwitch",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FExperienceBattleWidgetTest::RunTest(const FString&)
{
 using namespace ExperienceViewTests;TStrongObjectPtr<UPokeMonsterBattlePresenter> PUI(NewObject<UPokeMonsterBattlePresenter>());
 auto C=Creature();C.Experience=P::ExperienceForLevel(C.GetExperienceGrowthRate(),16)-1;auto Enemy=Creature(1);Enemy.CurrentHP=1;
 auto* Scratch=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Scratch.DA_Scratch"));C.AssignMove(0,Scratch);
 auto Other=Creature(25);Other.AddExperience(20);
 TestTrue(TEXT("Real existing battle initializes"),PUI->InitializeTeamBattle({C,Other},{Enemy},71));
 TStrongObjectPtr<UPokeMonsterBattleWidget> W(NewObject<UPokeMonsterBattleWidget>());W->SetEncounterOverlay(true);W->TakeWidget();W->SetPresenter(PUI.Get());
 TestNotNull(TEXT("Discreet player XP bar"),W->PlayerExperienceBar.Get());TestEqual(TEXT("Initial active creature XP"),W->GetPresentedExperience().Total,C.Experience);
 TestTrue(TEXT("Actual attack selected"),PUI->TrySelectMove(0));TestTrue(TEXT("Actual turn resolves"),PUI->ResolveSelection());
 auto Actions=UPokeMonsterBattlePresentationPlan::BuildActions(PUI->GetLastResult());int XPIndex=INDEX_NONE;
 for(int N=0;N<Actions.Num();++N)if(Actions[N].bExperienceGain){XPIndex=N;break;}
 if(!TestTrue(TEXT("Real XP gain reaches presentation"),XPIndex!=INDEX_NONE))return false;
 W->ActionIndex=XPIndex;W->BeginAction();TestTrue(TEXT("Dedicated presentation phase, no game-state award"),W->PresentationPhase==UPokeMonsterBattleWidget::EPresentationPhase::Experience);
 TestEqual(TEXT("Animation starts at actual pre-award XP"),W->ExperienceBefore.Total,C.Experience);TestTrue(TEXT("Level boundary carried by event"),W->ExperienceAfter.Level==16&&W->ExperienceAfter.Total>C.Experience);
 W->AdvancePhase();TestEqual(TEXT("Animation ends at exact awarded total"),W->GetPresentedExperience().Total,PUI->GetView().Player.Experience.Total);
 W->ResetVisuals();PUI->FinishPresentation();
 auto Rival=Creature(50);Rival.AssignMove(0,LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Growl.DA_Growl")));
 TestTrue(TEXT("Independent switch scenario"),PUI->InitializeTeamBattle({C,Other},{Rival},71));W->Refresh();
 TestTrue(TEXT("Select existing team switch"),PUI->TrySelectSwitch(1));PUI->ResolveSelection();W->EndPresentation();
 TestEqual(TEXT("After switch XP belongs to new active individual"),W->GetPresentedExperience().Total,Other.Experience);TestEqual(TEXT("After switch level"),W->GetPresentedExperience().Level,Other.Level);
 return true;
}
#endif
