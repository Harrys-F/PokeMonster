#pragma once
#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "PokeMonsterCreatureTestGround.generated.h"
class APokeMonsterCreatureVisualActor;
class UPokeMonsterCreatureRoamingComponent;
class UPokeMonsterCreatureSpeciesData;
class UTextRenderComponent;
class AStaticMeshActor;

/** Automatically available in ordinary VisualV2 PIE. Visual specimens own no encounter/save state. */
UCLASS()
class POKEMONSTER_API UPokeMonsterCreatureTestGround : public UTickableWorldSubsystem
{
 GENERATED_BODY()
public:
 /** Editor console resolves only an unambiguous active VisualV2 game world. */
 static UWorld* ResolveConsoleWorld(UWorld* Context);
 UFUNCTION(BlueprintCallable) bool VisitTarget(const FString& Target);
 UFUNCTION(BlueprintPure) TArray<FString> GetImportTargets();
 static FString ImportRoot() { return TEXT("/Game/Characters/Creatures/ModelIntakeV6"); }
 static bool IsInspectionAsset(const FString& PackagePath);
 static bool SupportsInspectionMode(const FString& Value);
 static bool IsSupportedMap(const FString& MapName, EWorldType::Type Type);
 // Separate test presentation stays beyond the visible south boundary of the main world.
 static FVector Center() { return FVector(-7500,-20000,-20000); }
 static FVector Station(int32 Index,int32 Columns=5,float Spacing=1800.f);
 UFUNCTION(BlueprintPure) FVector GetStation(int32 Index)const{return Station(Index,Columns,Spacing);}
 UFUNCTION(BlueprintCallable) bool ResetModels();
 UFUNCTION(BlueprintCallable) void ListModels();
 virtual void OnWorldBeginPlay(UWorld& World) override;
 virtual void Tick(float DeltaTime) override;
 virtual TStatId GetStatId() const override;
 virtual void Deinitialize() override;
 UFUNCTION(BlueprintCallable,Category="Development|Pokemon Test Ground") bool Visit(int32 StationNumber=0);
 UFUNCTION(BlueprintCallable,Category="Development|Pokemon Test Ground") bool ReturnToWorld();
 /** auto, idle, walk, run; no changes to shared species or presentation assets. */
 UFUNCTION(BlueprintCallable,Category="Development|Pokemon Test Ground") bool SetMode(const FString& Mode);
 UFUNCTION(BlueprintCallable,Category="Development|Pokemon Test Ground") bool React(const FString& Role);
 UFUNCTION(BlueprintPure,Category="Development|Pokemon Test Ground") bool HasReturnPosition() const { return bHaveReturn; }
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) TArray<TObjectPtr<UPokeMonsterCreatureSpeciesData>> Species;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) TArray<TObjectPtr<APokeMonsterCreatureVisualActor>> Specimens;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) TArray<TObjectPtr<UPokeMonsterCreatureRoamingComponent>> Movements;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) FString Mode=TEXT("auto");
protected:
 virtual bool DoesSupportWorldType(EWorldType::Type Type) const override;
private:
 bool CanTravel() const;
 void DiscoverImports(bool bScanDisk=false);
 bool VisitImport(const FString& Target);
 void EndImportInspection();
 UPROPERTY(Transient) TObjectPtr<AStaticMeshActor> ImportSpecimen;
 TMap<FString,FSoftObjectPath> ImportModels;
 FString ActiveImport;
 FTransform ImportOrigin;
 bool Travel(const FTransform& Destination);
 void Message(const FString& Text) const;
 UPROPERTY(Transient) TArray<TObjectPtr<AActor>> OwnedActors;
 UPROPERTY(Transient) TArray<TObjectPtr<UTextRenderComponent>> Labels;
 TArray<FVector2D> MovementReferenceSpeeds;
 TArray<int32> RouteSteps;
 TArray<float> TurnVelocity;
 int32 Columns=5;
 float Spacing=1800.f;
 FTransform ReturnPosition;
 FVector ReturnFacing=FVector::ForwardVector;
 FRotator ReturnOrbit=FRotator::ZeroRotator;
 float ReturnDistance=350.f;
 bool bReturnThirdPerson=true;
 TWeakObjectPtr<APawn> ReturnPawn;
 bool bHaveReturn=false;
 float Elapsed=0.f;
};
