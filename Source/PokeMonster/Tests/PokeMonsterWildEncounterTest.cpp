#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Encounter/PokeMonsterEncounterProfile.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Encounter/PokeMonsterWildEncounterZone.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Engine/AssetManager.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterWildEncounterTest,
	"PokeMonster.Encounter.WildProfileAndSources",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterWildEncounterTest::RunTest(const FString& Parameters)
{
	auto* Asset = LoadObject<UPokeMonsterEncounterProfile>(nullptr,
		TEXT("/Game/Data/Encounters/DA_DevWild.DA_DevWild"));
	if (!TestNotNull(TEXT("Wild profile loads"), Asset)) return false;
	TestEqual(TEXT("Profile primary type"), Asset->GetPrimaryAssetId().PrimaryAssetType,
		FPrimaryAssetType(TEXT("EncounterProfile")));
	TestEqual(TEXT("Asset manager discovers the profile for cooking"),
		UAssetManager::Get().GetPrimaryAssetPath(Asset->GetPrimaryAssetId()), FSoftObjectPath(Asset));
	auto* Grass = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	auto* Fire = LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,
		TEXT("/Game/Data/Creatures/DA_TestFire.DA_TestFire"));
	auto* Normal = LoadObject<UPokeMonsterMoveData>(nullptr,
		TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
	if (!TestNotNull(TEXT("Grass test species"), Grass)
		|| !TestNotNull(TEXT("Fire test species"), Fire)
		|| !TestNotNull(TEXT("Test move"), Normal)) return false;

	FPokeMonsterEncounterContext Context;
	FRandomStream First(3817), Second(3817);
	FPokeMonsterCreatureInstance A, B;
	int32 FirstIndex = INDEX_NONE;
	if (!TestTrue(TEXT("Profile rolls a creature"), Asset->Roll(Context, First, A, &FirstIndex))) return false;
	TestTrue(TEXT("Rolled species comes from profile"), Asset->Entries.IsValidIndex(FirstIndex)
		&& A.Species.ToSoftObjectPath() == Asset->Entries[FirstIndex].Species.ToSoftObjectPath());
	TestTrue(TEXT("Rolled level comes from profile"), A.Level >= Asset->Entries[FirstIndex].MinLevel
		&& A.Level <= Asset->Entries[FirstIndex].MaxLevel);
	TestTrue(TEXT("Rolled move has its own PP"), A.GetMoveSlots()[0].GetCurrentPP() > 0);
	if (!TestTrue(TEXT("Same seed can be replayed"), Asset->Roll(Context, Second, B))) return false;
	TestEqual(TEXT("Same seed selects the same species"), A.Species.ToSoftObjectPath(), B.Species.ToSoftObjectPath());
	TestEqual(TEXT("Same seed selects the same level"), A.Level, B.Level);
	TestTrue(TEXT("Each roll has an individual identity"), A.InstanceId != B.InstanceId);

	auto* Weighted = NewObject<UPokeMonsterEncounterProfile>();
	FPokeMonsterWildEncounterEntry Low;
	Low.Species = Grass;
	Low.MinLevel = 4;
	Low.MaxLevel = 6;
	Low.Weight = 1;
	Low.Moves.Add(Normal);
	FPokeMonsterWildEncounterEntry High = Low;
	High.Species = Fire;
	High.Weight = 3;
	Weighted->Entries = {Low, High};
	FRandomStream WeightStream(14);
	int32 HighCount = 0;
	for (int32 Roll = 0; Roll < 1000; ++Roll)
	{
		int32 EntryIndex = INDEX_NONE;
		FPokeMonsterCreatureInstance Creature;
		if (!Weighted->Roll(Context, WeightStream, Creature, &EntryIndex)) return false;
		if (EntryIndex == 1) ++HighCount;
		if (Creature.Level < 4 || Creature.Level > 6) return false;
	}
	TestTrue(TEXT("Three-to-one weight dominates across seeded rolls"), HighCount > 680 && HighCount < 820);
	Weighted->Entries[1].Time = EPokeMonsterEncounterTime::Night;
	Weighted->Entries[1].RegionId = TEXT("Forest");
	Weighted->Entries[1].RequiredCondition = TEXT("StoryGate");
	Context.Time = EPokeMonsterEncounterTime::Day;
	FRandomStream DayStream(9);
	int32 DayIndex = INDEX_NONE;
	TestTrue(TEXT("Optional filters leave matching entry"), Weighted->Roll(Context, DayStream, A, &DayIndex));
	TestEqual(TEXT("Day rejects night-only entry"), DayIndex, 0);
	Context.Time = EPokeMonsterEncounterTime::Night;
	Context.RegionId = TEXT("Forest");
	Context.ActiveConditions.Add(TEXT("StoryGate"));
	TestTrue(TEXT("Time, region and condition match together"), Weighted->Entries[1].Matches(Context));
	Context.ActiveConditions.Empty();
	TestFalse(TEXT("Missing special condition excludes entry"), Weighted->Entries[1].Matches(Context));

	TestTrue(TEXT("Visible actor implements interaction"),
		APokeMonsterVisibleWildCreatureActor::StaticClass()->ImplementsInterface(UPokeMonsterInteractable::StaticClass()));
	TestFalse(TEXT("Visible actor points at profile"),
		GetDefault<APokeMonsterVisibleWildCreatureActor>()->Profile.IsNull());
	TestFalse(TEXT("Zone points at profile"), GetDefault<APokeMonsterWildEncounterZone>()->Profile.IsNull());
	FPokeMonsterEncounterStartData Visible, Zone;
	if (!TestTrue(TEXT("Visible source prepares shared battle data"),
		UPokeMonsterEncounterSubsystem::PrepareWildEncounter(Asset, FPokeMonsterEncounterContext(),
			EPokeMonsterEncounterSource::VisibleCreature, nullptr, 3817, TEXT("Visible"), Visible))) return false;
	if (!TestTrue(TEXT("Zone source prepares shared battle data"),
		UPokeMonsterEncounterSubsystem::PrepareWildEncounter(Asset, FPokeMonsterEncounterContext(),
			EPokeMonsterEncounterSource::Zone, nullptr, 5719, TEXT("Zone"), Zone))) return false;
	TestEqual(TEXT("Visible uses wild battle kind"), Visible.Kind, EPokeMonsterEncounterKind::Wild);
	TestEqual(TEXT("Zone uses wild battle kind"), Zone.Kind, EPokeMonsterEncounterKind::Wild);
	TestEqual(TEXT("Visible source survives handoff"), Visible.Source, EPokeMonsterEncounterSource::VisibleCreature);
	TestEqual(TEXT("Zone source survives handoff"), Zone.Source, EPokeMonsterEncounterSource::Zone);
	TestEqual(TEXT("Visible prepares exactly one opponent"), Visible.OpponentTeam.Num(), 1);
	TestEqual(TEXT("Zone prepares exactly one opponent"), Zone.OpponentTeam.Num(), 1);
	TestTrue(TEXT("Both opponents have valid individual data"),
		Visible.OpponentTeam[0].IsValid() && Zone.OpponentTeam[0].IsValid());
	return true;
}
#endif
