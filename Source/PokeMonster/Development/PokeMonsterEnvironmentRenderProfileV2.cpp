#include "PokeMonsterEnvironmentRenderProfileV2.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
namespace { TWeakObjectPtr<APokeMonsterEnvironmentRenderProfileV2> OwnerV2; }
APokeMonsterEnvironmentRenderProfileV2::APokeMonsterEnvironmentRenderProfileV2()
{
    PrimaryActorTick.bCanEverTick = false;
    SetActorEnableCollision(false);
    RendererOverrides.Add(TEXT("r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor"), TEXT("2"));
    RendererOverrides.Add(TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"), TEXT("2"));
}
bool APokeMonsterEnvironmentRenderProfileV2::IsTargetLevelName(const FString& Name)
{
    return Name == TEXT("Dev_TestMap_EnvironmentPerfV2");
}
void APokeMonsterEnvironmentRenderProfileV2::BeginPlay()
{
    Super::BeginPlay();
    SetRenderingOverridesEnabled(true);
}
void APokeMonsterEnvironmentRenderProfileV2::SetRenderingOverridesEnabled(bool bEnabled)
{
    if (!bEnabled)
    {
        for (auto& Scope : Scopes) Scope.Restore();
        Scopes.Empty();
        if (OwnerV2.Get() == this) OwnerV2.Reset();
        return;
    }
    if (!Scopes.IsEmpty()) return;
    if (!GetWorld() || !GetWorld()->IsGameWorld() || !IsTargetLevelName(UGameplayStatics::GetCurrentLevelName(this, true)) || OwnerV2.IsValid()) return;
    OwnerV2 = this;
    for (const auto& Pair : RendererOverrides)
        Scopes.AddDefaulted_GetRef().Apply(*Pair.Key, *Pair.Value);
}
void APokeMonsterEnvironmentRenderProfileV2::EndPlay(const EEndPlayReason::Type Reason)
{
    SetRenderingOverridesEnabled(false);
    Super::EndPlay(Reason);
}
