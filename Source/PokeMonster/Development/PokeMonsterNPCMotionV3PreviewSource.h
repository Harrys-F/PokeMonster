#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterNPCMotionV3PreviewSource.generated.h"
/** Explicit test source only. No AI, interaction, story state, collision or autonomous tick. */
UCLASS()
class POKEMONSTER_API APokeMonsterNPCMotionV3PreviewSource : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterNPCMotionV3PreviewSource();
 virtual FVector GetVelocity() const override { return PreviewVelocity; }
 /** Reproduces the velocity contract of a movement controller. Restricted to the NPCMotionV3 test world. */
 UFUNCTION(BlueprintCallable, Category="Development", meta=(DevelopmentOnly)) void SetPreviewMotion(FVector Location, FVector Velocity);
private:
 FVector PreviewVelocity=FVector::ZeroVector;
};
