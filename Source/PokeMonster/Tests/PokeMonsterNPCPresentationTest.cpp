#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterNPCVisualActor.h"
#include "../Characters/PokeMonsterNPCAnimInstance.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequence.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "PaperSpriteComponent.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterNPCPresentationTest,"PokeMonster.NPC.PresentationAndFallback",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterNPCPresentationTest::RunTest(const FString& Parameters)
{
 UWorld* World=UWorld::CreateWorld(EWorldType::Game,false);
 GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
 ON_SCOPE_EXIT { GEngine->DestroyWorldContext(World); World->DestroyWorld(false); };
 auto* NPC=World->SpawnActor<APokeMonsterNPC>();
 NPC->Sprite->SetVisibility(true);
 const FTransform Before=NPC->GetActorTransform();
 auto* V=World->SpawnActor<APokeMonsterNPCVisualActor>(); V->SourceActor=NPC;
 TestEqual(TEXT("New visual never adds gameplay collision"),V->Visual->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
 TestFalse(TEXT("Standing visual has no permanent actor tick"),V->IsActorTickEnabled());
 V->IdleAnimation=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Idle_V1.A_Ranger_Idle_V1"));
 V->ConversationAnimation=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Talk_V1.A_Ranger_Talk_V1"));
 auto* Mesh=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1.SK_Ranger_NPC_V1"));
 if (!TestNotNull(TEXT("Ranger mesh imported"),Mesh) || !TestNotNull(TEXT("Idle available"),V->IdleAnimation.Get()) || !TestNotNull(TEXT("Talk available"),V->ConversationAnimation.Get())) return false;
 TestTrue(TEXT("Idle and talk share their own Ranger skeleton"),Mesh->GetSkeleton()==V->IdleAnimation->GetSkeleton() && Mesh->GetSkeleton()==V->ConversationAnimation->GetSkeleton());
 TestFalse(TEXT("Idle is in place"),V->IdleAnimation->bEnableRootMotion);
 TestFalse(TEXT("Talk is in place"),V->ConversationAnimation->bEnableRootMotion);
 V->Visual->SetSkeletalMesh(Mesh); V->RefreshPresentation();
 TestFalse(TEXT("Original sprite retained but hidden when valid 3D visual is enabled"),NPC->Sprite->IsVisible());
 V->bUseVisual=false; V->RefreshPresentation();
 TestTrue(TEXT("Disabling 3D restores the original sprite"),NPC->Sprite->IsVisible());
 TestFalse(TEXT("Disabled 3D is hidden"),V->Visual->IsVisible());
 TestTrue(TEXT("Presentation does not move or rotate gameplay NPC"),NPC->GetActorTransform().Equals(Before));
 return true;
}
#endif
