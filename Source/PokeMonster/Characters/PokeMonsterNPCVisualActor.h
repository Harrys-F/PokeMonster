#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PokeMonsterNPCVisualActor.generated.h"
class USkeletalMeshComponent;
class UStaticMeshComponent;
class UStaticMesh;
class UAnimSequence;
class UPaperSpriteComponent;
/** Optional presentation attached to an existing NPC. Owns no interaction, collision or story state. */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterNPCVisualActor : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterNPCVisualActor();
 UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USkeletalMeshComponent> Visual;
 /** Optional unrigged presentation; never pretends to provide skeletal animation. */
 UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> StaticVisual;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Presentation") TObjectPtr<UStaticMesh> StaticPresentationMesh;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Presentation") bool bShadowlessInteriorPresentation = false;
 UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category="NPC Presentation") TObjectPtr<AActor> SourceActor;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Presentation") TObjectPtr<UAnimSequence> IdleAnimation;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Presentation") TObjectPtr<UAnimSequence> ConversationAnimation;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Presentation") bool bUseVisual = true;
 /** Opt-in motion presentation; never drives the gameplay source actor. */
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") bool bEnableMotionPresentation = false;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") TObjectPtr<UAnimSequence> WalkAnimation;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") TObjectPtr<UAnimSequence> TurnLeftAnimation;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") TObjectPtr<UAnimSequence> TurnRightAnimation;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion", meta=(ClampMin="1")) float AuthoredWalkSpeed = 150.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion", meta=(ClampMin="0.05")) float MotionBlendSeconds = .22f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion", meta=(ClampMin="1")) float FacingDegreesPerSecond = 180.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") float ForwardYawOffset = 0.f;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") bool bEnableAccessoryMotion = false;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") FName CapeUpperBone = TEXT("cape_upper");
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") FName CapeLowerBone = TEXT("cape_lower");
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") FName CapeLeftBone = TEXT("cape_l");
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") FName CapeRightBone = TEXT("cape_r");
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="NPC Motion") FName BagBone = TEXT("bag");
 UPROPERTY(BlueprintReadOnly, Transient, Category="NPC Motion") float PresentationSpeed = 0.f;
 /** Game-thread sample, called by animation PreUpdate; no additional permanent actor tick. */
 void SampleMotion(float DeltaSeconds);
 UFUNCTION(BlueprintCallable, Category="NPC Presentation") void RefreshPresentation();
 UFUNCTION(BlueprintPure, Category="NPC Presentation") bool IsConversing() const { return bConversing; }
 virtual void OnConstruction(const FTransform& Transform) override;
 virtual void Tick(float DeltaSeconds) override;
protected:
 virtual void BeginPlay() override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
private:
 UFUNCTION() void HandleDialogueChanged();
 UPROPERTY() TObjectPtr<UPaperSpriteComponent> FallbackSprite;
 UPROPERTY() bool bFallbackWasVisible = true;
 bool bConversing = false;
 FVector PreviousSourceLocation = FVector::ZeroVector;
 bool bHaveSourceSample = false;
 double PreviousSourceSampleTime = 0.;
 FRotator DesiredRotation = FRotator::ZeroRotator;
};
