#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PokeMonsterCreatureOverworldSettings.h"
#include "PokeMonsterCreatureActivities.h"
#include "PokeMonsterCreatureRhythm.h"
#include "../../Time/PokeMonsterWorldClock.h"
#include "PokeMonsterCreatureRoamingComponent.generated.h"
class APokeMonsterBuildingCutaway;
class APokeMonsterBiomeHabitat;
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
    /** Null on all existing maps. Explicit sandbox surface/media contract only. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Development|Biome") TObjectPtr<APokeMonsterBiomeHabitat> BiomeHabitat;
    /** Per-instance immersion; one pond can contain differently sized swimmers. */
    UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Creature|Movement") float WaterDraftOverrideCm=-1.f;
	UFUNCTION(BlueprintCallable, Category="Creature|Movement") void Configure(const UPokeMonsterCreatureSpeciesData* Species, float RootGroundOffset,
		float Radius, float HalfHeight, AActor* Follow = nullptr, int32 Seed = 31);
	virtual void EndPlay(const EEndPlayReason::Type Reason) override;
	virtual void TickComponent(float Delta, ELevelTick Tick, FActorComponentTickFunction* Function) override;
	UFUNCTION(BlueprintCallable, Category="Creature|Movement") void SetMovementPaused(bool Paused);
	UFUNCTION(BlueprintPure, Category="Creature|Movement") bool ProjectWalkable(const FVector& Point, FVector& Ground) const;
	UFUNCTION(BlueprintPure, Category="Creature|Movement") bool CanTraverse(const FVector& Start, const FVector& End) const;
	UFUNCTION(BlueprintPure, Category="Creature|Movement") bool IsInsideHabitat(const FVector& Point) const;
	bool IsInRelocatedInterior(const FVector& Point) const;
	static bool CanSeparateFromContact(const FVector& Start,const FVector& End,const FVector& Player,float ContactRadius);
	static bool IsDecorativeSegmentBlocked(const FBox& Bounds,const FVector& Start,const FVector& End,float Radius,float HalfHeight,float StepHeight);
	bool CanGroundHover(float Height, const FBox& VisualBounds,bool RequireLandingColumn=false) const;
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
 /** Controlled visual specimen route. Uses this same planner/heading/speed, never a second wild AI. */
 UFUNCTION(BlueprintCallable,Category="Development|Model") bool RequestModelPreviewGoal(FVector Goal);
 UFUNCTION(BlueprintPure,Category="Development|Model") bool IsModelPreviewMoving()const{return bControlledModelPreview&&!Path.IsEmpty();}
 UPROPERTY(Transient,BlueprintReadWrite,Category="Development|Model") bool bControlledModelPreview=false;
 UFUNCTION(BlueprintCallable,Category="Behavior") void NotifyEncounterStarted();
 UFUNCTION(BlueprintCallable,Category="Behavior") void NotifyEncounterEnded();
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") bool bPlayerAware=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 GroupCompleted=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 GroupAlarms=0;
 bool CanReengage() const;
 void CancelDefeatEscape();
 UFUNCTION(BlueprintCallable,Category="Behavior") bool BeginDefeatEscape();
 UFUNCTION(BlueprintPure,Category="Behavior") FPokeMonsterCreatureBehaviorProfile GetBehaviorProfile() const;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") bool bEscapingDefeat=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") bool bEscapeBlocked=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Behavior") float EscapeElapsed=0.f;
/** VisualV2 rollout only: the six defaults can be tuned per placed wild encounter. */
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Activities") bool bOverrideActivities=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Activities") FPokeMonsterCreatureActivityProfile ActivityOverride;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Activities") EPokeMonsterActivityPeriod ActivityPeriod=EPokeMonsterActivityPeriod::Day;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") FPokeMonsterCreatureActivityProfile Activities;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") bool bActivitiesEnabled=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") bool bActivityDistant=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") float ActivityRemaining=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 ActivityDecisions=0;
 /** Optional development measurement; disabled during normal gameplay. */
 UPROPERTY(Transient,BlueprintReadWrite,Category="Activities|Diagnostics") bool bMeasureActivityCost=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Diagnostics") double TickWorkMicroseconds=0;
 /** Subset of the existing opt-in tick timing; includes failed local path/surface attempts. */
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Diagnostics") double PlanningWorkMicroseconds=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Diagnostics") int64 MeasuredPlans=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Diagnostics") int64 MeasuredTicks=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") FName LastSocialDecision=NAME_None;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 PeerQueries=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 PerceptionTraces=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 SocialCompleted=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 ForageCompleted=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") TObjectPtr<UPokeMonsterCreatureRoamingComponent> SocialPartner;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 SocialRequests=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 SocialDeclined=0;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities") int32 SocialInterrupted=0;
 UFUNCTION(BlueprintPure,Category="Activities") bool IsActivityTravelling() const { return bActivityTravelling; }
/** Optional per-encounter rhythm; normal rollout still uses the existing VisualV2 activity boundary. */
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Activities|Rhythm") bool bOverrideRhythm=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Activities|Rhythm") FPokeMonsterCreatureRhythm RhythmOverride;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Rhythm") bool bRhythmEnabled=false;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Rhythm") FPokeMonsterCreatureRhythm Rhythm;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Rhythm") FPokeMonsterCreatureActivityProfile RhythmActivities;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Rhythm") float RhythmActivity=1.f;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Rhythm") float RhythmOffsetMinutes=0.f;
 UPROPERTY(Transient,VisibleAnywhere,BlueprintReadOnly,Category="Activities|Rhythm") int32 RhythmRefreshes=0;
private:
 void ConfigureRhythm(int32 Seed);
 void BindRhythm(UPokeMonsterWorldClock* Clock);
 void UnbindRhythm();
 void RefreshRhythm();
 UFUNCTION() void RhythmTimeSet(FPokeMonsterWorldTime Time);
 UFUNCTION() void RhythmPhaseChanged(EPokeMonsterDayPhase Phase);
 bool IsAmbientClockPaused() const;
 bool IsSocialPartnerValid() const;
 const FPokeMonsterCreatureActivityProfile& ActivityWeights() const { return bRhythmEnabled?RhythmActivities:Activities; }
 TWeakObjectPtr<UPokeMonsterWorldClock> RhythmClock;
 float RhythmRefreshRemaining=0;
 friend struct FPokeMonsterNaturalActivityTestAccess;
 void ConfigureActivities(const UPokeMonsterCreatureSpeciesData* Species,int32 Seed);
 bool UpdateActivities(float Delta,const FVector& Current,const APawn* Player,float& Speed);
 void FinishActivity(bool Interrupted=false);
 void ReleaseSocial();
 bool FindSocialPartner();
 bool CanSocialize() const;
 bool TryStartSocial(UPokeMonsterCreatureRoamingComponent* Peer,const FVector& Current);
 bool PeerVisible(const UPokeMonsterCreatureRoamingComponent* Peer) const;
 bool PlanForage(const FVector& Current);
 void FaceActivity(float Delta,const FVector& Target);
 FName ActivitySpecies;
 FRandomStream ActivityRandom;
 TArray<FVector> ForageAnchors;
 TWeakObjectPtr<UPokeMonsterCreatureRoamingComponent> PerceivedPeer;
 float SocialCooldown=0, SleepCooldown=0, ForageCooldown=0, PeerQueryRemaining=0;
 float VisibilityRemaining=0;
 bool bPlayerVisibleCached=false, bActivityRunning=false, bActivityTravelling=false, bSocialLeader=false;
 float ActivityTravelRemaining=0, ActivityElapsed=0, SocialInvitationRemaining=0;
 float SocialDeadlineRemaining=0, SocialValidationRemaining=0;
 FVector ActivityFocus=FVector::ZeroVector;
 bool bWasAerialTravel=false;
 bool IsAerialTravelActive() const;
 bool CanTraverseHoverColumn(const FVector& Start,const FVector& End,float Height,const FBox& Bounds,bool RequireGroundColumn=false) const;
 float PresentationHoverHeight=0.f;
 FBox PresentationHoverBounds{ForceInit};
 bool UpdateBehavior(float Delta,const FVector& Current,const APawn* Player,float& Speed);
 bool PlayerVisible(const APawn* Player) const;
 float SightAcquiring=0,SightLost=0,AwarenessSeconds=0,PursuitElapsed=0,GroupAlertRemaining=0;
 FVector LastPlayerPoint=FVector::ZeroVector,GroupAlarmPoint=FVector::ZeroVector;
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
