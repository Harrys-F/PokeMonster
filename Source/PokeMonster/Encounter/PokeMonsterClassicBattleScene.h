#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterBattleEnvironment.h"
#include "PokeMonsterClassicBattleScene.generated.h"
class USceneCaptureComponent2D;
class UTextureRenderTarget2D;
class UStaticMeshComponent;
class UPointLightComponent;
class UInstancedStaticMeshComponent;
class UStaticMesh;
class UMaterialInterface;
class APokeMonsterCreatureVisualActor;
class UPokeMonsterCreatureSpeciesData;
/** Transient same-world presentation. Never moves the player or changes the view target. */
UCLASS(Transient)
class POKEMONSTER_API APokeMonsterClassicBattleScene : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterClassicBattleScene();
 void Configure(const UPokeMonsterCreatureSpeciesData* A,const UPokeMonsterCreatureSpeciesData* B,AActor* GroundReference,EPokeMonsterBattleEnvironment Theme=EPokeMonsterBattleEnvironment::Auto,FName Region=NAME_None,AActor* EncounterSource=nullptr);
 static EPokeMonsterBattleEnvironment ThemeForRegion(FName Region);
 static EPokeMonsterBattleEnvironment ResolveEnvironment(EPokeMonsterBattleEnvironment Requested,FName Region,AActor* Reference);
 void React(bool bPlayer,FName Step,int32 Damage);
 virtual void Tick(float DeltaSeconds)override;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) EPokeMonsterBattleEnvironment Environment=EPokeMonsterBattleEnvironment::Meadow;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) float FramingDistance=610.f;
 UPROPERTY(Transient)TArray<TObjectPtr<UInstancedStaticMeshComponent>> Dressing;
 UPROPERTY()TMap<FName,TObjectPtr<UStaticMesh>> DressingMeshes;
 UPROPERTY()TMap<FName,TObjectPtr<UMaterialInterface>> GroundMaterials;
private:
 void BuildEnvironment(float Fit);
 FVector RestCamera;
 float PulseTime=1.f,PulseStrength=0.f;
public:
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneCaptureComponent2D> Capture;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> Floor;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<UPointLightComponent> PresentationFill;
 UPROPERTY(Transient,BlueprintReadOnly) TObjectPtr<UTextureRenderTarget2D> Target;
 UPROPERTY(Transient,BlueprintReadOnly) TObjectPtr<APokeMonsterCreatureVisualActor> PlayerVisual;
 UPROPERTY(Transient,BlueprintReadOnly) TObjectPtr<APokeMonsterCreatureVisualActor> OpponentVisual;
 FVector2D ScreenAnchor(bool bPlayer,bool bGround=false) const;
};
