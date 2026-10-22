#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "UObject/StrongObjectPtr.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Components/SkeletalMeshComponent.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FAnimationV6FloatIsolation,"PokeMonster.AnimationV6.OverworldFloatDoesNotAffectBattleVisual",
 EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FAnimationV6FloatIsolation::RunTest(const FString&)
{
 auto* Original=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Nebulak/MotionV5/DA_Nebulak_Presentation.DA_Nebulak_Presentation"));
 if(!TestNotNull(TEXT("Previous Nebulak profile retained"),Original))return false;
 TStrongObjectPtr<UPokeMonsterCreaturePresentationData> P(DuplicateObject<UPokeMonsterCreaturePresentationData>(Original,GetTransientPackage()));
 P->OverworldFloatAmplitudeCm=6.f;
 TestTrue(TEXT("Floating rig accepts a restrained float"),P->GetValidationErrors().IsEmpty());
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);
 GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{W->DestroyWorld(false);GEngine->DestroyWorldContext(W);};
 auto* WorldVisual=W->SpawnActor<APokeMonsterCreatureVisualActor>();
 auto* BattleVisual=W->SpawnActor<APokeMonsterCreatureVisualActor>();
 if(!WorldVisual||!BattleVisual)return false;
 TestTrue(TEXT("Same valid visual profile"),WorldVisual->SetPresentation(P.Get())&&BattleVisual->SetPresentation(P.Get()));
 auto* Movement=NewObject<UPokeMonsterCreatureRoamingComponent>(WorldVisual);
 WorldVisual->SetGroundHoverContext(Movement);
 const FVector Before=WorldVisual->GetActorLocation();
 WorldVisual->Tick(1.f/60.f);BattleVisual->Tick(1.f/60.f);
 TestTrue(TEXT("Overworld mesh visibly floats"),WorldVisual->Mesh->GetRelativeLocation().Z>2.f);
 TestEqual(TEXT("Battle without roaming context stays unchanged"),BattleVisual->Mesh->GetRelativeLocation(),FVector::ZeroVector);
 TestEqual(TEXT("Logical ground position unchanged"),WorldVisual->GetActorLocation(),Before);
 TestEqual(TEXT("Visual collision remains disabled"),WorldVisual->Mesh->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
 TestTrue(TEXT("Swapping to preserved profile succeeds"),WorldVisual->SetPresentation(Original));
 TestEqual(TEXT("No residual float after model exchange"),WorldVisual->Mesh->GetRelativeLocation(),FVector::ZeroVector);
 TestTrue(TEXT("No residual tilt after model exchange"),WorldVisual->Mesh->GetRelativeRotation().IsNearlyZero());
 P->OverworldFloatAmplitudeCm=11.f;TestFalse(TEXT("Excessive float rejected"),P->GetValidationErrors().IsEmpty());
 P->OverworldFloatAmplitudeCm=6.f;P->RigFamily=EPokeMonsterCreatureRigFamily::Biped;
 TestFalse(TEXT("Land animal cannot accidentally gain floating motion"),P->GetValidationErrors().IsEmpty());
 return true;
}
#endif
