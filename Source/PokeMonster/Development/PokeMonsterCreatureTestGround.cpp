#include "PokeMonsterCreatureTestGround.h"
#include "BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "Components/BoxComponent.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "Engine/SkeletalMesh.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "HAL/IConsoleManager.h"
#include "Misc/PackageName.h"
#include "Camera/PlayerCameraManager.h"
#include "Engine/GameInstance.h"
#include "Materials/MaterialInterface.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/SpringArmComponent.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "Modules/ModuleManager.h"

UWorld* UPokeMonsterCreatureTestGround::ResolveConsoleWorld(UWorld* Context)
{
 if(Context&&(Context->WorldType==EWorldType::Game||Context->WorldType==EWorldType::PIE))
  return IsSupportedMap(Context->GetMapName(),Context->WorldType)?Context:nullptr;
 UWorld* Found=nullptr;
 if(GEngine)for(const auto& C:GEngine->GetWorldContexts())
  if(C.World()&&IsSupportedMap(C.World()->GetMapName(),C.WorldType))
  {if(Found&&Found!=C.World())return nullptr;Found=C.World();}
 return Found;
}
bool UPokeMonsterCreatureTestGround::IsInspectionAsset(const FString& Path)
{
 return Path.StartsWith(ImportRoot()+TEXT("/"));
}
bool UPokeMonsterCreatureTestGround::SupportsInspectionMode(const FString& Value)
{
 return Value==TEXT("idle")||Value==TEXT("turn")||Value==TEXT("reset");
}
void UPokeMonsterCreatureTestGround::DiscoverImports(bool bScanDisk)
{
 ImportModels.Reset();ImportSizes.Reset();
 auto& Registry=FModuleManager::LoadModuleChecked<FAssetRegistryModule>(TEXT("AssetRegistry")).Get();
 // Fresh -game processes need an explicit metadata scan of new uncooked inspection assets.
 // Do this only on a user review request, never as a model/texture load during normal play.
 if(bScanDisk)Registry.ScanPathsSynchronous({ImportRoot()},false);
 FARFilter Filter;Filter.PackagePaths.Add(*ImportRoot());Filter.bRecursivePaths=true;
 Filter.ClassPaths.Add(UStaticMesh::StaticClass()->GetClassPathName());TArray<FAssetData> Assets;
 Registry.GetAssets(Filter,Assets);
 for(const auto& A:Assets)if(IsInspectionAsset(A.PackageName.ToString()))
 {
  const FString Relative=A.PackageName.ToString().Mid(ImportRoot().Len()+1);
  FString Name,Remainder;Relative.Split(TEXT("/"),&Name,&Remainder);
  // One imported mesh per source directory; never load textures/models during normal play.
  if(!ImportModels.Contains(Name))
  {
   ImportModels.Add(Name,A.GetSoftObjectPath());FString Approx;A.GetTagValue(TEXT("ApproxSize"),Approx);TArray<FString> Parts;Approx.ParseIntoArray(Parts,TEXT("x"));
   FVector Size(200);if(Parts.Num()==3)Size=FVector(FCString::Atof(*Parts[0]),FCString::Atof(*Parts[1]),FCString::Atof(*Parts[2]));
   ImportSizes.Add(Name,Size);
  }
 }
}
TArray<FString> UPokeMonsterCreatureTestGround::GetImportTargets()
{
 if(ImportModels.IsEmpty())DiscoverImports(true);
 TArray<FString> Names;ImportModels.GetKeys(Names);Names.Sort();return Names;
}
void UPokeMonsterCreatureTestGround::EndImportInspection()
{
 // Changing selection or returning never removes a physically placed model.
 ImportSpecimen=nullptr;ActiveImport.Reset();
}
int32 UPokeMonsterCreatureTestGround::GetPhysicalModelCount()const
{
 int32 Count=0;for(const auto& A:Specimens)if(IsValid(A))++Count;for(const auto& A:StaticSpecimens)if(IsValid(A))++Count;return Count;
}
FVector UPokeMonsterCreatureTestGround::GetVisitGround(int32 Index)const
{
 if(!Stations.IsValidIndex(Index))return Center()+FVector(0,100,0);
 const auto* Presentation=Species[Index]->GetVisuals().Presentation.LoadSynchronous();
 // Water views enter at the open north gate, keeping the outer safety rail behind the camera.
 const float Side=Presentation&&Presentation->SwimClip?1.f:-1.f;
 return Stations[Index]+FVector(0,Side*(CellHalfSizes[Index]-65),0);
}
FVector UPokeMonsterCreatureTestGround::GetImportStation(const FString& Name)const
{
 const int32 Index=ImportNames.IndexOfByPredicate([&](const FString& N){return N.Equals(Name,ESearchCase::IgnoreCase);});
 return ImportStations.IsValidIndex(Index)?ImportStations[Index]:FVector::ZeroVector;
}
void UPokeMonsterCreatureTestGround::BuildLayout()
{
 Stations.SetNum(Species.Num());CellHalfSizes.SetNum(Species.Num());MotionRadii.SetNum(Species.Num());
 ImportNames=GetImportTargets();StaticSpecimens.SetNum(ImportNames.Num());ImportOrigins.SetNum(ImportNames.Num());
 struct FCell{bool Raw;int32 Index;float Half;};TArray<FCell> Land;TArray<int32> Water;
 for(int32 I=0;I<Species.Num();++I)
 {
  const auto* P=Species[I]->GetVisuals().Presentation.LoadSynchronous();const auto& B=P->Mesh->GetBounds();
  float Envelope=(B.Origin.GetAbs()+B.BoxExtent).Size2D()*1.2f;
  if(P->SwimMesh){const auto& SB=P->SwimMesh->GetBounds();Envelope=FMath::Max(Envelope,float((SB.Origin.GetAbs()+SB.BoxExtent).Size2D()*P->SwimBoundsScale));}
  MotionRadii[I]=FMath::Clamp(P->ReferenceSizeCm*1.15f,90.f,450.f);
  CellHalfSizes[I]=FMath::Max(200.f,Envelope+MotionRadii[I]+125.f);
  if(P->SwimClip){CellHalfSizes[I]+=100.f;Water.Add(I);}else Land.Add({false,I,CellHalfSizes[I]});
 }
 for(int32 I=0;I<ImportNames.Num();++I)
 {
  const FVector Size=ImportSizes.FindRef(ImportNames[I]);ImportDimensions.Add(Size);
  const float Half=FMath::Max(145.f,float(Size.Size2D()*.5f+85.f));ImportHalfSizes.Add(Half);ImportStations.Add(FVector::ZeroVector);Land.Add({true,I,Half});
 }
 // Small specimens share compact rows, while envelopes keep large models genuinely clear.
 Land.Sort([](const FCell& A,const FCell& B){return A.Half<B.Half;});
 float X=-1600.f,Y=300.f,Row=0.f;
 for(const auto& Cell:Land)
 {
  if(X+Cell.Half*2>1600.f&&X>-1600.f){X=-1600.f;Y-=Row+140.f;Row=0.f;}
  const FVector P=Center()+FVector(X+Cell.Half,Y-Cell.Half,0);
  if(Cell.Raw)ImportStations[Cell.Index]=P;else Stations[Cell.Index]=P;
  X+=Cell.Half*2+140.f;Row=FMath::Max(Row,Cell.Half*2);
 }
 Y-=Row+180.f;X=-1600.f;
 for(int32 I:Water){Stations[I]=Center()+FVector(X+CellHalfSizes[I],Y-CellHalfSizes[I],0);X+=CellHalfSizes[I]*2+180.f;}
}
void UPokeMonsterCreatureTestGround::CreatePlaque(const FVector& Location,const FString& Text)
{
 FActorSpawnParameters Spawn;Spawn.ObjectFlags|=RF_Transient;auto* A=GetWorld()->SpawnActor<AActor>(Location,FRotator(0,-90,0),Spawn);if(!A)return;
 OwnedActors.Add(A);A->Tags.Add(TEXT("PokemonDevelopmentPlaque"));auto* L=NewObject<UTextRenderComponent>(A);A->AddInstanceComponent(L);A->SetRootComponent(L);L->RegisterComponent();L->SetWorldLocationAndRotation(Location,FRotator(0,-90,0));
 L->SetText(FText::FromString(Text));L->SetWorldSize(9.f);L->SetTextRenderColor(FColor(229,220,181));L->SetHorizontalAlignment(EHTA_Center);L->SetVerticalAlignment(EVRTA_TextTop);L->SetCullDistance(1500.f);L->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}
bool UPokeMonsterCreatureTestGround::LoadImport(int32 Index)
{
 if(!StaticSpecimens.IsValidIndex(Index))return false;if(IsValid(StaticSpecimens[Index]))return true;
 const FString& Name=ImportNames[Index];auto* Mesh=Cast<UStaticMesh>(ImportModels.FindChecked(Name).TryLoad());if(!Mesh)return false;
 FActorSpawnParameters Spawn;Spawn.ObjectFlags|=RF_Transient;auto* A=GetWorld()->SpawnActor<AStaticMeshActor>(ImportStations[Index],FRotator(0,-90,0),Spawn);if(!A)return false;
 StaticSpecimens[Index]=A;OwnedActors.Add(A);A->SetActorEnableCollision(false);A->SetActorTickEnabled(false);A->Tags.Add(TEXT("PokemonStaticImportInspection"));
 auto* C=A->GetStaticMeshComponent();C->SetMobility(EComponentMobility::Movable);C->SetStaticMesh(Mesh);C->SetCollisionEnabled(ECollisionEnabled::NoCollision);C->SetCastShadow(true);C->SetComponentTickEnabled(false);
 // Preserve the imported centimetre geometry. This is explicitly not a canonical species scale.
 const auto B=Mesh->GetBoundingBox();const FVector Offset=FRotator(0,-90,0).RotateVector(FVector(B.GetCenter().X,B.GetCenter().Y,B.Min.Z));A->SetActorLocation(ImportStations[Index]-Offset);ImportOrigins[Index]=A->GetActorTransform();
 CreatePlaque(ImportStations[Index]+FVector(0,-ImportHalfSizes[Index]+25,65),FString::Printf(TEXT("%s | STATISCH\nRig / Animation fehlen | %.0f x %.0f x %.0f cm\nImportmassstab; Artmassstab offen"),*Name,ImportDimensions[Index].X,ImportDimensions[Index].Y,ImportDimensions[Index].Z));return true;
}
bool UPokeMonsterCreatureTestGround::VisitImport(const FString& Target)
{
 if(!CanTravel())return false;
 const int32 Index=ImportNames.IndexOfByPredicate([&](const FString& N){return N.Equals(Target,ESearchCase::IgnoreCase);});
 if(Index==INDEX_NONE){Message(TEXT("Unbekannter Modellimport. Verfuegbar: pm.TestGround.List"));return false;}
 if(!Visit(0)||!LoadImport(Index))return false;
 const FVector Safe=ImportStations[Index]+FVector(0,-ImportHalfSizes[Index]-65,0);
 auto* Player=CastChecked<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));
 if(!Travel(FTransform(Player->GetActorRotation(),Safe+FVector(0,0,Player->GetCapsuleComponent()->GetScaledCapsuleHalfHeight()+.5f))))return false;
 ImportSpecimen=StaticSpecimens[Index];ImportOrigin=ImportOrigins[Index];ActiveImport=ImportNames[Index];Mode=TEXT("idle");
 Player->RestoreSavedFacing(FVector(0,1,0));Player->ThirdPersonBoom->SetWorldRotation(FRotator(0,90,0));
 Message(FString::Printf(TEXT("%s: statischer Originalimport, Rig/Animation/Artmassstab offen. Die gesamte Sammlung wird einmalig vorbereitet und bleibt platziert."),*ActiveImport));return true;
}
bool UPokeMonsterCreatureTestGround::VisitTarget(const FString& Target)
{
 if(Target.StartsWith(TEXT("Modell:"),ESearchCase::IgnoreCase))return VisitImport(Target.Mid(7));
 if(Target.IsEmpty())return Visit(0);
 if(Target.IsNumeric())return Visit(FCString::Atoi(*Target));
 for(int32 I=0;I<Species.Num();++I)
  if(Species[I]->GetInternalId().ToString().Equals(Target,ESearchCase::IgnoreCase)||Species[I]->GetDisplayName().ToString().Equals(Target,ESearchCase::IgnoreCase))return Visit(I+1);
 for(const auto& N:ImportNames)if(N.Equals(Target,ESearchCase::IgnoreCase))return VisitImport(N);
 Message(FString::Printf(TEXT("Unbekanntes Ziel '%s'. Verfuegbare Ziele folgen im Protokoll: pm.TestGround.List"),*Target));ListModels();return false;
}
bool UPokeMonsterCreatureTestGround::IsSupportedMap(const FString& Name,EWorldType::Type Type)
{
#if !UE_BUILD_SHIPPING
 // PIE prefix is stripped by using the exact package leaf, never a substring match.
 FString Leaf=FPackageName::GetShortName(Name);
 if(Leaf.StartsWith(TEXT("UEDPIE_"))) { int32 End=INDEX_NONE; Leaf.FindChar(TEXT('_'),End); Leaf=Leaf.Mid(End+1); Leaf.FindChar(TEXT('_'),End); Leaf=Leaf.Mid(End+1); }
 return (Type==EWorldType::PIE||Type==EWorldType::Game) && Leaf==TEXT("Dev_TestMap_VisualV2");
#else
 return false;
#endif
}
bool UPokeMonsterCreatureTestGround::DoesSupportWorldType(EWorldType::Type Type) const
{
#if !UE_BUILD_SHIPPING
 return Type==EWorldType::PIE||Type==EWorldType::Game;
#else
 return false;
#endif
}
FVector UPokeMonsterCreatureTestGround::Station(int32 Index,int32 CountColumns,float Cell)
{
 CountColumns=FMath::Max(1,CountColumns);
 return Center()+FVector((Index%CountColumns-(CountColumns-1)*.5f)*Cell,400.f-Cell*.5f-(Index/CountColumns)*Cell,0);
}
void UPokeMonsterCreatureTestGround::OnWorldBeginPlay(UWorld& World)
{
 Super::OnWorldBeginPlay(World);
 if(!IsSupportedMap(World.GetMapName(),World.WorldType)||!OwnedActors.IsEmpty())return;
 DiscoverImports(true);
 for(auto* S:UPokeMonsterCreatureSpeciesData::GetRegisteredPlayableSpecies())Species.Add(S);
 if(Species.IsEmpty()){UE_LOG(LogTemp,Error,TEXT("PM_TESTGROUND registry contains no usable presentations"));return;}
 BuildLayout();
 FActorSpawnParameters Spawn;Spawn.ObjectFlags|=RF_Transient;Spawn.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* Cube=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));
 auto* Material=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Environment/HealingHouse/ArtV5/Materials/M_HH5_LandscapeGround.M_HH5_LandscapeGround"));
 if(!Cube||!Material){UE_LOG(LogTemp,Error,TEXT("PM_TESTGROUND missing existing floor assets"));return;}
 auto Box=[&](const FVector& P,const FVector& Scale)
 {
  auto* A=World.SpawnActor<AStaticMeshActor>(P,FRotator::ZeroRotator,Spawn);if(!A)return;
  A->Tags.Add(TEXT("PokemonDevelopmentTestGround"));OwnedActors.Add(A);
  auto* C=A->GetStaticMeshComponent();C->SetMobility(EComponentMobility::Movable);C->SetStaticMesh(Cube);C->SetMaterial(0,Material);
  C->SetCollisionProfileName(TEXT("BlockAll"));C->SetCastShadow(false);A->SetActorScale3D(Scale);
  if(FMath::IsNearlyEqual(Scale.Z,0.7,0.001))
  {
   // Preserve the continuous capsule barrier, but avoid hiding small swimming models.
   C->SetVisibility(false);
   for(float Side:{-1.f,1.f})
   {
    auto* Rail=NewObject<UStaticMeshComponent>(A);A->AddInstanceComponent(Rail);Rail->SetupAttachment(C);
    Rail->SetStaticMesh(Cube);Rail->SetMaterial(0,Material);Rail->SetCollisionEnabled(ECollisionEnabled::NoCollision);Rail->SetCastShadow(false);
    Rail->SetRelativeScale3D(FVector(1,1,.1f));Rail->SetRelativeLocation(FVector(0,0,Side*43.f));Rail->RegisterComponent();
   }
  }
 };
 // One land foundation, genuinely separate pool beds and continuous safe perimeter walks.
 FBox LandBounds(ForceInit);for(int32 I=0;I<Species.Num();++I)if(!Species[I]->GetVisuals().Presentation.LoadSynchronous()->SwimClip){LandBounds+=Stations[I]+FVector(CellHalfSizes[I]+90,CellHalfSizes[I]+90,0);LandBounds+=Stations[I]-FVector(CellHalfSizes[I]+90,CellHalfSizes[I]+90,0);}
 for(int32 I=0;I<ImportNames.Num();++I){LandBounds+=ImportStations[I]+FVector(ImportHalfSizes[I]+100,ImportHalfSizes[I]+100,0);LandBounds+=ImportStations[I]-FVector(ImportHalfSizes[I]+100,ImportHalfSizes[I]+100,0);}
 Box(LandBounds.GetCenter()-FVector(0,0,20),FVector(LandBounds.GetSize().X/100,LandBounds.GetSize().Y/100,.4));
 // Retain the old gallery's fall protection on the resized platform.
 for(float Side:{-1.f,1.f})
 {
  Box(LandBounds.GetCenter()+FVector(Side*(LandBounds.GetExtent().X-10),0,35),FVector(.2,LandBounds.GetSize().Y/100,.7));
  // South openings stay clear for both pool connectors; protect the other three edges.
  if(Side>0)Box(LandBounds.GetCenter()+FVector(0,LandBounds.GetExtent().Y-10,35),FVector(LandBounds.GetSize().X/100,.2,.7));
 }

 TArray<FVector2D> Gates;
 for(int32 I=0;I<Species.Num();++I)if(Species[I]->GetVisuals().Presentation.LoadSynchronous()->SwimClip)Gates.Add(FVector2D(Stations[I].X-70,Stations[I].X+70));
 Gates.Sort([](const FVector2D& A,const FVector2D& B){return A.X<B.X;});
 float Edge=LandBounds.Min.X;
 auto SouthRail=[&](float From,float To){if(To>From)Box(FVector((From+To)*.5f,LandBounds.Min.Y+10,Center().Z+35),FVector((To-From)/100,.2,.7));};
 for(const auto& Gate:Gates){SouthRail(Edge,FMath::Clamp(float(Gate.X),float(LandBounds.Min.X),float(LandBounds.Max.X)));Edge=FMath::Max(Edge,float(Gate.Y));}
 SouthRail(Edge,LandBounds.Max.X);
 TMap<int32,APokeMonsterBiomeHabitat*> Pools;
 auto* WaterMaterial=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Environment/VisualV2InteriorV7/Materials/M_V7_ReviewWater.M_V7_ReviewWater"));
 for(int32 I=0;I<Species.Num();++I)
 {
  const auto* P=Species[I]->GetVisuals().Presentation.LoadSynchronous();if(!P->SwimClip)continue;
  const FVector Origin=GetStation(I);const float Half=CellHalfSizes[I],Inside=Half-150.f,Depth=FMath::Max(180.f,P->SwimSubmergedDepthCm+100.f);
  Box(Origin-FVector(0,0,Depth+20),FVector(Inside*2/100,Inside*2/100,.4));
  for(float Side:{-1.f,1.f})
  {
   Box(Origin+FVector(Side*(Half-70),0,-20),FVector(1.4,Half*2/100,.4));
   Box(Origin+FVector(0,Side*(Half-70),-20),FVector((Half*2-280)/100,1.4,.4));
   // A low continuous kerb protects the player; water path queries explicitly ignore it.
   const int32 First=OwnedActors.Num();Box(Origin+FVector(Side*Inside,0,35),FVector(.18,Inside*2/100,.7));Box(Origin+FVector(0,Side*Inside,35),FVector(Inside*2/100,.18,.7));
   for(int32 K=First;K<OwnedActors.Num();++K)OwnedActors[K]->Tags.Add(TEXT("BiomePlayerWaterBarrier"));
  }
  for(float Side:{-1.f,1.f})Box(Origin+FVector(Side*(Half-10),0,35),FVector(.2,Half*2/100,.7));
  Box(Origin+FVector(0,-Half+10,35),FVector(Half*2/100,.2,.7));
  for(float Side:{-1.f,1.f})Box(Origin+FVector(Side*(Half+70)*.5f,Half-10,35),FVector((Half-70)/100,.2,.7));
  // Connect the north boardwalk to the existing land foundation, without covering the water.
  const float North=Origin.Y+Half,South=LandBounds.Min.Y,Gap=South-North;
  if(Gap>0)
  {
   Box(FVector(Origin.X,(North+South)*.5f,Center().Z-20),FVector(1.4,Gap/100,.4));
   for(float Side:{-1.f,1.f})Box(FVector(Origin.X+Side*60,(North+South)*.5f,Center().Z+35),FVector(.2,Gap/100,.7));
  }
  auto* Z=World.SpawnActor<APokeMonsterBiomeHabitat>(Origin,FRotator::ZeroRotator,Spawn);OwnedActors.Add(Z);Z->Medium=EPokeMonsterBiomeMedium::WaterOnly;Z->Bounds->SetBoxExtent(FVector(Inside,Inside,700));Z->WaterSurfaceZ=Origin.Z-20;Z->WaterDraftCm=P->SwimMesh?P->SwimSubmergedDepthCm:43.f;Z->MinimumDepthCm=20;Z->bAllowNaturalActivities=false;Z->SetActorTickEnabled(false);Pools.Add(I,Z);
  const int32 First=OwnedActors.Num();Box(Origin-FVector(0,0,25),FVector(Inside*2/100,Inside*2/100,.1));
  if(OwnedActors.Num()>First){auto* Water=CastChecked<AStaticMeshActor>(OwnedActors.Last());Water->SetActorEnableCollision(false);if(WaterMaterial)Water->GetStaticMeshComponent()->SetMaterial(0,WaterMaterial);}
 }
 for(int32 I=0;I<Species.Num();++I)
 {
  auto* S=Species[I].Get();
  auto* V=World.SpawnActor<APokeMonsterCreatureVisualActor>(GetStation(I),FRotator(0,135,0),Spawn);
  if(!V)continue;OwnedActors.Add(V);V->Tags.Add(TEXT("PokemonDevelopmentSpecimen"));
  if(!S||!V->SetSpecies(S)){V->Destroy();UE_LOG(LogTemp,Error,TEXT("PM_TESTGROUND invalid species %s"),*S->GetInternalId().ToString());continue;}
  float WaterDrop=0.f;if(auto* Pool=Pools.FindRef(I))WaterDrop=20.f+Pool->WaterDraftCm;
  V->SetActorLocation(GetStation(I)-FVector(0,0,V->Presentation->GroundOffsetCm+WaterDrop));V->IdlePhaseOffset=I*.173f;
  auto* M=NewObject<UPokeMonsterCreatureRoamingComponent>(V);V->AddInstanceComponent(M);M->RegisterComponent();
  M->bControlledModelPreview=true;
  M->HabitatRadiusOverride=FMath::Max(150.f,MotionRadii[I]+V->Presentation->ReferenceSizeCm);M->HabitatHalfExtent=FVector2D(MotionRadii[I]+20.f,MotionRadii[I]+20.f);
  M->BiomeHabitat=Pools.FindRef(I);
  M->bOverrideBehavior=true;M->BehaviorOverride.Temperament=EPokeMonsterOverworldTemperament::Calm;
  M->BehaviorOverride.Initiation=EPokeMonsterEncounterInitiation::Disabled;M->BehaviorOverride.bCanInitiateEncounter=false;
  M->BehaviorOverride.WalkMultiplier=1.f;
  M->Configure(S,-V->Presentation->GroundOffsetCm,S->Overworld.BodyRadius,FMath::Max(V->Presentation->ReferenceSizeCm*.5f,S->Overworld.BodyRadius),nullptr,7919+I*137);
  V->AddTickPrerequisiteComponent(M);V->SetGroundHoverContext(M);Specimens.Add(V);Movements.Add(M);
  RouteSteps.Add(0);TurnVelocity.Add(0.f);
  MovementReferenceSpeeds.Add(FVector2D(S->Overworld.WalkSpeedOverride>0.f?S->Overworld.WalkSpeedOverride:V->Presentation->WalkSpeed,
    S->Overworld.RunSpeedOverride>0.f?S->Overworld.RunSpeedOverride:V->Presentation->RunSpeed));
  CreatePlaque(GetVisitGround(I)+FVector(-75,0,65),FString::Printf(TEXT("%s | SPIELBEREIT\nRig + vorhandene Animationen | %.0f cm\nFlaeche %.1f x %.1f m"),*S->GetDisplayName().ToString(),V->Presentation->ReferenceSizeCm,CellHalfSizes[I]*.02f,CellHalfSizes[I]*.02f));
  if(V->Presentation->SwimClip)OwnedActors.Last()->SetActorRotation(FRotator(0,90,0));
  auto* L=NewObject<UTextRenderComponent>(V);V->AddInstanceComponent(L);L->SetupAttachment(V->GetRootComponent());L->RegisterComponent();
  L->SetText(FText::FromString(FString::Printf(TEXT("TEST %02d | %s"),I+1,*S->GetDisplayName().ToString())));APokeMonsterCreatureVisualActor::StyleNameplate(L);V->PlaceNameplate(L,nullptr);L->SetVisibility(false);Labels.Add(L);
 }
 UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND %d playable and %d static targets; individual mesh/motion envelopes. First visit prepares the permanent collection. pm.TestGround.List / Go [index|name] / Return"),Specimens.Num(),ImportNames.Num());
}
void UPokeMonsterCreatureTestGround::Tick(float Delta)
{
 if(Specimens.IsEmpty())return;
 auto* Player=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));auto* PC=UGameplayStatics::GetPlayerController(this,0);
 const bool Visiting=Player&&Player->ActorHasTag(TEXT("PokemonDevelopmentTestVisit"));
 const bool CanAnimate=Visiting&&!Player->IsOverworldInputLocked();
 if(bCollectionRequested)
 {
  bCollectionRequested=false;
  for(int32 I=0;I<StaticSpecimens.Num();++I)if(!IsValid(StaticSpecimens[I])){bCollectionRequested=true;LoadImport(I);break;}
 }
 if(CanAnimate)Elapsed+=Delta;
 if(IsValid(ImportSpecimen)&&CanAnimate&&Mode==TEXT("turn"))ImportSpecimen->AddActorWorldRotation(FRotator(0,Delta*25.f,0));
 for(int32 I=0;I<Specimens.Num();++I)
 {
  auto* V=Specimens[I].Get();auto* M=Movements[I].Get();if(!IsValid(V)||!IsValid(M))continue;
  const bool Nearby=Visiting&&FVector::DistSquared2D(Player->GetActorLocation(),GetStation(I))<FMath::Square(CellHalfSizes[I]+1500.f);
  V->SetActorHiddenInGame(false);V->SetActorTickEnabled(Nearby);V->Mesh->SetComponentTickEnabled(Nearby);
  FString Selected=Mode;
  if(Mode==TEXT("auto"))
  {
   const float Phase=FMath::Fmod(Elapsed,38.f);
   Selected=Phase<5?TEXT("idle"):Phase<17?TEXT("walk"):Phase<29?TEXT("run"):Phase<34?TEXT("turn"):TEXT("idle");
  }
  const auto* P=V->Presentation.Get();
  const bool HasWalk=P->Clips.FindRef(EPokeMonsterCreatureClip::Walk)!=nullptr;
  const bool HasRun=P->Clips.FindRef(EPokeMonsterCreatureClip::Run)!=nullptr
   && P->Clips.FindRef(EPokeMonsterCreatureClip::Run)!=P->Clips.FindRef(EPokeMonsterCreatureClip::Idle);
  const bool Run=Selected==TEXT("run");
  const bool Move=CanAnimate&&Nearby&&(Selected==TEXT("walk")||Selected==TEXT("directions")||Run)&&(Run?HasRun:HasWalk);
  M->Settings.WalkSpeedOverride=Run?MovementReferenceSpeeds[I].Y:MovementReferenceSpeeds[I].X;
  M->SetMovementPaused(!Move);M->SetComponentTickEnabled(Nearby);
  // Fish/sea-serpent reviews use their authored swim layer, without a fake land gait.
  V->AquaticPoseAlpha=P->SwimClip&&(P->RigFamily==EPokeMonsterCreatureRigFamily::Aquatic||P->RigFamily==EPokeMonsterCreatureRigFamily::Serpentine)?1.f:0.f;
  if(Move&&!M->IsModelPreviewMoving())
  {
   const int32 Step=RouteSteps[I]%8;const float Angle=Step*45.f;
   FVector Goal=Movements[I]->HabitatOrigin+FVector(MotionRadii[I],0,0).RotateAngleAxis(Angle,FVector::UpVector);
   if(M->RequestModelPreviewGoal(Goal))++RouteSteps[I];
  }
  if(CanAnimate&&Nearby&&Selected==TEXT("turn"))
  {
   const float Yaw=UPokeMonsterCreatureRoamingComponent::AdvanceHeading(V->GetActorRotation().Yaw,135.f+Elapsed*35.f,TurnVelocity[I],M->Settings,Delta);
   V->SetActorRotation(FRotator(0,Yaw,0));
  }
  if(PC&&Nearby&&I<Labels.Num())V->PlaceNameplate(Labels[I],PC->PlayerCameraManager);
 }
}
bool UPokeMonsterCreatureTestGround::ResetModels()
{
 if(IsValid(ImportSpecimen)){ImportSpecimen->SetActorTransform(ImportOrigin);Mode=TEXT("idle");Elapsed=0;return true;}
 for(int32 I=0;I<Specimens.Num();++I)
 {
  if(!IsValid(Specimens[I])||!IsValid(Movements[I]))return false;
  Movements[I]->SetMovementPaused(true);Specimens[I]->SetSpecies(Species[I]);Specimens[I]->SetActorLocation(Movements[I]->HabitatOrigin-FVector(0,0,Specimens[I]->Presentation->GroundOffsetCm));
  Specimens[I]->SetActorRotation(FRotator(0,135,0));RouteSteps[I]=0;TurnVelocity[I]=0;
 }
 Mode=TEXT("idle");Elapsed=0;return !Specimens.IsEmpty();
}
void UPokeMonsterCreatureTestGround::ListModels()
{
 for(int32 I=0;I<ImportNames.Num();++I)UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND Modell:%s | STATISCH | Rig/Animation fehlen | %.0fx%.0fx%.0f cm Importmassstab (Artmassstab offen) | Flaeche %.1f m"),*ImportNames[I],ImportDimensions[I].X,ImportDimensions[I].Y,ImportDimensions[I].Z,ImportHalfSizes[I]*.02f);
 for(int32 I=0;I<Species.Num();++I)
 {
  const auto* P=Species[I]->GetVisuals().Presentation.LoadSynchronous();
  const FVector Size=P->Mesh->GetBounds().BoxExtent*2.f;
  const bool Run=P->Clips.FindRef(EPokeMonsterCreatureClip::Run)&&P->Clips.FindRef(EPokeMonsterCreatureClip::Run)!=P->Clips.FindRef(EPokeMonsterCreatureClip::Idle);
  UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND %02d | %s | SPIELBEREIT, Rig vorhanden | Mesh %.0fx%.0fx%.0f cm, Referenz %.0f cm | Flaeche %.1f m | walk=%d run=%d swim=%d"),I+1,
   *Species[I]->GetDisplayName().ToString(),Size.X,Size.Y,Size.Z,P->ReferenceSizeCm,CellHalfSizes[I]*.02f,
   P->Clips.FindRef(EPokeMonsterCreatureClip::Walk)!=nullptr,Run,P->SwimClip!=nullptr);
 }
}
TStatId UPokeMonsterCreatureTestGround::GetStatId() const {RETURN_QUICK_DECLARE_CYCLE_STAT(PokemonTestGround,STATGROUP_Tickables);}
bool UPokeMonsterCreatureTestGround::CanTravel() const
{
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));
 const auto* GI=GetWorld()?GetWorld()->GetGameInstance():nullptr;
 const auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 const auto* C=GI?GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>():nullptr;
 return !Specimens.IsEmpty()&&Specimens.Num()==Species.Num()&&P&&!P->IsOverworldInputLocked()&&!P->IsUsingInteriorMovementBasis()&&!(E&&E->IsEncounterActive())&&!(C&&C->IsReturningFromDefeat());
}
void UPokeMonsterCreatureTestGround::Message(const FString& Text) const
{
 UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND %s"),*Text);
 if(GEngine)GEngine->AddOnScreenDebugMessage(62051,8.f,FColor(200,240,170),Text);
}
bool UPokeMonsterCreatureTestGround::Travel(const FTransform& Destination)
{
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));if(!P)return false;
 if(!P->TeleportTo(Destination.GetLocation(),Destination.Rotator(),false,false))return false;
 P->GetCharacterMovement()->StopMovementImmediately();
 TArray<USpringArmComponent*> Arms;P->GetComponents(Arms);
 for(auto* Arm:Arms)
 {
  const bool Lag=Arm->bEnableCameraLag,RotationLag=Arm->bEnableCameraRotationLag;
  Arm->bEnableCameraLag=false;Arm->bEnableCameraRotationLag=false;Arm->TickComponent(0.f,LEVELTICK_All,nullptr);
  Arm->bEnableCameraLag=Lag;Arm->bEnableCameraRotationLag=RotationLag;
 }
 if(auto* PC=UGameplayStatics::GetPlayerController(this,0);PC&&PC->PlayerCameraManager)PC->PlayerCameraManager->SetGameCameraCutThisFrame();
 return true;
}
bool UPokeMonsterCreatureTestGround::Visit(int32 Number)
{
 if(!CanTravel()||Number<0||Number>Specimens.Num()){Message(TEXT("Nicht verfuegbar: nur VisualV2 Entwicklung/PIE, freie Aussenansicht; pm.TestGround.List."));return false;}
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));
 const FTransform Before=P->GetActorTransform();
 const FVector Facing=P->GetInteractionWorldDirection();const FRotator Orbit=P->ThirdPersonBoom->GetComponentRotation();
 const bool Third=P->IsThirdPersonCamera();const float Distance=P->ThirdPersonDistance;
 bCollectionRequested=true;
 FVector Ground=GetVisitGround(-1);
 if(Number>0)
 {
  const auto* V=Specimens[Number-1].Get();if(!IsValid(V))return false;
  // Visit the current animal, not an empty spawn point after it has wandered away.
  Ground=GetVisitGround(Number-1);
 }
 const float Height=Cast<APokeMonsterPlayerCharacter>(P)->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
 if(!Travel(FTransform(Before.GetRotation(),Ground+FVector(0,0,Height+.5f))))return false;
 EndImportInspection();
 if(Number>0)
 {
  const FVector Look=(Specimens[Number-1]->GetActorLocation()-P->GetActorLocation()).GetSafeNormal2D();
  P->RestoreSavedFacing(Look);if(P->IsThirdPersonCamera())P->ThirdPersonBoom->SetWorldRotation(FRotator(0,Look.Rotation().Yaw,0));
 }
 if(!bHaveReturn){ReturnFacing=Facing;ReturnOrbit=Orbit;bReturnThirdPerson=Third;ReturnDistance=Distance;ReturnPosition=Before;ReturnPawn=P;bHaveReturn=true;P->Tags.AddUnique(TEXT("PokemonDevelopmentTestVisit"));}
 Message(TEXT("Modell-Testgelaende: keine Begegnungen oder Speichervorgaenge. Zurueck: pm.TestGround.Return"));return true;
}
bool UPokeMonsterCreatureTestGround::ReturnToWorld()
{
 if(!bHaveReturn||ReturnPawn.Get()!=UGameplayStatics::GetPlayerPawn(this,0)||!CanTravel())return false;
 if(!Travel(ReturnPosition)){Message(TEXT("Rueckkehrposition blockiert; Anker bleibt erhalten."));return false;}
 auto* Player=CastChecked<APokeMonsterPlayerCharacter>(ReturnPawn.Get());
 Player->RestoreSavedFacing(ReturnFacing);Player->ThirdPersonDistance=ReturnDistance;Player->ThirdPersonBoom->TargetArmLength=ReturnDistance;
 Player->SetThirdPersonCamera(bReturnThirdPerson);Player->ThirdPersonBoom->SetWorldRotation(ReturnOrbit);
 EndImportInspection();
 ReturnPawn->Tags.Remove(TEXT("PokemonDevelopmentTestVisit"));bHaveReturn=false;ReturnPawn.Reset();Message(TEXT("Zur urspruenglichen Position zurueckgekehrt."));return true;
}
bool UPokeMonsterCreatureTestGround::SetMode(const FString& Requested)
{
 const FString Value=Requested.ToLower();
 if(!ActiveImport.IsEmpty()&&!SupportsInspectionMode(Value)){Message(TEXT("Statischer Originalimport besitzt keine Bewegungsanimationen. Verfuegbar: idle | turn | reset."));return false;}
 if(Value==TEXT("reset"))return ResetModels();
 if(Value!=TEXT("auto")&&Value!=TEXT("idle")&&Value!=TEXT("walk")&&Value!=TEXT("run")&&Value!=TEXT("turn")&&Value!=TEXT("directions"))return false;
 for(const auto& M:Movements)M->SetMovementPaused(true);Mode=Value;Elapsed=0;return true;
}
bool UPokeMonsterCreatureTestGround::React(const FString& Role)
{
 if(!ActiveImport.IsEmpty()){Message(TEXT("Keine Reaktionsanimation am ungeriggten Modellimport vorhanden."));return false;}
 EPokeMonsterCreatureClip Clip;
 if(Role==TEXT("attack"))Clip=EPokeMonsterCreatureClip::Attack;else if(Role==TEXT("hit"))Clip=EPokeMonsterCreatureClip::Hit;
 else if(Role==TEXT("faint"))Clip=EPokeMonsterCreatureClip::Faint;else if(Role==TEXT("happy"))Clip=EPokeMonsterCreatureClip::Happy;else return false;
 bool Result=!Specimens.IsEmpty()&&Specimens.Num()==Species.Num();for(const auto& V:Specimens)Result=V->PlayReaction(Clip)&&Result;return Result;
}
void UPokeMonsterCreatureTestGround::Deinitialize()
{
 EndImportInspection();ImportModels.Reset();StaticSpecimens.Reset();ImportNames.Reset();ImportSizes.Reset();
 for(const auto& A:OwnedActors)if(IsValid(A))A->Destroy();OwnedActors.Reset();Labels.Reset();Movements.Reset();Specimens.Reset();Species.Reset();MovementReferenceSpeeds.Reset();RouteSteps.Reset();TurnVelocity.Reset();if(ReturnPawn.IsValid())ReturnPawn->Tags.Remove(TEXT("PokemonDevelopmentTestVisit"));ReturnPawn.Reset();bHaveReturn=false;Super::Deinitialize();
}
#if !UE_BUILD_SHIPPING
namespace
{
 UPokeMonsterCreatureTestGround* Ground(UWorld* Context)
 {
  if(auto* W=UPokeMonsterCreatureTestGround::ResolveConsoleWorld(Context))return W->GetSubsystem<UPokeMonsterCreatureTestGround>();
  UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND Keine eindeutige laufende VisualV2-Spielwelt. VisualV2 in PIE/Development starten; bei mehreren PIE-Welten Spielkonsole verwenden."));return nullptr;
 }
 FAutoConsoleCommandWithWorldAndArgs Go(TEXT("pm.TestGround.Go"),TEXT("VisualV2 Development/PIE: center or registered specimen index/name; preserves return anchor."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W)){G->VisitTarget(FString::Join(A,TEXT(" ")));}}));
 FAutoConsoleCommandWithWorldAndArgs Back(TEXT("pm.TestGround.Return"),TEXT("Return to the original position before visiting the test ground."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W))G->ReturnToWorld();}));
 FAutoConsoleCommandWithWorldAndArgs Mode(TEXT("pm.TestGround.Mode"),TEXT("auto | idle | walk | run | turn | directions | reset. Registered test visuals only."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()==1)G->SetMode(A[0]);}));
 FAutoConsoleCommandWithWorldAndArgs TestGroundList(TEXT("pm.TestGround.List"),TEXT("List registered playable models and animation availability."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W))G->ListModels();}));
 FAutoConsoleCommandWithWorldAndArgs Reset(TEXT("pm.TestGround.Reset"),TEXT("Reset model positions and hold Idle."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W))G->ResetModels();}));
 FAutoConsoleCommandWithWorldAndArgs React(TEXT("pm.TestGround.React"),TEXT("attack | hit | faint | happy. Existing reactions, no combat."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()==1)G->React(A[0]);}));
}
#endif
