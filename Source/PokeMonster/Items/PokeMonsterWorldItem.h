#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterWorldItem.generated.h"
class UPokeMonsterItemData;
class UStaticMeshComponent;
/** Event-driven pickup, using the existing interaction, inventory, world flags and save transaction. */
UCLASS()
class POKEMONSTER_API APokeMonsterWorldItem : public AActor, public IPokeMonsterInteractable
{
 GENERATED_BODY()
public:
 APokeMonsterWorldItem();
 UPROPERTY(EditAnywhere,BlueprintReadOnly,Category="Pickup") FName PickupId;
 UPROPERTY(EditAnywhere,BlueprintReadOnly,Category="Pickup") TSoftObjectPtr<UPokeMonsterItemData> Item;
 UPROPERTY(EditAnywhere,BlueprintReadOnly,Category="Pickup",meta=(ClampMin="1")) int32 Quantity=1;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Pickup") TObjectPtr<UStaticMeshComponent> Mesh;
 virtual bool CanInteract_Implementation(APawn* Interactor) const override;
 virtual void Interact_Implementation(APawn* Interactor) override;
 virtual void BeginPlay() override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 UFUNCTION() void RefreshCollectedState();
private:
 bool bBusy=false;
};
