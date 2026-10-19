// Explicit development-only comparison of the six World Art V1 groups. No automatic gameplay hook.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/StaticMeshActor.h"
#include "EngineUtils.h"
#include "Components/HierarchicalInstancedStaticMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "HAL/IConsoleManager.h"

#if !UE_BUILD_SHIPPING && WITH_EDITOR
namespace PMWorldArtStudy
{
struct FGroup
{
 TWeakObjectPtr<UHierarchicalInstancedStaticMeshComponent> Component;
 bool Visible=false;int32 LOD=0;
};
static TArray<FGroup> Groups;
static TArray<TWeakObjectPtr<AStaticMeshActor>> Individuals;
static TWeakObjectPtr<UWorld> PreparedWorld;
static UWorld* FindWorld()
{
 if(!GEngine)return nullptr;
 for(const auto& C:GEngine->GetWorldContexts())if(C.World()&&(C.WorldType==EWorldType::PIE||C.WorldType==EWorldType::Game))
  if(UWorld::RemovePIEPrefix(C.World()->GetPackage()->GetName())==TEXT("/Game/Maps/Dev_TestMap_VisualV2"))return C.World();
 return nullptr;
}
static void Restore()
{
 for(const auto& G:Groups)if(auto* C=G.Component.Get()){C->SetVisibility(G.Visible);C->SetForcedLodModel(G.LOD);}
 for(const auto& A:Individuals)if(auto* P=A.Get())P->GetStaticMeshComponent()->SetVisibility(false);
}
static FAutoConsoleCommand PrepareCommand(TEXT("pm.WorldArt2.Prepare"),TEXT("Opt-in transient individual-object comparison, VisualV2 game world only."),FConsoleCommandDelegate::CreateLambda([]()
{
 UWorld* W=FindWorld();if(!W||PreparedWorld.Get()==W)return;
 Restore();for(const auto& A:Individuals)if(A.IsValid())A->Destroy();Individuals.Empty();Groups.Empty();PreparedWorld=W;
 for(TActorIterator<AActor> I(W);I;++I)if(I->GetActorLabel().StartsWith(TEXT("WAQ1_")))
 {
  auto* C=I->FindComponentByClass<UHierarchicalInstancedStaticMeshComponent>();if(!C)continue;
  if(C->CastShadow||C->GetCollisionEnabled()!=ECollisionEnabled::NoCollision){UE_LOG(LogTemp,Error,TEXT("WAQ2 unsafe source group"));return;}
  Groups.Add({C,C->IsVisible(),C->GetForcedLodModel()});
 }
 int32 Count=0;for(const auto& G:Groups)if(auto* C=G.Component.Get())for(int32 J=0;J<C->GetInstanceCount();++J)
 {
  FTransform T;C->GetInstanceTransform(J,T,true);FActorSpawnParameters P;P.ObjectFlags|=RF_Transient;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
  auto* A=W->SpawnActor<AStaticMeshActor>(AStaticMeshActor::StaticClass(),T,P);if(!A)continue;A->Tags.Add(TEXT("WAQ2_TransientIndividual"));A->SetActorTickEnabled(false);
  auto* S=A->GetStaticMeshComponent();S->SetMobility(EComponentMobility::Movable);S->SetStaticMesh(C->GetStaticMesh());
  for(int32 K=0;K<C->GetNumMaterials();++K)S->SetMaterial(K,C->GetMaterial(K));
  S->SetCollisionEnabled(ECollisionEnabled::NoCollision);S->SetGenerateOverlapEvents(false);S->SetCanEverAffectNavigation(false);S->SetCastShadow(false);
  S->bAffectDistanceFieldLighting=false;S->bAffectDynamicIndirectLighting=false;S->SetCullDistance(6500.f);S->SetForcedLodModel(G.LOD);S->SetVisibility(false);S->SetMobility(C->GetMobility());
  Individuals.Add(A);++Count;
 }
 UE_LOG(LogTemp,Display,TEXT("WAQ2 prepared groups=%d individuals=%d; transient only"),Groups.Num(),Count);
}));
// Runtime Python intentionally does not expose the editor-only material array.
// Use the engine API to release overrides safely before installing a tested palette.
static FAutoConsoleCommand ClearMaterialsCommand(TEXT("pm.WorldArt2.ClearMaterials"),TEXT("Explicit runtime-only clear for one of the six WAQ1 dressing groups."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 UWorld* W=FindWorld();if(!W||Args.Num()!=1)return;
 for(TActorIterator<AActor> I(W);I;++I)if(I->GetName()==Args[0]&&I->GetActorLabel().StartsWith(TEXT("WAQ1_")))
  if(auto* C=I->FindComponentByClass<UHierarchicalInstancedStaticMeshComponent>())if(!C->CastShadow&&C->GetCollisionEnabled()==ECollisionEnabled::NoCollision){C->EmptyOverrideMaterials();return;}
}));
static FAutoConsoleCommand ModeCommand(TEXT("pm.WorldArt2.Mode"),TEXT("Opt-in HISM/Individual/No175 or matched LOD0 variants; does not change camera, lighting or saved assets."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||PreparedWorld.Get()!=FindWorld()||Groups.Num()!=6||Individuals.Num()!=175)return;
 const FString& M=Args[0];if(M!=TEXT("HISM")&&M!=TEXT("Individual")&&M!=TEXT("No175")&&M!=TEXT("HISM_LOD0")&&M!=TEXT("Individual_LOD0"))return;
 const bool H=M==TEXT("HISM")||M==TEXT("HISM_LOD0"),I=M==TEXT("Individual")||M==TEXT("Individual_LOD0"),LOD0=M.EndsWith(TEXT("LOD0"));
 for(const auto& G:Groups)if(auto* C=G.Component.Get()){C->SetVisibility(G.Visible&&H);C->SetForcedLodModel(LOD0?1:G.LOD);}
 for(const auto& A:Individuals)if(auto* P=A.Get()){auto* C=P->GetStaticMeshComponent();C->SetVisibility(I);C->SetForcedLodModel(LOD0?1:0);}
 UE_LOG(LogTemp,Display,TEXT("WAQ2 representation=%s"),*M);
}));
}
#endif
