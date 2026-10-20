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
#include "Slate/WidgetRenderer.h"
#include "Slate/SceneViewport.h"
#include "Widgets/SViewport.h"
#include "Framework/Application/SlateApplication.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "GameFramework/PlayerController.h"
#if !UE_BUILD_SHIPPING
namespace PMCreatureReview
{
static FAutoConsoleCommand Start(TEXT("pm.CreatureReview.Start"),TEXT("Explicit runtime-only Glumanda versus Glumanda composition test: classic or world. No asset/save mutation."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||(Args[0]!=TEXT("classic")&&Args[0]!=TEXT("world")))return;
 for(const auto& C:GEngine->GetWorldContexts()){
  auto* W=C.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;auto* PC=W->GetFirstPlayerController();auto* P=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;if(!P)continue;
  auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
  auto* M=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));if(!S||!M)return;
  FPokeMonsterEncounterStartData D;D.EncounterId=TEXT("ExplicitGlumandaReview");D.PresentationMode=Args[0]==TEXT("classic")?EPokeMonsterBattlePresentationMode::ClassicBattle:EPokeMonsterBattlePresentationMode::WorldBattle;
  auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(S,10);auto B=FPokeMonsterCreatureInstance::CreateFromSpecies(S,10);A.AssignMove(0,M);B.AssignMove(0,M);D.PlayerTeam.Add(A);D.OpponentTeam.Add(B);
  W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>()->StartEncounter(D,P);return;
 }
}));
void SavePixels(const FString& File,const FIntPoint Size,const TArray<FColor>& Pixels)
{
 TArray64<uint8> PNG;FImageUtils::PNGCompressImageArray(Size.X,Size.Y,Pixels,PNG);FFileHelper::SaveArrayToFile(PNG,*File);
}
static FAutoConsoleCommand Capture(TEXT("pm.CreatureReview.CaptureLiveUI"),TEXT("Saved/GlumandaV11/LiveUI/<name>: exact Slate game viewport screenshot; never changes game camera or saves an asset."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||Args[0].IsEmpty())return;for(TCHAR C:Args[0])if(!FChar::IsAlnum(C)&&C!=TEXT('_'))return;
 const FString Dir=FPaths::ProjectSavedDir()/TEXT("GlumandaV11/LiveUI")/Args[0];if(IFileManager::Get().DirectoryExists(*Dir))return;
 for(const auto& Context:GEngine->GetWorldContexts()){
  auto* W=Context.World();if(!W||!W->IsGameWorld()||!W->GetGameInstance())continue;
  auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();auto* Widget=E?E->GetBattleWidget():nullptr;if(!Widget)continue;
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
