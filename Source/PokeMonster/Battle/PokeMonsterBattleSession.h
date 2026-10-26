#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "PokeMonsterBattleLibrary.h"
#include "../Capture/PokeMonsterCaptureDeviceData.h"
#include "PokeMonsterBattleSession.generated.h"

class UPokeMonsterItemData;

UENUM(BlueprintType)
enum class EPokeMonsterBattleSide : uint8 { None, A, B };

UENUM(BlueprintType)
enum class EPokeMonsterBattlePhase : uint8 { Uninitialized, AwaitingChoices, AwaitingSwitch, Finished };

UENUM(BlueprintType)
enum class EPokeMonsterBattleError : uint8
{
	None, NotInitialized, AlreadyInitialized, BattleFinished, InvalidCreature, DuplicateCreature,
	MissingSpecies, CreatureFainted, InvalidStats, InvalidSlot, MissingMove, InvalidMove,
	NoPP, InvalidPP, InvalidDamage, RoundLimitReached, InvalidTeam, InvalidSwitch, SwitchRequired,
	CaptureNotAllowed, InvalidCaptureDevice, FleeNotAllowed, InvalidItem, InvalidItemTarget, LearningRequired
};

UENUM(BlueprintType)
enum class EPokeMonsterBattleEventType : uint8
{
	MoveChosen, MoveExecuted, Missed, Damage, SuperEffective, NotVeryEffective, Immune, KnockedOut, BattleEnded,
	SwitchChosen, SwitchedIn, CaptureChosen, CaptureSucceeded, CaptureFailed,
 Recoil, FleeChosen, FleeSucceeded, FleeFailed, ItemChosen, Healed, AttackLowered, EffectFailed, Burned, BurnDamage, ExperienceGained, LevelUp, DefenseLowered, DefenseRaised, SpeedLowered, Seeded, SeedDamage, SeedHeal, EvolutionPending, MoveLearned, MoveUnavailable, StatusApplied, StatusPrevented, StatusDamage, StatusRecovered, StatChanged, Flinched, Confused, ConfusionDamage, Protected, HitCount
};

UENUM(BlueprintType)
enum class EPokeMonsterBattleChoiceType : uint8 { Move, Switch, Capture, Flee, Item };

UENUM(BlueprintType)
enum class EPokeMonsterBattleEndReason : uint8 { None, Knockout, Captured, Escaped, ForcedOut };

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleChoice
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Battle")
	EPokeMonsterBattleChoiceType Type = EPokeMonsterBattleChoiceType::Move;
	/** Move slot (0-3) or team index (0-5), depending on Type. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Battle")
	int32 Index = INDEX_NONE;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Battle")
	TSoftObjectPtr<UPokeMonsterCaptureDeviceData> CaptureDevice;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TSoftObjectPtr<UPokeMonsterItemData> Item;
};

/** Ordered, self-contained event data for a future presentation layer. No UObject/world dependency. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleEvent
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleEventType Type = EPokeMonsterBattleEventType::MoveChosen;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 RoundNumber = 0;
	/** For KO: Source caused the KO, Target fainted. For BattleEnded: Source won. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleSide Source = EPokeMonsterBattleSide::None;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleSide Target = EPokeMonsterBattleSide::None;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	FGuid SourceInstanceId;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	FGuid TargetInstanceId;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 SlotIndex = INDEX_NONE;
	/** For switch events, the selected team index. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 TeamIndex = INDEX_NONE;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	FPrimaryAssetId MoveId;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterMoveCategory Category = EPokeMonsterMoveCategory::Physical;
	/** Actual HP removed, capped at remaining HP (not theoretical overkill). */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 Damage = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	float TypeMultiplier = 1.0f;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 HPBefore = INDEX_NONE;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 HPAfter = INDEX_NONE;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 PPBefore = INDEX_NONE;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 PPAfter = INDEX_NONE;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 HitRoll = INDEX_NONE;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	FPrimaryAssetId CaptureDeviceId;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	float CaptureChance = 0.0f;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 CaptureRoll = INDEX_NONE;
 UPROPERTY(BlueprintReadOnly) FPrimaryAssetId ItemId;
 UPROPERTY(BlueprintReadOnly) int32 RestoredHP=0;
 UPROPERTY(BlueprintReadOnly) int32 FleeThreshold=0;
 UPROPERTY(BlueprintReadOnly) int32 FleeRoll=INDEX_NONE;
 UPROPERTY(BlueprintReadOnly) int32 StageAfter=0;
 UPROPERTY(BlueprintReadOnly) int64 ExperienceAdded=0;
 UPROPERTY(BlueprintReadOnly) int32 LevelsGained=0;
 UPROPERTY(BlueprintReadOnly) FText Information;
 UPROPERTY(BlueprintReadOnly) int32 LevelBefore=0;
 UPROPERTY(BlueprintReadOnly) int32 LevelAfter=0;

};

UENUM(BlueprintType)
enum class EPokeMonsterBattleWeather:uint8 { Clear, Rain, Sun, Sand };

/** New battle-local modifiers; persistent primary ailments stay on the individual. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleVolatileEffects
{
 GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly) int32 SpecialAttack=0;
 UPROPERTY(BlueprintReadOnly) int32 SpecialDefense=0;
 UPROPERTY(BlueprintReadOnly) int32 Accuracy=0;
 UPROPERTY(BlueprintReadOnly) int32 Evasion=0;
 UPROPERTY(BlueprintReadOnly) int32 ConfusionTurns=0;
 UPROPERTY(BlueprintReadOnly) bool bFlinched=false;
 UPROPERTY(BlueprintReadOnly) bool bProtected=false;
 UPROPERTY(BlueprintReadOnly) int32 ProtectStreak=0;
 UPROPERTY(BlueprintReadOnly) int32 LastMoveSlot=INDEX_NONE;
 UPROPERTY(BlueprintReadOnly) int32 DisabledSlot=INDEX_NONE;
 UPROPERTY(BlueprintReadOnly) int32 DisableTurns=0;
 UPROPERTY(BlueprintReadOnly) int32 ChargeSlot=INDEX_NONE;
 UPROPERTY(BlueprintReadOnly) int32 RampageSlot=INDEX_NONE;
 UPROPERTY(BlueprintReadOnly) int32 RampageTurns=0;
 UPROPERTY(BlueprintReadOnly) int32 TrapTurns=0;
 UPROPERTY(BlueprintReadOnly) FGuid TrapSource;
 UPROPERTY(BlueprintReadOnly) FGuid SwitchBlockSource;
 UPROPERTY(BlueprintReadOnly) int32 FocusStage=0;
 UPROPERTY(BlueprintReadOnly) bool bIdentified=false;
 UPROPERTY(BlueprintReadOnly) bool bCursed=false;
 UPROPERTY(BlueprintReadOnly) bool bDestinyBond=false;
 UPROPERTY(BlueprintReadOnly) bool bRage=false;
 UPROPERTY(BlueprintReadOnly) int32 RageCounter=0;
 UPROPERTY(BlueprintReadOnly) bool bJustFrozen=false;
 UPROPERTY(BlueprintReadOnly) int32 RechargeSlot=INDEX_NONE;
 UPROPERTY(BlueprintReadOnly) bool bAirborne=false;
 UPROPERTY() TSoftObjectPtr<UPokeMonsterMoveData> LastExecutedMove;
 UPROPERTY() TSoftObjectPtr<UPokeMonsterMoveData> ForcedMoveData;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleState
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattlePhase Phase = EPokeMonsterBattlePhase::Uninitialized;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	FPokeMonsterCreatureInstance SideA;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	FPokeMonsterCreatureInstance SideB;
	/** Canonical copies of all individual team members, including the active one. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	TArray<FPokeMonsterCreatureInstance> TeamA;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	TArray<FPokeMonsterCreatureInstance> TeamB;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 ActiveIndexA = INDEX_NONE;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 ActiveIndexB = INDEX_NONE;
	/** Number of successfully resolved rounds; rejected choices do not increment it. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 RoundNumber = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleSide Winner = EPokeMonsterBattleSide::None;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleEndReason EndReason = EPokeMonsterBattleEndReason::None;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	bool bCaptureAllowed = false;
 UPROPERTY(BlueprintReadOnly) bool bFleeAllowed=false;
 UPROPERTY(BlueprintReadOnly) bool bTrainerExperience=false;
 UPROPERTY(BlueprintReadOnly) int32 FleeAttempts=0;
 UPROPERTY(BlueprintReadOnly) int32 AttackStageA=0;
 UPROPERTY(BlueprintReadOnly) int32 AttackStageB=0;
 UPROPERTY(BlueprintReadOnly) int32 DefenseStageA=0;
 UPROPERTY(BlueprintReadOnly) int32 DefenseStageB=0;
 UPROPERTY(BlueprintReadOnly) int32 SpeedStageA=0;
 UPROPERTY(BlueprintReadOnly) int32 SpeedStageB=0;
 UPROPERTY(BlueprintReadOnly) bool bSeededA=false;
 UPROPERTY(BlueprintReadOnly) bool bSeededB=false;
 UPROPERTY() TSet<FGuid> ParticipantsA;
 UPROPERTY(BlueprintReadOnly) FPokeMonsterBattleVolatileEffects EffectsA;
 UPROPERTY(BlueprintReadOnly) FPokeMonsterBattleVolatileEffects EffectsB;
 UPROPERTY(BlueprintReadOnly) int32 ScreenTurnsA=0;
 UPROPERTY(BlueprintReadOnly) int32 ScreenTurnsB=0;
 UPROPERTY(BlueprintReadOnly) int32 SafeguardTurnsA=0;
 UPROPERTY(BlueprintReadOnly) int32 SafeguardTurnsB=0;
 UPROPERTY(BlueprintReadOnly) EPokeMonsterBattleWeather Weather=EPokeMonsterBattleWeather::Clear;
 UPROPERTY(BlueprintReadOnly) int32 WeatherTurns=0;

	/** Preserves the exact wild individual at capture time, including HP, PP and level. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	FPokeMonsterCreatureInstance CapturedCreature;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleResult
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	bool bSucceeded = false;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleError Error = EPokeMonsterBattleError::None;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleSide ErrorSide = EPokeMonsterBattleSide::None;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	int32 RoundNumber = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	EPokeMonsterBattleSide Winner = EPokeMonsterBattleSide::None;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Battle")
	TArray<FPokeMonsterBattleEvent> Events;
};

/** Explicit rules for new ailments. Legacy battle initialization does not opt in silently. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleEffectRules
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadOnly) bool bExtendedStatus=false;
 /** Production encounters opt into the user-approved Crystal rules. Legacy arithmetic fixtures do not. */
 UPROPERTY(EditAnywhere,BlueprintReadOnly) bool bCrystal=false;
 /** 0 morning, 1 day, 2 night; an explicit battle context, not a world-light modification. */
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 TimeOfDay=1;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) EPokeMonsterBattleWeather InitialWeather=EPokeMonsterBattleWeather::Clear;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 InitialWeatherTurns=5;
 static FPokeMonsterBattleEffectRules Crystal(){FPokeMonsterBattleEffectRules R;R.bCrystal=R.bExtendedStatus=true;return R;}
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 ParalysisSpeedDivisor=4;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 ParalysisSkipPercent=25;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 FreezeThawPercent=10;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) int32 PoisonDenominator=8;
 bool IsConfigured()const{return uint8(InitialWeather)<=uint8(EPokeMonsterBattleWeather::Sand) && InitialWeatherTurns>=1 && InitialWeatherTurns<=15 && TimeOfDay>=0 && TimeOfDay<=2 && ParalysisSpeedDivisor>=1 && ParalysisSpeedDivisor<=16 && ParalysisSkipPercent>=0 && ParalysisSkipPercent<=100 && FreezeThawPercent>=0 && FreezeThawPercent<=100 && PoisonDenominator>=1 && PoisonDenominator<=64;}
};

/** Up to six creatures per side, exactly one active. Owns battle copies. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterBattleSession : public UObject
{
	GENERATED_BODY()

public:
 bool ConfigureEffectRules(const FPokeMonsterBattleEffectRules& InRules);
	/** Initialize once. Dead/invalid participants are rejected; create another session for a new battle. */
	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Battle")
	FPokeMonsterBattleResult Initialize(const FPokeMonsterCreatureInstance& SideA,
		const FPokeMonsterCreatureInstance& SideB, int32 RandomSeed = 0);

	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Battle")
	FPokeMonsterBattleResult InitializeTeams(const TArray<FPokeMonsterCreatureInstance>& TeamA,
		const TArray<FPokeMonsterCreatureInstance>& TeamB, int32 RandomSeed = 0,
		bool bAllowCapture = false, bool bAllowFlee = false, bool bTrainerExperience = false);

	/** Both selections are validated before committing a round. No external delegates run during resolution. */
	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Battle")
	FPokeMonsterBattleResult ResolveRound(int32 SlotA, int32 SlotB);

	/** A voluntary switch takes this turn; the other side may still use its move. */
	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Battle")
	FPokeMonsterBattleResult ResolveTurn(const FPokeMonsterBattleChoice& ChoiceA,
		const FPokeMonsterBattleChoice& ChoiceB);

	/** Replaces a fainted active creature without consuming another turn. */
	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Battle")
	FPokeMonsterBattleResult ForceSwitch(EPokeMonsterBattleSide Side, int32 TeamIndex);

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Battle")
	const FPokeMonsterBattleState& GetState() const { return State; }

public:
 bool ResolveMoveLearning(int32 TeamIndex, int32 SlotIndex);
 bool HasPendingLearning() const;
 int32 ForcedMoveSlot(EPokeMonsterBattleSide Side) const;
 bool CanSelectMove(EPokeMonsterBattleSide Side,int32 Slot) const;
 bool HasSelectableMove(EPokeMonsterBattleSide Side) const;
 bool CanLeave(EPokeMonsterBattleSide Side) const;
 /** Gen-2-style threshold in [0,256], with checked arithmetic. Attempts includes current attempt. */
 static bool HasUsableMove(const FPokeMonsterCreatureInstance& Creature);
 static int32 EscapeThreshold(int32 PlayerSpeed,int32 EnemySpeed,int32 Attempts);
private:
	FPokeMonsterBattleResult Reject(EPokeMonsterBattleError Error, EPokeMonsterBattleSide Side = EPokeMonsterBattleSide::None) const;

	UPROPERTY(Transient)
	FPokeMonsterBattleState State;

	/** Keep referenced species/moves alive across GC between rounds despite soft instance references. */
	UPROPERTY(Transient)
	TArray<TObjectPtr<UObject>> RetainedData;

	UPROPERTY(Transient) FPokeMonsterBattleEffectRules EffectRules;
	FRandomStream Random;
};
