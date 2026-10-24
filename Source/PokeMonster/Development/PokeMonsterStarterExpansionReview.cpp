// Explicit runtime-only acceptance fixtures; never modify maps, assets or saves here.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "HAL/IConsoleManager.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#if !UE_BUILD_SHIPPING
namespace PMStarterReview
{
static bool Creature(const FString& Name, FPokeMonsterCreatureInstance& Out)
{
	const TSet<FString> Allowed = {TEXT("Schiggy"),TEXT("Bisasam"),TEXT("Zunderlauf"),TEXT("Pikachu"),TEXT("Myrapla"),TEXT("Enton"),TEXT("Machomei"),TEXT("Nebulak"),TEXT("Gengar"),TEXT("Glurak"),TEXT("Glutexo"),TEXT("Karpador"),TEXT("Garados"),TEXT("Raupy"),TEXT("Hornliu"),TEXT("Smettbo"),TEXT("Bibor"),TEXT("Habitak")};
	if (!Allowed.Contains(Name)) return false;
	const FString Path = TEXT("/Game/Data/Creatures/DA_") + Name + TEXT(".DA_") + Name;
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, *Path);
	if (!Species) return false;
	Out = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, Species->GetStartingLevel());
	return Out.AssignSpeciesMoves();
}
static FAutoConsoleCommand Start(TEXT("pm.StarterReview.Start"),
	TEXT("Runtime-only battle fixture: classic|world configured species ID opponent."),
	FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
	if (Args.Num() != 3 || (Args[0] != TEXT("classic") && Args[0] != TEXT("world"))) return;
	for (const auto& Context : GEngine->GetWorldContexts())
	{
		UWorld* World = Context.World();
		if (!World || !World->IsGameWorld() || !World->GetGameInstance()) continue;
		auto* Controller = World->GetFirstPlayerController();
		auto* Player = Controller ? Cast<APokeMonsterPlayerCharacter>(Controller->GetPawn()) : nullptr;
		auto* Encounter = World->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
		if (!Player || Encounter->IsEncounterActive()) return;
		FPokeMonsterCreatureInstance A, B;
		if (!Creature(Args[1], A) || !Creature(Args[2], B)) return;
		FPokeMonsterEncounterStartData Start;
		Start.EncounterId = TEXT("ExplicitStarterAcceptance");
		Start.Kind = EPokeMonsterEncounterKind::Wild;
		Start.Source = EPokeMonsterEncounterSource::VisibleCreature;
		Start.bAllowFlee = true;
		Start.PresentationMode = Args[0] == TEXT("classic")
			? EPokeMonsterBattlePresentationMode::ClassicBattle : EPokeMonsterBattlePresentationMode::WorldBattle;
		Start.PlayerTeam = {A};
		Start.OpponentTeam = {B};
		Start.RandomSeed = 51;
		Encounter->StartEncounter(Start, Player);
		return;
	}
}));
static FAutoConsoleCommand Party(TEXT("pm.StarterReview.Party"),
	TEXT("Explicit unsaved party fixture: one to six configured creature IDs, outside battle only."),
	FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
	if (Args.IsEmpty() || Args.Num() > 6) return;
	TArray<FPokeMonsterCreatureInstance> Team;
	for (const FString& Id : Args)
	{
		FPokeMonsterCreatureInstance C;
		if (!Creature(Id, C)) return;
		Team.Add(C);
	}
	for (const auto& Context : GEngine->GetWorldContexts())
	{
		UWorld* World = Context.World();
		if (!World || !World->IsGameWorld() || !World->GetGameInstance()) continue;
		auto* Encounter = World->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();
		if (!Encounter->IsEncounterActive()) Encounter->RestorePersistentState(Team,
			Encounter->GetDefeatedTrainerIds(), Encounter->GetCompletedEncounterIds());
		return;
	}
}));
}
#endif
