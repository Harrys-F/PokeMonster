// Explicit review recording. Default framebuffer path is preserved; Slate mode includes actual UMG.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Containers/Ticker.h"
#include "HAL/IConsoleManager.h"
#include "HAL/FileManager.h"
#include "HAL/ThreadSafeCounter64.h"
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
// Bounded diagnostic comparison; unchanged default budget until measured.
static TAutoConsoleVariable<int32> CVarReadbackSlots(TEXT("pm.TAAReview.ReadbackSlots"),3,
 TEXT("Review-only staging budget, 3-6 buffers. Does not change game graphics or requested capture rate."));
struct FRecording : TSharedFromThis<FRecording,ESPMode::ThreadSafe>
{
 FString Directory,CSV=TEXT("frame,game_seconds,wall_seconds,width,height,file\n");
 int32 Frame=0;double Start=0,Last=-1;bool bSlate=false;float Interval=.05f;
 TAtomic<int32> Pending{0};TAtomic<bool> Stopping{false},RenderDrained{false};
 FTSTicker::FDelegateHandle Handle;FDelegateHandle SlateHandle,WorldCleanupHandle;
 TWeakObjectPtr<UWorld> CaptureWorld;
 int32 MaxReadbacks=3,CreatedReadbacks=0,BufferBusy=0,EncoderBusy=0;
 FThreadSafeCounter64 CopyMicros,ReadyMicros,JPEGMicros,WriteMicros;
 // These fields are render-thread-only in Slate mode.
 const SWindow* Window=nullptr;FIntRect Crop;double GameSeconds=0;
 struct FReadback
 {
  TUniquePtr<FRHIGPUTextureReadback> GPU;FIntPoint Size;double Game=0,Wall=0;bool bSwap=false;
 };
 TArray<FReadback> Readbacks;
 // Reuse staging resources instead of allocating and retiring one Metal buffer per frame.
 // All access is confined to the render thread and the total count is strictly bounded.
 TArray<TUniquePtr<FRHIGPUTextureReadback>> FreeReadbacks;
 void Save(FIntPoint Size,TArray<FColor>&& Pixels,double Game,double Wall)
 {
  if(!Frame)Start=Game;
  const FString File=FString::Printf(TEXT("Frame_%05d.jpg"),Frame++);
  CSV+=FString::Printf(TEXT("%d,%.9f,%.9f,%d,%d,%s\n"),Frame-1,Game-Start,Wall,Size.X,Size.Y,*File);
  ++Pending;
  Async(EAsyncExecution::ThreadPool,[Hold=AsShared(),Size,Data=MoveTemp(Pixels),Path=Directory/File]()
  {
   const double EncodeStart=FPlatformTime::Seconds();
   TArray64<uint8> Encoded;FImageUtils::CompressImage(Encoded,TEXT("jpg"),FImageView(Data.GetData(),Size.X,Size.Y),94);
   Hold->JPEGMicros.Add(int64((FPlatformTime::Seconds()-EncodeStart)*1.e6));
   const double WriteStart=FPlatformTime::Seconds();FFileHelper::SaveArrayToFile(Encoded,*Path);
   Hold->WriteMicros.Add(int64((FPlatformTime::Seconds()-WriteStart)*1.e6));--Hold->Pending;
  });
 }
 void PumpReadbacks()
 {
  check(IsInRenderingThread());
  while(!Readbacks.IsEmpty()&&Readbacks[0].GPU->IsReady())
  {
   auto& Read=Readbacks[0];ReadyMicros.Add(int64((FPlatformTime::Seconds()-Read.Wall)*1.e6));const double CopyStart=FPlatformTime::Seconds();int32 Pitch=0;const uint8* Data=static_cast<const uint8*>(Read.GPU->Lock(Pitch));
   if(Data)
   {
    TArray<FColor> Pixels;Pixels.SetNumUninitialized(Read.Size.X*Read.Size.Y);
    for(int Y=0;Y<Read.Size.Y;++Y)FMemory::Memcpy(Pixels.GetData()+Y*Read.Size.X,Data+Y*Pitch*4,Read.Size.X*4);
    Read.GPU->Unlock();
    if(Read.bSwap)for(auto& Pixel:Pixels)Swap(Pixel.R,Pixel.B);
    CopyMicros.Add(int64((FPlatformTime::Seconds()-CopyStart)*1.e6));Save(Read.Size,MoveTemp(Pixels),Read.Game,Read.Wall);
   }
   FreeReadbacks.Add(MoveTemp(Read.GPU));Readbacks.RemoveAt(0);
  }
  if(Stopping.Load()&&Readbacks.IsEmpty())RenderDrained.Store(true);
 }
 void OnPresent(SWindow& Presented,ISlateViewportProvider& Provider)
 {
  PumpReadbacks();
  if(Stopping.Load()||&Presented!=Window||GameSeconds-Last<Interval)return;
  if(Readbacks.Num()>=MaxReadbacks){++BufferBusy;return;}
  if(Pending.Load()>=3){++EncoderBusy;return;}
  FRHITexture* Texture=Provider.GetBackBufferResource();if(!Texture)return;
  const auto Format=Texture->GetFormat();
  if(Format!=PF_B8G8R8A8&&Format!=PF_R8G8B8A8)
  {FFileHelper::SaveStringToFile(TEXT("Unsupported native backbuffer format; no fabricated frames."),*(Directory/TEXT("Error.txt")));Stopping.Store(true);return;}
  const auto Extent=Texture->GetSizeXY();const FIntRect Rect(FIntPoint(FMath::Clamp(Crop.Min.X,0,Extent.X),FMath::Clamp(Crop.Min.Y,0,Extent.Y)),FIntPoint(FMath::Clamp(Crop.Max.X,0,Extent.X),FMath::Clamp(Crop.Max.Y,0,Extent.Y)));
  if(Rect.Width()<640||Rect.Height()<360)return;
  Last=GameSeconds;FReadback Read;Read.Size=Rect.Size();Read.Game=GameSeconds;Read.Wall=FPlatformTime::Seconds();Read.bSwap=Format==PF_R8G8B8A8;
  if(!FreeReadbacks.IsEmpty())Read.GPU=FreeReadbacks.Pop();
  else{Read.GPU=MakeUnique<FRHIGPUTextureReadback>(TEXT("PokeMonsterActualSlateReview"));++CreatedReadbacks;}
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
   FWorldDelegates::OnWorldBeginTearDown.Remove(WorldCleanupHandle);
   if(SlateHandle.IsValid()&&FSlateApplication::IsInitialized())FSlateApplication::Get().GetRenderer()->OnBackBufferReadyToPresent().Remove(SlateHandle);
   FFileHelper::SaveStringToFile(CSV,*(Directory/TEXT("Frames.csv")));
   const FString Metrics=FString::Printf(TEXT("{\"frames\":%d,\"readback_slots\":%d,\"created_readbacks\":%d,\"buffer_busy_skips\":%d,\"encoder_busy_skips\":%d,\"readback_wait_us_sum\":%lld,\"copy_us_sum\":%lld,\"jpeg_us_sum\":%lld,\"write_us_sum\":%lld}"),
    Frame,MaxReadbacks,CreatedReadbacks,BufferBusy,EncoderBusy,(long long)ReadyMicros.GetValue(),(long long)CopyMicros.GetValue(),(long long)JPEGMicros.GetValue(),(long long)WriteMicros.GetValue());
   FFileHelper::SaveStringToFile(Metrics,*(Directory/TEXT("Metrics.json")));
   FFileHelper::SaveStringToFile(FString::FromInt(Frame),*(Directory/TEXT("Complete.txt")));return false;
  }
  for(const auto& C:GEngine->GetWorldContexts())
  {
   UWorld* W=C.World();if(!W||!W->IsGameWorld()||!(W->GetMapName().Contains(TEXT("Dev_TestMap_VisualV2GPUBottleneckV1"))||W->GetMapName()==TEXT("Dev_TestMap_VisualV2")||W->GetMapName().EndsWith(TEXT("_Dev_TestMap_VisualV2"))||W->GetMapName()==TEXT("Dev_BiomeTestMap_V1")||W->GetMapName().EndsWith(TEXT("_Dev_BiomeTestMap_V1"))))continue;
   CaptureWorld=W;auto* GI=W->GetGameInstance();auto* Client=GI?GI->GetGameViewportClient():nullptr;auto* VP=Client?Client->GetGameViewport():nullptr;if(!VP)return true;
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
 IFileManager::Get().MakeDirectory(*Dir,true);Recording=MakeShared<FRecording,ESPMode::ThreadSafe>();Recording->Directory=Dir;Recording->MaxReadbacks=FMath::Clamp(CVarReadbackSlots.GetValueOnGameThread(),3,6);
 // Ending PIE/map travel must finish the review even if no further game Tick can run.
 // Never flush or wait synchronously inside world teardown.
 Recording->WorldCleanupHandle=FWorldDelegates::OnWorldBeginTearDown.AddLambda([Weak=Recording.ToWeakPtr()](UWorld* World)
 {if(auto Hold=Weak.Pin())if(Hold->CaptureWorld.Get()==World)Hold->Stopping.Store(true);});
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
