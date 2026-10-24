// Explicit AA review capture from Unreal's actual game viewport. Never enabled by default.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Containers/Ticker.h"
#include "HAL/IConsoleManager.h"
#include "HAL/FileManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "ImageUtils.h"
#include "Async/Async.h"
#include "Slate/SceneViewport.h"

#if !UE_BUILD_SHIPPING
namespace PMTAAReviewCapture
{
struct FRecording
{
 FString Directory,CSV=TEXT("frame,game_seconds,wall_seconds,width,height,file\n");
 int32 Frame=0;double Start=0,Last=-1;TAtomic<int32> Pending{0};bool Stopping=false;
 FTSTicker::FDelegateHandle Handle;
 bool Tick(float)
 {
  if(Stopping)
  {
   if(Pending.Load()>0)return true;
   FFileHelper::SaveStringToFile(CSV,*(Directory/TEXT("Frames.csv")));
   FFileHelper::SaveStringToFile(FString::FromInt(Frame),*(Directory/TEXT("Complete.txt")));
   return false;
  }
  if(Pending.Load()>=2)return true;
  for(const auto& C:GEngine->GetWorldContexts())
  {
   UWorld* W=C.World();if(!W||!W->IsGameWorld()||!(W->GetMapName().Contains(TEXT("Dev_TestMap_VisualV2GPUBottleneckV1"))||W->GetMapName()==TEXT("Dev_TestMap_VisualV2")||W->GetMapName().EndsWith(TEXT("_Dev_TestMap_VisualV2"))||W->GetMapName()==TEXT("Dev_BiomeTestMap_V1")||W->GetMapName().EndsWith(TEXT("_Dev_BiomeTestMap_V1"))))continue;
   auto* GI=W->GetGameInstance();auto* Client=GI?GI->GetGameViewportClient():nullptr;auto* VP=Client?Client->GetGameViewport():nullptr;
   if(!VP)return true;const double Now=W->GetTimeSeconds();if(Now-Last<.05)return true;Last=Now;
   const FIntPoint Size=VP->GetSizeXY();if(!((Size.X==1280&&Size.Y==720)||(Size.X==2560&&Size.Y==1440)))return true;
   TArray<FColor> Pixels;if(!GetViewportScreenShot(VP,Pixels))return true;
   if(!Frame)Start=Now;
   const FString File=FString::Printf(TEXT("Frame_%05d.jpg"),Frame++);
   CSV+=FString::Printf(TEXT("%d,%.9f,%.9f,%d,%d,%s\n"),Frame-1,Now-Start,FPlatformTime::Seconds(),Size.X,Size.Y,*File);
   ++Pending;
   Async(EAsyncExecution::ThreadPool,[this,Size,Data=MoveTemp(Pixels),Path=Directory/File]()
   {
    // JPEG encoding is much cheaper than lossless PNG for continuous review.
    // QHD shape/quality comparisons remain separate lossless screenshots.
    TArray64<uint8> Encoded;FImageUtils::CompressImage(Encoded,TEXT("jpg"),FImageView(Data.GetData(),Size.X,Size.Y),94);
    FFileHelper::SaveArrayToFile(Encoded,*Path);--Pending;
   });
   break;
  }
  return true;
 }
};
static TSharedPtr<FRecording> Recording;
static FAutoConsoleCommand Start(TEXT("pm.TAAReview.CaptureStart"),TEXT("Explicit real game framebuffer recording, 720p/QHD, <=20Hz, JPEG frames with actual game timestamps."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||Recording)return;
 const FString Root=FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()/TEXT("Saved/VisualV2TAAIntegrationV1/Recordings/"));
 const FString Dir=FPaths::ConvertRelativePathToFull(Args[0]);if(!Dir.StartsWith(Root)||IFileManager::Get().DirectoryExists(*Dir))return;
 IFileManager::Get().MakeDirectory(*Dir,true);Recording=MakeShared<FRecording>();Recording->Directory=Dir;
 Recording->Handle=FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([](float D){auto Hold=Recording;if(!Hold)return false;const bool Keep=Hold->Tick(D);if(!Keep)Recording.Reset();return Keep;}));
}));
static FAutoConsoleCommand Stop(TEXT("pm.TAAReview.CaptureStop"),TEXT("Finish recording after pending JPEG writes; no camera or quality changes."),FConsoleCommandDelegate::CreateLambda([](){if(Recording)Recording->Stopping=true;}));
}
#endif
