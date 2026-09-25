#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "PokeMonsterEncounterSubsystem.generated.h"

class AActor;
class APlayerController;
class APokeMonsterPlayerCharacter;
class UPokeMonsterBattlePresenter;
class UPokeMonsterBattleWidget;
class UPokeMonsterEncounterProfile;
struct FPokeMonsterEncounterContext;
struct FPokeMonsterBattleState;

UENUM(BlueprintType)
enum class EPokeMonsterEncounterKind : uint8 { Test, Wild, Trainer };

UENUM(BlueprintType)
enum class EPokeMonsterEncounterOutcome : uint8 { Victory, Defeat, Fled, Cancelled, Captured };

UENUM(BlueprintType)
enum class EPokeMonsterCaptureTransfer : uint8 { None, AddedToTeam, TeamFull };

UENUM(BlueprintType)
enum class EPokeMonsterEncounterSource : uint8 { Scripted, VisibleCreature, Zone, Random };

/** Independent of the visual transition; future wild/trainer encounters use the same contract. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterEncounterStartData
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") FName EncounterId;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") EPokeMonsterEncounterKind Kind = EPokeMonsterEncounterKind::Test;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") EPokeMonsterEncounterSource Source = EPokeMonsterEncounterSource::Scripted;
	/** Empty uses the persistent overworld party. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") TArray<FPokeMonsterCreatureInstance> PlayerTeam;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") TArray<FPokeMonsterCreatureInstance> OpponentTeam;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") int32 RandomSeed = 2026;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Encounter") TObjectPtr<AActor> SourceActor = nullptr;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterEncounterEndData
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly, Category="Encounter") FName EncounterId;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") EPokeMonsterEncounterKind Kind = EPokeMonsterEncounterKind::Test;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") EPokeMonsterEncounterSource Source = EPokeMonsterEncounterSource::Scripted;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") EPokeMonsterEncounterOutcome Outcome = EPokeMonsterEncounterOutcome::Cancelled;
	/** TeamFull is a structured handoff for a future storage system; no creature is discarded. */
	UPROPERTY(BlueprintReadOnly, Category="Encounter") EPokeMonsterCaptureTransfer CaptureTransfer = EPokeMonsterCaptureTransfer::None;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") FPokeMonsterCreatureInstance CapturedCreature;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") TArray<FPokeMonsterCreatureInstance> PlayerTeam;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") TArray<FPokeMonsterCreatureInstance> OpponentTeam;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") int32 Rounds = 0;
	UPROPERTY(BlueprintReadOnly, Category="Encounter") TObjectPtr<AActor> SourceActor = nullptr;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FPokeMonsterEncounterEnded, const FPokeMonsterEncounterEndData&, Result);

/** Keeps the loaded overworld intact while a BattleSession is presented in UMG. */
UCLASS()
class POKEMONSTER_API UPokeMonsterEncounterSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Encounter")
	bool StartEncounter(const FPokeMonsterEncounterStartData& Start, APokeMonsterPlayerCharacter* Player);

	/** Uses existing test species/moves; only the first encounter creates a default player party. */
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Encounter")
	bool StartTestEncounter(APokeMonsterPlayerCharacter* Player, AActor* SourceActor);

	/** Creates the existing development party once. Never revives a defeated party. */
	bool EnsureDevPlayerParty();
	bool StartWildEncounter(const UPokeMonsterEncounterProfile* Profile,
		const FPokeMonsterEncounterContext& Context, EPokeMonsterEncounterSource Source,
		APokeMonsterPlayerCharacter* Player, AActor* SourceActor, int32 Seed, FName EncounterId);
	static bool PrepareWildEncounter(const UPokeMonsterEncounterProfile* Profile,
		const FPokeMonsterEncounterContext& Context, EPokeMonsterEncounterSource Source,
		AActor* SourceActor, int32 Seed, FName EncounterId, FPokeMonsterEncounterStartData& OutStart);

	UFUNCTION(BlueprintPure, Category="PokeMonster|Encounter") bool IsEncounterActive() const { return bActive; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Encounter") const TArray<FPokeMonsterCreatureInstance>& GetPlayerParty() const { return PlayerParty; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Encounter") const FPokeMonsterEncounterEndData& GetLastResult() const { return LastResult; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Encounter") UPokeMonsterBattlePresenter* GetPresenter() const { return Presenter; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Encounter") UPokeMonsterBattleWidget* GetBattleWidget() const { return BattleWidget; }
	UPROPERTY(BlueprintAssignable, Category="PokeMonster|Encounter") FPokeMonsterEncounterEnded OnEncounterEnded;

	virtual void Deinitialize() override;

private:
#if WITH_DEV_AUTOMATION_TESTS
	friend class FPokeMonsterEncounterIntegrationTest;
	friend class FPokeMonsterCaptureTest;
#endif
	static bool BuildTestTeams(TArray<FPokeMonsterCreatureInstance>& Player,
		TArray<FPokeMonsterCreatureInstance>& Opponent);
	static FPokeMonsterEncounterEndData BuildEndData(const FPokeMonsterEncounterStartData& Start,
		const FPokeMonsterBattleState& State);
	UFUNCTION() void HandlePresenterChanged();
	void CompleteEncounter();
	void ReleaseOverworld();

	UPROPERTY(Transient) TArray<FPokeMonsterCreatureInstance> PlayerParty;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterBattlePresenter> Presenter;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterBattleWidget> BattleWidget;
	UPROPERTY(Transient) FPokeMonsterEncounterStartData ActiveStart;
	UPROPERTY(Transient) FPokeMonsterEncounterEndData LastResult;
	UPROPERTY(Transient) TWeakObjectPtr<APokeMonsterPlayerCharacter> ActivePlayer;
	UPROPERTY(Transient) TWeakObjectPtr<APlayerController> ActiveController;
	FTimerHandle CompletionTimer;
	bool bActive = false;
	bool bPreviousMouseCursor = false;
};
