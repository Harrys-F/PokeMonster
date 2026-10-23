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
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "HAL/IConsoleManager.h"
#include "Misc/PackageName.h"
#include "Camera/PlayerCameraManager.h"
#include "Engine/GameInstance.h"
#include "Materials/MaterialInterface.h"
#include "Kismet/GameplayStatics.h"

namespace
{
 const TCHAR* DevelopmentSpecimenNames[]={TEXT("Zunderlauf"),TEXT("Schiggy"),TEXT("Bisasam"),TEXT("Pikachu"),TEXT("Myrapla"),TEXT("Enton"),TEXT("Machomei"),TEXT("Nebulak"),TEXT("Gengar"),TEXT("Glurak")};
 const TCHAR* DisplayNames[]={TEXT("Glumanda"),TEXT("Schiggy"),TEXT("Bisasam"),TEXT("Pikachu"),TEXT("Myrapla"),TEXT("Enton"),TEXT("Machomei"),TEXT("Nebulak"),TEXT("Gengar"),TEXT("Glurak")};
}
bool UPokeMonsterCreatureTestGround::IsSupportedMap(const FString& Name,EWorldType::Type Type)
{
#if WITH_EDITOR && !UE_BUILD_SHIPPING
 // PIE prefix is stripped by using the exact package leaf, never a substring match.
 FString Leaf=FPackageName::GetShortName(Name);
 if(Leaf.StartsWith(TEXT("UEDPIE_"))) { int32 End=INDEX_NONE; Leaf.FindChar(TEXT('_'),End); Leaf=Leaf.Mid(End+1); Leaf.FindChar(TEXT('_'),End); Leaf=Leaf.Mid(End+1); }
 return Type==EWorldType::PIE && Leaf==TEXT("Dev_TestMap_VisualV2");
#else
 return false;
#endif
}
bool UPokeMonsterCreatureTestGround::DoesSupportWorldType(EWorldType::Type Type) const
{
#if WITH_EDITOR && !UE_BUILD_SHIPPING
 return Type==EWorldType::PIE;
#else
 return false;
#endif
}
FVector UPokeMonsterCreatureTestGround::Station(int32 Index)
{
 return Center()+FVector((Index%5-2)*1000.f,(Index/5==0?-700.f:700.f),0);
}
void UPokeMonsterCreatureTestGround::OnWorldBeginPlay(UWorld& World)
{
 Super::OnWorldBeginPlay(World);
 if(!IsSupportedMap(World.GetMapName(),World.WorldType)||!OwnedActors.IsEmpty())return;
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
 // Separate from all authored scenery; top surface Z=0, low perimeter stops accidental falls.
 Box(Center()+FVector(0,0,-20),FVector(56,36,.4));
 Box(Center()+FVector(-2790,0,35),FVector(.2,36,.7));Box(Center()+FVector(2790,0,35),FVector(.2,36,.7));
 Box(Center()+FVector(0,-1790,35),FVector(56,.2,.7));Box(Center()+FVector(0,1790,35),FVector(56,.2,.7));
 for(int32 I=0;I<10;++I)
 {
  const FString Path=FString(TEXT("/Game/Data/Creatures/DA_"))+DevelopmentSpecimenNames[I]+TEXT(".DA_")+DevelopmentSpecimenNames[I];
  auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*Path);
  auto* V=World.SpawnActor<APokeMonsterCreatureVisualActor>(Station(I),FRotator(0,135,0),Spawn);
  if(!V)continue;OwnedActors.Add(V);V->Tags.Add(TEXT("PokemonDevelopmentSpecimen"));
  if(!S||!V->SetSpecies(S)){V->Destroy();UE_LOG(LogTemp,Error,TEXT("PM_TESTGROUND invalid species %s"),DevelopmentSpecimenNames[I]);continue;}
  V->SetActorLocation(Station(I)-FVector(0,0,V->Presentation->GroundOffsetCm));V->IdlePhaseOffset=I*.173f;
  auto* M=NewObject<UPokeMonsterCreatureRoamingComponent>(V);V->AddInstanceComponent(M);M->RegisterComponent();
  M->HabitatRadiusOverride=430.f;M->HabitatHalfExtent=FVector2D(430,430);
  M->bOverrideBehavior=true;M->BehaviorOverride.Temperament=EPokeMonsterOverworldTemperament::Calm;
  M->BehaviorOverride.Initiation=EPokeMonsterEncounterInitiation::Disabled;M->BehaviorOverride.bCanInitiateEncounter=false;
  M->BehaviorOverride.WalkMultiplier=1.f;
  M->Configure(S,-V->Presentation->GroundOffsetCm,S->Overworld.BodyRadius,FMath::Max(V->Presentation->ReferenceSizeCm*.5f,S->Overworld.BodyRadius),nullptr,7919+I*137);
  V->AddTickPrerequisiteComponent(M);V->SetGroundHoverContext(M);Specimens.Add(V);Movements.Add(M);
  MovementReferenceSpeeds.Add(FVector2D(S->Overworld.WalkSpeedOverride>0.f?S->Overworld.WalkSpeedOverride:V->Presentation->WalkSpeed,
    S->Overworld.RunSpeedOverride>0.f?S->Overworld.RunSpeedOverride:V->Presentation->RunSpeed));
  auto* L=NewObject<UTextRenderComponent>(V);V->AddInstanceComponent(L);L->SetupAttachment(V->GetRootComponent());L->RegisterComponent();
  L->SetText(FText::FromString(FString::Printf(TEXT("TEST %02d | %s"),I+1,DisplayNames[I])));L->SetWorldSize(26);L->SetTextRenderColor(FColor(220,240,190));L->SetHorizontalAlignment(EHTA_Center);L->SetRelativeLocation(FVector(0,0,V->Presentation->ReferenceSizeCm+55));L->SetCollisionEnabled(ECollisionEnabled::NoCollision);L->SetCastShadow(false);Labels.Add(L);
 }
 UE_LOG(LogTemp,Display,TEXT("PM_TESTGROUND ordinary PIE ready: %d/10 visual-only specimens. pm.TestGround.Go [1..10], pm.TestGround.Return"),Specimens.Num());
}
void UPokeMonsterCreatureTestGround::Tick(float Delta)
{
 if(Specimens.IsEmpty())return;
 Elapsed+=Delta;
 auto* P=UGameplayStatics::GetPlayerPawn(this,0);auto* PC=UGameplayStatics::GetPlayerController(this,0);
 for(int32 I=0;I<Specimens.Num();++I)
 {
  auto* V=Specimens[I].Get();auto* M=Movements[I].Get();if(!IsValid(V)||!IsValid(M))continue;
  const bool Nearby=P&&FVector::DistSquared2D(P->GetActorLocation(),V->GetActorLocation())<FMath::Square(3500.f);
  M->SetMovementPaused(!Nearby||Mode==TEXT("idle"));
  // Respect the same species overrides as wild/companion movement; authored clip references stay unchanged.
  const bool Run=Mode==TEXT("run")||(Mode==TEXT("auto")&&FMath::Fmod(Elapsed+I*3.7f,38.f)>24.f);
  M->Settings.WalkSpeedOverride=Run?MovementReferenceSpeeds[I].Y:MovementReferenceSpeeds[I].X;
  if(PC&&I<Labels.Num())Labels[I]->SetWorldRotation((PC->PlayerCameraManager->GetCameraLocation()-Labels[I]->GetComponentLocation()).Rotation());
 }
}
TStatId UPokeMonsterCreatureTestGround::GetStatId() const {RETURN_QUICK_DECLARE_CYCLE_STAT(PokemonTestGround,STATGROUP_Tickables);}
bool UPokeMonsterCreatureTestGround::CanTravel() const
{
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));
 const auto* GI=GetWorld()?GetWorld()->GetGameInstance():nullptr;
 const auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 const auto* C=GI?GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>():nullptr;
 return Specimens.Num()==10&&P&&!P->IsOverworldInputLocked()&&!P->IsUsingInteriorMovementBasis()&&!(E&&E->IsEncounterActive())&&!(C&&C->IsReturningFromDefeat());
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
 if(!CanTravel()||Number<0||Number>10){Message(TEXT("Nicht verfuegbar: nur VisualV2 PIE, freie Aussenansicht; Ziel 0..10."));return false;}
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
 if(!bHaveReturn){ReturnPosition=Before;ReturnPawn=P;bHaveReturn=true;}
 Message(TEXT("Entwicklungs-Testgelaende: TEST 01..10, keine Begegnungen. Zurueck: pm.TestGround.Return"));return true;
}
bool UPokeMonsterCreatureTestGround::ReturnToWorld()
{
 if(!bHaveReturn||ReturnPawn.Get()!=UGameplayStatics::GetPlayerPawn(this,0)||!CanTravel())return false;
 if(!Travel(ReturnPosition)){Message(TEXT("Rueckkehrposition blockiert; Anker bleibt erhalten."));return false;}
 bHaveReturn=false;ReturnPawn.Reset();Message(TEXT("Zur urspruenglichen Position zurueckgekehrt."));return true;
}
bool UPokeMonsterCreatureTestGround::SetMode(const FString& Requested)
{
 const FString Value=Requested.ToLower();if(Value!=TEXT("auto")&&Value!=TEXT("idle")&&Value!=TEXT("walk")&&Value!=TEXT("run"))return false;
 Mode=Value;return true;
}
bool UPokeMonsterCreatureTestGround::React(const FString& Role)
{
 EPokeMonsterCreatureClip Clip;
 if(Role==TEXT("attack"))Clip=EPokeMonsterCreatureClip::Attack;else if(Role==TEXT("hit"))Clip=EPokeMonsterCreatureClip::Hit;
 else if(Role==TEXT("faint"))Clip=EPokeMonsterCreatureClip::Faint;else if(Role==TEXT("happy"))Clip=EPokeMonsterCreatureClip::Happy;else return false;
 bool Result=Specimens.Num()==10;for(const auto& V:Specimens)Result=V->PlayReaction(Clip)&&Result;return Result;
}
void UPokeMonsterCreatureTestGround::Deinitialize()
{
 for(const auto& A:OwnedActors)if(IsValid(A))A->Destroy();OwnedActors.Reset();Labels.Reset();Movements.Reset();Specimens.Reset();MovementReferenceSpeeds.Reset();ReturnPawn.Reset();bHaveReturn=false;Super::Deinitialize();
}
#if WITH_EDITOR && !UE_BUILD_SHIPPING
namespace
{
 UPokeMonsterCreatureTestGround* Ground(UWorld* W){return W&&UPokeMonsterCreatureTestGround::IsSupportedMap(W->GetMapName(),W->WorldType)?W->GetSubsystem<UPokeMonsterCreatureTestGround>():nullptr;}
 FAutoConsoleCommandWithWorldAndArgs Go(TEXT("pm.TestGround.Go"),TEXT("Ordinary VisualV2 PIE: visit center or numbered specimen 1..10; preserves return anchor."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W)){if(A.Num()>1||(A.Num()==1&&!A[0].IsNumeric()))return;G->Visit(A.IsEmpty()?0:FCString::Atoi(*A[0]));}}));
 FAutoConsoleCommandWithWorldAndArgs Back(TEXT("pm.TestGround.Return"),TEXT("Return to the original position before visiting the test ground."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W))G->ReturnToWorld();}));
 FAutoConsoleCommandWithWorldAndArgs Mode(TEXT("pm.TestGround.Mode"),TEXT("auto | idle | walk | run. Test visuals only."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()==1)G->SetMode(A[0]);}));
 FAutoConsoleCommandWithWorldAndArgs React(TEXT("pm.TestGround.React"),TEXT("attack | hit | faint | happy. Existing reactions, no combat."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()==1)G->React(A[0]);}));
}
#endif
