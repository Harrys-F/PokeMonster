#include "PokeMonsterPlayerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "HAL/IConsoleManager.h"
#include "Kismet/GameplayStatics.h"

bool APokeMonsterPlayerCharacter::SetTestSpeedFactor(float Factor)
{
#if !UE_BUILD_SHIPPING
    if (!FMath::IsFinite(Factor) || (Factor != 1.f && Factor != 2.f && Factor != 3.f)) return false;
    auto* Movement = GetCharacterMovement();
    if (!Movement) return false;
    // Scale the existing walk/sprint pair once. RefreshSprint still owns all
    // sprint transitions, including its current configured walking-speed capture.
    const float Ratio = Factor / TestSpeedFactor;
    Movement->MaxWalkSpeed *= Ratio;
    NormalWalkSpeed *= Ratio;
    TestSpeedFactor = Factor;
    return true;
#else
    return false;
#endif
}

#if !UE_BUILD_SHIPPING
namespace PokeMonsterPlayerSpeedConsole
{
static FAutoConsoleCommandWithWorldAndArgs Command(
    TEXT("pm.Speed"), TEXT("1 | 2 | 3 | Status: transient player movement test factor; no time dilation or save changes."),
    FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args, UWorld* World)
{
    auto* Player = Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(World, 0));
    if (!Player || Args.Num() != 1)
    { UE_LOG(LogTemp, Display, TEXT("pm.Speed 1 | 2 | 3 | Status (active game required)")); return; }
    const FString& Value = Args[0];
    if (!Value.Equals(TEXT("Status"), ESearchCase::IgnoreCase))
    {
        if (Value != TEXT("1") && Value != TEXT("2") && Value != TEXT("3"))
        { UE_LOG(LogTemp, Display, TEXT("pm.Speed: allowed factors are 1, 2, 3; no change")); return; }
        if (!Player->SetTestSpeedFactor(FCString::Atof(*Value))) return;
    }
    UE_LOG(LogTemp, Display, TEXT("PM_SPEED factor=%.0f walk=%.2f current_limit=%.2f cm/s sprint=%s (session only)"),
        Player->GetTestSpeedFactor(), Player->GetNormalWalkSpeed(), Player->GetCharacterMovement()->MaxWalkSpeed,
        Player->IsSprinting() ? TEXT("on") : TEXT("off"));
}));
}
#endif
