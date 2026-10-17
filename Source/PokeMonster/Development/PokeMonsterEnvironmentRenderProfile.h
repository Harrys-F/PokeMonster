#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Info.h"
#include "HAL/IConsoleManager.h"
#include "PokeMonsterEnvironmentRenderProfile.generated.h"

/** A tagged, reversible renderer override. Higher-priority user overrides are respected. */
struct POKEMONSTER_API FPokeMonsterEnvironmentCVarOverride
{
    FString Name, PreviousValue, AppliedValue;
    EConsoleVariableFlags PreviousPriority = ECVF_SetByConstructor;
    bool bOwned = false;
    bool Apply(const TCHAR* VariableName, const TCHAR* Value);
    void Restore();
};

/** Experimental presentation only: no tick, collision, input, or gameplay references.
 * Explicitly restricted to the separate EnvironmentPerfV1 map. Never saves config.
 */
UCLASS(NotBlueprintable)
class POKEMONSTER_API APokeMonsterEnvironmentRenderProfile : public AInfo
{
    GENERATED_BODY()
public:
    APokeMonsterEnvironmentRenderProfile();
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type Reason) override;
    static bool IsTargetLevelName(const FString& Name);

    UPROPERTY(EditAnywhere, Category="Environment Experiment")
    bool bEnableHalfResolutionLumenIntegration = true;

    UPROPERTY(EditAnywhere, Category="Environment Experiment")
    bool bEnableTwoRayDirectionalShadows = true;

private:
    TArray<FPokeMonsterEnvironmentCVarOverride> Overrides;
};
