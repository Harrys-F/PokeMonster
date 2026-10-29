#pragma once
#include "CoreMinimal.h"

/** Pure screen layout shared by wild and model labels; never drops a name to declutter. */
struct FPokeMonsterNameplateLayout
{
 static FVector2D Place(FVector2D Anchor,FVector2D Size,FVector2D View,const TArray<FBox2D>& Occupied)
 {
  const FVector2D Limit(FMath::Max(0.,View.X-Size.X),FMath::Max(0.,View.Y-Size.Y));
  FVector2D P(FMath::Clamp(Anchor.X-Size.X*.5,0.,Limit.X),FMath::Clamp(Anchor.Y-Size.Y,0.,Limit.Y));
  const FVector2D Initial=P;
  for(int32 I=0;I<=Occupied.Num();++I)
  {
   const FBox2D Box(P,P+Size);bool Overlap=false;
   for(const auto& Other:Occupied)if(Box.Intersect(Other))
   {
    const double Above=Other.Min.Y-Size.Y-3.;
    P.Y=Above>=0?Above:FMath::Clamp(Other.Max.Y+3.,0.,Limit.Y);Overlap=true;break;
   }
   if(!Overlap)return P;
  }
  // Tiny/crowded viewports may not fit every name. Keep all of them readable/on screen.
  return Initial;
 }
};
