#include "PokeMonsterNPCMotionPreviewSource.h"
#include "Components/SceneComponent.h"
#include "Engine/World.h"
APokeMonsterNPCMotionPreviewSource::APokeMonsterNPCMotionPreviewSource()
{
 PrimaryActorTick.bCanEverTick=false;
 SetRootComponent(CreateDefaultSubobject<USceneComponent>(TEXT("PreviewOrigin")));
}
void APokeMonsterNPCMotionPreviewSource::SetPreviewMotion(FVector Location,FVector Velocity)
{
#if !UE_BUILD_SHIPPING
 if(!GetWorld()||!GetWorld()->IsGameWorld()||!GetWorld()->GetMapName().Contains(TEXT("Dev_TestMap_NPCMotionV2")))return;
 SetActorLocation(Location,false,nullptr,ETeleportType::None);
 PreviewVelocity=Velocity.GetClampedToMaxSize(300.f);
#endif
}
