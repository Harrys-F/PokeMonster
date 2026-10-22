#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "InputMappingContext.h"
#include "InputAction.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterPlayerSprintTest, "PokeMonster.Player.Sprint",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterPlayerSprintTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
    GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
    ON_SCOPE_EXIT { GEngine->DestroyWorldContext(World); World->DestroyWorld(false); };
    auto* P = World->SpawnActor<APokeMonsterPlayerCharacter>();
    auto* M = P->GetCharacterMovement(); M->SetMovementMode(MOVE_Walking);
    bool Left = false, Right = false, Stick = false;
    for (const auto& Mapping : P->DefaultMappingContext->GetMappings())
    {
        Left |= Mapping.Action == P->SprintHoldAction && Mapping.Key == EKeys::LeftShift;
        Right |= Mapping.Action == P->SprintHoldAction && Mapping.Key == EKeys::RightShift;
        Stick |= Mapping.Action == P->SprintToggleAction && Mapping.Key == EKeys::Gamepad_LeftThumbstick;
    }
    TestTrue(TEXT("Both shift keys and L3 have their own Enhanced Input actions"), Left && Right && Stick);
    P->StartSprintHold(FInputActionValue(true));
    TestFalse(TEXT("Held shift at rest does not change standing speed"), P->IsSprinting());
    const FVector2D Directions[] = {{0,1},{1,1},{1,0},{1,-1},{0,-1},{-1,-1},{-1,0},{-1,1}};
    for (const auto& D : Directions)
    {
        P->Move(FInputActionValue(D));
        TestTrue(TEXT("Shift activates in each of eight directions"), P->IsSprinting());
        TestEqual(TEXT("Sprint is exactly 1.5 times 210"), M->MaxWalkSpeed, 315.f);
        TestTrue(TEXT("Diagonal and cardinal sprint direction remain unit length"),
            FMath::IsNearlyEqual(P->CalculateCameraRelativeMovement(D, -45.f).Size2D(), 1.f, .001f));
    }
    const auto LastFacing = P->GetInteractionWorldDirection();
    P->StopMoving(FInputActionValue(FVector2D::ZeroVector));
    TestEqual(TEXT("Stopping restores normal speed"), M->MaxWalkSpeed, 210.f);
    TestTrue(TEXT("Last facing survives stop"), LastFacing.Equals(P->GetInteractionWorldDirection()));
    P->StopSprintHold(FInputActionValue(false));
    P->Move(FInputActionValue(FVector2D(0,1))); M->Velocity = FVector(210,0,0);
    P->ToggleSprint(FInputActionValue(true)); TestTrue(TEXT("L3 toggles on while moving"), P->IsSprinting());
    P->ToggleSprint(FInputActionValue(true)); TestFalse(TEXT("Second L3 toggles off"), P->IsSprinting());
    P->ToggleSprint(FInputActionValue(true));
    P->StopMoving(FInputActionValue(FVector2D::ZeroVector));
    P->Move(FInputActionValue(FVector2D(0,1)));
    TestTrue(TEXT("L3 mode survives stopping and resumes movement"), P->IsSprinting());
    M->Velocity = FVector::ZeroVector;
    P->OnMovementUpdated(.016f, FVector::ZeroVector, FVector(315,0,0));
    TestTrue(TEXT("Explicit mode remains selected after a collision stop"), P->IsSprintModeEnabled());
    P->ToggleSprint(FInputActionValue(true));
    P->StartSprintHold(FInputActionValue(true));
    P->SetOverworldInputLocked(true);
    TestFalse(TEXT("Existing menu/dialogue/battle lock blocks sprint"), P->CanSprint());
    TestEqual(TEXT("Input lock restores walk speed immediately"), M->MaxWalkSpeed, 210.f);
    P->SetOverworldInputLocked(false); P->Move(FInputActionValue(FVector2D(0,1)));
    TestFalse(TEXT("Unlock does not retain a stale sprint request"), P->IsSprinting());
    P->StartSprintHold(FInputActionValue(true));
    auto* Building = World->SpawnActor<APokeMonsterBuildingCutaway>();
    Building->bUseInteriorCamera = false; P->SprintInteriorAreas.Add(Building); P->RefreshSprint();
    TestFalse(TEXT("Ordinary interior footprint blocks sprint without camera overrides"), P->IsSprinting());
    TestEqual(TEXT("Indoor speed remains 210"), M->MaxWalkSpeed, 210.f);
    P->SetActorLocation(FVector(1000,0,0)); P->RefreshSprint();
    TestTrue(TEXT("Held shift can resume outside the footprint"), P->IsSprinting());
    P->SetInteriorCameraSource(Building);
    TestFalse(TEXT("Interior transition also blocks sprint"), P->IsSprinting());
    P->ClearInteriorCameraSource(Building); P->StopSprintHold(FInputActionValue(false));
    M->MaxWalkSpeed = 240.f;
    P->StartSprintHold(FInputActionValue(true));
    TestEqual(TEXT("Multiplier uses the currently configured walking speed"), M->MaxWalkSpeed, 360.f);
    P->StopSprintHold(FInputActionValue(false));
    TestEqual(TEXT("Release restores that configured speed without changing it"), M->MaxWalkSpeed, 240.f);
    return true;
}
#endif
