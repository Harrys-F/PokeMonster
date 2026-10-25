#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PokeMonsterNPCPresentationData.generated.h"
class USkeletalMesh;
class UAnimSequence;
class UMaterialInterface;
/** Reusable appearance only; no profession, quest, dialogue or save identity. */
UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterNPCPresentationData : public UDataAsset
{
 GENERATED_BODY()
public:
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") FName TechnicalId;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") FString OriginalSource;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") FText Limitations;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<USkeletalMesh> Mesh;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TArray<TObjectPtr<UMaterialInterface>> Materials;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<UAnimSequence> Idle;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<UAnimSequence> Walk;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<UAnimSequence> Run;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<UAnimSequence> Talk;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<UAnimSequence> Greeting;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<UAnimSequence> TurnLeft;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") TObjectPtr<UAnimSequence> TurnRight;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC", meta=(ClampMin="1")) float ReferenceHeightCm=180.f;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC", meta=(ClampMin="0")) float WalkSpeed=120.f;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC", meta=(ClampMin="0")) float RunSpeed=220.f;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") bool bFootContacts=true;
 UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="NPC") bool bAccessoryMotion=false;
 UFUNCTION(BlueprintPure, Category="NPC") TArray<FString> GetValidationErrors() const;
};
