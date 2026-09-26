#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "PokeMonsterDefeatWidget.generated.h"

class UTextBlock;

/** Small replaceable UMG blackout placeholder. Input stays locked by the checkpoint subsystem. */
UCLASS(Blueprintable)
class POKEMONSTER_API UPokeMonsterDefeatWidget : public UUserWidget
{
	GENERATED_BODY()
public:
	void SetMessage(const FText& Message);
protected:
	virtual TSharedRef<SWidget> RebuildWidget() override;
private:
	void BuildDefaultTree();
	UPROPERTY(Transient) TObjectPtr<UTextBlock> MessageLabel;
	FText CurrentMessage;
};
