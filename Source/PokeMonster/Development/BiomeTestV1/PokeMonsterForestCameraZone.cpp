#include "PokeMonsterForestCameraZone.h"
#include "../../Camera/PokeMonsterCameraVisibilityComponent.h"
#include "../../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Components/BoxComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/Pawn.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
APokeMonsterForestCameraZone::APokeMonsterForestCameraZone()
{
 PrimaryActorTick.bCanEverTick=true;PrimaryActorTick.TickGroup=TG_PrePhysics;
 Bounds=CreateDefaultSubobject<UBoxComponent>(TEXT("DenseForestArea"));SetRootComponent(Bounds);
 Bounds->SetBoxExtent(FVector(1200,850,600));Bounds->SetCollisionEnabled(ECollisionEnabled::NoCollision);
 Bounds->SetHiddenInGame(true);Bounds->ShapeColor=FColor(50,170,130);
}
float APokeMonsterForestCameraZone::TargetAmount(FVector P,FVector B,float Feather)
{
 if(P.ContainsNaN()||B.ContainsNaN()||!FMath::IsFinite(Feather)||Feather<=0||B.X<=0||B.Y<=0||B.Z<=0)return 0;
 const float Outside=FMath::Max3(FMath::Abs(P.X)-B.X,FMath::Abs(P.Y)-B.Y,FMath::Abs(P.Z)-B.Z);
 return 1.f-FMath::Clamp(Outside/Feather,0.f,1.f);
}
float APokeMonsterForestCameraZone::SmoothAmount(float T){T=FMath::Clamp(T,0.f,1.f);return T*T*(3.f-2.f*T);}
void APokeMonsterForestCameraZone::Restore()
{
 if(Arm.IsValid()){Arm->TargetArmLength=OriginalArmLength;Arm->RemoveTickPrerequisiteActor(this);}
 if(Visibility.IsValid())Visibility->DenseCanopyAmount=0.f;
 Arm.Reset();Visibility.Reset();Viewer.Reset();CurrentAmount=0;
}
void APokeMonsterForestCameraZone::Tick(float Dt)
{
 Super::Tick(Dt);APawn* P=UGameplayStatics::GetPlayerPawn(this,0);
 if(Viewer.Get()!=P){Restore();if(P){Viewer=P;Arm=P->FindComponentByClass<USpringArmComponent>();Visibility=P->FindComponentByClass<UPokeMonsterCameraVisibilityComponent>();if(Arm.IsValid()){OriginalArmLength=Arm->TargetArmLength;Arm->AddTickPrerequisiteActor(this);}}}
 if(!P||!Arm.IsValid()||!Visibility.IsValid())return;
 if(const auto* GI=GetGameInstance())if(const auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>())if(E->IsEncounterActive())return;
 const float Target=bEnabled?TargetAmount(GetActorTransform().InverseTransformPosition(P->GetActorLocation()),Bounds->GetUnscaledBoxExtent(),EdgeFeatherCm):0.f;
 CurrentAmount=FMath::FInterpConstantTo(CurrentAmount,Target,FMath::Max(0.f,Dt),1.f/FMath::Max(.2f,TransitionSeconds));
 const float Smooth=SmoothAmount(CurrentAmount);
 // Exact restoration at zero avoids drift and preserves other interior-camera ownership outside this zone.
 if(Smooth>0.f)Arm->TargetArmLength=FMath::Lerp(OriginalArmLength,FMath::Clamp(LocalArmLengthCm,1200.f,OriginalArmLength),Smooth);
 else if(CurrentAmount==0.f&&Visibility->DenseCanopyAmount>0.f)Arm->TargetArmLength=OriginalArmLength;
 Visibility->DenseCanopyAmount=Smooth;
}
void APokeMonsterForestCameraZone::EndPlay(const EEndPlayReason::Type Reason){Restore();Super::EndPlay(Reason);}
