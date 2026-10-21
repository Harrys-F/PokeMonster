#pragma once
#include "CoreMinimal.h"
#include "PokeMonsterCreatureOverworldSettings.generated.h"

class UAnimSequence;

/** Centimetres/seconds. Presentation clip speeds remain the default locomotion speeds. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureOverworldSettings
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="150")) float RoamRadius = 650.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="50")) float MinimumTravel = 180.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="0")) float WalkSpeedOverride = 0.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="0")) float RunSpeedOverride = 0.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="0.25")) float PauseMinimum = 1.4f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="0.25")) float PauseMaximum = 3.8f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float TurnDegreesPerSecond = 110.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float Acceleration = 90.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float BrakingDeceleration = 180.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float CompanionAcceleration = 480.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float CompanionBrakingDeceleration = 600.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float TurnAcceleration = 260.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float MaxStepHeight = 25.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1")) float BodyRadius = 24.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="100")) float CompanionRoamRadius = 260.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="150")) float RecallDistance = 420.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="100")) float CompanionMaximumSpeed = 400.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="500")) float MaximumActiveDistance = 1400.f;
	/** Optional faster in-place clip, used only by the companion visual, never by ClassicBattle. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) TSoftObjectPtr<UAnimSequence> SprintAnimation;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="0")) float SprintReferenceSpeed = 0.f;
	/** Land locomotion by default, including Schiggy. Swimming requires a later rig/terrain contract. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bCanEnterWater = false;
	bool IsValid() const;
};
