#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/GameModeBase.h"
#include "PokeMonsterBattleTestController.generated.h"

class UPokeMonsterBattlePresenter;
class UPokeMonsterBattleWidget;

UCLASS()
class POKEMONSTER_API APokeMonsterBattleTestController : public APlayerController
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category="Battle Test") bool ChooseMove(int32 Slot);
	UFUNCTION(BlueprintCallable, Category="Battle Test") void RestartBattle();
	UFUNCTION(BlueprintPure, Category="Battle Test") UPokeMonsterBattlePresenter* GetPresenter() const { return Presenter; }
	UFUNCTION(BlueprintPure, Category="Battle Test") UPokeMonsterBattleWidget* GetBattleWidget() const { return BattleWidget; }
protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type Reason) override;
	UPROPERTY(EditDefaultsOnly, Category="Battle Test") TSubclassOf<UPokeMonsterBattleWidget> WidgetClass;
private:
	void ResolvePending();
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterBattlePresenter> Presenter;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterBattleWidget> BattleWidget;
	FTimerHandle RoundTimer;
};

/** Selected only by Dev_BattleTestMap's World Settings; never replaces the overworld GameMode. */
UCLASS()
class POKEMONSTER_API APokeMonsterBattleTestGameMode : public AGameModeBase
{
	GENERATED_BODY()
public:
	APokeMonsterBattleTestGameMode();
};
