#include "PokeMonsterWorldClock.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "Misc/App.h"
#include "UObject/StrongObjectPtr.h"
#include "Kismet/GameplayStatics.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"

bool UPokeMonsterWorldClockSettings::IsValidConfiguration() const
{
 if(!FMath::IsFinite(RealMinutesPerDay)||RealMinutesPerDay<=0||PhaseStartMinutes.Num()!=5)return false;
 for(int32 I=0;I<5;++I)if(PhaseStartMinutes[I]<0||PhaseStartMinutes[I]>=1440||(I&&PhaseStartMinutes[I]<=PhaseStartMinutes[I-1]))return false;
 return true;
}
EPokeMonsterDayPhase UPokeMonsterWorldClockSettings::PhaseAt(double Second) const
{
 for(int32 I=PhaseStartMinutes.Num()-1;I>=0;--I)
  if(Second>=PhaseStartMinutes[I]*60.0)return static_cast<EPokeMonsterDayPhase>(I);
 return EPokeMonsterDayPhase::Night;
}
bool FPokeMonsterWorldTime::IsValid() const { return Day>=1&&FMath::IsFinite(SecondsOfDay)&&SecondsOfDay>=0&&SecondsOfDay<86400; }
FText FPokeMonsterWorldTime::Label() const { return FText::FromString(FString::Printf(TEXT("Tag %d – %02d:%02d Uhr"),Day,Hour(),Minute())); }
bool FPokeMonsterWorldTime::Advance(double RealSeconds,double DayMinutes,double Multiplier)
{
 if(!IsValid()||!FMath::IsFinite(RealSeconds)||RealSeconds<0||!FMath::IsFinite(DayMinutes)||DayMinutes<=0||!FMath::IsFinite(Multiplier)||Multiplier<0)return false;
 const double Total=SecondsOfDay+RealSeconds*(1440.0/DayMinutes)*Multiplier;
 if(!FMath::IsFinite(Total)||FMath::FloorToDouble(Total/86400.0)>double(MAX_int32-Day))return false;
 const int32 Days=int32(FMath::FloorToDouble(Total/86400.0));
 Day+=Days;SecondsOfDay=FMath::Fmod(Total,86400.0);return true;
}
const UPokeMonsterWorldClockSettings& UPokeMonsterWorldClock::Settings() const
{
 const auto* Config=GetDefault<UPokeMonsterWorldClockSettings>();
 // Reject a broken config as a whole; never create gaps/overlaps or divide by zero.
 static TStrongObjectPtr<UPokeMonsterWorldClockSettings> Defaults([]{auto* S=NewObject<UPokeMonsterWorldClockSettings>();S->RealMinutesPerDay=120.0;S->PhaseStartMinutes={240,300,420,1080,1200};return S;}());
 return Config->IsValidConfiguration()?*Config:*Defaults.Get();
}
void UPokeMonsterWorldClock::Initialize(FSubsystemCollectionBase& Collection)
{
 Super::Initialize(Collection);
 TickHandle=FWorldDelegates::OnWorldPreActorTick.AddUObject(this,&UPokeMonsterWorldClock::WorldTick);
}
void UPokeMonsterWorldClock::Deinitialize()
{
 FWorldDelegates::OnWorldPreActorTick.Remove(TickHandle);LastWorld.Reset();Super::Deinitialize();
}
EPokeMonsterDayPhase UPokeMonsterWorldClock::GetPhase() const { return Settings().PhaseAt(Time.SecondsOfDay); }
double UPokeMonsterWorldClock::GetRealMinutesPerDay() const { return Settings().RealMinutesPerDay; }
FPokeMonsterClockPauseContext UPokeMonsterWorldClock::GetPauseContext() const
{
 FPokeMonsterClockPauseContext P;P.bDebug=bDebugPaused;
 const auto* GI=GetGameInstance();const auto* W=GetWorld();
 const auto* PC=W?Cast<APokeMonsterOverworldPlayerController>(W->GetFirstPlayerController()):nullptr;
 P.bLoading=!W||!W->HasBegunPlay()||!PC||!PC->GetPawn();
 P.bMenu=PC&&(PC->IsMenuOpen()||PC->GetEvolutionWidget()!=nullptr);
 P.bExplicitPause=W&&UGameplayStatics::IsGamePaused(W);
 if(GI)
 {
  const auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>();
  P.bClassicBattle=E&&E->IsEncounterActive(); // All command battles suspend ordinary exploration, including optional WorldBattle.
  const auto* D=GI->GetSubsystem<UPokeMonsterDialogueSubsystem>();P.bDialogue=D&&D->IsDialogueActive();
  const auto* S=GI->GetSubsystem<UPokeMonsterSaveSubsystem>();const auto* C=GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>();
  P.bLoading|=(S&&S->IsLoadInProgress())||(C&&C->IsReturningFromDefeat());
 }
 return P;
}
bool UPokeMonsterWorldClock::IsClockPaused() const { return GetPauseContext().IsPaused(); }
void UPokeMonsterWorldClock::WorldTick(UWorld* World,ELevelTick TickType,float DeltaSeconds)
{
 if(!World||!World->IsGameWorld()||World->GetGameInstance()!=GetGameInstance()||LastFrame==GFrameCounter)return;
 LastFrame=GFrameCounter;
 // Loading does not accumulate wall time; discard the first frame of each new world.
 if(LastWorld.Get()!=World){LastWorld=World;return;}
 if(bSkipNextFrame){bSkipNextFrame=false;return;}
 if(IsClockPaused())return;
 const auto Before=Time;
 // App delta is real frame duration: unaffected by gameplay time dilation/world delta clamping.
 if(Time.Advance(FApp::GetDeltaTime(),GetRealMinutesPerDay(),DebugSpeed))NotifyAdvance(Before);
}
void UPokeMonsterWorldClock::NotifyAdvance(FPokeMonsterWorldTime Before)
{
 const double Start=(Before.Day-1)*86400.0+Before.SecondsOfDay,End=(Time.Day-1)*86400.0+Time.SecondsOfDay;
 // Deliver every crossed boundary, even when a long frame starts/ends in the same phase.
 for(int64 Day=Before.Day;Day<=Time.Day;++Day)
 {
  const double Midnight=(Day-1)*86400.0;
  if(Midnight>Start&&Midnight<=End)OnDayChanged.Broadcast(int32(Day));
  for(int32 I=0;I<5;++I)
  {
   const double Boundary=Midnight+Settings().PhaseStartMinutes[I]*60.0;
   if(Boundary>Start&&Boundary<=End)OnPhaseChanged.Broadcast(static_cast<EPokeMonsterDayPhase>(I));
  }
 }
}
void UPokeMonsterWorldClock::RestoreTime(const FPokeMonsterWorldTime& Saved,bool bHasValidVersion)
{
 bSkipNextFrame=true;
 const auto Before=Time;Time=bHasValidVersion&&Saved.IsValid()?Saved:FPokeMonsterWorldTime();
 // Runtime speed/pause are session controls and are neither loaded nor serialized.
 if(Before.Day!=Time.Day)OnDayChanged.Broadcast(Time.Day);
 if(Settings().PhaseAt(Before.SecondsOfDay)!=GetPhase())OnPhaseChanged.Broadcast(GetPhase());
 OnTimeSet.Broadcast(Time);
}
#if WITH_EDITOR
bool UPokeMonsterWorldClock::SetDevelopmentTime(int32 Day,int32 Hour,int32 Minute)
{
 if(!GetWorld()||GetWorld()->WorldType!=EWorldType::PIE||Day<1||Hour<0||Hour>23||Minute<0||Minute>59)return false;
 FPokeMonsterWorldTime Target;Target.Day=Day;Target.SecondsOfDay=Hour*3600.0+Minute*60.0;RestoreTime(Target,true);return true;
}
bool UPokeMonsterWorldClock::SetDevelopmentSpeed(double Speed)
{
 if(!GetWorld()||GetWorld()->WorldType!=EWorldType::PIE||!FMath::IsFinite(Speed)||Speed<=0||Speed>3600)return false;
 DebugSpeed=Speed;return true;
}
#endif
