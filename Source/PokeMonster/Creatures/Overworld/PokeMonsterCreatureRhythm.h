#pragma once
#include "CoreMinimal.h"
#include "PokeMonsterCreatureActivities.h"
#include "PokeMonsterCreatureRhythm.generated.h"
class UPokeMonsterWorldClockSettings;

UENUM(BlueprintType)
enum class EPokeMonsterActivityRhythm : uint8 { Diurnal, Nocturnal, Crepuscular, Flexible };

/** Multipliers on the existing activity profile, not another scheduler or clock. */
USTRUCT(BlueprintType)
struct POKEMONSTER_API FPokeMonsterCreatureRhythm
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite) EPokeMonsterActivityRhythm Rhythm=EPokeMonsterActivityRhythm::Flexible;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float IndividualOffsetMinutes=45.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ActiveWander=1.35f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float QuietWander=.25f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ActiveForage=1.6f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float QuietForage=.35f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ActiveSocial=1.4f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float QuietSocial=.15f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ActiveRest=.6f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float QuietRest=2.2f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float ActiveSleep=.15f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float QuietSleep=8.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float QuietAcceptance=.2f;
 bool IsValid() const;
 float ActivityAt(double SecondsOfDay,float IndividualOffset,const UPokeMonsterWorldClockSettings& Clock) const;
 FPokeMonsterCreatureActivityProfile Weight(const FPokeMonsterCreatureActivityProfile& Base,float Activity) const;
};
USTRUCT()
struct POKEMONSTER_API FPokeMonsterSpeciesRhythm
{
 GENERATED_BODY()
 UPROPERTY(EditAnywhere) FName Species;
 UPROPERTY(EditAnywhere) FPokeMonsterCreatureRhythm Profile;
};
/** Six opt-in VisualV2 species, editable in DefaultGame.ini without code or model changes. */
UCLASS(Config=Game,DefaultConfig)
class POKEMONSTER_API UPokeMonsterCreatureRhythmSettings : public UObject
{
 GENERATED_BODY()
public:
 UPROPERTY(Config,EditAnywhere) bool bEnableRhythms=true;
 UPROPERTY(Config,EditAnywhere) TArray<FPokeMonsterSpeciesRhythm> SpeciesProfiles;
 bool Find(FName Species,FPokeMonsterCreatureRhythm& Result) const;
};
