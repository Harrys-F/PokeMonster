#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../UI/PokeMonsterEvolutionPresentation.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionPresentationTimeline,"PokeMonster.EvolutionV21.PresentationTimelineAndCutoff",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionPresentationTimeline::RunTest(const FString&)
{
 using namespace PokeMonsterEvolutionPresentation;
 TestEqual(TEXT("Existing data boundary unchanged"),CommitSeconds,5.f);
 float Previous=0;
 for(int I=0;I<=1000;++I)
 {
  const float T=I*.01f;const auto F=Sample(T);
  TestTrue(TEXT("Dissolve is continuous, forward and bounded"),F.Morph>=Previous&&F.Morph>=0&&F.Morph<=1);Previous=F.Morph;
  TestTrue(TEXT("Restrained flash, no opaque white screen"),F.Flash>=0&&F.Flash<=.101f);
  TestEqual(TEXT("Cancel only before data boundary"),F.bCanCancel,T<CommitSeconds);
 }
 TestTrue(TEXT("Both forms overlap in a true dissolve"),Sample(3.3f).Morph>.1f&&Sample(3.3f).Morph<.9f);
 TestTrue(TEXT("Source initially original color"),Sample(0).Glow==0&&Sample(0).Morph==0);
 TestEqual(TEXT("Destination completely takes over before reveal"),Sample(CommitSeconds).Morph,1.f);
 TestEqual(TEXT("White silhouette ends before celebration"),Sample(ColorSeconds).Glow,0.f);
 TestEqual(TEXT("No residual particles over success message"),Sample(CompleteSeconds).Particles,0.f);
 TestTrue(TEXT("Colored celebration has time before success message"),CompleteSeconds-ColorSeconds>=1.8f);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FEvolutionPresentationFraming,"PokeMonster.EvolutionV21.CenteredUnscaledFraming",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FEvolutionPresentationFraming::RunTest(const FString&)
{
 using namespace PokeMonsterEvolutionPresentation;
 // Small biped, tall biped, full wing/tail span and asymmetric tail bounds.
 const TArray<FBox> Boxes={FBox(FVector(-30,-20,0),FVector(30,60,60)),FBox(FVector(-45,-30,0),FVector(45,100,110)),FBox(FVector(-155,-70,0),FVector(155,170,190))};
 for(const auto& B:Boxes)
 {
  const auto F=Fit(B);const auto Basis=FRotationMatrix(F.Rotation);const float T=FMath::Tan(FMath::DegreesToRadians(17.5f));
  const FVector Focus=B.GetCenter()-F.Location;TestTrue(TEXT("Bounds centre projects to exact image centre"),FMath::Abs(FVector::DotProduct(Focus,Basis.GetUnitAxis(EAxis::Y)))<.01f&&FMath::Abs(FVector::DotProduct(Focus,Basis.GetUnitAxis(EAxis::Z)))<.01f);
  float Max=0;
  for(int I=0;I<8;++I)
  {
   const FVector P(I&1?B.Max.X:B.Min.X,I&2?B.Max.Y:B.Min.Y,I&4?B.Max.Z:B.Min.Z);const FVector D=P-F.Location;const float Depth=FVector::DotProduct(D,Basis.GetUnitAxis(EAxis::X));
   const float X=FMath::Abs(FVector::DotProduct(D,Basis.GetUnitAxis(EAxis::Y))/(Depth*T));const float Y=FMath::Abs(FVector::DotProduct(D,Basis.GetUnitAxis(EAxis::Z))/(Depth*T/(16.f/9.f)));
   TestTrue(TEXT("All wings/tail/body corners inside safe image border"),Depth>0&&X<=.841f&&Y<=.841f);Max=FMath::Max(Max,FMath::Max(X,Y));
  }
  TestTrue(TEXT("Creature uses the presentation frame instead of remaining distant"),Max>=.83f);
 }
 const FBox Wing(FVector(-60,-150,0),FVector(150,150,170));const FTransform Transform(FRotator(0,135,0));TArray<FVector> Oriented;FBox WorldBox(ForceInit);
 for(int I=0;I<8;++I){const auto P=Transform.TransformPosition(FVector(I&1?Wing.Max.X:Wing.Min.X,I&2?Wing.Max.Y:Wing.Min.Y,I&4?Wing.Max.Z:Wing.Min.Z));Oriented.Add(P);WorldBox+=P;}
 TestTrue(TEXT("Direct oriented projection avoids artificial retreat for rotated wings"),FitPoints(Oriented).Distance<Fit(WorldBox).Distance*.95f);
 return true;
}
#endif
