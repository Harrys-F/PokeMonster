#include "PokeMonsterBattleWidget.h"
#include "PokeMonsterBattleTestController.h"
#include "Blueprint/WidgetTree.h"
#include "Components/Border.h"
#include "Components/Button.h"
#include "Components/ButtonSlot.h"
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
	const FLinearColor Ink(0.93f, 0.91f, 0.79f);
	const FLinearColor Muted(0.65f, 0.72f, 0.60f);
	const FLinearColor DarkInk(0.10f, 0.16f, 0.15f);
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
	UImage* Shape(UWidgetTree* Tree, UCanvasPanel* Canvas, float X, float Y, float W, float H,
		FLinearColor Color, float Radius, FName Name = NAME_None)
	{
		auto* Image = Tree->ConstructWidget<UImage>(UImage::StaticClass(), Name);
		Image->SetBrush(FSlateRoundedBoxBrush(Color, Radius));
		Image->SetVisibility(ESlateVisibility::HitTestInvisible);
		Place(Canvas, Image, X,Y,W,H);
		return Image;
	}
	UImage* Artwork(UWidgetTree* Tree, UCanvasPanel* Canvas, FName Name, const TCHAR* AssetPath,
		float X, float Y, float W, float H)
	{
		auto* Image = Tree->ConstructWidget<UImage>(UImage::StaticClass(), Name);
		if (auto* Texture = LoadObject<UTexture2D>(nullptr, AssetPath)) Image->SetBrushFromTexture(Texture, true);
		Image->SetVisibility(ESlateVisibility::HitTestInvisible);
		Place(Canvas, Image, X, Y, W, H);
		return Image;
	}
	FLinearColor TypeTint(const FString& Type)
	{
		if (Type == TEXT("Feuer")) return FLinearColor(0.49f, 0.23f, 0.16f);
		if (Type == TEXT("Wasser")) return FLinearColor(0.18f, 0.36f, 0.43f);
		if (Type == TEXT("Pflanze")) return FLinearColor(0.25f, 0.40f, 0.25f);
		if (Type == TEXT("Elektro")) return FLinearColor(0.52f, 0.41f, 0.16f);
		if (Type == TEXT("Eis")) return FLinearColor(0.26f, 0.43f, 0.47f);
		return FLinearColor(0.33f, 0.36f, 0.30f);
	}
	void TintButton(UButton* Button, const FLinearColor& Tint)
	{
		FButtonStyle Style;
		Style.SetNormal(FSlateRoundedBoxBrush(FLinearColor(0.15f, 0.22f, 0.20f, 0.96f), 18.0f));
		Style.SetHovered(FSlateRoundedBoxBrush(FLinearColor(0.20f, 0.30f, 0.26f, 0.98f) + Tint * 0.12f, 18.0f));
		Style.SetPressed(FSlateRoundedBoxBrush(FLinearColor(0.23f, 0.34f, 0.29f, 0.98f) + Tint * 0.15f, 18.0f));
		Style.SetDisabled(FSlateRoundedBoxBrush(FLinearColor(0.10f, 0.14f, 0.13f, 0.86f), 18.0f));
		Button->SetStyle(Style);
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
	Back->SetBrushColor(FLinearColor(0.06f,0.10f,0.08f)); Back->SetPadding(FMargin(0));
	WidgetTree->RootWidget = Back;
	auto* Scale = WidgetTree->ConstructWidget<UScaleBox>(); Scale->SetStretch(EStretch::ScaleToFit); Back->SetContent(Scale);
	auto* Size = WidgetTree->ConstructWidget<USizeBox>(); Size->SetWidthOverride(1280); Size->SetHeightOverride(800); Scale->SetContent(Size);
	auto* Canvas = WidgetTree->ConstructWidget<UCanvasPanel>(); Size->SetContent(Canvas);
	Shape(WidgetTree,Canvas,0,0,1280,800,FLinearColor(0.07f,0.12f,0.09f),0);
	Artwork(WidgetTree,Canvas,TEXT("BattleGlen"),TEXT("/Game/Battle/Textures/T_BattleGlen.T_BattleGlen"),0,0,1280,720);
	// Soft overlays preserve text contrast while the painted clearing remains visible.
	Shape(WidgetTree,Canvas,0,0,1280,111,FLinearColor(0.025f,0.055f,0.045f,0.70f),0);
	Shape(WidgetTree,Canvas,0,515,1280,285,FLinearColor(0.045f,0.073f,0.063f,0.98f),0);
	Shape(WidgetTree,Canvas,0,514,1280,3,FLinearColor(0.45f,0.45f,0.30f,0.55f),0);
	Shape(WidgetTree,Canvas,19,23,224,35,FLinearColor(0.08f,0.16f,0.13f,0.86f),17);
	Place(Canvas,Text(WidgetTree,TEXT("Title"),TEXT("POKEMONSTER  ·  DUELL"),16,Ink),38,28,260,28);
	auto* Status = Text(WidgetTree,TEXT("StatusLabel"),TEXT("Battle wird vorbereitet …"),23,Ink);
	Status->SetJustification(ETextJustify::Center);
	Place(Canvas,Status,319,38,642,38);
	RestartButton = WidgetTree->ConstructWidget<UButton>(UButton::StaticClass(), TEXT("RestartButton"));
	TintButton(RestartButton,FLinearColor(0.35f,0.39f,0.30f));
	RestartButton->AddChild(Text(WidgetTree,NAME_None,TEXT("Neu beginnen"),15,Ink));
	Place(Canvas,RestartButton,1087,27,165,43);

	Shape(WidgetTree,Canvas,185,448,387,44,FLinearColor(0.02f,0.04f,0.03f,0.27f),22);
	Shape(WidgetTree,Canvas,865,368,224,27,FLinearColor(0.02f,0.04f,0.03f,0.25f),14);
	Artwork(WidgetTree,Canvas,TEXT("OpponentFigure"),TEXT("/Game/Battle/Textures/T_TestGrass.T_TestGrass"),830,133,274,253);
	Artwork(WidgetTree,Canvas,TEXT("PlayerFigure"),TEXT("/Game/Battle/Textures/T_TestWater.T_TestWater"),137,148,450,350);
	Place(Canvas,Text(WidgetTree,TEXT("PlayerKO"),TEXT("K.O."),32,Ink),302,315,120,48);
	Place(Canvas,Text(WidgetTree,TEXT("OpponentKO"),TEXT("K.O."),29,Ink),916,264,120,48);
	const auto Card = [&](bool bPlayer, float X, float Y, float Width)
	{
		Shape(WidgetTree,Canvas,X+3,Y+6,Width,96,FLinearColor(0.02f,0.04f,0.03f,0.36f),24);
		Shape(WidgetTree,Canvas,X,Y,Width,96,FLinearColor(0.83f,0.80f,0.67f,0.94f),23);
		Shape(WidgetTree,Canvas,X+7,Y+7,5,82,bPlayer?FLinearColor(0.15f,0.43f,0.47f):FLinearColor(0.34f,0.44f,0.20f),3);
		Place(Canvas,Text(WidgetTree,bPlayer?TEXT("PlayerName"):TEXT("OpponentName"),TEXT("—"),20,DarkInk),X+23,Y+10,Width-42,30);
		Place(Canvas,Text(WidgetTree,bPlayer?TEXT("PlayerHP"):TEXT("OpponentHP"),TEXT("HP —"),17,DarkInk),X+23,Y+42,Width-42,26);
		Shape(WidgetTree,Canvas,X+22,Y+74,Width-45,10,FLinearColor(0.27f,0.32f,0.27f,0.50f),5);
		auto* Bar=WidgetTree->ConstructWidget<UProgressBar>(UProgressBar::StaticClass(),bPlayer?TEXT("PlayerBar"):TEXT("OpponentBar"));
		Bar->SetFillColorAndOpacity(FLinearColor(0.19f,0.48f,0.28f));
		Place(Canvas,Bar,X+23,Y+74,Width-47,10);
	};
	Card(true,58,410,400); Card(false,869,96,370);
	Place(Canvas,Text(WidgetTree,NAME_None,TEXT("DEINE ATTACKEN"),15,Muted),37,539,650,24);
	Place(Canvas,Text(WidgetTree,NAME_None,TEXT("KAMPFVERLAUF"),15,Muted),806,539,420,24);
	for (int32 Index=0; Index<4; ++Index)
	{
		auto* Button=WidgetTree->ConstructWidget<UButton>(UButton::StaticClass(),FName(*FString::Printf(TEXT("MoveButton%d"),Index)));
		TintButton(Button,FLinearColor(0.33f,0.36f,0.30f));
		auto* Inner=WidgetTree->ConstructWidget<UCanvasPanel>();
		Inner->SetVisibility(ESlateVisibility::SelfHitTestInvisible);
		if(auto* ButtonSlot=Cast<UButtonSlot>(Button->AddChild(Inner)))
		{
			ButtonSlot->SetHorizontalAlignment(HAlign_Fill);
			ButtonSlot->SetVerticalAlignment(VAlign_Fill);
		}
		Shape(WidgetTree,Inner,13,41,92,25,FLinearColor(0.33f,0.36f,0.30f),12,
			FName(*FString::Printf(TEXT("MoveTypeAccent%d"),Index)));
		Place(Inner,Text(WidgetTree,FName(*FString::Printf(TEXT("MoveLabel%d"),Index)),TEXT("—"),19,Ink),20,8,310,30);
		Place(Inner,Text(WidgetTree,FName(*FString::Printf(TEXT("MoveType%d"),Index)),TEXT("—"),14,Ink),23,44,83,22);
		auto* PP=Text(WidgetTree,FName(*FString::Printf(TEXT("MovePP%d"),Index)),TEXT("PP —"),15,Muted);
		PP->SetJustification(ETextJustify::Right);
		Place(Inner,PP,217,44,113,22);
		Place(Canvas,Button,37+(Index%2)*367,570+(Index/2)*91,350,78);
	}
	Shape(WidgetTree,Canvas,793,571,449,170,FLinearColor(0.10f,0.16f,0.14f,0.96f),23);
	Shape(WidgetTree,Canvas,807,583,3,145,FLinearColor(0.48f,0.48f,0.33f,0.65f),2);
	auto* Scroll=WidgetTree->ConstructWidget<UScrollBox>(UScrollBox::StaticClass(),TEXT("LogScroll"));
	auto* Log=Text(WidgetTree,TEXT("LogLabel"),TEXT(""),15,Ink);
	Log->SetAutoWrapText(true); Scroll->AddChild(Log); Place(Canvas,Scroll,824,581,399,146);
	Place(Canvas,Text(WidgetTree,NAME_None,TEXT("1 GEGEN 1   ·   TESTDATEN   ·   STATUSATTACKEN NOCH OHNE EFFEKT"),12,Muted),38,764,1080,24);
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
	Buttons.Reset(); MoveLabels.Reset(); MoveTypeLabels.Reset(); MovePPLabels.Reset(); MoveTypeAccents.Reset();
	for(int32 I=0;I<4;++I)
	{
		Buttons.Add(Cast<UButton>(GetWidgetFromName(FName(*FString::Printf(TEXT("MoveButton%d"),I)))));
		MoveLabels.Add(Cast<UTextBlock>(GetWidgetFromName(FName(*FString::Printf(TEXT("MoveLabel%d"),I)))));
		MoveTypeLabels.Add(Cast<UTextBlock>(GetWidgetFromName(FName(*FString::Printf(TEXT("MoveType%d"),I)))));
		MovePPLabels.Add(Cast<UTextBlock>(GetWidgetFromName(FName(*FString::Printf(TEXT("MovePP%d"),I)))));
		MoveTypeAccents.Add(Cast<UImage>(GetWidgetFromName(FName(*FString::Printf(TEXT("MoveTypeAccent%d"),I)))));
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
		if(Bar)
		{
			const float Ratio=Data.MaxHP>0 ? FMath::Clamp(float(Data.CurrentHP)/Data.MaxHP,0.0f,1.0f):0;
			Bar->SetPercent(Ratio);
			Bar->SetFillColorAndOpacity(Ratio>0.5f ? FLinearColor(0.19f,0.48f,0.28f)
				: Ratio>0.25f ? FLinearColor(0.65f,0.48f,0.18f) : FLinearColor(0.65f,0.24f,0.18f));
		}
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
		if(MoveLabels.IsValidIndex(I) && MoveLabels[I]) MoveLabels[I]->SetText(Move.Name);
		if(MoveTypeLabels.IsValidIndex(I) && MoveTypeLabels[I]) MoveTypeLabels[I]->SetText(Move.Type);
		if(MovePPLabels.IsValidIndex(I) && MovePPLabels[I])
			MovePPLabels[I]->SetText(FText::FromString(FString::Printf(TEXT("PP %d / %d"),Move.CurrentPP,Move.MaxPP)));
		if(MoveTypeAccents.IsValidIndex(I) && MoveTypeAccents[I])
			MoveTypeAccents[I]->SetBrush(FSlateRoundedBoxBrush(TypeTint(Move.Type.ToString()),12.0f));
	}
	OnBattleViewUpdated(View);
}

UButton* UPokeMonsterBattleWidget::GetAttackButton(int32 Slot) const { return Buttons.IsValidIndex(Slot)?Buttons[Slot].Get():nullptr; }
void UPokeMonsterBattleWidget::RoundResolved(const FPokeMonsterBattleResult& Result) { OnBattleRoundResolved(Result); }
void UPokeMonsterBattleWidget::Choose(int32 Slot) { if(auto* PC=Cast<APokeMonsterBattleTestController>(GetOwningPlayer())) PC->ChooseMove(Slot); }
void UPokeMonsterBattleWidget::Move0(){Choose(0);} void UPokeMonsterBattleWidget::Move1(){Choose(1);}
void UPokeMonsterBattleWidget::Move2(){Choose(2);} void UPokeMonsterBattleWidget::Move3(){Choose(3);}
void UPokeMonsterBattleWidget::Restart(){if(auto* PC=Cast<APokeMonsterBattleTestController>(GetOwningPlayer())) PC->RestartBattle();}
