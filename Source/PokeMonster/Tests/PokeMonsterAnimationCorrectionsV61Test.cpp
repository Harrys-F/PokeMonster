#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Characters/PokeMonsterFootContact.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Characters/PokeMonsterMeshyVisualComponent.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimSequence.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPMFootPlantV61Test,"PokeMonster.AnimationV61.BoundedFootContacts",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPMFootPlantV61Test::RunTest(const FString&)
{
 FPokeMonsterFootContact C;
 C.Update(FVector(0,0,8.7),FQuat::Identity,true,true,1.f/60.f);
 for (int32 I=1;I<=6;++I) C.Update(FVector(I,0,8.7),FQuat::Identity,true,true,1.f/60.f);
 TestTrue(TEXT("Stance fixes the original world contact despite root motion"),C.Target(FVector(6,0,8.7)).Equals(FVector(0,0,8.7),.001));
 C.Update(FVector(7,0,8.7),FQuat(FVector::UpVector,FMath::DegreesToRadians(80.)),true,true,1.f/60.f);
 TestFalse(TEXT("Tight pivot releases before twisting knee"),C.bLocked);
 for (int I=0;I<10;++I) C.Update(FVector(8,0,8.7),FQuat::Identity,false,true,1.f/60.f);
 TestEqual(TEXT("Recovery has no planted correction"),C.Weight,0.f);
 C.Update(FVector(12,3,8.7),FQuat::Identity,true,true,1.f/60.f);
 TestTrue(TEXT("Next step plants at its own new location"),C.Anchor.Equals(FVector(12,3,8.7)));
 C.Update(FVector(200,0,0),FQuat::Identity,true,true,.2f);
 TestEqual(TEXT("Long recording hitch cannot leave a stale foot anchor"),C.Weight,0.f);
 C.Update(FVector::ZeroVector,FQuat::Identity,true,false,1.f/60.f);
 TestFalse(TEXT("Airborne/missing ground cannot plant"),C.bLocked);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPMV61AssetsTest,"PokeMonster.AnimationV61.PreservedRigAndClips",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPMV61AssetsTest::RunTest(const FString&)
{
 auto* Original=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2"));
 auto* Mesh=GetDefault<APokeMonsterPlayerCharacter>()->MeshyVisual->GetSkeletalMeshAsset();
 if (!TestNotNull(TEXT("Original player preserved"),Original)||!TestNotNull(TEXT("Player mesh"),Mesh)) return false;
 TestTrue(TEXT("Player keeps exact V2 skeleton"),Mesh->GetSkeleton()==Original->GetSkeleton());
 TestTrue(TEXT("Player retains 140 cm size"),FMath::IsNearlyEqual(Mesh->GetBounds().BoxExtent.Z*2,140.f,.2f));
 TestEqual(TEXT("Player material count"),Mesh->GetMaterials().Num(),Original->GetMaterials().Num());
 for (int I=0;I<FMath::Min(Mesh->GetMaterials().Num(),Original->GetMaterials().Num());++I)
  TestTrue(TEXT("Player original appearance material reused"),Mesh->GetMaterials()[I].MaterialInterface==Original->GetMaterials()[I].MaterialInterface);
 auto* Before=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Glurak/AnimationV6/DA_Glurak_Presentation_V6"));
 auto* After=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Glurak/AnimationV61/DA_Glurak_Presentation_V61"));
 if (!TestNotNull(TEXT("Glurak V6 retained"),Before)||!TestNotNull(TEXT("Glurak V6.1 candidate"),After)) return false;
 TestTrue(TEXT("Exact original skeleton, no animation retarget"),Before->Mesh->GetSkeleton()==After->Mesh->GetSkeleton());
 TestTrue(TEXT("Candidate validates"),After->GetValidationErrors().IsEmpty());
 for (auto& Pair:Before->Clips) TestTrue(TEXT("Every V6 battle/ground clip remains identical"),After->Clips.FindRef(Pair.Key)==Pair.Value);
 TestTrue(TEXT("Takeoff/hover/landing identical"),Before->TakeoffClip==After->TakeoffClip&&Before->HoverClip==After->HoverClip&&Before->LandClip==After->LandClip);
 TestEqual(TEXT("Glurak keeps original reference size"),After->ReferenceSizeCm,Before->ReferenceSizeCm);
 return true;
}
#endif
