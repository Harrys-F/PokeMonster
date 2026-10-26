#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "PokeMonsterBattlePresenter.h"
#include "PokeMonsterBattlePresentationPlan.h"
#include "TimerManager.h"
#include "PokeMonsterBattleWidget.generated.h"

class UButton;
class UTextBlock;
class UProgressBar;
class UScrollBox;
class UCanvasPanel;
class UImage;
class UTextureRenderTarget2D;
class UTexture2D;
UENUM(BlueprintType)
enum class EPokeMonsterBattleMenu : uint8 { Commands, Moves, Team, Bag };

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FPokeMonsterWorldPresentationStep, const FPokeMonsterPresentationAction&, Action, FName, Step);

/** Native UMG fallback view. A Blueprint subclass can supply matching named widgets and visual hooks. */
UCLASS(Blueprintable)
class POKEMONSTER_API UPokeMonsterBattleWidget : public UUserWidget
{
	GENERATED_BODY()
 friend class FPokeMonsterSwitchProInputTest;
 friend class FPokeMonsterSwitchProWidgetTest;
 friend class FExperienceBattleWidgetTest;
public:
	UFUNCTION(BlueprintCallable, Category="Battle UI") void SetPresenter(UPokeMonsterBattlePresenter* InPresenter);
	UFUNCTION(BlueprintPure, Category="Battle UI") UButton* GetAttackButton(int32 SlotIndex) const;
	UFUNCTION(BlueprintPure, Category="Battle UI") UButton* GetSwitchButton(int32 TeamIndex) const;
	UFUNCTION(BlueprintPure, Category="Battle UI") UButton* GetCaptureButton() const { return CaptureButton; }
	/** Reuses this presentation in the loaded overworld, without the test-map restart control. */
	void SetEncounterOverlay(bool bEnabled);
	void SetWorldPresentation(bool Player3D, bool Opponent3D);
	void SetClassicPresentation(UTextureRenderTarget2D* Target,bool Player3D,bool Opponent3D);
	void SetBattleAnchors(FVector2D Player,FVector2D Opponent){PlayerAnchor=Player;OpponentAnchor=Opponent;}
 void SetBattleGroundAnchors(FVector2D Player,FVector2D Opponent);
	UFUNCTION(BlueprintPure) bool IsClassicPresentation() const {return bClassicPresentation;}
	UFUNCTION(BlueprintCallable) void SetBattleMenu(EPokeMonsterBattleMenu Page);
 UFUNCTION(BlueprintPure,Category="Battle UI") FPokeMonsterExperienceView GetPresentedExperience()const{return DisplayedExperience;}
 UFUNCTION(BlueprintPure) EPokeMonsterBattleMenu GetBattleMenu() const {return MenuPage;}
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Input") bool bNintendoButtonLayout=true;
 UFUNCTION(BlueprintPure) UButton* GetHealingButton(int32 Index)const{return HealingButtons.IsValidIndex(Index)?HealingButtons[Index].Get():nullptr;}
 UFUNCTION(BlueprintPure) UButton* GetCommandButton(int32 Index)const{return CommandButtons.IsValidIndex(Index)?CommandButtons[Index].Get():nullptr;}
 UPROPERTY(BlueprintAssignable) FPokeMonsterWorldPresentationStep OnWorldPresentationStep;
protected:
	virtual TSharedRef<SWidget> RebuildWidget() override;
	virtual void NativeConstruct() override;
	virtual void NativeDestruct() override;
 virtual void NativeTick(const FGeometry&,float DeltaSeconds)override;
 virtual FReply NativeOnPreviewKeyDown(const FGeometry&,const FKeyEvent&)override;
 virtual FNavigationReply NativeOnNavigation(const FGeometry&,const FNavigationEvent&)override;
	UFUNCTION(BlueprintImplementableEvent, Category="Battle UI") void OnBattleViewUpdated(const FPokeMonsterBattleView& View);
	UFUNCTION(BlueprintImplementableEvent, Category="Battle UI") void OnBattleRoundResolved(const FPokeMonsterBattleResult& Result);
	/** Replace placeholder motion/VFX/sound per step without changing the BattleSession. */
	UFUNCTION(BlueprintImplementableEvent, Category="Battle UI") void OnBattlePresentationStep(const FPokeMonsterPresentationAction& Action, FName Step);
private:
	enum class EPresentationPhase : uint8 { Windup, Travel, Impact, HP, Message, KO, Gap, Experience };
	void BuildDefaultTree();
	void BuildClassicTree();
 void UpdateClassicMenu();
 void FocusMenu(int32 Direction);
 TArray<UButton*> ActiveMenuButtons()const;
 UFUNCTION() void Healing0();UFUNCTION() void Healing1();UFUNCTION() void Healing2();UFUNCTION() void NextBagPage();
 void SelectHealing(int32 ButtonIndex);
 UPROPERTY(Transient) TArray<TObjectPtr<UButton>> HealingButtons;
 UPROPERTY(Transient) TObjectPtr<UButton> BagNextButton;
 UPROPERTY(Transient) TObjectPtr<UPokeMonsterItemData> HealingTargetItem;
 int32 BagPage=0;
 UFUNCTION()void CommandFight();UFUNCTION()void CommandTeam();UFUNCTION()void CommandBag();UFUNCTION()void CommandFlee();UFUNCTION()void MenuBack();
 UPROPERTY(Transient)TArray<TObjectPtr<UButton>> CommandButtons;
 UPROPERTY(Transient)TArray<TObjectPtr<UCanvasPanel>> MenuPanels;
 UPROPERTY(Transient)TObjectPtr<UButton> BackButton;
 UPROPERTY(Transient)TObjectPtr<UTextBlock> MenuHint;
 EPokeMonsterBattleMenu MenuPage=EPokeMonsterBattleMenu::Commands;
 TWeakObjectPtr<UButton> LastFocusedButton;
 bool bLastMenuBusy=false,bInitialMenuFocused=false;
 float IntroTime=0.f,ExitTime=0.f;
	UPROPERTY(Transient) TObjectPtr<UTextureRenderTarget2D> ClassicTarget;
	UPROPERTY(Transient) TObjectPtr<UImage> ClassicImage;
 UPROPERTY(Transient) TObjectPtr<UTexture2D> ContactTexture;
 UPROPERTY(Transient) TObjectPtr<UTexture2D> FireEffectTexture;
 UPROPERTY(Transient) TArray<TObjectPtr<UImage>> ContactMarks;
 FVector2D PlayerGroundAnchor=FVector2D(350,450),OpponentGroundAnchor=FVector2D(890,330);
	bool bClassicPresentation=false;
	FVector2D PlayerAnchor=FVector2D(350,350),OpponentAnchor=FVector2D(890,235);
	void BindControls();
	void Choose(int32 Slot);
	void ChooseSwitch(int32 TeamIndex);
	void ChooseCapture();
	void ResolveOverlaySelection();
	void BeginAction();
	void BeginPhase(EPresentationPhase NewPhase);
	void TickPresentation();
	void AdvancePhase();
	void EndPresentation();
	void ResetVisuals();
	void AppendPresentationLog(const FString& Line);
	void SetPresentedExperience(const FPokeMonsterExperienceView& Value,bool UpdateLevel=false);
 FPokeMonsterExperienceView DisplayedExperience,ExperienceBefore,ExperienceAfter;
 FGuid DisplayedExperienceId;
 double ExperiencePhaseStartTime=0;
 UPROPERTY(Transient) TObjectPtr<UProgressBar> PlayerExperienceBar;
 UPROPERTY(Transient) TObjectPtr<UTextBlock> PlayerExperienceLabel;
	void SetPresentedHP(EPokeMonsterBattleSide Side, float HP);
	UWidget* FigureFor(EPokeMonsterBattleSide Side) const;
	FString NameFor(EPokeMonsterBattleSide Side) const;
	FString MoveNameFor(const FPokeMonsterPresentationAction& Action) const;
	UFUNCTION() void Refresh();
	UFUNCTION() void RoundResolved(const FPokeMonsterBattleResult& Result);
	UFUNCTION() void Move0();
	UFUNCTION() void Move1();
	UFUNCTION() void Move2();
	UFUNCTION() void Move3();
	UFUNCTION() void Team0();
	UFUNCTION() void Team1();
	UFUNCTION() void Team2();
	UFUNCTION() void Team3();
	UFUNCTION() void Team4();
	UFUNCTION() void Team5();
	UFUNCTION() void Restart();
	UFUNCTION() void Capture();
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterBattlePresenter> Presenter;
	UPROPERTY(Transient) TArray<TObjectPtr<UButton>> Buttons;
	UPROPERTY(Transient) TArray<TObjectPtr<UTextBlock>> MoveLabels;
	UPROPERTY(Transient) TArray<TObjectPtr<UButton>> TeamButtons;
	UPROPERTY(Transient) TArray<TObjectPtr<UTextBlock>> TeamLabels;
	UPROPERTY(Transient) TArray<TObjectPtr<UTextBlock>> OpponentTeamLabels;
	UPROPERTY(Transient) TArray<TObjectPtr<UImage>> OpponentTeamPlates;
	UPROPERTY(Transient) TArray<TObjectPtr<UTextBlock>> MoveTypeLabels;
	UPROPERTY(Transient) TArray<TObjectPtr<UTextBlock>> MovePPLabels;
	UPROPERTY(Transient) TArray<TObjectPtr<UImage>> MoveTypeAccents;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> PlayerName;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> OpponentName;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> PlayerHP;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> OpponentHP;
	UPROPERTY(Transient) TObjectPtr<UProgressBar> PlayerBar;
	UPROPERTY(Transient) TObjectPtr<UProgressBar> OpponentBar;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> StatusLabel;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> LogLabel;
	UPROPERTY(Transient) TObjectPtr<UScrollBox> LogScroll;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> PlayerKO;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> OpponentKO;
	UPROPERTY(Transient) TObjectPtr<UWidget> PlayerFigure;
	UPROPERTY(Transient) TObjectPtr<UWidget> OpponentFigure;
	UPROPERTY(Transient) TObjectPtr<UButton> RestartButton;
	UPROPERTY(Transient) TObjectPtr<UButton> CaptureButton;
	UPROPERTY(Transient) TObjectPtr<UImage> BattleEffect;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> FeedbackLabel;
	TArray<FPokeMonsterPresentationAction> PresentationActions;
	FString PresentedLog;
	FTimerHandle PresentationTimer;
	FTimerHandle OverlayRoundTimer;
	bool bEncounterOverlay = false;
	bool bWorldPresentation=false,bWorldPlayer=false,bWorldOpponent=false;
	EPresentationPhase PresentationPhase = EPresentationPhase::Windup;
	float PhaseElapsed = 0.0f;
	int32 ActionIndex = INDEX_NONE;
	int32 DisplayedRound = 0;
	int32 DisplayedPlayerHP = 0;
	int32 DisplayedOpponentHP = 0;
	bool bPresenting = false;
};
