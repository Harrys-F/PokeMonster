#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Characters/PokeMonsterMeshyVisualComponent.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Animation/AnimSequence.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterMotionFacingTest,"PokeMonster.MotionV5.PlayerFacingAndPreservedDefaults",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterMotionFacingTest::RunTest(const FString&)
{
 float Velocity=0,Angle=0;
 for(int I=0;I<60;++I)
 {
  const float Before=Angle;Angle=UPokeMonsterMeshyVisualComponent::AdvanceVisualYaw(Angle,180,Velocity,1.f/60.f);
  TestTrue(TEXT("Bounded visual turn per frame"),FMath::Abs(FMath::FindDeltaAngleDegrees(Before,Angle))<=12.001f);
 }
 TestTrue(TEXT("Opposite facing settles exactly"),FMath::Abs(FMath::FindDeltaAngleDegrees(Angle,180))<.01f);
 for(int I=0;I<60;++I)Angle=UPokeMonsterMeshyVisualComponent::AdvanceVisualYaw(Angle,-45,Velocity,1.f/60.f);
 TestTrue(TEXT("Diagonal change settles without oscillation"),FMath::Abs(FMath::FindDeltaAngleDegrees(Angle,-45))<.01f);
 const auto* P=GetDefault<APokeMonsterPlayerCharacter>();
 TestEqual(TEXT("Walk physics unchanged"),P->GetCharacterMovement()->MaxWalkSpeed,210.f);
 TestEqual(TEXT("Authored run reference unchanged"),P->MeshyVisual->AuthoredRunSpeed,315.f);
 TestEqual(TEXT("Visual remains nonblocking"),P->MeshyVisual->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterGroundHoverContractTest,"PokeMonster.MotionV5.GroundHoverContract",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterGroundHoverContractTest::RunTest(const FString&)
{
 auto* Original=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Glurak/PolishV4/DA_Glurak_Presentation.DA_Glurak_Presentation"));
 if(!TestNotNull(TEXT("Retained original V4 profile"),Original)) return false;
 TStrongObjectPtr<UPokeMonsterCreaturePresentationData> D(DuplicateObject<UPokeMonsterCreaturePresentationData>(Original,GetTransientPackage()));
 TestFalse(TEXT("Old profile does not gain autonomous flight"),D->bAllowGroundHover);
 D->bAllowGroundHover=true;TestTrue(TEXT("Missing hover clips rejected"),!D->GetValidationErrors().IsEmpty());
 D->TakeoffClip=D->HoverClip=D->LandClip=D->Clips.FindRef(EPokeMonsterCreatureClip::Idle);
 TestTrue(TEXT("Compatible in-place clips accepted"),D->GetValidationErrors().IsEmpty());
 D->HoverHeightCm=151.f;TestTrue(TEXT("Over-height rejected"),!D->GetValidationErrors().IsEmpty());
 D->HoverHeightCm=49.f;TestTrue(TEXT("Under-height rejected"),!D->GetValidationErrors().IsEmpty());
 D->HoverHeightCm=90.f;D->HoverClip=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/Creatures/Nebulak/PolishV4/A_Nebulak_Idle.A_Nebulak_Idle"));
 TestTrue(TEXT("Wrong anatomy rejected"),!D->GetValidationErrors().IsEmpty());
 TestEqual(TEXT("Battle role count remains seven"),D->Clips.Num(),7);
 return true;
}
#endif
