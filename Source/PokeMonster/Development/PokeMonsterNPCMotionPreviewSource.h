#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterNPCMotionPreviewSource.generated.h"
/** Explicit test source only. No AI, interaction, story state, collision or autonomous tick. */
UCLASS()
class POKEMONSTER_API APokeMonsterNPCMotionPreviewSource : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterNPCMotionPreviewSource();
 virtual FVector GetVelocity() const override { return PreviewVelocity; }
 /** Reproduces the velocity contract of a movement controller. Restricted to the NPCMotionV2 test world. */
 UFUNCTION(BlueprintCallable, Category="Development", meta=(DevelopmentOnly)) void SetPreviewMotion(FVector Location, FVector Velocity);
private:
 FVector PreviewVelocity=FVector::ZeroVector;
};
