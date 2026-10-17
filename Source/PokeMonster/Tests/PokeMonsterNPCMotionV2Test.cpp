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
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPMNPCMotionV2Test,"PokeMonster.NPC.MotionV2.IsolationSpeedAndSkeleton",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPMNPCMotionV2Test::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* Source=W->SpawnActor<APokeMonsterNPC>();auto* V=W->SpawnActor<APokeMonsterNPCVisualActor>();V->SourceActor=Source;
 TestFalse(TEXT("Legacy motion remains opt-in"),V->bEnableMotionPresentation);TestFalse(TEXT("No permanent actor tick"),V->IsActorTickEnabled());
 V->bEnableMotionPresentation=true;V->AuthoredWalkSpeed=150.f;V->SampleMotion(1.f/60.f);
 for(int32 I=0;I<8;++I)
 {
  const FVector Direction=FRotator(0,I*45.f,0).Vector();Source->SetActorLocation(Source->GetActorLocation()+Direction*2.5f);
  const FTransform Before=Source->GetActorTransform();V->SampleMotion(1.f/60.f);
  TestTrue(TEXT("All eight directions measure 150 cm/s without diagonal boost"),FMath::IsNearlyEqual(V->PresentationSpeed,150.f,.02f));
  TestTrue(TEXT("Presentation never changes source transform"),Before.Equals(Source->GetActorTransform()));
 }
 const double LastYaw=V->GetActorRotation().Yaw;V->SampleMotion(1.f/60.f);TestEqual(TEXT("Stop speed"),V->PresentationSpeed,0.f);TestEqual(TEXT("Last direction retained at stop"),V->GetActorRotation().Yaw,LastYaw);
 Source->SetActorLocation(Source->GetActorLocation()+FVector(10000,0,0));V->SampleMotion(1.f/60.f);TestEqual(TEXT("Relocation is not walking"),V->PresentationSpeed,0.f);
 auto* Mesh=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/NPCs/RangerMotionV2/Meshes/SK_Ranger_AQV2"));
 if(!TestNotNull(TEXT("V2 mesh"),Mesh))return false;
 for(const TCHAR* Name:{TEXT("Idle"),TEXT("Walk"),TEXT("Talk"),TEXT("TurnLeft"),TEXT("TurnRight")})
 {
  auto* A=LoadObject<UAnimSequence>(nullptr,*FString::Printf(TEXT("/Game/Characters/NPCs/RangerMotionV2/Animations/A_Ranger_%s_AQV2"),Name));
  if(TestNotNull(Name,A)){TestTrue(TEXT("Own compatible skeleton"),A->GetSkeleton()==Mesh->GetSkeleton());TestFalse(TEXT("In-place"),A->bEnableRootMotion);}
 }
 V->Visual->SetSkeletalMeshAsset(Mesh);V->IdleAnimation=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/NPCs/RangerMotionV2/Animations/A_Ranger_Idle_AQV2"));Source->Sprite->SetVisibility(true);V->RefreshPresentation();TestFalse(TEXT("Valid V2 hides sprite"),Source->Sprite->IsVisible());V->bUseVisual=false;V->RefreshPresentation();TestTrue(TEXT("Sprite fallback survives"),Source->Sprite->IsVisible());
 TestEqual(TEXT("No new collision"),V->Visual->GetCollisionEnabled(),ECollisionEnabled::NoCollision);return true;
}
#endif
