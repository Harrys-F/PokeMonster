#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterEncounterProfile.h"
#include "PokeMonsterWildEncounterZone.generated.h"

class UBoxComponent;
class UStaticMeshComponent;
class UTextRenderComponent;

/** One controlled zone activation per play session; not a random-step system. */
UCLASS()
class POKEMONSTER_API APokeMonsterWildEncounterZone : public AActor
{
	GENERATED_BODY()
public:
	APokeMonsterWildEncounterZone();
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") TSoftObjectPtr<UPokeMonsterEncounterProfile> Profile;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") FPokeMonsterEncounterContext Context;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") int32 Seed = 5719;
	bool HasTriggered() const { return bTriggered; }
private:
	UFUNCTION() void OnEntered(UPrimitiveComponent* Overlapped, AActor* OtherActor,
		UPrimitiveComponent* OtherComponent, int32 BodyIndex, bool bFromSweep, const FHitResult& Hit);
	UPROPERTY(VisibleAnywhere) TObjectPtr<UBoxComponent> Trigger;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> GroundMarker;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> Label;
	bool bTriggered = false;
};
