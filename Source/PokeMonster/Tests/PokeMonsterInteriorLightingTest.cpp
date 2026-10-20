#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterInteriorLightingTest,
 "PokeMonster.Building.InteriorLightingRestoresExterior", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterInteriorLightingTest::RunTest(const FString& Parameters)
{
 UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
 if (!TestNotNull(TEXT("Lighting world"), World)) return false;
 GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
 ON_SCOPE_EXIT { GEngine->DestroyWorldContext(World); World->DestroyWorld(false); };
 auto* Player = World->SpawnActor<APokeMonsterPlayerCharacter>(FVector(-600,0,48), FRotator::ZeroRotator);
 auto* Controller = World->SpawnActor<APlayerController>(); World->AddController(Controller); Controller->Possess(Player);
 auto* Probe = NewObject<UStaticMeshComponent>(Player); Player->AddInstanceComponent(Probe); Probe->SetupAttachment(Player->GetRootComponent()); Probe->RegisterComponent();
 Probe->SetLightingChannels(true, false, true); Probe->SetCastShadow(true);
 auto* House = World->SpawnActor<APokeMonsterBuildingCutaway>(FVector(0,0,150), FRotator::ZeroRotator);
 TestFalse(TEXT("Existing maps do not opt in"), House->bUseShadowlessInteriorLighting);
 House->Tick(0.f);
 TestTrue(TEXT("Exterior channels unchanged"), Probe->LightingChannels.bChannel0 && !Probe->LightingChannels.bChannel1 && Probe->LightingChannels.bChannel2);
 TestTrue(TEXT("Exterior shadows retained"), Probe->CastShadow != 0);
 House->bUseShadowlessInteriorLighting = true; House->Tick(0.f);
 TestTrue(TEXT("Opt-in has no effect outside"), Probe->CastShadow != 0);
 Player->SetActorLocation(FVector(0,0,48)); House->Tick(.4f);
 TestTrue(TEXT("Interior uses room light channel only"), !Probe->LightingChannels.bChannel0 && Probe->LightingChannels.bChannel1 && !Probe->LightingChannels.bChannel2);
 TestFalse(TEXT("Interior pawn casts no shadow"), Probe->CastShadow != 0);
 Player->SetActorLocation(FVector(-600,0,48)); House->Tick(.4f);
 TestTrue(TEXT("Exit restores all three original channel bits"), Probe->LightingChannels.bChannel0 && !Probe->LightingChannels.bChannel1 && Probe->LightingChannels.bChannel2);
 TestTrue(TEXT("Exit restores original shadow flag"), Probe->CastShadow != 0);
 Probe->SetCastShadow(false); Player->SetActorLocation(FVector(0,0,48)); House->Tick(.4f);
 House->bUseShadowlessInteriorLighting = false; House->Tick(0.f);
 TestFalse(TEXT("An originally shadowless component stays shadowless"), Probe->CastShadow != 0);
 TestTrue(TEXT("Disabling the opt-in restores original channels"), Probe->LightingChannels.bChannel0 && Probe->LightingChannels.bChannel2);
 return true;
}
#endif
