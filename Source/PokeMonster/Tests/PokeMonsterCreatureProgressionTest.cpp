#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "UObject/UnrealType.h"

using FProgression = UPokeMonsterCreatureProgression;

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterGrowthTest, "PokeMonster.Creatures.GrowthCurves",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterGrowthTest::RunTest(const FString& Parameters)
{
	struct FReference { EPokeMonsterGrowthRate Rate; int64 At10; int64 At50; int64 At100; };
	const FReference References[] = {
		{EPokeMonsterGrowthRate::Fast, 800, 100000, 800000},
		{EPokeMonsterGrowthRate::MediumFast, 1000, 125000, 1000000},
		{EPokeMonsterGrowthRate::MediumSlow, 560, 117360, 1059860},
		{EPokeMonsterGrowthRate::Slow, 1250, 156250, 1250000},
		{EPokeMonsterGrowthRate::Erratic, 1800, 125000, 600000},
		{EPokeMonsterGrowthRate::Fluctuating, 540, 142500, 1640000}
	};
	for (const FReference& Ref : References)
	{
		TestEqual(TEXT("Level 1 starts at zero XP"), FProgression::ExperienceForLevel(Ref.Rate, 1), int64(0));
		TestEqual(TEXT("Level 10 reference"), FProgression::ExperienceForLevel(Ref.Rate, 10), Ref.At10);
		TestEqual(TEXT("Level 50 reference"), FProgression::ExperienceForLevel(Ref.Rate, 50), Ref.At50);
		TestEqual(TEXT("Level 100 reference"), FProgression::ExperienceForLevel(Ref.Rate, 100), Ref.At100);
		TestEqual(TEXT("Lower bound"), FProgression::ExperienceForLevel(Ref.Rate, -10), int64(0));
		TestEqual(TEXT("Upper bound"), FProgression::ExperienceForLevel(Ref.Rate, 200), Ref.At100);
		for (int32 Level = 2; Level <= 100; ++Level)
		{
			TestTrue(FString::Printf(TEXT("Group %d increases at level %d"), int32(Ref.Rate), Level),
				FProgression::ExperienceForLevel(Ref.Rate, Level) > FProgression::ExperienceForLevel(Ref.Rate, Level - 1));
		}
	}
	TestEqual(TEXT("Unknown growth groups fail explicitly"),
		FProgression::ExperienceForLevel(static_cast<EPokeMonsterGrowthRate>(255), 10), int64(-1));
	TestEqual(TEXT("Erratic second segment"), FProgression::ExperienceForLevel(EPokeMonsterGrowthRate::Erratic, 51), int64(131324));
	TestEqual(TEXT("Erratic third segment rounding"), FProgression::ExperienceForLevel(EPokeMonsterGrowthRate::Erratic, 69), int64(267406));
	TestEqual(TEXT("Erratic final segment"), FProgression::ExperienceForLevel(EPokeMonsterGrowthRate::Erratic, 99), int64(591882));
	TestEqual(TEXT("Fluctuating first segment rounding"), FProgression::ExperienceForLevel(EPokeMonsterGrowthRate::Fluctuating, 15), int64(1957));
	TestEqual(TEXT("Fluctuating second segment"), FProgression::ExperienceForLevel(EPokeMonsterGrowthRate::Fluctuating, 16), int64(2457));
	TestEqual(TEXT("Fluctuating final segment"), FProgression::ExperienceForLevel(EPokeMonsterGrowthRate::Fluctuating, 37), int64(50653));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterProgressionTest, "PokeMonster.Creatures.Progression",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterProgressionTest::RunTest(const FString& Parameters)
{
	UPokeMonsterCreatureSpeciesData* Species = NewObject<UPokeMonsterCreatureSpeciesData>();
	FEnumProperty* GrowthProperty = FindFProperty<FEnumProperty>(Species->GetClass(), TEXT("GrowthRate"));
	if (!TestNotNull(TEXT("Growth rate is configurable on species"), GrowthProperty)) return false;
	for (const EPokeMonsterGrowthRate Rate : {EPokeMonsterGrowthRate::Fast, EPokeMonsterGrowthRate::MediumFast,
		EPokeMonsterGrowthRate::MediumSlow, EPokeMonsterGrowthRate::Slow, EPokeMonsterGrowthRate::Erratic, EPokeMonsterGrowthRate::Fluctuating})
	{
		// Only a transient test species is configured; project data assets remain untouched.
		GrowthProperty->GetUnderlyingProperty()->SetIntPropertyValue(GrowthProperty->ContainerPtrToValuePtr<void>(Species), uint64(Rate));
		auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 10);
		const int64 InitialXP = Creature.Experience;
		const int64 ToNext = Creature.GetExperienceToNextLevel();
		TestTrue(TEXT("Next level requires positive XP"), ToNext > 1);
		TestEqual(TEXT("Starts at current level's cumulative threshold"), InitialXP, FProgression::ExperienceForLevel(Rate, 10));
		Creature.CurrentHP -= 3;
		auto Result = Creature.AddExperience(ToNext - 1);
		TestTrue(TEXT("XP addition succeeds"), Result.bSucceeded);
		TestEqual(TEXT("XP is added exactly"), Creature.Experience, InitialXP + ToNext - 1);
		TestEqual(TEXT("One XP below threshold does not level up"), Creature.Level, 10);
		TestEqual(TEXT("Remaining XP is derived"), FProgression::ExperienceToNextLevel(Creature), int64(1));
		Result = FProgression::AddExperience(Creature, 1);
		TestEqual(TEXT("Exact threshold grants one level"), Result.LevelsGained, 1);
		TestEqual(TEXT("Level becomes 11"), Creature.Level, 11);
		TestEqual(TEXT("Missing HP are preserved"), Creature.CurrentHP, Creature.GetMaxHP() - 3);
		Result = Creature.AddExperience(FProgression::ExperienceForLevel(Rate, 30) - Creature.Experience + 2);
		TestEqual(TEXT("Large grants produce all intermediate level-ups"), Result.LevelsGained, 19);
		TestEqual(TEXT("Multiple levels reach requested threshold"), Creature.Level, 30);
		TestEqual(TEXT("Remainder is retained"), Creature.Experience, FProgression::ExperienceForLevel(Rate, 30) + 2);
		const int64 BeforeRejected = Creature.Experience;
		TestFalse(TEXT("Negative grants are rejected"), Creature.AddExperience(-1).bSucceeded);
		TestEqual(TEXT("Rejected grant leaves XP untouched"), Creature.Experience, BeforeRejected);
		TestTrue(TEXT("Zero grant is a valid no-op"), Creature.AddExperience(0).bSucceeded);
		Creature.CurrentHP = 0;
		Result = Creature.AddExperience(MAX_int64);
		TestEqual(TEXT("Huge grants stop at level cap"), Creature.Level, 100);
		TestEqual(TEXT("Accepted XP is capped without overflow"), Result.ExperienceAdded, FProgression::ExperienceForLevel(Rate, 100) - BeforeRejected);
		TestEqual(TEXT("Cumulative XP stops at cap"), Creature.Experience, FProgression::ExperienceForLevel(Rate, 100));
		TestEqual(TEXT("Fainted creatures are not revived"), Creature.CurrentHP, 0);
		TestEqual(TEXT("No next level at cap"), Creature.GetExperienceToNextLevel(), int64(0));
		TestEqual(TEXT("Grants at cap add nothing"), Creature.AddExperience(500).ExperienceAdded, int64(0));
	}
	TestEqual(TEXT("Requested level is clamped down"), FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 500).Level, 100);
	TestEqual(TEXT("Requested level is clamped up"), FPokeMonsterCreatureInstance::CreateFromSpecies(Species, -5).Level, 1);
	TestEqual(TEXT("Default uses species starting level"), FPokeMonsterCreatureInstance::CreateFromSpecies(Species).Level, Species->GetStartingLevel());
	auto Invalid = FPokeMonsterCreatureInstance::CreateFromSpecies(nullptr);
	TestFalse(TEXT("Missing species cannot gain XP"), Invalid.AddExperience(100).bSucceeded);
	auto Inconsistent = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 10);
	Inconsistent.Experience = 0;
	TestFalse(TEXT("Inconsistent imported state is rejected"), Inconsistent.AddExperience(10).bSucceeded);
	TestEqual(TEXT("Invalid state is not silently rewritten"), Inconsistent.Experience, int64(0));
	FPokeMonsterCreatureBaseStats Base;
	Base.HP = 45; Base.Attack = 49; Base.Defense = 50; Base.SpecialAttack = 65; Base.SpecialDefense = 66; Base.Speed = 45;
	const auto Stats = FProgression::CalculateStats(Base, 50);
	TestEqual(TEXT("HP uses base value and level"), Stats.MaxHP, 105);
	TestEqual(TEXT("Attack calculation"), Stats.Attack, 54);
	TestEqual(TEXT("Defense calculation"), Stats.Defense, 55);
	TestEqual(TEXT("Special attack calculation"), Stats.SpecialAttack, 70);
	TestEqual(TEXT("Special defense calculation"), Stats.SpecialDefense, 71);
	TestEqual(TEXT("Speed calculation"), Stats.Speed, 50);
	TestEqual(TEXT("Calculation leaves species values untouched"), Base.HP, 45);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterEvolutionTest, "PokeMonster.Creatures.EvolutionEligibility",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterEvolutionTest::RunTest(const FString& Parameters)
{
	FPokeMonsterEvolutionData Rule;
	Rule.TargetSpecies = FPrimaryAssetId(TEXT("CreatureSpecies"), TEXT("TestEvolution"));
	Rule.MinimumLevel = 20;
	FPokeMonsterEvolutionContext Context;
	TestFalse(TEXT("Below minimum level"), FProgression::IsEvolutionEligible(Rule, 19, Context));
	TestTrue(TEXT("Exact minimum level"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Rule.Trigger = Context.Trigger = EPokeMonsterEvolutionTrigger::Item;
	TestFalse(TEXT("Item trigger needs an item requirement"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Rule.RequiredItemId = TEXT("TestStone");
	TestFalse(TEXT("Wrong or absent item"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Context.UsedItemId = TEXT("TestStone");
	TestTrue(TEXT("Matching item"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Rule.RequirementId = Rule.RequiredItemId;
	Rule.RequiredItemId = NAME_None;
	TestTrue(TEXT("Legacy item requirement remains supported"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Rule.RequirementId = NAME_None;
	Rule.Trigger = Context.Trigger = EPokeMonsterEvolutionTrigger::Friendship;
	Rule.MinimumFriendship = 200;
	Context.Friendship = 199;
	TestFalse(TEXT("Insufficient friendship"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Context.Friendship = 200;
	TestTrue(TEXT("Friendship threshold"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Rule.MinimumFriendship = 0;
	Rule.Trigger = Context.Trigger = EPokeMonsterEvolutionTrigger::Location;
	Rule.RequiredLocationId = TEXT("AncientSanctum");
	TestFalse(TEXT("Wrong location"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Context.LocationId = TEXT("AncientSanctum");
	TestTrue(TEXT("Location trigger"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Rule.Trigger = Context.Trigger = EPokeMonsterEvolutionTrigger::SpecialInteraction;
	Rule.RequiredActionId = TEXT("CompleteTrial");
	TestFalse(TEXT("Missing action despite matching level and place"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Context.ActionId = TEXT("CompleteTrial");
	TestTrue(TEXT("Former trade evolution: level AND place AND action"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	TestFalse(TEXT("Matching place/action do not bypass level"), FProgression::IsEvolutionEligible(Rule, 19, Context));
	Context.LocationId = TEXT("Elsewhere");
	TestFalse(TEXT("Matching level/action do not bypass place"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Context.LocationId = Rule.RequiredLocationId;
	Context.Trigger = EPokeMonsterEvolutionTrigger::Level;
	TestFalse(TEXT("Wrong triggering event"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Context.Trigger = Rule.Trigger;
	UPokeMonsterCreatureSpeciesData* Species = NewObject<UPokeMonsterCreatureSpeciesData>();
	FArrayProperty* RulesProperty = FindFProperty<FArrayProperty>(Species->GetClass(), TEXT("Evolutions"));
	if (!TestNotNull(TEXT("Species own evolution routes"), RulesProperty)) return false;
	auto& Routes = *RulesProperty->ContainerPtrToValuePtr<TArray<FPokeMonsterEvolutionData>>(Species);
	Routes.Add(Rule);
	Routes.Add(Rule); // Equivalent routes must not duplicate the target.
	auto SelfRule = Rule;
	SelfRule.TargetSpecies = Species->GetPrimaryAssetId();
	Routes.Add(SelfRule);
	auto Creature = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 20);
	const auto Eligible = FProgression::GetEligibleEvolutions(Creature, Context);
	TestEqual(TEXT("Evaluates species routes, deduplicates and excludes self-evolution"), Eligible.Num(), 1);
	TestTrue(TEXT("Eligible target is returned"), Eligible.Contains(Rule.TargetSpecies));
	TestTrue(TEXT("Eligibility does not change the species"), Creature.Species.Get() == Species);
	TestEqual(TEXT("Eligibility does not change level"), Creature.Level, 20);
	TestEqual(TEXT("Eligibility does not consume item/context"), Context.UsedItemId, FName(TEXT("TestStone")));
	Rule.Trigger = Context.Trigger = EPokeMonsterEvolutionTrigger::Custom;
	TestFalse(TEXT("Unsupported custom triggers fail closed"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	Rule.Trigger = Context.Trigger = EPokeMonsterEvolutionTrigger::SpecialInteraction;
	Rule.TargetSpecies = FPrimaryAssetId();
	TestFalse(TEXT("Missing target is ineligible"), FProgression::IsEvolutionEligible(Rule, 20, Context));
	return true;
}

#endif
