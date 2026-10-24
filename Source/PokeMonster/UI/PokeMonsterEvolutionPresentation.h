#pragma once
#include "CoreMinimal.h"

/** Presentation timing only. The existing encounter service owns every data transaction. */
namespace PokeMonsterEvolutionPresentation
{
 inline constexpr float CommitSeconds=5.f; // Preserve the existing V2 cancellation/data boundary.
 inline constexpr float ColorSeconds=5.85f;
 inline constexpr float CompleteSeconds=7.8f;
 inline float Ease(float A,float B,float T)
 {
  const float X=FMath::Clamp((T-A)/(B-A),0.f,1.f);
  return X*X*(3.f-2.f*X);
 }
 struct FFrame
 {
  float Morph=0,Glow=0,Flash=0,Particles=0;
  bool bCanCancel=true;
 };
 inline FFrame Sample(float Time)
 {
  const float T=FMath::Max(0.f,Time);
  FFrame F;
  F.Morph=Ease(2.35f,4.45f,T);
  const float Charge=Ease(0.f,1.45f,T);
  const float Reveal=1.f-Ease(CommitSeconds,ColorSeconds,T);
  // Slow breathing and one restrained crest; no rapid full-screen strobe.
  F.Glow=Charge*Reveal*(9.f+1.4f*FMath::Sin(T*4.f)+3.f*FMath::Exp(-FMath::Square((T-3.7f)/.42f)));
  F.Flash=.10f*Charge*Reveal*FMath::Exp(-FMath::Square((T-3.7f)/.48f));
  F.Particles=Charge*(1.f-Ease(5.2f,6.6f,T));
  F.bCanCancel=T<CommitSeconds;
  return F;
 }
 struct FFraming { FVector Location;FRotator Rotation;float Distance=0; };
 /** Fit complete conservative bounds, including wings/tail, with no scale mutation. */
 inline FFraming FitPoints(TConstArrayView<FVector> Points)
 {
  FFraming F;F.Rotation=FRotator(-16.f,-45.f,0.f);
  const FVector Forward=F.Rotation.Vector(),Right=FRotationMatrix(F.Rotation).GetUnitAxis(EAxis::Y),Up=FRotationMatrix(F.Rotation).GetUnitAxis(EAxis::Z);
  FBox Bounds(ForceInit);for(const auto& P:Points)Bounds+=P;
  const FVector Focus=Bounds.GetCenter();const float Tan=FMath::Tan(FMath::DegreesToRadians(35.f*.5f));
  F.Distance=50.f;
  for(const FVector& P:Points)
  {
   const FVector D=P-Focus;const float Depth=FVector::DotProduct(D,Forward);
   F.Distance=FMath::Max(F.Distance,FMath::Abs(FVector::DotProduct(D,Right))/(Tan*.84f)-Depth);
   F.Distance=FMath::Max(F.Distance,FMath::Abs(FVector::DotProduct(D,Up))/(Tan/(16.f/9.f)*.84f)-Depth);
  }
  F.Location=Focus-Forward*F.Distance;
  return F;
 }
 inline FFraming Fit(const FBox& Bounds)
 {
  TArray<FVector> Points;
  for(int I=0;I<8;++I)Points.Add(FVector(I&1?Bounds.Max.X:Bounds.Min.X,I&2?Bounds.Max.Y:Bounds.Min.Y,I&4?Bounds.Max.Z:Bounds.Min.Z));
  return FitPoints(Points);
 }
}
