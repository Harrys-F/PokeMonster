#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../UI/PokeMonsterOverworldWidget.h"
#include "../UI/PokeMonsterControllerInput.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/StrongObjectPtr.h"

namespace MoveManagementV2Tests
{
FPokeMonsterCreatureInstance Offered()
{
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Schiggy.DA_Schiggy"));
 auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(S,12);C.AssignSpeciesMoves();
 C.ConsumeMovePP(0,3);C.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(S->GetGrowthRate(),13)-1;C.AddExperience(1);
 return C;
}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FMoveManagementV2Repertoire,"PokeMonster.MoveManagementV2.LearningRepertoireAndPP",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FMoveManagementV2Repertoire::RunTest(const FString&)
{
 auto C=MoveManagementV2Tests::Offered();const auto Old=C.GetMoveSlots()[0];const auto New=C.PendingMoves[0];
 TestEqual(TEXT("Offer is not learned"),C.GetLearnedMoves().Num(),4);
 auto Declined=C;Declined.ResolveMoveLearning(INDEX_NONE);TestEqual(TEXT("Declined remains unknown"),Declined.GetLearnedMoves().Num(),4);
 auto Independent=C;Independent.InstanceId=FGuid::NewGuid();Independent.ResolveMoveLearning(INDEX_NONE);
 TestTrue(TEXT("Accepted new attack"),C.ResolveMoveLearning(0));TestEqual(TEXT("Old move retained"),C.GetLearnedMoves().Num(),5);
 TestEqual(TEXT("Other instance has separate history"),Independent.GetLearnedMoves().Num(),4);
 const auto NewSlot=C.GetMoveSlots()[0];TestTrue(TEXT("Spend new move PP"),C.ConsumeMovePP(0,4));
 TArray<TSoftObjectPtr<UPokeMonsterMoveData>> Draft={Old.GetMove()};
 TestTrue(TEXT("Reactivate old move"),C.SetActiveLearnedMoves(Draft));TestEqual(TEXT("Old AP retained"),C.GetMoveSlots()[0].GetCurrentPP(),Old.GetCurrentPP());
 TestTrue(TEXT("Reactivate new move"),C.SetActiveLearnedMoves({New}));TestEqual(TEXT("No AP refill on repeated swap"),C.GetMoveSlots()[0].GetCurrentPP(),NewSlot.GetCurrentPP()-4);
 TestFalse(TEXT("Duplicate active moves rejected"),C.SetActiveLearnedMoves({New,New}));TestFalse(TEXT("Empty set rejected"),C.SetActiveLearnedMoves({}));
 TestFalse(TEXT("Unknown move cannot be unlocked"),C.SetActiveLearnedMoves({LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestFireSpecial.DA_TestFireSpecial"))}));
 auto TooMany=Draft;for(int I=0;I<4;++I)TooMany.Add(New);TestFalse(TEXT("Fifth active move rejected"),C.SetActiveLearnedMoves(TooMany));
 auto BadKnown=C.GetLearnedMoves();const auto Duplicate=BadKnown[0];BadKnown.Add(Duplicate);TestFalse(TEXT("Duplicate repertoire rejected"),C.RestoreLearnedMoves(BadKnown));
 TestTrue(TEXT("Healing restores inactive as well as active PP"),C.RestoreFully());for(const auto& Known:C.GetLearnedMoves())TestEqual(TEXT("Legitimate healing fills remembered PP"),Known.GetCurrentPP(),Known.GetMaxPP());
 TestEqual(TEXT("Exactly four physical slots"),C.GetMoveSlots().Num(),4);TestEqual(TEXT("History survives healing"),C.GetLearnedMoves().Num(),5);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FMoveManagementV2Save,"PokeMonster.MoveManagementV2.SaveMigrationAndPending",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FMoveManagementV2Save::RunTest(const FString&)
{
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
 auto C=MoveManagementV2Tests::Offered();auto D=C;D.InstanceId=FGuid::NewGuid();D.ResolveMoveLearning(INDEX_NONE);C.ResolveMoveLearning(0);C.ConsumeMovePP(0,5);
 TestTrue(TEXT("Two individuals"),E->RestorePersistentState({C,D},{},{}));auto* S=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());if(!TestNotNull(TEXT("Version 6 capture"),S))return false;
 TestEqual(TEXT("New schema"),S->SaveVersion,6);TestEqual(TEXT("Accepted retains five"),S->PlayerTeam[0].LearnedMoves.Num(),5);TestEqual(TEXT("Declined retains four"),S->PlayerTeam[1].LearnedMoves.Num(),4);
 TArray<uint8> Bytes;TestTrue(TEXT("Engine save serialization"),UGameplayStatics::SaveGameToMemory(S,Bytes));auto* Loaded=Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));
 TestTrue(TEXT("Round trip"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Loaded,E,I));TestEqual(TEXT("Inactive history saved"),E->GetPlayerParty()[0].GetLearnedMoves().Num(),5);TestEqual(TEXT("Spent AP saved"),E->GetPlayerParty()[0].GetMoveSlots()[0].GetCurrentPP(),20);
 const auto Id=C.InstanceId;TestTrue(TEXT("Team sort"),E->ReorderParty(Id,1));TestEqual(TEXT("History follows instance not slot"),E->GetPlayerParty()[1].GetLearnedMoves().Num(),5);
 for(int V=1;V<=5;++V){S->SaveVersion=V;TestTrue(TEXT("All old schemas migrate"),UPokeMonsterSaveSubsystem::RestoreSnapshot(S,E,I));TestEqual(TEXT("No old unrecorded attacks invented"),E->GetPlayerParty()[0].GetLearnedMoves().Num(),4);TestEqual(TEXT("Old actual PP preserved"),E->GetPlayerParty()[0].GetMoveSlots()[0].GetCurrentPP(),20);}
 auto Pending=MoveManagementV2Tests::Offered();E->RestorePersistentState({Pending},{},{});auto* P=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get());TestNotNull(TEXT("Pending capture"),P);
 TestTrue(TEXT("Pending reload"),UPokeMonsterSaveSubsystem::RestoreSnapshot(P,E,I));TestEqual(TEXT("Offer persists separately"),E->GetPlayerParty()[0].PendingMoves.Num(),1);TestEqual(TEXT("Not silently learned"),E->GetPlayerParty()[0].GetLearnedMoves().Num(),4);
 const auto Duplicate=P->PlayerTeam[0].LearnedMoves[0];P->PlayerTeam[0].LearnedMoves.Add(Duplicate);
 AddExpectedError(TEXT("Invalid creature in save"),EAutomationExpectedErrorFlags::Contains,1);TestFalse(TEXT("Duplicate save rejected atomically"),UPokeMonsterSaveSubsystem::RestoreSnapshot(P,E,I));TestEqual(TEXT("Party retained after rejected save"),E->GetPlayerParty()[0].InstanceId,Pending.InstanceId);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FMoveManagementV2Widget,"PokeMonster.MoveManagementV2.ReadOnlyAndControllerDraft",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FMoveManagementV2Widget::RunTest(const FString&)
{
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get());auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());auto C=MoveManagementV2Tests::Offered();C.ResolveMoveLearning(0);E->RestorePersistentState({C},{},{});
 TStrongObjectPtr<UPokeMonsterOverworldWidget> W(NewObject<UPokeMonsterOverworldWidget>());W->TakeWidget();W->UpdateView(FPokeMonsterOverworldViewBuilder::Build(E,I));W->SetMenuOpen(true,EPokeMonsterOverworldMenuSection::Team);
 auto Press=[&](FKey K,bool Repeat=false){return W->NativeOnPreviewKeyDown(FGeometry(),FKeyEvent(K,FModifierKeysState(),0,Repeat,0,0)).IsEventHandled();};
 TestTrue(TEXT("Read-only moves category via L"),Press(EKeys::Gamepad_LeftShoulder));TestEqual(TEXT("Moves category"),W->GetSection(),EPokeMonsterOverworldMenuSection::Moves);
 Press(PokeMonsterControllerInput::Confirm());TestFalse(TEXT("Pokemon selected"),W->bChoosingMovePokemon);Press(PokeMonsterControllerInput::Confirm());TestTrue(TEXT("Read-only reminder"),W->MoveMessage.Contains(TEXT("Meister der Erinnerungen")));TestEqual(TEXT("No normal menu mutation"),E->GetPlayerParty()[0].GetMoveSlots()[0].GetMove(),C.GetMoveSlots()[0].GetMove());
 W->SetMoveMasterMode(true);Press(PokeMonsterControllerInput::Confirm());const auto Draft=W->DraftMoves;Press(PokeMonsterControllerInput::Confirm(),true);TestEqual(TEXT("Held B no double action"),W->DraftMoves.Num(),Draft.Num());
 Press(PokeMonsterControllerInput::Confirm());TestEqual(TEXT("Inactive move at full set opens replacement"),W->ReplaceCursor,0);Press(EKeys::Gamepad_DPad_Down);Press(PokeMonsterControllerInput::Confirm());TestEqual(TEXT("Four active draft moves"),W->DraftMoves.Num(),4);
 TestEqual(TEXT("Draft never modifies party"),E->GetPlayerParty()[0].GetMoveSlots()[1].GetMove(),C.GetMoveSlots()[1].GetMove());
 W->MoveCursor=5;Press(PokeMonsterControllerInput::Confirm());TestTrue(TEXT("Explicit review before commit"),W->bMoveReview);Press(PokeMonsterControllerInput::Confirm());TestTrue(TEXT("No controller/NPC authorization fails closed"),W->IsMenuOpen());
 Press(PokeMonsterControllerInput::Cancel());TestFalse(TEXT("A returns from review"),W->bMoveReview);Press(PokeMonsterControllerInput::Cancel());TestTrue(TEXT("A discards draft"),W->bChoosingMovePokemon);TestTrue(TEXT("Draft gone"),W->DraftMoves.IsEmpty());
 Press(EKeys::Gamepad_RightShoulder);TestEqual(TEXT("Master cannot escape to sorting/inventory"),W->GetSection(),EPokeMonsterOverworldMenuSection::Moves);W->SetBattleVisible(true);TestFalse(TEXT("Battle input does not mutate draft"),W->SelectTeamSlot(0));PokeMonsterControllerInput::ObserveKey(EKeys::E);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FMoveManagementV2NPC,"PokeMonster.MoveManagementV2.NPCLocationAuthorization",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FMoveManagementV2NPC::RunTest(const FString&)
{
 UWorld* World=nullptr;for(const auto& C:GEngine->GetWorldContexts())if(C.WorldType==EWorldType::Editor)World=C.World();if(!TestNotNull(TEXT("Editor world"),World))return false;
 FActorSpawnParameters Params;Params.ObjectFlags|=RF_Transient;Params.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* NPC=World->SpawnActor<APokeMonsterNPC>(Params);auto* Player=World->SpawnActor<APokeMonsterPlayerCharacter>(Params);if(!NPC||!Player)return false;
 NPC->SetActorLocation(Player->GetActorLocation()+FVector(80,0,0));TestFalse(TEXT("Ordinary NPC has no move authority"),NPC->CanProvideMoveService(Player));NPC->Service=EPokeMonsterNPCService::RememberMoves;
 TestTrue(TEXT("Configured nearby master authorized"),NPC->CanProvideMoveService(Player));NPC->SetActorLocation(Player->GetActorLocation()+FVector(1000,0,0));TestFalse(TEXT("Remote master cannot edit"),NPC->CanProvideMoveService(Player));TestFalse(TEXT("Null user rejected"),NPC->CanProvideMoveService(nullptr));
 World->DestroyActor(NPC);World->DestroyActor(Player);return true;
}
#endif
