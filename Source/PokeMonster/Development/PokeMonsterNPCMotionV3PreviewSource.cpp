#include "PokeMonsterNPCMotionV3PreviewSource.h"
#include "Components/SceneComponent.h"
#include "Engine/World.h"
APokeMonsterNPCMotionV3PreviewSource::APokeMonsterNPCMotionV3PreviewSource()
{
 PrimaryActorTick.bCanEverTick=false;
 SetRootComponent(CreateDefaultSubobject<USceneComponent>(TEXT("PreviewOrigin")));
}
void APokeMonsterNPCMotionV3PreviewSource::SetPreviewMotion(FVector Location,FVector Velocity)
{
#if !UE_BUILD_SHIPPING
 if(!GetWorld()||!GetWorld()->IsGameWorld()||!GetWorld()->GetMapName().Contains(TEXT("Dev_TestMap_NPCMotionV3")))return;
 SetActorLocation(Location,false,nullptr,ETeleportType::None);
 PreviewVelocity=Velocity.GetClampedToMaxSize(300.f);
#endif
}
