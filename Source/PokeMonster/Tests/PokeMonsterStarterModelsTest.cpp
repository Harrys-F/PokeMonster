#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterProfile.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimSequence.h"
#include "Engine/GameInstance.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStarterModelContract, "PokeMonster.Creatures.Starters.ModelContract",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FStarterModelContract::RunTest(const FString& Parameters)
{
	USkeleton* Previous = nullptr;
	for (const FString Name : {TEXT("Schiggy"), TEXT("Bisasam")})
	{
		const FString Path = TEXT("/Game/Data/Creatures/DA_") + Name + TEXT(".DA_") + Name;
		auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, *Path);
		if (!TestNotNull(*Name, Species)) return false;
		TestEqual(TEXT("Stable own species ID"), Species->GetInternalId(), FName(*Name));
		auto* Profile = Species->GetVisuals().Presentation.LoadSynchronous();
		if (!TestNotNull(TEXT("Own presentation"), Profile)) return false;
		TestTrue(TEXT("Import contract"), Profile->GetValidationErrors().IsEmpty());
		TestEqual(TEXT("Seven clips"), Profile->Clips.Num(), 7);
		TestEqual(TEXT("Anatomy-specific rig family"), Profile->RigFamily, Name == TEXT("Schiggy")
			? EPokeMonsterCreatureRigFamily::Biped : EPokeMonsterCreatureRigFamily::Quadruped);
		TestTrue(TEXT("Different skeletons"), Profile->Mesh->GetSkeleton() != Previous);
		Previous = Profile->Mesh->GetSkeleton();
		const float Height = Name == TEXT("Schiggy") ? 50.f : 70.f;
		TestEqual(TEXT("Documented scale"), Profile->ReferenceSizeCm, Height);
		TestTrue(TEXT("Actual imported mesh height"), FMath::Abs(Profile->Mesh->GetBounds().BoxExtent.Z * 2 - Height) < 1.f);
		TestNull(TEXT("No imported tail fire on other starters"), Profile->TailFlame.Get());
		TestTrue(TEXT("No effect anchors on other starters"), Profile->EffectAnchors.IsEmpty());
		for (const auto& Pair : Profile->Clips)
		{
			TestTrue(TEXT("Positive duration"), Pair.Value && Pair.Value->GetPlayLength() > 0);
			TestEqual(TEXT("No cross-species retarget"), Pair.Value->GetSkeleton(), Profile->Mesh->GetSkeleton());
		}
	}
	auto* Original = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
	TestEqual(TEXT("Glumanda ID preserved"), Original->GetInternalId(), FName(TEXT("Zunderlauf")));
	TestEqual(TEXT("Glumanda remains 60 cm"), Original->GetVisuals().Presentation.LoadSynchronous()->ReferenceSizeCm, 60.f);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStarterPersistence, "PokeMonster.Creatures.Starters.CaptureHealSave",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FStarterPersistence::RunTest(const FString& Parameters)
{
	auto* GI = NewObject<UGameInstance>();
	auto* Encounter = NewObject<UPokeMonsterEncounterSubsystem>(GI);
	auto* Inventory = NewObject<UPokeMonsterInventorySubsystem>(GI);
	TArray<FPokeMonsterCreatureInstance> Team;
	for (const FString Name : {TEXT("Schiggy"), TEXT("Bisasam")})
	{
		const FString Prefix = TEXT("/Game/Data/Creatures/DA_") + Name;
		auto* Species = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr, *(Prefix + TEXT(".DA_") + Name));
		const FString Wild = TEXT("/Game/Data/Encounters/DA_") + Name + TEXT("_Wild.DA_") + Name + TEXT("_Wild");
		auto* Pool = LoadObject<UPokeMonsterEncounterProfile>(nullptr, *Wild);
		if (!Species || !Pool) { AddError(TEXT("Missing starter data")); return false; }
		FRandomStream Random(31);
		FPokeMonsterCreatureInstance C;
		TestTrue(TEXT("Existing wild roll supports species"), Pool->Roll({}, Random, C));
		TestEqual(TEXT("Rolled stable identity"), C.Species.Get(), Species);
		TestTrue(TEXT("Species has actual original moves"), !C.GetMoveSlots()[0].GetMove().IsNull() && C.GetMoveSlots()[0].GetCurrentPP() > 0);
		C.CurrentHP = 1;
		TestTrue(TEXT("PP spent"), C.ConsumeMovePP(0, 2));
		Team.Add(C);
	}
	TestTrue(TEXT("Existing party handoff accepts both"), Encounter->RestorePersistentState(Team, {}, {}));
	TestTrue(TEXT("Common healing supports both"), Encounter->RestorePlayerPartyAtRestPoint());
	auto* Save = UPokeMonsterSaveSubsystem::CaptureSnapshot(Encounter, Inventory, GI);
	if (!TestNotNull(TEXT("Snapshot"), Save)) return false;
	TestTrue(TEXT("Clear runtime fixture"), Encounter->RestorePersistentState({}, {}, {}));
	TestTrue(TEXT("Existing schema reload"), UPokeMonsterSaveSubsystem::RestoreSnapshot(Save, Encounter, Inventory));
	if (!TestEqual(TEXT("Both creatures reloaded"), Encounter->GetPlayerParty().Num(), 2)) return false;
	for (int32 I = 0; I < 2; ++I)
	{
		const auto& C = Encounter->GetPlayerParty()[I];
		TestEqual(TEXT("Identity preserved"), C.InstanceId, Team[I].InstanceId);
		TestEqual(TEXT("Fully healed"), C.CurrentHP, C.GetMaxHP());
		TestEqual(TEXT("PP healed"), C.GetMoveSlots()[0].GetCurrentPP(), C.GetMoveSlots()[0].GetMaxPP());
	}
	return true;
}
#endif
