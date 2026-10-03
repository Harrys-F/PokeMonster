#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "Components/BoxComponent.h"
#include "Camera/CameraTypes.h"
#include "Engine/World.h"
#include "Engine/Level.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterInnCameraTest,
    "PokeMonster.Building.Inn.CameraAndFootprint", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterInnCameraTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
    if (!TestNotNull(TEXT("Footprint test world"), World)) return false;
    ON_SCOPE_EXIT { World->DestroyWorld(false); };
    auto* Inn = World->SpawnActor<APokeMonsterBuildingCutaway>(FVector(100,-1500,150), FRotator::ZeroRotator);
    Inn->InteriorArea->SetBoxExtent(FVector(410,410,200));
    Inn->DoorThreshold->SetRelativeLocation(FVector(-400,-100,-42.5));
    Inn->DoorThreshold->SetBoxExtent(FVector(20,80,107.5));
    TestTrue(TEXT("Empty regions retain the original bounding box"), Inn->IsViewerInside(FVector(450,-1850,50)));
    FPokeMonsterBuildingInteriorRegion Main, Wing;
    Main.Center = FVector(-100,0,0); Main.Extent = FVector(310,410,200);
    Wing.Center = FVector(300,100,0); Wing.Extent = FVector(110,310,200);
    Inn->InteriorRegions = { Main, Wing };
    TestTrue(TEXT("Main hall is interior"), Inn->IsViewerInside(FVector(0,-1500,50)));
    TestTrue(TEXT("Rear wing is interior"), Inn->IsViewerInside(FVector(450,-1400,50)));
    TestTrue(TEXT("Join has no interior detection seam"), Inn->IsViewerInside(FVector(300,-1400,50)));
    TestFalse(TEXT("L-notch stays outdoors"), Inn->IsViewerInside(FVector(450,-1850,50)));
    TestFalse(TEXT("Approach does not trigger interior before door"), Inn->IsViewerInside(FVector(-306,-1600,50)));
    TestTrue(TEXT("Doorway still uses real public aperture"), Inn->IsViewerInDoorway(FVector(-300,-1600,50)));
    TestFalse(TEXT("Doorway excludes adjacent wall"), Inn->IsViewerInDoorway(FVector(-300,-1690,50)));
    Inn->SetActorRotation(FRotator(0,90,0));
    TestTrue(TEXT("Region union follows building transform"), Inn->IsViewerInside(Inn->GetActorTransform().TransformPosition(FVector(350,100,-100))));
    TestFalse(TEXT("Rotated L-notch remains outdoors"), Inn->IsViewerInside(Inn->GetActorTransform().TransformPosition(FVector(350,-350,-100))));
    auto* Map = LoadObject<UWorld>(nullptr,TEXT("/Game/Maps/Dev_BuildingKitTestMap.Dev_BuildingKitTestMap"));
    if (!TestNotNull(TEXT("Saved Inn map loads"),Map)) return false;
    APokeMonsterBuildingCutaway* Saved = nullptr;
    for (AActor* Actor : Map->PersistentLevel->Actors)
        if (Actor && Actor->GetActorLabel()==TEXT("WL_Inn_Cutaway")) Saved = Cast<APokeMonsterBuildingCutaway>(Actor);
    if (!TestNotNull(TEXT("Exactly configured Inn provider"),Saved)) return false;
    TestTrue(TEXT("Inn reuses opt-in interior camera"),Saved->bUseInteriorCamera);
    TestEqual(TEXT("Inn keeps the visually verified 2200 cm camera"),Saved->InteriorCameraDistance,2200.f);
    TestEqual(TEXT("Inn camera pitch"),Saved->InteriorCameraPitch,-50.f);
    TestEqual(TEXT("Inn has two joined interior regions"),Saved->InteriorRegions.Num(),2);
    TestEqual(TEXT("Reversible fade stays 0.4s"),Saved->FadeDuration,.4f);
    FMinimalViewInfo View;
    Saved->GetInteriorCameraView(View);
    TestTrue(TEXT("Inn camera is frontal in doorway coordinates"),View.Rotation.Equals(FRotator(-50,0,0)));
    int32 Roof = 0, Front = 0, Sides = 0, Junction = 0;
    for (AActor* Actor : Map->PersistentLevel->Actors)
    {
        if (!Actor || !Actor->ActorHasTag(TEXT("Westland_Inn"))) continue;
        const bool Hidden = Saved->OccludingActors.Contains(Actor);
        if (Actor->ActorHasTag(TEXT("Westland_Role_MainRoof")) || Actor->ActorHasTag(TEXT("Westland_Role_WingRoof")))
        { ++Roof; TestTrue(TEXT("Both roofs have explicit occluders"),Hidden); }
        if (Actor->ActorHasTag(TEXT("Westland_Role_FrontWall")))
        { ++Front; TestTrue(TEXT("Camera-facing public facade is an occluder"),Hidden); }
        if (Actor->ActorHasTag(TEXT("Westland_Role_JunctionUpperGable")))
        { ++Junction; TestTrue(TEXT("Upper joining gable cannot hide rear-wing player"),Hidden); }
        if (Actor->ActorHasTag(TEXT("Westland_Role_LeftWall")) || Actor->ActorHasTag(TEXT("Westland_Role_RightWall"))
            || Actor->ActorHasTag(TEXT("Westland_Role_WingNotchWall")) || Actor->ActorHasTag(TEXT("Westland_Role_WingRearWall")))
        { ++Sides; TestFalse(TEXT("Lower sides/rear enclose the room without blanket hiding"),Hidden); }
    }
    TestTrue(TEXT("Roof/front/wing and retained sides are all present"),Roof>0 && Front==4 && Junction==2 && Sides==11);
    return true;
}
#endif
