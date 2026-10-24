#include "PokeMonsterCreatureRoamingComponent.h"
#include "../../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "PokeMonsterCreaturePath.h"
#include "../PokeMonsterCreatureSpeciesData.h"
#include "../PokeMonsterCreaturePresentation.h"
#include "../../Characters/PokeMonsterPlayerCharacter.h"
#include "../../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Components/PrimitiveComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "../../World/PokeMonsterBuildingCutaway.h"
#include "Kismet/GameplayStatics.h"

UPokeMonsterCreatureRoamingComponent::UPokeMonsterCreatureRoamingComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.bStartWithTickEnabled = false;
	// Translate every rendered game frame; animation speed must not alternate between 0 and double speed.
	PrimaryComponentTick.TickInterval = 0.f;
}
void UPokeMonsterCreatureRoamingComponent::Configure(const UPokeMonsterCreatureSpeciesData* Species,
	float RootGroundOffset, float Radius, float HalfHeight, AActor* Follow, int32 Seed)
{
	SetComponentTickEnabled(false); bReady = false; bPresentationHold = false; PresentationHoverHeight=0.f;
	if (!Species || !Species->Overworld.IsValid() || !FMath::IsFinite(RootGroundOffset)
		|| !FMath::IsFinite(Radius) || Radius <= 0 || !FMath::IsFinite(HalfHeight) || HalfHeight <= 0
		|| !FMath::IsFinite(HabitatRadiusOverride) || HabitatRadiusOverride < 0
		|| (HabitatRadiusOverride > 0 && (HabitatRadiusOverride < 150 || HabitatRadiusOverride > 5000))
		|| HabitatHalfExtent.ContainsNaN() || HabitatHalfExtent.X < 0 || HabitatHalfExtent.Y < 0) return;
	Presentation = Species->GetVisuals().Presentation.LoadSynchronous();
	if (!Presentation || !Presentation->GetValidationErrors().IsEmpty()) return;
	Settings = Species->Overworld;
	if(bOverrideBehavior) { if(!BehaviorOverride.IsValid()) return; Settings.Behavior=BehaviorOverride; }
	BehaviorState=EPokeMonsterOverworldState::Rest; WarningElapsed=CooldownRemaining=ReactionRemaining=InterestRemaining=0; bTerritoryArmed=true; bEscapingDefeat=bEscapeBlocked=false; EscapeElapsed=EscapeReplan=EscapeStalled=0;
	Offset = RootGroundOffset; BodyRadius = FMath::Max(Radius, Settings.BodyRadius);
	// Wide visual appendages may need more navigation clearance than the contact capsule.
	BodyHalfHeight = FMath::Max(HalfHeight, BodyRadius); FollowTarget = Follow;
	HabitatOrigin = GetOwner()->GetActorLocation() - FVector(0, 0, Offset);
	Buildings.Reset();
	for (TActorIterator<APokeMonsterBuildingCutaway> It(GetWorld()); It; ++It) Buildings.Add(*It);
	// Some art props intentionally have no gameplay collision. Avoid their solid trunk/rock
 // cores locally, without changing landscape/player collision or treating foliage as a wall.
 DecorativeObstacles.Reset(); HoverObstacles.Reset();
 for(TActorIterator<AActor> It(GetWorld());It;++It)
 {
  TInlineComponentArray<UStaticMeshComponent*> Components(*It);
  for(const auto* Mesh:Components)
  {
   if(!Mesh->GetStaticMesh()||(Mesh->GetCollisionResponseToChannel(ECC_Pawn)==ECR_Block&&Mesh->IsCollisionEnabled()))continue;
   const FString Asset=Mesh->GetStaticMesh()->GetPathName();
   const bool Tree=Asset.Contains(TEXT("/Trees/")),Rock=Asset.Contains(TEXT("Boulder"));if(!Tree&&!Rock)continue;
   auto Add=[&](const FTransform& Transform)
   {
    const FBox Local=Mesh->GetStaticMesh()->GetBoundingBox(),World=Local.TransformBy(Transform);
    HoverObstacles.Add(World);
    if(Tree)
    {
     const FVector Bottom=Transform.TransformPosition(FVector(0,0,Local.Min.Z));
     const float Radius=FMath::Clamp(FMath::Min(World.GetExtent().X,World.GetExtent().Y)*.12f,12.f,65.f);
     DecorativeObstacles.Add(FBox(Bottom-FVector(Radius,Radius,5),Bottom+FVector(Radius,Radius,FMath::Min(250.f,World.GetSize().Z*.4f))));
    }
    else if(World.GetSize().Z>35.f)DecorativeObstacles.Add(World);
   };
   if(const auto* Instances=Cast<UInstancedStaticMeshComponent>(Mesh))
   {for(int32 I=0;I<Instances->GetInstanceCount();++I){FTransform Transform;if(Instances->GetInstanceTransform(I,Transform,true))Add(Transform);}}
   else Add(Mesh->GetComponentTransform());
  }
 }
 Random.Initialize(Seed); DistanceTravelled = 0.f; SuccessfulPlans = BlockedSteps = RejectedTargets = 0;
	CurrentSpeed = AngularVelocity = 0.f; RecentGoals.Reset();
	for (int32& Visits : SectorVisits) Visits=0;
	Path.Reset(); bPaused = false; bRecalling = false; bReady = true; BeginPause();
	SetComponentTickEnabled(true);
}
void UPokeMonsterCreatureRoamingComponent::SetMovementPaused(bool Paused)
{
	if (bPaused != Paused) { Path.Reset(); PauseRemaining = .2f; ReplanRemaining = 0.f; }
	bPaused = Paused; if(Paused) CurrentSpeed=AngularVelocity=0.f;
}
FCollisionQueryParams UPokeMonsterCreatureRoamingComponent::Query() const
{
	FCollisionQueryParams Q(SCENE_QUERY_STAT(CreatureOverworldGround), false);
	Q.AddIgnoredActor(GetOwner());
    if (BiomeHabitat) BiomeHabitat->IgnorePlayerWaterBarriers(Q);
	TArray<AActor*> Attached; GetOwner()->GetAttachedActors(Attached);
	for (AActor* Actor : Attached) Q.AddIgnoredActor(Actor);
	if (FollowTarget.IsValid()) Q.AddIgnoredActor(FollowTarget.Get());
	// Escape uses the actual body-radius guard below, rather than trapping the contact
	// start inside the larger silhouette navigation buffer. All world checks remain active.
	if(bEscapingDefeat)Q.AddIgnoredActor(UGameplayStatics::GetPlayerPawn(this,0));
	return Q;
}
bool UPokeMonsterCreatureRoamingComponent::IsInsideHabitat(const FVector& Point) const
{
	if (!bReady || Point.ContainsNaN()) return false;
    if (BiomeHabitat && !BiomeHabitat->ContainsFootprint(Point, BodyRadius)) return false;
	const FVector BodyPoint = Point + FVector(0,0,BodyHalfHeight);
	for (const auto& Weak : Buildings)
	{
		const auto* Building = Weak.Get(); if (!Building) continue;
		const bool PointInside = Building->IsViewerInside(BodyPoint);
		if (!FollowTarget.IsValid())
        {
            if (BiomeHabitat && BiomeHabitat->InteriorOwner==Building)
            { if (!Building->IsViewerInRelocatedRoom(BodyPoint)) return false; }
            else if (PointInside) return false;
            continue;
        }
		const FVector Viewer = FollowTarget->GetActorLocation();
		if (Building->IsViewerInRelocatedRoom(Viewer))
		{ if (!Building->IsViewerInRelocatedRoom(BodyPoint)) return false; }
		else if (Building->IsViewerInside(Viewer))
		{ if (!PointInside || Building->IsViewerInRelocatedRoom(BodyPoint)) return false; }
		else if (PointInside) return false;
	}
	if (FollowTarget.IsValid())
		return FVector::DistSquared2D(Point, FollowTarget->GetActorLocation())
			<= FMath::Square(Settings.MaximumActiveDistance);
	if(bEscapingDefeat)return FVector::DistSquared2D(Point,HabitatOrigin)<=FMath::Square(6000.f);
	const float Radius = HabitatRadiusOverride > 0 ? HabitatRadiusOverride : Settings.RoamRadius;
	const FVector D = Point - HabitatOrigin;
	return D.SizeSquared2D() <= FMath::Square(Radius)
		&& (HabitatHalfExtent.X <= 0 || FMath::Abs(D.X) <= HabitatHalfExtent.X)
		&& (HabitatHalfExtent.Y <= 0 || FMath::Abs(D.Y) <= HabitatHalfExtent.Y);
}
bool UPokeMonsterCreatureRoamingComponent::ProjectWalkable(const FVector& Point, FVector& Ground) const
{
	UWorld* W = GetWorld(); if (!W || !IsInsideHabitat(Point)) return false;
    if (BiomeHabitat) return BiomeHabitat->ProjectFoot(Point, BodyRadius, BodyHalfHeight, Query(), Ground);
	const auto Q = Query(); FHitResult Hit;
	if (!W->LineTraceSingleByChannel(Hit, Point + FVector(0, 0, Settings.MaxStepHeight + 55.f),
		Point - FVector(0, 0, 100.f), ECC_Visibility, Q) || Hit.ImpactNormal.Z < .75f) return false;
	if (!Hit.GetComponent() || Hit.GetComponent()->GetCollisionResponseToChannel(ECC_Pawn) != ECR_Block) return false;
	const AActor* Surface = Hit.GetActor();
	if (Surface && (Surface->ActorHasTag(TEXT("CreatureNoWalk"))
		|| (!Settings.bCanEnterWater && Surface->ActorHasTag(TEXT("Water"))))) return false;
	Ground = Hit.ImpactPoint;
 for(const auto& Box:DecorativeObstacles)
 {
  if(Ground.Z+BodyHalfHeight*2 < Box.Min.Z || Ground.Z>Box.Max.Z+Settings.MaxStepHeight)continue;
  if(Ground.X>=Box.Min.X-BodyRadius && Ground.X<=Box.Max.X+BodyRadius && Ground.Y>=Box.Min.Y-BodyRadius && Ground.Y<=Box.Max.Y+BodyRadius)return false;
 }
 return !W->OverlapBlockingTestByChannel(Ground + FVector(0, 0, BodyHalfHeight + Settings.MaxStepHeight + 2.f),
		FQuat::Identity, ECC_Pawn, FCollisionShape::MakeCapsule(BodyRadius, BodyHalfHeight), Q);
}
bool UPokeMonsterCreatureRoamingComponent::CanTraverse(const FVector& Start, const FVector& End) const
{
	if (!GetWorld() || !bReady || Start.ContainsNaN() || End.ContainsNaN()) return false;
	if(bEscapingDefeat)if(const auto* Player=UGameplayStatics::GetPlayerPawn(this,0))
	{
	 const auto* Body=GetOwner()->FindComponentByClass<UCapsuleComponent>();
	 const auto* PlayerBody=Player->FindComponentByClass<UCapsuleComponent>();
	 if(!Body||!PlayerBody||!CanSeparateFromContact(Start,End,Player->GetActorLocation(),Body->GetScaledCapsuleRadius()+PlayerBody->GetScaledCapsuleRadius()))return false;
	}
	// Continuous clearance for local decoration cores. Sparse ground samples alone can
 // miss a very short crossing of an expanded rock/trunk corner, then reject each real step.
 for(const auto& Box:DecorativeObstacles)
  if(IsDecorativeSegmentBlocked(Box,Start,End,BodyRadius,BodyHalfHeight,Settings.MaxStepHeight))return false;
 if(PresentationHoverHeight>0.f&&!CanTraverseHoverColumn(Start,End,PresentationHoverHeight,PresentationHoverBounds))return false;
	const auto Q = Query(); FHitResult Obstacle;
	const float Lift = BodyHalfHeight + Settings.MaxStepHeight + 2.f;
	if (GetWorld()->SweepSingleByChannel(Obstacle, Start + FVector(0, 0, Lift),
		End + FVector(0, 0, Lift), FQuat::Identity, ECC_Pawn,
		FCollisionShape::MakeCapsule(BodyRadius, BodyHalfHeight), Q)) return false;
	FVector Previous = Start;
	const int32 Steps = FMath::Max(1, FMath::CeilToInt(FVector::Dist2D(Start, End) / 25.f));
	for (int32 I = 1; I <= Steps; ++I)
	{
		FVector Ground;
		if (!ProjectWalkable(FMath::Lerp(Start, End, static_cast<float>(I) / Steps), Ground)
			|| FMath::Abs(Ground.Z - Previous.Z) > Settings.MaxStepHeight) return false;
		Previous = Ground;
	}
	return true;
}
bool UPokeMonsterCreatureRoamingComponent::Plan(const FVector& Target)
{
	const FVector Start = GetOwner()->GetActorLocation() - FVector(0, 0, Offset);
	FVector Goal;
	if (!ProjectWalkable(Target, Goal)) return false;
	if (!FPokeMonsterCreaturePath::Find(Start, Goal,
		[this](const FVector& P, FVector& G) { return ProjectWalkable(P, G); },
		[this](const FVector& A, const FVector& B) { return CanTraverse(A, B); }, Path)) return false;
	CurrentGoal = Goal; ++SuccessfulPlans; return true;
}
void UPokeMonsterCreatureRoamingComponent::BeginPause()
{
	PauseRemaining = Random.FRandRange(Settings.PauseMinimum, Settings.PauseMaximum)*(FollowTarget.IsValid()?1.f:Settings.Behavior.RestMultiplier);
	AngularVelocity=0.f;
	LookYaw = GetOwner()->GetActorRotation().Yaw + Random.FRandRange(-35.f, 35.f);
	Path.Reset();
}
void UPokeMonsterCreatureRoamingComponent::TickComponent(float Delta, ELevelTick Tick,
	FActorComponentTickFunction* Function)
{
	Super::TickComponent(Delta, Tick, Function);
	AActor* Owner = GetOwner();
	if (!bReady || bPaused || !Owner || Owner->IsHidden() || Delta <= 0.f) return;
 if (bPresentationHold) { CurrentSpeed=AngularVelocity=0.f; return; }
	const auto* GI = GetWorld()->GetGameInstance();
	const auto* E = GI ? GI->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* C = GI ? GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>() : nullptr;
	if ((E && E->IsEncounterActive()) || (C && C->IsReturningFromDefeat())) return;
	const FVector Current = Owner->GetActorLocation() - FVector(0, 0, Offset);
	auto* Player = Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this, 0));
	if (!FollowTarget.IsValid() && Player && (Player->IsOverworldInputLocked()
		))
	{
		Path.Reset(); CurrentSpeed=0.f; PauseRemaining = .6f;
		const float Yaw = (Player->GetActorLocation() - Current).Rotation().Yaw;
		Owner->SetActorRotation(FMath::RInterpConstantTo(Owner->GetActorRotation(), FRotator(0,Yaw,0),Delta,Settings.TurnDegreesPerSecond));
		return;
	}
	float Speed = Settings.WalkSpeedOverride > 0 ? Settings.WalkSpeedOverride : Presentation->WalkSpeed;
	if(bEscapingDefeat)
	{
	 EscapeElapsed+=Delta; EscapeReplan-=Delta; PauseRemaining=0;
	 Speed=FMath::Clamp((Settings.RunSpeedOverride>0?Settings.RunSpeedOverride:Presentation->RunSpeed)*1.5f,25.f,180.f);
	 if(Path.IsEmpty() && EscapeReplan<=0)
	 {
	  if(!PlanEscape(Current,Player)){EscapeStalled+=1.5f; bEscapeBlocked=EscapeStalled>=6.f;}
	  else {EscapeStalled=0; bEscapeBlocked=false;}
	  EscapeReplan=1.5f;
	 }
	 if(Path.IsEmpty()){CurrentSpeed=0;return;}
	}
	else if(!FollowTarget.IsValid())
	{
	 Speed*=Settings.Behavior.WalkMultiplier;
	 if(UpdateBehavior(Delta,Current,Player,Speed)) return;
	}
	ReplanRemaining -= Delta;
	if (FollowTarget.IsValid())
	{
		const float Distance = FVector::Dist2D(Current, FollowTarget->GetActorLocation());
		if (Distance > Settings.RecallDistance || (FollowTarget->GetVelocity().Size2D()>30.f && Distance>Settings.CompanionRoamRadius)) bRecalling = true;
		else if (Distance < 170.f) bRecalling = false;
		BehaviorState=bRecalling?EPokeMonsterOverworldState::Follow:Path.IsEmpty()?EPokeMonsterOverworldState::Rest:EPokeMonsterOverworldState::Wander;
		if (bRecalling)
		{
			const float Run = Settings.RunSpeedOverride > 0 ? Settings.RunSpeedOverride
				: Settings.SprintReferenceSpeed > 0 ? Settings.SprintReferenceSpeed : Presentation->RunSpeed;
			Speed = FMath::Min(Settings.CompanionMaximumSpeed,
				FMath::Max(Run, FollowTarget->GetVelocity().Size2D() + 70.f));
			PauseRemaining = 0;
			if (ReplanRemaining <= 0)
			{
				const FVector Toward = (FollowTarget->GetActorLocation() - Current).GetSafeNormal2D();
				FVector Target = Distance > 900.f ? Current + Toward * 800.f
					: FollowTarget->GetActorLocation() - Toward * 130.f;
				Target.Z = Current.Z; Path.Reset();
				if (!Plan(Target))
				{
					// The point behind a player crossing a bridge can still lie in water.
					// Try reachable ground around the player rather than wandering away.
					for (float Angle : {0.f, 45.f, -45.f, 90.f, -90.f, 135.f, -135.f, 180.f})
					{
						FVector Near = FollowTarget->GetActorLocation() + (-Toward).RotateAngleAxis(Angle,FVector::UpVector)*130.f;
						Near.Z = Current.Z;
						if (FVector::Dist2D(Current,Near) <= 1000.f && Plan(Near)) break;
					}
				}
				ReplanRemaining = 1.f;
			}
		}
	}
	if (PauseRemaining > 0 && !bRecalling)
	{
		CurrentSpeed=0.f; PauseRemaining -= Delta;
		Owner->SetActorRotation(FMath::RInterpConstantTo(Owner->GetActorRotation(), FRotator(0,LookYaw,0),Delta,35.f));
		return;
	}
	if (Path.IsEmpty())
	{
		CurrentSpeed=0.f;
		if (bRecalling || ReplanRemaining > 0 || BehaviorState==EPokeMonsterOverworldState::Approach || BehaviorState==EPokeMonsterOverworldState::Retreat) return;
		const FVector Center = FollowTarget.IsValid() ? FollowTarget->GetActorLocation() : HabitatOrigin;
		const float Radius = FollowTarget.IsValid() ? Settings.CompanionRoamRadius
			: HabitatRadiusOverride > 0 ? HabitatRadiusOverride : Settings.RoamRadius;
		struct FCandidate { FVector Point; float Score; int32 Sector; };
		TArray<FCandidate> Candidates;
		for (int32 Attempt=0; Attempt<16; ++Attempt)
		{
			const float Angle=Random.FRandRange(-PI,PI), Distance=Radius*FMath::Sqrt(Random.FRand());
			FVector Goal=Center+FVector(FMath::Cos(Angle)*Distance,FMath::Sin(Angle)*Distance,0); Goal.Z=Current.Z;
            if (BiomeHabitat && !BiomeHabitat->TravelPoints.IsEmpty())
                Goal = BiomeHabitat->GetActorTransform().TransformPosition(BiomeHabitat->TravelPoints[Random.RandRange(0,BiomeHabitat->TravelPoints.Num()-1)])
                    + FVector(Random.FRandRange(-35,35),Random.FRandRange(-35,35),0);
			if(FVector::Dist2D(Current,Goal)<(FollowTarget.IsValid()?90.f:Settings.MinimumTravel)) continue;
			if(FollowTarget.IsValid() && FVector::Dist2D(Goal,Center)<100.f) continue;
			if(RecentGoals.ContainsByPredicate([&](const FVector& P){return FVector::Dist2D(P,Goal)<Settings.MinimumTravel*.65f;})) continue;
			if(FVector::Dist2D(Current,Goal)>1000.f) Goal=Current+(Goal-Current).GetSafeNormal2D()*1000.f;
			const int32 Sector=FMath::Clamp(FMath::FloorToInt((Angle+PI)/(PI/4)),0,7);
			const float Score=FollowTarget.IsValid()?Random.FRand():4.f/(1+SectorVisits[Sector])+Distance/Radius+Random.FRand()*.4f;
			Candidates.Add({Goal,Score,Sector});
		}
		Candidates.Sort([](const FCandidate& A,const FCandidate& B){return A.Score>B.Score;});
		for(const auto& Candidate:Candidates)
		{
			if(Plan(Candidate.Point))
			{
				if(!FollowTarget.IsValid()) ++SectorVisits[Candidate.Sector];
				RecentGoals.Add(Candidate.Point); if(RecentGoals.Num()>4) RecentGoals.RemoveAt(0);
				break;
			}
			++RejectedTargets;
		}
		if (Path.IsEmpty()) { BeginPause(); ReplanRemaining = 1.f; return; }
	}
	while (!Path.IsEmpty() && FVector::Dist2D(Current, Path[0]) < 1.f) Path.RemoveAt(0);
	if (Path.IsEmpty()) { if (!bRecalling&&!bEscapingDefeat) BeginPause(); return; }
	const FVector Target = Path[0];
	const FVector Direction = (Target - Current).GetSafeNormal2D();
	const float TargetYaw = Direction.Rotation().Yaw;
	const FRotator Rotation(0,AdvanceHeading(Owner->GetActorRotation().Yaw,TargetYaw,AngularVelocity,Settings,Delta),0);
	Owner->SetActorRotation(Rotation);
	// Turn before translating; this avoids diagonal sideways steps at large heading changes.
	if (FMath::Abs(FMath::FindDeltaAngleDegrees(Rotation.Yaw, TargetYaw)) > 35.f) { CurrentSpeed=0.f; return; }
	CurrentSpeed=AdvanceSpeed(CurrentSpeed,Speed,Path.Num()==1?FVector::Dist2D(Current,Target):BIG_NUMBER,FollowTarget.IsValid(),Settings,Delta);
	const FVector Candidate = Current + Direction * FMath::Min(CurrentSpeed * FMath::Min(Delta, .1f), FVector::Dist2D(Current,Target));
	FVector Ground;
	if (!ProjectWalkable(Candidate, Ground) || !CanTraverse(Current, Ground))
	{ ++BlockedSteps; CurrentSpeed=0.f; BeginPause(); ReplanRemaining = .5f; return; }
	const FVector Before = Owner->GetActorLocation(); FHitResult Hit;
	auto* Primitive=Cast<UPrimitiveComponent>(Owner->GetRootComponent());
	const bool IgnoreContact=bEscapingDefeat&&Primitive&&Player&&!Primitive->GetMoveIgnoreActors().Contains(Player);
	if(IgnoreContact)Primitive->IgnoreActorWhenMoving(Player,true);
	Owner->SetActorLocation(Ground + FVector(0,0,Offset), true, &Hit);
	if(IgnoreContact)Primitive->IgnoreActorWhenMoving(Player,false);
	DistanceTravelled += FVector::Dist2D(Before, Owner->GetActorLocation());
	if (Hit.bBlockingHit) { ++BlockedSteps; CurrentSpeed=0.f; BeginPause(); return; }
	if (FVector::Dist2D(Ground, Target) < 1.f)
	{
		Path.RemoveAt(0);
		if (Path.IsEmpty() && !bRecalling&&!bEscapingDefeat) BeginPause();
	}
}

float UPokeMonsterCreatureRoamingComponent::AdvanceSpeed(float Current,float Desired,float Distance,bool Companion,
 const FPokeMonsterCreatureOverworldSettings& Config,float Delta)
{
 if(!FMath::IsFinite(Current)||!FMath::IsFinite(Desired)||!FMath::IsFinite(Distance)||!FMath::IsFinite(Delta)||Delta<=0) return 0.f;
 const float Brake=Companion?Config.CompanionBrakingDeceleration:Config.BrakingDeceleration;
 const float Accel=Companion?Config.CompanionAcceleration:Config.Acceleration;
 const float Target=FMath::Min(FMath::Max(0.f,Desired),FMath::Sqrt(2.f*Brake*FMath::Max(0.f,Distance)));
 return FMath::FInterpConstantTo(FMath::Max(0.f,Current),Target,FMath::Min(Delta,.1f),Target>Current?Accel:Brake);
}
float UPokeMonsterCreatureRoamingComponent::AdvanceHeading(float CurrentYaw,float DesiredYaw,float& Velocity,
 const FPokeMonsterCreatureOverworldSettings& Config,float Delta)
{
 const float Error=FMath::FindDeltaAngleDegrees(CurrentYaw,DesiredYaw),Step=FMath::Clamp(Delta,0.f,.1f);
 if(FMath::Abs(Error)<.05f){Velocity=0;return DesiredYaw;}
 Velocity=FMath::FInterpConstantTo(Velocity,FMath::Clamp(Error*4.f,-Config.TurnDegreesPerSecond,Config.TurnDegreesPerSecond),Step,Config.TurnAcceleration);
 return FRotator::NormalizeAxis(CurrentYaw+FMath::Clamp(Velocity*Step,-FMath::Abs(Error),FMath::Abs(Error)));
}


bool UPokeMonsterCreatureRoamingComponent::PlayerVisible(const APawn* Player) const
{
 if(!Player||!GetWorld())return false;
 FCollisionQueryParams Q=Query();Q.AddIgnoredActor(Player);
 FHitResult Hit;
 return !GetWorld()->LineTraceSingleByChannel(Hit,GetOwner()->GetActorLocation()+FVector(0,0,35),
  Player->GetActorLocation()+FVector(0,0,35),ECC_Visibility,Q);
}
bool UPokeMonsterCreatureRoamingComponent::UpdateBehavior(float Delta,const FVector& Current,const APawn* Player,float& Speed)
{
 using EOverworldState = EPokeMonsterOverworldState;using EOverworldTemperament = EPokeMonsterOverworldTemperament;
 CooldownRemaining=FMath::Max(0.f,CooldownRemaining-Delta);
 const auto& P=Settings.Behavior;
 const float D=Player?FVector::Dist2D(Current,Player->GetActorLocation()):BIG_NUMBER;
 // Leaving the entire response radius is necessary even after the time cooldown has expired.
 if(D>P.DisengageRadius)bTerritoryArmed=true;
 const bool Visible=Player&&D<=P.DisengageRadius&&PlayerVisible(Player);
 const bool Reacting=BehaviorState==EOverworldState::Approach||BehaviorState==EOverworldState::Retreat||BehaviorState==EOverworldState::Observe||BehaviorState==EOverworldState::Warning;
 EOverworldState Next=FPokeMonsterCreatureBehavior::Decide(P,D,Visible,Reacting,CooldownRemaining>0||(P.Temperament==EOverworldTemperament::Territorial&&!bTerritoryArmed));
 // Curiosity alternates observation and approach, rather than following forever.
 InterestRemaining=FMath::Max(0.f,InterestRemaining-Delta);
 if(P.Temperament==EOverworldTemperament::Curious && Next==EOverworldState::Approach && InterestRemaining>0)Next=EOverworldState::Observe;
 if(P.Temperament==EOverworldTemperament::Territorial && BehaviorState==EOverworldState::Approach && Visible && bTerritoryArmed && CooldownRemaining<=0)Next=EOverworldState::Approach;
 if(Next!=BehaviorState)
 {
  Path.Reset();ReactionRemaining=0;WarningElapsed=0;PauseRemaining=0;
  if(BehaviorState==EOverworldState::Approach&&Next==EOverworldState::Observe)InterestRemaining=Random.FRandRange(1.5f,3.5f);
  BehaviorState=Next;
 }
 if(Next==EOverworldState::Warning && BehaviorState==EOverworldState::Warning) WarningElapsed+=Delta;
 if(Next==EOverworldState::Warning && WarningElapsed>=P.WarningSeconds)Next=EOverworldState::Approach;
 // Chasing follows the warning, never starts a battle; only the actor's actual contact gate can.
 if(BehaviorState==EOverworldState::Approach && P.Temperament==EOverworldTemperament::Territorial && Visible && bTerritoryArmed)Next=EOverworldState::Approach;
 if(Next==EOverworldState::Approach && BehaviorState!=Next){BehaviorState=Next;Path.Reset();ReactionRemaining=0;}
 if(Next==EOverworldState::Warning||Next==EOverworldState::Observe)
 {
  CurrentSpeed=0;Path.Reset();
  if(Player)GetOwner()->SetActorRotation(FMath::RInterpConstantTo(GetOwner()->GetActorRotation(),
   FRotator(0,(Player->GetActorLocation()-Current).Rotation().Yaw,0),Delta,Settings.TurnDegreesPerSecond));
  if(Next==EOverworldState::Warning)
  {
   // Warning animation is visual only.
  }
  return true;
 }
 WarningElapsed=0;
 if(Next==EOverworldState::Approach||Next==EOverworldState::Retreat)
 {
  PauseRemaining=0;ReactionRemaining-=Delta;
  if(Next==EOverworldState::Retreat)Speed*=P.ReactionSpeedMultiplier;
  if(ReactionRemaining<=0)
  {
   const FVector Away=(Current-Player->GetActorLocation()).GetSafeNormal2D(SMALL_NUMBER,FVector::ForwardVector);
   const FVector Direction=Next==EOverworldState::Retreat?Away:-Away;
   const float Distance=Next==EOverworldState::Retreat?320.f:FMath::Clamp(D-(P.Temperament==EOverworldTemperament::Curious?P.PersonalSpace+100.f:65.f),5.f,350.f);
   Path.Reset();
   for(float Angle:{0.f,30.f,-30.f,60.f,-60.f,90.f,-90.f})
   {
    const FVector Candidate=Current+Direction.RotateAngleAxis(Angle,FVector::UpVector)*Distance;
    if(Next==EOverworldState::Retreat && FVector::Dist2D(Candidate,Player->GetActorLocation())<D+30.f)continue;
    if(Plan(Candidate))break;
    ++RejectedTargets;
   }
   ReactionRemaining=Random.FRandRange(1.1f,1.8f);
  }
 }
 return false;
}
void UPokeMonsterCreatureRoamingComponent::NotifyEncounterEnded()
{
 CooldownRemaining=Settings.Behavior.EncounterCooldown;bTerritoryArmed=false;
 WarningElapsed=0;BehaviorState=EPokeMonsterOverworldState::Cooldown;CurrentSpeed=0;BeginPause();
}
FPokeMonsterCreatureBehaviorProfile UPokeMonsterCreatureRoamingComponent::GetBehaviorProfile() const
{
 return bOverrideBehavior?BehaviorOverride:Settings.Behavior;
}
bool UPokeMonsterCreatureRoamingComponent::BeginDefeatEscape()
{
 if(!bReady||FollowTarget.IsValid())return false;
 bEscapingDefeat=true;bEscapeBlocked=false;EscapeElapsed=EscapeReplan=EscapeStalled=0;
 bPaused=false;Path.Reset();PauseRemaining=0;CurrentSpeed=AngularVelocity=0;
 BehaviorState=EPokeMonsterOverworldState::Retreat;SetComponentTickEnabled(true);return true;
}
bool UPokeMonsterCreatureRoamingComponent::PlanEscape(const FVector& Current,const APawn* Player)
{
 const FVector Away=Player?(Current-Player->GetActorLocation()).GetSafeNormal2D(SMALL_NUMBER,FVector::ForwardVector):GetOwner()->GetActorForwardVector();
 // Routes may turn around an obstruction; a bounded A* validates every segment and ground sample.
 for(float Length:{850.f,550.f,300.f})for(float Angle:{0.f,35.f,-35.f,70.f,-70.f,110.f,-110.f,150.f,-150.f})
 {
  const FVector Target=Current+Away.RotateAngleAxis(Angle,FVector::UpVector)*Length;
  if(RecentGoals.ContainsByPredicate([&](const FVector& P){return FVector::Dist2D(P,Target)<120.f;}))continue;
  if(Plan(Target)){RecentGoals.Add(Target);if(RecentGoals.Num()>8)RecentGoals.RemoveAt(0);return true;}
  ++RejectedTargets;
 }
 return false;
}

bool UPokeMonsterCreatureRoamingComponent::CanReengage() const
{
 return CooldownRemaining<=0 && (Settings.Behavior.Temperament!=EPokeMonsterOverworldTemperament::Territorial||bTerritoryArmed);
}
void UPokeMonsterCreatureRoamingComponent::CancelDefeatEscape()
{
 bEscapingDefeat=bEscapeBlocked=false;EscapeElapsed=0;Path.Reset();CurrentSpeed=0;BeginPause();
}

bool UPokeMonsterCreatureRoamingComponent::IsDecorativeSegmentBlocked(const FBox& Bounds,const FVector& Start,const FVector& End,float Radius,float HalfHeight,float StepHeight)
{
 const FBox Clearance(Bounds.Min-FVector(Radius,Radius,HalfHeight*2),Bounds.Max+FVector(Radius,Radius,StepHeight));
 return FMath::LineBoxIntersection(Clearance,Start,End,End-Start);
}


bool UPokeMonsterCreatureRoamingComponent::CanSeparateFromContact(const FVector& Start,const FVector& End,const FVector& Player,float Radius)
{
 if(Start.ContainsNaN()||End.ContainsNaN()||Player.ContainsNaN()||!FMath::IsFinite(Radius)||Radius<=0)return false;
 const FVector2D From(Start.X-Player.X,Start.Y-Player.Y),Delta(End.X-Start.X,End.Y-Start.Y);
 const double Initial=From.SizeSquared(),Length=Delta.SizeSquared(),Limit=double(Radius)*Radius;
 if(Length<=UE_DOUBLE_SMALL_NUMBER)return Initial>=Limit;
 const double Dot=FVector2D::DotProduct(From,Delta);
 if(Initial<Limit)return Dot>=0 && (From+Delta).SizeSquared()>Initial;
 const double Fraction=FMath::Clamp(-Dot/Length,0.,1.);
 return (From+Delta*Fraction).SizeSquared()>=Limit-UE_DOUBLE_KINDA_SMALL_NUMBER;
}


bool UPokeMonsterCreatureRoamingComponent::IsInRelocatedInterior(const FVector& Point) const
{
 for(const auto& Building:Buildings)
  if(Building.IsValid()&&Building->IsViewerInRelocatedRoom(Point))return true;
 return false;
}


bool UPokeMonsterCreatureRoamingComponent::CanGroundHover(float Height, const FBox& Bounds) const
{
 if (!bReady || bPaused || bEscapingDefeat || !GetWorld() || !GetOwner() || !Bounds.IsValid
  || !FMath::IsFinite(Height) || Height < 0.f || Height > 150.f) return false;
 const FVector Ground=GetOwner()->GetActorLocation()-FVector(0,0,Offset);
 if (BiomeHabitat && (!BiomeHabitat->bAllowGroundFlight || !BiomeHabitat->ContainsFlightColumn(Ground,Height,Bounds))) return false;
 for (const auto& Weak:Buildings) if (const auto* B=Weak.Get())
  if (B->IsViewerInside(Ground+FVector(0,0,50))) return false;
 FVector Projected;
 if (!ProjectWalkable(Ground,Projected) || FMath::Abs(Projected.Z-Ground.Z)>Settings.MaxStepHeight) return false;
 return CanTraverseHoverColumn(Ground,Ground,Height,Bounds);
}

bool UPokeMonsterCreatureRoamingComponent::CanTraverseHoverColumn(const FVector& Start,const FVector& End,float Height,const FBox& Bounds) const
{
 if(!Bounds.IsValid||!GetWorld()||!GetOwner())return false;
 // Rotation-independent footprint covers both wing tips through a turn. The whole column
 // remains clear, so hovering never permits passing above a ground obstruction or beneath
 // an overhang that the elevated head/wings would strike. Ordinary land paths are unchanged.
 const float Radius=FMath::Max(FMath::Max(FMath::Abs(Bounds.Min.X),FMath::Abs(Bounds.Max.X)),
  FMath::Max(FMath::Abs(Bounds.Min.Y),FMath::Abs(Bounds.Max.Y)))+5.f;
 const float Bottom=Bounds.Min.Z+2.f,Top=Bounds.Max.Z+Height+12.f;
 const FVector Extent(Radius,Radius,(Top-Bottom)*.5f),Lift(0,0,(Top+Bottom)*.5f);
 const FVector A=Start+Lift,B=End+Lift;
 FBox Column(A-Extent,A+Extent);Column+=FBox(B-Extent,B+Extent);
 for(const auto& Obstacle:HoverObstacles)if(Column.Intersect(Obstacle))return false;
 const auto Q=Query();const auto Shape=FCollisionShape::MakeBox(Extent);
 if(GetWorld()->OverlapBlockingTestByChannel(A,FQuat::Identity,ECC_Pawn,Shape,Q))return false;
 FHitResult Hit;return !GetWorld()->SweepSingleByChannel(Hit,A,B,FQuat::Identity,ECC_Pawn,Shape,Q);
}
