#include "PokeMonsterDayNight.h"
#if WITH_EDITOR
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HAL/IConsoleManager.h"
namespace
{
 FAutoConsoleCommandWithWorldArgsAndOutputDevice Command(TEXT("pm.DayNight"),TEXT("VisualV2 PIE only: show | B (75 degrees) | C (85 degrees) | off (original lighting) | on. WorldClock remains authoritative."),
 FConsoleCommandWithWorldArgsAndOutputDeviceDelegate::CreateLambda([](const TArray<FString>& Args,UWorld*,FOutputDevice& Out)
 {
  UWorld* W=nullptr;
  if(GEngine)for(const auto& C:GEngine->GetWorldContexts())if(C.WorldType==EWorldType::PIE&&C.World())
   {if(W){Out.Logf(TEXT("DayNight: genau einen PIE-Test starten."));return;}W=C.World();}
  if(!W||!UPokeMonsterDayNightSubsystem::IsTargetMap(W->GetPackage()->GetName())){Out.Logf(TEXT("DayNight: nur VisualV2 im Editor-PIE."));return;}
  auto* S=W->GetSubsystem<UPokeMonsterDayNightSubsystem>();if(!S||Args.Num()>1)return;
  const FString A=Args.IsEmpty()?TEXT("show"):Args[0].ToLower();
  if(A==TEXT("b"))S->SetNoonVariant(EPokeMonsterNoonSun::B75);
  else if(A==TEXT("c"))S->SetNoonVariant(EPokeMonsterNoonSun::C85);
  else if(A==TEXT("on")||A==TEXT("off"))S->SetCycleEnabled(A==TEXT("on"));
  else if(A!=TEXT("show")){Out.Logf(TEXT("DayNight: show | B | C | on | off; keine dritte Mittagsvariante."));return;}
  const auto V=S->GetLightingSample();Out.Logf(TEXT("DayNight: aktiv=%d, Mittag=%g Grad (B75 Standard / C85 Vergleich), Sonnenhoehe=%.3f, Azimut=%.3f, direkt=%.3f, Fuellung=%.3f, Sterne=%.3f, Himmel=%d"),S->IsCycleEnabled(),UPokeMonsterDayNightSettings::MaximumElevation(S->GetNoonVariant()),V.SunElevation,V.SunAzimuth,V.DirectIntensity,V.FillIntensity,V.Stars,S->IsSkyReady());
 }),ECVF_Cheat);
}
#endif
