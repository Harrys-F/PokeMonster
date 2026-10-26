#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Lighting/PokeMonsterDayNight.h"
#include "UObject/StrongObjectPtr.h"
namespace
{
 auto LightingAt(double H,EPokeMonsterNoonSun V=EPokeMonsterNoonSun::B75)
 {return GetDefault<UPokeMonsterDayNightSettings>()->Evaluate(H/24.,V,*GetDefault<UPokeMonsterWorldClockSettings>());}
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FDayNightNoonTest,"PokeMonster.DayNight.B75C85OnlyHeightDiffers",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FDayNightNoonTest::RunTest(const FString&)
{
 const auto B=LightingAt(12),C=LightingAt(12,EPokeMonsterNoonSun::C85);
 TestEqual(TEXT("B elevation over horizon"),B.SunElevation,75.f);TestEqual(TEXT("C elevation over horizon"),C.SunElevation,85.f);
 TestTrue(TEXT("Light points down by exact 75 degrees"),FMath::IsNearlyEqual(B.LightRotation.Pitch,-75.0,.001));TestTrue(TEXT("Light points down by exact 85 degrees"),FMath::IsNearlyEqual(C.LightRotation.Pitch,-85.0,.001));
 TestEqual(TEXT("Identical azimuth"),B.SunAzimuth,C.SunAzimuth);TestEqual(TEXT("Identical intensity"),B.DirectIntensity,C.DirectIntensity);TestEqual(TEXT("Identical fill"),B.FillIntensity,C.FillIntensity);TestEqual(TEXT("Identical temperature"),B.Temperature,C.Temperature);TestTrue(TEXT("Identical sky colors"),B.Zenith.Equals(C.Zenith)&&B.Horizon.Equals(C.Horizon));
 TestTrue(TEXT("Noon is maximum"),LightingAt(11.99).SunElevation<B.SunElevation&&LightingAt(12.01).SunElevation<B.SunElevation);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FDayNightContinuityTest,"PokeMonster.DayNight.ContinuousDayDawnDuskAndMidnight",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FDayNightContinuityTest::RunTest(const FString&)
{
 for(auto Variant:{EPokeMonsterNoonSun::B75,EPokeMonsterNoonSun::C85})
 {
  auto Previous=LightingAt(0,Variant);
  for(int M=1;M<=1440;++M)
  {
   const auto S=LightingAt(M/60.,Variant);TestTrue(TEXT("Finite bounded intensities"),FMath::IsFinite(S.DirectIntensity)&&S.DirectIntensity>=0&&S.DirectIntensity<=7.7&&S.FillIntensity>=0&&S.FillIntensity<=1.81);
   TestTrue(TEXT("No minute-scale rotation jump"),Previous.LightRotation.Quaternion().AngularDistance(S.LightRotation.Quaternion())<.10);
   TestTrue(TEXT("No minute-scale brightness jump"),FMath::Abs(Previous.DirectIntensity-S.DirectIntensity)<.20);
   TestTrue(TEXT("Finite sky and stars"),FMath::IsFinite(S.Zenith.R)&&FMath::IsFinite(S.Zenith.G)&&FMath::IsFinite(S.Zenith.B)&&S.Stars>=0&&S.Stars<=1);Previous=S;
  }
  for(double H:{4.,5.,7.,12.,18.,19.,20.,24.})
  {
   auto A=LightingAt(H-.000001,Variant),B=LightingAt(H+.000001,Variant);
   TestTrue(TEXT("Exact boundary rotation continuity"),A.LightRotation.Quaternion().AngularDistance(B.LightRotation.Quaternion())<.0001);
   TestTrue(TEXT("Exact boundary color continuity"),A.Zenith.Equals(B.Zenith,.0001)&&A.Horizon.Equals(B.Horizon,.0001));TestTrue(TEXT("Exact boundary intensity continuity"),FMath::Abs(A.DirectIntensity-B.DirectIntensity)<.0001);
  }
 }
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FDayNightPhaseTest,"PokeMonster.DayNight.CentralPhasesAndNightContrast",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FDayNightPhaseTest::RunTest(const FString&)
{
 const auto* Clock=GetDefault<UPokeMonsterWorldClockSettings>();TestEqual(TEXT("Existing day duration unchanged"),Clock->RealMinutesPerDay,120.0);
 for(int M=0;M<1440;++M)TestTrue(TEXT("Every phase supplied by central clock configuration"),LightingAt(M/60.).Phase==Clock->PhaseAt(M*60.));
 auto Noon=LightingAt(12),Night=LightingAt(22);TestTrue(TEXT("Night direct far below day"),Night.DirectIntensity<Noon.DirectIntensity*.1f);TestTrue(TEXT("Night fill subdued but nonzero"),Night.FillIntensity>0&&Night.FillIntensity<Noon.FillIntensity*.65f);TestTrue(TEXT("Combined night light stays well below daytime"),Night.DirectIntensity+Night.FillIntensity<(Noon.DirectIntensity+Noon.FillIntensity)*.2f);TestTrue(TEXT("Night stars"),Night.Stars>.99f);TestEqual(TEXT("Day stars hidden"),Noon.Stars,0.f);
 float Previous=LightingAt(4).DirectIntensity+LightingAt(4).FillIntensity;
 for(int M=241;M<=420;++M){const auto V=LightingAt(M/60.);const float Total=V.DirectIntensity+V.FillIntensity;TestTrue(TEXT("Early morning never dims as moon recedes"),Total+.0001f>=Previous);Previous=Total;}
 TestTrue(TEXT("Morning lower than noon"),LightingAt(6).SunElevation>0&&LightingAt(6).SunElevation<LightingAt(9).SunElevation&&LightingAt(9).SunElevation<Noon.SunElevation);TestTrue(TEXT("Evening sun falls"),LightingAt(16).SunElevation>LightingAt(18).SunElevation&&LightingAt(20).SunElevation<0);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FDayNightDeterminismTest,"PokeMonster.DayNight.RestoreSetAndFramerateIndependentSampling",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FDayNightDeterminismTest::RunTest(const FString&)
{
 FPokeMonsterWorldTime T;auto Saved=T;T.Advance(7200);TestEqual(TEXT("Central clock still 120-minute day"),T.Day,2);
 auto Before=LightingAt(Saved.SecondsOfDay/3600.),After=LightingAt(T.SecondsOfDay/3600.);TestTrue(TEXT("Same time next day gives same light"),Before.LightRotation.Equals(After.LightRotation,.0001));
 FPokeMonsterWorldTime Many;for(int I=0;I<300;++I)Many.Advance(1);auto One=Saved;One.Advance(300);TestEqual(TEXT("No lighting timer advances the world clock"),Many.SecondsOfDay,One.SecondsOfDay);
 auto A=LightingAt(Many.SecondsOfDay/3600.),B=LightingAt(One.SecondsOfDay/3600.);TestTrue(TEXT("Frame splitting independent light"),A.LightRotation.Equals(B.LightRotation,.0001));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FDayNightMapTest,"PokeMonster.DayNight.VisualV2ScopeAndConfiguration",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FDayNightMapTest::RunTest(const FString&)
{
 TestTrue(TEXT("Central map"),UPokeMonsterDayNightSubsystem::IsTargetMap(TEXT("/Game/Maps/Dev_TestMap_VisualV2")));TestTrue(TEXT("PIE prefix"),UPokeMonsterDayNightSubsystem::IsTargetMap(TEXT("/Game/Maps/UEDPIE_0_Dev_TestMap_VisualV2")));
 for(const TCHAR* Name:{TEXT("/Game/Maps/Dev_WestlandRegion"),TEXT("/Game/Maps/Dev_BiomeTestMap_V1"),TEXT("/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1")})TestFalse(TEXT("Other maps excluded"),UPokeMonsterDayNightSubsystem::IsTargetMap(Name));
 TestTrue(TEXT("Lighting config valid"),GetDefault<UPokeMonsterDayNightSettings>()->IsValidConfiguration());return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FDayNightRefinementTest,"PokeMonster.DayNight.V11TwilightAndBoundedShadowUpdates",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FDayNightRefinementTest::RunTest(const FString&)
{
 const auto Morning=LightingAt(6),Evening=LightingAt(19),Night=LightingAt(22);
 TestTrue(TEXT("Recognizable direct sunrise"),Morning.DirectIntensity>4.5f&&Morning.Temperature<4300);
 TestTrue(TEXT("Sunset is still visible at 19"),Evening.SunElevation>5&&Evening.DirectIntensity>1.5f&&Evening.Temperature<4000);
 TestTrue(TEXT("Night readability without a bright blue day"),Night.DirectIntensity+Night.FillIntensity>1.6f&&Night.DirectIntensity+Night.FillIntensity<1.86f);
 auto Applied=LightingAt(12).LightRotation;int Updates=0;
 for(int I=1;I<=500;++I)
 {
  const auto Desired=LightingAt(12.+I*.1/300.).LightRotation;
  if(UPokeMonsterDayNightSettings::NeedsRotationUpdate(Applied,Desired,.025f)){Applied=Desired;++Updates;}
  TestTrue(TEXT("Maximum shadow angle error bounded"),Applied.Quaternion().AngularDistance(Desired.Quaternion())<=FMath::DegreesToRadians(.0251));
 }
 TestTrue(TEXT("Normal time invalidates substantially fewer shadow frames"),Updates<180&&Updates>20);
 TestTrue(TEXT("Large clock jumps cannot remain stale"),UPokeMonsterDayNightSettings::NeedsRotationUpdate(Applied,LightingAt(22).LightRotation,.025f));
 return true;
}
#endif
