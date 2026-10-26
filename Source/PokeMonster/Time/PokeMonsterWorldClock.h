#pragma once
#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterWorldClock.generated.h"

UENUM(BlueprintType)
enum class EPokeMonsterDayPhase : uint8 { EarlyMorning, Dawn, Day, Dusk, Night };

/** Half-open phase intervals; starts indexed by EPokeMonsterDayPhase. No lighting/AI consumers yet. */
UCLASS(Config=Game, DefaultConfig)
class POKEMONSTER_API UPokeMonsterWorldClockSettings : public UObject
{
 GENERATED_BODY()
public:
 UPROPERTY(Config, EditAnywhere, Category="World Clock") double RealMinutesPerDay=120.0;
 UPROPERTY(Config, EditAnywhere, Category="World Clock") TArray<int32> PhaseStartMinutes={240,300,420,1080,1200};
 bool IsValidConfiguration() const;
 double GameSecondsPerRealSecond() const { return 1440.0/RealMinutesPerDay; }
 EPokeMonsterDayPhase PhaseAt(double Second) const;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterWorldTime
{
 GENERATED_BODY()
 UPROPERTY(SaveGame, BlueprintReadOnly) int32 Day=1;
 UPROPERTY(SaveGame, BlueprintReadOnly) double SecondsOfDay=32400.0;
 bool IsValid() const;
 int32 Hour() const { return int32(SecondsOfDay/3600.0); }
 int32 Minute() const { return int32(SecondsOfDay/60.0)%60; }
 FText Label() const;
 /** Pure conversion: no OS time, no map clock, no truncation of long frames. */
 bool Advance(double RealSeconds, double DayMinutes=120.0, double Multiplier=1.0);
};

/** Snapshot of existing gameplay guards, not another pause manager. Reasons combine with OR. */
struct POKEMONSTER_API FPokeMonsterClockPauseContext
{
 bool bMenu=false, bDialogue=false, bClassicBattle=false, bLoading=false, bExplicitPause=false, bDebug=false;
 bool IsPaused() const { return bMenu||bDialogue||bClassicBattle||bLoading||bExplicitPause||bDebug; }
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FPokeMonsterDayChanged,int32,Day);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FPokeMonsterPhaseChanged,EPokeMonsterDayPhase,Phase);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FPokeMonsterTimeSet,FPokeMonsterWorldTime,Time);

/** One authority per GameInstance. One matching world pre-tick; no actors/timers per map. */
UCLASS()
class POKEMONSTER_API UPokeMonsterWorldClock : public UGameInstanceSubsystem
{
 GENERATED_BODY()
public:
 virtual void Initialize(FSubsystemCollectionBase& Collection) override;
 virtual void Deinitialize() override;
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") FPokeMonsterWorldTime GetTime() const { return Time; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") int32 GetDay() const { return Time.Day; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") int32 GetHour() const { return Time.Hour(); }
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") int32 GetMinute() const { return Time.Minute(); }
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") EPokeMonsterDayPhase GetPhase() const;
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") double GetDayFraction() const { return Time.SecondsOfDay/86400.0; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") bool IsClockPaused() const;
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") FText GetTimeLabel() const { return Time.Label(); }
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") double GetDebugSpeed() const { return DebugSpeed; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|World Time") double GetRealMinutesPerDay() const;
 UPROPERTY(BlueprintAssignable) FPokeMonsterDayChanged OnDayChanged;
 UPROPERTY(BlueprintAssignable) FPokeMonsterPhaseChanged OnPhaseChanged;
 UPROPERTY(BlueprintAssignable) FPokeMonsterTimeSet OnTimeSet;
 FPokeMonsterClockPauseContext GetPauseContext() const;
 /** Save transaction calls only after all persistent data has validated/committed. Invalid/legacy => Day 1 09:00. */
 void RestoreTime(const FPokeMonsterWorldTime& Saved, bool bHasValidVersion);
#if WITH_EDITOR
 bool SetDevelopmentTime(int32 Day,int32 Hour,int32 Minute);
 bool SetDevelopmentSpeed(double Speed);
 void SetDevelopmentPause(bool Paused) { bDebugPaused=Paused; }
#endif
private:
 UPROPERTY(Transient) FPokeMonsterWorldTime Time;
 const UPokeMonsterWorldClockSettings& Settings() const;
 void WorldTick(UWorld* World,ELevelTick TickType,float DeltaSeconds);
 void NotifyAdvance(FPokeMonsterWorldTime Before);
 FDelegateHandle TickHandle;
 TWeakObjectPtr<UWorld> LastWorld;
 uint64 LastFrame=MAX_uint64;
 double DebugSpeed=1.0;
 bool bDebugPaused=false;
 bool bSkipNextFrame=false;
};
