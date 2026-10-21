#include "PokeMonsterOverworldWidget.h"

#include "PokeMonsterOverworldPlayerController.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
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
	const FLinearColor OverworldInk(0.91f, 0.90f, 0.79f);
	const FLinearColor OverworldSoftInk(0.67f, 0.73f, 0.63f);
	const FLinearColor OverworldDarkInk(0.11f, 0.20f, 0.17f);
	const FLinearColor OverworldPine(0.09f, 0.17f, 0.14f, 0.94f);
	const FLinearColor OverworldLeaf(0.21f, 0.35f, 0.27f);
	const FLinearColor OverworldParchment(0.83f, 0.80f, 0.66f, 0.98f);

	UTextBlock* MakeText(UWidgetTree* Tree, const FName Name, const FString& Value, const int32 Size,
		const FLinearColor Color = OverworldInk)
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
		const FAnchors Anchors = FAnchors(0.f, 0.f), const int32 FontSize = 18)
	{
		auto* Button = Tree->ConstructWidget<UButton>(UButton::StaticClass(), Name);
		FButtonStyle Style;
		Style.SetNormal(FSlateRoundedBoxBrush(OverworldPine, 16.f));
		Style.SetHovered(FSlateRoundedBoxBrush(FLinearColor(0.16f, 0.27f, 0.20f, 0.98f), 16.f));
		Style.SetPressed(FSlateRoundedBoxBrush(FLinearColor(0.24f, 0.37f, 0.27f, 0.98f), 16.f));
		Button->SetStyle(Style);
		Button->AddChild(MakeText(Tree, NAME_None, Label, FontSize));
		Place(Canvas, Button, Position, Size, Anchors);
		return Button;
	}

	FString RenderKey(const FPokeMonsterOverworldView& View, const EPokeMonsterOverworldMenuSection Section)
	{
		FString Key = FString::FromInt(static_cast<int32>(Section));
		for (const auto& Row : View.Team)
			Key += Row.InstanceId.ToString() + FString::Printf(TEXT("|%s:%d:%d:%d:%d"), *Row.Name.ToString(), Row.Level,
				Row.CurrentHP, Row.MaxHP, Row.bKnockedOut ? 1 : 0);
	for (const auto& Row : View.Inventory)
			Key += FString::Printf(TEXT("|%s:%s:%d"), *Row.Name.ToString(),
				*Row.Category.ToString(), Row.Quantity);
		Key += TEXT("|Q:") + View.ActiveQuestName.ToString() + TEXT(":") + View.ActiveQuestObjective.ToString();
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
	Shape(WidgetTree, HudLayer, TEXT("HudShadow"), FVector2D(23,27), FVector2D(296,250),
		FLinearColor(0.01f,0.04f,0.03f,0.30f), 24.f);
	Shape(WidgetTree, HudLayer, TEXT("HudPlate"), FVector2D(20,24), FVector2D(296,250), OverworldPine, 22.f);
	Shape(WidgetTree, HudLayer, TEXT("HudAccent"), FVector2D(20,24), FVector2D(4,250), OverworldLeaf, 3.f);
	Place(HudLayer, MakeText(WidgetTree,TEXT("HudTitle"),TEXT("REISEGEFÄHRTEN"),14,OverworldSoftInk),
		FVector2D(38,35),FVector2D(260,22));
	HudTeamRows = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass(),TEXT("HudTeamRows"));
	Place(HudLayer,HudTeamRows,FVector2D(38,62),FVector2D(258,190));
	InventoryButton = MakeButton(WidgetTree,HudLayer,TEXT("InventoryButton"),TEXT("Tasche  ·  Tab"),
		FVector2D(-190,24),FVector2D(164,42),FAnchors(1.f,0.f),15);
	QuestPanel = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), TEXT("QuestPanel"));
	Place(HudLayer, QuestPanel, FVector2D(-330,78), FVector2D(304,83), FAnchors(1.f,0.f));
	Shape(WidgetTree, QuestPanel, TEXT("QuestPlate"), FVector2D::ZeroVector, FVector2D(304,83),
		FLinearColor(0.08f,0.17f,0.14f,0.83f), 17.f);
	Shape(WidgetTree, QuestPanel, TEXT("QuestAccent"), FVector2D(0,0), FVector2D(3,83), OverworldLeaf, 2.f);
	QuestTitle = MakeText(WidgetTree,TEXT("QuestTitle"),TEXT(""),16,OverworldInk);
	QuestObjective = MakeText(WidgetTree,TEXT("QuestObjective"),TEXT(""),14,OverworldSoftInk);
	Place(QuestPanel,QuestTitle,FVector2D(16,13),FVector2D(274,25));
	Place(QuestPanel,QuestObjective,FVector2D(16,42),FVector2D(274,28));
	QuestPanel->SetVisibility(ESlateVisibility::Collapsed);
	InteractionLabel = MakeText(WidgetTree,TEXT("InteractionPrompt"),TEXT("E  ·  Interagieren"),15,OverworldInk);
	Place(HudLayer,InteractionLabel,FVector2D(-119,-61),FVector2D(238,28),FAnchors(0.5f,1.f));
	InteractionLabel->SetVisibility(ESlateVisibility::Collapsed);

	MenuLayer = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(),TEXT("MenuLayer"));
	Place(Root, MenuLayer, FVector2D::ZeroVector, FVector2D::ZeroVector, FAnchors(0.f,0.f,1.f,1.f));
	if (auto* Slot = Cast<UCanvasPanelSlot>(MenuLayer->Slot)) Slot->SetOffsets(FMargin(0));
	Shape(WidgetTree,MenuLayer,TEXT("MenuDim"),FVector2D::ZeroVector,FVector2D::ZeroVector,
		FLinearColor(0.015f,0.035f,0.03f,0.57f),0.f,FAnchors(0.f,0.f,1.f,1.f));
	Shape(WidgetTree,MenuLayer,TEXT("MenuShadow"),FVector2D(-416,-280),FVector2D(832,580),
		FLinearColor(0.01f,0.035f,0.025f,0.53f),28.f,FAnchors(0.5f,0.5f));
	Shape(WidgetTree,MenuLayer,TEXT("MenuPlate"),FVector2D(-420,-288),FVector2D(832,580),
		OverworldParchment,27.f,FAnchors(0.5f,0.5f));
	Shape(WidgetTree,MenuLayer,TEXT("MenuHeader"),FVector2D(-420,-288),FVector2D(832,92),
		OverworldPine,25.f,FAnchors(0.5f,0.5f));
	Place(MenuLayer,MakeText(WidgetTree,TEXT("MenuTitle"),TEXT("REISEBUCH"),28,OverworldInk),
		FVector2D(-384,-263),FVector2D(280,42),FAnchors(0.5f,0.5f));
	CloseButton = MakeButton(WidgetTree,MenuLayer,TEXT("CloseButton"),TEXT("Schließen  ×"),
		FVector2D(224,-269),FVector2D(150,48),FAnchors(0.5f,0.5f));
	TeamTab = MakeButton(WidgetTree,MenuLayer,TEXT("TeamTab"),TEXT("Team"),
		FVector2D(-383,-173),FVector2D(170,49),FAnchors(0.5f,0.5f));
	InventoryTab = MakeButton(WidgetTree,MenuLayer,TEXT("InventoryTab"),TEXT("Inventar"),
		FVector2D(-201,-173),FVector2D(170,49),FAnchors(0.5f,0.5f));
	SectionTitle = MakeText(WidgetTree,TEXT("SectionTitle"),TEXT("Team"),23,OverworldDarkInk);
	Place(MenuLayer,SectionTitle,FVector2D(-378,-102),FVector2D(500,36),FAnchors(0.5f,0.5f));
	MenuRows = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass(),TEXT("MenuRows"));
	Place(MenuLayer,MenuRows,FVector2D(-380,-51),FVector2D(748,296),FAnchors(0.5f,0.5f));
	Place(MenuLayer,MakeText(WidgetTree,TEXT("MenuHint"),TEXT("↑↓: Platz · Interagieren: wählen/tauschen · ESC: zurück"),14,OverworldDarkInk),
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
	QuestPanel = Cast<UCanvasPanel>(GetWidgetFromName(TEXT("QuestPanel")));
	QuestTitle = Cast<UTextBlock>(GetWidgetFromName(TEXT("QuestTitle")));
	QuestObjective = Cast<UTextBlock>(GetWidgetFromName(TEXT("QuestObjective")));
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

FReply UPokeMonsterOverworldWidget::NativeOnPreviewKeyDown(const FGeometry& InGeometry, const FKeyEvent& InKeyEvent)
{
	const FKey Key = InKeyEvent.GetKey();
	if (bMenuOpen && Section == EPokeMonsterOverworldMenuSection::Team)
	{
		if (Key == EKeys::Up || Key == EKeys::Down || Key == EKeys::Gamepad_DPad_Up || Key == EKeys::Gamepad_DPad_Down)
		{
			FocusedTeamSlot = (FocusedTeamSlot + (Key == EKeys::Up || Key == EKeys::Gamepad_DPad_Up ? 5 : 1)) % 6;
			RefreshTeamFocus(); return FReply::Handled();
		}
		const auto* Player = OwnerController.IsValid() ? Cast<APokeMonsterPlayerCharacter>(OwnerController->GetPawn()) : nullptr;
		if (Player && Player->GetInteractionKeys().Contains(Key))
		{
			SelectTeamSlot(FocusedTeamSlot); return FReply::Handled();
		}
		if (Key == EKeys::Escape && SelectedInstanceId.IsValid())
		{
			SelectedInstanceId.Invalidate(); LastRenderKey.Reset(); Render(); return FReply::Handled();
		}
	}

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
	return Super::NativeOnPreviewKeyDown(InGeometry, InKeyEvent);
}

void UPokeMonsterOverworldWidget::SetMenuOpen(const bool bOpen, const EPokeMonsterOverworldMenuSection InitialSection)
{
	bMenuOpen = bOpen;
	SelectedInstanceId.Invalidate(); FocusedTeamSlot = 0;
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

void UPokeMonsterOverworldWidget::SetInteractionAvailable(const bool bAvailable,const FString& Action)
{
	if (InteractionLabel) {InteractionLabel->SetVisibility(bAvailable ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
  InteractionLabel->SetText(FText::FromString(Action.IsEmpty()?TEXT("E · Interagieren"):Action));}
}

void UPokeMonsterOverworldWidget::UpdateView(const FPokeMonsterOverworldView& NewView)
{
	View = NewView;
	Render();
	OnOverworldViewUpdated(View);
}

void UPokeMonsterOverworldWidget::Render()
{
	const FString Key = RenderKey(View, Section) + SelectedInstanceId.ToString();
	if (Key == LastRenderKey || !WidgetTree || !HudTeamRows || !MenuRows) return;
	LastRenderKey = Key;
	if (QuestPanel) QuestPanel->SetVisibility(View.ActiveQuestName.IsEmpty()
		? ESlateVisibility::Collapsed : ESlateVisibility::HitTestInvisible);
	if (QuestTitle) QuestTitle->SetText(View.ActiveQuestName);
	if (QuestObjective) QuestObjective->SetText(View.ActiveQuestObjective);
	const float HudHeight = 62.f + 27.f * FMath::Max(1, View.Team.Num());
	if (auto* Shadow = Cast<UImage>(GetWidgetFromName(TEXT("HudShadow"))))
		if (auto* Slot = Cast<UCanvasPanelSlot>(Shadow->Slot)) Slot->SetSize(FVector2D(296.f, HudHeight));
	if (auto* Plate = Cast<UImage>(GetWidgetFromName(TEXT("HudPlate"))))
		if (auto* Slot = Cast<UCanvasPanelSlot>(Plate->Slot)) Slot->SetSize(FVector2D(296.f, HudHeight));
	if (auto* Accent = Cast<UImage>(GetWidgetFromName(TEXT("HudAccent"))))
		if (auto* Slot = Cast<UCanvasPanelSlot>(Accent->Slot)) Slot->SetSize(FVector2D(4.f, HudHeight));
	if (auto* Slot = Cast<UCanvasPanelSlot>(HudTeamRows->Slot))
		Slot->SetSize(FVector2D(258.f, HudHeight - 62.f));
	HudTeamRows->ClearChildren();
	if (View.Team.IsEmpty())
		HudTeamRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Noch kein Team"),17,OverworldSoftInk));
	for (const auto& Row : View.Team)
	{
		const FString Line = FString::Printf(TEXT("%s  ·  Lv %d  ·  %s"), *Row.Name.ToString(),
			Row.Level, Row.bKnockedOut ? TEXT("K.O.")
				: *FString::Printf(TEXT("%d/%d HP"),Row.CurrentHP,Row.MaxHP));
		HudTeamRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,Line,15,
			Row.bKnockedOut ? FLinearColor(0.83f,0.56f,0.49f) : OverworldInk));
	}
	if (SectionTitle) SectionTitle->SetText(FText::FromString(Section == EPokeMonsterOverworldMenuSection::Team
		? TEXT("Deine Kreaturen") : TEXT("Deine Gegenstände")));
	TeamButtons.Reset();
	MenuRows->ClearChildren();
	if (Section == EPokeMonsterOverworldMenuSection::Team)
	{
		if (View.Team.IsEmpty())
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Noch keine Kreaturen im Team."),19,OverworldDarkInk));
		if (SelectedInstanceId.IsValid() && !View.Team.ContainsByPredicate([&](const auto& Row) { return Row.InstanceId == SelectedInstanceId; })) SelectedInstanceId.Invalidate();
		if (SectionTitle) SectionTitle->SetText(FText::FromString(SelectedInstanceId.IsValid()
			? TEXT("Zielplatz wählen · freie Plätze rücken ans Teamende") : TEXT("Pokémon wählen · danach Zielplatz")));
		for (int32 Index = 0; Index < 6; ++Index)
		{
			const auto* Row = View.Team.IsValidIndex(Index) ? &View.Team[Index] : nullptr;
			const FString Line = Row ? FString::Printf(TEXT("%d  %s%s  ·  Lv %d  ·  %d/%d KP"), Index+1,
				Row->InstanceId == SelectedInstanceId ? TEXT("↔ ") : TEXT(""), *Row->Name.ToString(), Row->Level, Row->CurrentHP, Row->MaxHP)
				: FString::Printf(TEXT("%d  Frei%s"), Index+1, SelectedInstanceId.IsValid() ? TEXT(" · ans Teamende verschieben") : TEXT(""));
			auto* Button = WidgetTree->ConstructWidget<UButton>(UButton::StaticClass());
			Button->AddChild(MakeText(WidgetTree, NAME_None, Line, 19, OverworldDarkInk));
			MenuRows->AddChildToVerticalBox(Button); TeamButtons.Add(Button);
		}
		TeamButtons[0]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::Team0);
		TeamButtons[1]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::Team1);
		TeamButtons[2]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::Team2);
		TeamButtons[3]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::Team3);
		TeamButtons[4]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::Team4);
		TeamButtons[5]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::Team5);
		RefreshTeamFocus();
	}
	else
	{
		if (View.Inventory.IsEmpty())
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Die Tasche ist leer."),19,OverworldDarkInk));
		for (const auto& Row : View.Inventory)
		{
			const FString Line = FString::Printf(TEXT("%s     ·     %s     ·     × %d"),
				*Row.Name.ToString(),*Row.Category.ToString(),Row.Quantity);
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,Line,21,OverworldDarkInk));
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
	SelectedInstanceId.Invalidate();
	Section = EPokeMonsterOverworldMenuSection::Inventory;
	LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::CloseMenu()
{
	if (APokeMonsterOverworldPlayerController* Controller = OwnerController.Get()) Controller->CloseMenu();
}

void UPokeMonsterOverworldWidget::RefreshTeamFocus()
{
	for (int32 Index=0; Index<TeamButtons.Num(); ++Index)
		if (TeamButtons[Index]) TeamButtons[Index]->SetBackgroundColor(Index == FocusedTeamSlot
			? FLinearColor(.40f,.67f,.45f) : FLinearColor(.78f,.79f,.65f));
}

bool UPokeMonsterOverworldWidget::SelectTeamSlot(const int32 Slot)
{
	if (!bMenuOpen || bBattleVisible || Section != EPokeMonsterOverworldMenuSection::Team || Slot < 0 || Slot >= 6) return false;
	FocusedTeamSlot = Slot;
	if (!SelectedInstanceId.IsValid())
	{
		if (!View.Team.IsValidIndex(Slot)) return false;
		SelectedInstanceId = View.Team[Slot].InstanceId;
	}
	else
	{
		const FGuid Source = SelectedInstanceId;
		SelectedInstanceId.Invalidate();
		const bool bChanged = OwnerController.IsValid() && OwnerController->ReorderParty(Source, Slot);
		LastRenderKey.Reset(); Render(); return bChanged;
	}
	LastRenderKey.Reset(); Render(); return true;
}

FNavigationReply UPokeMonsterOverworldWidget::NativeOnNavigation(const FGeometry& Geometry, const FNavigationEvent& Event)
{
	if (bMenuOpen && Section == EPokeMonsterOverworldMenuSection::Team)
	{
		const auto Direction = Event.GetNavigationType();
		FocusedTeamSlot = (FocusedTeamSlot + (Direction == EUINavigation::Up || Direction == EUINavigation::Previous ? 5 : 1)) % 6;
		RefreshTeamFocus(); return FNavigationReply::Stop();
	}
	return Super::NativeOnNavigation(Geometry, Event);
}
void UPokeMonsterOverworldWidget::Team0(){SelectTeamSlot(0);} void UPokeMonsterOverworldWidget::Team1(){SelectTeamSlot(1);}
void UPokeMonsterOverworldWidget::Team2(){SelectTeamSlot(2);} void UPokeMonsterOverworldWidget::Team3(){SelectTeamSlot(3);}
void UPokeMonsterOverworldWidget::Team4(){SelectTeamSlot(4);} void UPokeMonsterOverworldWidget::Team5(){SelectTeamSlot(5);}
