#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "../Interaction/PokeMonsterInteractable.h"
#include "PokeMonsterEncounterProfile.h"
#include "PokeMonsterEncounterSubsystem.h"
#include "PokeMonsterVisibleWildCreatureActor.generated.h"

UENUM(BlueprintType)
enum class EPokeMonsterWildLifeState : uint8 { Active, Recovering, Escaping, WaitingForExit, Removed };

class UPokeMonsterCreatureRoamingComponent;
class UCapsuleComponent;
struct FCollisionQueryParams;
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
 UFUNCTION(BlueprintPure,Category="Wild Encounter") bool IsOutsidePlayerView() const;
 UFUNCTION(BlueprintPure,Category="Wild Encounter") bool IsTouchingPlayer(const APokeMonsterPlayerCharacter* Player) const;
 UFUNCTION(BlueprintPure,Category="Wild Encounter") FString GetChallengeName() const;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Wild Encounter") EPokeMonsterWildLifeState LifeState=EPokeMonsterWildLifeState::Active;
 /** Explicit, stable-ID group. Each member remains an independent encounter; never a group battle. */
 UPROPERTY(EditInstanceOnly,BlueprintReadOnly,Category="Wild Group",meta=(ClampMin="1",ClampMax="4")) int32 GroupSize=1;
 UPROPERTY(EditInstanceOnly,BlueprintReadOnly,Category="Wild Group",meta=(ClampMin="120",ClampMax="400")) float GroupSpacing=180.f;
 /** Runtime-only suppression of old demonstration sources; identities/assets/save state remain intact. */
 UFUNCTION(BlueprintCallable) void SuspendForHabitatPopulation();
 UPROPERTY(Transient,BlueprintReadOnly) bool bHabitatDormant=false;
	void SuppressPresentation(bool Suppressed);
 void SetChallengeFocused(bool Focused);
 /** Configure before FinishSpawning; existing authored sources keep their body sizes. */
 void ConfigureHabitatBody(float Radius,float HalfHeight);
 /** Shared by the actor and player target selection; land interaction stays unchanged. */
 float GetShoreInteractionRadius() const;
 /** Shared UI source. Active instances only; no distance or geometry visibility filter. */
 UFUNCTION(BlueprintPure) APokeMonsterCreatureVisualActor* GetNameplateVisual() const;
 UFUNCTION(BlueprintPure) FString GetNameplateText() const;
 void PrepareInteractionSight(FCollisionQueryParams& Query) const;
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
	bool TryStart(APokeMonsterPlayerCharacter* Player,bool Contact=false);
 bool IsReady(const APokeMonsterPlayerCharacter* Player) const;
 void RemoveWildPresentation();
 void SpawnGroup();
 FTransform InitialSpawnTransform;
 float EncounterReadyAt=0.f,RecoveryRemaining=0.f,OffscreenSeconds=0.f;
 bool bAwaitSeparation=false;
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
 bool bChallengeFocused=false;

};
