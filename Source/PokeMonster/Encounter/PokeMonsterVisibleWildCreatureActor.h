#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterEncounterProfile.h"
#include "PokeMonsterEncounterSubsystem.h"
#include "PokeMonsterVisibleWildCreatureActor.generated.h"

class UPokeMonsterCreatureRoamingComponent;
class UCapsuleComponent;
class USphereComponent;
class UPaperSpriteComponent;
class UTextRenderComponent;
class APokeMonsterPlayerCharacter;
class APokeMonsterCreatureVisualActor;
class UPokeMonsterCreatureSpeciesData;

/** A deliberately placed wild creature. Contact or interaction uses the shared encounter flow. */
UCLASS()
class POKEMONSTER_API APokeMonsterVisibleWildCreatureActor : public AActor, public IPokeMonsterInteractable
{
	GENERATED_BODY()
public:
	APokeMonsterVisibleWildCreatureActor();
	virtual void Tick(float DeltaSeconds) override;
	void SuppressPresentation(bool Suppressed);
	virtual bool CanInteract_Implementation(APawn* Interactor) const override;
	virtual void Interact_Implementation(APawn* Interactor) override;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") TSoftObjectPtr<UPokeMonsterEncounterProfile> Profile;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") FPokeMonsterEncounterContext Context;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") int32 Seed = 3817;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") FName EncounterId = TEXT("Dev_VisibleWild");
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") bool bDeactivateAfterVictory = true;
	/** Optional, opt-in 3D presentation for a deliberately placed species. */
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Presentation") TSoftObjectPtr<UPokeMonsterCreatureSpeciesData> VisualSpecies;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Presentation") bool bAmbientMotion=false;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Wild Movement") TObjectPtr<UPokeMonsterCreatureRoamingComponent> OverworldMovement;
protected:
	virtual void EndPlay(const EEndPlayReason::Type Reason) override;
	virtual void BeginPlay() override;
private:
	bool TryStart(APokeMonsterPlayerCharacter* Player);
	void UpdateVisualGround();
	UFUNCTION() void OnContact(UPrimitiveComponent* Overlapped, AActor* OtherActor,
		UPrimitiveComponent* OtherComponent, int32 BodyIndex, bool bFromSweep, const FHitResult& Hit);
	UFUNCTION() void OnEncounterFinished(const FPokeMonsterEncounterEndData& Result);
	UFUNCTION() void RefreshPersistentState();
	UPROPERTY(VisibleAnywhere) TObjectPtr<UCapsuleComponent> Body;
	UPROPERTY(VisibleAnywhere) TObjectPtr<USphereComponent> ContactRange;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UPaperSpriteComponent> Sprite;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> Label;
	UPROPERTY(Transient) TObjectPtr<APokeMonsterCreatureVisualActor> Visual;
	bool bDeactivated = false;
 bool bWasWarning=false;
};
