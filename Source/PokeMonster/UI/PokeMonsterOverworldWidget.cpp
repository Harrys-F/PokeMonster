#include "PokeMonsterOverworldWidget.h"
#include "PokeMonsterControllerInput.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Items/PokeMonsterItemData.h"
#include "../Moves/PokeMonsterMoveData.h"

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
  for (const auto& Row:View.Team)for(const auto& M:Row.Repertoire)
   Key+=M.Move.ToSoftObjectPath().ToString()+FString::Printf(TEXT(":%d:%d"),M.CurrentPP,M.ActiveSlot);
  for (const auto& Row:View.Team) Key+=Row.bPendingLearning?TEXT("pending"):TEXT("ready");
	for (const auto& Row : View.Inventory)
			Key += FString::Printf(TEXT("|%s:%s:%d"), *Row.Name.ToString(),
				*Row.Category.ToString(), Row.Quantity) + Row.Item.ToSoftObjectPath().ToString();
		Key += TEXT("|Q:") + View.ActiveQuestName.ToString() + TEXT(":") + View.ActiveQuestObjective.ToString();
		return Key;
	}
}

void UPokeMonsterOverworldWidget::SetOwnerController(APokeMonsterOverworldPlayerController* InController)
{ OwnerController = InController; }

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
 MovesTab=MakeButton(WidgetTree,MenuLayer,TEXT("MovesTab"),TEXT("Attacken"),FVector2D(-19,-173),FVector2D(170,49),FAnchors(.5f,.5f));
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
 MovesTab=Cast<UButton>(GetWidgetFromName(TEXT("MovesTab")));
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
	if(MovesTab)MovesTab->OnClicked.AddUniqueDynamic(this,&UPokeMonsterOverworldWidget::ShowMoves);
 if (CloseButton) CloseButton->OnClicked.AddUniqueDynamic(this,&UPokeMonsterOverworldWidget::CloseMenu);
	SetIsFocusable(true);
	SetBattleVisible(bBattleVisible);
	SetMenuOpen(bMenuOpen, Section);
	Render();
}

FReply UPokeMonsterOverworldWidget::NativeOnPreviewKeyDown(const FGeometry& Geometry, const FKeyEvent& Event)
{
 if (!bMenuOpen || bBattleVisible) return Super::NativeOnPreviewKeyDown(Geometry, Event);
 const FKey Key = Event.GetKey();
 PokeMonsterControllerInput::ObserveKey(Key);
 const bool bConfirm = Key == PokeMonsterControllerInput::Confirm() || Key == EKeys::Enter
  || Key == EKeys::E || Key == EKeys::SpaceBar;
 const bool bCancel = Key == PokeMonsterControllerInput::Cancel() || Key == EKeys::Escape;
 if (bConfirm) { if (!Event.IsRepeat()) ConfirmMenu(); return FReply::Handled(); }
 if (bCancel)
 {
  if (!Event.IsRepeat())
  {
   if (PendingStorageAction) CancelStorage();
   else if(Section==EPokeMonsterOverworldMenuSection::Moves) CancelMoves();
   else if (PendingHealingItem) { PendingHealingItem=nullptr; ShowInventory(); }
   else if (SelectedInstanceId.IsValid()) { SelectedInstanceId.Invalidate(); LastRenderKey.Reset(); Render(); }
   else CloseMenu();
  }
  return FReply::Handled();
 }
 if (Key == EKeys::Gamepad_Special_Right || Key == EKeys::Tab)
 { if (!Event.IsRepeat()) CloseMenu(); return FReply::Handled(); }
 // X opens once; a held/repeated X cannot close and reopen the same menu.
 if (Key == PokeMonsterControllerInput::QuickMenu() || Key == EKeys::Gamepad_LeftThumbstick)
  return FReply::Handled();
 if (Key == EKeys::Gamepad_LeftShoulder || Key == EKeys::Gamepad_RightShoulder)
 {
  if (!Event.IsRepeat() && !bMoveMasterMode && !PendingStorageAction)
  {
   const bool Next=Key==EKeys::Gamepad_RightShoulder;
   if(Section==EPokeMonsterOverworldMenuSection::Team) {if(Next)ShowInventory();else ShowMoves();}
   else if(Section==EPokeMonsterOverworldMenuSection::Inventory) {if(Next)ShowMoves();else ShowTeam();}
   else {if(Next)ShowTeam();else ShowInventory();}
  }
  return FReply::Handled();
 }
 if (Key == EKeys::I || Key == EKeys::T)
 { if (!Event.IsRepeat() && !bMoveMasterMode && !PendingStorageAction) { if (Key == EKeys::I) ShowInventory(); else ShowTeam(); } return FReply::Handled(); }
 if (Key == EKeys::Up || Key == EKeys::Left || Key == EKeys::Gamepad_DPad_Up || Key == EKeys::Gamepad_DPad_Left)
 { NavigateMenu(-1); return FReply::Handled(); }
 if (Key == EKeys::Down || Key == EKeys::Right || Key == EKeys::Gamepad_DPad_Down || Key == EKeys::Gamepad_DPad_Right)
 { NavigateMenu(1); return FReply::Handled(); }
 return Super::NativeOnPreviewKeyDown(Geometry, Event);
}

void UPokeMonsterOverworldWidget::NavigateMenu(int32 Delta)
{
 if(Section==EPokeMonsterOverworldMenuSection::Moves)
 {
  if(bChoosingMovePokemon && !View.Team.IsEmpty())MovePokemon=(MovePokemon+Delta+View.Team.Num())%View.Team.Num();
  else if(ReplaceCursor!=INDEX_NONE)ReplaceCursor=(ReplaceCursor+Delta+4)%4;
  else if(!bMoveReview && View.Team.IsValidIndex(MovePokemon)) {const int32 N=View.Team[MovePokemon].Repertoire.Num()+1;MoveCursor=(MoveCursor+Delta+N)%N;}
  LastRenderKey.Reset();Render();
 }
 else if (Section == EPokeMonsterOverworldMenuSection::Team)
 { FocusedTeamSlot = (FocusedTeamSlot + Delta + 6) % 6; RefreshTeamFocus(); }
 else if (Section == EPokeMonsterOverworldMenuSection::Inventory)
 { if (!View.Inventory.IsEmpty()) FocusedInventorySlot = (FocusedInventorySlot + Delta + View.Inventory.Num()) % View.Inventory.Num(); LastRenderKey.Reset(); Render(); }
 else
 {
  const int32 Count = FMath::Max(1, MainButtons.Num());
  FocusedMainSlot = (FocusedMainSlot + Delta + Count) % Count;
  for (int32 I=0; I<MainButtons.Num(); ++I) if (MainButtons[I])
   MainButtons[I]->SetBackgroundColor(I==FocusedMainSlot?FLinearColor(.40f,.67f,.45f):FLinearColor(.78f,.79f,.65f));
 }
}

void UPokeMonsterOverworldWidget::ConfirmMenu()
{
 if (bStorageBusy) return;
 if (PendingStorageAction)
 {
  if (FocusedMainSlot == 0) ConfirmStorage(); else CancelStorage();
 }
 else if(Section==EPokeMonsterOverworldMenuSection::Moves)ConfirmMoves();
 else if (Section == EPokeMonsterOverworldMenuSection::Team) SelectTeamSlot(FocusedTeamSlot);
 else if (Section == EPokeMonsterOverworldMenuSection::Main)
 {
  if (FocusedMainSlot==0) ShowTeam();
  else if (FocusedMainSlot==1) ShowInventory();
  else if (FocusedMainSlot==2) SaveGame();
  else if (FocusedMainSlot==3) LoadGame();
  else if (FocusedMainSlot==4) LoadRecoveryGame();
  else CloseMenu();
 }
 else if (View.Inventory.IsValidIndex(FocusedInventorySlot))
 {
  auto* Item=View.Inventory[FocusedInventorySlot].Item.LoadSynchronous();
  if (Item && Item->CanUseInOverworld() && Item->GetCategory()==EPokeMonsterItemCategory::Healing)
  {
   PendingHealingItem=Item; SelectedInstanceId.Invalidate(); ShowTeam();
  }
  else if (SectionTitle) SectionTitle->SetText(FText::FromString(View.Inventory[FocusedInventorySlot].Name.ToString()+TEXT(" · Hier nicht verwendbar")));
 }
}

void UPokeMonsterOverworldWidget::SaveGame()
{
 if (!bMenuOpen || Section != EPokeMonsterOverworldMenuSection::Main || bStorageBusy
  || LastStorageInputFrame == GFrameCounter) return;
 LastStorageInputFrame = GFrameCounter;
 PendingStorageAction = 1; FocusedMainSlot = 0;
 StorageMessage = TEXT("Speichern bestätigen");
 LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::LoadGame()
{
 if (!bMenuOpen || Section != EPokeMonsterOverworldMenuSection::Main || bStorageBusy
  || LastStorageInputFrame == GFrameCounter) return;
 LastStorageInputFrame = GFrameCounter;
 auto* C = OwnerController.Get();
 auto* Save = C && C->GetGameInstance() ? C->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>() : nullptr;
 if (!Save || !Save->HasSaveGame()) StorageMessage = TEXT("Kein manueller Spielstand vorhanden");
 else { PendingStorageAction = 2; FocusedMainSlot = 0; StorageMessage = TEXT("Spielstand laden?"); }
 LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::LoadRecoveryGame()
{
 if (!bMenuOpen || Section != EPokeMonsterOverworldMenuSection::Main || bStorageBusy
  || LastStorageInputFrame == GFrameCounter) return;
 LastStorageInputFrame = GFrameCounter;
 auto* C = OwnerController.Get();
 auto* Save = C && C->GetGameInstance() ? C->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>() : nullptr;
 if (!Save || !Save->HasRecoveryGame()) StorageMessage = TEXT("Kein automatischer Stand vorhanden");
 else { PendingStorageAction = 3; FocusedMainSlot = 0; StorageMessage = TEXT("Automatischen Stand laden?"); }
 LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::CancelStorage()
{
 if (bStorageBusy) return;
 PendingStorageAction = 0; FocusedMainSlot = 0; StorageMessage = TEXT("Abgebrochen · Daten unverändert");
 LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::ConfirmStorage()
{
 if (!PendingStorageAction || bStorageBusy || LastStorageInputFrame == GFrameCounter) return;
 LastStorageInputFrame = GFrameCounter;
 TGuardValue<bool> Busy(bStorageBusy, true);
 const int32 Action = PendingStorageAction; PendingStorageAction = 0;
 auto* C = OwnerController.Get();
 auto* Save = C && C->GetGameInstance() ? C->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>() : nullptr;
 const bool Success = Save && (Action == 1 ? Save->SaveCurrentGame() : Action == 2 ? Save->LoadGame() : Save->LoadRecoveryGame());
 StorageMessage = Save ? Save->GetLastStorageMessage() : TEXT("Speicherdienst nicht verfügbar");
 if (Success && Action != 1 && C) { C->CloseMenu(); return; }
 FocusedMainSlot = 0; LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::SetMenuOpen(const bool bOpen, const EPokeMonsterOverworldMenuSection InitialSection)
{
	bMenuOpen = bOpen;
 PendingStorageAction = 0; StorageMessage.Reset(); LastStorageInputFrame = MAX_uint64;
 bMoveMasterMode=false; bChoosingMovePokemon=true;bMoveReview=false;MovePokemon=0;MoveCursor=0;ReplaceCursor=INDEX_NONE;DraftMoves.Reset();MoveMessage.Reset();
	SelectedInstanceId.Invalidate(); PendingHealingItem=nullptr; FocusedTeamSlot = 0; FocusedMainSlot = 0; FocusedInventorySlot = 0;
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
  InteractionLabel->SetText(FText::FromString((PokeMonsterControllerInput::IsGamepadActive()?TEXT("B · "):TEXT("E · ")) + (Action.IsEmpty()?FString(TEXT("Interagieren")):Action)));}
}

void UPokeMonsterOverworldWidget::UpdateView(const FPokeMonsterOverworldView& NewView)
{
	View = NewView;
	Render();
	OnOverworldViewUpdated(View);
}

void UPokeMonsterOverworldWidget::Render()
{
	FString Key = StorageMessage + FString::FromInt(PendingStorageAction) + RenderKey(View, Section) + SelectedInstanceId.ToString() + (PokeMonsterControllerInput::IsGamepadActive()?TEXT("Gamepad"):TEXT("Keyboard"));
	Key+=FString::Printf(TEXT("|m%d:%d:%d:%d:%d:%d"),bMoveMasterMode,bChoosingMovePokemon,bMoveReview,MovePokemon,MoveCursor,ReplaceCursor)+MoveMessage;
 for(const auto& M:DraftMoves)Key+=M.ToSoftObjectPath().ToString();
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
 TeamButtons.Reset(); MainButtons.Reset();
 if (auto* Hint=Cast<UTextBlock>(GetWidgetFromName(TEXT("MenuHint")))) Hint->SetText(FText::FromString(
  PokeMonsterControllerInput::IsGamepadActive()?TEXT("B: wählen · A: zurück · L/R: Team / Beutel · +: schließen"):TEXT("↑↓: wählen · E / Enter: bestätigen · T/I: Kategorien · Esc: zurück")));
 if (InventoryButton) if (auto* Label=Cast<UTextBlock>(InventoryButton->GetContent()))
  Label->SetText(FText::FromString(PokeMonsterControllerInput::IsGamepadActive()?TEXT("Team / Beutel · X"):TEXT("Team / Beutel · Tab")));
 MenuRows->ClearChildren();
 if(TeamTab)TeamTab->SetVisibility(bMoveMasterMode?ESlateVisibility::Collapsed:ESlateVisibility::Visible);
 if(InventoryTab)InventoryTab->SetVisibility(bMoveMasterMode?ESlateVisibility::Collapsed:ESlateVisibility::Visible);
 if(MovesTab)MovesTab->SetVisibility(bMoveMasterMode?ESlateVisibility::Collapsed:ESlateVisibility::Visible);
 if(Section==EPokeMonsterOverworldMenuSection::Moves){RenderMoves();return;}
	if (Section == EPokeMonsterOverworldMenuSection::Team)
	{
		if (View.Team.IsEmpty())
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Noch keine Kreaturen im Team."),19,OverworldDarkInk));
		if (SelectedInstanceId.IsValid() && !View.Team.ContainsByPredicate([&](const auto& Row) { return Row.InstanceId == SelectedInstanceId; })) SelectedInstanceId.Invalidate();
		if (SectionTitle) SectionTitle->SetText(FText::FromString(PendingHealingItem
   ? PendingHealingItem->GetDisplayName().ToString()+TEXT(" · Ziel wählen")
   : SelectedInstanceId.IsValid()?FString(TEXT("Zielplatz wählen · freie Plätze rücken ans Teamende")):FString(TEXT("Pokémon wählen · danach Zielplatz"))));
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
 else if (Section == EPokeMonsterOverworldMenuSection::Main)
 {
  if (SectionTitle) SectionTitle->SetText(FText::FromString(StorageMessage.IsEmpty() ? TEXT("Hauptmenü") : StorageMessage));
  if (PendingStorageAction)
  {
   auto* Note = MakeText(WidgetTree, NAME_None, PendingStorageAction == 1
    ? TEXT("Der manuelle Slot wird ersetzt. Rückkehrpunkt und Rettungsstand bleiben erhalten.")
    : (PendingStorageAction == 2 ? TEXT("Ungespeicherte Änderungen werden verworfen. Der manuelle Weltstand wird geladen.")
    : TEXT("Letzten automatischen Stand laden. Der manuelle Spielstand bleibt erhalten.")), 17, OverworldDarkInk);
   Note->SetWrapTextAt(720.f); MenuRows->AddChildToVerticalBox(Note);
   for (const FString& Label : {FString(TEXT("Bestätigen")), FString(TEXT("Abbrechen"))})
   {
    auto* B = WidgetTree->ConstructWidget<UButton>();
    B->AddChild(MakeText(WidgetTree, NAME_None, Label, 22, OverworldDarkInk));
    MenuRows->AddChildToVerticalBox(B); MainButtons.Add(B);
   }
   MainButtons[0]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::ConfirmStorage);
   MainButtons[1]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::CancelStorage);
   NavigateMenu(0); return;
  }
  for (const FString& Label : {FString(TEXT("Team")), FString(TEXT("Beutel")), FString(TEXT("Speichern")), FString(TEXT("Laden")), FString(TEXT("Automatischen Stand laden")), FString(TEXT("Fortsetzen"))})
  {
   auto* B=WidgetTree->ConstructWidget<UButton>();
   B->AddChild(MakeText(WidgetTree, NAME_None, Label, 22, OverworldDarkInk));
   MenuRows->AddChildToVerticalBox(B); MainButtons.Add(B);
  }
  MainButtons[0]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::ShowTeam);
  MainButtons[1]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::ShowInventory);
  MainButtons[2]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::SaveGame);
  MainButtons[3]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::LoadGame);
  MainButtons[4]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::LoadRecoveryGame);
  MainButtons[5]->OnClicked.AddUniqueDynamic(this, &UPokeMonsterOverworldWidget::CloseMenu);
  NavigateMenu(0);
 }
 else
 {
  FocusedInventorySlot=FMath::Clamp(FocusedInventorySlot,0,FMath::Max(0,View.Inventory.Num()-1));
  if (View.Inventory.IsEmpty())
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,TEXT("Die Tasche ist leer."),19,OverworldDarkInk));
		for (int32 Index=0; Index<View.Inventory.Num(); ++Index)
		{
   const auto& Row=View.Inventory[Index];
			const FString Line = FString::Printf(TEXT("%s     ·     %s     ·     × %d"),
				*Row.Name.ToString(),*Row.Category.ToString(),Row.Quantity);
			MenuRows->AddChildToVerticalBox(MakeText(WidgetTree,NAME_None,(Index==FocusedInventorySlot?TEXT("› "):TEXT("  "))+Line,21,OverworldDarkInk));
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
 if (bStorageBusy || PendingStorageAction) return;
 if(bMoveMasterMode)return;
	Section = EPokeMonsterOverworldMenuSection::Team;
	LastRenderKey.Reset(); Render();
}

void UPokeMonsterOverworldWidget::ShowInventory()
{
 if (bStorageBusy || PendingStorageAction) return;
 if(bMoveMasterMode)return;
 PendingHealingItem=nullptr;
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
 if (PendingHealingItem)
 {
  const bool bUsed=View.Team.IsValidIndex(Slot) && OwnerController.IsValid() && OwnerController->UseMenuHealingItem(PendingHealingItem,Slot);
  if (bUsed) { PendingHealingItem=nullptr; ShowInventory(); }
  else if (SectionTitle) SectionTitle->SetText(FText::FromString(TEXT("Ungültiges Ziel · kein Item verbraucht")));
  return bUsed;
 }
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
 if (!bMenuOpen || bBattleVisible) return Super::NativeOnNavigation(Geometry, Event);
 const auto Direction=Event.GetNavigationType();
 if (Direction==EUINavigation::Up || Direction==EUINavigation::Left || Direction==EUINavigation::Previous) NavigateMenu(-1);
 else if (Direction==EUINavigation::Down || Direction==EUINavigation::Right || Direction==EUINavigation::Next) NavigateMenu(1);
 return FNavigationReply::Stop();
}
void UPokeMonsterOverworldWidget::Team0(){SelectTeamSlot(0);} void UPokeMonsterOverworldWidget::Team1(){SelectTeamSlot(1);}
void UPokeMonsterOverworldWidget::Team2(){SelectTeamSlot(2);} void UPokeMonsterOverworldWidget::Team3(){SelectTeamSlot(3);}
void UPokeMonsterOverworldWidget::Team4(){SelectTeamSlot(4);} void UPokeMonsterOverworldWidget::Team5(){SelectTeamSlot(5);}

void UPokeMonsterOverworldWidget::SetMoveMasterMode(bool bEnabled)
{
 bMoveMasterMode=bEnabled; Section=EPokeMonsterOverworldMenuSection::Moves;
 bChoosingMovePokemon=true;bMoveReview=false;MovePokemon=0;MoveCursor=0;ReplaceCursor=INDEX_NONE;DraftMoves.Reset();MoveMessage.Reset();
 LastRenderKey.Reset();Render();
}

void UPokeMonsterOverworldWidget::ShowMoves()
{
 if (bStorageBusy || PendingStorageAction) return;
 if(bMoveMasterMode)return;
 PendingHealingItem=nullptr;SelectedInstanceId.Invalidate();Section=EPokeMonsterOverworldMenuSection::Moves;
 bChoosingMovePokemon=true;MovePokemon=FMath::Clamp(FocusedTeamSlot,0,FMath::Max(0,View.Team.Num()-1));MoveCursor=0;
 LastRenderKey.Reset();Render();
}

void UPokeMonsterOverworldWidget::RenderMoves()
{
 if(SectionTitle)SectionTitle->SetText(FText::FromString(bMoveMasterMode?TEXT("Meister der Erinnerungen"):TEXT("Attackenrepertoire · Nur Ansicht")));
 auto Add=[&](const FString& T,int Size=17)
 {
  auto* Text=MakeText(WidgetTree,NAME_None,T,Size,OverworldDarkInk);
  Text->SetWrapTextAt(728.f);
  MenuRows->AddChildToVerticalBox(Text);
 };
 if(auto* Hint=Cast<UTextBlock>(GetWidgetFromName(TEXT("MenuHint"))))Hint->SetText(FText::FromString(
  bMoveMasterMode?TEXT("↑↓ / Steuerkreuz · B / Enter: wählen · A / Esc: zurück · kostenlos"):TEXT("↑↓ / Steuerkreuz · B / Enter: ansehen · A / Esc: zurück · L/R: Kategorien")));
 if(bChoosingMovePokemon)
 {
  Add(bMoveMasterMode?TEXT("Wessen erlernte Attacken möchtest du neu zusammenstellen?"):TEXT("Pokémon auswählen · aktive Attacken und alle Erinnerungen"));
  for(int32 I=0;I<View.Team.Num();++I)Add(FString::Printf(TEXT("%s %s · Lv %d"),I==MovePokemon?TEXT("›"):TEXT(" "),*View.Team[I].Name.ToString(),View.Team[I].Level),21);
  if(View.Team.IsEmpty())Add(TEXT("Noch kein Team vorhanden."));
 }
 else if(View.Team.IsValidIndex(MovePokemon))
 {
  const auto& C=View.Team[MovePokemon];
  Add(C.Name.ToString()+TEXT(" · ")+(bMoveReview?TEXT("Änderungen prüfen"):bMoveMasterMode?TEXT("Entwurf · noch nicht gespeichert"):TEXT("Persönliche Erinnerungen")),19);
  const auto& Active=bMoveMasterMode?DraftMoves:C.ActiveMoves;
  FString Slots;
  for(int32 I=0;I<4;++I){const auto* M=Active.IsValidIndex(I)?Active[I].LoadSynchronous():nullptr;Slots+=FString::Printf(TEXT("%d %s%s"),I+1,M?*M->GetPlayerFacingName().ToString():TEXT("—"),I==3?TEXT(""):TEXT("   ·   "));}
  Add(Slots,16);
  if(bMoveReview)
  {
   Add(TEXT("Nur aktive Plätze ändern sich. Alle erlernten Attacken bleiben erhalten."));
   Add(TEXT("AP bleiben erhalten. Nicht erlernte Attacken werden nicht freigeschaltet."));
   Add(TEXT("B / Enter: verbindlich übernehmen und speichern"),20);
   Add(TEXT("A / Esc: zurück zum Entwurf · Schließen: alles verwerfen"));
  }
  else if(ReplaceCursor!=INDEX_NONE)
  {
   Add(TEXT("Vier Plätze belegt · welchen aktiven Platz ersetzen?"),20);
   for(int32 I=0;I<4;++I){const auto* M=DraftMoves.IsValidIndex(I)?DraftMoves[I].LoadSynchronous():nullptr;Add(FString::Printf(TEXT("%s %d · %s"),I==ReplaceCursor?TEXT("›"):TEXT(" "),I+1,M?*M->GetPlayerFacingName().ToString():TEXT("—")),20);}
  }
  else
  {
   const int32 N=C.Repertoire.Num();const int32 Start=FMath::Clamp(MoveCursor-2,0,FMath::Max(0,N-4));
   for(int32 I=Start;I<FMath::Min(N,Start+4);++I)
   {
    const auto& M=C.Repertoire[I];const int32 Slot=Active.IndexOfByKey(M.Move);
    Add(FString::Printf(TEXT("%s %s%s · %s · AP %d/%d"),I==MoveCursor?TEXT("›"):TEXT(" "),*M.Name.ToString(),Slot!=INDEX_NONE?*FString::Printf(TEXT(" [%d]"),Slot+1):TEXT(" [inaktiv]"),*M.Type.ToString(),M.CurrentPP,M.MaxPP),18);
   }
   if(C.Repertoire.IsValidIndex(MoveCursor))
   {
    const auto& M=C.Repertoire[MoveCursor];Add(FString::Printf(TEXT("Stärke %d · Genauigkeit %d %% · %s"),M.Power,M.Accuracy,*M.Effect.ToString()),15);
   }
   Add((MoveCursor==N?TEXT("› "):TEXT("  "))+FString(bMoveMasterMode?TEXT("Entwurf prüfen → bestätigen / speichern"):TEXT("Zur Pokémon-Auswahl")),18);
  }
 }
 if(!MoveMessage.IsEmpty())Add(MoveMessage,15);
 // One explicit mouse action shares the same state machine as keyboard/controller confirmation.
 MoveActionButton=WidgetTree->ConstructWidget<UButton>();
 MoveActionButton->AddChild(MakeText(WidgetTree,NAME_None,TEXT("Auswahl bestätigen"),16,OverworldDarkInk));
 MoveActionButton->OnClicked.AddUniqueDynamic(this,&UPokeMonsterOverworldWidget::ConfirmMoves);
 MenuRows->AddChildToVerticalBox(MoveActionButton);
}

void UPokeMonsterOverworldWidget::ConfirmMoves()
{
 if(Section!=EPokeMonsterOverworldMenuSection::Moves || !bMenuOpen || bBattleVisible)return;
 MoveMessage.Reset();
 if(bChoosingMovePokemon)
 {
  if(!View.Team.IsValidIndex(MovePokemon))return;
  if(bMoveMasterMode && View.Team[MovePokemon].bPendingLearning){MoveMessage=TEXT("Zuerst das offene Lernangebot im Fortschrittssystem entscheiden.");}
  else {bChoosingMovePokemon=false;MoveCursor=0;DraftMoves.Reset();for(const auto& M:View.Team[MovePokemon].ActiveMoves)if(!M.IsNull())DraftMoves.AddUnique(M);}
 }
 else if(View.Team.IsValidIndex(MovePokemon))
 {
  const auto& C=View.Team[MovePokemon];
  if(bMoveReview)
  {
   if(OwnerController.IsValid() && OwnerController->CommitMoveMaster(C.InstanceId,DraftMoves))return;
   MoveMessage=TEXT("Nicht übernommen: Meister, Pokémon-Daten oder Speicherung prüfen.");
  }
  else if(ReplaceCursor!=INDEX_NONE && C.Repertoire.IsValidIndex(MoveCursor))
  {DraftMoves[ReplaceCursor]=C.Repertoire[MoveCursor].Move;ReplaceCursor=INDEX_NONE;}
  else if(MoveCursor==C.Repertoire.Num())
  {
   if(!bMoveMasterMode)bChoosingMovePokemon=true;
   else if(DraftMoves.IsEmpty())MoveMessage=TEXT("Mindestens eine aktive Attacke wählen.");
   else bMoveReview=true;
  }
  else if(C.Repertoire.IsValidIndex(MoveCursor))
  {
   const auto M=C.Repertoire[MoveCursor].Move;
   if(!bMoveMasterMode)MoveMessage=TEXT("Diese Attacke kann bei einem Meister der Erinnerungen wieder aktiviert werden.");
   else if(DraftMoves.Contains(M))DraftMoves.Remove(M);
   else if(DraftMoves.Num()<4)DraftMoves.Add(M);
   else ReplaceCursor=0;
  }
 }
 LastRenderKey.Reset();Render();
}

void UPokeMonsterOverworldWidget::CancelMoves()
{
 MoveMessage.Reset();
 if(bMoveReview)bMoveReview=false;
 else if(ReplaceCursor!=INDEX_NONE)ReplaceCursor=INDEX_NONE;
 else if(!bChoosingMovePokemon){bChoosingMovePokemon=true;DraftMoves.Reset();}
 else if(bMoveMasterMode)CloseMenu();
 else ShowTeam();
 LastRenderKey.Reset();Render();
}
