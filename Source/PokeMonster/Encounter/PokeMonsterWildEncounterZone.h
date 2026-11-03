#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterEncounterProfile.h"
#include "PokeMonsterWildEncounterZone.generated.h"

class UBoxComponent;
class UStaticMeshComponent;
class UTextRenderComponent;

/** Shared tuning for opt-in walkable bush fields; no save or spawn state. */
UCLASS(Config=PokeMonsterBushEncounters, DefaultConfig)
class POKEMONSTER_API UPokeMonsterBushEncounterSettings : public UObject
{
 GENERATED_BODY()
public:
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") bool bEnabled=true;
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") float ChancePerStep=.18f;
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") float StepDistanceCm=250.f;
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") float CooldownSeconds=12.f;
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") float MinimumTravelBetweenEncountersCm=800.f;
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") float SampleSeconds=.2f;
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") float MaximumAcceptedDisplacementCm=500.f;
 UPROPERTY(Config, EditAnywhere, Category="Bush Encounters") TArray<FName> AllowedHabitats={TEXT("Meadow"),TEXT("Edge"),TEXT("Forest"),TEXT("Glade")};
 bool IsValidConfiguration() const;
};
/** Distance sampler: pauses/load/teleports reset the anchor, never produce a check burst. */
struct POKEMONSTER_API FPokeMonsterBushTravel
{
 FVector Previous=FVector::ZeroVector;
 float Remainder=0;
 bool bAnchored=false;
 void Reset(){bAnchored=false;Remainder=0;}
 bool Advance(FVector Position,bool bEligible,const UPokeMonsterBushEncounterSettings& Settings,float& OutTravel);
};

/** Existing one-shot test zone, with opt-in distance-based habitat encounters. */
UCLASS()
class POKEMONSTER_API APokeMonsterWildEncounterZone : public AActor
{
	GENERATED_BODY()
public:
	APokeMonsterWildEncounterZone();
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") TSoftObjectPtr<UPokeMonsterEncounterProfile> Profile;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") FPokeMonsterEncounterContext Context;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") int32 Seed = 5719;
	UPROPERTY(EditInstanceOnly, BlueprintReadOnly, Category="Wild Encounter") FName EncounterId = TEXT("Dev_ZoneWild");
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Bush Encounters") bool bDistanceBasedBushEncounters=false;
 UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="Bush Encounters") FName HabitatZoneId;
 UFUNCTION(BlueprintPure, Category="Bush Encounters") int32 GetBushChecks()const{return BushChecks;}
 UFUNCTION(BlueprintPure, Category="Bush Encounters") int32 GetBushStarts()const{return BushStarts;}
 static bool AreBushEncountersEnabled();
 bool HasTriggered() const { return bTriggered; }
protected:
	virtual void BeginPlay() override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
private:
	UFUNCTION() void RefreshPersistentState();
 UFUNCTION() void OnLeft(UPrimitiveComponent* Overlapped,AActor* OtherActor,UPrimitiveComponent* OtherComponent,int32 BodyIndex);
 void BeginBushTracking(class APokeMonsterPlayerCharacter* Player);
 void SampleBushTravel();
 TWeakObjectPtr<class APokeMonsterPlayerCharacter> BushPlayer;
 FPokeMonsterBushTravel BushTravel;
 FRandomStream BushRandom;
 FTimerHandle BushTimer;
 int32 BushChecks=0,BushStarts=0;
	UFUNCTION() void OnEntered(UPrimitiveComponent* Overlapped, AActor* OtherActor,
		UPrimitiveComponent* OtherComponent, int32 BodyIndex, bool bFromSweep, const FHitResult& Hit);
	UPROPERTY(VisibleAnywhere) TObjectPtr<UBoxComponent> Trigger;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> GroundMarker;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UTextRenderComponent> Label;
	bool bTriggered = false;
};
