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
 static float SampleSpeed(const FVector& Delta,float Seconds,bool HasPrevious);
 /** Rejects invalid replacement data before altering a working visual. */
 bool SetSpecies(const UPokeMonsterCreatureSpeciesData* Species);
 UFUNCTION(BlueprintCallable) bool PlayReaction(EPokeMonsterCreatureClip Clip);
 UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USkeletalMeshComponent> Mesh;
 UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> Flame;
 UPROPERTY(Transient) TObjectPtr<UPokeMonsterCreaturePresentationData> Presentation;
 UPROPERTY(Transient, BlueprintReadOnly) TArray<TObjectPtr<UStaticMeshComponent>> EffectComponents;
 UPROPERTY(Transient, BlueprintReadOnly) float MotionSpeed=0.f;
 UPROPERTY(Transient, BlueprintReadOnly) EPokeMonsterCreatureClip Reaction=EPokeMonsterCreatureClip::Idle;
 uint32 ReactionSerial=0;
private:
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
