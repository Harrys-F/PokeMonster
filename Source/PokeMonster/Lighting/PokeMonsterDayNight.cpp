#include "PokeMonsterDayNight.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "Engine/DirectionalLight.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "EngineUtils.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "UObject/ConstructorHelpers.h"
#include "TimerManager.h"

namespace
{
 float Smooth(double A,double B,double X){return FMath::SmoothStep(float(A),float(B),float(X));}
}
bool UPokeMonsterDayNightSettings::IsValidConfiguration() const
{
 return FMath::IsFinite(NoonAzimuth)&&FMath::IsFinite(UpdateSeconds)&&UpdateSeconds>=.05f&&UpdateSeconds<=1
  &&FMath::IsFinite(DayDirectIntensity)&&DayDirectIntensity>0&&FMath::IsFinite(DayFillIntensity)&&DayFillIntensity>=0
  &&FMath::IsFinite(MoonIntensity)&&MoonIntensity>=0&&MoonIntensity<DayDirectIntensity
  &&FMath::IsFinite(RotationThresholdDegrees)&&RotationThresholdDegrees>=0&&RotationThresholdDegrees<=.05f
  &&FMath::IsFinite(NightFillIntensity)&&NightFillIntensity>=0&&NightFillIntensity<DayFillIntensity;
}
FPokeMonsterDayNightSample UPokeMonsterDayNightSettings::Evaluate(double Fraction,EPokeMonsterNoonSun Variant,const UPokeMonsterWorldClockSettings& C) const
{
 FPokeMonsterDayNightSample S;
 const double H=(Fraction-FMath::FloorToDouble(Fraction))*24.0;
 const double Early=C.PhaseStartMinutes[0]/60.0,Dawn=C.PhaseStartMinutes[1]/60.0,Day=C.PhaseStartMinutes[2]/60.0,Dusk=C.PhaseStartMinutes[3]/60.0,Night=C.PhaseStartMinutes[4]/60.0;
 const double Sunset=FMath::Lerp(Dusk,Night,.75);
 S.Phase=C.PhaseAt(H*3600);
 // Artistic rise/set, apex exactly 12:00. Below-horizon parts never illuminate the world.
 const double HalfSpan=H<=12?12-Dawn:Sunset-12;
 S.SunElevation=MaximumElevation(Variant)*FMath::Cos((H-12)*UE_PI/(2.0*FMath::Max(HalfSpan,1.0)));
 S.SunAzimuth=NoonAzimuth+float((H-12)*15.0);
 const float SunStrength=Smooth(Dawn,Day-.35,H)*(1-Smooth(Dusk,Sunset,H));
 const float MoonStrength=H<12?1-Smooth(Early,Day-1,H):Smooth(Dusk,Night,H);
 float Ambient=H<12?FMath::Lerp(.11f,.19f,Smooth(Early,Dawn,H)):FMath::Lerp(1.f,.11f,Smooth(Dusk,Night,H));
 if(H>=Dawn&&H<12)Ambient=FMath::Lerp(.19f,1.f,Smooth(Dawn,Day,H));
 S.DirectIntensity=DayDirectIntensity*SunStrength+MoonIntensity*MoonStrength;
 // Blend the reused caster over a fixed time interval, not by rapidly changing light-energy ratios.
 const float MoonBlend=H<12?1-Smooth(Early,Day-1,H):Smooth((Dusk+Night)*.5,Night,H);
 S.LightRotation=FQuat::Slerp(FRotator(-S.SunElevation,S.SunAzimuth,0).Quaternion(),FRotator(-50,NoonAzimuth+110,0).Quaternion(),MoonBlend).Rotator();
 S.FillIntensity=FMath::Lerp(NightFillIntensity,DayFillIntensity,FMath::Clamp((Ambient-.11f)/.89f,0.f,1.f));
 // Receding moon must not darken the early morning before sunlight takes over.
 if(H>=Early&&H<Day)S.FillIntensity+=MoonIntensity*(1-SunStrength)*(1-MoonStrength);
 const float DayTemperature=FMath::Lerp(2900.f,5700.f,Smooth(6,35,S.SunElevation));
 S.Temperature=FMath::Lerp(DayTemperature,8500.f,MoonBlend);
 const float DaySky=Smooth(Dawn,Day-.35,H)*(1-Smooth(Dusk,Night,H));
 const float Twilight=Smooth(Early,Dawn,H)*(1-Smooth(Dawn,Day,H))+Smooth(Dusk,Dusk+.6,H)*(1-Smooth(Dusk+.6,Night,H));
 S.Zenith=FMath::Lerp(FLinearColor(.006f,.012f,.029f),FLinearColor(.08f,.25f,.48f),DaySky);
 S.Horizon=FMath::Lerp(FLinearColor(.018f,.025f,.045f),FLinearColor(.48f,.65f,.72f),DaySky);
 S.Horizon=FMath::Lerp(S.Horizon,FLinearColor(.75f,.32f,.11f),FMath::Clamp(Twilight*.75f,0.f,1.f));
 S.Stars=1-Smooth(Early,Day,H);if(H>=12)S.Stars=Smooth(Dusk,Night,H);
 return S;
}
UPokeMonsterDayNightSubsystem::UPokeMonsterDayNightSubsystem()
{
 static ConstructorHelpers::FObjectFinder<UStaticMesh> Mesh(TEXT("/Engine/EngineSky/SM_SkySphere.SM_SkySphere"));SkyMeshAsset=Mesh.Object;
 static ConstructorHelpers::FObjectFinder<UMaterialInterface> Material(TEXT("/Engine/EngineSky/M_Sky_Panning_Clouds2.M_Sky_Panning_Clouds2"));SkyMaterialAsset=Material.Object;
}
bool UPokeMonsterDayNightSubsystem::DoesSupportWorldType(EWorldType::Type Type) const{return Type==EWorldType::Game||Type==EWorldType::PIE;}
bool UPokeMonsterDayNightSubsystem::IsTargetMap(const FString& Name){return UWorld::RemovePIEPrefix(Name)==TEXT("/Game/Maps/Dev_TestMap_VisualV2");}
void UPokeMonsterDayNightSubsystem::OnWorldBeginPlay(UWorld& World)
{
 Super::OnWorldBeginPlay(World);if(!IsTargetMap(World.GetPackage()->GetName()))return;
 const auto* Config=GetDefault<UPokeMonsterDayNightSettings>();
 if(!Config->IsValidConfiguration()){UE_LOG(LogTemp,Warning,TEXT("DayNight: invalid lighting configuration; existing lights preserved."));return;}
 for(TActorIterator<ADirectionalLight> I(&World);I;++I)
 {
  if(I->GetFName()==Config->SunActor)Sun=Cast<UDirectionalLightComponent>(I->GetLightComponent());
  if(I->GetFName()==Config->FillActor)Fill=Cast<UDirectionalLightComponent>(I->GetLightComponent());
 }
 Clock=World.GetGameInstance()?World.GetGameInstance()->GetSubsystem<UPokeMonsterWorldClock>():nullptr;
 if(!Sun||!Fill||!Clock){UE_LOG(LogTemp,Warning,TEXT("DayNight: existing sun/fill/clock missing; no replacement lights created."));return;}
 OriginalSunRotation=Sun->GetOwner()->GetActorRotation();OriginalSunIntensity=Sun->Intensity;OriginalSunTemperature=Sun->Temperature;OriginalSunTemperatureEnabled=Sun->bUseTemperature;OriginalFillIntensity=Fill->Intensity;
 bBound=true;NoonVariant=Config->NoonVariant;
 // No added light, atmosphere volume, capture, fog or postprocess. Reuse Engine sky geometry/material.
 if(SkyMeshAsset&&SkyMaterialAsset)
 {
  FActorSpawnParameters Params;Params.ObjectFlags|=RF_Transient;Params.Name=TEXT("VisualV2_DayNightSky");
  Sky=World.SpawnActor<AStaticMeshActor>(FVector::ZeroVector,FRotator::ZeroRotator,Params);
  auto* M=Sky->GetStaticMeshComponent();M->SetMobility(EComponentMobility::Movable);M->SetStaticMesh(SkyMeshAsset);M->SetCollisionEnabled(ECollisionEnabled::NoCollision);M->SetCastShadow(false);
  M->bVisibleInReflectionCaptures=false;M->bVisibleInRealTimeSkyCaptures=false;M->bAffectDynamicIndirectLighting=false;M->bAffectDistanceFieldLighting=false;
  Sky->SetActorScale3D(FVector(400));Sky->SetActorEnableCollision(false);Sky->SetActorTickEnabled(false);
  SkyMID=M->CreateDynamicMaterialInstance(0,SkyMaterialAsset);
  SkyMID->SetScalarParameterValue(TEXT("Cloud speed"),0);SkyMID->SetScalarParameterValue(TEXT("Cloud opacity"),.18f);SkyMID->SetScalarParameterValue(TEXT("Horizon Falloff"),3);
  SkyMID->SetVectorParameterValue(TEXT("Overall Color"),FLinearColor::White);M->MarkRenderStateDirty();
 }
 Clock->OnTimeSet.AddUniqueDynamic(this,&UPokeMonsterDayNightSubsystem::HandleTimeSet);
 SetCycleEnabled(true);
 World.GetTimerManager().SetTimer(UpdateTimer,this,&UPokeMonsterDayNightSubsystem::UpdateFromClock,Config->UpdateSeconds,true);
}
void UPokeMonsterDayNightSubsystem::SetCycleEnabled(bool Enabled)
{
 if(!bBound||bEnabled==Enabled)return;bEnabled=Enabled;LastSeconds=-1;
 if(Sky)Sky->SetActorHiddenInGame(!Enabled);
 if(Enabled)RefreshLighting();else RestoreLights();
}
void UPokeMonsterDayNightSubsystem::SetNoonVariant(EPokeMonsterNoonSun Variant){if(Variant!=EPokeMonsterNoonSun::B75&&Variant!=EPokeMonsterNoonSun::C85)return;NoonVariant=Variant;LastSeconds=-1;if(bEnabled)RefreshLighting();}
void UPokeMonsterDayNightSubsystem::HandleTimeSet(FPokeMonsterWorldTime){if(bEnabled)RefreshLighting();}
bool UPokeMonsterDayNightSettings::NeedsRotationUpdate(const FRotator& Current,const FRotator& Desired,float Degrees)
{return Degrees<=0 || Current.Quaternion().AngularDistance(Desired.Quaternion())>=FMath::DegreesToRadians(double(Degrees));}
void UPokeMonsterDayNightSubsystem::UpdateFromClock(){if(bEnabled&&Clock&&Clock->GetTime().SecondsOfDay!=LastSeconds)ApplyLighting(false);}
void UPokeMonsterDayNightSubsystem::RefreshLighting(){ApplyLighting(true);}
void UPokeMonsterDayNightSubsystem::ApplyLighting(bool ForceRotation)
{
 if(!bBound||!bEnabled||!Clock)return;
 const auto* C=GetDefault<UPokeMonsterWorldClockSettings>();if(!C->IsValidConfiguration())return;
 const auto* Config=GetDefault<UPokeMonsterDayNightSettings>();LastSeconds=Clock->GetTime().SecondsOfDay;
 LastSample=Config->Evaluate(Clock->GetDayFraction(),NoonVariant,*C);
 ++LightingEvaluations;
 if(ForceRotation||UPokeMonsterDayNightSettings::NeedsRotationUpdate(Sun->GetOwner()->GetActorRotation(),LastSample.LightRotation,Config->RotationThresholdDegrees))
 {Sun->GetOwner()->SetActorRotation(LastSample.LightRotation);++RotationApplications;}
 Sun->SetIntensity(LastSample.DirectIntensity);Sun->SetUseTemperature(true);Sun->SetTemperature(LastSample.Temperature);Fill->SetIntensity(LastSample.FillIntensity);
 if(SkyMID)
 {
  // CameraVectorWS points from the sky pixel toward the camera; the disk therefore uses the downward light ray.
  const FVector SkyLightDirection=FRotator(-LastSample.SunElevation,LastSample.SunAzimuth,0).Vector();
  SkyMID->SetVectorParameterValue(TEXT("Light direction"),FLinearColor(SkyLightDirection));// Engine material uses this misleadingly named parameter only as a multiplier of stars.
  SkyMID->SetScalarParameterValue(TEXT("Sun height"),1.f);
  SkyMID->SetScalarParameterValue(TEXT("Sun brightness"),25.f*Smooth(-2,3,LastSample.SunElevation));SkyMID->SetVectorParameterValue(TEXT("Sun color"),FLinearColor(1,.8f,.5f));
  SkyMID->SetVectorParameterValue(TEXT("Zenith Color"),LastSample.Zenith);SkyMID->SetVectorParameterValue(TEXT("Horizon color"),LastSample.Horizon);SkyMID->SetVectorParameterValue(TEXT("Cloud color"),FMath::Lerp(LastSample.Zenith,LastSample.Horizon,.4f));SkyMID->SetScalarParameterValue(TEXT("Stars brightness"),LastSample.Stars);
 }
}
void UPokeMonsterDayNightSubsystem::RestoreLights()
{
 if(!bBound)return; // Missing prerequisites never captured originals or changed these lights.
 if(Sun){Sun->GetOwner()->SetActorRotation(OriginalSunRotation);Sun->SetIntensity(OriginalSunIntensity);Sun->SetUseTemperature(OriginalSunTemperatureEnabled);Sun->SetTemperature(OriginalSunTemperature);}
 if(Fill)Fill->SetIntensity(OriginalFillIntensity);
}
void UPokeMonsterDayNightSubsystem::Deinitialize()
{
 if(GetWorld())GetWorld()->GetTimerManager().ClearTimer(UpdateTimer);
 if(Clock)Clock->OnTimeSet.RemoveDynamic(this,&UPokeMonsterDayNightSubsystem::HandleTimeSet);
 RestoreLights();if(Sky)Sky->Destroy();SkyMID=nullptr;Sky=nullptr;Sun=nullptr;Fill=nullptr;Clock=nullptr;bBound=false;Super::Deinitialize();
}
