#include "PokeMonsterDialogueWidget.h"

#include "PokeMonsterOverworldPlayerController.h"
#include "Blueprint/WidgetTree.h"
#include "Brushes/SlateRoundedBoxBrush.h"
#include "Components/Button.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "Styling/CoreStyle.h"

namespace
{
	const FLinearColor DialogueInk(0.93f, 0.90f, 0.78f);
	const FLinearColor DialogueSoftInk(0.72f, 0.78f, 0.66f);
	const FLinearColor DialoguePine(0.075f, 0.15f, 0.125f, 0.97f);
	UTextBlock* DialogueTextWidget(UWidgetTree* Tree, FName Name, int32 Size, FLinearColor Color)
	{
		auto* Result = Tree->ConstructWidget<UTextBlock>(UTextBlock::StaticClass(), Name);
		Result->SetFont(FCoreStyle::GetDefaultFontStyle(TEXT("Regular"), Size));
		Result->SetColorAndOpacity(FSlateColor(Color));
		Result->SetVisibility(ESlateVisibility::HitTestInvisible);
		return Result;
	}
	void DialoguePlace(UCanvasPanel* Canvas, UWidget* Child, FVector2D Position, FVector2D Size)
	{
		auto* Slot = Canvas->AddChildToCanvas(Child);
		Slot->SetAnchors(FAnchors(0.5f, 1.f));
		Slot->SetPosition(Position);
		Slot->SetSize(Size);
	}
}

TSharedRef<SWidget> UPokeMonsterDialogueWidget::RebuildWidget()
{
	if (!WidgetTree) Initialize();
	if (WidgetTree && !WidgetTree->RootWidget) BuildDefaultTree();
	return Super::RebuildWidget();
}

void UPokeMonsterDialogueWidget::SetOwnerController(APokeMonsterOverworldPlayerController* Controller)
{
	OwnerController = Controller;
}

void UPokeMonsterDialogueWidget::BuildDefaultTree()
{
	auto* Root = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), TEXT("DialogueRoot"));
	WidgetTree->RootWidget = Root;
	auto* Shadow = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), TEXT("DialogueShadow"));
	Shadow->SetBrush(FSlateRoundedBoxBrush(FLinearColor(0.01f,0.035f,0.025f,0.48f), 22.f));
	Shadow->SetVisibility(ESlateVisibility::HitTestInvisible);
	DialoguePlace(Root, Shadow, FVector2D(-386.f,-253.f), FVector2D(772.f,204.f));
	auto* Plate = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), TEXT("DialoguePlate"));
	Plate->SetBrush(FSlateRoundedBoxBrush(DialoguePine, 20.f));
	Plate->SetVisibility(ESlateVisibility::HitTestInvisible);
	DialoguePlace(Root, Plate, FVector2D(-390.f,-259.f), FVector2D(772.f,204.f));
	auto* Accent = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), TEXT("DialogueAccent"));
	Accent->SetBrush(FSlateRoundedBoxBrush(FLinearColor(0.30f,0.42f,0.28f), 4.f));
	Accent->SetVisibility(ESlateVisibility::HitTestInvisible);
	DialoguePlace(Root, Accent, FVector2D(-390.f,-259.f), FVector2D(6.f,204.f));
	PortraitImage = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), TEXT("Portrait"));
	PortraitImage->SetVisibility(ESlateVisibility::Collapsed);
	DialoguePlace(Root, PortraitImage, FVector2D(-365.f,-224.f), FVector2D(110.f,110.f));
	SpeakerLabel = DialogueTextWidget(WidgetTree, TEXT("SpeakerName"), 20, DialogueSoftInk);
	DialoguePlace(Root, SpeakerLabel, FVector2D(-358.f,-235.f), FVector2D(570.f,32.f));
	BodyLabel = DialogueTextWidget(WidgetTree, TEXT("DialogueText"), 20, DialogueInk);
	BodyLabel->SetAutoWrapText(true);
	DialoguePlace(Root, BodyLabel, FVector2D(-358.f,-191.f), FVector2D(635.f,105.f));
	PageLabel = DialogueTextWidget(WidgetTree, TEXT("PageIndicator"), 15, DialogueSoftInk);
	DialoguePlace(Root, PageLabel, FVector2D(-357.f,-82.f), FVector2D(160.f,25.f));
	AdvanceButton = WidgetTree->ConstructWidget<UButton>(UButton::StaticClass(), TEXT("AdvanceButton"));
	FButtonStyle ButtonStyle;
	ButtonStyle.SetNormal(FSlateRoundedBoxBrush(FLinearColor(0.25f,0.37f,0.27f), 11.f));
	ButtonStyle.SetHovered(FSlateRoundedBoxBrush(FLinearColor(0.34f,0.46f,0.32f), 11.f));
	ButtonStyle.SetPressed(FSlateRoundedBoxBrush(FLinearColor(0.42f,0.52f,0.38f), 11.f));
	AdvanceButton->SetStyle(ButtonStyle);
	AdvanceLabel = DialogueTextWidget(WidgetTree, TEXT("AdvanceLabel"), 17, DialogueInk);
	AdvanceButton->AddChild(AdvanceLabel);
	DialoguePlace(Root, AdvanceButton, FVector2D(208.f,-108.f), FVector2D(145.f,44.f));
	CloseButton = WidgetTree->ConstructWidget<UButton>(UButton::StaticClass(), TEXT("CloseButton"));
	CloseButton->SetStyle(ButtonStyle);
	CloseButton->AddChild(DialogueTextWidget(WidgetTree, NAME_None, 16, DialogueInk));
	if (auto* Label = Cast<UTextBlock>(CloseButton->GetChildAt(0)))
		Label->SetText(FText::FromString(TEXT("×")));
	DialoguePlace(Root, CloseButton, FVector2D(329.f,-248.f), FVector2D(37.f,37.f));
}

void UPokeMonsterDialogueWidget::NativeConstruct()
{
	Super::NativeConstruct();
	SpeakerLabel = Cast<UTextBlock>(GetWidgetFromName(TEXT("SpeakerName")));
	BodyLabel = Cast<UTextBlock>(GetWidgetFromName(TEXT("DialogueText")));
	PageLabel = Cast<UTextBlock>(GetWidgetFromName(TEXT("PageIndicator")));
	AdvanceLabel = Cast<UTextBlock>(GetWidgetFromName(TEXT("AdvanceLabel")));
	PortraitImage = Cast<UImage>(GetWidgetFromName(TEXT("Portrait")));
	AdvanceButton = Cast<UButton>(GetWidgetFromName(TEXT("AdvanceButton")));
	CloseButton = Cast<UButton>(GetWidgetFromName(TEXT("CloseButton")));
	if (AdvanceButton) AdvanceButton->OnClicked.AddUniqueDynamic(this, &UPokeMonsterDialogueWidget::Advance);
	if (CloseButton) CloseButton->OnClicked.AddUniqueDynamic(this, &UPokeMonsterDialogueWidget::Close);
	SetIsFocusable(true);
	SetVisibility(ESlateVisibility::Collapsed);
}

void UPokeMonsterDialogueWidget::ShowPage(const FPokeMonsterDialoguePage& Page,
	const int32 PageIndex, const int32 PageCount)
{
	CurrentPage = Page;
	if (SpeakerLabel) SpeakerLabel->SetText(Page.SpeakerName);
	if (BodyLabel) BodyLabel->SetText(Page.Text);
	if (PageLabel) PageLabel->SetText(FText::Format(FText::FromString(TEXT("{0} / {1}")),
		FText::AsNumber(PageIndex + 1), FText::AsNumber(PageCount)));
	if (AdvanceLabel) AdvanceLabel->SetText(FText::FromString(PageIndex + 1 == PageCount
		? TEXT("Schließen  ↵") : TEXT("Weiter  ↵")));
	if (PortraitImage)
	{
		if (UTexture2D* Texture = Page.Portrait.LoadSynchronous())
		{
			PortraitImage->SetBrushFromTexture(Texture);
			PortraitImage->SetVisibility(ESlateVisibility::HitTestInvisible);
			if (BodyLabel)
			{
				BodyLabel->SetRenderTranslation(FVector2D(125.f,0.f));
				if (auto* Slot = Cast<UCanvasPanelSlot>(BodyLabel->Slot))
					Slot->SetSize(FVector2D(510.f,105.f));
			}
		}
		else
		{
			PortraitImage->SetVisibility(ESlateVisibility::Collapsed);
			if (BodyLabel)
			{
				BodyLabel->SetRenderTranslation(FVector2D::ZeroVector);
				if (auto* Slot = Cast<UCanvasPanelSlot>(BodyLabel->Slot))
					Slot->SetSize(FVector2D(635.f,105.f));
			}
		}
	}
	SetVisibility(ESlateVisibility::Visible);
	OnDialoguePageChanged(Page, PageIndex, PageCount);
}

void UPokeMonsterDialogueWidget::HideDialogue()
{
	SetVisibility(ESlateVisibility::Collapsed);
}

FReply UPokeMonsterDialogueWidget::NativeOnKeyDown(const FGeometry& InGeometry, const FKeyEvent& InKeyEvent)
{
	const FKey Key = InKeyEvent.GetKey();
	if (Key == EKeys::Enter || Key == EKeys::E || Key == EKeys::SpaceBar)
	{
		Advance(); return FReply::Handled();
	}
	if (Key == EKeys::Escape)
	{
		Close(); return FReply::Handled();
	}
	return Super::NativeOnKeyDown(InGeometry, InKeyEvent);
}

void UPokeMonsterDialogueWidget::Advance()
{
	if (APokeMonsterOverworldPlayerController* Controller = OwnerController.Get())
		Controller->AdvanceDialogue();
}

void UPokeMonsterDialogueWidget::Close()
{
	if (APokeMonsterOverworldPlayerController* Controller = OwnerController.Get())
		Controller->CloseDialogue();
}
