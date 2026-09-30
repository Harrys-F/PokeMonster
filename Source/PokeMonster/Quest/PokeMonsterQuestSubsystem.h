#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterQuestData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "PokeMonsterQuestSubsystem.generated.h"

class UPokeMonsterEncounterSubsystem;
class UPokeMonsterInventorySubsystem;

UENUM(BlueprintType)
enum class EPokeMonsterQuestStatus : uint8 { NotStarted, Active, Completed };

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterQuestProgress
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly) FName QuestId;
	UPROPERTY(BlueprintReadOnly) EPokeMonsterQuestStatus Status = EPokeMonsterQuestStatus::NotStarted;
	/** Ordered objectives [0, CurrentStep) are complete. */
	UPROPERTY(BlueprintReadOnly) int32 CurrentStep = 0;
};

/** Quest-specific events are stored here; trainer, flags and items remain owned by their existing subsystems. */
UCLASS()
class POKEMONSTER_API UPokeMonsterQuestSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	bool StartQuest(const UPokeMonsterQuestData* Definition);
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Quest") bool StartQuestById(FName QuestId);
	void RecordDialogue(FName DialogueId);
	void RecordCapturedSpecies(FName SpeciesId);
	TArray<FName> GetCapturedSpeciesIds() const { return CapturedSpeciesIds.Array(); }
	void RestoreCapturedSpeciesIds(const TArray<FName>& Ids)
	{ CapturedSpeciesIds.Reset(); for (FName Id : Ids) if (!Id.IsNone()) CapturedSpeciesIds.Add(Id); }
	void RefreshProgress(UPokeMonsterEncounterSubsystem* Encounter, const UPokeMonsterInventorySubsystem* Inventory);
	EPokeMonsterQuestStatus GetStatus(FName QuestId) const;
	int32 GetCurrentStep(FName QuestId) const;
	const UPokeMonsterQuestData* GetDefinition(FName QuestId) const;
	const UPokeMonsterQuestData* GetActiveMainQuest() const;
	const TArray<FPokeMonsterQuestProgress>& GetProgress() const { return Progress; }
	bool ValidateSavedProgress(const TArray<FPokeMonsterQuestProgress>& Saved) const;
	void RestoreProgress(const TArray<FPokeMonsterQuestProgress>& Saved);
	/** Versions 1/2 had no quest record; infer only the mini-slice milestones visible in existing world state. */
	void MigrateLegacyMiniSlice(const UPokeMonsterEncounterSubsystem* Encounter);
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;
private:
	UFUNCTION() void HandleEncounterEnded(const FPokeMonsterEncounterEndData& Result);
	UFUNCTION() void HandlePersistentStateRestored();
	const UPokeMonsterQuestData* ResolveDefinition(FName QuestId) const;
	bool IsSatisfied(const FPokeMonsterQuestObjective& Objective,
		const UPokeMonsterEncounterSubsystem* Encounter, const UPokeMonsterInventorySubsystem* Inventory) const;
	void Advance(UPokeMonsterEncounterSubsystem* Encounter);
	UPROPERTY(Transient) TArray<FPokeMonsterQuestProgress> Progress;
	UPROPERTY(Transient) TArray<TObjectPtr<UPokeMonsterQuestData>> RuntimeDefinitions;
	UPROPERTY(Transient) TSet<FName> CapturedSpeciesIds;
};
