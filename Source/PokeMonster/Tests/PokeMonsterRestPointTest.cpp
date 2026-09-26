#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Interaction/PokeMonsterRestPoint.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Engine/GameInstance.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterRestPointTest, "PokeMonster.Overworld.RestPoint.HealAndSave",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterRestPointTest::RunTest(const FString& Parameters)
{
	auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
	auto* Attack = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	auto* Status = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestStatus.DA_TestStatus"));
	if (!TestNotNull(TEXT("Test species"), Species) || !TestNotNull(TEXT("Test attack"), Attack)
		|| !TestNotNull(TEXT("Test status move"), Status)) return false;
	TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
	auto First = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 20);
	auto Second = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 12);
	if (!TestTrue(TEXT("First move assigned"), First.AssignMove(0, Attack))
		|| !TestTrue(TEXT("Second move assigned"), First.AssignMove(1, Status))
		|| !TestTrue(TEXT("Other member move assigned"), Second.AssignMove(0, Attack))) return false;
	First.CurrentHP = 1;
	Second.CurrentHP = 0;
	TestTrue(TEXT("First PP reduced"), First.ConsumeMovePP(0, 3));
	TestTrue(TEXT("Second PP reduced"), First.ConsumeMovePP(1, 2));
	TestTrue(TEXT("Fainted member PP reduced"), Second.ConsumeMovePP(0, 4));
	const FGuid FirstId = First.InstanceId;
	const int64 FirstExperience = First.Experience;
	TestTrue(TEXT("Team installed"), Encounter->RestorePersistentState({First, Second},
		{TEXT("DevTrainer_RestTest")}, {TEXT("Dev_FlagRestTest")}));
	int32 SaveCalls = 0;
	const FPokeMonsterRestResult Saved = APokeMonsterRestPoint::PerformRest(Encounter, true,
		[&]
		{
			++SaveCalls;
			auto* Snapshot = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI.Get());
			return Snapshot && Snapshot->PlayerTeam.Num() == 2
				&& Snapshot->PlayerTeam[0].CurrentHP == Encounter->GetPlayerParty()[0].GetMaxHP()
				&& Snapshot->PlayerTeam[0].Moves[0].CurrentPP == Attack->MaxPP;
		});
	TestEqual(TEXT("Successful save reported"), Saved.Outcome, EPokeMonsterRestOutcome::HealedAndSaved);
	TestEqual(TEXT("Save called exactly once after healing"), SaveCalls, 1);
	TestEqual(TEXT("Two members restored"), Saved.TeamCount, 2);
	const auto& Party = Encounter->GetPlayerParty();
	TestEqual(TEXT("First HP full"), Party[0].CurrentHP, Party[0].GetMaxHP());
	TestEqual(TEXT("Fainted member revived"), Party[1].CurrentHP, Party[1].GetMaxHP());
	TestEqual(TEXT("First move PP full"), Party[0].GetMoveSlots()[0].GetCurrentPP(), Attack->MaxPP);
	TestEqual(TEXT("Second move PP full"), Party[0].GetMoveSlots()[1].GetCurrentPP(), Status->MaxPP);
	TestEqual(TEXT("Other member PP full"), Party[1].GetMoveSlots()[0].GetCurrentPP(), Attack->MaxPP);
	TestEqual(TEXT("Identity retained"), Party[0].InstanceId, FirstId);
	TestEqual(TEXT("Experience retained"), Party[0].Experience, FirstExperience);
	TestTrue(TEXT("Trainer flag retained"), Encounter->IsTrainerDefeated(TEXT("DevTrainer_RestTest")));
	TestTrue(TEXT("World flag retained"), Encounter->IsEncounterCompleted(TEXT("Dev_FlagRestTest")));

	TArray<FPokeMonsterCreatureInstance> Damaged = Party;
	Damaged[0].CurrentHP = 2;
	TestTrue(TEXT("Team damaged again"), Encounter->RestorePersistentState(Damaged,
		Encounter->GetDefeatedTrainerIds(), Encounter->GetCompletedEncounterIds()));
	const FPokeMonsterRestResult FailedSave = APokeMonsterRestPoint::PerformRest(Encounter, true,
		[&] { ++SaveCalls; return false; });
	TestEqual(TEXT("Save failure distinguished from heal failure"), FailedSave.Outcome,
		EPokeMonsterRestOutcome::HealedSaveFailed);
	TestEqual(TEXT("Failed save was attempted"), SaveCalls, 2);
	TestEqual(TEXT("Failed save leaves healing intact"), Encounter->GetPlayerParty()[0].CurrentHP,
		Encounter->GetPlayerParty()[0].GetMaxHP());
	Damaged = Encounter->GetPlayerParty();
	Damaged[0].CurrentHP = 1;
	TestTrue(TEXT("Team damaged for heal-only case"), Encounter->RestorePersistentState(Damaged,
		Encounter->GetDefeatedTrainerIds(), Encounter->GetCompletedEncounterIds()));
	const FPokeMonsterRestResult HealOnly = APokeMonsterRestPoint::PerformRest(Encounter, false,
		[&] { ++SaveCalls; return true; });
	TestEqual(TEXT("Heal-only outcome"), HealOnly.Outcome, EPokeMonsterRestOutcome::Healed);
	TestEqual(TEXT("Heal-only did not call save"), SaveCalls, 2);
	TestTrue(TEXT("Team cleared for empty case"), Encounter->RestorePersistentState({}, {}, {}));
	const FPokeMonsterRestResult Empty = APokeMonsterRestPoint::PerformRest(Encounter, true,
		[&] { ++SaveCalls; return true; });
	TestEqual(TEXT("No team reported"), Empty.Outcome, EPokeMonsterRestOutcome::NoTeam);
	TestEqual(TEXT("No save without a team"), SaveCalls, 2);
	return true;
}
#endif
