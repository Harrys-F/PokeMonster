#include "PokeMonsterClassicBattleScene.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Components/StaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Engine/World.h"
#include "Engine/SkeletalMesh.h"
#include "UObject/ConstructorHelpers.h"

APokeMonsterClassicBattleScene::APokeMonsterClassicBattleScene()
{
 PrimaryActorTick.bCanEverTick=false;
 auto* Root=CreateDefaultSubobject<USceneComponent>(TEXT("BattleStage"));SetRootComponent(Root);
 Floor=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PresentationFloor"));Floor->SetupAttachment(Root);
 static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));Floor->SetStaticMesh(Cube.Object);
 Floor->SetCollisionEnabled(ECollisionEnabled::NoCollision);Floor->SetCastShadow(false);Floor->SetCanEverAffectNavigation(false);
 Floor->bAffectDynamicIndirectLighting=false;Floor->bAffectDistanceFieldLighting=false;Floor->SetVisibleInSceneCaptureOnly(true);
 Capture=CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("ClassicBattleCapture"));Capture->SetupAttachment(Root);
 Capture->PrimitiveRenderMode=ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList;
 Capture->CaptureSource=ESceneCaptureSource::SCS_FinalColorLDR;Capture->bCaptureEveryFrame=true;Capture->bAlwaysPersistRenderingState=true;
 PresentationFill=CreateDefaultSubobject<UPointLightComponent>(TEXT("CaptureOnlyFigureFill"));PresentationFill->SetupAttachment(Root);PresentationFill->SetCastShadows(false);PresentationFill->SetLightingChannels(false,false,true);PresentationFill->SetIndirectLightingIntensity(0.f);PresentationFill->SetVolumetricScatteringIntensity(0.f);PresentationFill->SetIntensityUnits(ELightUnits::Candelas);
 Capture->FOVAngle=35.f;Capture->PostProcessBlendWeight=0.f;
}
void APokeMonsterClassicBattleScene::Configure(const UPokeMonsterCreatureSpeciesData* A,const UPokeMonsterCreatureSpeciesData* B,AActor* GroundReference)
{
 if(IsValid(PlayerVisual))PlayerVisual->Destroy();PlayerVisual=nullptr;if(IsValid(OpponentVisual))OpponentVisual->Destroy();OpponentVisual=nullptr;
 if(!Target){Target=NewObject<UTextureRenderTarget2D>(this,NAME_None,RF_Transient);Target->RenderTargetFormat=RTF_RGBA8;Target->ClearColor=FLinearColor(.18f,.24f,.17f);Target->InitAutoFormat(2560,1040);Capture->TextureTarget=Target;}
 float Size=60.f;
 for(auto* Species:{A,B})if(Species)if(auto* Data=Species->GetVisuals().Presentation.LoadSynchronous())if(Data->Mesh)Size=FMath::Max(Size,Data->Mesh->GetBounds().BoxExtent.GetMax()*2.f);
 const float Fit=FMath::Max(1.f,Size/110.f);
 const FVector Forward=FRotator(0,-45,0).Vector(),Right=FRotationMatrix(FRotator(0,-45,0)).GetUnitAxis(EAxis::Y);
 const FVector Origin=GetActorLocation();
 Floor->SetRelativeLocation(FVector(0,0,-1));Floor->SetRelativeScale3D(FVector(80*Fit,80*Fit,.02f));
 if(GroundReference){FHitResult Hit;FCollisionQueryParams Q(SCENE_QUERY_STAT(ClassicFloorMaterial),true);Q.AddIgnoredActor(GroundReference);const FVector P=GroundReference->GetActorLocation();if(GetWorld()->LineTraceSingleByChannel(Hit,P+FVector(0,0,50),P-FVector(0,0,200),ECC_Visibility,Q))if(Hit.Component.IsValid())if(auto* M=Hit.Component->GetMaterial(0))Floor->SetMaterial(0,M);}
 Capture->SetRelativeLocation((-Forward*700+FVector(0,0,220))*Fit);
 Capture->SetWorldRotation((Origin+FVector(0,0,40*Fit)-Capture->GetComponentLocation()).Rotation());
 PresentationFill->SetRelativeLocation((-Forward*350+FVector(0,0,200))*Fit);PresentationFill->SetAttenuationRadius(1100*Fit);PresentationFill->SetIntensity(50*Fit*Fit);
 Capture->ShowOnlyActors.Reset();Capture->ShowOnlyActors.Add(this);
 auto Spawn=[&](const UPokeMonsterCreatureSpeciesData* Species,bool bPlayer)->APokeMonsterCreatureVisualActor*
 {
  if(!Species)return nullptr;auto* Data=Species->GetVisuals().Presentation.LoadSynchronous();if(!Data||!Data->Mesh)return nullptr;
  const FVector Offset=(bPlayer?(-Forward*70-Right*95):(Forward*80+Right*95))*Fit;
  auto* V=GetWorld()->SpawnActor<APokeMonsterCreatureVisualActor>(Origin+Offset-FVector(0,0,Data->GroundOffsetCm),(bPlayer?(Forward*150+Right*115):(-Forward*150-Right*115)).Rotation());
  if(!V)return nullptr;if(!V->SetSpecies(Species)){V->Destroy();return nullptr;}
  V->SetOwner(this);V->Mesh->VisibilityBasedAnimTickOption=EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
  TInlineComponentArray<UPrimitiveComponent*> Primitives(V);for(auto* P:Primitives){P->SetVisibleInSceneCaptureOnly(true);P->SetCastShadow(false);P->SetLightingChannels(true,false,true);P->bAffectDynamicIndirectLighting=false;P->bAffectDistanceFieldLighting=false;}
  Capture->ShowOnlyActors.Add(V);return V;
 };
 PlayerVisual=Spawn(A,true);OpponentVisual=Spawn(B,false);
 Capture->CaptureScene();
}
FVector2D APokeMonsterClassicBattleScene::ScreenAnchor(bool bPlayer) const
{
 const auto* V=bPlayer?PlayerVisual.Get():OpponentVisual.Get();if(!V)return bPlayer?FVector2D(350,350):FVector2D(890,235);
 const FVector D=V->GetActorLocation()+FVector(0,0,V->Mesh->Bounds.BoxExtent.Z)-Capture->GetComponentLocation();
 const float Depth=FMath::Max(1.f,FVector::DotProduct(D,Capture->GetForwardVector())),Tan=FMath::Tan(FMath::DegreesToRadians(Capture->FOVAngle*.5f));
 return FVector2D((.5f+.5f*FVector::DotProduct(D,Capture->GetRightVector())/(Depth*Tan))*1280,(.5f-.5f*FVector::DotProduct(D,Capture->GetUpVector())/(Depth*Tan/(2560.f/1040.f)))*520);
}
void APokeMonsterClassicBattleScene::EndPlay(const EEndPlayReason::Type Reason)
{
 if(PlayerVisual)PlayerVisual->Destroy();if(OpponentVisual)OpponentVisual->Destroy();Capture->TextureTarget=nullptr;Super::EndPlay(Reason);
}
