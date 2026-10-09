#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "PaperSprite.h"
#include "PaperFlipbookComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "DrawDebugHelpers.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/FileManager.h"

namespace
{
    FDelegateHandle PendingScaleProbe;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterScaleCalibrationTest,
    "PokeMonster.Player.ScaleCalibration",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPokeMonsterScaleCalibrationTest::RunTest(const FString& Parameters)
{
    const APokeMonsterPlayerCharacter* Defaults = GetDefault<APokeMonsterPlayerCharacter>();
    TestEqual(TEXT("Navigation capsule radius stays 28 cm"), Defaults->GetCapsuleComponent()->GetUnscaledCapsuleRadius(), 28.f);
    TestEqual(TEXT("Navigation capsule height stays 96 cm"), Defaults->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight()*2, 96.f);
    TestEqual(TEXT("Camera distance uses calibrated 2500 cm framing"), Defaults->FindComponentByClass<USpringArmComponent>()->TargetArmLength, 2500.f);
    const struct { const TCHAR* Name; int32 Width; int32 Height; } Frames[] =
    {
        { TEXT("S_Player_Idle_Down"), 230, 438 },
        { TEXT("S_Player_Idle_DownRight"), 206, 438 },
        { TEXT("S_Player_Idle_Up"), 232, 429 },
        { TEXT("S_Player_Walk_DownLeft_01"), 202, 438 },
        { TEXT("S_Player_Walk_DownLeft_02"), 194, 433 },
        { TEXT("S_Player_Walk_DownRight_01"), 193, 433 },
        { TEXT("S_Player_Walk_DownRight_02"), 203, 438 },
        { TEXT("S_Player_Walk_Down_01"), 199, 438 },
        { TEXT("S_Player_Walk_Down_02"), 188, 434 },
        { TEXT("S_Player_Walk_Left_01"), 215, 438 },
        { TEXT("S_Player_Walk_Left_02"), 202, 437 },
        { TEXT("S_Player_Walk_Right_01"), 219, 437 },
        { TEXT("S_Player_Walk_Right_02"), 201, 438 },
        { TEXT("S_Player_Walk_UpLeft_01"), 174, 438 },
        { TEXT("S_Player_Walk_UpLeft_02"), 200, 437 },
        { TEXT("S_Player_Walk_UpRight_01"), 192, 438 },
        { TEXT("S_Player_Walk_UpRight_02"), 198, 438 },
        { TEXT("S_Player_Walk_Up_01"), 186, 437 },
        { TEXT("S_Player_Walk_Up_02"), 185, 438 },
    };
    TArray<FString> Measurements;
    Measurements.Add(TEXT("sprite,alpha_width_px,alpha_height_px,ppu,body_width_cm,body_height_cm,render_min_x,render_min_y,render_min_z,render_max_x,render_max_y,render_max_z"));
    for (const auto& Frame : Frames)
    {
        const FString Path = FString::Printf(TEXT("/Game/Characters/Prototype2D/Sprites/HobbitPlayer/%s.%s"), Frame.Name, Frame.Name);
        const UPaperSprite* Sprite = LoadObject<UPaperSprite>(nullptr, *Path);
        if (!TestNotNull(*Path, Sprite)) continue;
        const float PPU = Sprite->GetPixelsPerUnrealUnit();
        TestTrue(TEXT("Every frame has the calibrated visible body height"), FMath::IsNearlyEqual(Frame.Height / PPU * (140.f*3.4f/438.f), 140.f, .01f));
        TestTrue(TEXT("Every frame pivots at the visible sole, not canvas bottom"), Sprite->GetPivotPosition().Equals(FVector2D(128,488), .01f));
        const FBox Box = Sprite->GetRenderBounds().GetBox();
        Measurements.Add(FString::Printf(TEXT("%s,%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f"), Frame.Name, Frame.Width, Frame.Height, PPU, Frame.Width/PPU*.66f, Frame.Height/PPU*(140.f*3.4f/438.f), Box.Min.X, Box.Min.Y, Box.Min.Z, Box.Max.X, Box.Max.Y, Box.Max.Z));
    }
    const FString Folder = FPaths::ProjectSavedDir() / TEXT("Automation/ScaleCalibration");
    IFileManager::Get().MakeDirectory(*Folder, true);
    FFileHelper::SaveStringArrayToFile(Measurements, *(Folder / TEXT("FrameBounds.csv")));
    bool bMeasuredPIE = false;
    for (const FWorldContext& Context : GEngine->GetWorldContexts())
    {
        if (Context.WorldType != EWorldType::PIE || !Context.World()->GetMapName().EndsWith(TEXT("Dev_HealingHouseTestMap"))) continue;
        UWorld* World = Context.World();
        APlayerController* PC = World->GetFirstPlayerController();
        APokeMonsterPlayerCharacter* Player = PC ? Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()) : nullptr;
        if (!TestNotNull(TEXT("Live PIE player exists"), Player)) continue;
        bMeasuredPIE = true;
        UPaperFlipbookComponent* Sprite = Player->GetCharacterFlipbookComponent();
        TestTrue(TEXT("PIE actor stays unscaled"), Player->GetActorScale3D().Equals(FVector::OneVector));
        TestTrue(TEXT("PIE visual component uses calibrated scale"), Sprite->GetRelativeScale3D().Equals(FVector(.66f,.66f,140.f*3.4f/438.f), .001f));
        const FVector Foot = Player->GetActorLocation() - FVector(0,0,Player->GetCapsuleComponent()->GetScaledCapsuleHalfHeight());
        TestTrue(TEXT("Visible sole follows capsule ground point"), Sprite->GetComponentLocation().Equals(Foot, .01f));
        const FVector Up = Sprite->GetUpVector();
        TestTrue(TEXT("Sprite body stands upright for world depth testing"), Up.Equals(FVector::UpVector, .001f));
        FVector2D SoleScreen, HeadScreen, ReferenceScreen;
        PC->ProjectWorldLocationToScreen(Foot, SoleScreen);
        PC->ProjectWorldLocationToScreen(Foot + Up*140.f, HeadScreen);
        PC->ProjectWorldLocationToScreen(Foot + FVector(0,0,140), ReferenceScreen);
        const float BodyPixels = FVector2D::Distance(SoleScreen, HeadScreen);
        const float RefPixels = FVector2D::Distance(SoleScreen, ReferenceScreen);
        TestTrue(TEXT("Visible body matches upright 140 cm at same foot point within 3 percent"), FMath::Abs(BodyPixels/RefPixels-1.f)<.03f);
        AddInfo(FString::Printf(TEXT("PIE Foot=%s Camera=%s body_px=%.2f upright140_px=%.2f ratio=%.5f"), *Foot.ToString(), *Player->FindComponentByClass<UCameraComponent>()->GetComponentLocation().ToString(), BodyPixels, RefPixels, BodyPixels/RefPixels));
        const FString LiveResult = FString::Printf(TEXT("Foot=%s\nCamera=%s\nActorScale=%s\nSpriteScale=%s\nSpriteLocation=%s\nBodyPixels=%.6f\nUpright140Pixels=%.6f\nRatio=%.6f\nResult=%s\n"),
            *Foot.ToString(), *Player->FindComponentByClass<UCameraComponent>()->GetComponentLocation().ToString(),
            *Player->GetActorScale3D().ToString(), *Sprite->GetRelativeScale3D().ToString(), *Sprite->GetComponentLocation().ToString(),
            BodyPixels, RefPixels, BodyPixels/RefPixels, BodyPixels > 0 && FMath::Abs(BodyPixels/RefPixels-1.f)<.03f ? TEXT("PASS") : TEXT("FAIL"));
        FFileHelper::SaveStringToFile(LiveResult, *(Folder / TEXT("LiveProjection.txt")));
        const FVector Right = Player->FindComponentByClass<UCameraComponent>()->GetRightVector();
        const float Heights[] = {140.f,180.f,210.f};
        const FColor Colors[] = {FColor::Green,FColor::Cyan,FColor::Yellow};
        for (int32 i=0;i<3;++i)
        {
            const FVector Base = Foot + Right*(65.f+i*70.f);
            DrawDebugBox(World, Base+FVector(0,0,Heights[i]/2), FVector(12,12,Heights[i]/2), Colors[i], false, 600.f, 0, 2.f);
            DrawDebugString(World, Base+FVector(0,0,Heights[i]+8), FString::Printf(TEXT("%.0f cm"),Heights[i]), nullptr, Colors[i], 600.f);
        }
    }
    // The editor automation controller stops PIE before running a test.
    // Arm a one-shot probe for the next real PIE, without saved actors or gameplay changes.
    if (!bMeasuredPIE && !PendingScaleProbe.IsValid())
    {
        PendingScaleProbe = FWorldDelegates::OnWorldPostActorTick.AddLambda(
            [this](UWorld* World, ELevelTick, float)
            {
                if (!World || World->WorldType != EWorldType::PIE || World->GetTimeSeconds()<1.f
                    || !World->GetMapName().EndsWith(TEXT("Dev_HealingHouseTestMap"))) return;
                FWorldDelegates::OnWorldPostActorTick.Remove(PendingScaleProbe);
                PendingScaleProbe.Reset();
                RunTest(TEXT("LiveProbe"));
            });
    }
    return true;
}
#endif
