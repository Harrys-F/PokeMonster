#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterSaveGame.h"
#include "PokeMonsterSaveSubsystem.generated.h"

struct FPokeMonsterCreatureInstance;
class UPokeMonsterInventorySubsystem;
class UPokeMonsterEncounterSubsystem;

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
	/** Explicit PIE diagnostics: mutate, save, clear, load and verify session state. */
	bool RunDevRoundTripTest();

	/** Exposed for precise tests and future save transports; no runtime mutation. */
	static UPokeMonsterSaveGame* CaptureSnapshot(const UPokeMonsterEncounterSubsystem* Encounter,
		const UPokeMonsterInventorySubsystem* Inventory, UObject* Outer);
	/** Validates and commits a snapshot atomically outside an encounter. */
	static bool RestoreSnapshot(const UPokeMonsterSaveGame* Save,
		UPokeMonsterEncounterSubsystem* Encounter, UPokeMonsterInventorySubsystem* Inventory);
};
