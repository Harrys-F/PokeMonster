#pragma once

#include "CoreMinimal.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "PokeMonsterBattlePresenter.generated.h"

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleMoveView
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly, Category="Battle") FText Name;
	UPROPERTY(BlueprintReadOnly, Category="Battle") FText Type;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 CurrentPP = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 MaxPP = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bEnabled = false;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleCreatureView
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly, Category="Battle") FText Name;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 Level = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 CurrentHP = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 MaxHP = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bKO = false;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleTeamMemberView
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly, Category="Battle") FText Name;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 Level = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 CurrentHP = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 MaxHP = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bActive = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bKO = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bCanSwitch = false;
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterBattleView
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly, Category="Battle") FPokeMonsterBattleCreatureView Player;
	UPROPERTY(BlueprintReadOnly, Category="Battle") FPokeMonsterBattleCreatureView Opponent;
	UPROPERTY(BlueprintReadOnly, Category="Battle") TArray<FPokeMonsterBattleTeamMemberView> PlayerTeam;
	UPROPERTY(BlueprintReadOnly, Category="Battle") TArray<FPokeMonsterBattleTeamMemberView> OpponentTeam;
	UPROPERTY(BlueprintReadOnly, Category="Battle") TArray<FPokeMonsterBattleMoveView> Moves;
	UPROPERTY(BlueprintReadOnly, Category="Battle") FText Status;
	UPROPERTY(BlueprintReadOnly, Category="Battle") FText Log;
	UPROPERTY(BlueprintReadOnly, Category="Battle") int32 Round = 0;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bBusy = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bFinished = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bCaptured = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bMustSwitch = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bPresentationPending = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") bool bCaptureEnabled = false;
	UPROPERTY(BlueprintReadOnly, Category="Battle") FText CaptureDeviceName;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FPokeMonsterBattleViewChanged);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FPokeMonsterBattleRoundPresented, const FPokeMonsterBattleResult&, Result);

/** Presentation boundary. No widget/world dependency; animation completion controls the input lock. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterBattlePresenter : public UObject
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category="Battle UI") bool StartDemo();
	UFUNCTION(BlueprintCallable, Category="Battle UI") bool StartTeamDemo();
	bool InitializeBattle(const FPokeMonsterCreatureInstance& Player, const FPokeMonsterCreatureInstance& Opponent, int32 Seed);
	bool InitializeTeamBattle(const TArray<FPokeMonsterCreatureInstance>& Player,
		const TArray<FPokeMonsterCreatureInstance>& Opponent, int32 Seed, bool bAllowCapture = false);
	UFUNCTION(BlueprintCallable, Category="Battle UI") bool TrySelectMove(int32 Slot);
	UFUNCTION(BlueprintCallable, Category="Battle UI") bool TrySelectCapture();
	UFUNCTION(BlueprintCallable, Category="Battle UI") bool TrySelectSwitch(int32 TeamIndex);
	UFUNCTION(BlueprintCallable, Category="Battle UI") bool ResolveSelection();
	UFUNCTION(BlueprintCallable, Category="Battle UI") void FinishPresentation();
	UFUNCTION(BlueprintPure, Category="Battle UI") const FPokeMonsterBattleView& GetView() const { return View; }
	UFUNCTION(BlueprintPure, Category="Battle UI") const FPokeMonsterBattleResult& GetLastResult() const { return LastResult; }
	/** Read-only battle copies for returning each team member's HP and PP to the caller. */
	const FPokeMonsterBattleState* GetBattleState() const { return Session ? &Session->GetState() : nullptr; }
	UPROPERTY(BlueprintAssignable, Category="Battle UI") FPokeMonsterBattleViewChanged OnChanged;
	UPROPERTY(BlueprintAssignable, Category="Battle UI") FPokeMonsterBattleRoundPresented OnRoundResolved;
private:
	void Refresh();
	void AppendEvents(const FPokeMonsterBattleResult& Result);
	static bool CanUse(const FPokeMonsterCreatureInstance& Creature, int32 Slot);
	int32 ChooseOpponentMove() const;
	int32 NextOpponentSwitch() const;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterBattleSession> Session;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterCaptureDeviceData> TestCaptureDevice;
	UPROPERTY(Transient) FPokeMonsterBattleView View;
	UPROPERTY(Transient) FPokeMonsterBattleResult LastResult;
	TArray<FString> LogLines;
	FString Problem;
	int32 PendingSlot = INDEX_NONE;
	bool bPendingSwitch = false;
	bool bPendingCapture = false;
	bool bBusy = false;
	bool bResolved = false;
};
