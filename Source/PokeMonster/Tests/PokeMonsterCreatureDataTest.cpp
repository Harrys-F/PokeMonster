// Copyright Epic Games, Inc. All Rights Reserved.

#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"

#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPokeMonsterCreatureDataTest,
	"PokeMonster.Creatures.DataSystem",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterCreatureDataTest::RunTest(const FString& Parameters)
{
	UPokeMonsterCreatureSpeciesData* GrassSpecies = LoadObject<UPokeMonsterCreatureSpeciesData>(
		nullptr, TEXT("/Game/Data/Creatures/DA_TestGrass.DA_TestGrass"));
	UPokeMonsterCreatureSpeciesData* FireSpecies = LoadObject<UPokeMonsterCreatureSpeciesData>(
		nullptr, TEXT("/Game/Data/Creatures/DA_TestFire.DA_TestFire"));
	UPokeMonsterCreatureSpeciesData* WaterSpecies = LoadObject<UPokeMonsterCreatureSpeciesData>(
		nullptr, TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));

	TestNotNull(TEXT("The grass test species data asset loads"), GrassSpecies);
	TestNotNull(TEXT("The fire test species data asset loads"), FireSpecies);
	TestNotNull(TEXT("The water test species data asset loads"), WaterSpecies);
	if (!GrassSpecies || !FireSpecies || !WaterSpecies)
	{
		return false;
	}

	TestEqual(TEXT("Grass species keeps its primary type"), GrassSpecies->GetPrimaryType(), EPokeMonsterCreatureType::Grass);
	TestEqual(TEXT("Fire species keeps its primary type"), FireSpecies->GetPrimaryType(), EPokeMonsterCreatureType::Fire);
	TestEqual(TEXT("Water species keeps its primary type"), WaterSpecies->GetPrimaryType(), EPokeMonsterCreatureType::Water);
	TestEqual(TEXT("An absent secondary type is stored explicitly"), GrassSpecies->GetSecondaryType(), EPokeMonsterCreatureType::None);
	TestTrue(TEXT("Base HP is available"), GrassSpecies->GetBaseStats().HP > 0);
	TestTrue(TEXT("All six base stats are available"),
		GrassSpecies->GetBaseStats().Attack > 0
		&& GrassSpecies->GetBaseStats().Defense > 0
		&& GrassSpecies->GetBaseStats().SpecialAttack > 0
		&& GrassSpecies->GetBaseStats().SpecialDefense > 0
		&& GrassSpecies->GetBaseStats().Speed > 0);
	TestEqual(TEXT("The species exposes a stable primary asset type"),
		GrassSpecies->GetPrimaryAssetId().PrimaryAssetType,
		FPrimaryAssetType(TEXT("CreatureSpecies")));

	FPokeMonsterCreatureInstance FirstCreature = FPokeMonsterCreatureInstance::CreateFromSpecies(GrassSpecies, 7);
	FPokeMonsterCreatureInstance SecondCreature = FPokeMonsterCreatureInstance::CreateFromSpecies(GrassSpecies, 7);
	TestTrue(TEXT("A runtime creature instance can be created from species data"), FirstCreature.IsValid());
	TestEqual(TEXT("The requested instance level is stored"), FirstCreature.Level, 7);
	TestEqual(TEXT("A new instance starts with the species base HP placeholder"),
		FirstCreature.CurrentHP, GrassSpecies->GetBaseStats().HP);
	TestTrue(TEXT("Each runtime creature receives an independent identity"),
		FirstCreature.InstanceId != SecondCreature.InstanceId);

	const int32 SharedBaseHP = GrassSpecies->GetBaseStats().HP;
	FirstCreature.CurrentHP = FMath::Max(0, FirstCreature.CurrentHP - 3);
	FirstCreature.Experience = 25;
	TestEqual(TEXT("Changing current HP does not alter shared species base HP"),
		GrassSpecies->GetBaseStats().HP, SharedBaseHP);
	TestEqual(TEXT("Another instance keeps its own current HP"), SecondCreature.CurrentHP, SharedBaseHP);
	TestEqual(TEXT("Individual experience remains on the runtime instance"), FirstCreature.Experience, static_cast<int64>(25));

	return true;
}

#endif
