#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "PokeMonsterCreaturePolishLibrary.generated.h"
class APokeMonsterCreatureVisualActor;
class USkeletalMesh;
class UPokeMonsterCreatureSpeciesData;
/** Explicit development review helpers, never available in a normal game world. */
UCLASS()
class POKEMONSTER_API UPokeMonsterCreaturePolishLibrary : public UBlueprintFunctionLibrary
{
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintPure, Category="Development|Creature Review")
 static bool HaveMatchingReferenceSkeleton(USkeletalMesh* CandidateMesh, USkeletalMesh* ReferenceMesh);
 UFUNCTION(BlueprintCallable, Category="Development|Creature Review")
 static bool ReuseReviewedGlurakSkeleton(USkeletalMesh* CandidateMesh, USkeletalMesh* ReferenceMesh);
 UFUNCTION(BlueprintCallable, Category="Development|Creature Review")
 static AActor* SpawnReviewActor(UObject* WorldContext, bool bFloor, FVector Location);
 UFUNCTION(BlueprintCallable, Category="Development|Creature Review")
 static bool ConfigureGroundHoverReview(APokeMonsterCreatureVisualActor* Visual, UPokeMonsterCreatureSpeciesData* Species);
 UFUNCTION(BlueprintPure, Category="Development|Creature Review")
 static FTransform GetReferenceBoneTransform(USkeletalMesh* Mesh, FName Bone);
 UFUNCTION(BlueprintPure, Category="Development|Creature Review")
 static bool ProbeReviewHoverClearance(APokeMonsterCreatureVisualActor* Visual, float Height);
};
