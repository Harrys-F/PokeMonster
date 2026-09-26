#include "PokeMonsterDefeatWidget.h"

#include "Blueprint/WidgetTree.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "Styling/CoreStyle.h"

TSharedRef<SWidget> UPokeMonsterDefeatWidget::RebuildWidget()
{
	if (!WidgetTree) Initialize();
	if (WidgetTree && !WidgetTree->RootWidget) BuildDefaultTree();
	return Super::RebuildWidget();
}

void UPokeMonsterDefeatWidget::BuildDefaultTree()
{
	auto* Root = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), TEXT("DefeatRoot"));
	WidgetTree->RootWidget = Root;
	auto* Veil = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), TEXT("DefeatVeil"));
	Veil->SetColorAndOpacity(FLinearColor(0.015f, 0.045f, 0.035f, 0.91f));
	Veil->SetVisibility(ESlateVisibility::HitTestInvisible);
	auto* VeilSlot = Root->AddChildToCanvas(Veil);
	VeilSlot->SetAnchors(FAnchors(0.f, 0.f, 1.f, 1.f));
	VeilSlot->SetOffsets(FMargin(0.f));
	MessageLabel = WidgetTree->ConstructWidget<UTextBlock>(UTextBlock::StaticClass(), TEXT("DefeatMessage"));
	MessageLabel->SetFont(FCoreStyle::GetDefaultFontStyle(TEXT("Regular"), 27));
	MessageLabel->SetColorAndOpacity(FSlateColor(FLinearColor(0.91f, 0.89f, 0.76f)));
	MessageLabel->SetJustification(ETextJustify::Center);
	MessageLabel->SetAutoWrapText(true);
	MessageLabel->SetVisibility(ESlateVisibility::HitTestInvisible);
	MessageLabel->SetText(CurrentMessage);
	auto* LabelSlot = Root->AddChildToCanvas(MessageLabel);
	LabelSlot->SetAnchors(FAnchors(0.5f, 0.5f));
	LabelSlot->SetAlignment(FVector2D(0.5f, 0.5f));
	LabelSlot->SetSize(FVector2D(760.f, 130.f));
}

void UPokeMonsterDefeatWidget::SetMessage(const FText& Message)
{
	CurrentMessage = Message;
	if (MessageLabel) MessageLabel->SetText(CurrentMessage);
}
