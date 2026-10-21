#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PokeMonsterCreatureOverworldSettings.h"
#include "PokeMonsterCreatureRoamingComponent.generated.h"
class APokeMonsterBuildingCutaway;
struct FCollisionQueryParams;
class UPokeMonsterCreatureSpeciesData;
class UPokeMonsterCreaturePresentationData;

/** Shared land movement for placed wild creatures and the collisionless party visual. */
UCLASS(ClassGroup=(PokeMonster), meta=(BlueprintSpawnableComponent))
class POKEMONSTER_API UPokeMonsterCreatureRoamingComponent : public UActorComponent
{
	GENERATED_BODY()
public:
	UPokeMonsterCreatureRoamingComponent();
	UFUNCTION(BlueprintCallable, Category="Creature|Movement") void Configure(const UPokeMonsterCreatureSpeciesData* Species, float RootGroundOffset,
		float Radius, float HalfHeight, AActor* Follow = nullptr, int32 Seed = 31);
	virtual void TickComponent(float Delta, ELevelTick Tick, FActorComponentTickFunction* Function) override;
	UFUNCTION(BlueprintCallable, Category="Creature|Movement") void SetMovementPaused(bool Paused);
	UFUNCTION(BlueprintPure, Category="Creature|Movement") bool ProjectWalkable(const FVector& Point, FVector& Ground) const;
	UFUNCTION(BlueprintPure, Category="Creature|Movement") bool CanTraverse(const FVector& Start, const FVector& End) const;
	UFUNCTION(BlueprintPure, Category="Creature|Movement") bool IsInsideHabitat(const FVector& Point) const;
	bool IsInRelocatedInterior(const FVector& Point) const;
	static bool CanSeparateFromContact(const FVector& Start,const FVector& End,const FVector& Player,float ContactRadius);
	static bool IsDecorativeSegmentBlocked(const FBox& Bounds,const FVector& Start,const FVector& End,float Radius,float HalfHeight,float StepHeight);
	bool CanGroundHover(float Height, const FBox& VisualBounds) const;
 void SetPresentationHoverClearance(float Height,const FBox& Bounds) { PresentationHoverHeight=Height;PresentationHoverBounds=Bounds; }
 void SetPresentationHold(bool Held) { bPresentationHold=Held; }
 static float AdvanceSpeed(float Current, float Desired, float Distance, bool Companion,
		const FPokeMonsterCreatureOverworldSettings& Config, float Delta);
	static float AdvanceHeading(float CurrentYaw, float DesiredYaw, float& AngularVelocity,
		const FPokeMonsterCreatureOverworldSettings& Config, float Delta);
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") float CurrentSpeed = 0.f;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") int32 RejectedTargets = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Habitat", meta=(ClampMin="0")) float HabitatRadiusOverride = 0.f;
	/** Optional bounds around the original spawn, intersected with species radius. Zero disables the box. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Habitat") FVector2D HabitatHalfExtent = FVector2D::ZeroVector;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") FVector HabitatOrigin;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") FVector CurrentGoal;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") float DistanceTravelled = 0.f;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") int32 SuccessfulPlans = 0;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") int32 BlockedSteps = 0;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") bool bRecalling = false;
	UPROPERTY(Transient, VisibleAnywhere, BlueprintReadOnly, Category="Movement") FPokeMonsterCreatureOverworldSettings Settings;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Behavior") bool bOverrideBehavior=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Behavior") FPokeMonsterCreatureBehaviorProfile BehaviorOverride;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") EPokeMonsterOverworldState BehaviorState=EPokeMonsterOverworldState::Rest;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") float WarningElapsed=0.f;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") float CooldownRemaining=0.f;
 UFUNCTION(BlueprintCallable,Category="Behavior") void NotifyEncounterEnded();
 bool CanReengage() const;
 void CancelDefeatEscape();
 UFUNCTION(BlueprintCallable,Category="Behavior") bool BeginDefeatEscape();
 UFUNCTION(BlueprintPure,Category="Behavior") FPokeMonsterCreatureBehaviorProfile GetBehaviorProfile() const;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") bool bEscapingDefeat=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") bool bEscapeBlocked=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") float EscapeElapsed=0.f;
private:
 bool CanTraverseHoverColumn(const FVector& Start,const FVector& End,float Height,const FBox& Bounds) const;
 float PresentationHoverHeight=0.f;
 FBox PresentationHoverBounds{ForceInit};
 bool UpdateBehavior(float Delta,const FVector& Current,const APawn* Player,float& Speed);
 bool PlayerVisible(const APawn* Player) const;
 bool bTerritoryArmed=true;
 float EscapeReplan=0.f,EscapeStalled=0.f;
 bool PlanEscape(const FVector& Current,const APawn* Player);
 float ReactionRemaining=0.f,InterestRemaining=0.f;
	bool Plan(const FVector& Goal);
	void BeginPause();
	FCollisionQueryParams Query() const;
	UPROPERTY(Transient) TObjectPtr<UPokeMonsterCreaturePresentationData> Presentation;
	TWeakObjectPtr<AActor> FollowTarget;
	TArray<TWeakObjectPtr<APokeMonsterBuildingCutaway>> Buildings;
	TArray<FVector> Path;
 TArray<FBox> DecorativeObstacles;
 TArray<FBox> HoverObstacles;
	FRandomStream Random;
	TArray<FVector> RecentGoals;
	int32 SectorVisits[8] = {};
	float AngularVelocity = 0.f;
	float Offset = 0.f, BodyRadius = 24.f, BodyHalfHeight = 30.f, PauseRemaining = 0.f;
	float ReplanRemaining = 0.f, LookYaw = 0.f;
	bool bReady = false, bPaused = false, bPresentationHold=false;
};
