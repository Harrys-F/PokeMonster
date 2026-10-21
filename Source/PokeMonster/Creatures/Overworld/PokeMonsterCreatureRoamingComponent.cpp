#include "PokeMonsterCreatureRoamingComponent.h"
#include "PokeMonsterCreaturePath.h"
#include "../PokeMonsterCreatureSpeciesData.h"
#include "../PokeMonsterCreaturePresentation.h"
#include "../../Characters/PokeMonsterPlayerCharacter.h"
#include "../../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Components/PrimitiveComponent.h"
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
	SetComponentTickEnabled(false); bReady = false;
	if (!Species || !Species->Overworld.IsValid() || !FMath::IsFinite(RootGroundOffset)
		|| !FMath::IsFinite(Radius) || Radius <= 0 || !FMath::IsFinite(HalfHeight) || HalfHeight <= 0
		|| !FMath::IsFinite(HabitatRadiusOverride) || HabitatRadiusOverride < 0
		|| (HabitatRadiusOverride > 0 && (HabitatRadiusOverride < 150 || HabitatRadiusOverride > 5000))
		|| HabitatHalfExtent.ContainsNaN() || HabitatHalfExtent.X < 0 || HabitatHalfExtent.Y < 0) return;
	Presentation = Species->GetVisuals().Presentation.LoadSynchronous();
	if (!Presentation || !Presentation->GetValidationErrors().IsEmpty()) return;
	Settings = Species->Overworld; Offset = RootGroundOffset; BodyRadius = Radius;
	BodyHalfHeight = FMath::Max(HalfHeight, Radius); FollowTarget = Follow;
	HabitatOrigin = GetOwner()->GetActorLocation() - FVector(0, 0, Offset);
	Buildings.Reset();
	for (TActorIterator<APokeMonsterBuildingCutaway> It(GetWorld()); It; ++It) Buildings.Add(*It);
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
	TArray<AActor*> Attached; GetOwner()->GetAttachedActors(Attached);
	for (AActor* Actor : Attached) Q.AddIgnoredActor(Actor);
	if (FollowTarget.IsValid()) Q.AddIgnoredActor(FollowTarget.Get());
	return Q;
}
bool UPokeMonsterCreatureRoamingComponent::IsInsideHabitat(const FVector& Point) const
{
	if (!bReady || Point.ContainsNaN()) return false;
	const FVector BodyPoint = Point + FVector(0,0,BodyHalfHeight);
	for (const auto& Weak : Buildings)
	{
		const auto* Building = Weak.Get(); if (!Building) continue;
		const bool PointInside = Building->IsViewerInside(BodyPoint);
		if (!FollowTarget.IsValid()) { if (PointInside) return false; continue; }
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
	const float Radius = HabitatRadiusOverride > 0 ? HabitatRadiusOverride : Settings.RoamRadius;
	const FVector D = Point - HabitatOrigin;
	return D.SizeSquared2D() <= FMath::Square(Radius)
		&& (HabitatHalfExtent.X <= 0 || FMath::Abs(D.X) <= HabitatHalfExtent.X)
		&& (HabitatHalfExtent.Y <= 0 || FMath::Abs(D.Y) <= HabitatHalfExtent.Y);
}
bool UPokeMonsterCreatureRoamingComponent::ProjectWalkable(const FVector& Point, FVector& Ground) const
{
	UWorld* W = GetWorld(); if (!W || !IsInsideHabitat(Point)) return false;
	const auto Q = Query(); FHitResult Hit;
	if (!W->LineTraceSingleByChannel(Hit, Point + FVector(0, 0, Settings.MaxStepHeight + 55.f),
		Point - FVector(0, 0, 100.f), ECC_Visibility, Q) || Hit.ImpactNormal.Z < .75f) return false;
	if (!Hit.GetComponent() || Hit.GetComponent()->GetCollisionResponseToChannel(ECC_Pawn) != ECR_Block) return false;
	const AActor* Surface = Hit.GetActor();
	if (Surface && (Surface->ActorHasTag(TEXT("CreatureNoWalk"))
		|| (!Settings.bCanEnterWater && Surface->ActorHasTag(TEXT("Water"))))) return false;
	Ground = Hit.ImpactPoint;
	return !W->OverlapBlockingTestByChannel(Ground + FVector(0, 0, BodyHalfHeight + Settings.MaxStepHeight + 2.f),
		FQuat::Identity, ECC_Pawn, FCollisionShape::MakeCapsule(BodyRadius, BodyHalfHeight), Q);
}
bool UPokeMonsterCreatureRoamingComponent::CanTraverse(const FVector& Start, const FVector& End) const
{
	if (!GetWorld() || !bReady || Start.ContainsNaN() || End.ContainsNaN()) return false;
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
	PauseRemaining = Random.FRandRange(Settings.PauseMinimum, Settings.PauseMaximum);
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
	const auto* GI = GetWorld()->GetGameInstance();
	const auto* E = GI ? GI->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
	const auto* C = GI ? GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>() : nullptr;
	if ((E && E->IsEncounterActive()) || (C && C->IsReturningFromDefeat())) return;
	const FVector Current = Owner->GetActorLocation() - FVector(0, 0, Offset);
	const auto* Player = Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this, 0));
	if (!FollowTarget.IsValid() && Player && (Player->IsOverworldInputLocked()
		|| FVector::Dist2D(Current, Player->GetActorLocation()) < 110.f))
	{
		Path.Reset(); CurrentSpeed=0.f; PauseRemaining = .6f;
		const float Yaw = (Player->GetActorLocation() - Current).Rotation().Yaw;
		Owner->SetActorRotation(FMath::RInterpConstantTo(Owner->GetActorRotation(), FRotator(0,Yaw,0),Delta,Settings.TurnDegreesPerSecond));
		return;
	}
	float Speed = Settings.WalkSpeedOverride > 0 ? Settings.WalkSpeedOverride : Presentation->WalkSpeed;
	ReplanRemaining -= Delta;
	if (FollowTarget.IsValid())
	{
		const float Distance = FVector::Dist2D(Current, FollowTarget->GetActorLocation());
		if (Distance > Settings.RecallDistance) bRecalling = true;
		else if (Distance < 170.f) bRecalling = false;
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
		if (bRecalling || ReplanRemaining > 0) return;
		const FVector Center = FollowTarget.IsValid() ? FollowTarget->GetActorLocation() : HabitatOrigin;
		const float Radius = FollowTarget.IsValid() ? Settings.CompanionRoamRadius
			: HabitatRadiusOverride > 0 ? HabitatRadiusOverride : Settings.RoamRadius;
		struct FCandidate { FVector Point; float Score; int32 Sector; };
		TArray<FCandidate> Candidates;
		for (int32 Attempt=0; Attempt<16; ++Attempt)
		{
			const float Angle=Random.FRandRange(-PI,PI), Distance=Radius*FMath::Sqrt(Random.FRand());
			FVector Goal=Center+FVector(FMath::Cos(Angle)*Distance,FMath::Sin(Angle)*Distance,0); Goal.Z=Current.Z;
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
	if (Path.IsEmpty()) { if (!bRecalling) BeginPause(); return; }
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
	Owner->SetActorLocation(Ground + FVector(0,0,Offset), true, &Hit);
	DistanceTravelled += FVector::Dist2D(Before, Owner->GetActorLocation());
	if (Hit.bBlockingHit) { ++BlockedSteps; CurrentSpeed=0.f; BeginPause(); return; }
	if (FVector::Dist2D(Ground, Target) < 1.f)
	{
		Path.RemoveAt(0);
		if (Path.IsEmpty() && !bRecalling) BeginPause();
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
