// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "InputActionValue.h"
#include "PaperCharacter.h"
#include "PokeMonsterPlayerCharacter.generated.h"

class UCameraComponent;
class UInputAction;
class UInputMappingContext;
class UPaperFlipbook;
class UPaperFlipbookComponent;
class USpringArmComponent;
class UStaticMeshComponent;

#if WITH_DEV_AUTOMATION_TESTS
class FPokeMonsterPlayerFoundationTest;
#endif

UENUM(BlueprintType)
enum class EPokeMonsterFacingDirection : uint8
{
	Up,
	Down,
	Left,
	Right
};

UENUM(BlueprintType)
enum class EPokeMonsterLocomotionState : uint8
{
	Idle,
	Walking
};

/** One flipbook slot for each screen-facing direction. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterDirectionalFlipbookSet
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Flipbooks")
	TObjectPtr<UPaperFlipbook> Up;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Flipbooks")
	TObjectPtr<UPaperFlipbook> Down;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Flipbooks")
	TObjectPtr<UPaperFlipbook> Left;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Flipbooks")
	TObjectPtr<UPaperFlipbook> Right;

	UPaperFlipbook* GetFlipbook(EPokeMonsterFacingDirection Direction) const;
	bool HasAnyFlipbook() const;
};

/**
 * Technical player foundation for the top-down exploration game.
 *
 * Movement and camera behavior live in C++. The Paper2D component and camera
 * components remain accessible to Blueprint children for later visual tuning.
 */
UCLASS(Blueprintable)
class POKEMONSTER_API APokeMonsterPlayerCharacter : public APaperCharacter
{
	GENERATED_BODY()

public:
	APokeMonsterPlayerCharacter();

	virtual void PawnClientRestart() override;
	virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Movement")
	FVector2D GetMovementInput() const { return MovementInput; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Visual")
	EPokeMonsterFacingDirection GetFacingDirection() const { return FacingDirection; }

	UFUNCTION(BlueprintPure, Category = "PokeMonster|Visual")
	EPokeMonsterLocomotionState GetLocomotionState() const { return LocomotionState; }

	/** APaperCharacter's native Paper2D component used for all character flipbooks. */
	UFUNCTION(BlueprintPure, Category = "PokeMonster|Visual")
	UPaperFlipbookComponent* GetCharacterFlipbookComponent() const { return GetSprite(); }

protected:
	virtual void BeginPlay() override;

	/** Smooth camera follow and the fixed, angled top-down view. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "PokeMonster|Camera")
	TObjectPtr<USpringArmComponent> CameraBoom;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "PokeMonster|Camera")
	TObjectPtr<UCameraComponent> FollowCamera;

	/** Temporary visible stand-in. It hides itself when a flipbook is assigned. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "PokeMonster|Visual")
	TObjectPtr<UStaticMeshComponent> PlaceholderMesh;

	/** Small marker that makes the current facing direction readable without final art. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "PokeMonster|Visual")
	TObjectPtr<UStaticMeshComponent> FacingMarkerMesh;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "PokeMonster|Visual")
	bool bShowPlaceholderWithoutFlipbook = true;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "PokeMonster|Visual|Flipbooks")
	FPokeMonsterDirectionalFlipbookSet IdleFlipbooks;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "PokeMonster|Visual|Flipbooks")
	FPokeMonsterDirectionalFlipbookSet WalkingFlipbooks;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "PokeMonster|Visual", meta = (ClampMin = "0.0", ClampMax = "1.0"))
	float FacingInputThreshold = 0.1f;

	/** Lets a later Blueprint select directional flipbooks without replacing movement code. */
	UFUNCTION(BlueprintImplementableEvent, Category = "PokeMonster|Visual")
	void OnMovementInputChanged(FVector2D NewMovementInput);

	/** Optional Blueprint hook for effects that react to animation-state changes. */
	UFUNCTION(BlueprintImplementableEvent, Category = "PokeMonster|Visual")
	void OnVisualStateChanged(EPokeMonsterFacingDirection NewDirection, EPokeMonsterLocomotionState NewState);

private:
#if WITH_DEV_AUTOMATION_TESTS
	friend class FPokeMonsterPlayerFoundationTest;
#endif

	void Move(const FInputActionValue& Value);
	void StopMoving(const FInputActionValue& Value);
	void UpdateMovementInput(FVector2D NewMovementInput);
	void RefreshCharacterVisual();
	static FVector CalculateCameraRelativeMovement(FVector2D Input, float CameraYawDegrees);
	static EPokeMonsterFacingDirection CalculateFacingDirection(
		FVector2D Input,
		EPokeMonsterFacingDirection CurrentDirection,
		float InputThreshold);

	UPROPERTY(Transient)
	TObjectPtr<UInputMappingContext> DefaultMappingContext;

	UPROPERTY(Transient)
	TObjectPtr<UInputAction> MoveAction;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "PokeMonster|Movement", meta = (AllowPrivateAccess = "true"))
	FVector2D MovementInput = FVector2D::ZeroVector;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "PokeMonster|Visual", meta = (AllowPrivateAccess = "true"))
	EPokeMonsterFacingDirection FacingDirection = EPokeMonsterFacingDirection::Down;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "PokeMonster|Visual", meta = (AllowPrivateAccess = "true"))
	EPokeMonsterLocomotionState LocomotionState = EPokeMonsterLocomotionState::Idle;
};
