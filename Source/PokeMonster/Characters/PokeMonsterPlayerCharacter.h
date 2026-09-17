// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "InputActionValue.h"
#include "PaperCharacter.h"
#include "PokeMonsterPlayerCharacter.generated.h"

class UCameraComponent;
class UInputAction;
class UInputMappingContext;
class USpringArmComponent;
class UStaticMeshComponent;

#if WITH_DEV_AUTOMATION_TESTS
class FPokeMonsterPlayerFoundationTest;
#endif

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

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "PokeMonster|Visual")
	bool bShowPlaceholderWithoutFlipbook = true;

	/** Lets a later Blueprint select directional flipbooks without replacing movement code. */
	UFUNCTION(BlueprintImplementableEvent, Category = "PokeMonster|Visual")
	void OnMovementInputChanged(FVector2D NewMovementInput);

private:
#if WITH_DEV_AUTOMATION_TESTS
	friend class FPokeMonsterPlayerFoundationTest;
#endif

	void Move(const FInputActionValue& Value);
	void StopMoving(const FInputActionValue& Value);
	void UpdateMovementInput(FVector2D NewMovementInput);
	static FVector CalculateCameraRelativeMovement(FVector2D Input, float CameraYawDegrees);

	UPROPERTY(Transient)
	TObjectPtr<UInputMappingContext> DefaultMappingContext;

	UPROPERTY(Transient)
	TObjectPtr<UInputAction> MoveAction;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "PokeMonster|Movement", meta = (AllowPrivateAccess = "true"))
	FVector2D MovementInput = FVector2D::ZeroVector;
};
