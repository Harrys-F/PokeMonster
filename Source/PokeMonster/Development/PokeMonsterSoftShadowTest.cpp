#include "PokeMonsterSoftShadowTest.h"
#include "CoreMinimal.h"
#include "Engine/World.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "Containers/Ticker.h"
#include "HAL/IConsoleManager.h"
#include "Components/DecalComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "Components/MeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/Character.h"
#include "Materials/MaterialInterface.h"
#include "UObject/StrongObjectPtr.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Characters/PokeMonsterNPCVisualActor.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Encounter/PokeMonsterTrainerNPC.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"

#if !UE_BUILD_SHIPPING
namespace PMSoftShadowTest
{
namespace
{
struct FOriginal { TWeakObjectPtr<UPrimitiveComponent> Component; bool Shadow; };
struct FBlob
{
 TWeakObjectPtr<UPrimitiveComponent> Source;
 TWeakObjectPtr<AActor> Mover;
 TWeakObjectPtr<UDecalComponent> Decal;
 FVector Base = FVector::ZeroVector;
 float RadiusX = 0.f, RadiusY = 0.f;
 bool Grounded = false;
 FVector GroundPoint = FVector::ZeroVector, GroundNormal = FVector::UpVector;
 double NextGroundTrace = 0.;
};
struct FState
{
 TWeakObjectPtr<UWorld> World;
 TWeakObjectPtr<AActor> Holder;
 TArray<FOriginal> Originals;
 TArray<FBlob> Blobs;
 FTSTicker::FDelegateHandle Tick;
 FDelegateHandle PostActorTick;
 int32 Trees = 0, Characters = 0, BushComponents = 0, SmallPlants = 0;

 void Place(FBlob& B)
 {
  auto* W=World.Get();auto* D=B.Decal.Get();auto* S=B.Source.Get();if(!W||!D||!S)return;
  if(auto* M=B.Mover.Get())B.Base=M->GetActorLocation();
  if(!B.Mover.IsValid()||W->GetTimeSeconds()>=B.NextGroundTrace||FVector::DistSquared2D(B.Base,B.GroundPoint)>10000.f)
  {
   FCollisionQueryParams Q(SCENE_QUERY_STAT(PMSoftShadowFloor),false);
   Q.AddIgnoredActor(Holder.Get());Q.AddIgnoredActor(S->GetOwner());
   TArray<FHitResult> Hits;
   W->LineTraceMultiByObjectType(Hits,B.Base+FVector(0,0,80),B.Base-FVector(0,0,260),FCollisionObjectQueryParams(ECC_WorldStatic),Q);
   B.Grounded=false;B.NextGroundTrace=W->GetTimeSeconds()+.05;
   for(const auto& H:Hits)if(H.bBlockingHit&&H.ImpactNormal.Z>.65f)
   {B.Grounded=true;B.GroundPoint=H.ImpactPoint;B.GroundNormal=H.ImpactNormal;break;}
  }
  if(B.Grounded)
  {
   FVector Position=B.Base;
   Position.Z=B.GroundPoint.Z-((Position.X-B.GroundPoint.X)*B.GroundNormal.X+(Position.Y-B.GroundPoint.Y)*B.GroundNormal.Y)/B.GroundNormal.Z;
   D->SetWorldLocation(Position+B.GroundNormal*2.f);
   D->SetWorldRotation(FRotationMatrix::MakeFromX(-B.GroundNormal).Rotator());
  }
  D->SetVisibility(B.Grounded&&S->IsVisible()&&!S->bHiddenInGame&&!S->GetOwner()->IsHidden());
 }
 void Add(UPrimitiveComponent* S,AActor* Mover,const FVector& Base,float RX,float RY,UMaterialInterface* Material)
 {
  auto* D=NewObject<UDecalComponent>(Holder.Get(),NAME_None,RF_Transient);
  D->SetupAttachment(Holder->GetRootComponent());D->SetDecalMaterial(Material);
  D->DecalSize=FVector(Mover?18.f:65.f,RY,RX);D->SetFadeScreenSize(.001f);
  D->RegisterComponentWithWorld(World.Get());
  FBlob B{S,Mover,D,Base,RX,RY,false};Place(B);Blobs.Add(B);
 }
 void Restore()
 {
  FTSTicker::GetCoreTicker().RemoveTicker(Tick);
  FWorldDelegates::OnWorldPostActorTick.Remove(PostActorTick);
  for(const auto& S:Originals)if(auto* C=S.Component.Get())C->SetCastShadow(S.Shadow);
  for(const auto& B:Blobs)if(auto* D=B.Decal.Get())D->DestroyComponent();
  if(auto* A=Holder.Get())A->Destroy();
 }
};
TUniquePtr<FState> Active;
}

void Stop(){if(Active){Active->Restore();Active.Reset();}}

bool Enable(UWorld* W)
{
 UE_LOG(LogTemp,Display,TEXT("PM_SOFT_BEGIN"));
 Stop();
 if(!W||(W->WorldType!=EWorldType::PIE&&W->WorldType!=EWorldType::Game)||!W->GetMapName().Contains(TEXT("Dev_TestMap_VisualV2GPUBottleneckV1")))return false;
 auto* TreeMaterial=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Development/VisualV2AASoftShadowsV1/MI_TreeBlob.MI_TreeBlob"));
 auto* Figure=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Development/VisualV2AASoftShadowsV1/MI_FigureBlob.MI_FigureBlob"));
 if(!TreeMaterial||!Figure)return false;
 UE_LOG(LogTemp,Display,TEXT("PM_SOFT_MATERIALS"));
 auto S=MakeUnique<FState>();S->World=W;
 FActorSpawnParameters P;P.ObjectFlags|=RF_Transient;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* Holder=W->SpawnActor<AActor>(FVector::ZeroVector,FRotator::ZeroRotator,P);if(!Holder)return false;
 S->Holder=Holder;auto* Root=NewObject<USceneComponent>(Holder,NAME_None,RF_Transient);Holder->SetRootComponent(Root);Root->RegisterComponent();
 UE_LOG(LogTemp,Display,TEXT("PM_SOFT_HOLDER"));
 TSet<AActor*> Presented;
 for(TActorIterator<APokeMonsterNPCVisualActor> I(W);I;++I)if(I->bUseVisual&&I->SourceActor&&I->Visual&&I->Visual->IsVisible())Presented.Add(I->SourceActor);
 for(TObjectIterator<UPrimitiveComponent> I;I;++I)
 {
  auto* C=*I;if(C->GetWorld()!=W||!C->GetOwner()||!C->IsRegistered()||!C->IsVisible()||C->bHiddenInGame||C->GetOwner()->IsHidden())continue;
  auto* M=Cast<UStaticMeshComponent>(C);const FString N=M&&M->GetStaticMesh()?M->GetStaticMesh()->GetName():TEXT("");
  const bool Tree=N.StartsWith(TEXT("SM_WLA_"))&&(N.Contains(TEXT("Oak"))||N.Contains(TEXT("Birch")));
  const bool Bush=N.StartsWith(TEXT("SM_WLA_"))&&N.Contains(TEXT("Bush"));
  const bool Small=N.StartsWith(TEXT("SM_WLA_"))&&(N.Contains(TEXT("Grass"))||N.Contains(TEXT("Fern"))||N.Contains(TEXT("Flower"))||N.Contains(TEXT("Herb")));
  AActor* A=C->GetOwner();const bool Person=A->IsA<APokeMonsterPlayerCharacter>()||A->IsA<APokeMonsterNPCVisualActor>()||A->IsA<APokeMonsterNPC>()||A->IsA<APokeMonsterTrainerNPC>()||A->IsA<APokeMonsterVisibleWildCreatureActor>();
  if(!(Tree||Bush||Small||Person))continue;
  S->Originals.Add({C,!!C->CastShadow});C->SetCastShadow(false);
  UE_LOG(LogTemp,Verbose,TEXT("PM_SOFT_COMPONENT %s"),*C->GetPathName());
  if(Tree)
  {
   ++S->Trees;
   const FBox Local=M->GetStaticMesh()->GetBoundingBox();
   auto AddTree=[&](const FTransform& T)
   {
    const FVector Extent=Local.GetExtent()*T.GetScale3D().GetAbs();
    FVector Base=T.GetLocation();const FVector Center=T.TransformPosition(Local.GetCenter());Base.X=Center.X;Base.Y=Center.Y;
    S->Add(C,nullptr,Base,FMath::Max(80.f,Extent.X*.83f),FMath::Max(80.f,Extent.Y*.83f),TreeMaterial);
   };
   if(auto* Inst=Cast<UInstancedStaticMeshComponent>(C)){for(int32 J=0;J<Inst->GetInstanceCount();++J){FTransform T;Inst->GetInstanceTransform(J,T,true);AddTree(T);}}
   else AddTree(C->GetComponentTransform());
  }
  if(Bush)++S->BushComponents;
  if(Small)++S->SmallPlants;
 }
 UE_LOG(LogTemp,Display,TEXT("PM_SOFT_VEGETATION_DONE"));
 // Exactly one blob per visible logical figure. Ignore collision capsules and text labels.
 for(TActorIterator<AActor> I(W);I;++I)
 {
  AActor* A=*I;if(A->IsHidden()||Presented.Contains(A))continue;
  if(!(A->IsA<APokeMonsterPlayerCharacter>()||A->IsA<APokeMonsterNPCVisualActor>()||A->IsA<APokeMonsterNPC>()||A->IsA<APokeMonsterTrainerNPC>()||A->IsA<APokeMonsterVisibleWildCreatureActor>()))continue;
  UPrimitiveComponent* Source=nullptr;TInlineComponentArray<UPrimitiveComponent*> Components(A);
  for(auto* C:Components)if(C->IsA<UMeshComponent>()&&C->IsVisible()&&!C->bHiddenInGame&&C->GetNumMaterials()>0&&(!Source||C->Bounds.BoxExtent.Z>Source->Bounds.BoxExtent.Z))Source=C;
  if(!Source)continue;
  const float R=FMath::Clamp(Source->Bounds.BoxExtent.Z*.30f,19.f,42.f);
  S->Add(Source,A,A->GetActorLocation(),R,R*.72f,Figure);++S->Characters;
 }
 UE_LOG(LogTemp,Display,TEXT("PM_SOFT_SHADOWS trees=%d figures=%d bushes_without_blob=%d small_without_blob=%d decals=%d components=%d"),S->Trees,S->Characters,S->BushComponents,S->SmallPlants,S->Blobs.Num(),S->Originals.Num());
 Active=MoveTemp(S);
 // After movement/physics, before viewport rendering. A CoreTicker-only follow
 // runs after viewport submission and leaves fast characters one frame ahead.
 Active->PostActorTick=FWorldDelegates::OnWorldPostActorTick.AddLambda([](UWorld* TickWorld,ELevelTick,float)
 {
  if(!Active||Active->World.Get()!=TickWorld)return;
  for(auto& B:Active->Blobs)if(B.Mover.IsValid())Active->Place(B);
 });
 Active->Tick=FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([](float)
 {
  if(!Active||!Active->World.IsValid()||Active->World->bIsTearingDown){Stop();return false;}
  return true;
 }));
 return true;
}

// Test receiver only: spawned in the game world, never through editor map APIs.
static TWeakObjectPtr<AStaticMeshActor> SlopeReceiver;
static FAutoConsoleCommand SlopeCommand(TEXT("pm.SoftShadows.Slope"),TEXT("Temporary 8-degree receiver in the GPU test game world. 1 creates, 0 destroys."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1)return;
 if(Args[0]==TEXT("0")){if(auto* A=SlopeReceiver.Get())A->Destroy();SlopeReceiver.Reset();return;}
 if(Args[0]!=TEXT("1")||SlopeReceiver.IsValid())return;
 for(const auto& Context:GEngine->GetWorldContexts())if((Context.WorldType==EWorldType::PIE||Context.WorldType==EWorldType::Game)&&Context.World()&&Context.World()->GetMapName().Contains(TEXT("Dev_TestMap_VisualV2GPUBottleneckV1")))
 {
  auto* W=Context.World();auto* Player=UGameplayStatics::GetPlayerPawn(W,0);if(!Player)return;
  FActorSpawnParameters P;P.ObjectFlags|=RF_Transient;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
  auto* A=W->SpawnActor<AStaticMeshActor>(Player->GetActorLocation()+FVector(450,0,30-Player->GetActorLocation().Z),FRotator(8,0,0),P);if(!A)return;
  A->Tags.Add(TEXT("VAS_RuntimeOnly_Slope"));auto* C=A->GetStaticMeshComponent();C->SetMobility(EComponentMobility::Movable);
  C->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));C->SetMaterial(0,LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass.M_WL_NG_Grass")));
  A->SetActorScale3D(FVector(4,3,.04));C->SetCastShadow(false);C->bAffectDynamicIndirectLighting=false;C->bAffectDistanceFieldLighting=false;C->SetCanEverAffectNavigation(false);C->SetCollisionProfileName(TEXT("BlockAll"));SlopeReceiver=A;return;
 }
}));

static FAutoConsoleCommand Command(TEXT("pm.SoftShadows.Test"),TEXT("Opt-in Development-only: 1 enables scoped blobs in the existing GPU test map; 0 restores all shadows."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1)return;
 if(Args[0]==TEXT("0")){Stop();return;}
 if(Args[0]!=TEXT("1"))return;
 for(const auto& C:GEngine->GetWorldContexts())if(C.WorldType==EWorldType::PIE||C.WorldType==EWorldType::Game){Enable(C.World());return;}
}));
}
#else
namespace PMSoftShadowTest { bool Enable(UWorld*){return false;}void Stop(){} }
#endif
