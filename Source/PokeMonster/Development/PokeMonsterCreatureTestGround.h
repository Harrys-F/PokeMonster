#pragma once
#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "PokeMonsterCreatureTestGround.generated.h"
class APokeMonsterCreatureVisualActor;
class UPokeMonsterCreatureRoamingComponent;
class UTextRenderComponent;

/** Automatically available in ordinary VisualV2 PIE. Visual specimens own no encounter/save state. */
UCLASS()
class POKEMONSTER_API UPokeMonsterCreatureTestGround : public UTickableWorldSubsystem
{
 GENERATED_BODY()
public:
 static bool IsSupportedMap(const FString& MapName, EWorldType::Type Type);
 static FVector Center() { return FVector(-7500,-4000,0); }
 static FVector Station(int32 Index);
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
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) TArray<TObjectPtr<APokeMonsterCreatureVisualActor>> Specimens;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) TArray<TObjectPtr<UPokeMonsterCreatureRoamingComponent>> Movements;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly) FString Mode=TEXT("auto");
protected:
 virtual bool DoesSupportWorldType(EWorldType::Type Type) const override;
private:
 bool CanTravel() const;
 bool Travel(const FTransform& Destination);
 void Message(const FString& Text) const;
 UPROPERTY(Transient) TArray<TObjectPtr<AActor>> OwnedActors;
 UPROPERTY(Transient) TArray<TObjectPtr<UTextRenderComponent>> Labels;
 TArray<FVector2D> MovementReferenceSpeeds;
 FTransform ReturnPosition;
 TWeakObjectPtr<APawn> ReturnPawn;
 bool bHaveReturn=false;
 float Elapsed=0.f;
};
