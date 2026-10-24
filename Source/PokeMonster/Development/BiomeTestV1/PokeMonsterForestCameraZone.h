#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterForestCameraZone.generated.h"
class APawn;
class UBoxComponent;
class USpringArmComponent;
class UPokeMonsterCameraVisibilityComponent;
/** Explicit local opt-in. The ordinary camera and existing sight radii remain untouched elsewhere. */
UCLASS()
class POKEMONSTER_API APokeMonsterForestCameraZone : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterForestCameraZone();
 virtual void Tick(float DeltaSeconds) override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Forest Camera") TObjectPtr<UBoxComponent> Bounds;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Forest Camera",meta=(ClampMin="1200",ClampMax="2850")) float LocalArmLengthCm=1700.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Forest Camera",meta=(ClampMin="0.2",ClampMax="3")) float TransitionSeconds=.8f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Forest Camera",meta=(ClampMin="20",ClampMax="400")) float EdgeFeatherCm=180.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Forest Camera") bool bEnabled=true;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Transient,Category="Forest Camera") float CurrentAmount=0.f;
 /** Oriented local box membership, including a soft outside margin, no collision trigger or input binding. */
 static float TargetAmount(FVector LocalPoint,FVector Extent,float Feather);
 static float SmoothAmount(float Linear);
private:
 void Restore();
 TWeakObjectPtr<USpringArmComponent> Arm;
 TWeakObjectPtr<UPokeMonsterCameraVisibilityComponent> Visibility;
 TWeakObjectPtr<APawn> Viewer;
 float OriginalArmLength=2850.f;
};
