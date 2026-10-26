#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../UI/PokeMonsterOverworldWidget.h"
#include "../UI/PokeMonsterControllerInput.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/GameInstance.h"
#include "UObject/StrongObjectPtr.h"
#include <limits>

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FSaveV2PositionContractTest, "PokeMonster.SaveV2.PositionContractAndSerialization", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FSaveV2PositionContractTest::RunTest(const FString&)
{
 auto* Save = NewObject<UPokeMonsterSaveGame>();
 auto& Position = Save->PlayerLocation;
 TestFalse(TEXT("No invented position for old snapshots"), Position.IsValid());
 Position.bHasPosition = true; Position.MapPackage = TEXT("/Game/Maps/Dev_TestMap_VisualV2");
 Position.Location = FVector(-1721,1942,71.5); Position.Rotation = FRotator(0,137,0);
 TestTrue(TEXT("Ordinary world location valid"), Position.IsValid());
 Save->ActiveCheckpoint.CheckpointId = TEXT("ExplicitCheckpoint");
 Save->ActiveCheckpoint.MapPackage = TEXT("/Game/Maps/Dev_TestMap");
 Save->ActiveCheckpoint.Location = FVector(100,200,90);
 TArray<uint8> Bytes; TestTrue(TEXT("Existing native format encodes V9"), UGameplayStatics::SaveGameToMemory(Save,Bytes));
 auto* Loaded = Cast<UPokeMonsterSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));
 if (!TestNotNull(TEXT("Native decode"),Loaded)) return false;
 TestEqual(TEXT("Saved position exact"),Loaded->PlayerLocation.Location,Position.Location);
 TestEqual(TEXT("Saved facing exact"),Loaded->PlayerLocation.Rotation,Position.Rotation);
 TestEqual(TEXT("Independent visible facing retained"),Loaded->PlayerLocation.FacingDirection,Position.FacingDirection);
 TestEqual(TEXT("Checkpoint map independent"),Loaded->ActiveCheckpoint.MapPackage,FName(TEXT("/Game/Maps/Dev_TestMap")));
 TestTrue(TEXT("Resume is not checkpoint"),Loaded->PlayerLocation.Location != Loaded->ActiveCheckpoint.Location);
 Position.InteriorActor=TEXT("ExistingHealingHouse"); Position.bRelocatedInterior=true;
 TestTrue(TEXT("Existing relocated-room context supported"),Position.IsValid());
 Position.InteriorActor=NAME_None; TestFalse(TEXT("No anonymous relocated room"),Position.IsValid());
 Position.bRelocatedInterior=false; Position.MapPackage=TEXT("../Invalid"); TestFalse(TEXT("No malformed map"),Position.IsValid());
 Position.MapPackage=TEXT("/Engine/Maps/Entry"); TestFalse(TEXT("Only project map references"),Position.IsValid());
 Position.MapPackage=TEXT("/Game/Maps/Dev_TestMap_VisualV2"); Position.Location.X=std::numeric_limits<double>::quiet_NaN();
 TestFalse(TEXT("NaN rejected"),Position.IsValid()); Position.Location=FVector(std::numeric_limits<double>::infinity(),0,0);
 TestFalse(TEXT("Infinity rejected"),Position.IsValid());
 TestNotEqual(TEXT("Recovery has a distinct slot"),UPokeMonsterSaveSubsystem::RecoverySlotName,UPokeMonsterSaveSubsystem::DevSlotName);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FSaveV2LegacyAndValidationTest,"PokeMonster.SaveV2.LegacyDataAndValidateOnly",EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FSaveV2LegacyAndValidationTest::RunTest(const FString&)
{
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());
 auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI.Get()); auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI.Get());
 auto* C=NewObject<UPokeMonsterCheckpointSubsystem>(GI.Get());
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf"));
 if(!TestNotNull(TEXT("Existing species"),Species))return false;
 auto Creature=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,15);
 TestTrue(TEXT("Install existing instance"),E->RestorePersistentState({Creature},{},{TEXT("Before")}));
 auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI.Get(),C);
 if(!TestNotNull(TEXT("Capture existing data"),Save))return false;
 Save->SaveVersion=8; Save->PlayerLocation={};
 TestTrue(TEXT("Schema8 without position loads data"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I,C));
 TestEqual(TEXT("Old identity retained"),E->GetPlayerParty()[0].InstanceId,Creature.InstanceId);
 TestEqual(TEXT("Old repertoire retained"),E->GetPlayerParty()[0].GetLearnedMoves().Num(),Creature.GetLearnedMoves().Num());
 Save->CompletedEncounterIds={TEXT("After")};
 TestTrue(TEXT("Validate-only reuses full validator"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I,C,nullptr,true));
 TestTrue(TEXT("Validation never commits flags"),E->IsEncounterCompleted(TEXT("Before"))&&!E->IsEncounterCompleted(TEXT("After")));
 TestTrue(TEXT("Validated data commit"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I,C));
 TestTrue(TEXT("Commit updates flags"),E->IsEncounterCompleted(TEXT("After")));
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FSaveV2MenuGuardTest,"PokeMonster.SaveV2.MenuConfirmationAndControllerGuards",EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FSaveV2MenuGuardTest::RunTest(const FString&)
{
 TStrongObjectPtr<UPokeMonsterOverworldWidget> UI(NewObject<UPokeMonsterOverworldWidget>());
 UI->TakeWidget(); UI->SetMenuOpen(true,EPokeMonsterOverworldMenuSection::Main);
 TestEqual(TEXT("Existing main menu with Load added"),UI->MainButtons.Num(),6);
 UI->FocusedMainSlot=2; UI->ConfirmMenu();
 TestEqual(TEXT("First B only requests save"),UI->PendingStorageAction,1);
 UI->ConfirmMenu(); TestEqual(TEXT("Overlapping same-frame B cannot save"),UI->PendingStorageAction,1);
 UI->NativeOnPreviewKeyDown(FGeometry(),FKeyEvent(PokeMonsterControllerInput::Cancel(),FModifierKeysState(),0,false,0,0));
 TestEqual(TEXT("A cancels save request"),UI->PendingStorageAction,0);
 TestTrue(TEXT("Cancel returns to menu"),UI->IsMenuOpen());
 UI->LastStorageInputFrame=MAX_uint64; UI->SaveGame();
 UI->NativeOnPreviewKeyDown(FGeometry(),FKeyEvent(PokeMonsterControllerInput::Confirm(),FModifierKeysState(),0,true,0,0));
 TestEqual(TEXT("Repeated held B cannot confirm"),UI->PendingStorageAction,1);
 UI->CancelStorage(); UI->FocusedMainSlot=5; UI->NavigateMenu(1);
 TestEqual(TEXT("Navigation wraps the actual 6 entries"),UI->FocusedMainSlot,0);
 return true;
}
#endif
