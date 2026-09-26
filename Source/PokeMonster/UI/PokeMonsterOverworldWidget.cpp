#include "PokeMonsterOverworldWidget.h"

#include "PokeMonsterOverworldPlayerController.h"
#include "Blueprint/WidgetTree.h"
#include "Components/Button.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "Components/VerticalBox.h"
#include "Brushes/SlateRoundedBoxBrush.h"
#include "Styling/CoreStyle.h"

namespace
{
	const FLinearColor Ink(0.91f, 0.90f, 0.79f);
	const FLinearColor SoftInk(0.67f, 0.73f, 0.63f);
	const FLinearColor DarkInk(0.11f, 0.20f, 0.17f);
	const FLinearColor Pine(0.09f, 0.17f, 0.14f, 0.94f);
	const FLinearColor Leaf(0.21f, 0.35f, 0.27f);
	const FLinearColor Parchment(0.83f, 0.80f, 0.66f, 0.98f);

	UTextBlock* MakeText(UWidgetTree* Tree, const FName Name, const FString& Value, const int32 Size,
		const FLinearColor Color = Ink)
	{
		auto* Text = Tree->ConstructWidget<UTextBlock>(UTextBlock::StaticClass(), Name);
		Text->SetText(FText::FromString(Value));
		Text->SetFont(FCoreStyle::GetDefaultFontStyle(TEXT("Regular"), Size));
		Text->SetColorAndOpacity(FSlateColor(Color));
		Text->SetVisibility(ESlateVisibility::HitTestInvisible);
		return Text;
	}

	void Place(UCanvasPanel* Canvas, UWidget* Child, const FVector2D Position, const FVector2D Size,
		const FAnchors Anchors = FAnchors(0.f, 0.f))
	{
		auto* Slot = Canvas->AddChildToCanvas(Child);
		Slot->SetAnchors(Anchors);
		Slot->SetPosition(Position);
		Slot->SetSize(Size);
	}

	UImage* Shape(UWidgetTree* Tree, UCanvasPanel* Canvas, const FName Name,
		const FVector2D Position, const FVector2D Size, const FLinearColor Color, const float Radius,
		const FAnchors Anchors = FAnchors(0.f, 0.f))
	{
		auto* Image = Tree->ConstructWidget<UImage>(UImage::StaticClass(), Name);
		Image->SetBrush(FSlateRoundedBoxBrush(Color, Radius));
		Image->SetVisibility(ESlateVisibility::HitTestInvisible);
		Place(Canvas, Image, Position, Size, Anchors);
		return Image;
	}

	UButton* MakeButton(UWidgetTree* Tree, UCanvasPanel* Canvas, const FName Name,
		const FString& Label, const FVector2D Position, const FVector2D Size,
		const FAnchors Anchors = FAnchors(0.f, 0.f))
	{
		auto* Button = Tree->ConstructWidget<UButton>(UButton::StaticClass(), Name);
		FButtonStyle Style;
		Style.SetNormal(FSlateRoundedBoxBrush(Pine, 16.f));
		Style.SetHovered(FSlateRoundedBoxBrush(FLinearColor(0.16f, 0.27f, 0.20f, 0.98f), 16.f));
		Style.SetPressed(FSlateRoundedBoxBrush(FLinearColor(0.24f, 0.37f, 0.27f, 0.98f), 16.f));
		Button->SetStyle(Style);
		Button->AddChild(MakeText(Tree, NAME_None, Label, 18));
		Place(Canvas, Button, Position, Size, Anchors);
		return Button;
	}

	FString RenderKey(const FPokeMonsterOverworldView& View, const EPokeMonsterOverworldMenuSection Section)
	{
		FString Key = FString::FromInt(static_cast<int32>(Section));
		for (const auto& Row : View.Team)
			Key += FString::Printf(TEXT("|%s:%d:%d:%d:%d"), *Row.Name.ToString(), Row.Level,
				Row.CurrentHP, Row.MaxHP, Row.bKnockedOut ? 1 : 0);
		for (const auto& Row : View.Inventory)
			Key += FString::Printf(TEXT("|%s:%s:%d"), *Row.Name.ToString(),
				*Row.Category.ToString(), Row.Quantity);
		return Key;
	}
}

TSharedRef<SWidget> UPokeMonsterOverworldWidget::RebuildWidget()
{
	if (!WidgetTree) Initialize();
	if (WidgetTree && !WidgetTree->RootWidget) BuildDefaultTree();
	return Super::RebuildWidget();
}

void UPokeMonsterOverworldWidget::BuildDefaultTree()
{
	auto* Root = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), TEXT("OverworldRoot"));
	WidgetTree->RootWidget = Root;
	HudLayer = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), TEXT("HudLayer"));
	Place(Root, HudLayer, FVector2D::ZeroVector, FVector2D::ZeroVector, FAnchors(0.f,0.f,1.f,1.f));
	if (auto* Slot = Cast<UCanvasPanelSlot>(HudLayer->Slot)) Slot->SetOffsets(FMargin(0));
	Shape(WidgetTree, HudLayer, TEXT("HudShadow"), FVector2D(24,28), FVector2D(320,275),
		FLinearColor(0.01f,0.04f,0.03f,0.40f), 22.f);
	Shape(WidgetTree, HudLayer, TEXT("HudPlate"), FVector2D(20,24), FVector2D(320,275), Pine, 20.f);
	Shape(WidgetTree, HudLayer, TEXT("HudAccent"), FVector2D(20,24), FVector2D(6,275), Leaf, 3.f);
	Place(HudLayer, MakeText(WidgetTree,TEXT("HudTitle"),TEXT("DEIN TEAM"),16,SoftInk),
		FVector2D(43,40),FVector2D(260,25));
	HudTeamRows = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass(),TEXT("HudTeamRows"));
	Place(HudLayer,HudTeamRows,FVector2D(40,72),FVector2D(280,210));
	InventoryButton = MakeButton(WidgetTree,HudLayer,TEXT("InventoryButton"),TEXT("TASCHE  ·  TAB"),
		FVector2D(-224,24),FVector2D(198,50),FAnchors(1.f,0.f));
	InteractionLabel = MakeText(WidgetTree,TEXT("InteractionPrompt"),TEXT("E  ·  INTERAGIEREN"),16,Ink);
	Place(HudLayer,InteractionLabel,FVector2D(-125,-67),FVector2D(250,30),FAnchors(0.5f,1.f));
	InteractionLabel->SetVisibility(ESlateVisibility::Collapsed);

	MenuLayer = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(),TEXT("MenuLayer"));
	Place(Root, MenuLayer, FVector2D::ZeroVector, FVector2D::ZeroVector, FAnchors(0.f,0.f,1.f,1.f));
	if (auto* Slot = Cast<UCanvasPanelSlot>(MenuLayer->Slot)) Slot->SetOffsets(FMargin(0));
	Shape(WidgetTree,MenuLayer,TEXT("MenuDim"),FVector2D::ZeroVector,FVector2D::ZeroVector,
		FLinearColor(0.015f,0.035f,0.03f,0.57f),0.f,FAnchors(0.f,0.f,1.f,1.f));
	Shape(WidgetTree,MenuLayer,TEXT("MenuShadow"),FVector2D(-416,-280),FVector2D(832,580),
		FLinearColor(0.01f,0.035f,0.025f,0.53f),28.f,FAnchors(0.5f,0.5f));
	Shape(WidgetTree,MenuLayer,TEXT("MenuPlate"),FVector2D(-420,-288),FVector2D(832,580),
		Parchment,27.f,FAnchors(0.5f,0.5f));
	Shape(WidgetTree,MenuLayer,TEXT("MenuHeader"),FVector2D(-420,-288),FVector2D(832,92),
		Pine,25.f,FAnchors(0.5f,0.5f));
	Place(MenuLayer,MakeText(WidgetTree,TEXT("MenuTitle"),TEXT("REISEBUCH"),28,Ink),
		FVector2D(-384,-263),FVector2D(280,42),FAnchors(0.5f,0.5f));
	CloseButton = MakeButton(WidgetTree,MenuLayer,TEXT("CloseButton"),TEXT("Schließen  ×"),
		FVector2D(224,-269),FVector2D(150,48),FAnchors(0.5f,0.5f));
	TeamTab = MakeButton(WidgetTree,MenuLayer,TEXT("TeamTab"),TEXT("Team"),
		FVector2D(-383,-173),FVector2D(170,49),FAnchors(0.5f,0.5f));
	InventoryTab = MakeButton(WidgetTree,MenuLayer,TEXT("InventoryTab"),TEXT("Inventar"),
		FVector2D(-201,-173),FVector2D(170,49),FAnchors(0.5f,0.5f));
	SectionTitle = MakeText(WidgetTree,TEXT("SectionTitle"),TEXT("Team"),23,DarkInk);
	Place(MenuLayer,SectionTitle,FVector2D(-378,-102),FVector2D(500,36),FAnchors(0.5f,0.5f));
	MenuRows = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass(),TEXT("MenuRows"));
	Place(MenuLayer,MenuRows,FVector2D(-380,-51),FVector2D(748,296),FAnchors(0.5f,0.5f));
	Place(MenuLayer,MakeText(WidgetTree,TEXT("MenuHint"),TEXT("T: Team  ·  I: Inventar  ·  TAB/ESC: Schließen"),14,DarkInk),
		FVector2D(-378,255),FVector2D(600,26),FAnchors(0.5f,0.5f));
	MenuLayer->SetVisibility(ESlateVisibility::Collapsed);
}

void UPokeMonsterOverworldWidget::NativeConstruct()
{
	Super::NativeConstruct();
	InventoryButton = Cast<UButton>(GetWidgetFromName(TEXT("InventoryButton")));
	TeamTab = Cast<UButton>(GetWidgetFromName(TEXT("TeamTab")));
	InventoryTab = Cast<UButton>(GetWidgetFromName(TEXT("InventoryTab")));
	CloseButton = Cast<UButton>(GetWidgetFromName(TEXT("CloseButton")));
	HudTeamRows = Cast<UVerticalBox>(GetWidgetFromName(TEXT("HudTeamRows")));
	MenuRows = Cast<UVerticalBox>(GetWidgetFromName(TEXT("MenuRows")));
	SectionTitle = Cast<UTextBlock>(GetWidgetFromName(TEXT("SectionTitle")));
	InteractionLabel = Cast<UTextBlock>(GetWidgetFromName(TEXT("InteractionPrompt")));
	HudLayer = Cast<UCanvasPanel>(GetWidgetFromName(TEXT("HudLayer")));
	MenuLayer = Cast<UCanvasPanel>(GetWidgetFromName(TEXT("MenuLayer")));
	if (InventoryButton) InventoryButton->OnClicked.AddUniqueDynamic(this,&UPokeMonsterOverworldWidget::OpenInventory);
	if (TeamTab) TeamTab->OnClicked.AddUniqueDynamic(this,&UPokeMonsterOverworldWidget::ShowTeam);
	if (InventoryTab) InventoryTab->OnClicked.AddUniqueDynamic(this,&UPokeMonsterOverworldWidget::ShowInventory);
	if (CloseButton) CloseButton->OnClicked.AddUniqueDynamic(this,&UPokeMonsterOverworldWidget::CloseMenu);
	SetIsFocusable(true);
	SetBattleVisible(bBattleVisible);
	SetMenuOpen(bMenuOpen, Section);
	Render();
}

FReply UPokeMonsterOverworldWidget::NativeOnKeyDown(const FGeometry& InGeometry, const FKeyEvent& InKeyEvent)
{
	if (bMenuOpen && InKeyEvent.GetKey() == EKeys::I)
	{
		ShowInventory();
		return FReply::Handled();
	}
	if (bMenuOpen && InKeyEvent.GetKey() == EKeys::T)
	{
		ShowTeam();
		return FReply::Handled();
	}
	if (bMenuOpen && (InKeyEvent.GetKey() == EKeys::Escape || InKeyEvent.GetKey() == EKeys::Tab))
	{
		CloseMenu();
		return FReply::Handled();
	}
	return Super::NativeOnKeyDown(InGeometry, InKeyEvent);
}

void UPokeMonsterOverworldWidget::SetMenuOpen(const bool bOpen, const EPokeMonsterOverworldMenuSection InitialSection)
{
	bMenuOpen = bOpen;
	Section = InitialSection;
	LastRenderKey.Reset();
	if (MenuLayer) MenuLayer->SetVisibility(bOpen ? ESlateVisibility::Visible : ESlateVisibility::Collapsed);
	if (HudLayer) HudLayer->SetVisibility(bOpen ? ESlateVisibility::Collapsed : ESlateVisibility::SelfHitTestInvisible);
	Render();
}

void UPokeMonsterOverworldWidget::SetBattleVisible(const bool bVisible)
{
	bBattleVisible = bVisible;
	SetVisibility(bVisible ? ESlateVisibility::Collapsed : ESlateVisibility::SelfHitTestInvisible);
}

void UPokeMonsterOverworldWidget::SetInteractionAvailable(const bool bAvailable)
{
	if (InteractionLabel) InteractionLabel->SetVisibility(bAvailable ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
}

void UPokeMonsterOverworldWidget::UpdateView(const FPokeMonsterOverworldView& NewView)
{
	View = NewView;
	Render();
	OnOverworldViewUpdated(View);
}

void UPokeMonsterOverworldWidget::Render()
{
	const FString Key = RenderKey(View, Section);
	if (Key == LastRenderKey || !WidgetTree || !HudTeamRows || !MenuRows) return;
	LastRenderKey = Key;
	const float HudHeight = 72.f + 29.f * FMath::Max(1, View.Team.Num());
	if (auto* Shadow = Cast<UImage>(GetWidgetFromName(TEXT("HudShadow"))))
		if (auto* Slot = Cast<UCanvasPanelSlot>(Shadow->Slot)) Slot->SetSize(FVector2D(320.f, HudHeight));
	if (auto* Plate = Cast<UImage>(GetWidgetFromName(TEXT("HudPlate"))))
		if (auto* Slot = Cast<UCanvasPanelSlot>(Plate->Slot)) Slot->SetSize(FVector2D(320.f, HudHeight));
	if (auto* Accent = Cast<UImage>(GetWidgetFromName(TEXT("HudAccent"))))
		if (auto* Slot = Cast<UCanvasPanelSlot>(Accent->Slot)) Slot->SetSize(FVector2D(6.f, HudHeight));
	if (auto* Slot = Cast<UCanvasPanelSlot>(HudTeamRows->Slot))
		Slot->SetSize(FVector2D(280.f, HudHeight - 72.f));
	HudTeamRows->ClearChildren();
	if (View.Team.IsEmpty())
		HudTeamRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Noch kein Team"),17,SoftInk));
	for (const auto& Row : View.Team)
	{
		const FString Line = FString::Printf(TEXT("%s  ·  Lv %d  ·  %s"), *Row.Name.ToString(),
			Row.Level, Row.bKnockedOut ? TEXT("K.O.")
				: *FString::Printf(TEXT("%d/%d HP"),Row.CurrentHP,Row.MaxHP));
		HudTeamRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,Line,16,
			Row.bKnockedOut ? FLinearColor(0.83f,0.56f,0.49f) : Ink));
	}
	if (SectionTitle) SectionTitle->SetText(FText::FromString(Section == EPokeMonsterOverworldMenuSection::Team
		? TEXT("Deine Kreaturen") : TEXT("Deine Gegenstände")));
	MenuRows->ClearChildren();
	if (Section == EPokeMonsterOverworldMenuSection::Team)
	{
		if (View.Team.IsEmpty())
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Noch keine Kreaturen im Team."),19,DarkInk));
		for (const auto& Row : View.Team)
		{
			const FString Line = FString::Printf(TEXT("%s     ·     Level %d     ·     %s"), *Row.Name.ToString(),
				Row.Level, Row.bKnockedOut ? TEXT("K.O.")
					: *FString::Printf(TEXT("%d / %d HP"),Row.CurrentHP,Row.MaxHP));
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,Line,21,
				Row.bKnockedOut ? FLinearColor(0.52f,0.25f,0.20f) : DarkInk));
		}
	}
	else
	{
		if (View.Inventory.IsEmpty())
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Die Tasche ist leer."),19,DarkInk));
		for (const auto& Row : View.Inventory)
		{
			const FString Line = FString::Printf(TEXT("%s     ·     %s     ·     × %d"),
				*Row.Name.ToString(),*Row.Category.ToString(),Row.Quantity);
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,Line,21,DarkInk));
		}
	}
}

void UPokeMonsterOverworldWidget::OpenInventory()
{
	if (APokeMonsterOverworldPlayerController* Controller = OwnerController.Get())
		Controller->OpenMenu(EPokeMonsterOverworldMenuSection::Inventory);
}

void UPokeMonsterOverworldWidget::ShowTeam()
{
	Section = EPokeMonsterOverworldMenuSection::Team;
	LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::ShowInventory()
{
	Section = EPokeMonsterOverworldMenuSection::Inventory;
	LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::CloseMenu()
{
	if (APokeMonsterOverworldPlayerController* Controller = OwnerController.Get()) Controller->CloseMenu();
}
