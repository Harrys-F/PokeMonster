#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "PokeMonsterBattlePresenter.h"
#include "PokeMonsterBattleWidget.generated.h"

class UButton;
class UTextBlock;
class UProgressBar;
class UScrollBox;
class UCanvasPanel;

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
private:
	void BuildDefaultTree();
	void BindControls();
	void Choose(int32 Slot);
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
};
