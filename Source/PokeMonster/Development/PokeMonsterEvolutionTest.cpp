#include "PokeMonsterEvolutionTest.h"
#if WITH_EDITOR
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "HAL/IConsoleManager.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"

namespace
{
    TWeakObjectPtr<UGameInstance> TestInstance;
    FGuid TestCreature;
    // Output Log console may supply the editor world; never guess between multiple PIE instances.
    UWorld* SinglePIE()
    {
        UWorld* Result = nullptr;
        if (!GEngine) return nullptr;
        for (const auto& C : GEngine->GetWorldContexts())
            if (C.WorldType == EWorldType::PIE && C.World())
            {
                if (Result) return nullptr;
                Result = C.World();
            }
        return Result;
    }
    void Message(FOutputDevice& Out, const FString& Text)
    {
        Out.Logf(TEXT("EvolutionTest: %s"), *Text);
        if (GEngine) GEngine->AddOnScreenDebugMessage(-1, 14.f, FColor::Yellow, Text);
    }
    bool Safe(UWorld* W, bool Ending)
    {
        auto* GI = W ? W->GetGameInstance() : nullptr;
        auto* E = GI ? GI->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
        auto* D = GI ? GI->GetSubsystem<UPokeMonsterDialogueSubsystem>() : nullptr;
        auto* C = GI ? GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>() : nullptr;
        auto* PC = W ? Cast<APokeMonsterOverworldPlayerController>(W->GetFirstPlayerController()) : nullptr;
        auto* P = PC ? Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()) : nullptr;
        return E && PC && P && !E->IsEncounterActive() && !(D && D->IsDialogueActive())
            && !(C && C->IsReturningFromDefeat())
            && ((Ending && PC->GetEvolutionWidget()) || (!PC->IsMenuOpen() && !P->IsOverworldInputLocked()));
    }
    FAutoConsoleCommandWithWorldArgsAndOutputDevice List(TEXT("pm.EvolutionTest.List"),
        TEXT("PIE only: list current team using one-based slots, identity and level evolution targets."),
        FConsoleCommandWithWorldArgsAndOutputDeviceDelegate::CreateLambda([](const TArray<FString>& Args, UWorld*, FOutputDevice& Out)
        {
            auto* W = SinglePIE();
            auto* E = W && W->GetGameInstance() ? W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>() : nullptr;
            if (!E || !Args.IsEmpty()) { Message(Out, TEXT("Genau einen normalen PIE-Spieltest starten. Verwendung: pm.EvolutionTest.List")); return; }
            const auto& Team = E->GetPlayerParty();
            Message(Out, FString::Printf(TEXT("Team: %d Pokemon. Start <Teamplatz 1-6>; End stellt den Zustand vor dem Test wieder her."), Team.Num()));
            for (int32 I = 0; I < Team.Num(); ++I)
            {
                const auto* S = Team[I].Species.LoadSynchronous();
                auto Copy = Team[I]; FPrimaryAssetId Target;
                const bool Ready = PokeMonsterEvolutionTest::PrepareConditions(Copy, Target);
                Out.Logf(TEXT("%d: %s | Level %d | ID %s | %s"), I+1,
                    S ? *S->GetDisplayName().ToString() : TEXT("ungueltig"), Team[I].Level,
                    *Team[I].InstanceId.ToString(), Ready ? *FString::Printf(TEXT("Test ab Level %d -> %s"), Copy.Level, *Target.ToString()) : TEXT("keine eindeutig testbare Levelroute mit vorhandenem Zielmodell"));
            }
        }), ECVF_Cheat);
    FAutoConsoleCommandWithWorldArgsAndOutputDevice EvolutionPreviewStartCommand(TEXT("pm.EvolutionTest.Start"),
        TEXT("PIE only: Start <team slot 1-6>. Memory-only saves; reach regular level threshold, then use normal learning/evolution UI."),
        FConsoleCommandWithWorldArgsAndOutputDeviceDelegate::CreateLambda([](const TArray<FString>& Args, UWorld*, FOutputDevice& Out)
        {
            auto* W = SinglePIE();
            if (Args.Num()!=1 || Args[0].Len()!=1 || Args[0][0]<'1' || Args[0][0]>'6' || !Safe(W, false))
            { Message(Out, TEXT("Verwendung: pm.EvolutionTest.Start <1-6>. Nur ein PIE-Spiel; Kampf, Dialog und Menues zuerst schliessen.")); return; }
            auto* Auto = IConsoleManager::Get().FindConsoleVariable(TEXT("pm.Evolution.Auto"));
            if (!Auto || !Auto->GetInt()) { Message(Out, TEXT("Zuerst pm.Evolution.Auto 1 setzen; es wird kein globaler Testschalter heimlich geaendert.")); return; }
            auto* GI = W->GetGameInstance(); auto* E = GI->GetSubsystem<UPokeMonsterEncounterSubsystem>();
            auto* Save = GI->GetSubsystem<UPokeMonsterSaveSubsystem>();
            const int32 Index = FCString::Atoi(*Args[0])-1; auto Team = E->GetPlayerParty();
            FPrimaryAssetId Target;
            if (!Save || !Team.IsValidIndex(Index) || !PokeMonsterEvolutionTest::PrepareConditions(Team[Index], Target))
            { Message(Out, TEXT("Teamplatz/Route ungueltig, Zielmodell fehlt oder Bedingungen sind nicht eindeutig. Keine Aenderung.")); return; }
            if (!Save->IsPIEMemoryPreviewActive() && !Save->BeginPIEMemoryPreview())
            { Message(Out, TEXT("Speicherschutz konnte nicht gestartet werden. Keine Teamaenderung.")); return; }
            TestInstance = GI; TestCreature = Team[Index].InstanceId;
            if (!E->RestorePersistentState(Team, E->GetDefeatedTrainerIds(), E->GetCompletedEncounterIds()) || !Save->SaveCurrentGame())
            { Message(Out, TEXT("Testvorbereitung fehlgeschlagen. RAM-Schutz bleibt aktiv; pm.EvolutionTest.End oder PIE stoppen.")); return; }
            Message(Out, FString::Printf(TEXT("TEST NUR IM RAM: Teamplatz %d, Level %d -> %s. Lernangebote zuerst entscheiden; B/Enter starten, A/Esc abbrechen. End oder PIE-Stopp verwirft den Test."), Index+1, Team[Index].Level, *Target.PrimaryAssetName.ToString()));
        }), ECVF_Cheat);
    FAutoConsoleCommandWithWorldArgsAndOutputDevice EvolutionPreviewEndCommand(TEXT("pm.EvolutionTest.End"),
        TEXT("PIE only: discard the manual test, restore pre-test team/inventory/quest/checkpoint state; never writes a save."),
        FConsoleCommandWithWorldArgsAndOutputDeviceDelegate::CreateLambda([](const TArray<FString>& Args, UWorld*, FOutputDevice& Out)
        {
            auto* W = SinglePIE(); auto* GI = W ? W->GetGameInstance() : nullptr;
            auto* Save = GI ? GI->GetSubsystem<UPokeMonsterSaveSubsystem>() : nullptr;
            if (!Args.IsEmpty() || !Save || !Save->IsPIEMemoryPreviewActive())
            { Message(Out, TEXT("Kein aktiver manueller PIE-Entwicklungstest.")); return; }
            if (!Safe(W, true)) { Message(Out, TEXT("Kampf, Dialog oder anderes Menue zuerst beenden; RAM-Schutz bleibt aktiv. Alternativ PIE stoppen.")); return; }
            auto* PC = Cast<APokeMonsterOverworldPlayerController>(W->GetFirstPlayerController());
            if (PC->GetEvolutionWidget()) PC->CloseEvolutionPresentation();
            if (!Save->EndPIEMemoryPreview()) { Message(Out, TEXT("Wiederherstellung fehlgeschlagen; RAM-Schutz bleibt aktiv. PIE stoppen.")); return; }
            TestInstance.Reset(); TestCreature.Invalidate();
            Message(Out, TEXT("Test verworfen, vorheriger Sitzungszustand wiederhergestellt. Normales Speichern ist wieder aktiv. Save-Datei unveraendert."));
        }), ECVF_Cheat);
}
FGuid PokeMonsterEvolutionTest::SelectedCreature(const UWorld* World)
{
    auto* GI = World ? World->GetGameInstance() : nullptr;
    auto* Save = GI ? GI->GetSubsystem<UPokeMonsterSaveSubsystem>() : nullptr;
    return TestInstance.Get()==GI && Save && Save->IsPIEMemoryPreviewActive() ? TestCreature : FGuid();
}
bool PokeMonsterEvolutionTest::PrepareConditions(FPokeMonsterCreatureInstance& Creature, FPrimaryAssetId& Target)
{
    const auto* Species = Creature.Species.LoadSynchronous();
    if (!Creature.IsValid() || !Creature.ValidateEvolutionState() || !Species) return false;
    int32 Matches = 0; auto Prepared = Creature;
    for (const auto& Route : Species->GetEvolutions())
    {
        if (Route.Trigger != EPokeMonsterEvolutionTrigger::Level) continue;
        auto Candidate = Creature;
        const int32 Level = FMath::Max(Creature.Level, Route.MinimumLevel);
        const int64 XP = UPokeMonsterCreatureProgression::ExperienceForLevel(Creature.GetExperienceGrowthRate(), Level);
        if (!Candidate.AddExperience(FMath::Max<int64>(0, XP-Creature.Experience)).bSucceeded) continue;
        Candidate.CurrentHP = FMath::Max(1, Candidate.CurrentHP);
        Candidate.PendingEvolutionTarget = FPrimaryAssetId(); Candidate.PendingEvolutionItemId=NAME_None; Candidate.LastEvolutionOfferedLevel = 0;
        FPokeMonsterEvolutionContext Context;
        for (const auto& Option : UPokeMonsterCreatureProgression::GetEvolutionOptions(Candidate, Context))
            if (Option.TargetSpecies == Route.TargetSpecies && Option.Readiness == EPokeMonsterEvolutionReadiness::Ready)
            { Prepared = Candidate; Target = Option.TargetSpecies; ++Matches; break; }
    }
    if (Matches != 1) return false;
    Creature = MoveTemp(Prepared);
    return true;
}
#endif
