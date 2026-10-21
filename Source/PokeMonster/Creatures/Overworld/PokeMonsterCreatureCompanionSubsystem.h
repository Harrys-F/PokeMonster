#pragma once
#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "PokeMonsterCreatureCompanionSubsystem.generated.h"
struct FPokeMonsterCreatureInstance;
class APokeMonsterCreatureVisualActor;
class UPokeMonsterCreatureRoamingComponent;
class UPokeMonsterCreatureSpeciesData;
class UPokeMonsterEncounterSubsystem;

/** One visual of party slot zero; never silently substitutes another member. Owns no creature/gameplay data. */
UCLASS()
class POKEMONSTER_API UPokeMonsterCreatureCompanionSubsystem : public UTickableWorldSubsystem
{
	GENERATED_BODY()
public:
	static int32 SelectPartyIndex(const TArray<FPokeMonsterCreatureInstance>& Team);
	virtual void Tick(float DeltaTime) override;
	virtual TStatId GetStatId() const override;
	virtual void Deinitialize() override;
	UFUNCTION(BlueprintCallable, Category="Creature|Companion") void SetEnabled(bool Enabled);
	UFUNCTION(BlueprintPure, Category="Creature|Companion") APokeMonsterCreatureVisualActor* GetVisual() const { return Visual; }
	UFUNCTION(BlueprintPure, Category="Creature|Companion") UPokeMonsterCreatureRoamingComponent* GetMovement() const { return Movement; }
protected:
	virtual bool DoesSupportWorldType(EWorldType::Type WorldType) const override;
private:
	UFUNCTION() void HideForEncounter();
	bool PlaceNearPlayer(AActor* Player);
	void ClearVisual();
	UPROPERTY(Transient) TObjectPtr<APokeMonsterCreatureVisualActor> Visual;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterCreatureRoamingComponent> Movement;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterCreatureSpeciesData> CurrentSpecies;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterEncounterSubsystem> BoundEncounter;
	FGuid CurrentId;
	FVector PreviousPlayerLocation = FVector::ZeroVector;
	float RefreshRemaining = 0.f;
	bool bEnabled = true, bPlaced = false, bHavePlayerLocation = false;
};
