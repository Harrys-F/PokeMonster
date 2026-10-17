#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Info.h"
#include "PokeMonsterEnvironmentRenderProfile.h"
#include "PokeMonsterEnvironmentRenderProfileV3.generated.h"

/** Explicit experimental configuration, restricted to the independent V3 test world; no baseline map effect. */
UCLASS(NotBlueprintable)
class POKEMONSTER_API APokeMonsterEnvironmentRenderProfileV3 : public AInfo
{
    GENERATED_BODY()
public:
    APokeMonsterEnvironmentRenderProfileV3();
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type Reason) override;
    static bool IsTargetLevelName(const FString& Name);
    /** Explicit reversible review switch; does not move the player or touch gameplay. */
    UFUNCTION(BlueprintCallable, Category="Environment Experiment")
    void SetRenderingOverridesEnabled(bool bEnabled);
    UPROPERTY(EditAnywhere, Category="Environment Experiment")
    TMap<FString, FString> RendererOverrides;
private:
    TArray<FPokeMonsterEnvironmentCVarOverride> Scopes;
};
