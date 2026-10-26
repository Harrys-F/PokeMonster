#include "PokeMonsterWorldClock.h"
#if WITH_EDITOR
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "HAL/IConsoleManager.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
namespace
{
 void ClockCommand(const TArray<FString>& Args,UWorld*,FOutputDevice& Out)
 {
  UWorld* W=nullptr;
  if(GEngine)for(const auto& C:GEngine->GetWorldContexts())if(C.WorldType==EWorldType::PIE&&C.World())
   {if(W){Out.Logf(TEXT("WorldClock: genau eine PIE-Sitzung erforderlich."));return;}W=C.World();}
  auto* GI=W?W->GetGameInstance():nullptr;auto* Clock=GI?GI->GetSubsystem<UPokeMonsterWorldClock>():nullptr;
  if(!Clock){Out.Logf(TEXT("WorldClock: nur im Unreal-Editor während PIE verfügbar."));return;}
  const FString Action=Args.IsEmpty()?TEXT("show"):Args[0].ToLower();
  if(Action!=TEXT("show"))
  {
   if(Action!=TEXT("set")&&Action!=TEXT("speed")&&Action!=TEXT("pause")&&Action!=TEXT("resume")&&Action!=TEXT("reset")&&Action!=TEXT("end"))
    {Out.Logf(TEXT("WorldClock: show | set <Tag> <Stunde> <Minute> | speed <0..3600> | pause | resume | reset | end"));return;}
   auto* Save=GI->GetSubsystem<UPokeMonsterSaveSubsystem>();
   // Reuse the established RAM/isolated-slot guard before changing any PIE clock state.
   if(!Save||(!Save->IsPIETestStorageActive()&&!Save->BeginPIEMemoryPreview()))
    {Out.Logf(TEXT("WorldClock: Speicherschutz konnte nicht beginnen; Kampf/Dialog beenden. Keine Änderung."));return;}
   bool Success=false;
   if(Action==TEXT("set")&&Args.Num()==4)
   {int32 Day,Hour,Minute;if(LexTryParseString(Day,*Args[1])&&LexTryParseString(Hour,*Args[2])&&LexTryParseString(Minute,*Args[3]))Success=Clock->SetDevelopmentTime(Day,Hour,Minute);}
   else if(Action==TEXT("speed")&&Args.Num()==2)
   {double Speed;if(LexTryParseString(Speed,*Args[1]))Success=Clock->SetDevelopmentSpeed(Speed);}
   else if(Args.Num()==1)
   {
    if(Action==TEXT("pause")||Action==TEXT("resume")){Clock->SetDevelopmentPause(Action==TEXT("pause"));Success=true;}
    else if(Action==TEXT("reset")){Clock->SetDevelopmentPause(false);Success=Clock->SetDevelopmentSpeed(1);}
    else if(Action==TEXT("end"))
    {Success=Save->IsPIEMemoryPreviewActive()&&Save->EndPIEMemoryPreview();if(Success){Clock->SetDevelopmentPause(false);Clock->SetDevelopmentSpeed(1);}}
   }
   if(!Success){Out.Logf(TEXT("WorldClock: ungültige Argumente oder Testzustand; kein Zeitwechsel. RAM-Schutz bleibt aktiv."));return;}
  }
  const auto T=Clock->GetTime();
  Out.Logf(TEXT("WorldClock: %s | Phase=%s | Tagesfortschritt=%.6f | pausiert=%d | %.3fx | Tagdauer=%.3f Echtminuten. PIE-Testschutz aktiv nach Änderungen."),
   *T.Label().ToString(),*UEnum::GetValueAsString(Clock->GetPhase()),Clock->GetDayFraction(),Clock->IsClockPaused(),Clock->GetDebugSpeed(),Clock->GetRealMinutesPerDay());
 }
 FAutoConsoleCommandWithWorldArgsAndOutputDevice Command(TEXT("pm.WorldClock"),
  TEXT("PIE only. show; set <day> <hour> <minute>; speed <multiplier>; pause; resume; reset; end. Changes use existing RAM save protection."),
  FConsoleCommandWithWorldArgsAndOutputDeviceDelegate::CreateStatic(&ClockCommand),ECVF_Cheat);
}
#endif
