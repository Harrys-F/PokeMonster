// Explicit opt-in profiling only; no production gameplay or automatic quality changes.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Engine/PostProcessVolume.h"
#include "EngineUtils.h"
#include "HAL/IConsoleManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/FileManager.h"
#include "Containers/Ticker.h"
#include "Slate/SceneViewport.h"
#include "Widgets/SWindow.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Pawn.h"
#include "Camera/PlayerCameraManager.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/LightComponent.h"
#include "SceneView.h"
#include "SceneViewExtension.h"
#include "DynamicResolutionState.h"

#if !UE_BUILD_SHIPPING
namespace PMEnvironmentPerf
{
// Reads the renderer driver's upper bound with dynamic resolution explicitly disabled.
// Internal dimensions are derived using UE 5.8 ApplyResolutionFraction (ceil), not an allocation readback.
struct FResolutionState { FCriticalSection Lock; FIntPoint Output=FIntPoint::ZeroValue,Internal=FIntPoint::ZeroValue; float Primary=0,Secondary=0; uint64 Samples=0; };
class FResolutionObserver : public FSceneViewExtensionBase
{
public:
 FResolutionObserver(const FAutoRegister& A,TSharedRef<FResolutionState,ESPMode::ThreadSafe> S,FViewport* V):FSceneViewExtensionBase(A),State(S),Viewport(V){}
 void PreRenderViewFamily_RenderThread(FRDGBuilder&,FSceneViewFamily& F) override
 {
  if(F.RenderTarget!=Viewport||F.Views.IsEmpty()||!F.GetScreenPercentageInterface())return;
  const auto* V=F.Views[0];const auto Fractions=F.GetScreenPercentageInterface()->GetResolutionFractionsUpperBound();
  const float Primary=Fractions[GDynamicPrimaryResolutionFraction],Secondary=F.SecondaryViewFraction;
  FScopeLock L(&State->Lock);State->Primary=Primary;State->Secondary=Secondary;State->Output=V->UnscaledViewRect.Size();
  State->Internal=FIntPoint(FMath::CeilToInt(State->Output.X*Primary*Secondary),FMath::CeilToInt(State->Output.Y*Primary*Secondary));++State->Samples;
 }
private:TSharedRef<FResolutionState,ESPMode::ThreadSafe> State;FViewport* Viewport;
};
struct FComponentState { TWeakObjectPtr<UPrimitiveComponent> C;bool Visible,Shadow;int32 ForcedLOD=0,CullStart=0,CullEnd=0; };
struct FPostState { TWeakObjectPtr<APostProcessVolume> V;FPostProcessSettings Settings; };
struct FRow { FString Site,Condition;int32 Repeat=0,Width=1280,Height=740,Quality=1,Percentage=75; };
struct FProbe : public TSharedFromThis<FProbe>
{
 TWeakObjectPtr<UWorld> World;TWeakObjectPtr<APawn> Player;FTransform PlayerBefore;TArray<FComponentState> Components;TArray<FPostState> PostVolumes;
 TMap<FString,FString> CVars,Factors;TMap<FString,EConsoleVariableFlags> Priorities,FactorPriorities;TArray<FRow> Rows;int32 Index=0;float Warmup=5,Duration=8;FString Label,Mode,Directory,Frames,Segments,Settings;double Start=0,Last=0;bool Capturing=false,Initialized=false;
 TSharedPtr<FResolutionObserver,ESPMode::ThreadSafe> Observer;TSharedRef<FResolutionState,ESPMode::ThreadSafe> Resolution=MakeShared<FResolutionState,ESPMode::ThreadSafe>();FTSTicker::FDelegateHandle Handle;
 UWorld* FindWorld(){for(const auto& C:GEngine->GetWorldContexts())if(C.World()&&(C.WorldType==EWorldType::PIE||C.WorldType==EWorldType::Game))return C.World();return nullptr;}
 FSceneViewport* Viewport(){auto* W=World.Get();auto* C=W&&W->GetGameInstance()?W->GetGameInstance()->GetGameViewportClient():nullptr;return C?C->GetGameViewport():nullptr;}
 void Set(const FString& N,const FString& Value,bool Factor=false){if(auto* V=IConsoleManager::Get().FindConsoleVariable(*N)){auto Priority=(EConsoleVariableFlags)(V->GetFlags()&ECVF_SetByMask);if(!CVars.Contains(N)){CVars.Add(N,V->GetString());Priorities.Add(N,Priority);}if(Factor&&!Factors.Contains(N)){Factors.Add(N,V->GetString());FactorPriorities.Add(N,Priority);}V->Set(*Value,ECVF_SetByConsole,TEXT("PM_EnvPerf"));}}
 void RestoreVar(const FString& N,const FString& Value,EConsoleVariableFlags Priority){if(auto* V=IConsoleManager::Get().FindConsoleVariable(*N)){V->Unset(ECVF_SetByConsole,TEXT("PM_EnvPerf"));V->ClearFlags(ECVF_SetByMask);V->Set(*Value,Priority);}}
 void RestoreFactors(){for(const auto& P:Factors)RestoreVar(P.Key,P.Value,FactorPriorities[P.Key]);Factors.Empty();FactorPriorities.Empty();for(const auto& S:Components)if(auto* C=S.C.Get()){C->SetVisibility(S.Visible);C->SetCastShadow(S.Shadow);if(auto* M=Cast<UStaticMeshComponent>(C))M->SetForcedLodModel(S.ForcedLOD);if(auto* I=Cast<UInstancedStaticMeshComponent>(C))I->SetCullDistances(S.CullStart,S.CullEnd);}for(const auto& P:PostVolumes)if(auto* V=P.V.Get())V->Settings=P.Settings;}
 bool Vegetation(UPrimitiveComponent* C,bool TreesOnly=false){auto* S=Cast<UStaticMeshComponent>(C);if(!S||!S->GetStaticMesh())return false;auto N=S->GetStaticMesh()->GetName();if(!N.StartsWith(TEXT("SM_WLA_")))return false;return N.Contains(TEXT("Oak"))||N.Contains(TEXT("Birch"))||(!TreesOnly&&(N.Contains(TEXT("Bush"))||N.Contains(TEXT("Grass"))||N.Contains(TEXT("Fern"))||N.Contains(TEXT("Flower"))||N.Contains(TEXT("Herb"))));}
 bool Initialize()
 {
  auto* W=FindWorld();if(!W)return false;World=W;Player=UGameplayStatics::GetPlayerPawn(W,0);if(!Player.IsValid()||!Viewport())return false;
  PlayerBefore=Player->GetActorTransform();for(TObjectIterator<UPrimitiveComponent> I;I;++I)if(I->GetWorld()==W&&I->IsRegistered()){FComponentState S{*I,I->IsVisible(),!!I->CastShadow};if(auto* M=Cast<UStaticMeshComponent>(*I))S.ForcedLOD=M->GetForcedLodModel();if(auto* M=Cast<UInstancedStaticMeshComponent>(*I))M->GetCullDistances(S.CullStart,S.CullEnd);Components.Add(S);}
  for(TActorIterator<APostProcessVolume> I(W);I;++I)PostVolumes.Add({*I,I->Settings});
  Set(TEXT("r.VSync"),TEXT("0"));Set(TEXT("t.MaxFPS"),TEXT("0"));Set(TEXT("r.GPUCsvStatsEnabled"),TEXT("1"));Set(TEXT("r.DynamicRes.OperationMode"),TEXT("0"));Set(TEXT("r.Editor.Viewport.OverridePIEScreenPercentage"),TEXT("0"));Set(TEXT("r.SecondaryScreenPercentage.GameViewport"),TEXT("100"));
  Observer=FSceneViewExtensions::NewExtension<FResolutionObserver>(Resolution,Viewport());
  Frames=TEXT("segment,site,condition,repeat,quality,percentage,utc,frame_ms,viewport_w,viewport_h,target_w,target_h,window_slate_w,window_slate_h,window_dpi,view_w,view_h,internal_w,internal_h,primary_fraction,secondary_fraction,renderer_samples,camera_x,camera_y,camera_z,pitch,yaw,fov,window_active\n");
  Segments=TEXT("segment,site,condition,repeat,start_utc,end_utc,mode,width,height,quality,percentage\n");Initialized=true;BeginRow();return true;
 }
 void BeginRow()
 {
  RestoreFactors();const auto& R=Rows[Index];const auto& C=R.Condition;
  for(const TCHAR* N:{TEXT("sg.ViewDistanceQuality"),TEXT("sg.AntiAliasingQuality"),TEXT("sg.ShadowQuality"),TEXT("sg.GlobalIlluminationQuality"),TEXT("sg.ReflectionQuality"),TEXT("sg.PostProcessQuality"),TEXT("sg.TextureQuality"),TEXT("sg.EffectsQuality"),TEXT("sg.FoliageQuality"),TEXT("sg.ShadingQuality")})Set(N,FString::FromInt(R.Quality));
  Set(TEXT("r.ScreenPercentage"),FString::FromInt(R.Percentage));Viewport()->SetFixedViewportSize(R.Width,R.Height);
  FVector P=R.Site==TEXT("Dorf")?FVector(-4100,450,50.15):R.Site==TEXT("Wald")?FVector(-4300,1550,50.15):R.Site==TEXT("NPCWald")?FVector(-760,-1410,50.15):FVector(-36.6,-47.1,50.15);
  Player->SetActorLocation(P,false,nullptr,ETeleportType::TeleportPhysics);
  for(const auto& S:Components)if(auto* PComp=S.C.Get())if(Vegetation(PComp))
  {if(C==TEXT("VegetationHidden"))PComp->SetVisibility(false);if(C==TEXT("VegetationNoShadow")||(C==TEXT("TreeNoShadow")&&Vegetation(PComp,true)))PComp->SetCastShadow(false);
   if(C==TEXT("TreeLOD1")&&Vegetation(PComp,true))CastChecked<UStaticMeshComponent>(PComp)->SetForcedLodModel(2);
   if(C==TEXT("FernLOD1")&&CastChecked<UStaticMeshComponent>(PComp)->GetStaticMesh()->GetName().Contains(TEXT("Fern")))CastChecked<UStaticMeshComponent>(PComp)->SetForcedLodModel(2);
   if(C==TEXT("SmallFoliageCull"))if(auto* I=Cast<UInstancedStaticMeshComponent>(PComp)){const auto N=I->GetStaticMesh()->GetName();if(!N.Contains(TEXT("Bush"))&&!Vegetation(PComp,true))I->SetCullDistances(3200,4300);}
  }
  for(const auto& Post:PostVolumes)if(auto* V=Post.V.Get())if(V->bUnbound)
  {
   if(C==TEXT("GIFinalGatherHalf")){V->Settings.bOverride_LumenFinalGatherQuality=true;V->Settings.LumenFinalGatherQuality=.5f;}
   if(C==TEXT("ReflectionHalf")){V->Settings.bOverride_LumenReflectionQuality=true;V->Settings.LumenReflectionQuality=.5f;}
  }
  if(C==TEXT("MapCandidate"))
  {
   Set(TEXT("r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor"),TEXT("2"),true);
   Set(TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"),TEXT("2"),true);
  }
  if(C==TEXT("MapCandidate"))for(const auto& Post:PostVolumes)if(auto* V=Post.V.Get())
  {
   // Map-local postprocess settings; preserve the existing interior's original look.
   V->Settings.bOverride_BloomIntensity=true;V->Settings.bOverride_MotionBlurAmount=true;
   V->Settings.BloomIntensity=V->bUnbound?0.f:Post.Settings.BloomIntensity;
   V->Settings.MotionBlurAmount=V->bUnbound?0.f:Post.Settings.MotionBlurAmount;
  }
  const TMap<FString,TPair<FString,FString>> Tests={
   {TEXT("BloomOff"),{TEXT("r.BloomQuality"),TEXT("0")}}, {TEXT("AOOff"),{TEXT("r.AmbientOcclusionLevels"),TEXT("0")}},
   {TEXT("MotionBlurOff"),{TEXT("r.MotionBlurQuality"),TEXT("0")}}, {TEXT("DOFOff"),{TEXT("r.DepthOfFieldQuality"),TEXT("0")}},
   {TEXT("TonemapperFast"),{TEXT("r.Tonemapper.Quality"),TEXT("3")}}, {TEXT("TSRHistory100"),{TEXT("r.TSR.History.ScreenPercentage"),TEXT("100")}},
   {TEXT("LumenIntegrate2"),{TEXT("r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor"),TEXT("2")}},
   {TEXT("ShadowRes1024"),{TEXT("r.Shadow.MaxResolution"),TEXT("1024")}}, {TEXT("ShadowDistanceHalf"),{TEXT("r.Shadow.DistanceScale"),TEXT("0.5")}},
   {TEXT("VSMBiasPlus1"),{TEXT("r.Shadow.Virtual.ResolutionLodBiasDirectional"),TEXT("1")}}, {TEXT("VSMRayCount2"),{TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"),TEXT("2")}},
   {TEXT("AllShadowsOff"),{TEXT("ShowFlag.DynamicShadows"),TEXT("0")}}, {TEXT("PostProcessingOff"),{TEXT("ShowFlag.PostProcessing"),TEXT("0")}}
  };
  if(const auto* T=Tests.Find(C))Set(T->Key,T->Value,true);
  Settings+=FString::Printf(TEXT("segment=%d site=%s condition=%s repeat=%d utc=%s\n"),Index,*R.Site,*C,R.Repeat,*FDateTime::UtcNow().ToIso8601());
  for(const TCHAR* N:{TEXT("sg.ViewDistanceQuality"),TEXT("sg.AntiAliasingQuality"),TEXT("sg.ShadowQuality"),TEXT("sg.GlobalIlluminationQuality"),TEXT("sg.ReflectionQuality"),TEXT("sg.PostProcessQuality"),TEXT("sg.TextureQuality"),TEXT("sg.EffectsQuality"),TEXT("sg.FoliageQuality"),TEXT("sg.ShadingQuality"),TEXT("r.ScreenPercentage"),TEXT("r.DynamicRes.OperationMode"),TEXT("r.VSync"),TEXT("t.MaxFPS"),TEXT("r.Shadow.Virtual.Enable"),TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"),TEXT("r.Shadow.Virtual.ResolutionLodBiasDirectional"),TEXT("r.Shadow.MaxResolution"),TEXT("r.Shadow.DistanceScale"),TEXT("r.AntiAliasingMethod"),TEXT("r.Lumen.FinalGatherMethod"),TEXT("r.Lumen.Reflections.Allow"),TEXT("r.BloomQuality"),TEXT("r.MotionBlurQuality")})if(auto* V=IConsoleManager::Get().FindConsoleVariable(N))Settings+=FString::Printf(TEXT("%s=%s priority=%d\n"),N,*V->GetString(),(int32)(V->GetFlags()&ECVF_SetByMask));
  for(const auto& Post:PostVolumes)if(auto* V=Post.V.Get())Settings+=FString::Printf(TEXT("volume=%s unbound=%d bloom=%.6f override_bloom=%d motionblur=%.6f override_motionblur=%d finalgather=%.6f override_finalgather=%d\n"),*V->GetName(),V->bUnbound,V->Settings.BloomIntensity,V->Settings.bOverride_BloomIntensity,V->Settings.MotionBlurAmount,V->Settings.bOverride_MotionBlurAmount,V->Settings.LumenFinalGatherQuality,V->Settings.bOverride_LumenFinalGatherQuality);
  Start=Last=FPlatformTime::Seconds();Capturing=false;
 }
 void Save(){FFileHelper::SaveStringToFile(Frames,*(Directory/(Label+TEXT("_Frames.csv"))));FFileHelper::SaveStringToFile(Segments,*(Directory/(Label+TEXT("_Segments.csv"))));FFileHelper::SaveStringToFile(Settings,*(Directory/(Label+TEXT("_Settings.txt"))));}
 void Stop(const FString& Error=TEXT(""))
 {
  if(Capturing&&World.IsValid())GEngine->Exec(World.Get(),TEXT("csvprofile stop"));RestoreFactors();Observer.Reset();
  // Restore factors before scalability so their lower-priority settings can take effect again.
  for(const auto& P:CVars)if(!P.Key.StartsWith(TEXT("sg.")))RestoreVar(P.Key,P.Value,Priorities[P.Key]);
  for(const auto& P:CVars)if(P.Key.StartsWith(TEXT("sg.")))RestoreVar(P.Key,P.Value,Priorities[P.Key]);
  if(auto* V=Viewport())V->SetFixedViewportSize(0,0);if(Player.IsValid())Player->SetActorTransform(PlayerBefore,false,nullptr,ETeleportType::TeleportPhysics);
  Save();FFileHelper::SaveStringToFile(Error.IsEmpty()?TEXT("Complete"):Error,*(Directory/(Label+TEXT("_Done.txt"))));UE_LOG(LogTemp,Display,TEXT("PM_ENV_PERF_DONE %s %s"),*Label,*Error);FTSTicker::GetCoreTicker().RemoveTicker(Handle);
  if(Mode==TEXT("Standalone")&&World.IsValid())GEngine->Exec(World.Get(),TEXT("quit"));
 }
 bool Tick(float)
 {
  if(!Initialized){if(!Initialize())return true;}if(!Player.IsValid()||!Viewport()){Stop(TEXT("PIE or viewport lost"));return false;}
  double Now=FPlatformTime::Seconds(),Elapsed=Now-Start,Ms=(Now-Last)*1000;Last=Now;if(Elapsed<Warmup)return true;const auto& R=Rows[Index];
  if(!Capturing){GEngine->Exec(World.Get(),*FString::Printf(TEXT("csvprofile startfile=ENV1_%s_%03d"),*Label,Index));GEngine->Exec(World.Get(),TEXT("csvprofile start"));Capturing=true;Segments+=FString::Printf(TEXT("%d,%s,%s,%d,%s,"),Index,*R.Site,*R.Condition,R.Repeat,*FDateTime::UtcNow().ToIso8601());return true;}
  auto* VP=Viewport();auto Size=VP->GetSizeXY(),Target=VP->GetRenderTargetTextureSizeXY();auto Window=VP->FindWindow();auto WS=Window.IsValid()?Window->GetSizeInScreen():FVector2D::ZeroVector;float DPI=Window.IsValid()?Window->GetDPIScaleFactor():0;
  FIntPoint View,Internal;float Primary,Secondary;uint64 Samples;{FScopeLock L(&Resolution->Lock);View=Resolution->Output;Internal=Resolution->Internal;Primary=Resolution->Primary;Secondary=Resolution->Secondary;Samples=Resolution->Samples;}
  auto* Cam=UGameplayStatics::GetPlayerController(World.Get(),0)->PlayerCameraManager.Get();auto P=Cam->GetCameraLocation();auto Rot=Cam->GetCameraRotation();
  Frames+=FString::Printf(TEXT("%d,%s,%s,%d,%d,%d,%s,%.6f,%d,%d,%d,%d,%.2f,%.2f,%.3f,%d,%d,%d,%d,%.5f,%.5f,%llu,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%d\n"),Index,*R.Site,*R.Condition,R.Repeat,R.Quality,R.Percentage,*FDateTime::UtcNow().ToIso8601(),Ms,Size.X,Size.Y,Target.X,Target.Y,WS.X,WS.Y,DPI,View.X,View.Y,Internal.X,Internal.Y,Primary,Secondary,Samples,P.X,P.Y,P.Z,Rot.Pitch,Rot.Yaw,Cam->GetFOVAngle(),Window.IsValid()&&Window->IsActive());
  if(Elapsed<Warmup+Duration)return true;GEngine->Exec(World.Get(),TEXT("csvprofile stop"));Capturing=false;Segments+=FString::Printf(TEXT("%s,%s,%d,%d,%d,%d\n"),*FDateTime::UtcNow().ToIso8601(),*Mode,Size.X,Size.Y,R.Quality,R.Percentage);Save();
  if(++Index>=Rows.Num()){Stop();return false;}BeginRow();return true;
 }
};
static TSharedPtr<FProbe> Active;
static FAutoConsoleCommand SetViewport(TEXT("pm.EnvPerf.Viewport"),TEXT("Explicit review viewport width height; 0 0 restores automatic sizing. Does not move the player."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=2||Active)return;
 const int32 Width=FCString::Atoi(*Args[0]),Height=FCString::Atoi(*Args[1]);
 if(!((Width==0&&Height==0)||(Width>=320&&Height>=240&&Width<=4096&&Height<=4096)))return;
 for(const auto& Context:GEngine->GetWorldContexts())if(auto* W=Context.World())if(Context.WorldType==EWorldType::PIE||Context.WorldType==EWorldType::Game)
  if(auto* GI=W->GetGameInstance())if(auto* Client=GI->GetGameViewportClient())if(auto* VP=Client->GetGameViewport()){VP->SetFixedViewportSize(Width,Height);return;}
}));
static FAutoConsoleCommand Run(TEXT("pm.EnvPerf.Run"),TEXT("Opt-in scoped environment probe. TSV header label/mode/warmup/duration; rows site/factor/repeat/width/height/quality/percentage."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||Active)return;FString Text;if(!FFileHelper::LoadFileToString(Text,*Args[0]))return;TArray<FString> Lines;Text.ParseIntoArrayLines(Lines);if(Lines.Num()<2)return;TArray<FString> H;Lines[0].ParseIntoArray(H,TEXT("\t"),false);if(H.Num()!=4)return;
 auto P=MakeShared<FProbe>();P->Label=H[0];P->Mode=H[1];P->Warmup=FCString::Atof(*H[2]);P->Duration=FCString::Atof(*H[3]);P->Directory=FPaths::ProjectSavedDir()/TEXT("EnvironmentPerfV1");IFileManager::Get().MakeDirectory(*P->Directory,true);
 for(int32 I=1;I<Lines.Num();++I){TArray<FString> F;Lines[I].ParseIntoArray(F,TEXT("\t"),false);if(F.Num()==7)P->Rows.Add({F[0],F[1],FCString::Atoi(*F[2]),FCString::Atoi(*F[3]),FCString::Atoi(*F[4]),FCString::Atoi(*F[5]),FCString::Atoi(*F[6])});}
 if(P->Rows.IsEmpty())return;Active=P;P->Handle=FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([](float D){auto P=Active;bool Keep=P->Tick(D);if(!Keep)Active.Reset();return Keep;}));
}));
static FAutoConsoleCommand Stop(TEXT("pm.EnvPerf.Stop"),TEXT("Stop explicit environment probe and restore all temporary state."),FConsoleCommandDelegate::CreateLambda([](){if(Active){Active->Stop(TEXT("Cancelled"));Active.Reset();}}));
}
#endif
