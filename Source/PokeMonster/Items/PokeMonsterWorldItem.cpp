#include "PokeMonsterWorldItem.h"
#include "PokeMonsterItemData.h"
#include "PokeMonsterInventorySubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "UObject/ConstructorHelpers.h"

APokeMonsterWorldItem::APokeMonsterWorldItem()
{
 PrimaryActorTick.bCanEverTick=false;
 Mesh=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PickupMesh"));SetRootComponent(Mesh);
 static ConstructorHelpers::FObjectFinder<UStaticMesh> Crate(TEXT("/Game/Environment/WestlandAssetLibrary/Meshes/Village/SM_WLA_Crate_A.SM_WLA_Crate_A"));
 if(Crate.Succeeded())Mesh->SetStaticMesh(Crate.Object);
 Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);Mesh->SetCastShadow(false);
 Mesh->SetRelativeScale3D(FVector(.32f));
}
void APokeMonsterWorldItem::BeginPlay()
{
 Super::BeginPlay();
 if(auto* Data=Item.LoadSynchronous())if(auto* Model=Data->GetWorldMesh())Mesh->SetStaticMesh(Model);
 if(auto* GI=GetGameInstance())if(auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>())E->OnPersistentStateRestored.AddUniqueDynamic(this,&APokeMonsterWorldItem::RefreshCollectedState);
 RefreshCollectedState();
}
void APokeMonsterWorldItem::EndPlay(const EEndPlayReason::Type Reason)
{
 if(auto* GI=GetGameInstance())if(auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>())E->OnPersistentStateRestored.RemoveDynamic(this,&APokeMonsterWorldItem::RefreshCollectedState);
 Super::EndPlay(Reason);
}
void APokeMonsterWorldItem::RefreshCollectedState()
{
 const auto* GI=GetGameInstance();const auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 const bool Hidden=PickupId.IsNone()||!Item.LoadSynchronous()||(E&&E->IsEncounterCompleted(PickupId));
 SetActorHiddenInGame(Hidden);
}
bool APokeMonsterWorldItem::CanInteract_Implementation(APawn* Interactor) const
{
 const auto* Player=Cast<APokeMonsterPlayerCharacter>(Interactor);
 const auto* E=GetGameInstance()?GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 const auto* Data=Item.LoadSynchronous();
 if(bBusy||IsHidden()||!Player||Player->IsOverworldInputLocked()||!Data||!Data->IsConfigured()||Quantity<=0||PickupId.IsNone()||!E||E->IsEncounterActive()||E->IsEncounterCompleted(PickupId))return false;
 if(FVector::Dist2D(Player->GetActorLocation(),GetActorLocation())>220.f||FMath::Abs(Player->GetActorLocation().Z-GetActorLocation().Z)>120.f)return false;
 FCollisionQueryParams Q(SCENE_QUERY_STAT(ItemInteraction),false,Player);Q.AddIgnoredActor(this);FHitResult Hit;
 return !GetWorld()->LineTraceSingleByChannel(Hit,Player->GetActorLocation(),GetActorLocation()+FVector(0,0,20),ECC_Visibility,Q);
}
void APokeMonsterWorldItem::Interact_Implementation(APawn* Interactor)
{
 if(!CanInteract_Implementation(Interactor))return;
 TGuardValue<bool> Guard(bBusy,true);
 if(auto* I=GetGameInstance()->GetSubsystem<UPokeMonsterInventorySubsystem>())if(I->CollectItem(Item.LoadSynchronous(),Quantity,PickupId))RefreshCollectedState();
}
