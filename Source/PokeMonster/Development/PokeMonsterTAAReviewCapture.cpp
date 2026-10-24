// Explicit review recording. Default framebuffer path is preserved; Slate mode includes actual UMG.
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
#include "Slate/SlateViewportProvider.h"
#include "Widgets/SViewport.h"
#include "Widgets/SWindow.h"
#include "Framework/Application/SlateApplication.h"
#include "Rendering/SlateRenderer.h"
#include "RenderingThread.h"
#include "RHICommandList.h"
#include "RHIGPUReadback.h"

#if !UE_BUILD_SHIPPING
namespace PMTAAReviewCapture
{
struct FRecording : TSharedFromThis<FRecording,ESPMode::ThreadSafe>
{
 FString Directory,CSV=TEXT("frame,game_seconds,wall_seconds,width,height,file\n");
 int32 Frame=0;double Start=0,Last=-1;bool bSlate=false;float Interval=.05f;
 TAtomic<int32> Pending{0};TAtomic<bool> Stopping{false},RenderDrained{false};
 FTSTicker::FDelegateHandle Handle;FDelegateHandle SlateHandle;
 // These fields are render-thread-only in Slate mode.
 const SWindow* Window=nullptr;FIntRect Crop;double GameSeconds=0;
 struct FReadback
 {
  TUniquePtr<FRHIGPUTextureReadback> GPU;FIntPoint Size;double Game=0,Wall=0;bool bSwap=false;
 };
 TArray<FReadback> Readbacks;
 void Save(FIntPoint Size,TArray<FColor>&& Pixels,double Game,double Wall)
 {
  if(!Frame)Start=Game;
  const FString File=FString::Printf(TEXT("Frame_%05d.jpg"),Frame++);
  CSV+=FString::Printf(TEXT("%d,%.9f,%.9f,%d,%d,%s\n"),Frame-1,Game-Start,Wall,Size.X,Size.Y,*File);
  ++Pending;
  Async(EAsyncExecution::ThreadPool,[Hold=AsShared(),Size,Data=MoveTemp(Pixels),Path=Directory/File]()
  {
   TArray64<uint8> Encoded;FImageUtils::CompressImage(Encoded,TEXT("jpg"),FImageView(Data.GetData(),Size.X,Size.Y),94);
   FFileHelper::SaveArrayToFile(Encoded,*Path);--Hold->Pending;
  });
 }
 void PumpReadbacks()
 {
  check(IsInRenderingThread());
  while(!Readbacks.IsEmpty()&&Readbacks[0].GPU->IsReady())
  {
   auto& Read=Readbacks[0];int32 Pitch=0;const uint8* Data=static_cast<const uint8*>(Read.GPU->Lock(Pitch));
   if(Data)
   {
    TArray<FColor> Pixels;Pixels.SetNumUninitialized(Read.Size.X*Read.Size.Y);
    for(int Y=0;Y<Read.Size.Y;++Y)FMemory::Memcpy(Pixels.GetData()+Y*Read.Size.X,Data+Y*Pitch*4,Read.Size.X*4);
    Read.GPU->Unlock();
    if(Read.bSwap)for(auto& Pixel:Pixels)Swap(Pixel.R,Pixel.B);
    Save(Read.Size,MoveTemp(Pixels),Read.Game,Read.Wall);
   }
   Readbacks.RemoveAt(0);
  }
  if(Stopping.Load()&&Readbacks.IsEmpty())RenderDrained.Store(true);
 }
 void OnPresent(SWindow& Presented,ISlateViewportProvider& Provider)
 {
  PumpReadbacks();
  if(Stopping.Load()||&Presented!=Window||GameSeconds-Last<Interval||Readbacks.Num()>=3||Pending.Load()>=3)return;
  FRHITexture* Texture=Provider.GetBackBufferResource();if(!Texture)return;
  const auto Format=Texture->GetFormat();
  if(Format!=PF_B8G8R8A8&&Format!=PF_R8G8B8A8)
  {FFileHelper::SaveStringToFile(TEXT("Unsupported native backbuffer format; no fabricated frames."),*(Directory/TEXT("Error.txt")));Stopping.Store(true);return;}
  const auto Extent=Texture->GetSizeXY();const FIntRect Rect(FIntPoint(FMath::Clamp(Crop.Min.X,0,Extent.X),FMath::Clamp(Crop.Min.Y,0,Extent.Y)),FIntPoint(FMath::Clamp(Crop.Max.X,0,Extent.X),FMath::Clamp(Crop.Max.Y,0,Extent.Y)));
  if(Rect.Width()<640||Rect.Height()<360)return;
  Last=GameSeconds;FReadback Read;Read.Size=Rect.Size();Read.Game=GameSeconds;Read.Wall=FPlatformTime::Seconds();Read.bSwap=Format==PF_R8G8B8A8;
  Read.GPU=MakeUnique<FRHIGPUTextureReadback>(TEXT("PokeMonsterActualSlateReview"));
  Read.GPU->EnqueueCopy(FRHICommandListExecutor::GetImmediateCommandList(),Texture,FResolveRect(Rect.Min.X,Rect.Min.Y,Rect.Max.X,Rect.Max.Y));Readbacks.Add(MoveTemp(Read));
 }
 bool Tick(float)
 {
  if(Stopping.Load())
  {
   if(bSlate)
   {
    ENQUEUE_RENDER_COMMAND(PMDrainReview)([Hold=AsShared()](FRHICommandListImmediate&){Hold->PumpReadbacks();});
    if(!RenderDrained.Load())return true;
   }
   if(Pending.Load()>0)return true;
   if(SlateHandle.IsValid()&&FSlateApplication::IsInitialized())FSlateApplication::Get().GetRenderer()->OnBackBufferReadyToPresent().Remove(SlateHandle);
   FFileHelper::SaveStringToFile(CSV,*(Directory/TEXT("Frames.csv")));
   FFileHelper::SaveStringToFile(FString::FromInt(Frame),*(Directory/TEXT("Complete.txt")));return false;
  }
  for(const auto& C:GEngine->GetWorldContexts())
  {
   UWorld* W=C.World();if(!W||!W->IsGameWorld()||!(W->GetMapName().Contains(TEXT("Dev_TestMap_VisualV2GPUBottleneckV1"))||W->GetMapName()==TEXT("Dev_TestMap_VisualV2")||W->GetMapName().EndsWith(TEXT("_Dev_TestMap_VisualV2"))||W->GetMapName()==TEXT("Dev_BiomeTestMap_V1")||W->GetMapName().EndsWith(TEXT("_Dev_BiomeTestMap_V1"))))continue;
   auto* GI=W->GetGameInstance();auto* Client=GI?GI->GetGameViewportClient():nullptr;auto* VP=Client?Client->GetGameViewport():nullptr;if(!VP)return true;
   const double Now=W->GetTimeSeconds();
   if(bSlate)
   {
    auto View=VP->GetViewportWidget().Pin();auto SlateWindow=View?FSlateApplication::Get().FindWidgetWindow(View.ToSharedRef()):nullptr;if(!View||!SlateWindow)return true;
    // Same geometry basis as Slate's screenshot implementation, without its redraw/tick/readback stall.
    const auto G=View->GetCachedGeometry();const FVector2D Position=G.GetAbsolutePosition()-FVector2D(SlateWindow->GetPositionInScreen());const FVector2D Size=G.GetDrawSize();
    const FIntRect Rect(FIntPoint(FMath::RoundToInt(Position.X),FMath::RoundToInt(Position.Y)),FIntPoint(FMath::RoundToInt(Position.X+Size.X),FMath::RoundToInt(Position.Y+Size.Y)));
    ENQUEUE_RENDER_COMMAND(PMReviewViewport)([Hold=AsShared(),Target=SlateWindow.Get(),Rect,Now](FRHICommandListImmediate&){Hold->Window=Target;Hold->Crop=Rect;Hold->GameSeconds=Now;Hold->PumpReadbacks();});
   }
   else
   {
    if(Pending.Load()>=2||Now-Last<Interval)return true;Last=Now;
    const FIntPoint Size=VP->GetSizeXY();if(!((Size.X==1280&&Size.Y==720)||(Size.X==2560&&Size.Y==1440)))return true;
    TArray<FColor> Pixels;if(GetViewportScreenShot(VP,Pixels))Save(Size,MoveTemp(Pixels),Now,FPlatformTime::Seconds());
   }
   break;
  }
  return true;
 }
};
static TSharedPtr<FRecording,ESPMode::ThreadSafe> Recording;
static FAutoConsoleCommand StartCommand(TEXT("pm.TAAReview.CaptureStart"),TEXT("Actual framebuffer (default <=20Hz), or path slate 10-60: asynchronously record presented game viewport including UMG. Original timestamps, no interpolation; requested rate is only a ceiling."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if((Args.Num()!=1&&Args.Num()!=3)||Recording)return;
 if(Args.Num()==3&&(Args[1]!=TEXT("slate")||!Args[2].IsNumeric()||FCString::Atoi(*Args[2])<10||FCString::Atoi(*Args[2])>60))return;
 const FString Root=FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()/TEXT("Saved/VisualV2TAAIntegrationV1/Recordings/"));
 const FString Dir=FPaths::ConvertRelativePathToFull(Args[0]);if(!Dir.StartsWith(Root)||IFileManager::Get().DirectoryExists(*Dir))return;
 IFileManager::Get().MakeDirectory(*Dir,true);Recording=MakeShared<FRecording,ESPMode::ThreadSafe>();Recording->Directory=Dir;
 if(Args.Num()==3)
 {
  Recording->bSlate=true;Recording->Interval=1.f/FCString::Atoi(*Args[2]);
  Recording->SlateHandle=FSlateApplication::Get().GetRenderer()->OnBackBufferReadyToPresent().AddLambda([Weak=Recording.ToWeakPtr()](SWindow& Window,ISlateViewportProvider& Provider){if(auto Hold=Weak.Pin())Hold->OnPresent(Window,Provider);});
 }
 FFileHelper::SaveStringToFile(Recording->bSlate?TEXT("Actual presented Slate game viewport including UMG, cropped from native backbuffer via asynchronous GPU readback. No redraw or interpolated frames. Original game timestamps.\n"):TEXT("Game framebuffer excluding Slate UI; original timestamps.\n"),*(Dir/TEXT("CaptureMethod.txt")));
 Recording->Handle=FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([](float D){auto Hold=Recording;if(!Hold)return false;const bool Keep=Hold->Tick(D);if(!Keep)Recording.Reset();return Keep;}));
}));
static FAutoConsoleCommand StopCommand(TEXT("pm.TAAReview.CaptureStop"),TEXT("Finish after GPU readbacks and pending JPEG writes; no camera/quality changes."),FConsoleCommandDelegate::CreateLambda([](){if(Recording)Recording->Stopping.Store(true);}));
}
#endif
