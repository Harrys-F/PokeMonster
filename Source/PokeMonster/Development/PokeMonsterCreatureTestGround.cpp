#include "PokeMonsterCreatureTestGround.h"
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
 for(auto* S:UPokeMonsterCreatureSpeciesData::GetRegisteredPlayableSpecies())Species.Add(S);
 if(Species.IsEmpty()){UE_LOG(LogTemp,Error,TEXT("PM_TESTGROUND registry contains no usable presentations"));return;}
 Columns=FMath::Clamp(FMath::CeilToInt(FMath::Sqrt(float(Species.Num()))),3,6);
 for(const auto& S:Species)
  if(const auto* P=S->GetVisuals().Presentation.LoadSynchronous())
   Spacing=FMath::Max(Spacing,2.f*P->Mesh->GetBounds().BoxExtent.Size2D()+1000.f);
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
 };
 // North edge stays at Y=-3600, outside the real world's Y=-3250 boundary.
 const int32 ModelRows=FMath::DivideAndRoundUp(Species.Num(),Columns);
 const float Width=Columns*Spacing,Height=ModelRows*Spacing;
 const FVector FloorCenter=Center()+FVector(0,400.f-Height*.5f,0);
 Box(FloorCenter-FVector(0,0,20),FVector(Width/100,Height/100,.4));
 for(float Side:{-1.f,1.f})
 {
  Box(FloorCenter+FVector(Side*(Width*.5f-10),0,35),FVector(.2,Height/100,.7));
  Box(FloorCenter+FVector(0,Side*(Height*.5f-10),35),FVector(Width/100,.2,.7));
 }
 for(int32 I=0;I<Species.Num();++I)
 {
  auto* S=Species[I].Get();
  auto* V=World.SpawnActor<APokeMonsterCreatureVisualActor>(GetStation(I),FRotator(0,135,0),Spawn);
  if(!V)continue;OwnedActors.Add(V);V->Tags.Add(TEXT("PokemonDevelopmentSpecimen"));
  if(!S||!V->SetSpecies(S)){V->Destroy();UE_LOG(LogTemp,Error,TEXT("PM_TESTGROUND invalid species %s"),*S->GetInternalId().ToString());continue;}
  V->SetActorLocation(GetStation(I)-FVector(0,0,V->Presentation->GroundOffsetCm));V->IdlePhaseOffset=I*.173f;
  auto* M=NewObject<UPokeMonsterCreatureRoamingComponent>(V);V->AddInstanceComponent(M);M->RegisterComponent();
  M->bControlledModelPreview=true;
  M->HabitatRadiusOverride=430.f;M->HabitatHalfExtent=FVector2D(430,430);
  M->bOverrideBehavior=true;M->BehaviorOverride.Temperament=EPokeMonsterOverworldTemperament::Calm;
  M->BehaviorOverride.Initiation=EPokeMonsterEncounterInitiation::Disabled;M->BehaviorOverride.bCanInitiateEncounter=false;
  M->BehaviorOverride.WalkMultiplier=1.f;
  M->Configure(S,-V->Presentation->GroundOffsetCm,S->Overworld.BodyRadius,FMath::Max(V->Presentation->ReferenceSizeCm*.5f,S->Overworld.BodyRadius),nullptr,7919+I*137);
  V->AddTickPrerequisiteComponent(M);V->SetGroundHoverContext(M);Specimens.Add(V);Movements.Add(M);
  RouteSteps.Add(0);TurnVelocity.Add(0.f);
  MovementReferenceSpeeds.Add(FVector2D(S->Overworld.WalkSpeedOverride>0.f?S->Overworld.WalkSpeedOverride:V->Presentation->WalkSpeed,
    S->Overworld.RunSpeedOverride>0.f?S->Overworld.RunSpeedOverride:V->Presentation->RunSpeed));
  auto* L=NewObject<UTextRenderComponent>(V);V->AddInstanceComponent(L);L->SetupAttachment(V->GetRootComponent());L->RegisterComponent();
  L->SetText(FText::FromString(FString::Printf(TEXT("TEST %02d | %s"),I+1,*S->GetDisplayName().ToString())));L->SetWorldSize(26);L->SetTextRenderColor(FColor(220,240,190));L->SetHorizontalAlignment(EHTA_Center);L->SetRelativeLocation(FVector(0,0,V->Presentation->ReferenceSizeCm+55));L->SetCollisionEnabled(ECollisionEnabled::NoCollision);L->SetCastShadow(false);Labels.Add(L);
 }
 UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND registered %d visual-only specimens; cell %.0f cm. pm.TestGround.List / Go [index|name] / Return"),Specimens.Num(),Spacing);
}
void UPokeMonsterCreatureTestGround::Tick(float Delta)
{
 if(Specimens.IsEmpty())return;
 auto* Player=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));auto* PC=UGameplayStatics::GetPlayerController(this,0);
 const bool Visiting=Player&&Player->ActorHasTag(TEXT("PokemonDevelopmentTestVisit"));
 const bool CanAnimate=Visiting&&!Player->IsOverworldInputLocked();
 if(CanAnimate)Elapsed+=Delta;
 for(int32 I=0;I<Specimens.Num();++I)
 {
  auto* V=Specimens[I].Get();auto* M=Movements[I].Get();if(!IsValid(V)||!IsValid(M))continue;
  const bool Nearby=Visiting&&FVector::DistSquared2D(Player->GetActorLocation(),GetStation(I))<FMath::Square(3500.f);
  V->SetActorHiddenInGame(!Nearby);V->SetActorTickEnabled(Nearby);V->Mesh->SetComponentTickEnabled(Nearby);
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
   const FVector Goal=GetStation(I)+FVector(320,0,0).RotateAngleAxis(Angle,FVector::UpVector);
   if(M->RequestModelPreviewGoal(Goal))++RouteSteps[I];
  }
  if(CanAnimate&&Nearby&&Selected==TEXT("turn"))
  {
   const float Yaw=UPokeMonsterCreatureRoamingComponent::AdvanceHeading(V->GetActorRotation().Yaw,135.f+Elapsed*35.f,TurnVelocity[I],M->Settings,Delta);
   V->SetActorRotation(FRotator(0,Yaw,0));
  }
  if(PC&&I<Labels.Num())Labels[I]->SetWorldRotation((PC->PlayerCameraManager->GetCameraLocation()-Labels[I]->GetComponentLocation()).Rotation());
 }
}
bool UPokeMonsterCreatureTestGround::ResetModels()
{
 for(int32 I=0;I<Specimens.Num();++I)
 {
  if(!IsValid(Specimens[I])||!IsValid(Movements[I]))return false;
  Movements[I]->SetMovementPaused(true);Specimens[I]->SetSpecies(Species[I]);Specimens[I]->SetActorLocation(GetStation(I)-FVector(0,0,Specimens[I]->Presentation->GroundOffsetCm));
  Specimens[I]->SetActorRotation(FRotator(0,135,0));RouteSteps[I]=0;TurnVelocity[I]=0;
 }
 Mode=TEXT("idle");Elapsed=0;return !Specimens.IsEmpty();
}
void UPokeMonsterCreatureTestGround::ListModels()const
{
 for(int32 I=0;I<Species.Num();++I)
 {
  const auto* P=Species[I]->GetVisuals().Presentation.LoadSynchronous();
  UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND %02d | %s | %s | %.0f cm | walk=%d run=%d swim=%d"),I+1,
   *Species[I]->GetDisplayName().ToString(),*Species[I]->GetInternalId().ToString(),P->ReferenceSizeCm,
   P->Clips.FindRef(EPokeMonsterCreatureClip::Walk)!=nullptr,P->Clips.FindRef(EPokeMonsterCreatureClip::Run)!=nullptr,P->SwimClip!=nullptr);
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
 P->GetCharacterMovement()->StopMovementImmediately();return true;
}
bool UPokeMonsterCreatureTestGround::Visit(int32 Number)
{
 if(!CanTravel()||Number<0||Number>Specimens.Num()){Message(TEXT("Nicht verfuegbar: nur VisualV2 Entwicklung/PIE, freie Aussenansicht; pm.TestGround.List."));return false;}
 auto* P=UGameplayStatics::GetPlayerPawn(this,0);
 const FTransform Before=P->GetActorTransform();
 FVector Ground=Center();
 if(Number>0)
 {
  const auto* V=Specimens[Number-1].Get();if(!IsValid(V))return false;
  // Visit the current animal, not an empty spawn point after it has wandered away.
  Ground=V->GetActorLocation()+FVector(-240,240,0);Ground.Z=Movements[Number-1]->HabitatOrigin.Z;
 }
 const float Height=Cast<APokeMonsterPlayerCharacter>(P)->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
 if(!Travel(FTransform(Before.GetRotation(),Ground+FVector(0,0,Height+.5f))))return false;
 if(!bHaveReturn){ReturnPosition=Before;ReturnPawn=P;bHaveReturn=true;P->Tags.AddUnique(TEXT("PokemonDevelopmentTestVisit"));}
 Message(TEXT("Modell-Testgelaende: keine Begegnungen oder Speichervorgaenge. Zurueck: pm.TestGround.Return"));return true;
}
bool UPokeMonsterCreatureTestGround::ReturnToWorld()
{
 if(!bHaveReturn||ReturnPawn.Get()!=UGameplayStatics::GetPlayerPawn(this,0)||!CanTravel())return false;
 if(!Travel(ReturnPosition)){Message(TEXT("Rueckkehrposition blockiert; Anker bleibt erhalten."));return false;}
 ReturnPawn->Tags.Remove(TEXT("PokemonDevelopmentTestVisit"));bHaveReturn=false;ReturnPawn.Reset();Message(TEXT("Zur urspruenglichen Position zurueckgekehrt."));return true;
}
bool UPokeMonsterCreatureTestGround::SetMode(const FString& Requested)
{
 const FString Value=Requested.ToLower();if(Value==TEXT("reset"))return ResetModels();
 if(Value!=TEXT("auto")&&Value!=TEXT("idle")&&Value!=TEXT("walk")&&Value!=TEXT("run")&&Value!=TEXT("turn")&&Value!=TEXT("directions"))return false;
 for(const auto& M:Movements)M->SetMovementPaused(true);Mode=Value;Elapsed=0;return true;
}
bool UPokeMonsterCreatureTestGround::React(const FString& Role)
{
 EPokeMonsterCreatureClip Clip;
 if(Role==TEXT("attack"))Clip=EPokeMonsterCreatureClip::Attack;else if(Role==TEXT("hit"))Clip=EPokeMonsterCreatureClip::Hit;
 else if(Role==TEXT("faint"))Clip=EPokeMonsterCreatureClip::Faint;else if(Role==TEXT("happy"))Clip=EPokeMonsterCreatureClip::Happy;else return false;
 bool Result=!Specimens.IsEmpty()&&Specimens.Num()==Species.Num();for(const auto& V:Specimens)Result=V->PlayReaction(Clip)&&Result;return Result;
}
void UPokeMonsterCreatureTestGround::Deinitialize()
{
 for(const auto& A:OwnedActors)if(IsValid(A))A->Destroy();OwnedActors.Reset();Labels.Reset();Movements.Reset();Specimens.Reset();Species.Reset();MovementReferenceSpeeds.Reset();RouteSteps.Reset();TurnVelocity.Reset();if(ReturnPawn.IsValid())ReturnPawn->Tags.Remove(TEXT("PokemonDevelopmentTestVisit"));ReturnPawn.Reset();bHaveReturn=false;Super::Deinitialize();
}
#if !UE_BUILD_SHIPPING
namespace
{
 UPokeMonsterCreatureTestGround* Ground(UWorld* W){return W&&UPokeMonsterCreatureTestGround::IsSupportedMap(W->GetMapName(),W->WorldType)?W->GetSubsystem<UPokeMonsterCreatureTestGround>():nullptr;}
 FAutoConsoleCommandWithWorldAndArgs Go(TEXT("pm.TestGround.Go"),TEXT("VisualV2 Development/PIE: center or registered specimen index/name; preserves return anchor."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W)){if(A.Num()>1)return;int32 Number=A.IsEmpty()?0:FCString::Atoi(*A[0]);if(A.Num()==1&&!A[0].IsNumeric()){Number=INDEX_NONE;for(int32 I=0;I<G->Species.Num();++I)if(G->Species[I]->GetInternalId().ToString().Equals(A[0],ESearchCase::IgnoreCase)||G->Species[I]->GetDisplayName().ToString().Equals(A[0],ESearchCase::IgnoreCase)){Number=I+1;break;}}G->Visit(Number);}}));
 FAutoConsoleCommandWithWorldAndArgs Back(TEXT("pm.TestGround.Return"),TEXT("Return to the original position before visiting the test ground."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W))G->ReturnToWorld();}));
 FAutoConsoleCommandWithWorldAndArgs Mode(TEXT("pm.TestGround.Mode"),TEXT("auto | idle | walk | run | turn | directions | reset. Registered test visuals only."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()==1)G->SetMode(A[0]);}));
 FAutoConsoleCommandWithWorldAndArgs TestGroundList(TEXT("pm.TestGround.List"),TEXT("List registered playable models and animation availability."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W))G->ListModels();}));
 FAutoConsoleCommandWithWorldAndArgs Reset(TEXT("pm.TestGround.Reset"),TEXT("Reset model positions and hold Idle."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W))G->ResetModels();}));
 FAutoConsoleCommandWithWorldAndArgs React(TEXT("pm.TestGround.React"),TEXT("attack | hit | faint | happy. Existing reactions, no combat."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()==1)G->React(A[0]);}));
}
#endif
