#include "PokeMonsterClassicBattleScene.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Components/StaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "EngineUtils.h"
#include "Materials/MaterialInterface.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Engine/World.h"
#include "Engine/SkeletalMesh.h"
#include "UObject/ConstructorHelpers.h"

APokeMonsterClassicBattleScene::APokeMonsterClassicBattleScene()
{
 PrimaryActorTick.bCanEverTick=true;PrimaryActorTick.bStartWithTickEnabled=false;
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
 const TCHAR* MeshNames[]={TEXT("Grass"),TEXT("Herbs"),TEXT("Fern"),TEXT("Bush"),TEXT("RockA"),TEXT("RockB"),TEXT("Tree"),TEXT("Column"),TEXT("Wall"),TEXT("Moss")};
 const TCHAR* MeshPaths[]={TEXT("/Game/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_GrassMedium"),TEXT("/Game/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_MeadowHerbs"),TEXT("/Game/Environment/VisualV2WorldArtV7/Meshes/SM_WA7_Fern_A"),TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Bush_A"),TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Boulder_A"),TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Boulder_B"),TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Trees/SM_WLA_OakYoung_A"),TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Ruins/SM_WLA_Column_A"),TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Ruins/SM_WLA_WallRemnant_A"),TEXT("/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_MossCushion")};
 for(int I=0;I<10;++I){ConstructorHelpers::FObjectFinder<UStaticMesh> Asset(MeshPaths[I]);if(Asset.Object)DressingMeshes.Add(MeshNames[I],Asset.Object);}
 const TCHAR* Names[]={TEXT("Grass"),TEXT("Earth"),TEXT("Stone")};const TCHAR* Paths[]={TEXT("/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass"),TEXT("/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Earth"),TEXT("/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_MossStone")};
 for(int I=0;I<3;++I){ConstructorHelpers::FObjectFinder<UMaterialInterface> Asset(Paths[I]);if(Asset.Object)GroundMaterials.Add(Names[I],Asset.Object);}

}
void APokeMonsterClassicBattleScene::Configure(const UPokeMonsterCreatureSpeciesData* A,const UPokeMonsterCreatureSpeciesData* B,AActor* GroundReference,EPokeMonsterBattleEnvironment Theme,FName Region,AActor* EncounterSource)
{
 Environment=ResolveEnvironment(Theme,Region,EncounterSource?EncounterSource:GroundReference);
 if(IsValid(PlayerVisual))PlayerVisual->Destroy();PlayerVisual=nullptr;if(IsValid(OpponentVisual))OpponentVisual->Destroy();OpponentVisual=nullptr;
 if(!Target){Target=NewObject<UTextureRenderTarget2D>(this,NAME_None,RF_Transient);Target->RenderTargetFormat=RTF_RGBA8;Target->ClearColor=FLinearColor(.18f,.24f,.17f);Target->InitAutoFormat(2560,1080);Capture->TextureTarget=Target;}
 float Size=60.f;
 for(auto* Species:{A,B})if(Species)if(auto* Data=Species->GetVisuals().Presentation.LoadSynchronous())if(Data->Mesh)Size=FMath::Max(Size,Data->Mesh->GetBounds().BoxExtent.GetMax()*2.f);
 const float Fit=FMath::Max(1.f,Size/110.f);
 const FVector Forward=FRotator(0,-45,0).Vector(),Right=FRotationMatrix(FRotator(0,-45,0)).GetUnitAxis(EAxis::Y);
 const FVector Origin=GetActorLocation();
 Floor->SetRelativeLocation(FVector(0,0,-1));Floor->SetRelativeScale3D(FVector(80*Fit,80*Fit,.02f));
 Floor->SetMaterial(0,GroundMaterials.FindRef(Environment==EPokeMonsterBattleEnvironment::Cave?TEXT("Stone"):Environment==EPokeMonsterBattleEnvironment::Forest?TEXT("Earth"):TEXT("Grass")));
 Floor->SetLightingChannels(Environment!=EPokeMonsterBattleEnvironment::Cave,false,true);
 FramingDistance=610*Fit;
 Capture->SetRelativeLocation((-Forward*FramingDistance+FVector(0,0,FramingDistance*.33f)));
 Capture->SetWorldRotation((Origin+FVector(0,0,42*Fit)-Capture->GetComponentLocation()).Rotation());
 PresentationFill->SetRelativeLocation((-Forward*350+FVector(0,0,200))*Fit);PresentationFill->SetAttenuationRadius(1600*Fit);PresentationFill->SetIntensity((Environment==EPokeMonsterBattleEnvironment::Cave?160:50)*Fit*Fit);
 Capture->ShowOnlyActors.Reset();Capture->ShowOnlyActors.Add(this);
 auto Spawn=[&](const UPokeMonsterCreatureSpeciesData* Species,bool bPlayer)->APokeMonsterCreatureVisualActor*
 {
  if(!Species)return nullptr;auto* Data=Species->GetVisuals().Presentation.LoadSynchronous();if(!Data||!Data->Mesh)return nullptr;
  const FVector Offset=(bPlayer?(-Forward*70-Right*95):(Forward*80+Right*95))*Fit;
  auto* V=GetWorld()->SpawnActor<APokeMonsterCreatureVisualActor>(Origin+Offset-FVector(0,0,Data->GroundOffsetCm),(bPlayer?(Forward*150+Right*115):(-Forward*150-Right*115)).Rotation());
  if(!V)return nullptr;if(!V->SetSpecies(Species)){V->Destroy();return nullptr;}
  V->SetOwner(this);V->Mesh->VisibilityBasedAnimTickOption=EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
  TInlineComponentArray<UPrimitiveComponent*> Primitives(V);for(auto* P:Primitives){P->SetVisibleInSceneCaptureOnly(true);P->SetCastShadow(false);P->SetLightingChannels(Environment!=EPokeMonsterBattleEnvironment::Cave,false,true);P->bAffectDynamicIndirectLighting=false;P->bAffectDistanceFieldLighting=false;}
  Capture->ShowOnlyActors.Add(V);return V;
 };
 PlayerVisual=Spawn(A,true);OpponentVisual=Spawn(B,false);
 // Fit conservative body/tail bounds. Never rescale either creature.
 for(int Iter=0;Iter<24;++Iter){
  bool Fits=true;const float T=FMath::Tan(FMath::DegreesToRadians(Capture->FOVAngle*.5f));
  for(auto* V:{PlayerVisual.Get(),OpponentVisual.Get()})if(V){const FBox Box=V->Presentation->Mesh->GetBounds().GetBox().ExpandBy(4.f);for(int Corner=0;Corner<8;++Corner){const FVector P=V->GetActorTransform().TransformPosition(FVector(Corner&1?Box.Max.X:Box.Min.X,Corner&2?Box.Max.Y:Box.Min.Y,Corner&4?Box.Max.Z:Box.Min.Z));const FVector D=P-Capture->GetComponentLocation();const float Z=FVector::DotProduct(D,Capture->GetForwardVector());const float X=.5f+.5f*FVector::DotProduct(D,Capture->GetRightVector())/(Z*T),Y=.5f-.5f*FVector::DotProduct(D,Capture->GetUpVector())/(Z*T/(2560.f/1080.f));Fits&=Z>0&&X>.05f&&X<.95f&&Y>.06f&&Y<.95f;}}
  if(Fits)break;FramingDistance*=1.04f;Capture->SetRelativeLocation(-Forward*FramingDistance+FVector(0,0,FramingDistance*.33f));Capture->SetWorldRotation((Origin+FVector(0,0,42*Fit)-Capture->GetComponentLocation()).Rotation());
 }
 RestCamera=Capture->GetRelativeLocation();BuildEnvironment(Fit);
}
FVector2D APokeMonsterClassicBattleScene::ScreenAnchor(bool bPlayer,bool bGround) const
{
 const auto* V=bPlayer?PlayerVisual.Get():OpponentVisual.Get();if(!V)return bPlayer?FVector2D(350,350):FVector2D(890,235);
 const FVector D=V->GetActorLocation()+FVector(0,0,bGround?0.f:V->Mesh->Bounds.BoxExtent.Z)-Capture->GetComponentLocation();
 const float Depth=FMath::Max(1.f,FVector::DotProduct(D,Capture->GetForwardVector())),Tan=FMath::Tan(FMath::DegreesToRadians(Capture->FOVAngle*.5f));
 return FVector2D((.5f+.5f*FVector::DotProduct(D,Capture->GetRightVector())/(Depth*Tan))*1280,(.5f-.5f*FVector::DotProduct(D,Capture->GetUpVector())/(Depth*Tan/(2560.f/1080.f)))*540);
}
void APokeMonsterClassicBattleScene::EndPlay(const EEndPlayReason::Type Reason)
{
 if(PlayerVisual)PlayerVisual->Destroy();if(OpponentVisual)OpponentVisual->Destroy();Capture->TextureTarget=nullptr;Super::EndPlay(Reason);
}

EPokeMonsterBattleEnvironment APokeMonsterClassicBattleScene::ThemeForRegion(FName Region)
{
 const FString S=Region.ToString().ToLower();if(S.Contains(TEXT("cave"))||S.Contains(TEXT("hoehl")))return EPokeMonsterBattleEnvironment::Cave;
 if(S.Contains(TEXT("ruin")))return EPokeMonsterBattleEnvironment::Ruins;if(S.Contains(TEXT("forest"))||S.Contains(TEXT("wald")))return EPokeMonsterBattleEnvironment::Forest;
 return EPokeMonsterBattleEnvironment::Auto;
}
EPokeMonsterBattleEnvironment APokeMonsterClassicBattleScene::ResolveEnvironment(EPokeMonsterBattleEnvironment Requested,FName Region,AActor* Reference)
{
 if(Requested!=EPokeMonsterBattleEnvironment::Auto&&uint8(Requested)<=uint8(EPokeMonsterBattleEnvironment::Ruins))return Requested;
 if(auto R=ThemeForRegion(Region);R!=EPokeMonsterBattleEnvironment::Auto)return R;
 if(Reference&&Reference->GetWorld()){for(FName T:Reference->Tags)if(auto R=ThemeForRegion(T);R!=EPokeMonsterBattleEnvironment::Auto)return R;
  int Trees=0;
  for(TActorIterator<AActor> It(Reference->GetWorld());It;++It){
   TInlineComponentArray<UStaticMeshComponent*> Parts(*It);
   for(auto* C:Parts)if(C->GetStaticMesh()){
    const FString Path=C->GetStaticMesh()->GetPathName();const bool Ruin=Path.Contains(TEXT("/Ruins/")),Tree=Path.Contains(TEXT("/Trees/"));if(!Ruin&&!Tree)continue;
    auto Nearby=[&](const FVector& P){return FVector::DistSquared(P,Reference->GetActorLocation())<=FMath::Square(650.f);};
    int Count=0;if(auto* Instances=Cast<UInstancedStaticMeshComponent>(C)){for(int I=0;I<Instances->GetInstanceCount();++I){FTransform T;if(Instances->GetInstanceTransform(I,T,true)&&Nearby(T.GetLocation()))++Count;}}
    else Count=Nearby(C->GetComponentLocation())?1:0;
    if(Ruin&&Count>0)return EPokeMonsterBattleEnvironment::Ruins;if(Tree)Trees+=Count;
   }
  }
  if(Trees>=3)return EPokeMonsterBattleEnvironment::Forest;
 }
 return EPokeMonsterBattleEnvironment::Meadow;
}
void APokeMonsterClassicBattleScene::BuildEnvironment(float Fit)
{
 for(UInstancedStaticMeshComponent* C:Dressing)if(C)C->DestroyComponent();Dressing.Reset();
 const FVector F=FRotator(0,-45,0).Vector(),R=FRotationMatrix(FRotator(0,-45,0)).GetUnitAxis(EAxis::Y);
 TMap<FName,UInstancedStaticMeshComponent*> Groups;
 auto Add=[&](FName Name,float Ahead,float Across,float Size,float Yaw=0.f,float Z=0.f){
  UStaticMesh* Mesh=DressingMeshes.FindRef(Name);if(!Mesh)return;auto*& C=Groups.FindOrAdd(Name);if(!C){C=NewObject<UInstancedStaticMeshComponent>(this,NAME_None,RF_Transient);AddInstanceComponent(C);C->SetupAttachment(GetRootComponent());C->SetStaticMesh(Mesh);C->SetCollisionEnabled(ECollisionEnabled::NoCollision);C->SetCanEverAffectNavigation(false);C->SetCastShadow(false);C->SetVisibleInSceneCaptureOnly(true);C->SetLightingChannels(Environment!=EPokeMonsterBattleEnvironment::Cave,false,true);C->bAffectDynamicIndirectLighting=false;C->bAffectDistanceFieldLighting=false;C->RegisterComponent();Dressing.Add(C);}
  C->AddInstance(FTransform(FRotator(0,Yaw,0),(F*Ahead+R*Across+FVector(0,0,Z))*Fit,FVector(Size*Fit)));
 };
 FRandomStream Random(8117+int(Environment));
 // Deliberate clear central battle space; clusters on the side and behind the opponents.
 for(int I=0;I<72;++I){const float Side=I%2?-1.f:1.f,A=Random.FRandRange(-90,430),X=Side*Random.FRandRange(170,390);if(Environment!=EPokeMonsterBattleEnvironment::Cave)Add(I%5==0?TEXT("Herbs"):Environment==EPokeMonsterBattleEnvironment::Forest?TEXT("Fern"):TEXT("Grass"),A,X,Random.FRandRange(.3f,.7f),Random.FRandRange(0,360));if(I%7==0)Add(TEXT("RockA"),A,X,Random.FRandRange(.08f,.18f),I*39);}
 if(Environment==EPokeMonsterBattleEnvironment::Forest){for(int I=0;I<7;++I)Add(TEXT("Tree"),410+Random.FRandRange(-40,80),-390+I*130,Random.FRandRange(.45f,.7f),I*57);for(int I=0;I<12;++I)Add(TEXT("Bush"),260+I%3*75,-390+I*70,.8f,I*47);}
 else if(Environment==EPokeMonsterBattleEnvironment::Meadow){for(int I=0;I<10;++I)Add(TEXT("Bush"),420+Random.FRandRange(-50,60),-420+I*90,Random.FRandRange(.5f,.95f),I*41);Add(TEXT("Tree"),640,-480,.7f,17);Add(TEXT("Tree"),650,490,.8f,141);}
 else if(Environment==EPokeMonsterBattleEnvironment::Ruins){for(int I=0;I<5;++I)Add(TEXT("Column"),350+I%2*75,-350+I*175,1.35f,I*37);for(int I=0;I<5;++I)Add(TEXT("Wall"),510,-430+I*210,1.5f,45);for(int I=0;I<10;++I)Add(TEXT("Moss"),Random.FRandRange(200,420),Random.FRandRange(-380,380),1.f,I*53);}
 else {for(int I=0;I<11;++I){float A=FMath::DegreesToRadians(-100.f+I*20.f);Add(I%2?TEXT("RockA"):TEXT("RockB"),400+FMath::Cos(A)*140,FMath::Sin(A)*460,Random.FRandRange(2.5f,4.f),I*41,-20);}for(int I=0;I<20;++I)Add(TEXT("RockB"),Random.FRandRange(200,500),Random.FRandRange(-500,500),Random.FRandRange(.3f,.8f),I*39);}
}
void APokeMonsterClassicBattleScene::React(bool bPlayer,FName Step,int32 Damage)
{
 if(Step==TEXT("Windup")||(Step==TEXT("Impact")&&Damage>0)){PulseTime=0;PulseStrength=(Step==TEXT("Impact")?2.f:1.f)*(bPlayer?1.f:-1.f);SetActorTickEnabled(true);}
}
void APokeMonsterClassicBattleScene::Tick(float Delta)
{
 Super::Tick(Delta);PulseTime+=Delta;const float Wave=FMath::Sin(FMath::Clamp(PulseTime/.35f,0.f,1.f)*PI);
 Capture->SetRelativeLocation(RestCamera+Capture->GetRightVector()*Wave*PulseStrength);
 if(PulseTime>=.35f){Capture->SetRelativeLocation(RestCamera);SetActorTickEnabled(false);}
}
