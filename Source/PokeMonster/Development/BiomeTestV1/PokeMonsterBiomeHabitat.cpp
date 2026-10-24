#include "PokeMonsterBiomeHabitat.h"
#include "../../Characters/PokeMonsterPlayerCharacter.h"
#include "../../Creatures/PokeMonsterCreaturePresentation.h"
#include "../../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../../Creatures/Overworld/PokeMonsterCreatureCompanionSubsystem.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/GameInstance.h"
#include "../../Save/PokeMonsterSaveSubsystem.h"
#include "../../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/ConstructorHelpers.h"
APokeMonsterBiomeTestGameMode::APokeMonsterBiomeTestGameMode()
{
 bEnablePersistentGameplay=false;
 PlayerControllerClass=APlayerController::StaticClass();
}
void APokeMonsterBiomeTestGameMode::StartPlay()
{
 if(auto* Companion=GetWorld()->GetSubsystem<UPokeMonsterCreatureCompanionSubsystem>())Companion->SetEnabled(false);
 Super::StartPlay();
}
bool APokeMonsterBiomeTestGameMode::BeginIsolatedGameplayReview()
{
#if WITH_EDITOR
 if(!GetWorld()||GetWorld()->WorldType!=EWorldType::PIE||bReviewActive||bEnablePersistentGameplay||!GetGameInstance())return false;
 auto* Save=GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>();
 auto* Encounter=GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
 if(!Save||!Encounter||Encounter->IsEncounterActive()||Save->IsPIEMemoryPreviewActive()||!Save->BeginPIEMemoryPreview())return false;
 bReviewActive=true;bEnablePersistentGameplay=true;return true;
#else
 return false;
#endif
}
bool APokeMonsterBiomeTestGameMode::EndIsolatedGameplayReview()
{
#if WITH_EDITOR
 if(!GetWorld()||GetWorld()->WorldType!=EWorldType::PIE||!bReviewActive||!GetGameInstance())return false;
 auto* Save=GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>();
 auto* Encounter=GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
 if(!Save||!Encounter||Encounter->IsEncounterActive()||!Save->EndPIEMemoryPreview())return false;
 bEnablePersistentGameplay=false;bReviewActive=false;return true;
#else
 return false;
#endif
}
APokeMonsterBiomeHabitat::APokeMonsterBiomeHabitat()
{
 PrimaryActorTick.bCanEverTick=true;PrimaryActorTick.TickInterval=.25f;
 Bounds=CreateDefaultSubobject<UBoxComponent>(TEXT("HabitatBoundary"));SetRootComponent(Bounds);
 Bounds->SetBoxExtent(FVector(600,600,400));Bounds->SetCollisionEnabled(ECollisionEnabled::NoCollision);
 Bounds->SetHiddenInGame(true);Bounds->ShapeColor=FColor(110,190,150);
}
bool APokeMonsterBiomeHabitat::ContainsFootprint(FVector Point,float Radius) const
{
 if(Point.ContainsNaN()||!FMath::IsFinite(Radius)||Radius<0)return false;
 const FVector P=GetActorTransform().InverseTransformPosition(Point),B=Bounds->GetUnscaledBoxExtent();
 return FMath::Abs(P.X)+Radius<=B.X && FMath::Abs(P.Y)+Radius<=B.Y && P.Z>=-B.Z && P.Z<=B.Z;
}
bool APokeMonsterBiomeHabitat::ContainsFlightColumn(const FVector& Point,float Height,const FBox& B) const
{
 const float Radius=FMath::Max(FMath::Abs(B.Min.X),FMath::Abs(B.Max.X));
 return ContainsFootprint(Point,Radius)&&ContainsFootprint(Point+FVector(0,0,Height+B.Max.Z+15.f),Radius);
}
bool APokeMonsterBiomeHabitat::MediumFootHeight(EPokeMonsterBiomeMedium Mode,float Floor,float Surface,float Draft,float FloatHeight,float MinDepth,float& Height)
{
 for(float V:{Floor,Surface,Draft,FloatHeight,MinDepth})if(!FMath::IsFinite(V))return false;
 if(Draft<0||FloatHeight<0||MinDepth<0)return false;
 if(Mode==EPokeMonsterBiomeMedium::WaterOnly && Floor>Surface-FMath::Max(MinDepth,Draft+2.f))return false;
 if(Mode==EPokeMonsterBiomeMedium::Land && Floor<Surface-2.f)return false;
 Height=Mode==EPokeMonsterBiomeMedium::Floating?Floor+FloatHeight:
  (Mode==EPokeMonsterBiomeMedium::WaterOnly||Mode==EPokeMonsterBiomeMedium::Amphibious)?FMath::Max(Floor,Surface-Draft):Floor;
 return true;
}
void APokeMonsterBiomeHabitat::IgnorePlayerWaterBarriers(FCollisionQueryParams& Query) const
{
 for(const auto& A:PlayerWaterBarriers)if(A.IsValid())Query.AddIgnoredActor(A.Get());
}
bool APokeMonsterBiomeHabitat::ProjectFoot(const FVector& Point,float Radius,float HalfHeight,const FCollisionQueryParams& Input,FVector& Foot) const
{
 if(!GetWorld()||!ContainsFootprint(Point,Radius))return false;
 FHitResult Hit;auto Q=Input;IgnorePlayerWaterBarriers(Q);
 if(!GetWorld()->LineTraceSingleByChannel(Hit,FVector(Point.X,Point.Y,GetActorLocation().Z+1000.f),
  FVector(Point.X,Point.Y,GetActorLocation().Z-1500.f),ECC_Visibility,Q)||!Hit.GetComponent()
  ||Hit.GetComponent()->GetCollisionResponseToChannel(ECC_Pawn)!=ECR_Block)return false;
 const bool Swimming=(Medium==EPokeMonsterBiomeMedium::Amphibious||Medium==EPokeMonsterBiomeMedium::WaterOnly)
  && Hit.ImpactPoint.Z<WaterSurfaceZ-WaterDraftCm;
 if(!Swimming&&Hit.ImpactNormal.Z<.75f)return false;
 if(Hit.GetActor()&&Hit.GetActor()->ActorHasTag(TEXT("CreatureNoWalk")))return false;
 float Z=0;if(!MediumFootHeight(Medium,Hit.ImpactPoint.Z,WaterSurfaceZ,WaterDraftCm,FloatClearanceCm,MinimumDepthCm,Z))return false;
 Foot=FVector(Point.X,Point.Y,Z);
 return ContainsFootprint(Foot,Radius)&&!GetWorld()->OverlapBlockingTestByChannel(Foot+FVector(0,0,HalfHeight+28.f),FQuat::Identity,
  ECC_Pawn,FCollisionShape::MakeCapsule(Radius,FMath::Max(HalfHeight,Radius)),Q);
}
void APokeMonsterBiomeHabitat::BeginPlay()
{
 Super::BeginPlay();
 if(!GetWorld()->GetAuthGameMode<APokeMonsterBiomeTestGameMode>()) {SetActorTickEnabled(false);return;}
 bRunning=true;
 for(TActorIterator<AActor> It(GetWorld());It;++It)if(It->ActorHasTag(TEXT("BiomePlayerWaterBarrier")))PlayerWaterBarriers.Add(*It);
 for(const auto& S:Specimens)
 {
  auto* Species=S.Species.LoadSynchronous();if(!Species)continue;
  const FVector SpawnLocation=GetActorTransform().TransformPosition(S.LocalPosition);
  FActorSpawnParameters Params;Params.Owner=this;Params.ObjectFlags|=RF_Transient;Params.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
  AActor* Actor=nullptr;APokeMonsterCreatureVisualActor* Visual=nullptr;
  if(!S.bWaterDiagnostic)
  {
   Visual=GetWorld()->SpawnActor<APokeMonsterCreatureVisualActor>(SpawnLocation,FRotator::ZeroRotator,Params);
   if(!Visual||!Visual->SetSpecies(Species)){if(Visual)Visual->Destroy();continue;}
   if(!S.PresentationOverride.IsNull() && !Visual->SetPresentation(S.PresentationOverride.LoadSynchronous())) {Visual->Destroy();continue;}
   Actor=Visual;Visual->IdlePhaseOffset=FRandomStream(S.Seed).FRand();
  }
  else
  {
   Actor=GetWorld()->SpawnActor<AActor>(SpawnLocation,FRotator::ZeroRotator,Params);
   auto* Body=NewObject<UStaticMeshComponent>(Actor);Actor->SetRootComponent(Body);Actor->AddInstanceComponent(Body);
   Body->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Sphere.Sphere")));Body->SetRelativeScale3D(FVector(.60,.22,.18));
   Body->SetCollisionEnabled(ECollisionEnabled::NoCollision);Body->SetCastShadow(false);if(DiagnosticMaterial)Body->SetMaterial(0,DiagnosticMaterial);Body->RegisterComponent();
   Actor->Tags.Add(TEXT("WaterOnlyDiagnostic_NotGoldini"));
  }
  Actor->SetActorLocation(SpawnLocation);
  Actor->Tags.Add(TEXT("BiomeTestVisualOnly"));
  auto* Movement=NewObject<UPokeMonsterCreatureRoamingComponent>(Actor);Actor->AddInstanceComponent(Movement);Movement->RegisterComponent();
  Movement->BiomeHabitat=this;Movement->HabitatRadiusOverride=TravelPoints.IsEmpty()?FMath::Min(3500.f,FMath::Max(180.f,FMath::Max(Bounds->GetUnscaledBoxExtent().X,Bounds->GetUnscaledBoxExtent().Y)*1.1f)):3500.f;Movement->bOverrideBehavior=true;
  Movement->BehaviorOverride=Species->Overworld.Behavior;Movement->BehaviorOverride.Temperament=EPokeMonsterOverworldTemperament::Calm;
  Movement->BehaviorOverride.Initiation=EPokeMonsterEncounterInitiation::Disabled;Movement->BehaviorOverride.bCanInitiateEncounter=false;
  const float Radius=FMath::Max(ClearanceRadiusCm,Species->Overworld.BodyRadius),HalfHeight=FMath::Max(Radius,S.bWaterDiagnostic?12.f:Visual->Presentation->Mesh->GetBounds().BoxExtent.Z);
  const float Offset=Visual?-Visual->Presentation->GroundOffsetCm:0;
  Movement->Configure(Species,Offset,Radius,HalfHeight,nullptr,S.Seed);
  Movement->Settings.PauseMinimum=1.1f;Movement->Settings.PauseMaximum=3.9f;
  FVector Ground;if(Movement->ProjectWalkable(SpawnLocation,Ground))Actor->SetActorLocation(Ground+FVector(0,0,Offset));
  else {Actor->Destroy();continue;}
  if(Visual){Visual->AddTickPrerequisiteComponent(Movement);Visual->SetGroundHoverContext(Movement);}
  RuntimeSpecimens.Add(Actor);Movements.Add(Movement);WasSwimming.Add(false);
 }
}
void APokeMonsterBiomeHabitat::Tick(float Delta)
{
 Super::Tick(Delta);if(!bRunning)return;const auto* Player=UGameplayStatics::GetPlayerPawn(this,0);if(!Player)return;SuspendedCount=0;
 for(int32 I=0;I<RuntimeSpecimens.Num();++I)
 {
  auto* Actor=RuntimeSpecimens[I].Get();auto* Movement=Movements[I].Get();if(!Actor||!Movement)continue;
  const bool Far=FVector::DistSquared2D(Actor->GetActorLocation(),Player->GetActorLocation())>FMath::Square(ActiveDistanceCm);
  Movement->SetMovementPaused(Far);Movement->SetComponentTickEnabled(!Far);Actor->SetActorTickEnabled(!Far);if(Far)++SuspendedCount;
  if(auto* Visual=Cast<APokeMonsterCreatureVisualActor>(Actor))
  {
   Visual->Mesh->SetComponentTickEnabled(!Far);
   FCollisionQueryParams Q(SCENE_QUERY_STAT(BiomeMedia),false,Actor);IgnorePlayerWaterBarriers(Q);FHitResult Hit;
   const FVector P=Actor->GetActorLocation();float Alpha=0;
   if((Medium==EPokeMonsterBiomeMedium::Amphibious||Medium==EPokeMonsterBiomeMedium::WaterOnly)
    &&GetWorld()->LineTraceSingleByChannel(Hit,FVector(P.X,P.Y,800),FVector(P.X,P.Y,-1200),ECC_Visibility,Q))
    Alpha=FMath::Clamp((WaterSurfaceZ-WaterDraftCm-Hit.ImpactPoint.Z)/12.f,0.f,1.f);
   Visual->AquaticPoseAlpha=Alpha;
   const bool Swimming=Alpha>.5f;if(Swimming!=WasSwimming[I]){++MediaTransitions;WasSwimming[I]=Swimming;}
  }
 }
}
