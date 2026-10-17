#include "PokeMonsterEnvironmentRenderProfile.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"

namespace
{
    const FName ProfileTag(TEXT("PokeMonsterEnvironmentPerfV1"));
    TWeakObjectPtr<APokeMonsterEnvironmentRenderProfile> ProfileOwner;
}

bool FPokeMonsterEnvironmentCVarOverride::Apply(const TCHAR* VariableName, const TCHAR* Value)
{
    check(!bOwned);
    IConsoleVariable* Variable = IConsoleManager::Get().FindConsoleVariable(VariableName);
    if (!Variable) return false;
    const auto Priority = static_cast<EConsoleVariableFlags>(Variable->GetFlags() & ECVF_SetByMask);
    if (Priority > ECVF_SetByCode) return false;
    Name = VariableName;
    PreviousValue = Variable->GetString();
    PreviousPriority = Priority;
    AppliedValue = Value;
    Variable->Set(Value, ECVF_SetByCode, ProfileTag);
    bOwned = Variable->GetString() == AppliedValue && (Variable->GetFlags() & ECVF_SetByMask) == ECVF_SetByCode;
    return bOwned;
}

void FPokeMonsterEnvironmentCVarOverride::Restore()
{
    if (!bOwned) return;
    if (IConsoleVariable* Variable = IConsoleManager::Get().FindConsoleVariable(*Name))
    {
        const bool bStillOwned = Variable->GetString() == AppliedValue && (Variable->GetFlags() & ECVF_SetByMask) == ECVF_SetByCode;
        Variable->Unset(ECVF_SetByCode, ProfileTag);
        if (bStillOwned)
        {
            Variable->ClearFlags(ECVF_SetByMask);
            Variable->Set(*PreviousValue, PreviousPriority);
        }
    }
    bOwned = false;
}

APokeMonsterEnvironmentRenderProfile::APokeMonsterEnvironmentRenderProfile()
{
    PrimaryActorTick.bCanEverTick = false;
    SetActorEnableCollision(false);
}

bool APokeMonsterEnvironmentRenderProfile::IsTargetLevelName(const FString& Name)
{
    return Name == TEXT("Dev_TestMap_EnvironmentPerfV1");
}

void APokeMonsterEnvironmentRenderProfile::BeginPlay()
{
    Super::BeginPlay();
    if (!GetWorld() || !GetWorld()->IsGameWorld() || !IsTargetLevelName(UGameplayStatics::GetCurrentLevelName(this, true))) return;
    if (ProfileOwner.IsValid())
    {
        UE_LOG(LogTemp, Warning, TEXT("ENV_PROFILE skipped: another experimental world already owns the renderer scope"));
        return;
    }
    ProfileOwner = this;
    if (bEnableHalfResolutionLumenIntegration) Overrides.AddDefaulted_GetRef().Apply(TEXT("r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor"), TEXT("2"));
    if (bEnableTwoRayDirectionalShadows) Overrides.AddDefaulted_GetRef().Apply(TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"), TEXT("2"));
    UE_LOG(LogTemp, Display, TEXT("ENV_PROFILE applied only in %s; no persistent config write"), *GetWorld()->GetName());
}

void APokeMonsterEnvironmentRenderProfile::EndPlay(const EEndPlayReason::Type Reason)
{
    for (auto& Override : Overrides) Override.Restore();
    Overrides.Empty();
    if (ProfileOwner.Get() == this) ProfileOwner.Reset();
    Super::EndPlay(Reason);
}
