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

/** Native UMG fallback view. A Blueprint subclass can supply matching named widgets and visual hooks. */
UCLASS(Blueprintable)
class POKEMONSTER_API UPokeMonsterBattleWidget : public UUserWidget
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category="Battle UI") void SetPresenter(UPokeMonsterBattlePresenter* InPresenter);
	UFUNCTION(BlueprintPure, Category="Battle UI") UButton* GetAttackButton(int32 SlotIndex) const;
protected:
	virtual TSharedRef<SWidget> RebuildWidget() override;
	virtual void NativeConstruct() override;
	virtual void NativeDestruct() override;
	UFUNCTION(BlueprintImplementableEvent, Category="Battle UI") void OnBattleViewUpdated(const FPokeMonsterBattleView& View);
	UFUNCTION(BlueprintImplementableEvent, Category="Battle UI") void OnBattleRoundResolved(const FPokeMonsterBattleResult& Result);
	/** Replace placeholder motion/VFX/sound per step without changing the BattleSession. */
	UFUNCTION(BlueprintImplementableEvent, Category="Battle UI") void OnBattlePresentationStep(const FPokeMonsterPresentationAction& Action, FName Step);
private:
	enum class EPresentationPhase : uint8 { Windup, Travel, Impact, HP, Message, KO, Gap };
	void BuildDefaultTree();
	void BindControls();
	void Choose(int32 Slot);
	void BeginAction();
	void BeginPhase(EPresentationPhase NewPhase);
	void TickPresentation();
	void AdvancePhase();
	void EndPresentation();
	void ResetVisuals();
	void AppendPresentationLog(const FString& Line);
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
	UFUNCTION() void Restart();
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterBattlePresenter> Presenter;
	UPROPERTY(Transient) TArray<TObjectPtr<UButton>> Buttons;
	UPROPERTY(Transient) TArray<TObjectPtr<UTextBlock>> MoveLabels;
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
	UPROPERTY(Transient) TObjectPtr<UImage> BattleEffect;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> FeedbackLabel;
	TArray<FPokeMonsterPresentationAction> PresentationActions;
	FString PresentedLog;
	FTimerHandle PresentationTimer;
	EPresentationPhase PresentationPhase = EPresentationPhase::Windup;
	float PhaseElapsed = 0.0f;
	int32 ActionIndex = INDEX_NONE;
	int32 DisplayedRound = 0;
	int32 DisplayedPlayerHP = 0;
	int32 DisplayedOpponentHP = 0;
	bool bPresenting = false;
};
