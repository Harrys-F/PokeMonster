#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "PokeMonsterOverworldView.h"
#include "PokeMonsterOverworldWidget.generated.h"

class APokeMonsterOverworldPlayerController;
class UPokeMonsterItemData;
class UButton;
class UCanvasPanel;
class UTextBlock;
class UVerticalBox;
class UProgressBar;

UENUM(BlueprintType)
enum class EPokeMonsterOverworldMenuSection : uint8 { Team, Inventory, Main, Moves };

/** Native UMG fallback with named controls and a Blueprint view hook for later artwork. */
UCLASS(Blueprintable)
class POKEMONSTER_API UPokeMonsterOverworldWidget : public UUserWidget
{
	GENERATED_BODY()
 friend class FPokeMonsterSwitchProInputTest;
 friend class FPokeMonsterSwitchProWidgetTest;
public:
	void SetMoveMasterMode(bool bEnabled);
 void SetOwnerController(APokeMonsterOverworldPlayerController* InController);
	void SetMenuOpen(bool bOpen, EPokeMonsterOverworldMenuSection InitialSection = EPokeMonsterOverworldMenuSection::Team);
	void SetBattleVisible(bool bBattleVisible);
	void SetInteractionAvailable(bool bAvailable,const FString& Action=FString());
	void UpdateView(const FPokeMonsterOverworldView& NewView);
	UFUNCTION(BlueprintCallable, Category="PokeMonster|Team") bool SelectTeamSlot(int32 TeamIndex);
	UFUNCTION(BlueprintPure, Category="PokeMonster|Overworld UI") bool IsMenuOpen() const { return bMenuOpen; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Overworld UI") EPokeMonsterOverworldMenuSection GetSection() const { return Section; }
	UFUNCTION(BlueprintPure, Category="PokeMonster|Overworld UI") const FPokeMonsterOverworldView& GetView() const { return View; }
protected:
	virtual TSharedRef<SWidget> RebuildWidget() override;
	virtual void NativeConstruct() override;
 virtual void NativeTick(const FGeometry& Geometry,float DeltaSeconds) override;
	virtual FNavigationReply NativeOnNavigation(const FGeometry& Geometry, const FNavigationEvent& Event) override;
	virtual FReply NativeOnPreviewKeyDown(const FGeometry& InGeometry, const FKeyEvent& InKeyEvent) override;
	UFUNCTION(BlueprintImplementableEvent, Category="PokeMonster|Overworld UI")
	void OnOverworldViewUpdated(const FPokeMonsterOverworldView& NewView);
private:
 friend class FMoveManagementV2Widget;
 friend class FExperienceInfoWidgetTest;
 UPROPERTY(Transient) TObjectPtr<UProgressBar> ExperienceBar;
 friend class FSaveV2MenuGuardTest;
 void RenderMoves();
 UFUNCTION() void ConfirmMoves();
 void CancelMoves();
 UFUNCTION() void ShowMoves();
 bool bMoveMasterMode=false;
 bool bChoosingMovePokemon=true;
 bool bMoveReview=false;
 int32 MovePokemon=0;
 int32 MoveCursor=0;
 int32 ReplaceCursor=INDEX_NONE;
 UPROPERTY(Transient) TArray<TSoftObjectPtr<UPokeMonsterMoveData>> DraftMoves;
 UPROPERTY(Transient) TObjectPtr<UButton> MovesTab;
 UPROPERTY(Transient) TObjectPtr<UButton> MoveActionButton;
 FString MoveMessage;
 void UpdatePokemonNames(const FVector2D& ViewSize);
 UPROPERTY(Transient) TObjectPtr<UCanvasPanel> PokemonNameLayer;
 UPROPERTY(Transient) TArray<TObjectPtr<UTextBlock>> PokemonNameLabels;
public:
 UPROPERTY(Transient,BlueprintReadOnly) int32 VisiblePokemonNameCount=0;
private:
	void BuildDefaultTree();
	void RefreshTeamFocus();
 void NavigateMenu(int32 Delta);
 void ConfirmMenu();
 UFUNCTION() void SaveGame();
 UFUNCTION() void LoadGame();
 UFUNCTION() void LoadRecoveryGame();
 UFUNCTION() void ConfirmStorage();
 UFUNCTION() void CancelStorage();
 int32 PendingStorageAction = 0;
 bool bStorageBusy = false;
 uint64 LastStorageInputFrame = MAX_uint64;
 FString StorageMessage;
 UPROPERTY(Transient) TArray<TObjectPtr<UButton>> MainButtons;
 int32 FocusedMainSlot = 0;
 int32 FocusedInventorySlot = 0;
	UFUNCTION() void Team0();
	UFUNCTION() void Team1();
	UFUNCTION() void Team2();
	UFUNCTION() void Team3();
	UFUNCTION() void Team4();
	UFUNCTION() void Team5();
	UPROPERTY(Transient) TArray<TObjectPtr<UButton>> TeamButtons;
	FGuid SelectedInstanceId;
 UPROPERTY(Transient) TObjectPtr<UPokeMonsterItemData> PendingHealingItem;
	int32 FocusedTeamSlot = 0;
	void Render();
	UFUNCTION() void OpenInventory();
	UFUNCTION() void ShowTeam();
	UFUNCTION() void ShowInventory();
	UFUNCTION() void CloseMenu();
	UPROPERTY(Transient) TWeakObjectPtr<APokeMonsterOverworldPlayerController> OwnerController;
	UPROPERTY(Transient) TObjectPtr<UCanvasPanel> HudLayer;
	UPROPERTY(Transient) TObjectPtr<UCanvasPanel> MenuLayer;
	UPROPERTY(Transient) TObjectPtr<UVerticalBox> HudTeamRows;
	UPROPERTY(Transient) TObjectPtr<UVerticalBox> MenuRows;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> EmptyTeamLabel;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> SectionTitle;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> InteractionLabel;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> QuestTitle;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> QuestObjective;
	UPROPERTY(Transient) TObjectPtr<UCanvasPanel> QuestPanel;
	UPROPERTY(Transient) TObjectPtr<UButton> InventoryButton;
	UPROPERTY(Transient) TObjectPtr<UButton> TeamTab;
	UPROPERTY(Transient) TObjectPtr<UButton> InventoryTab;
	UPROPERTY(Transient) TObjectPtr<UButton> CloseButton;
	UPROPERTY(Transient) FPokeMonsterOverworldView View;
	FString LastRenderKey;
	EPokeMonsterOverworldMenuSection Section = EPokeMonsterOverworldMenuSection::Team;
	bool bMenuOpen = false;
	bool bBattleVisible = false;
};
