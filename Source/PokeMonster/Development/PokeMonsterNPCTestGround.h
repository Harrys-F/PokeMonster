#pragma once
#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "PokeMonsterNPCTestGround.generated.h"
class APokeMonsterNPC;
class APokeMonsterNPCVisualActor;
class UPokeMonsterNPCPresentationData;
class UPokeMonsterDialogueData;
/** Normal editor PIE fixture. Existing NPC/dialogue/presentation objects, never save identities. */
UCLASS()
class POKEMONSTER_API UPokeMonsterNPCTestGround : public UTickableWorldSubsystem
{
 GENERATED_BODY()
public:
 static bool IsSupportedMap(const FString& Name,EWorldType::Type Type);
 static FVector Center(){return FVector(-7500,3000,0);}
 static FVector Station(int32 Index){return Center()+FVector((Index%4-1.5f)*1100.f,(Index/4-1.f)*1100.f,0);}
 virtual void OnWorldBeginPlay(UWorld& World) override;
 virtual void Tick(float Delta) override;
 virtual TStatId GetStatId() const override;
 virtual void Deinitialize() override;
 UFUNCTION(BlueprintCallable, Category="Development|NPC") bool Visit(int32 Number=0);
 UFUNCTION(BlueprintCallable, Category="Development|NPC") bool ReturnToWorld();
 UFUNCTION(BlueprintCallable, Category="Development|NPC") bool SetMode(const FString& Requested);
 UFUNCTION(BlueprintCallable, Category="Development|NPC") bool Greet();
 UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly) TArray<TObjectPtr<APokeMonsterNPC>> Specimens;
 UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly) TArray<TObjectPtr<APokeMonsterNPCVisualActor>> Visuals;
 UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly) FString Mode=TEXT("auto");
protected:
 virtual bool DoesSupportWorldType(EWorldType::Type Type) const override;
private:
 bool CanTravel() const;
 bool Travel(const FTransform& T);
 UPROPERTY(Transient) TObjectPtr<UPokeMonsterDialogueData> TestDialogue;
 UPROPERTY(Transient) TArray<TObjectPtr<AActor>> Owned;
 UPROPERTY(Transient) TArray<TObjectPtr<UPokeMonsterNPCPresentationData>> Profiles;
 TArray<FVector> Velocities;
 TArray<FVector> Targets;
 TArray<float> Pauses;
 FTransform ReturnTransform;
 TWeakObjectPtr<APawn> ReturnPawn;
 bool bHaveReturn=false;
 bool bOwnsMemoryPreview=false;
 float Elapsed=0.f;
};
