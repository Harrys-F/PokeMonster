// Explicit review only. Captures an unmodified actual Slate game viewport.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Engine/GameViewportClient.h"
#include "Engine/TextureRenderTarget2D.h"
#include "HAL/IConsoleManager.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "ImageUtils.h"
#include "Components/Button.h"
#include "Input/Events.h"
#include "Slate/SceneViewport.h"
#include "Widgets/SViewport.h"
#include "Framework/Application/SlateApplication.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "GameFramework/PlayerController.h"
#if !UE_BUILD_SHIPPING
namespace PMCreatureReview
{
static FAutoConsoleCommand Start(TEXT("pm.CreatureReview.Start"),TEXT("Explicit runtime-only Glumanda versus Glumanda composition test: classic or world. No asset/save mutation."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()<1||Args.Num()>2||(Args[0]!=TEXT("classic")&&Args[0]!=TEXT("world")))return;
 for(const auto& C:GEngine->GetWorldContexts()){
  auto* W=C.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;auto* PC=W->GetFirstPlayerController();auto* P=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;if(!P)continue;
  auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
  auto* M=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));if(!S||!M)return;
  FPokeMonsterEncounterStartData D;D.EncounterId=TEXT("ExplicitGlumandaReview");D.PresentationMode=Args[0]==TEXT("classic")?EPokeMonsterBattlePresentationMode::ClassicBattle:EPokeMonsterBattlePresentationMode::WorldBattle;
  if(Args.Num()==2){const TMap<FString,EPokeMonsterBattleEnvironment> Themes={{TEXT("meadow"),EPokeMonsterBattleEnvironment::Meadow},{TEXT("forest"),EPokeMonsterBattleEnvironment::Forest},{TEXT("cave"),EPokeMonsterBattleEnvironment::Cave},{TEXT("ruins"),EPokeMonsterBattleEnvironment::Ruins}};if(!Themes.Contains(Args[1]))return;D.BattleEnvironment=Themes[Args[1]];}
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(S,10);auto B=FPokeMonsterCreatureInstance::CreateFromSpecies(S,10);A.AssignMove(0,M);B.AssignMove(0,M);if(auto* Fire=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestFireSpecial.DA_TestFireSpecial")))A.AssignMove(1,Fire);if(auto* Status=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestStatus.DA_TestStatus")))A.AssignMove(2,Status);A.AssignMove(3,M);D.PlayerTeam.Add(A);D.OpponentTeam.Add(B);
  W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>()->StartEncounter(D,P);return;
 }
}));
// Inject actual Slate gamepad events only on explicit development request. No hardware claim.
static FAutoConsoleCommand Input(TEXT("pm.BattleView2.Input"),TEXT("Development review: Focus or Nintendo A/B/Left/Right/Up/Down through Slate."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||!FSlateApplication::IsInitialized())return;
 for(const auto& C:GEngine->GetWorldContexts()){auto* W=C.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();auto* Widget=E&&E->IsEncounterActive()?E->GetBattleWidget():nullptr;auto* Overworld=Cast<APokeMonsterOverworldPlayerController>(W->GetFirstPlayerController());auto* Menu=Overworld?Overworld->GetOverworldWidget():nullptr;if(!Widget&&!(Menu&&Menu->IsMenuOpen()))return;
  if(Args[0]==TEXT("Focus")){if(Widget){if(auto* B=Widget->GetCommandButton(0))B->SetKeyboardFocus();}else if(Menu)Menu->SetKeyboardFocus();return;}
  const TMap<FString,FKey> Keys={{TEXT("Enter"),EKeys::Enter},{TEXT("Escape"),EKeys::Escape},{TEXT("KeyDown"),EKeys::Down},{TEXT("KeyUp"),EKeys::Up},{TEXT("KeyRight"),EKeys::Right},{TEXT("KeyLeft"),EKeys::Left},{TEXT("A"),EKeys::Gamepad_FaceButton_Right},{TEXT("B"),EKeys::Gamepad_FaceButton_Bottom},{TEXT("Left"),EKeys::Gamepad_DPad_Left},{TEXT("Right"),EKeys::Gamepad_DPad_Right},{TEXT("Up"),EKeys::Gamepad_DPad_Up},{TEXT("Down"),EKeys::Gamepad_DPad_Down}};
  if(const auto* Key=Keys.Find(Args[0])){FKeyEvent Event(*Key,FModifierKeysState(),0,false,0,0);FSlateApplication::Get().ProcessKeyDownEvent(Event);FSlateApplication::Get().ProcessKeyUpEvent(Event);}return;
 }
}));
void SavePixels(const FString& File,const FIntPoint Size,const TArray<FColor>& Pixels)
{
 TArray64<uint8> PNG;FImageUtils::PNGCompressImageArray(Size.X,Size.Y,Pixels,PNG);FFileHelper::SaveArrayToFile(PNG,*File);
}
static FAutoConsoleCommand Capture(TEXT("pm.CreatureReview.CaptureLiveUI"),TEXT("Saved/GlumandaV11/LiveUI/<name>: exact Slate game viewport screenshot; never changes game camera or saves an asset."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||Args[0].IsEmpty())return;for(TCHAR C:Args[0])if(!FChar::IsAlnum(C)&&C!=TEXT('_'))return;
 const FString Dir=FPaths::ProjectSavedDir()/(Args[0].StartsWith(TEXT("PolishV4_"))?TEXT("CreaturePolishV4/LiveUI"):Args[0].StartsWith(TEXT("BattleV3_"))?TEXT("BattleSystemV3/LiveUI"):Args[0].StartsWith(TEXT("BattleV2_"))?TEXT("BattleViewV2/LiveUI"):TEXT("GlumandaV11/LiveUI"))/Args[0];if(IFileManager::Get().DirectoryExists(*Dir))return;
 for(const auto& Context:GEngine->GetWorldContexts()){
  auto* W=Context.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;
  auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();auto* Widget=E?E->GetBattleWidget():nullptr;auto* Overworld=Cast<APokeMonsterOverworldPlayerController>(W->GetFirstPlayerController());if(!Widget&&!(Overworld&&Overworld->IsMenuOpen()))continue;
  IFileManager::Get().MakeDirectory(*Dir,true);
  FString Meta=TEXT("ActualSlateViewport.png: actual Slate viewport screenshot, no offscreen widget layout or resizing.\n");
  auto* Client=W->GetGameInstance()->GetGameViewportClient();auto* VP=Client?Client->GetGameViewport():nullptr;
  if(VP)if(auto Slate=VP->GetViewportWidget().Pin()){
   FIntVector Size;TArray<FColor> Pixels;if(FSlateApplication::Get().TakeScreenshot(Slate.ToSharedRef(),Pixels,Size)){SavePixels(Dir/TEXT("ActualSlateViewport.png"),FIntPoint(Size.X,Size.Y),Pixels);Meta+=FString::Printf(TEXT("Actual size: %d x %d.\n"),Size.X,Size.Y);}
  }
  FFileHelper::SaveStringToFile(Meta,*(Dir/TEXT("CaptureMethod.txt")));return;
 }
}));
}
#endif
