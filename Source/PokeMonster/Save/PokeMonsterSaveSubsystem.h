#pragma once

#include "CoreMinimal.h"
#include "Engine/EngineBaseTypes.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterSaveGame.h"
#include "PokeMonsterSaveSubsystem.generated.h"

struct FPokeMonsterCreatureInstance;
class UPokeMonsterInventorySubsystem;
class UPokeMonsterEncounterSubsystem;
class UPokeMonsterCheckpointSubsystem;
class UPokeMonsterQuestSubsystem;
class APokeMonsterPlayerCharacter;

/** Existing native snapshot transport, with independent manual and defeat-recovery slots. */
UCLASS()
class POKEMONSTER_API UPokeMonsterSaveSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	static const FString DevSlotName;
 static const FString RecoverySlotName;
 virtual void Initialize(FSubsystemCollectionBase& Collection) override;
 virtual void Deinitialize() override;
 /** Recovery never overwrites a manually saved game. */
 bool SaveRecoveryGame();
 /** Validated internal learning/evolution/master commits share the existing automatic slot. */
 bool SaveProgressGame();
 UFUNCTION(BlueprintCallable, Category="PokeMonster|Save") bool LoadRecoveryGame();
 UFUNCTION(BlueprintPure, Category="PokeMonster|Save") bool HasRecoveryGame() const;
 UFUNCTION(BlueprintPure, Category="PokeMonster|Save") bool IsLoadInProgress() const { return PendingLoad != nullptr; }
 UFUNCTION(BlueprintPure, Category="PokeMonster|Save") FString GetLastStorageMessage() const { return LastStorageMessage; }
 /** Editor PIE only; an explicitly named isolated slot, never a user slot. No copies. */
 UFUNCTION(BlueprintCallable, Category="Development", meta=(DevelopmentOnly)) bool UseIsolatedPIETestSlot(const FString& SlotName);
 static FPokeMonsterSavedPlayerLocation CapturePlayerLocation(const UWorld* World);
 static void SynchronizeRestoredPlayer(APokeMonsterPlayerCharacter* Player);
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Save") bool SaveCurrentGame();
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Save") bool LoadGame();
	UFUNCTION(BlueprintPure, Category="PokeMonster|Save") bool HasSaveGame() const;
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Save") bool DeleteDevSave();
#if WITH_EDITOR
    /** In-memory save transport for one explicit PIE test. No disk slot is created or changed. */
    bool BeginPIEMemoryPreview();
    bool EndPIEMemoryPreview();
    bool IsPIEMemoryPreviewActive() const { return !PIEOriginalSnapshot.IsEmpty(); }
    bool IsPIETestStorageActive() const { return IsPIEMemoryPreviewActive() || !IsolatedPIESlot.IsEmpty(); }
#endif
	/** Explicit PIE diagnostics: mutate, save, clear, load and verify session state. */
	bool RunDevRoundTripTest();

	/** macOS: verified sibling write followed by atomic rename; the previous slot survives failure. */
	static bool SaveSnapshotToSlot(UPokeMonsterSaveGame* Save, const FString& SlotName);

	/** Exposed for precise tests and future save transports; no runtime mutation. */
	static UPokeMonsterSaveGame* CaptureSnapshot(const UPokeMonsterEncounterSubsystem* Encounter,
		const UPokeMonsterInventorySubsystem* Inventory, UObject* Outer,
		const UPokeMonsterCheckpointSubsystem* Checkpoint = nullptr,
		const UPokeMonsterQuestSubsystem* Quests = nullptr);
	/** Validates and commits a snapshot atomically outside an encounter. */
	static bool RestoreSnapshot(const UPokeMonsterSaveGame* Save,
		UPokeMonsterEncounterSubsystem* Encounter, UPokeMonsterInventorySubsystem* Inventory,
		UPokeMonsterCheckpointSubsystem* Checkpoint = nullptr,
		UPokeMonsterQuestSubsystem* Quests = nullptr, bool bValidateOnly = false);
private:
 friend struct FPokeMonsterSaveV2TestAccess;
 bool WriteCurrentGame(bool bRecovery);
 bool ReadGame(bool bRecovery);
 bool CanAccessWorldState(bool bRecovery = false) const;
 bool HasSlot(bool bRecovery) const;
 FString SlotName(bool bRecovery) const;
 bool CompleteLoad(UWorld* World);
 void HandlePostLoadMap(UWorld* World);
 void HandleTravelFailure(UWorld* World, ETravelFailure::Type Type, const FString& Error);
 void ClearPendingLoad();
 UPROPERTY(Transient) TObjectPtr<UPokeMonsterSaveGame> PendingLoad;
 FPokeMonsterSavedPlayerLocation PendingLocation;
 FString LastStorageMessage;
 FDelegateHandle PostLoadMapHandle;
 FDelegateHandle TravelFailureHandle;
 bool bUsingPositionFallback = false;
 FTimerHandle LoadTimer;
 bool bWriting = false;
 int32 LoadAttempts = 0;
#if WITH_EDITOR
private:
    TArray<uint8> PIEOriginalSnapshot;
    TArray<uint8> PIEMemorySave;
    TArray<uint8> PIEMemoryRecovery;
    FString IsolatedPIESlot;
#endif
};
