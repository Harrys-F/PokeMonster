#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Development/PokeMonsterCreatureTestGround.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "Engine/World.h"
#include "Engine/Engine.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FV6ConsoleWorld,"PokeMonster.VisualV6.TeleportConsoleWorldSafety",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FV6ConsoleWorld::RunTest(const FString&)
{
 using G=UPokeMonsterCreatureTestGround;
 auto* W=UWorld::CreateWorld(EWorldType::PIE,false,FName(TEXT("Dev_TestMap_VisualV2")),CreatePackage(TEXT("/Temp/VisualV6/Dev_TestMap_VisualV2")));
 auto* Other=UWorld::CreateWorld(EWorldType::Game,false,FName(TEXT("OtherMap")));
 auto* Editor=UWorld::CreateWorld(EWorldType::Editor,false);
 GEngine->CreateNewWorldContext(EWorldType::PIE).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);Other->DestroyWorld(false);Editor->DestroyWorld(false);};
 TestEqual(TEXT("Game console uses its explicit eligible world"),G::ResolveConsoleWorld(W),W);
 TestEqual(TEXT("Editor console resolves the sole active VisualV2 PIE"),G::ResolveConsoleWorld(Editor),W);
 TestEqual(TEXT("Null editor context also resolves unambiguously"),G::ResolveConsoleWorld(nullptr),W);
 TestNull(TEXT("An explicit unrelated game must never be redirected"),G::ResolveConsoleWorld(Other));
 GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(Other);
 TestEqual(TEXT("Unrelated map does not introduce ambiguity"),G::ResolveConsoleWorld(Editor),W);
 GEngine->DestroyWorldContext(Other);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FV6ImportScope,"PokeMonster.VisualV6.UnriggedImportInspectionScope",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FV6ImportScope::RunTest(const FString&)
{
 using G=UPokeMonsterCreatureTestGround;
 TestTrue(TEXT("Only derived intake assets eligible"),G::IsInspectionAsset(TEXT("/Game/Characters/Creatures/ModelIntakeV6/Aquana/SM_Aquana_Import")));
 TestFalse(TEXT("Existing animated originals excluded"),G::IsInspectionAsset(TEXT("/Game/Characters/Creatures/Garados/SK_Garados")));
 TestFalse(TEXT("Similar prefix is not a directory match"),G::IsInspectionAsset(G::ImportRoot()+TEXT("Other/SM")));
 for(const TCHAR* Mode:{TEXT("idle"),TEXT("turn"),TEXT("reset")})TestTrue(TEXT("Honest static review operation"),G::SupportsInspectionMode(Mode));
 for(const TCHAR* Mode:{TEXT("walk"),TEXT("run"),TEXT("auto"),TEXT("directions"),TEXT("attack")})TestFalse(TEXT("Never fabricate animation on a source mesh"),G::SupportsInspectionMode(Mode));
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FV6SpeciesMovement,"PokeMonster.VisualV6.PikachuKarpadorSpeedAndStride",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FV6SpeciesMovement::RunTest(const FString&)
{
 auto* P=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Pikachu.DA_Pikachu"));
 auto* K=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Karpador.DA_Karpador"));
 if(!TestNotNull(TEXT("Existing Pikachu"),P)||!TestNotNull(TEXT("Existing Karpador"),K))return false;
 const auto* PV=P->GetVisuals().Presentation.LoadSynchronous();const auto* KV=K->GetVisuals().Presentation.LoadSynchronous();
 TestTrue(TEXT("Pikachu ordinary walk substantially faster than old 11.2125cm/s"),P->Overworld.WalkSpeedOverride*P->Overworld.Behavior.WalkMultiplier>25.f);
 TestTrue(TEXT("Pikachu distinct run above walk"),P->Overworld.RunSpeedOverride>P->Overworld.WalkSpeedOverride);
 TestEqual(TEXT("Authored Pikachu walk stride reference unchanged"),PV->WalkSpeed,13.f);
 TestEqual(TEXT("Authored Pikachu run stride reference unchanged"),PV->RunSpeed,28.f);
 TestTrue(TEXT("Fish ordinary swim at least 1.8x original 26.25cm/s"),K->Overworld.WalkSpeedOverride*K->Overworld.Behavior.WalkMultiplier>=47.25f);
 TestTrue(TEXT("Swimming rate fits the existing non-serpentine 1.75 limit"),K->Overworld.WalkSpeedOverride*K->Overworld.Behavior.WalkMultiplier/KV->SwimReferenceSpeed<=1.75f);
 TestEqual(TEXT("Original fish swim distance per cycle preserved"),KV->SwimReferenceSpeed,35.f);
 TestTrue(TEXT("Existing fish land/flop clip retained, no fabricated gait"),KV->SwimClip==KV->Clips.FindRef(EPokeMonsterCreatureClip::Walk));
 return true;
}
#endif
