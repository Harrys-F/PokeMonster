#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "UObject/StrongObjectPtr.h"
#include "UObject/UnrealType.h"
#include "UObject/GarbageCollection.h"

namespace
{
	using S = EPokeMonsterBattleSide;
	using E = EPokeMonsterBattleEventType;
	using BattleError = EPokeMonsterBattleError;
	using Phase = EPokeMonsterBattlePhase;
	using T = EPokeMonsterCreatureType;
	using C = EPokeMonsterMoveCategory;

	struct FFixture
	{
		TStrongObjectPtr<UPokeMonsterCreatureSpeciesData> SpeciesA{NewObject<UPokeMonsterCreatureSpeciesData>()};
		TStrongObjectPtr<UPokeMonsterCreatureSpeciesData> SpeciesB{NewObject<UPokeMonsterCreatureSpeciesData>()};
		TStrongObjectPtr<UPokeMonsterMoveData> MoveA{NewObject<UPokeMonsterMoveData>()};
		TStrongObjectPtr<UPokeMonsterMoveData> MoveB{NewObject<UPokeMonsterMoveData>()};
		FPokeMonsterCreatureInstance A;
		FPokeMonsterCreatureInstance B;

		FFixture()
		{
			A = FPokeMonsterCreatureInstance::CreateFromSpecies(SpeciesA.Get(), 50);
			B = FPokeMonsterCreatureInstance::CreateFromSpecies(SpeciesB.Get(), 50);
			MoveA->InternalId = TEXT("SessionTestA");
			MoveB->InternalId = TEXT("SessionTestB");
			for (auto* Move : {MoveA.Get(), MoveB.Get()})
			{
				Move->DisplayName = FText::FromString(TEXT("Session test move"));
				Move->BasePower = 50;
				Move->MaxPP = 50;
			}
			for (auto* Creature : {&A, &B})
			{
				Creature->CalculatedStats.MaxHP = Creature->CurrentHP = 500;
				Creature->CalculatedStats.Attack = Creature->CalculatedStats.Defense = 100;
				Creature->CalculatedStats.SpecialAttack = Creature->CalculatedStats.SpecialDefense = 100;
				Creature->CalculatedStats.Speed = 50;
			}
			A.AssignMove(0, MoveA.Get());
			B.AssignMove(0, MoveB.Get());
		}

		void StatusB() { MoveB->Category = C::Status; MoveB->BasePower = 0; }
		bool SetTargetType(T Primary, T Secondary = T::None)
		{
			auto* First = FindFProperty<FEnumProperty>(SpeciesB->GetClass(), TEXT("PrimaryType"));
			auto* Second = FindFProperty<FEnumProperty>(SpeciesB->GetClass(), TEXT("SecondaryType"));
			if (!First || !Second) return false;
			First->GetUnderlyingProperty()->SetIntPropertyValue(First->ContainerPtrToValuePtr<void>(SpeciesB.Get()), uint64(Primary));
			Second->GetUnderlyingProperty()->SetIntPropertyValue(Second->ContainerPtrToValuePtr<void>(SpeciesB.Get()), uint64(Secondary));
			return true;
		}
	};

	const FPokeMonsterBattleEvent* Find(const FPokeMonsterBattleResult& Result, E Type, S Source = S::None)
	{
		return Result.Events.FindByPredicate([=](const auto& Event)
		{
			return Event.Type == Type && (Source == S::None || Event.Source == Source);
		});
	}
	int32 Count(const FPokeMonsterBattleResult& Result, E Type)
	{
		int32 Num = 0;
		for (const auto& Event : Result.Events) Num += Event.Type == Type ? 1 : 0;
		return Num;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSessionOrderTest, "PokeMonster.Battle.Session.OrderAndPP",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterSessionOrderTest::RunTest(const FString& Parameters)
{
	struct FCase { int32 PriorityA; int32 PriorityB; int32 SpeedA; int32 SpeedB; S First; };
	const FCase Cases[] = {{0,1,200,10,S::B}, {2,1,10,200,S::A}, {0,0,10,20,S::B},
		{0,0,20,10,S::A}, {0,0,20,20,S::A}, {-2,-1,200,10,S::B}};
	for (const auto& Case : Cases)
	{
		FFixture F;
		F.MoveA->Priority = Case.PriorityA;
		F.MoveB->Priority = Case.PriorityB;
		F.A.CalculatedStats.Speed = Case.SpeedA;
		F.B.CalculatedStats.Speed = Case.SpeedB;
		F.A.AssignMove(1, F.MoveA.Get());
		TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());
		TestTrue(TEXT("Session accepts two valid participants"), Session->Initialize(F.A, F.B, 17).bSucceeded);
		const auto Result = Session->ResolveRound(1, 0);
		TestTrue(TEXT("Valid round resolves"), Result.bSucceeded);
		TestEqual(TEXT("Both choices are reported"), Count(Result, E::MoveChosen), 2);
		TestEqual(TEXT("Both surviving participants execute"), Count(Result, E::MoveExecuted), 2);
		const auto* Executed = Find(Result, E::MoveExecuted);
		if (!TestNotNull(TEXT("An execution event exists"), Executed)) return false;
		TestEqual(TEXT("Priority, then speed, then deterministic A tie-break"), Executed->Source, Case.First);
		TestEqual(TEXT("Execution includes previous PP"), Executed->PPBefore, 50);
		TestEqual(TEXT("Execution includes remaining PP"), Executed->PPAfter, 49);
		TestTrue(TEXT("Execution includes a valid roll"), Executed->HitRoll >= 0 && Executed->HitRoll < 100);
		TestEqual(TEXT("Selected A slot loses one PP"), Session->GetState().SideA.GetMoveSlots()[1].GetCurrentPP(), 49);
		TestEqual(TEXT("Unselected slot keeps PP"), Session->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(), 50);
		TestEqual(TEXT("B loses one PP"), Session->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(), 49);
		TestEqual(TEXT("Round number advances"), Session->GetState().RoundNumber, 1);
		TestEqual(TEXT("Survivors wait for next choices"), Session->GetState().Phase, Phase::AwaitingChoices);
		TestEqual(TEXT("No winner prematurely"), Result.Winner, S::None);
		TestEqual(TEXT("External creature HP remain untouched"), F.A.CurrentHP, 500);
		TestEqual(TEXT("External creature PP remain untouched"), F.A.GetMoveSlots()[1].GetCurrentPP(), 50);
		TestEqual(TEXT("Shared move PP remain untouched"), F.MoveA->MaxPP, 50);
		const auto* Chosen = Find(Result, E::MoveChosen, S::A);
		if (!TestNotNull(TEXT("A choice event exists"), Chosen)) return false;
		TestEqual(TEXT("Choice contains slot"), Chosen->SlotIndex, 1);
		TestEqual(TEXT("Choice contains move ID"), Chosen->MoveId, F.MoveA->GetPrimaryAssetId());
		TestEqual(TEXT("Choice contains creature ID"), Chosen->SourceInstanceId, F.A.InstanceId);
	}
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSessionDamageTest, "PokeMonster.Battle.Session.HitsAndTypes",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterSessionDamageTest::RunTest(const FString& Parameters)
{
	struct FCase { T Attack; T Primary; T Secondary; float Multiplier; E Event; };
	const FCase Cases[] = {
		{T::Fire,T::Grass,T::None,2,E::SuperEffective}, {T::Fire,T::Water,T::None,0.5f,E::NotVeryEffective},
		{T::Fire,T::Grass,T::Steel,4,E::SuperEffective}, {T::Fire,T::Water,T::Dragon,0.25f,E::NotVeryEffective},
		{T::Electric,T::Water,T::Ground,0,E::Immune}, {T::Normal,T::Ghost,T::None,0,E::Immune},
		{T::Normal,T::Normal,T::None,1,E::Damage}
	};
	for (const auto& Case : Cases)
	{
		FFixture F;
		F.StatusB();
		F.MoveA->Type = Case.Attack;
		TestTrue(TEXT("Transient target types configured"), F.SetTargetType(Case.Primary, Case.Secondary));
		TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());
		Session->Initialize(F.A, F.B, 42);
		const auto Result = Session->ResolveRound(0, 0);
		TestTrue(TEXT("Round resolves with status opponent"), Result.bSucceeded);
		const int32 ExpectedDamage = int32(24 * Case.Multiplier);
		TestEqual(TEXT("Type-adjusted damage is applied to HP"), Session->GetState().SideB.CurrentHP, 500 - ExpectedDamage);
		TestEqual(TEXT("Status placeholder does not change opponent HP"), Session->GetState().SideA.CurrentHP, 500);
		TestEqual(TEXT("Status and immunity still consume PP"), Session->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(), 49);
		TestEqual(TEXT("Attacker spends one PP even on immunity"), Session->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(), 49);
		const auto* Effect = Find(Result, Case.Event, S::A);
		if (!TestNotNull(TEXT("Expected effectiveness event exists"), Effect)) return false;
		TestEqual(TEXT("Effect event contains multiplier"), Effect->TypeMultiplier, Case.Multiplier);
		TestEqual(TEXT("Only effective direct damage produces a damage event"), Count(Result, E::Damage), ExpectedDamage > 0 ? 1 : 0);
		if (const auto* Damage = Find(Result, E::Damage))
		{
			TestEqual(TEXT("Damage amount matches HP loss"), Damage->Damage, ExpectedDamage);
			TestEqual(TEXT("Damage includes old HP"), Damage->HPBefore, 500);
			TestEqual(TEXT("Damage includes new HP"), Damage->HPAfter, 500 - ExpectedDamage);
		}
	}
	FFixture F;
	F.StatusB();
	F.MoveA->Accuracy = 0;
	TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());
	Session->Initialize(F.A, F.B);
	const auto Miss = Session->ResolveRound(0, 0);
	TestTrue(TEXT("Miss is a successful round resolution"), Miss.bSucceeded);
	TestEqual(TEXT("One miss event"), Count(Miss, E::Missed), 1);
	TestEqual(TEXT("Miss does not apply damage"), Count(Miss, E::Damage), 0);
	TestEqual(TEXT("Miss still consumes PP"), Session->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(), 49);
	TestEqual(TEXT("Miss leaves HP unchanged"), Session->GetState().SideB.CurrentHP, 500);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSessionKOTest, "PokeMonster.Battle.Session.KOAndFinish",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterSessionKOTest::RunTest(const FString& Parameters)
{
	// Either side can win before the opponent's pending action, regardless of submission order.
	for (const bool bAWins : {true, false})
	{
		FFixture F;
		F.MoveA->Priority = bAWins ? 1 : 0;
		F.MoveB->Priority = bAWins ? 0 : 1;
		(bAWins ? F.B : F.A).CurrentHP = 5;
		TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());
		Session->Initialize(F.A, F.B, 123);
		const auto Result = Session->ResolveRound(0, 0);
		const S Winner = bAWins ? S::A : S::B;
		const auto& WinnerCreature = bAWins ? Session->GetState().SideA : Session->GetState().SideB;
		const auto& LoserCreature = bAWins ? Session->GetState().SideB : Session->GetState().SideA;
		TestTrue(TEXT("KO round succeeds"), Result.bSucceeded);
		TestEqual(TEXT("Correct winner returned"), Result.Winner, Winner);
		TestEqual(TEXT("Session is finished"), Session->GetState().Phase, Phase::Finished);
		TestEqual(TEXT("HP clamp to zero"), LoserCreature.CurrentHP, 0);
		TestEqual(TEXT("KO opponent does not retaliate"), WinnerCreature.CurrentHP, 500);
		TestEqual(TEXT("Winner spends PP"), WinnerCreature.GetMoveSlots()[0].GetCurrentPP(), 49);
		TestEqual(TEXT("KO opponent spends no PP"), LoserCreature.GetMoveSlots()[0].GetCurrentPP(), 50);
		const E Expected[] = {E::MoveChosen,E::MoveChosen,E::MoveExecuted,E::Damage,E::KnockedOut,E::BattleEnded};
		TestEqual(TEXT("Complete ordered KO event sequence"), Result.Events.Num(), int32(UE_ARRAY_COUNT(Expected)));
		for (int32 Index = 0; Index < FMath::Min(Result.Events.Num(), int32(UE_ARRAY_COUNT(Expected))); ++Index)
		{
			TestEqual(TEXT("Event ordering"), Result.Events[Index].Type, Expected[Index]);
			TestEqual(TEXT("Events carry the accepted round number"), Result.Events[Index].RoundNumber, 1);
		}
		if (const auto* Damage = Find(Result, E::Damage)) TestEqual(TEXT("Reported damage excludes overkill"), Damage->Damage, 5);
		if (const auto* End = Find(Result, E::BattleEnded)) TestEqual(TEXT("End event identifies winner"), End->Source, Winner);
		const auto Rejected = Session->ResolveRound(0, 0);
		TestEqual(TEXT("Further rounds rejected"), Rejected.Error, BattleError::BattleFinished);
		TestEqual(TEXT("Winner preserved after rejected call"), Rejected.Winner, Winner);
		TestEqual(TEXT("No duplicate finish events"), Rejected.Events.Num(), 0);
		TestEqual(TEXT("Finished round number remains stable"), Session->GetState().RoundNumber, 1);
	}
	FFixture F;
	F.StatusB();
	F.B.CurrentHP = 50;
	TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());
	Session->Initialize(F.A, F.B);
	for (int32 Round = 1; Round <= 3; ++Round)
	{
		const auto Result = Session->ResolveRound(0, 0);
		TestTrue(TEXT("Repeated rounds resolve until KO"), Result.bSucceeded);
		TestEqual(TEXT("Round counter accumulates"), Result.RoundNumber, Round);
		TestEqual(TEXT("Only final round finishes"), Count(Result, E::BattleEnded), Round == 3 ? 1 : 0);
	}
	TestEqual(TEXT("Multi-round battle ends with A winning"), Session->GetState().Winner, S::A);
	TestEqual(TEXT("B attacked only before final KO"), Session->GetState().SideB.GetMoveSlots()[0].GetCurrentPP(), 48);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSessionValidationTest, "PokeMonster.Battle.Session.ValidationAndReplay",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterSessionValidationTest::RunTest(const FString& Parameters)
{
	FFixture F;
	TStrongObjectPtr<UPokeMonsterBattleSession> Session(NewObject<UPokeMonsterBattleSession>());
	TestEqual(TEXT("Must initialize first"), Session->ResolveRound(0, 0).Error, BattleError::NotInitialized);
	TestEqual(TEXT("Same instance cannot battle itself"), Session->Initialize(F.A, F.A).Error, BattleError::DuplicateCreature);
	auto Invalid = F.A;
	Invalid.Species.Reset();
	TestEqual(TEXT("Missing species is explicit"), Session->Initialize(Invalid, F.B).Error, BattleError::MissingSpecies);
	Invalid = F.A;
	Invalid.InstanceId.Invalidate();
	TestEqual(TEXT("Invalid identity is rejected"), Session->Initialize(Invalid, F.B).Error, BattleError::InvalidCreature);
	Invalid = F.B;
	Invalid.CurrentHP = 0;
	const auto Fainted = Session->Initialize(F.A, Invalid);
	TestEqual(TEXT("Already fainted participant is rejected"), Fainted.Error, BattleError::CreatureFainted);
	TestEqual(TEXT("Error identifies side"), Fainted.ErrorSide, S::B);
	Invalid = F.B;
	Invalid.CalculatedStats.Speed = 0;
	TestEqual(TEXT("Invalid speed is rejected"), Session->Initialize(F.A, Invalid).Error, BattleError::InvalidStats);
	TestEqual(TEXT("Failed starts leave session uninitialized"), Session->GetState().Phase, Phase::Uninitialized);
	TestTrue(TEXT("Corrected inputs can initialize"), Session->Initialize(F.A, F.B, 91).bSucceeded);
	TestEqual(TEXT("Cannot silently overwrite an active session"), Session->Initialize(F.A, F.B).Error, BattleError::AlreadyInitialized);
	const auto Initial = Session->GetState();
	TestEqual(TEXT("Negative slot rejected"), Session->ResolveRound(-1, 0).Error, BattleError::InvalidSlot);
	TestEqual(TEXT("Slot four rejected"), Session->ResolveRound(0, 4).Error, BattleError::InvalidSlot);
	const auto Missing = Session->ResolveRound(0, 3);
	TestEqual(TEXT("Empty/missing move is explicit"), Missing.Error, BattleError::MissingMove);
	TestEqual(TEXT("Invalid second choice identifies B"), Missing.ErrorSide, S::B);
	TestEqual(TEXT("Rejected round produces no execution/choice events"), Missing.Events.Num(), 0);
	F.MoveB->MaxPP = 51;
	TestEqual(TEXT("Changed PP design data is detected"), Session->ResolveRound(0, 0).Error, BattleError::InvalidPP);
	F.MoveB->MaxPP = 50;
	F.MoveB->Accuracy = 101;
	TestEqual(TEXT("Malformed move data is rejected"), Session->ResolveRound(0, 0).Error, BattleError::InvalidMove);
	F.MoveB->Accuracy = 100;
	TestTrue(TEXT("Rejected rounds leave the entire state unchanged"),
		FPokeMonsterBattleState::StaticStruct()->CompareScriptStruct(&Initial, &Session->GetState(), 0));
	F.B.ConsumeMovePP(0, 50);
	TStrongObjectPtr<UPokeMonsterBattleSession> Exhausted(NewObject<UPokeMonsterBattleSession>());
	Exhausted->Initialize(F.A, F.B);
	const auto NoPP = Exhausted->ResolveRound(0, 0);
	TestEqual(TEXT("Zero PP is explicit"), NoPP.Error, BattleError::NoPP);
	TestEqual(TEXT("Valid opponent is not charged PP for invalid round"), Exhausted->GetState().SideA.GetMoveSlots()[0].GetCurrentPP(), 50);
	TestEqual(TEXT("No PP does not advance the round"), Exhausted->GetState().RoundNumber, 0);

	FFixture Replay;
	Replay.StatusB();
	Replay.MoveA->Category = C::Status;
	Replay.MoveA->BasePower = 0;
	Replay.MoveA->Accuracy = Replay.MoveB->Accuracy = 55;
	TStrongObjectPtr<UPokeMonsterBattleSession> Left(NewObject<UPokeMonsterBattleSession>());
	TStrongObjectPtr<UPokeMonsterBattleSession> Right(NewObject<UPokeMonsterBattleSession>());
	Left->Initialize(Replay.A, Replay.B, 12345);
	Right->Initialize(Replay.A, Replay.B, 12345);
	Left->ResolveRound(0, -1); // Must not advance RNG relative to the untouched control.
	for (int32 Round = 0; Round < 8; ++Round)
	{
		const auto L = Left->ResolveRound(0, 0);
		const auto R = Right->ResolveRound(0, 0);
		TestTrue(TEXT("Seeded results, event ordering and RNG survive rejected input identically"),
			FPokeMonsterBattleResult::StaticStruct()->CompareScriptStruct(&L, &R, 0));
		TestEqual(TEXT("Status-only round produces no damage"), Count(L, E::Damage), 0);
	}
	// Only the session retains the transient data assets now; soft references alone would not suffice.
	Replay.SpeciesA.Reset(); Replay.SpeciesB.Reset(); Replay.MoveA.Reset(); Replay.MoveB.Reset();
	CollectGarbage(RF_NoFlags);
	TestTrue(TEXT("Session keeps species and moves alive across GC"), Left->ResolveRound(0, 0).bSucceeded);
	TestEqual(TEXT("No status effect or implicit timeout"), Left->GetState().Phase, Phase::AwaitingChoices);
	return true;
}

#endif
