#include "PokeMonsterCreaturePolishLibrary.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/SkeletalMesh.h"
AActor* UPokeMonsterCreaturePolishLibrary::SpawnReviewActor(UObject* WorldContext, const bool bFloor, const FVector Location)
{
#if !UE_BUILD_SHIPPING
 UWorld* World = GEngine ? GEngine->GetWorldFromContextObject(WorldContext, EGetWorldErrorMode::ReturnNull) : nullptr;
 if (!World || World->WorldType != EWorldType::PIE || !World->GetMapName().Contains(TEXT("Dev_TestMap_VisualV2")) || Location.ContainsNaN()) return nullptr;
 FActorSpawnParameters Spawn; Spawn.ObjectFlags |= RF_Transient;
 Spawn.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 AActor* Actor = bFloor ? static_cast<AActor*>(World->SpawnActor<AStaticMeshActor>(Location, FRotator::ZeroRotator, Spawn))
  : World->SpawnActor<APokeMonsterCreatureVisualActor>(Location, FRotator::ZeroRotator, Spawn);
 if (Actor) Actor->Tags.Add(TEXT("CreaturePolishV4Review"));
 return Actor;
#else
 return nullptr;
#endif
}

bool UPokeMonsterCreaturePolishLibrary::HaveMatchingReferenceSkeleton(USkeletalMesh* CandidateMesh, USkeletalMesh* ReferenceMesh)
{
 if (!CandidateMesh || !ReferenceMesh) return false;
 const auto& A = CandidateMesh->GetRefSkeleton(); const auto& B = ReferenceMesh->GetRefSkeleton();
 if (A.GetNum() != B.GetNum()) return false;
 for (int32 Index=0; Index<A.GetNum(); ++Index)
  if (A.GetBoneName(Index) != B.GetBoneName(Index) || A.GetParentIndex(Index) != B.GetParentIndex(Index)
   || !A.GetRefBonePose()[Index].Equals(B.GetRefBonePose()[Index], .001f)) return false;
 return true;
}

bool UPokeMonsterCreaturePolishLibrary::ReuseReviewedGlurakSkeleton(USkeletalMesh* CandidateMesh, USkeletalMesh* ReferenceMesh)
{
#if WITH_EDITOR
 if (!CandidateMesh || !ReferenceMesh || CandidateMesh == ReferenceMesh
  || !CandidateMesh->GetPathName().StartsWith(TEXT("/Game/Characters/Creatures/Glurak/PolishV4/"))
  || !ReferenceMesh->GetPathName().StartsWith(TEXT("/Game/Characters/Creatures/Glurak/MeshyV1/"))
  || !HaveMatchingReferenceSkeleton(CandidateMesh, ReferenceMesh)) return false;
 for (const auto& Context : GEngine->GetWorldContexts()) if (Context.WorldType == EWorldType::PIE) return false;
 CandidateMesh->Modify(); CandidateMesh->SetSkeleton(ReferenceMesh->GetSkeleton());
 return true;
#else
 return false;
#endif
}
