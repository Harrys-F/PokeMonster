#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Time/PokeMonsterWorldClock.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../UI/PokeMonsterOverworldWidget.h"
#include "Components/TextBlock.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"
#include <limits>

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FClockConversionTest,"PokeMonster.WorldClock.ConversionLongFramesAndDrift",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FClockConversionTest::RunTest(const FString&)
{
 FPokeMonsterWorldTime T;TestEqual(TEXT("New day"),T.Day,1);TestEqual(TEXT("New time"),T.Hour(),9);
 T.Advance(5);TestEqual(TEXT("Five seconds = one game minute"),T.Minute(),1);
 T={};T.Advance(300);TestEqual(TEXT("Five minutes = one game hour"),T.Hour(),10);
 T={};T.Advance(7200);TestEqual(TEXT("Two hours = next day"),T.Day,2);TestEqual(TEXT("Same time after full day"),T.SecondsOfDay,32400.0);
 FPokeMonsterWorldTime Split;double Remaining=7200;int N=0;
 while(Remaining>0){double Dt=FMath::Min(Remaining,(++N%4==0)?1.377:1.0/(30+N%90));Split.Advance(Dt);Remaining-=Dt;}
 TestEqual(TEXT("Variable frame day"),Split.Day,T.Day);TestTrue(TEXT("Double-precision drift below one microsecond"),FMath::Abs(Split.SecondsOfDay-T.SecondsOfDay)<1.e-6);
 T={};T.SecondsOfDay=86340;T.Advance(5);TestEqual(TEXT("23:59 to midnight"),T.SecondsOfDay,0.0);TestEqual(TEXT("Day increments"),T.Day,2);
 T={};T.Advance(7200*3.25);TestEqual(TEXT("Several days in a single long frame"),T.Day,4);TestEqual(TEXT("Remaining six hours"),T.Hour(),15);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FClockPhaseTest,"PokeMonster.WorldClock.AllMinutesAndExactPhaseBoundaries",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FClockPhaseTest::RunTest(const FString&)
{
 auto* S=GetDefault<UPokeMonsterWorldClockSettings>();if(!TestTrue(TEXT("Configuration valid"),S->IsValidConfiguration()))return false;TestEqual(TEXT("Default rate twelve"),S->GameSecondsPerRealSecond(),12.0);
 for(int M=0;M<1440;++M)
 {
  const auto Expected=M<240||M>=1200?EPokeMonsterDayPhase::Night:M<300?EPokeMonsterDayPhase::EarlyMorning:M<420?EPokeMonsterDayPhase::Dawn:M<1080?EPokeMonsterDayPhase::Day:EPokeMonsterDayPhase::Dusk;
  TestTrue(TEXT("Every minute covered exactly once"),S->PhaseAt(M*60)==Expected);
 }
 for(int I=0;I<5;++I){double B=S->PhaseStartMinutes[I]*60.;TestTrue(TEXT("Boundary inclusive"),S->PhaseAt(B)==static_cast<EPokeMonsterDayPhase>(I));TestTrue(TEXT("Previous instant exclusive"),S->PhaseAt(B-.001)!=static_cast<EPokeMonsterDayPhase>(I));}
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FClockValidationTest,"PokeMonster.WorldClock.ConfigurationAndInvalidTime",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FClockValidationTest::RunTest(const FString&)
{
 TStrongObjectPtr<UPokeMonsterWorldClockSettings> S(NewObject<UPokeMonsterWorldClockSettings>());
 S->PhaseStartMinutes={240,300,420,1080,1200};S->RealMinutesPerDay=60;TestEqual(TEXT("One source for alternative day rate"),S->GameSecondsPerRealSecond(),24.0);
 FPokeMonsterWorldTime T;T.Advance(300,60);TestEqual(TEXT("Changed rate"),T.Hour(),11);T={};T.Advance(5,120,5);TestEqual(TEXT("5x"),T.Minute(),5);
 S->PhaseStartMinutes[2]=300;TestFalse(TEXT("No duplicate phase boundaries"),S->IsValidConfiguration());S->RealMinutesPerDay=0;TestFalse(TEXT("No zero duration"),S->IsValidConfiguration());
 const double Before=T.SecondsOfDay;for(double Bad:{-1.0,std::numeric_limits<double>::quiet_NaN(),std::numeric_limits<double>::infinity()})TestFalse(TEXT("Bad delta rejected"),T.Advance(Bad));
 TestEqual(TEXT("Bad delta leaves state unchanged"),T.SecondsOfDay,Before);TestFalse(TEXT("Bad day duration"),T.Advance(1,0));TestFalse(TEXT("Bad speed"),T.Advance(1,120,-1));
 T.Day=MAX_int32;T.SecondsOfDay=86399;TestFalse(TEXT("Day overflow rejected"),T.Advance(1));TestEqual(TEXT("Overflow atomic"),T.SecondsOfDay,86399.0);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FClockPauseTest,"PokeMonster.WorldClock.PauseReasonsComposeWithoutReleaseLeaks",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FClockPauseTest::RunTest(const FString&)
{
 for(int Mask=0;Mask<64;++Mask)
 {
  FPokeMonsterClockPauseContext P;P.bMenu=Mask&1;P.bDialogue=Mask&2;P.bClassicBattle=Mask&4;P.bLoading=Mask&8;P.bExplicitPause=Mask&16;P.bDebug=Mask&32;
  TestEqual(TEXT("All combinations OR existing state"),P.IsPaused(),Mask!=0);
  P.bMenu=false;TestEqual(TEXT("Closing menu cannot release another reason"),P.IsPaused(),(Mask&~1)!=0);
 }
 FPokeMonsterClockPauseContext P;TestFalse(TEXT("Fresh context has no stale requests"),P.IsPaused());return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FClockSaveTest,"PokeMonster.WorldClock.ExistingSaveRoundTripAndLegacyAtomicity",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FClockSaveTest::RunTest(const FString&)
{
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
 auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());auto* C=NewObject<UPokeMonsterWorldClock>(GI.Get());
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 auto Pokemon=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,15);Pokemon.AssignSpeciesMoves();Pokemon.ConsumeMovePP(0,2);Pokemon.AddExperience(31);
 E->RestorePersistentState({Pokemon},{},{});
 for(double Seconds:{36000.,75600.,86399.5})
 {
  FPokeMonsterWorldTime Expected;Expected.Day=7;Expected.SecondsOfDay=Seconds;C->RestoreTime(Expected,true);
  auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get(),nullptr,nullptr,C);TArray<uint8> Bytes;
  TestTrue(TEXT("Native memory serialization"),UGameplayStatics::SaveGameToMemory(Save,Bytes));auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));
  C->RestoreTime({},false);TestTrue(TEXT("Existing save transaction"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I,nullptr,nullptr,false,C));
  TestEqual(TEXT("Day restored"),C->GetDay(),7);TestEqual(TEXT("Fractional seconds restored"),C->GetTime().SecondsOfDay,Seconds);
  TestEqual(TEXT("Individual identity preserved"),E->GetPlayerParty()[0].InstanceId,Pokemon.InstanceId);TestEqual(TEXT("Experience preserved"),E->GetPlayerParty()[0].Experience,Pokemon.Experience);TestEqual(TEXT("No PP change"),E->GetPlayerParty()[0].GetMoveSlots()[0].GetCurrentPP(),Pokemon.GetMoveSlots()[0].GetCurrentPP());
  Loaded->SaveVersion=9;TestTrue(TEXT("Legacy nine accepted"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I,nullptr,nullptr,false,C));TestEqual(TEXT("Legacy defaults Day 1"),C->GetDay(),1);TestEqual(TEXT("Legacy defaults 09"),C->GetHour(),9);
  Loaded->SaveVersion=10;Loaded->WorldTime.Day=0;UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I,nullptr,nullptr,false,C);TestEqual(TEXT("Invalid clock fallback only"),C->GetHour(),9);
  C->RestoreTime(Expected,true);Loaded->PlayerTeam[0].Level=0;AddExpectedError(TEXT("Invalid creature in save"),EAutomationExpectedErrorFlags::Contains,1);
  TestFalse(TEXT("Invalid Pokemon rejects whole transaction"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I,nullptr,nullptr,false,C));TestEqual(TEXT("Rejected save cannot rewind clock"),C->GetDay(),7);
 }
 TestEqual(TEXT("Fresh instance normal speed"),NewObject<UPokeMonsterWorldClock>(GI.Get())->GetDebugSpeed(),1.0);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FClockMenuTest,"PokeMonster.WorldClock.ExistingMenuLabelAndLoadRefresh",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FClockMenuTest::RunTest(const FString&)
{
 TStrongObjectPtr<UPokeMonsterOverworldWidget> W(NewObject<UPokeMonsterOverworldWidget>());W->TakeWidget();W->SetMenuOpen(true,EPokeMonsterOverworldMenuSection::Main);
 FPokeMonsterOverworldView V;V.WorldTimeLabel=FText::FromString(TEXT("Tag 1 – 09:00 Uhr"));W->UpdateView(V);
 auto* Label=Cast<UTextBlock>(W->GetWidgetFromName(TEXT("WorldTimeLabel")));if(!TestNotNull(TEXT("Small label inside existing menu"),Label))return false;
 TestEqual(TEXT("Initial time"),Label->GetText().ToString(),V.WorldTimeLabel.ToString());V.WorldTimeLabel=FText::FromString(TEXT("Tag 8 – 00:00 Uhr"));W->UpdateView(V);TestEqual(TEXT("Load/time change invalidates render cache"),Label->GetText().ToString(),V.WorldTimeLabel.ToString());return true;
}
#endif
