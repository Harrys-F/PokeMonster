#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PokeMonsterQuestData.generated.h"

UENUM(BlueprintType)
enum class EPokeMonsterQuestType : uint8 { MainStory, SideQuest };

UENUM(BlueprintType)
enum class EPokeMonsterQuestObjectiveType : uint8
{
	TalkToNPC, TrainerDefeated, WorldFlagSet, CreatureCaptured, ItemOwned, LocationInteracted
};

USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterQuestObjective
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") EPokeMonsterQuestObjectiveType Type = EPokeMonsterQuestObjectiveType::TalkToNPC;
	/** Stable dialogue, trainer, world flag, species or item identity. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") FName TargetId;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") FText Description;
};

UCLASS(BlueprintType)
class POKEMONSTER_API UPokeMonsterQuestData : public UPrimaryDataAsset
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") FName InternalId;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") FText DisplayName;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest", meta=(MultiLine="true")) FText Description;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") EPokeMonsterQuestType QuestType = EPokeMonsterQuestType::MainStory;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") TArray<FName> PrerequisiteQuestIds;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") FName CompletionFlag;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Quest") TArray<FPokeMonsterQuestObjective> Objectives;
	virtual FPrimaryAssetId GetPrimaryAssetId() const override { return FPrimaryAssetId(TEXT("Quest"), GetFName()); }
	bool IsConfigured() const;
};
