#include "PokeMonsterNPCMotionV3VisualActor.h"
#include "PokeMonsterNPCMotionV3AnimInstance.h"
#include "Components/SkeletalMeshComponent.h"
APokeMonsterNPCMotionV3VisualActor::APokeMonsterNPCMotionV3VisualActor()
{
 Visual->SetAnimInstanceClass(UPokeMonsterNPCMotionV3AnimInstance::StaticClass());
}
