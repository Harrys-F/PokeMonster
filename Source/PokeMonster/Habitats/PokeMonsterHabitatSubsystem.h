#pragma once
#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRhythm.h"
#include "PokeMonsterHabitatSubsystem.generated.h"
class APokeMonsterVisibleWildCreatureActor;
class UPokeMonsterCreatureSpeciesData;
class UPokeMonsterEncounterProfile;

/** Natural population uses the existing surface/media contract and roaming component. */
UCLASS()
class POKEMONSTER_API APokeMonsterHabitatZone : public APokeMonsterBiomeHabitat
{
 GENERATED_BODY()
public:
 APokeMonsterHabitatZone();
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FName ZoneId;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FName HabitatType;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) int32 MaximumPopulation=2;
};
USTRUCT()
struct FPokeMonsterHabitatLayout
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere) FName Id;
 UPROPERTY(EditAnywhere) FName Type;
 UPROPERTY(EditAnywhere) FVector Center=FVector::ZeroVector;
 UPROPERTY(EditAnywhere) FVector Extent=FVector(600,600,300);
 UPROPERTY(EditAnywhere) int32 Maximum=2;
};
USTRUCT()
struct POKEMONSTER_API FPokeMonsterHabitatRule
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere) FName Species;
 UPROPERTY(EditAnywhere) TSoftObjectPtr<UPokeMonsterEncounterProfile> Profile;
 UPROPERTY(EditAnywhere) TArray<FName> Habitats;
 UPROPERTY(EditAnywhere) float Weight=1.f;
 UPROPERTY(EditAnywhere) int32 Maximum=2;
 UPROPERTY(EditAnywhere) float MinimumPlayerDistance=1100.f;
 UPROPERTY(EditAnywhere) float MinimumPeerDistance=220.f;
 /** Population preference only. Existing six activity/rhythm profiles retain authority. */
 UPROPERTY(EditAnywhere) EPokeMonsterActivityRhythm Rhythm=EPokeMonsterActivityRhythm::Flexible;
 bool Allows(FName Habitat) const {return Habitats.Contains(Habitat);}
 float WeightAt(double SecondsOfDay) const;
 bool IsValid()const;
};
UCLASS(Config=PokeMonsterHabitats,DefaultConfig)
class POKEMONSTER_API UPokeMonsterHabitatSettings : public UObject
{
 GENERATED_BODY()
public:
 UPROPERTY(Config,EditAnywhere) bool bEnableVisualV2=true;
 UPROPERTY(Config,EditAnywhere) int32 MaximumPopulation=10;
 UPROPERTY(Config,EditAnywhere) int32 MaximumSpecies=6;
 UPROPERTY(Config,EditAnywhere) float UpdateSeconds=2.f;
 UPROPERTY(Config,EditAnywhere) float MinimumResidenceSeconds=120.f;
 UPROPERTY(Config,EditAnywhere) float DespawnDistance=4200.f;
 UPROPERTY(Config,EditAnywhere) TArray<FPokeMonsterHabitatLayout> VisualV2Zones;
 UPROPERTY(Config,EditAnywhere) TArray<FPokeMonsterHabitatRule> Rules;
 bool IsValidConfiguration()const;
};
UCLASS()
class POKEMONSTER_API UPokeMonsterHabitatSubsystem : public UWorldSubsystem
{
 GENERATED_BODY()
public:
 virtual void OnWorldBeginPlay(UWorld& World) override;
 virtual void Deinitialize() override;
 UFUNCTION(BlueprintCallable) void SetPopulationEnabled(bool Enabled);
 UFUNCTION(BlueprintCallable) void RefreshPopulation();
 UFUNCTION(BlueprintPure) bool IsPopulationEnabled()const{return bEnabled;}
 UPROPERTY(Transient,BlueprintReadOnly) TArray<TObjectPtr<APokeMonsterHabitatZone>> Zones;
 UPROPERTY(Transient,BlueprintReadOnly) TArray<TObjectPtr<APokeMonsterVisibleWildCreatureActor>> Population;
 UPROPERTY(Transient,BlueprintReadOnly) int32 Spawned=0;
 UPROPERTY(Transient,BlueprintReadOnly) int32 Retired=0;
 UPROPERTY(Transient,BlueprintReadOnly) int32 RejectedPositions=0;
 UPROPERTY(Transient,BlueprintReadOnly) int32 Updates=0;
 UPROPERTY(Transient,BlueprintReadOnly) double LastUpdateMicroseconds=0;
 static bool IsVisualV2(const FString& Name);
 static FName PopulationId(FName Zone,int32 Slot,FName Species,int32 Day);
protected:
 virtual bool DoesSupportWorldType(EWorldType::Type Type)const override;
private:
 bool CandidateOutsideView(const FVector& Foot,const FVector& Extent)const;
 bool TryPopulate(APokeMonsterHabitatZone* Zone);
 void Retire(APokeMonsterVisibleWildCreatureActor* Actor);
 FTimerHandle UpdateTimer;
 bool bEnabled=false;
 FRandomStream Random{837521};
 UPROPERTY(Transient) TArray<TObjectPtr<UPokeMonsterCreatureSpeciesData>> Registered;
 UPROPERTY(Transient) TArray<TObjectPtr<UPokeMonsterEncounterProfile>> Profiles;
 TMap<TWeakObjectPtr<APokeMonsterVisibleWildCreatureActor>,double> BirthTimes;
};
