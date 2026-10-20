#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterClassicBattleScene.generated.h"
class USceneCaptureComponent2D;
class UTextureRenderTarget2D;
class UStaticMeshComponent;
class UPointLightComponent;
class APokeMonsterCreatureVisualActor;
class UPokeMonsterCreatureSpeciesData;
/** Transient same-world presentation. Never moves the player or changes the view target. */
UCLASS(Transient)
class POKEMONSTER_API APokeMonsterClassicBattleScene : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterClassicBattleScene();
 void Configure(const UPokeMonsterCreatureSpeciesData* A,const UPokeMonsterCreatureSpeciesData* B,AActor* GroundReference);
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneCaptureComponent2D> Capture;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> Floor;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<UPointLightComponent> PresentationFill;
 UPROPERTY(Transient,BlueprintReadOnly) TObjectPtr<UTextureRenderTarget2D> Target;
 UPROPERTY(Transient,BlueprintReadOnly) TObjectPtr<APokeMonsterCreatureVisualActor> PlayerVisual;
 UPROPERTY(Transient,BlueprintReadOnly) TObjectPtr<APokeMonsterCreatureVisualActor> OpponentVisual;
 FVector2D ScreenAnchor(bool bPlayer) const;
};
