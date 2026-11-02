#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include <limits>
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterPlayerTestSpeedTest, "PokeMonster.Player.TransientTestSpeed",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterPlayerTestSpeedTest::RunTest(const FString&)
{
    UWorld* W = UWorld::CreateWorld(EWorldType::Game, false);
    GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
    ON_SCOPE_EXIT { GEngine->DestroyWorldContext(W); W->DestroyWorld(false); };
    auto* P = W->SpawnActor<APokeMonsterPlayerCharacter>();
    auto* Other = W->SpawnActor<APokeMonsterPlayerCharacter>();
    auto* M = P->GetCharacterMovement(); M->SetMovementMode(MOVE_Walking);
    TestEqual(TEXT("New pawn starts at one"), P->GetTestSpeedFactor(), 1.f);
    TestTrue(TEXT("Triple factor accepted"), P->SetTestSpeedFactor(3));
    TestEqual(TEXT("Walking is exactly 300 percent"), M->MaxWalkSpeed, 630.f);
    for (int32 I=0; I<8; ++I)
    {
        P->Move(FInputActionValue(FVector2D(1,1)));
        P->StartSprintHold(FInputActionValue(true));
        TestEqual(TEXT("Sprint uses existing 1.5 ratio once"), M->MaxWalkSpeed, 945.f);
        P->SetTestSpeedFactor(3);
        TestEqual(TEXT("Repeated factor never compounds"), M->MaxWalkSpeed, 945.f);
        P->StopSprintHold(FInputActionValue(false));
        TestEqual(TEXT("Release retains triple walking"), M->MaxWalkSpeed, 630.f);
    }
    P->StartSprintHold(FInputActionValue(true)); P->SetTestSpeedFactor(2);
    TestEqual(TEXT("Factor change during sprint"), M->MaxWalkSpeed, 630.f);
    P->SetTestSpeedFactor(1);
    TestEqual(TEXT("Sprint resets exactly"), M->MaxWalkSpeed, 315.f);
    P->StopSprintHold(FInputActionValue(false));
    TestEqual(TEXT("Walk resets exactly"), M->MaxWalkSpeed, 210.f);
    P->SetTestSpeedFactor(3); P->GamepadMove(FInputActionValue(FVector2D(0,1)));
    P->ToggleSprint(FInputActionValue(true));
    TestEqual(TEXT("Same factor for stick and L3"), M->MaxWalkSpeed, 945.f);
    P->SetOverworldInputLocked(true);
    TestEqual(TEXT("Existing UI/battle lock clears sprint only"), M->MaxWalkSpeed, 630.f);
    TestEqual(TEXT("Other actors are untouched"), Other->GetCharacterMovement()->MaxWalkSpeed, 210.f);
    TestFalse(TEXT("Invalid factor rejected"), P->SetTestSpeedFactor(0));
    TestFalse(TEXT("Nonfinite factor rejected"), P->SetTestSpeedFactor(std::numeric_limits<float>::quiet_NaN()));
    TestEqual(TEXT("Rejected values cannot corrupt factor"), P->GetTestSpeedFactor(), 3.f);
    auto* Fresh = W->SpawnActor<APokeMonsterPlayerCharacter>();
    TestEqual(TEXT("No global persistent factor"), Fresh->GetTestSpeedFactor(), 1.f);
    P->SetOverworldInputLocked(false); P->bSprintToggled=false; P->RefreshSprint();
    P->SetTestSpeedFactor(1); M->MaxWalkSpeed=240.f;
    P->SetTestSpeedFactor(3); P->Move(FInputActionValue(FVector2D(0,1))); P->StartSprintHold(FInputActionValue(true));
    TestEqual(TEXT("Existing custom baseline supported"), M->MaxWalkSpeed, 1080.f);
    P->StopSprintHold(FInputActionValue(false)); P->SetTestSpeedFactor(1);
    TestEqual(TEXT("Custom baseline restored exactly"), M->MaxWalkSpeed, 240.f);
    return true;
}
#endif
