#include "PokeMonsterCharacterFillComponent.h"
#include "PokeMonsterMeshyVisualComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/DirectionalLight.h"
#include "Engine/StaticMeshActor.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "Camera/PlayerCameraManager.h"
#include "HAL/IConsoleManager.h"

// Diagnostic overrides are transient; production uses conservative automatic activation.
static TAutoConsoleVariable<int32> CVarPlayerFill(TEXT("pm.PlayerFill.Mode"),1,TEXT("0 off, 1 conservative canopy estimate, 2 diagnostic forced fill"));
static TAutoConsoleVariable<float> CVarPlayerFillLumens(TEXT("pm.PlayerFill.Lumens"),20.f,TEXT("Player-only shadowless fill; no world or material edits"));
UPokeMonsterCharacterFillComponent::UPokeMonsterCharacterFillComponent()
{
 PrimaryComponentTick.bCanEverTick=true;PrimaryComponentTick.TickGroup=TG_PostUpdateWork;
}
void UPokeMonsterCharacterFillComponent::BeginPlay()
{
 Super::BeginPlay();Mesh=GetOwner()->FindComponentByClass<UPokeMonsterMeshyVisualComponent>();
 if(!Mesh)return;
 bOriginallyChannel2=Mesh->LightingChannels.bChannel2;
 Fill=NewObject<UPointLightComponent>(GetOwner(),TEXT("PlayerReadabilityFill"));
 GetOwner()->AddInstanceComponent(Fill);Fill->SetMobility(EComponentMobility::Movable);
 Fill->SetIntensityUnits(ELightUnits::Lumens);Fill->SetIntensity(0);Fill->SetAttenuationRadius(280);
 Fill->SetCastShadows(false);Fill->SetLightingChannels(false,false,true);Fill->SetIndirectLightingIntensity(0);
 Fill->SetAffectGlobalIllumination(false);Fill->SetAffectReflection(false);Fill->RegisterComponent();
 for(TActorIterator<ADirectionalLight> It(GetWorld());It;++It)
 {
  auto* L=Cast<UDirectionalLightComponent>(It->GetLightComponent());
  if(L&&L->CastShadows&&(!Sun.IsValid()||L->Intensity>Sun->Intensity))Sun=L;
 }
 for(TActorIterator<AActor> It(GetWorld());It;++It)
 {
  TInlineComponentArray<UStaticMeshComponent*> Components(*It);
  for(auto* C:Components)if(C->GetStaticMesh()&&C->CastShadow
   &&C->GetStaticMesh()->GetPathName().Contains(TEXT("/Trees/")))Trees.Add(C);
 }
}
float UPokeMonsterCharacterFillComponent::CanopyOcclusion(const FVector& P,const FVector& Direction,const FBox& B)
{
 if(!B.IsValid||P.ContainsNaN()||Direction.ContainsNaN()||Direction.Z<=.1f)return 0;
 const FVector Size=B.GetSize();if(Size.Z<200||Size.X<100||Size.Y<100)return 0;
 const FVector Center(B.GetCenter().X,B.GetCenter().Y,B.Min.Z+Size.Z*.76f);
 const FVector Radius(Size.X*.31f,Size.Y*.31f,Size.Z*.19f);
 const FVector Q=(P-Center)/Radius,D=Direction.GetSafeNormal()/Radius;
 const float T=FMath::Max(0.f,-FVector::DotProduct(Q,D)/D.SizeSquared());
 const float Metric=(Q+D*T).Size();
 // Only the inner core activates fully. Wind/holes/penumbra are not inferred as exact visibility.
 return 1.f-FMath::SmoothStep(.50f,.82f,Metric);
}
void UPokeMonsterCharacterFillComponent::TickComponent(float Delta,ELevelTick Type,FActorComponentTickFunction* Function)
{
 Super::TickComponent(Delta,Type,Function);if(!Fill||!Mesh)return;
 const int32 Mode=CVarPlayerFill.GetValueOnGameThread();
 const bool Exterior=Mesh->LightingChannels.bChannel0&&!Mesh->LightingChannels.bChannel1;
 SampleRemaining-=Delta;
 float Target=EstimatedShade;
 if(Mode<=0||!Exterior||!Mesh->IsVisible()||GetOwner()->IsHidden())Target=0;
 if(Mode>0&&Exterior&&Mesh->IsVisible()&&!GetOwner()->IsHidden()&&SampleRemaining<=0)
 {
  SampleRemaining=.2f;Target=0;
  if(Mode==2)Target=1;
  else if(Sun.IsValid())
  {
   const FVector TowardSun=-Sun->GetDirection();
   const FVector Base=GetOwner()->GetActorLocation()+FVector(0,0,35);
   float Coverage=1;
   for(FVector Offset:{FVector::ZeroVector,FVector(25,0,0),FVector(-25,0,0),FVector(0,25,0),FVector(0,-25,0)})
   {
    float Sample=0;
    for(const auto& Weak:Trees)if(const auto* C=Weak.Get())
     if(C->IsVisible()&&!C->GetOwner()->IsHidden())Sample=FMath::Max(Sample,CanopyOcclusion(Base+Offset,TowardSun,C->Bounds.GetBox()));
    // Solid building/rock blockers have real collision; foliage is deliberately collisionless.
    FHitResult Hit;FCollisionQueryParams Query(SCENE_QUERY_STAT(PlayerReadabilitySun),true,GetOwner());
    if(GetWorld()->LineTraceSingleByChannel(Hit,Base+Offset,Base+Offset+TowardSun*5000,ECC_Visibility,Query))
     if(const auto* Blocker=Cast<UStaticMeshComponent>(Hit.GetComponent()))
      if(Blocker->CastShadow&&Blocker->IsVisible()&&!Blocker->GetOwner()->IsHidden())Sample=1;
    Coverage=FMath::Min(Coverage,Sample);
   }
   Target=FMath::SmoothStep(.05f,.2f,Coverage);
  }
 }
 EstimatedShade=Target;
 FillLumens=FMath::FInterpTo(FillLumens,Target*FMath::Clamp(CVarPlayerFillLumens.GetValueOnGameThread(),0.f,60.f),Delta,3.f);
 if(!Exterior||Mode==0)FillLumens=0;
 // Interior machinery owns channel1; never replace its lighting contract.
 const auto Channels=Mesh->LightingChannels;
 Mesh->SetLightingChannels(Channels.bChannel0,Channels.bChannel1,bOriginallyChannel2||(Exterior&&Mode>0));
 FVector TowardCamera(-1,-1,0);
 if(auto* PC=GetWorld()->GetFirstPlayerController())if(PC->PlayerCameraManager)
  TowardCamera=(PC->PlayerCameraManager->GetCameraLocation()-GetOwner()->GetActorLocation()).GetSafeNormal2D();
 Fill->SetWorldLocation(GetOwner()->GetActorLocation()+TowardCamera*110+FVector(0,0,95));Fill->SetIntensity(FillLumens);
}
void UPokeMonsterCharacterFillComponent::EndPlay(const EEndPlayReason::Type Reason)
{
 if(Mesh){const auto C=Mesh->LightingChannels;Mesh->SetLightingChannels(C.bChannel0,C.bChannel1,bOriginallyChannel2);}
 if(Fill)Fill->DestroyComponent();Super::EndPlay(Reason);
}
