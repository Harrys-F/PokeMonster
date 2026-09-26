#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "../Dialogue/PokeMonsterDialogueData.h"
#include "PokeMonsterDialogueWidget.generated.h"

class APokeMonsterOverworldPlayerController;
class UButton;
class UImage;
class UTextBlock;

/** Native UMG fallback; a Widget Blueprint can replace its visual tree later. */
UCLASS(Blueprintable)
class POKEMONSTER_API UPokeMonsterDialogueWidget : public UUserWidget
{
	GENERATED_BODY()
public:
	void SetOwnerController(APokeMonsterOverworldPlayerController* Controller);
	void ShowPage(const FPokeMonsterDialoguePage& Page, int32 PageIndex, int32 PageCount);
	void HideDialogue();
	UFUNCTION(BlueprintPure, Category="PokeMonster|Dialogue") const FPokeMonsterDialoguePage& GetPage() const { return CurrentPage; }
protected:
	virtual TSharedRef<SWidget> RebuildWidget() override;
	virtual void NativeConstruct() override;
	virtual FReply NativeOnKeyDown(const FGeometry& InGeometry, const FKeyEvent& InKeyEvent) override;
	UFUNCTION(BlueprintImplementableEvent, Category="PokeMonster|Dialogue")
	void OnDialoguePageChanged(const FPokeMonsterDialoguePage& Page, int32 PageIndex, int32 PageCount);
private:
	void BuildDefaultTree();
	UFUNCTION() void Advance();
	UFUNCTION() void Close();
	UPROPERTY(Transient) TWeakObjectPtr<APokeMonsterOverworldPlayerController> OwnerController;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> SpeakerLabel;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> BodyLabel;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> PageLabel;
	UPROPERTY(Transient) TObjectPtr<UTextBlock> AdvanceLabel;
	UPROPERTY(Transient) TObjectPtr<UImage> PortraitImage;
	UPROPERTY(Transient) TObjectPtr<UButton> AdvanceButton;
	UPROPERTY(Transient) TObjectPtr<UButton> CloseButton;
	UPROPERTY(Transient) FPokeMonsterDialoguePage CurrentPage;
};
