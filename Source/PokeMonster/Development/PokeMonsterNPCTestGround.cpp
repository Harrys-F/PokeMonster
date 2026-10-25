#include "PokeMonsterNPCTestGround.h"
#include "../Characters/PokeMonsterNPCPresentationData.h"
#include "../Characters/PokeMonsterNPCVisualActor.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Dialogue/PokeMonsterDialogueData.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMeshActor.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Camera/PlayerCameraManager.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "HAL/IConsoleManager.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/PackageName.h"
#include "Materials/MaterialInterface.h"
namespace
{
 const TCHAR* Ids[]={TEXT("Ranger"),TEXT("SilverLady"),TEXT("TreeBeing"),TEXT("ElvenScholar"),TEXT("Wizard"),TEXT("WhiteHairedWarrior"),TEXT("DwarfWarrior"),TEXT("CrouchedCreature"),TEXT("ElvenArcher"),TEXT("DarkArmored"),TEXT("HobbitBase")};
}
bool UPokeMonsterNPCTestGround::IsSupportedMap(const FString& Name,EWorldType::Type Type)
{
#if WITH_EDITOR && !UE_BUILD_SHIPPING
 FString Leaf=FPackageName::GetShortName(Name);
 if(Leaf.StartsWith(TEXT("UEDPIE_"))){int32 Index=INDEX_NONE;Leaf.FindChar(TEXT('_'),Index);Leaf=Leaf.Mid(Index+1);Leaf.FindChar(TEXT('_'),Index);Leaf=Leaf.Mid(Index+1);}
 return Type==EWorldType::PIE&&Leaf==TEXT("Dev_TestMap_VisualV2");
#else
 return false;
#endif
}
bool UPokeMonsterNPCTestGround::DoesSupportWorldType(EWorldType::Type Type) const
{
#if WITH_EDITOR && !UE_BUILD_SHIPPING
 return Type==EWorldType::PIE;
#else
 return false;
#endif
}
void UPokeMonsterNPCTestGround::OnWorldBeginPlay(UWorld& World)
{
 Super::OnWorldBeginPlay(World);if(!IsSupportedMap(World.GetMapName(),World.WorldType)||!Owned.IsEmpty())return;
#if WITH_EDITOR && !UE_BUILD_SHIPPING
 FActorSpawnParameters Spawn;Spawn.ObjectFlags|=RF_Transient;Spawn.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* Cube=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));
 auto* Material=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Environment/HealingHouse/ArtV5/Materials/M_HH5_LandscapeGround.M_HH5_LandscapeGround"));
 if(!Cube||!Material)return;
 auto Box=[&](FVector Position,FVector Scale)
 {
  auto* A=World.SpawnActor<AStaticMeshActor>(Position,FRotator::ZeroRotator,Spawn);Owned.Add(A);
  auto* M=A->GetStaticMeshComponent();M->SetMobility(EComponentMobility::Movable);M->SetStaticMesh(Cube);M->SetMaterial(0,Material);M->SetCastShadow(false);M->SetCollisionProfileName(TEXT("BlockAll"));A->SetActorScale3D(Scale);A->Tags.Add(TEXT("NPCDevelopmentGround"));
 };
 Box(Center()+FVector(0,0,-20),FVector(50,38,.4));
 // Low development-only perimeter, so a normal manual test cannot walk into the void.
 Box(Center()+FVector(-2490,0,35),FVector(.2,38,.7));Box(Center()+FVector(2490,0,35),FVector(.2,38,.7));
 Box(Center()+FVector(0,-1890,35),FVector(50,.2,.7));Box(Center()+FVector(0,1890,35),FVector(50,.2,.7));
 TestDialogue=NewObject<UPokeMonsterDialogueData>(this);auto* Dialogue=TestDialogue.Get();FPokeMonsterDialoguePage Page;
 Page.SpeakerName=FText::FromString(TEXT("NPC-Bibliothek · technischer Test"));Page.Text=FText::FromString(TEXT("Hallo! Diese Figur zeigt Begruessung, Blickwendung und Gespraechsgesten. Rolle und Geschichte sind noch offen."));Dialogue->Pages.Add(Page);
 for(int32 I=0;I<UE_ARRAY_COUNT(Ids);++I)
 {
  const FString Asset=FString(TEXT("/Game/Characters/NPCs/Library/Profiles/DA_NPC_"))+Ids[I];
  auto* Profile=LoadObject<UPokeMonsterNPCPresentationData>(nullptr,*Asset);
  if(!Profile||!Profile->GetValidationErrors().IsEmpty()){UE_LOG(LogTemp,Error,TEXT("PM_NPCGROUND invalid profile %s"),Ids[I]);continue;}
  const float HalfHeight=FMath::Clamp(Profile->ReferenceHeightCm*.45f,40.f,160.f);
  const FVector Position=Station(I)+FVector(0,0,HalfHeight+.5f);
  auto* NPC=World.SpawnActorDeferred<APokeMonsterNPC>(APokeMonsterNPC::StaticClass(),FTransform(Position),nullptr,nullptr,ESpawnActorCollisionHandlingMethod::AlwaysSpawn);
  NPC->SetFlags(RF_Transient);NPC->DisplayName=FText::FromString(FString::Printf(TEXT("TEST %02d · %s"),I+1,Ids[I]));NPC->Dialogue=Dialogue;NPC->Tags.Add(TEXT("NPCDevelopmentSpecimen"));
  auto* Body=CastChecked<UCapsuleComponent>(NPC->GetRootComponent());Body->SetCapsuleSize(FMath::Clamp(Profile->ReferenceHeightCm*.12f,22.f,50.f),HalfHeight);Body->SetCollisionResponseToChannel(ECC_WorldStatic,ECR_Block);
  NPC->FinishSpawning(FTransform(Position));Owned.Add(NPC);
  auto* V=World.SpawnActor<APokeMonsterNPCVisualActor>(Station(I)+FVector(0,0,.5f),FRotator(0,135,0),Spawn);Owned.Add(V);V->SourceActor=NPC;V->ApplyPresentation(Profile);V->Tags.Add(TEXT("NPCDevelopmentSpecimen"));
  V->AttachToActor(NPC,FAttachmentTransformRules::KeepWorldTransform);
  // Source identity, labels and interaction remain those of the existing NPC class.
  for(auto* Label:NPC->GetComponents())
  {
   auto* T=Cast<UTextRenderComponent>(Label);if(!T)continue;if(T->GetFName()==TEXT("PlaceholderGlyph"))T->SetVisibility(false);
   else {T->SetRelativeLocation(FVector(0,0,Profile->ReferenceHeightCm-HalfHeight+25));T->SetWorldSize(18.f);}
  }
  Specimens.Add(NPC);Visuals.Add(V);Profiles.Add(Profile);Velocities.Add(FVector::ZeroVector);Targets.Add(Station(I)+FVector(220,0,0));Pauses.Add(I*.37f);
 }
 UE_LOG(LogTemp,Display,TEXT("PM_NPCGROUND ordinary PIE: %d/11. pm.NPCGround.Go [1..11], pm.NPCGround.Mode auto|idle|walk|run, pm.NPCGround.Return"),Specimens.Num());
#endif
}
void UPokeMonsterNPCTestGround::Tick(float Delta)
{
 if(Specimens.IsEmpty())return;Elapsed+=Delta;
 auto* Player=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));auto* PC=UGameplayStatics::GetPlayerController(this,0);
 auto* GI=GetWorld()->GetGameInstance();auto* Battle=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;auto* Dialogues=GI?GI->GetSubsystem<UPokeMonsterDialogueSubsystem>():nullptr;
 for(int32 I=0;I<Specimens.Num();++I)
 {
  auto* N=Specimens[I].Get();auto* V=Visuals[I].Get();auto* P=Profiles[I].Get();if(!IsValid(N)||!IsValid(V)||!P)continue;
  const bool Near=Player&&FVector::DistSquared2D(Player->GetActorLocation(),N->GetActorLocation())<FMath::Square(3200.f);
  const bool Speaking=Dialogues&&Dialogues->IsDialogueActive()&&Dialogues->GetActiveSource()==N;
  const bool Stop=!Near||Speaking||Battle&&Battle->IsEncounterActive()||Mode==TEXT("idle")||!P->Walk;
  const FVector Origin=Station(I);const FVector Now=N->GetActorLocation();
  float TargetSpeed=0.f;
  if(!Stop)
  {
   Pauses[I]=FMath::Max(0.f,Pauses[I]-Delta);
   FVector Direction=Targets[I]-Now;Direction.Z=0;
   if(Direction.Size2D()<12.f)
   {
    const float Angle=Elapsed*.37f+I*2.39996f;
    Targets[I]=Origin+FVector(FMath::Cos(Angle)*290.f,FMath::Sin(Angle)*290.f,0);
    Pauses[I]=Mode==TEXT("auto")?1.5f+FMath::Fmod(I*.73f+Elapsed,3.f):.35f;
   }
   if(Pauses[I]<=0.f)
   {
    const bool Running=P->Run&&(Mode==TEXT("run")||(Mode==TEXT("auto")&&FMath::Fmod(Elapsed+I*3.7f,32.f)>23.f));
    TargetSpeed=Running?P->RunSpeed:P->WalkSpeed;
   }
   FVector Desired=Direction.GetSafeNormal()*TargetSpeed;Velocities[I]=FMath::VInterpConstantTo(Velocities[I],Desired,Delta,220.f);
  }
  else Velocities[I]=FVector::ZeroVector;
  if(!Velocities[I].IsNearlyZero())
  {
   FHitResult Hit;N->SetActorLocation(Now+Velocities[I]*FMath::Min(Delta,.1f),true,&Hit);
   if(Hit.IsValidBlockingHit()){Velocities[I]=FVector::ZeroVector;Targets[I]=Origin-(Targets[I]-Origin)*.7f;Pauses[I]=.8f;}
  }
  if(PC)
   for(auto* C:N->GetComponents())
   {auto* T=Cast<UTextRenderComponent>(C);if(!T)continue;T->SetWorldRotation((PC->PlayerCameraManager->GetCameraLocation()-T->GetComponentLocation()).Rotation());}
 }
}
TStatId UPokeMonsterNPCTestGround::GetStatId() const {RETURN_QUICK_DECLARE_CYCLE_STAT(NPCTestGround,STATGROUP_Tickables);}
bool UPokeMonsterNPCTestGround::CanTravel() const
{
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));auto* GI=GetWorld()->GetGameInstance();auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 auto* D=GI?GI->GetSubsystem<UPokeMonsterDialogueSubsystem>():nullptr;
 return P&&!P->IsOverworldInputLocked()&&!P->IsUsingInteriorMovementBasis()&&!(E&&E->IsEncounterActive())&&!(D&&D->IsDialogueActive());
}
bool UPokeMonsterNPCTestGround::Travel(const FTransform& T)
{
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));if(!P||!P->TeleportTo(T.GetLocation(),T.Rotator(),false,false))return false;
 P->GetCharacterMovement()->StopMovementImmediately();return true;
}
bool UPokeMonsterNPCTestGround::Visit(int32 Number)
{
#if WITH_EDITOR && !UE_BUILD_SHIPPING
 if(!CanTravel()||Number<0||Number>Specimens.Num())return false;
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));auto* Save=GetWorld()->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>();if(!Save)return false;
 const bool Own=!Save->IsPIEMemoryPreviewActive();
 if(Own&&!Save->BeginPIEMemoryPreview())return false;
 FVector Position=Center()+FVector(0,350,0);
 if(Number>0)Position=Specimens[Number-1]->GetActorLocation()+FVector(-95,95,0);
 Position.Z=P->GetCapsuleComponent()->GetScaledCapsuleHalfHeight()+.5f;
 const FTransform Before=P->GetActorTransform();if(!Travel(FTransform(Before.GetRotation(),Position))){if(Own)Save->EndPIEMemoryPreview();return false;}
 if(!bHaveReturn){ReturnTransform=Before;ReturnPawn=P;bHaveReturn=true;bOwnsMemoryPreview=Own;}
 UE_LOG(LogTemp,Display,TEXT("PM_NPCGROUND visited %d; save transport is RAM-only until return"),Number);return true;
#else
 return false;
#endif
}
bool UPokeMonsterNPCTestGround::ReturnToWorld()
{
 if(!bHaveReturn||ReturnPawn.Get()!=UGameplayStatics::GetPlayerPawn(this,0)||!CanTravel()||!Travel(ReturnTransform))return false;
#if WITH_EDITOR
 if(bOwnsMemoryPreview)
  if(auto* S=GetWorld()->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>())if(!S->EndPIEMemoryPreview())return false;
#endif
 bOwnsMemoryPreview=false;bHaveReturn=false;ReturnPawn.Reset();return true;
}
bool UPokeMonsterNPCTestGround::SetMode(const FString& Requested)
{
 const FString M=Requested.ToLower();if(M!=TEXT("auto")&&M!=TEXT("idle")&&M!=TEXT("walk")&&M!=TEXT("run"))return false;Mode=M;return true;
}
bool UPokeMonsterNPCTestGround::Greet(){bool Any=false;for(const auto& V:Visuals)if(V)Any=V->PlayGreeting()||Any;return Any;}
void UPokeMonsterNPCTestGround::Deinitialize()
{
#if WITH_EDITOR
 if(bOwnsMemoryPreview&&GetWorld()&&GetWorld()->GetGameInstance())
  if(auto* S=GetWorld()->GetGameInstance()->GetSubsystem<UPokeMonsterSaveSubsystem>())S->EndPIEMemoryPreview();
#endif
 for(const auto& A:Owned)if(IsValid(A))A->Destroy();Owned.Reset();Specimens.Reset();Visuals.Reset();Profiles.Reset();Super::Deinitialize();
}
#if WITH_EDITOR && !UE_BUILD_SHIPPING
// Keep console registrations distinct when UBT combines development sources into one unity TU.
namespace PokeMonsterNPCGroundConsole
{
 UPokeMonsterNPCTestGround* Ground(UWorld* W){return W&&UPokeMonsterNPCTestGround::IsSupportedMap(W->GetMapName(),W->WorldType)?W->GetSubsystem<UPokeMonsterNPCTestGround>():nullptr;}
 FAutoConsoleCommandWithWorldAndArgs Go(TEXT("pm.NPCGround.Go"),TEXT("Ordinary VisualV2 PIE only: visit 0=center, 1..11=NPC; RAM-only save transport during visit."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()<=1){if(A.IsEmpty()||A[0].IsNumeric())G->Visit(A.IsEmpty()?0:FCString::Atoi(*A[0]));}}));
 FAutoConsoleCommandWithWorldAndArgs Back(TEXT("pm.NPCGround.Return"),TEXT("Return to original location and restore the temporary RAM session."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>&,UWorld* W){if(auto* G=Ground(W))G->ReturnToWorld();}));
 FAutoConsoleCommandWithWorldAndArgs Mode(TEXT("pm.NPCGround.Mode"),TEXT("auto | idle | walk | run; unsupported run safely remains walk."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& A,UWorld* W){if(auto* G=Ground(W);G&&A.Num()==1)G->SetMode(A[0]);}));
 FAutoConsoleCommandWithWorldAndArgs Greeting(TEXT("pm.NPCGround.Greet"),TEXT("Show available greeting clips; use normal B/E interaction for real dialogue."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>&,UWorld* W){if(auto* G=Ground(W))G->Greet();}));
}
#endif
