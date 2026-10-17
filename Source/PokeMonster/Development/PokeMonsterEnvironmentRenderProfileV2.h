#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Info.h"
#include "PokeMonsterEnvironmentRenderProfile.h"
#include "PokeMonsterEnvironmentRenderProfileV2.generated.h"

/** Explicit experimental configuration, restricted to the independent V2 test world. */
UCLASS(NotBlueprintable)
class POKEMONSTER_API APokeMonsterEnvironmentRenderProfileV2 : public AInfo
{
    GENERATED_BODY()
public:
    APokeMonsterEnvironmentRenderProfileV2();
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
