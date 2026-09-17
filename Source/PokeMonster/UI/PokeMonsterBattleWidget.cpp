#include "PokeMonsterBattleWidget.h"
#include "PokeMonsterBattleTestController.h"
#include "Blueprint/WidgetTree.h"
#include "Components/Border.h"
#include "Components/Button.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/ProgressBar.h"
#include "Components/ScaleBox.h"
#include "Components/ScrollBox.h"
#include "Components/SizeBox.h"
#include "Components/TextBlock.h"
#include "Brushes/SlateRoundedBoxBrush.h"
#include "Styling/CoreStyle.h"

namespace
{
	const FLinearColor Ink(0.85f, 0.89f, 0.81f);
	const FLinearColor Muted(0.47f, 0.59f, 0.53f);
	void Place(UCanvasPanel* Canvas, UWidget* Widget, float X, float Y, float W, float H)
	{
		auto* Slot = Canvas->AddChildToCanvas(Widget);
		Slot->SetPosition(FVector2D(X,Y)); Slot->SetSize(FVector2D(W,H));
	}
	UTextBlock* Text(UWidgetTree* Tree, FName Name, const FString& Value, int32 Size, FLinearColor Color = Ink)
	{
		auto* Widget = Tree->ConstructWidget<UTextBlock>(UTextBlock::StaticClass(), Name);
		Widget->SetText(FText::FromString(Value));
		Widget->SetFont(FCoreStyle::GetDefaultFontStyle(TEXT("Regular"), Size));
		Widget->SetColorAndOpacity(FSlateColor(Color));
		Widget->SetVisibility(ESlateVisibility::HitTestInvisible);
		return Widget;
	}
	UImage* Shape(UWidgetTree* Tree, UCanvasPanel* Canvas, float X, float Y, float W, float H, FLinearColor Color, float Radius)
	{
		auto* Image = Tree->ConstructWidget<UImage>();
		Image->SetBrush(FSlateRoundedBoxBrush(Color, Radius));
		Image->SetVisibility(ESlateVisibility::HitTestInvisible);
		Place(Canvas, Image, X,Y,W,H);
		return Image;
	}
	UCanvasPanel* Figure(UWidgetTree* Tree, FName Name, FLinearColor Body, bool bLeaf)
	{
		auto* Canvas = Tree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), Name);
		Canvas->SetVisibility(ESlateVisibility::HitTestInvisible);
		Shape(Tree,Canvas,10,133,160,22,FLinearColor(0.008f,0.018f,0.017f,0.55f),11);
		Shape(Tree,Canvas,22,115,44,26,Body*0.65f,13);
		Shape(Tree,Canvas,114,115,44,26,Body*0.65f,13);
		Shape(Tree,Canvas,22,36,138,100,Body,46);
		Shape(Tree,Canvas,39,78,105,48,Body*1.4f,24);
		Shape(Tree,Canvas,53,60,16,22,FLinearColor(0.018f,0.034f,0.04f),8);
		Shape(Tree,Canvas,114,60,16,22,FLinearColor(0.018f,0.034f,0.04f),8);
		Shape(Tree,Canvas,57,63,5,6,Ink,3);
		Shape(Tree,Canvas,118,63,5,6,Ink,3);
		if (bLeaf)
		{
			auto* Leaf = Shape(Tree,Canvas,60,4,28,50,FLinearColor(0.24f,0.40f,0.13f),14);
			Leaf->SetRenderTransformAngle(-28);
			Leaf = Shape(Tree,Canvas,92,0,24,50,FLinearColor(0.39f,0.52f,0.19f),12);
			Leaf->SetRenderTransformAngle(30);
		}
		else
		{
			Shape(Tree,Canvas,9,48,33,42,Body*0.8f,16)->SetRenderTransformAngle(-25);
			Shape(Tree,Canvas,142,48,33,42,Body*0.8f,16)->SetRenderTransformAngle(25);
		}
		return Canvas;
	}
}

TSharedRef<SWidget> UPokeMonsterBattleWidget::RebuildWidget()
{
	if (!WidgetTree) Initialize();
	if (WidgetTree && !WidgetTree->RootWidget) BuildDefaultTree();
	return Super::RebuildWidget();
}

void UPokeMonsterBattleWidget::BuildDefaultTree()
{
	auto* Back = WidgetTree->ConstructWidget<UBorder>();
	Back->SetBrushColor(FLinearColor(0.012f,0.022f,0.026f)); Back->SetPadding(FMargin(0));
	WidgetTree->RootWidget = Back;
	auto* Scale = WidgetTree->ConstructWidget<UScaleBox>(); Scale->SetStretch(EStretch::ScaleToFit); Back->SetContent(Scale);
	auto* Size = WidgetTree->ConstructWidget<USizeBox>(); Size->SetWidthOverride(1280); Size->SetHeightOverride(800); Scale->SetContent(Size);
	auto* Canvas = WidgetTree->ConstructWidget<UCanvasPanel>(); Size->SetContent(Canvas);
	Shape(WidgetTree,Canvas,0,0,1280,800,FLinearColor(0.016f,0.030f,0.034f),0);
	Place(Canvas,Text(WidgetTree,TEXT("Title"),TEXT("POKEMONSTER  /  KAMPFTEST"),17,Muted),40,25,650,26);
	Place(Canvas,Text(WidgetTree,TEXT("StatusLabel"),TEXT("Battle wird vorbereitet …"),24),40,61,990,34);
	RestartButton = WidgetTree->ConstructWidget<UButton>(UButton::StaticClass(), TEXT("RestartButton"));
	RestartButton->AddChild(Text(WidgetTree,NAME_None,TEXT("Neu starten"),16)); Place(Canvas,RestartButton,1090,31,150,38);
	Shape(WidgetTree,Canvas,40,118,1200,379,FLinearColor(0.043f,0.087f,0.078f),24);
	// Flat layered scenery and contact areas; no new world camera or external textures.
	Shape(WidgetTree,Canvas,57,255,1166,225,FLinearColor(0.066f,0.117f,0.084f),90);
	Shape(WidgetTree,Canvas,92,334,476,114,FLinearColor(0.12f,0.17f,0.12f),55);
	Shape(WidgetTree,Canvas,768,255,330,71,FLinearColor(0.12f,0.17f,0.12f),35);
	for (int32 I=0; I<12; ++I)
	{
		const float X=63+I*100;
		Shape(WidgetTree,Canvas,X,128+(I%3)*12,50+(I%2)*25,90,FLinearColor(0.055f,0.105f,0.084f),36);
	}
	Place(Canvas,Figure(WidgetTree,TEXT("PlayerFigure"),FLinearColor(0.16f,0.46f,0.49f),false),248,284,180,160);
	Place(Canvas,Figure(WidgetTree,TEXT("OpponentFigure"),FLinearColor(0.39f,0.49f,0.20f),true),853,185,155,140);
	Place(Canvas,Text(WidgetTree,TEXT("PlayerKO"),TEXT("K.O."),30),295,338,120,48);
	Place(Canvas,Text(WidgetTree,TEXT("OpponentKO"),TEXT("K.O."),30),900,235,120,48);
	const auto Card = [&](bool bPlayer, float X, float Y)
	{
		Shape(WidgetTree,Canvas,X,Y,330,104,FLinearColor(0.023f,0.046f,0.047f,0.97f),12);
		Place(Canvas,Text(WidgetTree,bPlayer?TEXT("PlayerName"):TEXT("OpponentName"),TEXT("—"),20),X+18,Y+12,300,30);
		Place(Canvas,Text(WidgetTree,bPlayer?TEXT("PlayerHP"):TEXT("OpponentHP"),TEXT("HP —"),16,Muted),X+18,Y+43,300,26);
		auto* Bar=WidgetTree->ConstructWidget<UProgressBar>(UProgressBar::StaticClass(),bPlayer?TEXT("PlayerBar"):TEXT("OpponentBar"));
		Bar->SetFillColorAndOpacity(FLinearColor(0.35f,0.67f,0.43f));
		Place(Canvas,Bar,X+18,Y+76,294,12);
	};
	Card(true,71,158); Card(false,867,353);
	Place(Canvas,Text(WidgetTree,NAME_None,TEXT("DEINE ATTACKEN"),15,Muted),40,520,650,24);
	Place(Canvas,Text(WidgetTree,NAME_None,TEXT("KAMPFVERLAUF"),15,Muted),794,520,420,24);
	for (int32 Index=0; Index<4; ++Index)
	{
		auto* Button=WidgetTree->ConstructWidget<UButton>(UButton::StaticClass(),FName(*FString::Printf(TEXT("MoveButton%d"),Index)));
		FButtonStyle Style;
		Style.SetNormal(FSlateRoundedBoxBrush(FLinearColor(0.055f,0.11f,0.12f),12.0f));
		Style.SetHovered(FSlateRoundedBoxBrush(FLinearColor(0.09f,0.20f,0.20f),12.0f));
		Style.SetPressed(FSlateRoundedBoxBrush(FLinearColor(0.12f,0.27f,0.24f),12.0f));
		Style.SetDisabled(FSlateRoundedBoxBrush(FLinearColor(0.028f,0.044f,0.045f),12.0f));
		Button->SetStyle(Style);
		auto* Label=Text(WidgetTree,FName(*FString::Printf(TEXT("MoveLabel%d"),Index)),TEXT("—"),18);
		Label->SetJustification(ETextJustify::Center);
		Button->AddChild(Label);
		Place(Canvas,Button,40+(Index%2)*366,553+(Index/2)*101,350,89);
	}
	Shape(WidgetTree,Canvas,790,553,450,190,FLinearColor(0.021f,0.042f,0.045f),12);
	auto* Scroll=WidgetTree->ConstructWidget<UScrollBox>(UScrollBox::StaticClass(),TEXT("LogScroll"));
	auto* Log=Text(WidgetTree,TEXT("LogLabel"),TEXT(""),17);
	Log->SetAutoWrapText(true); Scroll->AddChild(Log); Place(Canvas,Scroll,806,563,420,169);
	Place(Canvas,Text(WidgetTree,NAME_None,TEXT("1 GEGEN 1   ·   TESTDATEN   ·   STATUSATTACKEN NOCH OHNE EFFEKT"),13,Muted),40,768,1120,24);
}

void UPokeMonsterBattleWidget::BindControls()
{
	PlayerName=Cast<UTextBlock>(GetWidgetFromName(TEXT("PlayerName"))); OpponentName=Cast<UTextBlock>(GetWidgetFromName(TEXT("OpponentName")));
	PlayerHP=Cast<UTextBlock>(GetWidgetFromName(TEXT("PlayerHP"))); OpponentHP=Cast<UTextBlock>(GetWidgetFromName(TEXT("OpponentHP")));
	PlayerBar=Cast<UProgressBar>(GetWidgetFromName(TEXT("PlayerBar"))); OpponentBar=Cast<UProgressBar>(GetWidgetFromName(TEXT("OpponentBar")));
	StatusLabel=Cast<UTextBlock>(GetWidgetFromName(TEXT("StatusLabel"))); LogLabel=Cast<UTextBlock>(GetWidgetFromName(TEXT("LogLabel")));
	LogScroll=Cast<UScrollBox>(GetWidgetFromName(TEXT("LogScroll")));
	PlayerKO=Cast<UTextBlock>(GetWidgetFromName(TEXT("PlayerKO"))); OpponentKO=Cast<UTextBlock>(GetWidgetFromName(TEXT("OpponentKO")));
	PlayerFigure=GetWidgetFromName(TEXT("PlayerFigure")); OpponentFigure=GetWidgetFromName(TEXT("OpponentFigure"));
	RestartButton=Cast<UButton>(GetWidgetFromName(TEXT("RestartButton")));
	Buttons.Reset(); MoveLabels.Reset();
	for(int32 I=0;I<4;++I)
	{
		Buttons.Add(Cast<UButton>(GetWidgetFromName(FName(*FString::Printf(TEXT("MoveButton%d"),I)))));
		MoveLabels.Add(Cast<UTextBlock>(GetWidgetFromName(FName(*FString::Printf(TEXT("MoveLabel%d"),I)))));
	}
	if(Buttons[0]) Buttons[0]->OnClicked.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::Move0);
	if(Buttons[1]) Buttons[1]->OnClicked.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::Move1);
	if(Buttons[2]) Buttons[2]->OnClicked.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::Move2);
	if(Buttons[3]) Buttons[3]->OnClicked.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::Move3);
	if(RestartButton) RestartButton->OnClicked.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::Restart);
}

void UPokeMonsterBattleWidget::NativeConstruct()
{
	Super::NativeConstruct(); BindControls();
	if(Presenter)
	{
		Presenter->OnChanged.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::Refresh);
		Presenter->OnRoundResolved.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::RoundResolved);
	}
	Refresh();
}

void UPokeMonsterBattleWidget::NativeDestruct()
{
	if(Presenter)
	{
		Presenter->OnChanged.RemoveDynamic(this,&UPokeMonsterBattleWidget::Refresh);
		Presenter->OnRoundResolved.RemoveDynamic(this,&UPokeMonsterBattleWidget::RoundResolved);
	}
	Super::NativeDestruct();
}

void UPokeMonsterBattleWidget::SetPresenter(UPokeMonsterBattlePresenter* InPresenter)
{
	if(Presenter)
	{
		Presenter->OnChanged.RemoveDynamic(this,&UPokeMonsterBattleWidget::Refresh);
		Presenter->OnRoundResolved.RemoveDynamic(this,&UPokeMonsterBattleWidget::RoundResolved);
	}
	Presenter=InPresenter;
	if(Presenter)
	{
		Presenter->OnChanged.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::Refresh);
		Presenter->OnRoundResolved.AddUniqueDynamic(this,&UPokeMonsterBattleWidget::RoundResolved);
	}
	Refresh();
}

void UPokeMonsterBattleWidget::Refresh()
{
	if(!Presenter || !PlayerName) return;
	const auto& View=Presenter->GetView();
	const auto SetCreature=[](const FPokeMonsterBattleCreatureView& Data,UTextBlock* Name,UTextBlock* HP,UProgressBar* Bar,UTextBlock* KO,UWidget* Figure)
	{
		if(Name) Name->SetText(FText::FromString(FString::Printf(TEXT("%s   ·   Lv. %d"),*Data.Name.ToString(),Data.Level)));
		if(HP) HP->SetText(FText::FromString(FString::Printf(TEXT("HP  %d / %d"),Data.CurrentHP,Data.MaxHP)));
		if(Bar) Bar->SetPercent(Data.MaxHP>0 ? FMath::Clamp(float(Data.CurrentHP)/Data.MaxHP,0.0f,1.0f):0);
		if(KO) KO->SetVisibility(Data.bKO?ESlateVisibility::HitTestInvisible:ESlateVisibility::Collapsed);
		if(Figure) Figure->SetRenderOpacity(Data.bKO?0.3f:1.0f);
	};
	SetCreature(View.Player,PlayerName,PlayerHP,PlayerBar,PlayerKO,PlayerFigure);
	SetCreature(View.Opponent,OpponentName,OpponentHP,OpponentBar,OpponentKO,OpponentFigure);
	if(StatusLabel) StatusLabel->SetText(View.Status);
	if(LogLabel) LogLabel->SetText(View.Log);
	if(LogScroll) LogScroll->ScrollToEnd();
	if(RestartButton) RestartButton->SetIsEnabled(!View.bBusy);
	for(int32 I=0;I<4 && View.Moves.IsValidIndex(I);++I)
	{
		const auto& Move=View.Moves[I];
		if(Buttons.IsValidIndex(I) && Buttons[I]) Buttons[I]->SetIsEnabled(Move.bEnabled);
		if(MoveLabels.IsValidIndex(I) && MoveLabels[I]) MoveLabels[I]->SetText(FText::FromString(FString::Printf(TEXT("%s\n%s   ·   PP %d / %d"),*Move.Name.ToString(),*Move.Type.ToString(),Move.CurrentPP,Move.MaxPP)));
	}
	OnBattleViewUpdated(View);
}

UButton* UPokeMonsterBattleWidget::GetAttackButton(int32 Slot) const { return Buttons.IsValidIndex(Slot)?Buttons[Slot].Get():nullptr; }
void UPokeMonsterBattleWidget::RoundResolved(const FPokeMonsterBattleResult& Result) { OnBattleRoundResolved(Result); }
void UPokeMonsterBattleWidget::Choose(int32 Slot) { if(auto* PC=Cast<APokeMonsterBattleTestController>(GetOwningPlayer())) PC->ChooseMove(Slot); }
void UPokeMonsterBattleWidget::Move0(){Choose(0);} void UPokeMonsterBattleWidget::Move1(){Choose(1);}
void UPokeMonsterBattleWidget::Move2(){Choose(2);} void UPokeMonsterBattleWidget::Move3(){Choose(3);}
void UPokeMonsterBattleWidget::Restart(){if(auto* PC=Cast<APokeMonsterBattleTestController>(GetOwningPlayer())) PC->RestartBattle();}
