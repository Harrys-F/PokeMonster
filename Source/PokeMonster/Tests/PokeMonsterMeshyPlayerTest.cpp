#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Characters/PokeMonsterMeshyVisualComponent.h"
#include "Animation/AnimSequence.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "../Characters/PokeMonsterMeshyAnimInstance.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "PaperFlipbookComponent.h"
#include "PaperFlipbook.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterMeshyPlayerTest,"PokeMonster.Player.MeshyPresentation",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterMeshyPlayerTest::RunTest(const FString& Parameters)
{
 const auto* Defaults=GetDefault<APokeMonsterPlayerCharacter>();
 const auto* Visual=Defaults->MeshyVisual.Get();
 if (!TestNotNull(TEXT("Separate skeletal presentation exists"),Visual)) return false;
 if (!TestTrue(TEXT("Mesh and both clips loaded; 3D is selected"),Visual->IsMeshyActive())) return false;
 TestEqual(TEXT("Visual never blocks gameplay"),Visual->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
 const auto* Mesh=Visual->GetSkeletalMeshAsset();
 TestTrue(TEXT("Reference mesh is 140 cm high"),FMath::IsNearlyEqual(Mesh->GetBounds().BoxExtent.Z*2,140.f,.2f));
 TestTrue(TEXT("Idle uses imported skeleton"),Visual->IdleAnimation->GetSkeleton()==Mesh->GetSkeleton());
 TestTrue(TEXT("Walk uses imported skeleton"),Visual->WalkAnimation->GetSkeleton()==Mesh->GetSkeleton());
 TestTrue(TEXT("Idle is a complete three-second loop"),FMath::IsNearlyEqual(Visual->IdleAnimation->GetPlayLength(),3.f,.01f));
 TestTrue(TEXT("Walk contains a complete speed-matched alternating cycle"),FMath::IsNearlyEqual(Visual->WalkAnimation->GetPlayLength(),.55f,.01f));
 TestFalse(TEXT("Idle never drives root motion"),Visual->IdleAnimation->bEnableRootMotion);
 TestFalse(TEXT("Walk never drives root motion"),Visual->WalkAnimation->bEnableRootMotion);
 TestEqual(TEXT("Collision remains 96 cm high"),Defaults->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight()*2,96.f);
 TestEqual(TEXT("Gameplay speed remains 210 cm/s"),Defaults->GetCharacterMovement()->MaxWalkSpeed,210.f);
 UWorld* World=UWorld::CreateWorld(EWorldType::Game,false);
 GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
 ON_SCOPE_EXIT { GEngine->DestroyWorldContext(World); World->DestroyWorld(false); };
 auto* Player=World->SpawnActor<APokeMonsterPlayerCharacter>(FVector(0,0,48),FRotator::ZeroRotator);
 // A transient test world has not run BeginPlay, which normally selects the idle flipbook.
 Player->GetCharacterFlipbookComponent()->SetFlipbook(LoadObject<UPaperFlipbook>(nullptr,TEXT("/Game/Characters/Prototype2D/Flipbooks/HobbitPlayer/FB_PlayerIdleDown.FB_PlayerIdleDown")));
 auto* V=Player->MeshyVisual.Get();V->UpdatePresentation();
 TestTrue(TEXT("Soles align with collision ground point"),V->GetRelativeLocation().Equals(FVector(0,0,-48),.001f));
 TestFalse(TEXT("Retained sprite is hidden with skeletal display"),Player->GetCharacterFlipbookComponent()->IsVisible());
 V->SetMeshyEnabled(false);
 TestFalse(TEXT("Fallback hides skeletal display"),V->IsVisible());
 TestTrue(TEXT("Fallback restores retained eight-direction sprite"),Player->GetCharacterFlipbookComponent()->IsVisible());
 V->SetMeshyEnabled(true);
 Player->GetCharacterMovement()->Velocity=FVector(210,0,0);V->UpdatePresentation();
 auto* Animation=Cast<UPokeMonsterMeshyAnimInstance>(V->GetAnimInstance());
 if (TestNotNull(TEXT("Blended animation instance exists"),Animation))
 {
  V->TickAnimation(.05f,false);V->RefreshBoneTransforms();
  TestTrue(TEXT("Idle/Walk blends instead of snapping"),Animation->WalkAlpha>0.f && Animation->WalkAlpha<1.f);
  TestEqual(TEXT("210 cm/s plays authored cycle at one times speed"),Animation->WalkPlayRate,1.f);
  for (int32 I=0;I<8;++I) { V->TickAnimation(.03f,false);V->RefreshBoneTransforms(); }
  TestTrue(TEXT("Walking settles into full locomotion"),Animation->WalkAlpha>.99f);
  V->SetWorldRotation(FRotator(0,90,0));V->TickAnimation(.03f,false);V->RefreshBoneTransforms();
  TestTrue(TEXT("Turning drives accessory springs"),FMath::Abs(Animation->CapeSwing)>.01f && FMath::Abs(Animation->BagSwing)>.01f);
  Player->GetCharacterMovement()->Velocity=FVector::ZeroVector;
  for (int32 I=0;I<120;++I) { V->TickAnimation(1.f/60.f,false);V->RefreshBoneTransforms(); }
  TestTrue(TEXT("Stop blends back to idle"),Animation->WalkAlpha<.01f);
  TestTrue(TEXT("Accessories settle after stop"),FMath::Abs(Animation->CapeSwing)<.05f && FMath::Abs(Animation->BagSwing)<.05f && FMath::Abs(Animation->CapePitch)<.05f);
  // Independently sample the source clip, without the transition/spring layer.
  V->SetAnimationMode(EAnimationMode::AnimationSingleNode);V->PlayAnimation(V->WalkAnimation,true);
  const FVector RootBefore=V->GetSocketLocation(TEXT("root"));
  auto SampleFeet=[&](float Time)
  {
   V->SetPosition(Time,false);V->TickAnimation(0.f,false);V->RefreshBoneTransforms();
   TestTrue(TEXT("Animation remains in place"),V->GetSocketLocation(TEXT("root")).Equals(RootBefore,.1f));
   return FVector2D(V->GetSocketLocation(TEXT("foot_l")).Z,V->GetSocketLocation(TEXT("foot_r")).Z);
  };
  const FVector2D LeftStep=SampleFeet(.55f*.75f);
  const FVector2D RightStep=SampleFeet(.55f*.25f);
  TestTrue(TEXT("Left recovery foot lifts above planted right foot"),LeftStep.X>LeftStep.Y+4.f);
  TestTrue(TEXT("Right recovery foot lifts above planted left foot"),RightStep.Y>RightStep.X+4.f);

 }
 return true;
}
#endif
