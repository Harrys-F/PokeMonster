#pragma once
#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "PokeMonsterEvolutionWidget.generated.h"
class UImage;class UTextBlock;class UButton;class UMaterialInstanceDynamic;
class APokeMonsterClassicBattleScene;class APokeMonsterOverworldPlayerController;
/** Same-world, capture-only presentation. Party mutation remains in the existing encounter subsystem. */
UCLASS()
class POKEMONSTER_API UPokeMonsterEvolutionWidget : public UUserWidget
{
 GENERATED_BODY()
public:
 bool BeginEvolution(APokeMonsterOverworldPlayerController* Owner,int32 TeamIndex,bool bLearningOnly=false);
 UFUNCTION(BlueprintCallable) void Confirm();
 UFUNCTION(BlueprintCallable) void Cancel();
 UFUNCTION(BlueprintPure) FString GetPhase() const{return Phase;}
 UPROPERTY(Transient,BlueprintReadOnly) TObjectPtr<APokeMonsterClassicBattleScene> Stage;
 UPROPERTY(Transient,BlueprintReadOnly) FGuid CreatureId;
protected:
 virtual TSharedRef<SWidget> RebuildWidget() override;
 virtual void NativeTick(const FGeometry&,float Delta) override;
 virtual FReply NativeOnPreviewKeyDown(const FGeometry&,const FKeyEvent&) override;
 virtual void NativeDestruct() override;
private:
 void RefreshText();void Finish();void StartLearning();
 UPROPERTY(Transient) TObjectPtr<APokeMonsterOverworldPlayerController> OwnerController;
 UPROPERTY(Transient) TObjectPtr<UImage> View;
 UPROPERTY(Transient) TObjectPtr<UImage> Flash;
 UPROPERTY(Transient) TObjectPtr<UTextBlock> Title;
 UPROPERTY(Transient) TObjectPtr<UTextBlock> Details;
 UPROPERTY(Transient) TObjectPtr<UTextBlock> Hints;
 UPROPERTY(Transient) TArray<TObjectPtr<UImage>> Motes;
 UPROPERTY(Transient) TObjectPtr<UMaterialInstanceDynamic> Glow;
 FPrimaryAssetId Target;FString Phase=TEXT("offer");float Elapsed=0;int32 Selection=0;bool bPreviewChanged=false;
};
