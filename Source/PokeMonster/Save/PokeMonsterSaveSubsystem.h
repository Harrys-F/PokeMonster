#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterSaveGame.h"
#include "PokeMonsterSaveSubsystem.generated.h"

struct FPokeMonsterCreatureInstance;
class UPokeMonsterInventorySubsystem;
class UPokeMonsterEncounterSubsystem;
class UPokeMonsterCheckpointSubsystem;
class UPokeMonsterQuestSubsystem;

/** One development slot. Loading validates the complete snapshot before touching runtime state. */
UCLASS()
class POKEMONSTER_API UPokeMonsterSaveSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	static const FString DevSlotName;
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Save") bool SaveCurrentGame();
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Save") bool LoadGame();
	UFUNCTION(BlueprintPure, Category="PokeMonster|Save") bool HasSaveGame() const;
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Save") bool DeleteDevSave();
#if WITH_EDITOR
    /** In-memory save transport for one explicit PIE test. No disk slot is created or changed. */
    virtual void Deinitialize() override;
    bool BeginPIEMemoryPreview();
    bool EndPIEMemoryPreview();
    bool IsPIEMemoryPreviewActive() const { return !PIEOriginalSnapshot.IsEmpty(); }
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
		UPokeMonsterQuestSubsystem* Quests = nullptr);
#if WITH_EDITOR
private:
    TArray<uint8> PIEOriginalSnapshot;
    TArray<uint8> PIEMemorySave;
#endif
};
