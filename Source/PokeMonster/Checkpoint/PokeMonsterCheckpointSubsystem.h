#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterCheckpointSubsystem.generated.h"

class APokeMonsterPlayerCharacter;
class APlayerController;
class UPokeMonsterDefeatWidget;
class UPokeMonsterEncounterSubsystem;

/** Stable return location; the map package is stored without a PIE prefix. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCheckpointData
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Checkpoint") FName CheckpointId;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Checkpoint") FName MapPackage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Checkpoint") FVector Location = FVector::ZeroVector;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Checkpoint") FRotator Rotation = FRotator::ZeroRotator;
	bool IsValid() const;
};

/** Owns the active checkpoint and the short defeat transition across worlds. */
UCLASS()
class POKEMONSTER_API UPokeMonsterCheckpointSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;
	bool ActivateCheckpoint(FName Id, const UWorld* World, const FTransform& SafePlayerTransform);
	bool RestoreCheckpoint(const FPokeMonsterCheckpointData& Data);
	const FPokeMonsterCheckpointData& GetActiveCheckpoint() const { return ActiveCheckpoint; }
	bool HasActiveCheckpoint() const { return ActiveCheckpoint.IsValid(); }
	bool IsReturningFromDefeat() const { return bReturning; }
	bool BeginDefeatRecovery(APokeMonsterPlayerCharacter* Player, APlayerController* Controller);
	static FName GetMapPackage(const UWorld* World);
	static bool ResolveReturnTarget(FName CurrentMap, const FPokeMonsterCheckpointData& Active,
		const FTransform& Fallback, FPokeMonsterCheckpointData& OutTarget);
	static bool RestoreTeamAfterDefeat(UPokeMonsterEncounterSubsystem* Encounter);

private:
	void PerformReturn();
	void FinishReturn(UWorld* World);
	void UnlockAfterReturn();
	void HandlePostLoadMap(UWorld* World);
	void ShowOverlay(APlayerController* Controller, const FText& Message);
	void ClearOverlay();
	static bool FindFallback(UWorld* World, FTransform& OutTransform);

	UPROPERTY(Transient) FPokeMonsterCheckpointData ActiveCheckpoint;
	UPROPERTY(Transient) FPokeMonsterCheckpointData PendingTarget;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterDefeatWidget> DefeatWidget;
	TWeakObjectPtr<APokeMonsterPlayerCharacter> ReturningPlayer;
	TWeakObjectPtr<APlayerController> ReturningController;
	FTimerHandle TransitionTimer;
	FDelegateHandle PostLoadMapHandle;
	int32 ReturnAttempts = 0;
	bool bReturning = false;
};
