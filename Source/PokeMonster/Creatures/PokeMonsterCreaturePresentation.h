#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "GameFramework/Actor.h"
#include "Animation/AnimInstance.h"
#include "PokeMonsterCreaturePresentation.generated.h"
class USkeletalMesh;
class UAnimSequence;
class UStaticMesh;
class UMaterialInterface;
class USkeletalMeshComponent;
class UStaticMeshComponent;
class UPointLightComponent;
class UPokeMonsterCreatureSpeciesData;
class UPokeMonsterCreatureRoamingComponent;
class USceneComponent;

UENUM(BlueprintType)
enum class EPokeMonsterCreatureClip : uint8 { Idle, Walk, Run, Attack, Hit, Faint, Happy };

/** Classification only: never selects a humanoid rig or retarget automatically. */
UENUM(BlueprintType)
enum class EPokeMonsterCreatureRigFamily : uint8 { Custom, Biped, Quadruped, Serpentine, Winged, Aquatic, Floating };

/** Optional low-cost mesh effect; sockets belong to each model's own skeleton. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureEffectAnchor
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere, BlueprintReadOnly) FName Id;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) FName Socket;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMesh> Mesh;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) TObjectPtr<UMaterialInterface> Material;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) FTransform Offset=FTransform::Identity;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bWorldUpright=false;
};

/** Optional visuals; contains no battle stats, party state or save data. Units are centimetres. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterCreaturePresentationData : public UDataAsset
{
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintPure, Category="Creature|Import") TArray<FString> GetValidationErrors() const;
 /** Import metadata only. Zero means not yet measured; never rescales existing assets. */
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Import") EPokeMonsterCreatureRigFamily RigFamily=EPokeMonsterCreatureRigFamily::Custom;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Import", meta=(ClampMin="0")) float ReferenceSizeCm=0.f;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Import") FString SizeSource;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Effects") TArray<FPokeMonsterCreatureEffectAnchor> EffectAnchors;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) TObjectPtr<USkeletalMesh> Mesh;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) TMap<EPokeMonsterCreatureClip,TObjectPtr<UAnimSequence>> Clips;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, meta=(ClampMin="1")) float WalkSpeed=35.f;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, meta=(ClampMin="1")) float RunSpeed=60.f;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) float GroundOffsetCm=0.f;
 /** Optional authored swim layer. Zero aquatic context leaves all land/battle clips unchanged. */
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Swimming") TObjectPtr<UAnimSequence> SwimIdleClip;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Swimming") TObjectPtr<UAnimSequence> SwimClip;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Swimming", meta=(ClampMin="1")) float SwimReferenceSpeed=35.f;
 /** Optional low hover above the same walkable route, never a flight navigation mode. */
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ground Hover") bool bAllowGroundHover=false;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ground Hover") TObjectPtr<UAnimSequence> TakeoffClip;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ground Hover") TObjectPtr<UAnimSequence> HoverClip;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ground Hover") TObjectPtr<UAnimSequence> LandClip;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ground Hover", meta=(ClampMin="50",ClampMax="150")) float HoverHeightCm=90.f;
 /** Small visual-only float, applied exclusively with an overworld movement context. */
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Overworld Float", meta=(ClampMin="0",ClampMax="10")) float OverworldFloatAmplitudeCm=0.f;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMesh> TailFlame;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) TObjectPtr<UMaterialInterface> FlameMaterial;
 UPROPERTY(EditAnywhere, BlueprintReadOnly) FName FlameBone=TEXT("tail_socket");
};

/** Shared world/battle rendering only. It deliberately has no collision or gameplay identity. */
UCLASS()
class POKEMONSTER_API APokeMonsterCreatureVisualActor : public AActor
{
 GENERATED_BODY()
public:
 APokeMonsterCreatureVisualActor();
 virtual void Tick(float DeltaSeconds) override;
 /** Explicit roaming context; battle visuals never receive one. */
 void SetGroundHoverContext(UPokeMonsterCreatureRoamingComponent* Context);
 UFUNCTION(BlueprintPure) float GetGroundHoverHeight() const { return HoverHeight; }
 UFUNCTION(BlueprintPure) FString GetGroundHoverState() const;
 UPROPERTY(Transient, BlueprintReadOnly) float HoverHeight=0.f;
 UPROPERTY(Transient, BlueprintReadOnly) float HoverClipTime=0.f;
 UPROPERTY(Transient, BlueprintReadOnly) TObjectPtr<UAnimSequence> ActiveHoverClip;
 UPROPERTY(Transient, BlueprintReadOnly) float HoverPoseAlpha=0.f;
 UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USceneComponent> VisualOrigin;
 static float SampleSpeed(const FVector& Delta,float Seconds,bool HasPrevious);
 /** Rejects invalid replacement data before altering a working visual. */
 UFUNCTION(BlueprintCallable, Category="Creature|Presentation") bool SetSpecies(const UPokeMonsterCreatureSpeciesData* Species);
 /** Visual-only candidate preview; does not mutate a species asset or instance state. */
 UFUNCTION(BlueprintCallable, Category="Creature|Presentation") bool SetPresentation(UPokeMonsterCreaturePresentationData* Candidate);
 UFUNCTION(BlueprintCallable) bool PlayReaction(EPokeMonsterCreatureClip Clip);
 UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USkeletalMeshComponent> Mesh;
 UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> Flame;
 UPROPERTY(Transient) TObjectPtr<UPokeMonsterCreaturePresentationData> Presentation;
 UPROPERTY(Transient, BlueprintReadOnly) TArray<TObjectPtr<UStaticMeshComponent>> EffectComponents;
 UPROPERTY(Transient, BlueprintReadOnly) float MotionSpeed=0.f;
 UPROPERTY(Transient, BlueprintReadOnly) EPokeMonsterCreatureClip Reaction=EPokeMonsterCreatureClip::Idle;
 /** Per-visual idle phase only; locomotion cadence remains speed-driven. */
 UPROPERTY(Transient,BlueprintReadWrite) float IdlePhaseOffset=0.f;
 /** Explicit aquatic context; optional authored swim layer, otherwise existing idle/float fallback. Zero elsewhere. */
 UPROPERTY(Transient,BlueprintReadOnly) float AquaticPoseAlpha=0.f;
 uint32 ReactionSerial=0;
private:
 void UpdateGroundHover(float Delta);
 TWeakObjectPtr<UPokeMonsterCreatureRoamingComponent> HoverContext;
 enum class EHoverState : uint8 { Grounded, Takeoff, Hover, Landing };
 EHoverState HoverState=EHoverState::Grounded;
 float HoverStateTime=0.f, GroundWait=7.f, LandingHeight=0.f, HoverCheckRemaining=0.f;
 bool bHoverClear=false;
 bool bUsingAmbientFloat=false;
 bool bBoundFlightBattlePause=false;
 FVector PreviousLocation=FVector::ZeroVector;
 bool bHavePrevious=false;
};

UCLASS(Transient)
class POKEMONSTER_API UPokeMonsterCreatureAnimInstance : public UAnimInstance
{
 GENERATED_BODY()
public:
 UPROPERTY(BlueprintReadOnly) float WalkBlend=0.f;
 UPROPERTY(BlueprintReadOnly) float RunBlend=0.f;
 UPROPERTY(BlueprintReadOnly) float ReactionBlend=0.f;
 virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
 virtual void DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy) override;
};
