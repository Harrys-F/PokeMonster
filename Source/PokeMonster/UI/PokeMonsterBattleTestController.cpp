#include "PokeMonsterBattleTestController.h"
#include "PokeMonsterBattlePresenter.h"
#include "PokeMonsterBattleWidget.h"
#include "TimerManager.h"

APokeMonsterBattleTestGameMode::APokeMonsterBattleTestGameMode()
{
	PlayerControllerClass = APokeMonsterBattleTestController::StaticClass();
	DefaultPawnClass = nullptr;
}

void APokeMonsterBattleTestController::BeginPlay()
{
	Super::BeginPlay();
	if (!IsLocalController()) return;
	Presenter = NewObject<UPokeMonsterBattlePresenter>(this);
	Presenter->StartDemo();
	BattleWidget = CreateWidget<UPokeMonsterBattleWidget>(this, WidgetClass ? WidgetClass.Get() : UPokeMonsterBattleWidget::StaticClass());
	if (BattleWidget)
	{
		BattleWidget->SetPresenter(Presenter);
		BattleWidget->SetIsFocusable(true);
		BattleWidget->AddToViewport();
		FInputModeUIOnly Input;
		Input.SetWidgetToFocus(BattleWidget->TakeWidget());
		SetInputMode(Input);
		bShowMouseCursor = true;
	}
}

bool APokeMonsterBattleTestController::ChooseMove(const int32 Slot)
{
	if (!Presenter || !Presenter->TrySelectMove(Slot)) return false;
	GetWorldTimerManager().SetTimer(RoundTimer, this, &APokeMonsterBattleTestController::ResolvePending, 0.35f, false);
	return true;
}

void APokeMonsterBattleTestController::ResolvePending()
{
	if (!Presenter) return;
	Presenter->ResolveSelection();
	Presenter->FinishPresentation();
}

void APokeMonsterBattleTestController::RestartBattle()
{
	if (Presenter && !Presenter->GetView().bBusy) Presenter->StartDemo();
}

void APokeMonsterBattleTestController::EndPlay(const EEndPlayReason::Type Reason)
{
	GetWorldTimerManager().ClearTimer(RoundTimer);
	if (BattleWidget) BattleWidget->RemoveFromParent();
	Super::EndPlay(Reason);
}
