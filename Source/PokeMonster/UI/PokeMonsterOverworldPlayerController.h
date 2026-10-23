#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "PokeMonsterOverworldWidget.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "PokeMonsterOverworldPlayerController.generated.h"

class IInputProcessor;
class APokeMonsterNPC;
class UPokeMonsterItemData;
class APokeMonsterPlayerCharacter;
class APokeMonsterVisibleWildCreatureActor;
class UPokeMonsterEncounterSubsystem;
class UPokeMonsterDialogueWidget;
struct FPokeMonsterEncounterEndData;

/** Owns only Overworld input focus and presentation; gameplay data stay in their subsystems. */
UCLASS()
class POKEMONSTER_API APokeMonsterOverworldPlayerController : public APlayerController
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Overworld UI")
	bool OpenMenu(EPokeMonsterOverworldMenuSection InitialSection = EPokeMonsterOverworldMenuSection::Team);
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Overworld UI") bool CloseMenu();
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Overworld UI") void ToggleMenu();
 UFUNCTION(BlueprintCallable, Category="PokeMonster|Overworld UI") void ToggleMainMenu();
	UFUNCTION(BlueprintPure, Category="PokeMonster|Overworld UI") bool IsMenuOpen() const { return bMenuOpen; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Overworld UI") UPokeMonsterOverworldWidget* GetOverworldWidget() const { return OverworldWidget; }
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Dialogue") bool AdvanceDialogue();
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Dialogue") void CloseDialogue();
	UFUNCTION(BlueprintPure, Category="PokeMonster|Dialogue") UPokeMonsterDialogueWidget* GetDialogueWidget() const { return DialogueWidget; }
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Team") bool ReorderParty(FGuid SourceInstanceId, int32 TargetIndex);
 UFUNCTION(BlueprintCallable, Category="PokeMonster|Inventory") bool UseMenuHealingItem(UPokeMonsterItemData* Item, int32 TeamIndex);
 bool OpenMoveMaster(APokeMonsterNPC* Master);
 bool IsMoveMasterActive() const;
 bool CommitMoveMaster(FGuid CreatureId, const TArray<TSoftObjectPtr<UPokeMonsterMoveData>>& Moves);
	static bool CanOpenMenu(const APokeMonsterPlayerCharacter* Player,
		const UPokeMonsterEncounterSubsystem* Encounter, bool bAlreadyOpen);
	static bool TryLockMenu(APokeMonsterPlayerCharacter* Player,
		const UPokeMonsterEncounterSubsystem* Encounter, bool bAlreadyOpen);
	static void UnlockMenu(APokeMonsterPlayerCharacter* Player);
protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
	void RefreshHUD();
	UFUNCTION() void OnEncounterStarted();
	UFUNCTION() void OnEncounterEnded(const FPokeMonsterEncounterEndData& Result);
	UFUNCTION() void OnDialogueChanged();
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterOverworldWidget> OverworldWidget;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterDialogueWidget> DialogueWidget;
	FTimerHandle RefreshTimer;
 TWeakObjectPtr<APokeMonsterVisibleWildCreatureActor> FocusedWild;
 UPROPERTY(Transient) TWeakObjectPtr<APokeMonsterNPC> MoveMaster;
 UPROPERTY(Transient) TArray<FPokeMonsterCreatureInstance> MasterPartySnapshot;
	bool bMenuOpen = false;
 TSharedPtr<IInputProcessor> InputObserver;
};
