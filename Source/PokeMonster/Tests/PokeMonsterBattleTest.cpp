#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "../Battle/PokeMonsterBattleLibrary.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Engine/AssetManager.h"
#include "UObject/UnrealType.h"

namespace
{
	using T = EPokeMonsterCreatureType;
	using C = EPokeMonsterMoveCategory;
	using B = UPokeMonsterBattleLibrary;
	UPokeMonsterMoveData* MakeMove()
	{
		auto* Move = NewObject<UPokeMonsterMoveData>();
		Move->InternalId = TEXT("TransientTestMove");
		Move->DisplayName = FText::FromString(TEXT("Transient test move"));
		return Move;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterMoveDataTest, "PokeMonster.Moves.DataAssetsAndSlots",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterMoveDataTest::RunTest(const FString& Parameters)
{
	struct FExpected { const TCHAR* Id; T Type; C Category; int32 Power; int32 PP; };
	const FExpected Expected[] = {
		{TEXT("TestNormalPhysical"), T::Normal, C::Physical, 40, 35},
		{TEXT("TestFireSpecial"), T::Fire, C::Special, 50, 25},
		{TEXT("TestStatus"), T::Normal, C::Status, 0, 20}
	};
	auto* Species = NewObject<UPokeMonsterCreatureSpeciesData>();
	auto First = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 10);
	auto Second = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 10);
	TestEqual(TEXT("Exactly four slots per creature"), First.GetMoveSlots().Num(), 4);
	for (const auto& Slot : First.GetMoveSlots())
	{
		TestTrue(TEXT("Unassigned slot has no move"), Slot.GetMove().IsNull());
		TestEqual(TEXT("Unassigned slot has no current PP"), Slot.GetCurrentPP(), 0);
		TestEqual(TEXT("Unassigned slot has no maximum PP"), Slot.GetMaxPP(), 0);
	}
	TestFalse(TEXT("Empty slot cannot consume PP"), First.ConsumeMovePP(0));
	int32 Index = 0;
	for (const auto& Ref : Expected)
	{
		const FString Path = FString::Printf(TEXT("/Game/Data/Moves/DA_%s.DA_%s"), Ref.Id, Ref.Id);
		auto* Move = LoadObject<UPokeMonsterMoveData>(nullptr, *Path);
		if (!TestNotNull(*Path, Move)) return false;
		TestTrue(TEXT("Loaded move data is configured"), Move->IsConfigured());
		TestEqual(TEXT("Stable internal ID"), Move->InternalId, FName(Ref.Id));
		TestFalse(TEXT("Display name exists"), Move->DisplayName.IsEmpty());
		TestEqual(TEXT("Type stored on asset"), Move->Type, Ref.Type);
		TestEqual(TEXT("Category stored on asset"), Move->Category, Ref.Category);
		TestEqual(TEXT("Power stored on asset"), Move->BasePower, Ref.Power);
		TestEqual(TEXT("Maximum PP stored on asset"), Move->MaxPP, Ref.PP);
		TestEqual(TEXT("Primary asset type"), Move->GetPrimaryAssetId().PrimaryAssetType, FPrimaryAssetType(TEXT("CreatureMove")));
		TestEqual(TEXT("Asset manager discovers the move for loading/cooking"),
			UAssetManager::Get().GetPrimaryAssetPath(Move->GetPrimaryAssetId()), FSoftObjectPath(Move));
		TestTrue(TEXT("Move can be assigned to an individual slot"), B::AssignMove(First, Index, Move));
		TestTrue(TEXT("Another creature can reference the same data"), Second.AssignMove(Index, Move));
		TestEqual(TEXT("Assignment starts at full PP"), First.GetMoveSlots()[Index].GetCurrentPP(), Ref.PP);
		TestEqual(TEXT("Slot records maximum PP"), First.GetMoveSlots()[Index].GetMaxPP(), Ref.PP);
		TestTrue(TEXT("Slot references shared move asset"), First.GetMoveSlots()[Index].GetMove().Get() == Move);
		TestTrue(TEXT("PP consumption succeeds"), B::ConsumeMovePP(First, Index));
		TestEqual(TEXT("Exactly one PP consumed"), First.GetMoveSlots()[Index].GetCurrentPP(), Ref.PP - 1);
		TestEqual(TEXT("Other instance PP unaffected"), Second.GetMoveSlots()[Index].GetCurrentPP(), Ref.PP);
		TestEqual(TEXT("Shared move data unchanged"), Move->MaxPP, Ref.PP);
		TestFalse(TEXT("Overdrawing PP is rejected"), First.ConsumeMovePP(Index, Ref.PP));
		TestFalse(TEXT("Negative PP cost is rejected"), First.ConsumeMovePP(Index, -1));
		TestFalse(TEXT("Zero PP cost is rejected"), First.ConsumeMovePP(Index, 0));
		TestFalse(TEXT("Null assignment is rejected"), First.AssignMove(Index, nullptr));
		TestEqual(TEXT("Rejected operations are atomic"), First.GetMoveSlots()[Index].GetCurrentPP(), Ref.PP - 1);
		TestTrue(TEXT("Remaining PP can be consumed"), First.ConsumeMovePP(Index, Ref.PP - 1));
		TestFalse(TEXT("Exhausted move cannot be used"), First.ConsumeMovePP(Index));
		++Index;
	}
	auto* Move = MakeMove();
	TestTrue(TEXT("Fourth slot is usable"), First.AssignMove(3, Move));
	TestFalse(TEXT("Negative slot is rejected"), First.AssignMove(-1, Move));
	TestFalse(TEXT("Fifth slot is rejected"), First.AssignMove(4, Move));
	TestFalse(TEXT("Out-of-range consumption is rejected"), First.ConsumeMovePP(4));
	Move->MaxPP = 0;
	TestFalse(TEXT("Invalid move data cannot be assigned"), First.AssignMove(0, Move));
	TestTrue(TEXT("Progression remains available with move slots"), First.AddExperience(100000).bSucceeded);
	TestEqual(TEXT("Level-ups do not refill PP"), First.GetMoveSlots()[0].GetCurrentPP(), 0);
	TestEqual(TEXT("Level-ups preserve four slots"), First.GetMoveSlots().Num(), 4);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterHitTest, "PokeMonster.Battle.HitCheck",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterHitTest::RunTest(const FString& Parameters)
{
	auto* Move = MakeMove();
	for (const int32 Accuracy : {0, 1, 75, 100})
	{
		Move->Accuracy = Accuracy;
		int32 Hits = 0;
		for (int32 Roll = 0; Roll < 100; ++Roll) Hits += B::CheckHit(Move, Roll) ? 1 : 0;
		TestEqual(TEXT("Uniform rolls produce the configured accuracy exactly"), Hits, Accuracy);
	}
	Move->Accuracy = 75;
	TestTrue(TEXT("Last successful roll"), B::CheckHit(Move, 74));
	TestFalse(TEXT("First missing roll"), B::CheckHit(Move, 75));
	TestFalse(TEXT("Negative roll is invalid"), B::CheckHit(Move, -1));
	TestFalse(TEXT("Roll 100 is invalid"), B::CheckHit(Move, 100));
	TestFalse(TEXT("Missing move cannot hit"), B::CheckHit(nullptr, 0));
	Move->Accuracy = 101;
	TestFalse(TEXT("Out-of-range accuracy is invalid"), B::CheckHit(Move, 0));
	Move->Accuracy = 100;
	Move->Category = C::Status;
	Move->BasePower = 0;
	TestTrue(TEXT("Status moves use the same accuracy check"), B::CheckHit(Move, 99));
	// Accepted attempts consume PP even if the separate hit check misses.
	FPokeMonsterMoveSlot Slot;
	Slot.AssignMove(Move);
	Move->Accuracy = 0;
	TestTrue(TEXT("An accepted attempt consumes PP"), Slot.ConsumePP());
	TestFalse(TEXT("Attempt misses"), B::CheckHit(Move, 0));
	TestEqual(TEXT("A miss does not refund or consume a second PP"), Slot.GetCurrentPP(), Move->MaxPP - 1);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterTypeTest, "PokeMonster.Battle.TypeChart",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterTypeTest::RunTest(const FString& Parameters)
{
	// Independent dense reference: attacking rows, defending columns in explicit order.
	const T Types[] = {T::Normal, T::Fire, T::Water, T::Electric, T::Grass, T::Ice, T::Fighting,
		T::Poison, T::Ground, T::Flying, T::Psychic, T::Bug, T::Rock, T::Ghost, T::Dragon, T::Dark, T::Steel};
	const float H = 0.5f;
	const float Expected[17][17] = {
		{1,1,1,1,1,1,1,1,1,1,1,1,H,0,1,1,H},
		{1,H,H,1,2,2,1,1,1,1,1,2,H,1,H,1,2},
		{1,2,H,1,H,1,1,1,2,1,1,1,2,1,H,1,1},
		{1,1,2,H,H,1,1,1,0,2,1,1,1,1,H,1,1},
		{1,H,2,1,H,1,1,H,2,H,1,H,2,1,H,1,H},
		{1,H,H,1,2,H,1,1,2,2,1,1,1,1,2,1,H},
		{2,1,1,1,1,2,1,H,1,H,H,H,2,0,1,2,2},
		{1,1,1,1,2,1,1,H,H,1,1,1,H,H,1,1,0},
		{1,2,1,2,H,1,1,2,1,0,1,H,2,1,1,1,2},
		{1,1,1,H,2,1,2,1,1,1,1,2,H,1,1,1,H},
		{1,1,1,1,1,1,2,2,1,1,H,1,1,1,1,0,H},
		{1,H,1,1,2,1,H,H,1,H,2,1,1,H,1,2,H},
		{1,2,1,1,1,2,H,1,H,2,1,2,1,1,1,1,H},
		{0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,H,H},
		{1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,H},
		{1,1,1,1,1,1,H,1,1,1,2,1,1,2,1,H,H},
		{1,H,H,H,1,2,1,1,1,1,1,1,2,1,1,1,H}
	};
	for (int32 A = 0; A < 17; ++A)
	{
		for (int32 D = 0; D < 17; ++D)
		{
			TestEqual(FString::Printf(TEXT("Type pair %d -> %d"), A, D), B::GetTypeMultiplier(Types[A], Types[D]), Expected[A][D]);
		}
	}
	TestEqual(TEXT("Double weakness"), B::GetTypeMultiplier(T::Fire, T::Grass, T::Steel), 4.0f);
	TestEqual(TEXT("Double resistance"), B::GetTypeMultiplier(T::Fire, T::Water, T::Dragon), 0.25f);
	TestEqual(TEXT("Opposing modifiers cancel"), B::GetTypeMultiplier(T::Fire, T::Grass, T::Water), 1.0f);
	TestEqual(TEXT("Immunity dominates weakness"), B::GetTypeMultiplier(T::Electric, T::Water, T::Ground), 0.0f);
	TestEqual(TEXT("Swapping target types is equivalent"), B::GetTypeMultiplier(T::Electric, T::Ground, T::Water), 0.0f);
	TestEqual(TEXT("Duplicate type is not applied twice"), B::GetTypeMultiplier(T::Fire, T::Grass, T::Grass), 2.0f);
	TestEqual(TEXT("Missing attack type is rejected"), B::GetTypeMultiplier(T::None, T::Normal), -1.0f);
	TestEqual(TEXT("Missing primary type is rejected"), B::GetTypeMultiplier(T::Normal, T::None), -1.0f);
	TestEqual(TEXT("Unknown secondary type is rejected"), B::GetTypeMultiplier(T::Normal, T::Normal, static_cast<T>(255)), -1.0f);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterDamageTest, "PokeMonster.Battle.Damage",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterDamageTest::RunTest(const FString& Parameters)
{
	auto* Species = NewObject<UPokeMonsterCreatureSpeciesData>();
	auto* TargetSpecies = NewObject<UPokeMonsterCreatureSpeciesData>();
	auto Attacker = FPokeMonsterCreatureInstance::CreateFromSpecies(Species, 50);
	auto Defender = FPokeMonsterCreatureInstance::CreateFromSpecies(TargetSpecies, 50);
	auto* Move = MakeMove();
	Move->BasePower = 50;
	Attacker.CalculatedStats.Attack = 100;
	Attacker.CalculatedStats.SpecialAttack = 20;
	Defender.CalculatedStats.Defense = 50;
	Defender.CalculatedStats.SpecialDefense = 100;
	const int32 OriginalHP = Defender.CurrentHP;
	TestTrue(TEXT("Valid physical calculation"), B::CalculateDamage(Attacker, Defender, Move).bValid);
	TestEqual(TEXT("Physical uses Attack / Defense"), B::CalculateDamage(Attacker, Defender, Move).Damage, 46);
	Move->Category = C::Special;
	TestEqual(TEXT("Special uses SpecialAttack / SpecialDefense"), B::CalculateDamage(Attacker, Defender, Move).Damage, 6);
	Move->Category = C::Physical;
	Move->BasePower = 100;
	TestEqual(TEXT("Power affects damage"), B::CalculateDamage(Attacker, Defender, Move).Damage, 90);
	Move->BasePower = 50;
	auto Lower = Attacker;
	Lower.Level = 10;
	TestEqual(TEXT("Attacker level affects damage"), B::CalculateDamage(Lower, Defender, Move).Damage, 14);
	FEnumProperty* Primary = FindFProperty<FEnumProperty>(TargetSpecies->GetClass(), TEXT("PrimaryType"));
	FEnumProperty* Secondary = FindFProperty<FEnumProperty>(TargetSpecies->GetClass(), TEXT("SecondaryType"));
	if (!TestNotNull(TEXT("Primary type property"), Primary) || !TestNotNull(TEXT("Secondary type property"), Secondary)) return false;
	const auto SetTargetTypes = [&](T First, T Second = T::None)
	{
		Primary->GetUnderlyingProperty()->SetIntPropertyValue(Primary->ContainerPtrToValuePtr<void>(TargetSpecies), uint64(First));
		Secondary->GetUnderlyingProperty()->SetIntPropertyValue(Secondary->ContainerPtrToValuePtr<void>(TargetSpecies), uint64(Second));
	};
	Move->Type = T::Fire;
	SetTargetTypes(T::Grass);
	TestEqual(TEXT("Weakness doubles damage"), B::CalculateDamage(Attacker, Defender, Move).Damage, 92);
	SetTargetTypes(T::Water);
	TestEqual(TEXT("Resistance halves damage"), B::CalculateDamage(Attacker, Defender, Move).Damage, 23);
	SetTargetTypes(T::Grass, T::Steel);
	TestEqual(TEXT("Both species types affect damage"), B::CalculateDamage(Attacker, Defender, Move).Damage, 184);
	Move->Type = T::Normal;
	SetTargetTypes(T::Ghost);
	const auto Immune = B::CalculateDamage(Attacker, Defender, Move);
	TestTrue(TEXT("Immunity is a valid outcome"), Immune.bValid);
	TestEqual(TEXT("Immunity is exactly zero damage"), Immune.Damage, 0);
	TestEqual(TEXT("Multiplier exposes immunity"), Immune.TypeMultiplier, 0.0f);
	Move->Category = C::Status;
	Move->BasePower = 0;
	TestTrue(TEXT("Status data accepted"), B::CalculateDamage(Attacker, Defender, Move).bValid);
	TestEqual(TEXT("Status causes no direct damage"), B::CalculateDamage(Attacker, Defender, Move).Damage, 0);
	Move->Category = C::Physical;
	TestFalse(TEXT("Zero power is invalid for direct damage"), B::CalculateDamage(Attacker, Defender, Move).bValid);
	Move->BasePower = 1;
	Move->Type = T::Fire;
	SetTargetTypes(T::Water, T::Dragon);
	Attacker.CalculatedStats.Attack = 1;
	Defender.CalculatedStats.Defense = MAX_int32;
	TestEqual(TEXT("Nonimmune landed damage has a one-HP floor"), B::CalculateDamage(Attacker, Defender, Move).Damage, 1);
	Defender.CalculatedStats.Defense = 0;
	TestFalse(TEXT("Zero defense is rejected without division"), B::CalculateDamage(Attacker, Defender, Move).bValid);
	Defender.CalculatedStats.Defense = 1;
	Attacker.CalculatedStats.Attack = MAX_int32;
	Move->BasePower = MAX_int32;
	SetTargetTypes(T::Grass, T::Steel);
	TestEqual(TEXT("Extreme positive values saturate safely"), B::CalculateDamage(Attacker, Defender, Move).Damage, MAX_int32);
	TestFalse(TEXT("Null move fails safely"), B::CalculateDamage(Attacker, Defender, nullptr).bValid);
	TestFalse(TEXT("Invalid creature fails safely"), B::CalculateDamage(FPokeMonsterCreatureInstance(), Defender, Move).bValid);
	TestEqual(TEXT("Calculating damage never applies it"), Defender.CurrentHP, OriginalHP);
	TestEqual(TEXT("Calculating damage never modifies base stats"), TargetSpecies->GetBaseStats().Defense, 10);
	return true;
}

#endif
