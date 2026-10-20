#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Encounter/PokeMonsterEncounterProfile.h"
#include "../Encounter/PokeMonsterTrainerProfile.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "UObject/StrongObjectPtr.h"
#include "../Encounter/PokeMonsterClassicBattleScene.h"
#include "Components/PointLightComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Components/StaticMeshComponent.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterClassicBattleContractTest,"PokeMonster.Encounter.ClassicBattle.ProfileSelection",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterClassicBattleContractTest::RunTest(const FString& Parameters)
{
 using Mode=EPokeMonsterBattlePresentationMode;
 TestEqual(TEXT("Normal start defaults to ClassicBattle"),FPokeMonsterEncounterStartData().PresentationMode,Mode::ClassicBattle);
 const auto* Scene=GetDefault<APokeMonsterClassicBattleScene>();
 TestTrue(TEXT("Presentation fill is isolated from world and interior channels"),!Scene->PresentationFill->LightingChannels.bChannel0&&!Scene->PresentationFill->LightingChannels.bChannel1&&Scene->PresentationFill->LightingChannels.bChannel2);
 TestFalse(TEXT("Stage fill casts no shadow"),Scene->PresentationFill->CastShadows);
 TestEqual(TEXT("Stage floor cannot alter gameplay collision"),Scene->Floor->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
 TestEqual(TEXT("Capture includes only explicitly listed stage actors"),Scene->Capture->PrimitiveRenderMode,ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList);
 TStrongObjectPtr<UPokeMonsterEncounterProfile> Wild(NewObject<UPokeMonsterEncounterProfile>());
 TStrongObjectPtr<UPokeMonsterTrainerProfile> Trainer(NewObject<UPokeMonsterTrainerProfile>());
 TestEqual(TEXT("Wild defaults to classic"),Wild->PresentationMode,Mode::ClassicBattle);
 TestEqual(TEXT("Trainer defaults to classic"),Trainer->PresentationMode,Mode::ClassicBattle);
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 auto* Move=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
 if(!TestNotNull(TEXT("Existing creature"),Species)||!TestNotNull(TEXT("Existing move"),Move))return false;
 FPokeMonsterWildEncounterEntry E;E.Species=Species;E.MinLevel=5;E.MaxLevel=5;E.Moves.Add(Move);Wild->Entries.Add(E);
 Trainer->InternalId=TEXT("ModeContract");Trainer->DisplayName=FText::FromString(TEXT("Mode contract"));Trainer->TrainerClass=FText::FromString(TEXT("Technical fixture"));FPokeMonsterTrainerTeamEntry T;T.Species=Species;T.Level=5;T.StartingMoves.Add(Move);Trainer->Team.Add(T);
 for(Mode M:{Mode::ClassicBattle,Mode::WorldBattle}){
  Wild->PresentationMode=M;Trainer->PresentationMode=M;FPokeMonsterEncounterStartData W,B;
  if(!TestTrue(TEXT("Wild preparation succeeds"),UPokeMonsterEncounterSubsystem::PrepareWildEncounter(Wild.Get(),FPokeMonsterEncounterContext(),EPokeMonsterEncounterSource::Zone,nullptr,5,TEXT("ModeContract"),W)))return false;
  if(!TestTrue(TEXT("Trainer preparation succeeds"),UPokeMonsterEncounterSubsystem::PrepareTrainerEncounter(Trainer.Get(),nullptr,5,B)))return false;
  TestEqual(TEXT("Wild forwards chosen mode"),W.PresentationMode,M);TestEqual(TEXT("Trainer forwards chosen mode"),B.PresentationMode,M);
  TestEqual(TEXT("Mode never changes species identity"),W.OpponentTeam[0].Species,B.OpponentTeam[0].Species);
  TestEqual(TEXT("Mode never changes creature size"),Species->GetVisuals().Presentation.LoadSynchronous()->ReferenceSizeCm,60.f);
 }
 return true;
}
#endif
