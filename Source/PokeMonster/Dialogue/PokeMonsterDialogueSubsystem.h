#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "PokeMonsterDialogueData.h"
#include "PokeMonsterDialogueSubsystem.generated.h"

class APokeMonsterPlayerCharacter;
class UPokeMonsterEncounterSubsystem;

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FPokeMonsterDialogueChanged);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FPokeMonsterDialogueCustomAction, AActor*, Source, FName, ActionId);

/** One active Overworld conversation. It owns only navigation and the input lock. */
UCLASS()
class POKEMONSTER_API UPokeMonsterDialogueSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Dialogue")
	bool StartDialogue(APokeMonsterPlayerCharacter* Player, AActor* Source,
		const UPokeMonsterDialogueData* Data, UPokeMonsterEncounterSubsystem* Encounter);
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Dialogue") bool AdvanceDialogue();
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Dialogue") void CloseDialogue();
	UFUNCTION(BlueprintPure, Category="PokeMonster|Dialogue") bool IsDialogueActive() const { return bActive; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Dialogue") int32 GetPageIndex() const { return PageIndex; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Dialogue") int32 GetPageCount() const { return ActivePages.Num(); }
	const FPokeMonsterDialoguePage* GetCurrentPage() const;
	static bool IsConditionMet(const FPokeMonsterDialoguePage& Page,
		const UPokeMonsterEncounterSubsystem* Encounter);
	static TArray<FPokeMonsterDialoguePage> SelectPages(const UPokeMonsterDialogueData* Data,
		const UPokeMonsterEncounterSubsystem* Encounter);
	UPROPERTY(BlueprintAssignable, Category="PokeMonster|Dialogue") FPokeMonsterDialogueChanged OnDialogueChanged;
	/** Custom actions are deliberately left to the source actor or a later story system. */
	UPROPERTY(BlueprintAssignable, Category="PokeMonster|Dialogue") FPokeMonsterDialogueCustomAction OnCustomAction;
	virtual void Deinitialize() override;
private:
	void RunFollowUp(const FPokeMonsterDialoguePage& Page, AActor* Source,
		UPokeMonsterEncounterSubsystem* Encounter);
	UPROPERTY(Transient) TArray<FPokeMonsterDialoguePage> ActivePages;
	TWeakObjectPtr<APokeMonsterPlayerCharacter> ActivePlayer;
	TWeakObjectPtr<AActor> ActiveSource;
	TWeakObjectPtr<UPokeMonsterEncounterSubsystem> ActiveEncounter;
	int32 PageIndex = 0;
	bool bActive = false;
};
