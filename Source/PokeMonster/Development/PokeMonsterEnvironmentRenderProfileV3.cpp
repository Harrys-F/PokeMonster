#include "PokeMonsterEnvironmentRenderProfileV3.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
namespace { TWeakObjectPtr<APokeMonsterEnvironmentRenderProfileV3> OwnerV3; }
APokeMonsterEnvironmentRenderProfileV3::APokeMonsterEnvironmentRenderProfileV3()
{
    PrimaryActorTick.bCanEverTick = false;
    SetActorEnableCollision(false);
    RendererOverrides.Add(TEXT("r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor"), TEXT("2"));
    RendererOverrides.Add(TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"), TEXT("2"));
    RendererOverrides.Add(TEXT("r.Lumen.FinalGatherMethod"), TEXT("0"));
    RendererOverrides.Add(TEXT("r.Lumen.HardwareRayTracing"), TEXT("0"));
}
bool APokeMonsterEnvironmentRenderProfileV3::IsTargetLevelName(const FString& Name)
{
    return Name == TEXT("Dev_TestMap_EnvironmentPerfV3");
}
void APokeMonsterEnvironmentRenderProfileV3::BeginPlay()
{
    Super::BeginPlay();
    SetRenderingOverridesEnabled(true);
}
void APokeMonsterEnvironmentRenderProfileV3::SetRenderingOverridesEnabled(bool bEnabled)
{
    if (!bEnabled)
    {
        for (auto& Scope : Scopes) Scope.Restore();
        Scopes.Empty();
        if (OwnerV3.Get() == this) OwnerV3.Reset();
        return;
    }
    if (!Scopes.IsEmpty()) return;
    if (!GetWorld() || !GetWorld()->IsGameWorld() || !IsTargetLevelName(UGameplayStatics::GetCurrentLevelName(this, true)) || OwnerV3.IsValid()) return;
    OwnerV3 = this;
    for (const auto& Pair : RendererOverrides)
        Scopes.AddDefaulted_GetRef().Apply(*Pair.Key, *Pair.Value);
}
void APokeMonsterEnvironmentRenderProfileV3::EndPlay(const EEndPlayReason::Type Reason)
{
    SetRenderingOverridesEnabled(false);
    Super::EndPlay(Reason);
}
