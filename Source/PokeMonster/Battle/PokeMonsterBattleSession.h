#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "PokeMonsterBattleLibrary.h"
#include "../Capture/PokeMonsterCaptureDeviceData.h"
#include "PokeMonsterBattleSession.generated.h"

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
	CaptureNotAllowed, InvalidCaptureDevice
};

UENUM(BlueprintType)
enum class EPokeMonsterBattleEventType : uint8
{
	MoveChosen, MoveExecuted, Missed, Damage, SuperEffective, NotVeryEffective, Immune, KnockedOut, BattleEnded,
	SwitchChosen, SwitchedIn, CaptureChosen, CaptureSucceeded, CaptureFailed
};

UENUM(BlueprintType)
enum class EPokeMonsterBattleChoiceType : uint8 { Move, Switch, Capture };

UENUM(BlueprintType)
enum class EPokeMonsterBattleEndReason : uint8 { None, Knockout, Captured };

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

/** Up to six creatures per side, exactly one active. Owns battle copies. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterBattleSession : public UObject
{
	GENERATED_BODY()

public:
	/** Initialize once. Dead/invalid participants are rejected; create another session for a new battle. */
	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Battle")
	FPokeMonsterBattleResult Initialize(const FPokeMonsterCreatureInstance& SideA,
		const FPokeMonsterCreatureInstance& SideB, int32 RandomSeed = 0);

	UFUNCTION(BlueprintCallable, Category = "PokeMonster|Battle")
	FPokeMonsterBattleResult InitializeTeams(const TArray<FPokeMonsterCreatureInstance>& TeamA,
		const TArray<FPokeMonsterCreatureInstance>& TeamB, int32 RandomSeed = 0,
		bool bAllowCapture = false);

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

private:
	FPokeMonsterBattleResult Reject(EPokeMonsterBattleError Error, EPokeMonsterBattleSide Side = EPokeMonsterBattleSide::None) const;

	UPROPERTY(Transient)
	FPokeMonsterBattleState State;

	/** Keep referenced species/moves alive across GC between rounds despite soft instance references. */
	UPROPERTY(Transient)
	TArray<TObjectPtr<UObject>> RetainedData;

	FRandomStream Random;
};
