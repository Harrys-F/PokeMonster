#include "PokeMonsterVisibleWildCreatureActor.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "Camera/PlayerCameraManager.h"
#include "Components/SkeletalMeshComponent.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"

#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Components/SphereComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "PaperSprite.h"
#include "PaperSpriteComponent.h"
#include "UObject/ConstructorHelpers.h"

APokeMonsterVisibleWildCreatureActor::APokeMonsterVisibleWildCreatureActor()
{
	OverworldMovement = CreateDefaultSubobject<UPokeMonsterCreatureRoamingComponent>(TEXT("OverworldMovement"));
	AddTickPrerequisiteComponent(OverworldMovement);
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = false;
	Body = CreateDefaultSubobject<UCapsuleComponent>(TEXT("Body"));
	SetRootComponent(Body);
	Body->InitCapsuleSize(38.f, 60.f);
	Body->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	Body->SetCollisionResponseToAllChannels(ECR_Ignore);
	Body->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
	Body->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	ContactRange = CreateDefaultSubobject<USphereComponent>(TEXT("ContactRange"));
	ContactRange->SetupAttachment(Body);
	ContactRange->InitSphereRadius(68.f);
	ContactRange->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	ContactRange->SetCollisionResponseToAllChannels(ECR_Ignore);
	ContactRange->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	Sprite = CreateDefaultSubobject<UPaperSpriteComponent>(TEXT("CreatureSprite"));
	Sprite->SetupAttachment(Body);
	Sprite->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Sprite->SetCastShadow(false);
	Sprite->SetRelativeLocation(FVector(0.f, 0.f, -45.f));
	static ConstructorHelpers::FObjectFinder<UPaperSprite> Placeholder(TEXT("/Game/Environment/Prototype2D/Sprites/S_Bush.S_Bush"));
	if (Placeholder.Succeeded()) Sprite->SetSprite(Placeholder.Object);
	Label = CreateDefaultSubobject<UTextRenderComponent>(TEXT("WildLabel"));
	Label->SetupAttachment(Body);
	Label->SetRelativeLocation(FVector(0.f, 0.f, 85.f));
	Label->SetRelativeRotation(FRotator(0.f, 180.f, 0.f));
	Label->SetText(FText::FromString(TEXT("Wild")));
	Label->SetHorizontalAlignment(EHTA_Center);
	Label->SetWorldSize(24.f);
	Label->SetTextRenderColor(FColor(235, 228, 187));
	Label->SetCollisionEnabled(ECollisionEnabled::NoCollision);Label->SetCastShadow(false);
	Profile = TSoftObjectPtr<UPokeMonsterEncounterProfile>(FSoftObjectPath(TEXT("/Game/Data/Encounters/DA_DevWild.DA_DevWild")));
	Tags.Add(TEXT("VisibleWildEncounter"));
}

void APokeMonsterVisibleWildCreatureActor::BeginPlay()
{
	Super::BeginPlay();
 InitialSpawnTransform=GetActorTransform();
 if(auto* Species=VisualSpecies.LoadSynchronous())
 {
  Visual=GetWorld()->SpawnActor<APokeMonsterCreatureVisualActor>();
  if(Visual&&Visual->SetSpecies(Species))
  {
   Visual->AttachToActor(this,FAttachmentTransformRules::KeepRelativeTransform);Visual->AddTickPrerequisiteActor(this);
   Visual->SetActorRelativeLocation(FVector(0,0,-Body->GetScaledCapsuleHalfHeight()));
   UpdateVisualGround();Sprite->SetVisibility(false);Label->SetVisibility(false);SetActorTickEnabled(true);
   OverworldMovement->Configure(Species, Body->GetScaledCapsuleHalfHeight(), Body->GetScaledCapsuleRadius(), Body->GetScaledCapsuleHalfHeight(), nullptr, Seed);
   OverworldMovement->SetComponentTickEnabled(bAmbientMotion);Visual->SetGroundHoverContext(OverworldMovement);
  }
  else if(Visual){Visual->Destroy();Visual=nullptr;}
 }
	ContactRange->OnComponentBeginOverlap.AddDynamic(this, &APokeMonsterVisibleWildCreatureActor::OnContact);
	if (UGameInstance* Instance = GetGameInstance())
		if (UPokeMonsterEncounterSubsystem* Encounters = Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>())
		{
			Encounters->OnEncounterEnded.AddUniqueDynamic(this, &APokeMonsterVisibleWildCreatureActor::OnEncounterFinished);
			Encounters->OnPersistentStateRestored.AddUniqueDynamic(this, &APokeMonsterVisibleWildCreatureActor::RefreshPersistentState);
			RefreshPersistentState();
		}
 SpawnGroup();
}

void APokeMonsterVisibleWildCreatureActor::RefreshPersistentState()
{
	const UGameInstance* Instance = GetGameInstance();
	const auto* Encounters = Instance ? Instance->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const bool Reactivating=bDeactivated||LifeState!=EPokeMonsterWildLifeState::Active;
 bDeactivated = bDeactivateAfterVictory && Encounters && Encounters->IsEncounterCompleted(EncounterId);
 LifeState=bDeactivated?EPokeMonsterWildLifeState::Removed:EPokeMonsterWildLifeState::Active;
 if(bDeactivated){RemoveWildPresentation();return;}
 // An explicit load of a pre-victory snapshot reactivates the map spawn, not the
 // old off-screen escape position outside the habitat. Normal fleeing never teleports.
 if(Reactivating)
 {
  SetActorTransform(InitialSpawnTransform,false);
  if(const auto* Species=VisualSpecies.LoadSynchronous())
  {
   OverworldMovement->Configure(Species,Body->GetScaledCapsuleHalfHeight(),Body->GetScaledCapsuleRadius(),Body->GetScaledCapsuleHalfHeight(),nullptr,Seed);
   if(Visual)Visual->SetSpecies(Species);
  }
  EncounterReadyAt=GetWorld()->GetTimeSeconds()+1.f;bAwaitSeparation=true;bWasWarning=false;
 }
 SetActorTickEnabled(true);if(Visual){Visual->SetActorTickEnabled(true);Visual->Mesh->SetComponentTickEnabled(true);}
 OverworldMovement->CancelDefeatEscape();
	SetActorHiddenInGame(bDeactivated);
	if(Visual)Visual->SetActorHiddenInGame(bDeactivated);
	SetActorEnableCollision(!bDeactivated);
	OverworldMovement->SetComponentTickEnabled(!bDeactivated && bAmbientMotion && Visual && Visual->Presentation);
}

bool APokeMonsterVisibleWildCreatureActor::IsReady(const APokeMonsterPlayerCharacter* Player) const
{
 const auto* GI=GetGameInstance(); const auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 const auto* Checkpoint=GI?GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>():nullptr;
 return Player && LifeState==EPokeMonsterWildLifeState::Active && !bDeactivated && E && !E->IsEncounterActive()
  && !Player->IsOverworldInputLocked() && !(Checkpoint&&Checkpoint->IsReturningFromDefeat())
  && !Profile.IsNull() && GetWorld()->GetTimeSeconds()>=EncounterReadyAt
  && (!bAmbientMotion||OverworldMovement->CanReengage());
}
bool APokeMonsterVisibleWildCreatureActor::CanInteract_Implementation(APawn* Interactor) const
{
 const auto* Player=Cast<APokeMonsterPlayerCharacter>(Interactor);
 if(!IsReady(Player)||!FPokeMonsterCreatureBehavior::CanInitiate(OverworldMovement->GetBehaviorProfile(),false,true,false))return false;
 if(FVector::Dist2D(Player->GetActorLocation(),GetActorLocation())>Player->GetInteractionRange()+Body->GetScaledCapsuleRadius()
  ||FMath::Abs(Player->GetActorLocation().Z-GetActorLocation().Z)>120.f)return false;
 FCollisionQueryParams Q(SCENE_QUERY_STAT(WildChallengeSight),false,Player);Q.AddIgnoredActor(this);if(Visual)Q.AddIgnoredActor(Visual);
 FHitResult Hit;return !GetWorld()->LineTraceSingleByChannel(Hit,Player->GetActorLocation(),GetActorLocation(),ECC_Visibility,Q);
}
void APokeMonsterVisibleWildCreatureActor::Interact_Implementation(APawn* Interactor)
{
 TryStart(Cast<APokeMonsterPlayerCharacter>(Interactor));
}
bool APokeMonsterVisibleWildCreatureActor::IsTouchingPlayer(const APokeMonsterPlayerCharacter* Player) const
{
 if(!Player)return false; const auto* Other=Player->GetCapsuleComponent();if(!Other)return false;
 // Capsule surfaces, not the old 68-cm proximity sphere. 2 cm accommodates CharacterMovement skin.
 const FVector A=Body->GetComponentLocation(),B=Other->GetComponentLocation();
 const float AH=FMath::Max(0.f,Body->GetScaledCapsuleHalfHeight()-Body->GetScaledCapsuleRadius());
 const float BH=FMath::Max(0.f,Other->GetScaledCapsuleHalfHeight()-Other->GetScaledCapsuleRadius());
 const float ZGap=FMath::Max(0.f,FMath::Abs(A.Z-B.Z)-AH-BH);
 return FVector::DistSquared2D(A,B)+ZGap*ZGap<=FMath::Square(Body->GetScaledCapsuleRadius()+Other->GetScaledCapsuleRadius()+2.f);
}
void APokeMonsterVisibleWildCreatureActor::OnContact(UPrimitiveComponent*, AActor* OtherActor,UPrimitiveComponent*,int32,bool,const FHitResult&)
{
 TryStart(Cast<APokeMonsterPlayerCharacter>(OtherActor),true);
}
bool APokeMonsterVisibleWildCreatureActor::TryStart(APokeMonsterPlayerCharacter* Player,bool Contact)
{
 if(!IsReady(Player)||!FPokeMonsterCreatureBehavior::CanInitiate(OverworldMovement->GetBehaviorProfile(),Contact,!Contact,false))return false;
 if(Contact?bAwaitSeparation||!IsTouchingPlayer(Player):!CanInteract_Implementation(Player))return false;
 auto* E=Player->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();auto* Loaded=Profile.LoadSynchronous();
 const bool Started=Loaded&&E->EnsureDevPlayerParty()&&E->StartWildEncounter(Loaded,Context,EPokeMonsterEncounterSource::VisibleCreature,Player,this,Seed,EncounterId);
 if(Started)OverworldMovement->SetMovementPaused(true);
 return Started;
}
void APokeMonsterVisibleWildCreatureActor::RemoveWildPresentation()
{
 bDeactivated=true;LifeState=EPokeMonsterWildLifeState::Removed;
 SetActorHiddenInGame(true);if(Visual)Visual->SetActorHiddenInGame(true);
 SetActorEnableCollision(false);OverworldMovement->SetComponentTickEnabled(false);SetActorTickEnabled(false);
 // Keep the tiny completed source actor for persistent-state restore; no visible mesh tick/collision remains.
 if(Visual){Visual->SetActorTickEnabled(false);Visual->Mesh->SetComponentTickEnabled(false);}
}
void APokeMonsterVisibleWildCreatureActor::OnEncounterFinished(const FPokeMonsterEncounterEndData& Result)
{
 if(Result.SourceActor!=this)return;
 OverworldMovement->NotifyEncounterEnded();OverworldMovement->SetMovementPaused(false);
 EncounterReadyAt=GetWorld()->GetTimeSeconds()+OverworldMovement->GetBehaviorProfile().EncounterCooldown;bAwaitSeparation=true;
 if(!bDeactivateAfterVictory)return;
 if(Result.Outcome==EPokeMonsterEncounterOutcome::Captured){RemoveWildPresentation();return;}
 if(Result.Outcome!=EPokeMonsterEncounterOutcome::Victory)return;
 if(Result.Kind!=EPokeMonsterEncounterKind::Wild||Result.PresentationMode!=EPokeMonsterBattlePresentationMode::ClassicBattle)
 {RemoveWildPresentation();return;}
 bDeactivated=true;LifeState=EPokeMonsterWildLifeState::Recovering;RecoveryRemaining=.9f;OffscreenSeconds=0;
 SetActorHiddenInGame(false);if(Visual){Visual->SetActorHiddenInGame(false);Visual->PlayReaction(EPokeMonsterCreatureClip::Hit);}
 OverworldMovement->SetMovementPaused(true);SetActorTickEnabled(true);
}
FString APokeMonsterVisibleWildCreatureActor::GetChallengeName() const
{
 const auto* Species=VisualSpecies.LoadSynchronous();return Species?Species->GetDisplayName().ToString():TEXT("Wildes Pokémon");
}
bool APokeMonsterVisibleWildCreatureActor::IsOutsidePlayerView() const
{
 const auto* PC=UGameplayStatics::GetPlayerController(this,0);if(!PC||!PC->PlayerCameraManager||!Visual)return false;
 int32 Width=0,Height=0;PC->GetViewportSize(Width,Height);if(Width<=0||Height<=0)return false;
 FVector Origin,Extent;Visual->GetActorBounds(false,Origin,Extent);
 FVector2D Min(DBL_MAX,DBL_MAX),Max(-DBL_MAX,-DBL_MAX);bool AnyFront=false;
 for(int32 X:{-1,1})for(int32 Y:{-1,1})for(int32 Z:{-1,1})
 {
  FVector2D Screen;const FVector Corner=Origin+Extent*FVector(X,Y,Z);
  if(PC->ProjectWorldLocationToScreen(Corner,Screen))
  {AnyFront=true;Min.X=FMath::Min(Min.X,Screen.X);Min.Y=FMath::Min(Min.Y,Screen.Y);Max.X=FMath::Max(Max.X,Screen.X);Max.Y=FMath::Max(Max.Y,Screen.Y);}
 }
 return !AnyFront||Max.X < -96 || Max.Y < -96 || Min.X > Width+96 || Min.Y > Height+96;
}
void APokeMonsterVisibleWildCreatureActor::SpawnGroup()
{
 if(GroupSize<=1||EncounterId.IsNone()||!bAmbientMotion||!Visual)return;
 const FVector Ground=GetActorLocation()-FVector(0,0,Body->GetScaledCapsuleHalfHeight());
 for(int32 I=1;I<FMath::Clamp(GroupSize,1,4);++I)
 {
  const FName Id(*FString::Printf(TEXT("%s_Group_%d"),*EncounterId.ToString(),I));bool Exists=false;
  for(TActorIterator<APokeMonsterVisibleWildCreatureActor> It(GetWorld());It;++It)if(It->EncounterId==Id){Exists=true;break;}
  if(Exists)continue;
  FVector Spot;bool Found=false;
  for(int32 Try=0;Try<12;++Try)
  {
   const float Angle=(I*137.5f+Try*30.f)*PI/180;
   const FVector Target=Ground+FVector(FMath::Cos(Angle),FMath::Sin(Angle),0)*FMath::Clamp(GroupSpacing,120.f,400.f);
   if(OverworldMovement->ProjectWalkable(Target,Spot)&&OverworldMovement->CanTraverse(Ground,Spot)){Found=true;break;}
  }
  if(!Found){UE_LOG(LogTemp,Warning,TEXT("Wild group %s: no safe member position for %d"),*EncounterId.ToString(),I);continue;}
  const FTransform Transform(FRotator(0,I*113.f,0),Spot+FVector(0,0,FMath::Max(60.f,Body->GetScaledCapsuleHalfHeight())));
  auto* Member=GetWorld()->SpawnActorDeferred<APokeMonsterVisibleWildCreatureActor>(GetClass(),Transform,nullptr,nullptr,ESpawnActorCollisionHandlingMethod::DontSpawnIfColliding);
  if(!Member)continue;
  Member->Body->SetCapsuleSize(Body->GetUnscaledCapsuleRadius(),Body->GetUnscaledCapsuleHalfHeight());
  Member->Profile=Profile;Member->VisualSpecies=VisualSpecies;Member->Context=Context;Member->EncounterId=Id;Member->Seed=Seed+I*7919;
  Member->bAmbientMotion=true;Member->bDeactivateAfterVictory=bDeactivateAfterVictory;
  Member->OverworldMovement->bOverrideBehavior=OverworldMovement->bOverrideBehavior;Member->OverworldMovement->BehaviorOverride=OverworldMovement->BehaviorOverride;
  Member->OverworldMovement->HabitatRadiusOverride=OverworldMovement->HabitatRadiusOverride;Member->OverworldMovement->HabitatHalfExtent=OverworldMovement->HabitatHalfExtent;
  FTransform Final=Transform;Final.SetLocation(Spot+FVector(0,0,Body->GetScaledCapsuleHalfHeight()));
  UGameplayStatics::FinishSpawningActor(Member,Final);
  if(Member->Visual)Member->Visual->IdlePhaseOffset=I*.371f;
 }
}

void APokeMonsterVisibleWildCreatureActor::EndPlay(const EEndPlayReason::Type Reason)
{
 if(Visual)Visual->Destroy();Super::EndPlay(Reason);
}
void APokeMonsterVisibleWildCreatureActor::Tick(float Delta)
{
 Super::Tick(Delta);
 if(Visual&&Visual->Presentation)UpdateVisualGround();
 auto* Player=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));
 const auto* E=GetGameInstance()?GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 if(E&&E->IsEncounterActive())return;
 if(LifeState==EPokeMonsterWildLifeState::Recovering)
 {
  RecoveryRemaining-=Delta;
  if(RecoveryRemaining<=0){LifeState=EPokeMonsterWildLifeState::Escaping;
   if(!OverworldMovement->BeginDefeatEscape()){LifeState=EPokeMonsterWildLifeState::WaitingForExit;}}
 }
 if(LifeState==EPokeMonsterWildLifeState::Escaping||LifeState==EPokeMonsterWildLifeState::WaitingForExit)
 {
  LifeState=OverworldMovement->bEscapeBlocked?EPokeMonsterWildLifeState::WaitingForExit:LifeState;
  if(OverworldMovement->bEscapingDefeat&&!OverworldMovement->bEscapeBlocked)LifeState=EPokeMonsterWildLifeState::Escaping;
  OffscreenSeconds=IsOutsidePlayerView()?OffscreenSeconds+Delta:0;
  if(OffscreenSeconds>=.4f && (OverworldMovement->EscapeElapsed>=1.5f || LifeState==EPokeMonsterWildLifeState::WaitingForExit))RemoveWildPresentation();
  return;
 }
 if(LifeState!=EPokeMonsterWildLifeState::Active||bDeactivated)return;
 if(bAwaitSeparation&&Player&&FVector::Dist2D(GetActorLocation(),Player->GetActorLocation())>Body->GetScaledCapsuleRadius()+Player->GetCapsuleComponent()->GetScaledCapsuleRadius()+25.f)bAwaitSeparation=false;
 const bool Warning=OverworldMovement->BehaviorState==EPokeMonsterOverworldState::Warning;
 if(Warning&&!bWasWarning&&Visual)Visual->PlayReaction(EPokeMonsterCreatureClip::Attack);
 bWasWarning=Warning;
 if(IsTouchingPlayer(Player))TryStart(Player,true);
}

void APokeMonsterVisibleWildCreatureActor::SuppressPresentation(bool Suppressed)
{
 if(Suppressed)Label->SetVisibility(false);
 if(Visual)Visual->SetActorHiddenInGame(Suppressed||bDeactivated);
 else Sprite->SetVisibility(!Suppressed&&!bDeactivated);
}

void APokeMonsterVisibleWildCreatureActor::UpdateVisualGround()
{
 if(!Visual||!Visual->Presentation)return;FHitResult Hit;
 FCollisionQueryParams Params(SCENE_QUERY_STAT(WildCreatureVisualGround),true);Params.AddIgnoredActor(this);Params.AddIgnoredActor(Visual);
 if(auto* P=UGameplayStatics::GetPlayerPawn(this,0))Params.AddIgnoredActor(P);
 const FVector P=GetActorLocation();
 if(GetWorld()->LineTraceSingleByChannel(Hit,P+FVector(0,0,100),P-FVector(0,0,220),ECC_Visibility,Params))
  Visual->SetActorRelativeLocation(FVector(0,0,Hit.ImpactPoint.Z-P.Z-Visual->Presentation->GroundOffsetCm));
}

void APokeMonsterVisibleWildCreatureActor::SetChallengeFocused(bool Focused)
{
 auto* Player=UGameplayStatics::GetPlayerPawn(this,0);
 const bool Show=Focused&&CanInteract_Implementation(Player);
 Label->SetVisibility(Show);if(!Show)return;
 Label->SetText(FText::FromString(TEXT("▼")));Label->SetWorldSize(15.f);
 if(const auto* PC=UGameplayStatics::GetPlayerController(this,0))if(PC->PlayerCameraManager)
  Label->SetWorldRotation((PC->PlayerCameraManager->GetCameraLocation()-Label->GetComponentLocation()).Rotation());
}
