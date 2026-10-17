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
#include "ProfilingDebugging/CsvProfiler.h"
#include "../Characters/PokeMonsterNPCVisualActor.h"
#include "Animation/AnimSequence.h"
#include "Engine/SkeletalMesh.h"
#include "Rendering/SkeletalMeshRenderData.h"
#include "Components/SkeletalMeshComponent.h"
#include "UObject/StrongObjectPtr.h"

#if !UE_BUILD_SHIPPING
namespace PMNPCMotionV2
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
struct FComponentState { TWeakObjectPtr<UPrimitiveComponent> C;bool Visible,Shadow;int32 ForcedLOD=0,CullStart=0,CullEnd=0,MinLOD=0;bool OverrideMinLOD=false; };
struct FPostState { TWeakObjectPtr<APostProcessVolume> V;FPostProcessSettings Settings; };
struct FRow { FString Site,Condition;int32 Repeat=0,Width=1280,Height=740,Quality=1,Percentage=75; };
struct FProbe : public TSharedFromThis<FProbe>
{
 TWeakObjectPtr<APokeMonsterNPCVisualActor> Ranger;
 TStrongObjectPtr<USkeletalMesh> SavedMesh;TStrongObjectPtr<UAnimSequence> SavedIdle,SavedTalk;bool SavedMotion=false,SavedAccessories=false;
 TWeakObjectPtr<UWorld> World;TWeakObjectPtr<APawn> Player;FTransform PlayerBefore;TArray<FComponentState> Components;TArray<FPostState> PostVolumes;
 TMap<FString,FString> CVars,Factors;TMap<FString,EConsoleVariableFlags> Priorities,FactorPriorities;TArray<FRow> Rows;int32 Index=0;float Warmup=5,Duration=8;FString Label,Mode,Directory,Frames,Segments,Settings;double Start=0,Last=0;bool Capturing=false,Initialized=false;
 TSharedPtr<FResolutionObserver,ESPMode::ThreadSafe> Observer;TSharedRef<FResolutionState,ESPMode::ThreadSafe> Resolution=MakeShared<FResolutionState,ESPMode::ThreadSafe>();FTSTicker::FDelegateHandle Handle;
 UWorld* FindWorld(){for(const auto& C:GEngine->GetWorldContexts())if(C.World()&&(C.WorldType==EWorldType::PIE||C.WorldType==EWorldType::Game))return C.World();return nullptr;}
 FSceneViewport* Viewport(){auto* W=World.Get();auto* C=W&&W->GetGameInstance()?W->GetGameInstance()->GetGameViewportClient():nullptr;return C?C->GetGameViewport():nullptr;}
 void Set(const FString& N,const FString& Value,bool Factor=false){if(auto* V=IConsoleManager::Get().FindConsoleVariable(*N)){auto Priority=(EConsoleVariableFlags)(V->GetFlags()&ECVF_SetByMask);if(!CVars.Contains(N)){CVars.Add(N,V->GetString());Priorities.Add(N,Priority);}if(Factor&&!Factors.Contains(N)){Factors.Add(N,V->GetString());FactorPriorities.Add(N,Priority);}V->Set(*Value,ECVF_SetByConsole,TEXT("PM_NPCMotion2"));}}
 void RestoreVar(const FString& N,const FString& Value,EConsoleVariableFlags Priority){if(auto* V=IConsoleManager::Get().FindConsoleVariable(*N)){V->Unset(ECVF_SetByConsole,TEXT("PM_NPCMotion2"));V->ClearFlags(ECVF_SetByMask);V->Set(*Value,Priority);}}
 void RestoreFactors(){for(const auto& P:Factors)RestoreVar(P.Key,P.Value,FactorPriorities[P.Key]);Factors.Empty();FactorPriorities.Empty();for(const auto& S:Components)if(auto* C=S.C.Get()){C->SetVisibility(S.Visible);C->SetCastShadow(S.Shadow);if(auto* M=Cast<UStaticMeshComponent>(C)){M->SetForcedLodModel(S.ForcedLOD);if(M->MinLOD!=S.MinLOD||M->bOverrideMinLOD!=S.OverrideMinLOD){M->MinLOD=S.MinLOD;M->bOverrideMinLOD=S.OverrideMinLOD;M->MarkRenderStateDirty();}}if(auto* I=Cast<UInstancedStaticMeshComponent>(C))I->SetCullDistances(S.CullStart,S.CullEnd);}for(const auto& P:PostVolumes)if(auto* V=P.V.Get())V->Settings=P.Settings;}
 bool Vegetation(UPrimitiveComponent* C,bool TreesOnly=false){auto* S=Cast<UStaticMeshComponent>(C);if(!S||!S->GetStaticMesh())return false;auto N=S->GetStaticMesh()->GetName();if(!N.StartsWith(TEXT("SM_WLA_")))return false;return N.Contains(TEXT("Oak"))||N.Contains(TEXT("Birch"))||(!TreesOnly&&(N.Contains(TEXT("Bush"))||N.Contains(TEXT("Grass"))||N.Contains(TEXT("Fern"))||N.Contains(TEXT("Flower"))||N.Contains(TEXT("Herb"))));}
 bool Initialize()
 {
  auto* W=FindWorld();if(!W)return false;World=W;Player=UGameplayStatics::GetPlayerPawn(W,0);if(!Player.IsValid()||!Viewport())return false;
  const int32 Category=FCsvProfiler::GetCategoryIndex(TEXT("VSM"));
  Settings+=FString::Printf(TEXT("csv_VSM_category_enabled=%d\n"),Category>=0&&FCsvProfiler::Get()->IsCategoryEnabled(Category));
  for(TActorIterator<APokeMonsterNPCVisualActor> I(W);I;++I)if(I->SourceActor){Ranger=*I;break;}
  if(!Ranger.IsValid())return false;
  SavedMesh.Reset(Ranger->Visual->GetSkeletalMeshAsset());SavedIdle.Reset(Ranger->IdleAnimation);SavedTalk.Reset(Ranger->ConversationAnimation);SavedMotion=Ranger->bEnableMotionPresentation;SavedAccessories=Ranger->bEnableAccessoryMotion;
  PlayerBefore=Player->GetActorTransform();for(TObjectIterator<UPrimitiveComponent> I;I;++I)if(I->GetWorld()==W&&I->IsRegistered()){FComponentState S{*I,I->IsVisible(),!!I->CastShadow};if(auto* M=Cast<UStaticMeshComponent>(*I)){S.ForcedLOD=M->GetForcedLodModel();S.MinLOD=M->MinLOD;S.OverrideMinLOD=M->bOverrideMinLOD;}if(auto* M=Cast<UInstancedStaticMeshComponent>(*I))M->GetCullDistances(S.CullStart,S.CullEnd);Components.Add(S);}
  for(TActorIterator<APostProcessVolume> I(W);I;++I)PostVolumes.Add({*I,I->Settings});
  Set(TEXT("r.VSync"),TEXT("0"));Set(TEXT("t.MaxFPS"),TEXT("0"));Set(TEXT("r.GPUCsvStatsEnabled"),TEXT("1"));Set(TEXT("r.DynamicRes.OperationMode"),TEXT("0"));Set(TEXT("r.Editor.Viewport.OverridePIEScreenPercentage"),TEXT("0"));Set(TEXT("r.SecondaryScreenPercentage.GameViewport"),TEXT("100"));
  Observer=FSceneViewExtensions::NewExtension<FResolutionObserver>(Resolution,Viewport());
  Frames=TEXT("segment,site,condition,repeat,quality,percentage,utc,frame_ms,viewport_w,viewport_h,target_w,target_h,window_slate_w,window_slate_h,window_dpi,view_w,view_h,internal_w,internal_h,primary_fraction,secondary_fraction,renderer_samples,camera_x,camera_y,camera_z,pitch,yaw,fov,window_active\n");
  Segments=TEXT("segment,site,condition,repeat,start_utc,end_utc,mode,width,height,quality,percentage\n");Initialized=true;BeginRow();return true;
 }
 void BeginRow()
 {
  RestoreFactors();const auto& R=Rows[Index];const bool V2=R.Condition==TEXT("V2");
  for(const TCHAR* N:{TEXT("sg.ViewDistanceQuality"),TEXT("sg.AntiAliasingQuality"),TEXT("sg.ShadowQuality"),TEXT("sg.GlobalIlluminationQuality"),TEXT("sg.ReflectionQuality"),TEXT("sg.PostProcessQuality"),TEXT("sg.TextureQuality"),TEXT("sg.EffectsQuality"),TEXT("sg.FoliageQuality"),TEXT("sg.ShadingQuality")})Set(N,FString::FromInt(R.Quality));
  // Original VisualV2 lighting, identical for both NPC variants. No environment optimization here.
  Set(TEXT("r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor"),TEXT("1"));
  Set(TEXT("r.Shadow.Virtual.SMRT.RayCountDirectional"),TEXT("8"));
  Set(TEXT("r.Lumen.FinalGatherMethod"),TEXT("1"));Set(TEXT("r.Lumen.HardwareRayTracing"),TEXT("1"));
  Set(TEXT("r.ScreenPercentage"),FString::FromInt(R.Percentage));Viewport()->SetFixedViewportSize(R.Width,R.Height);
  if(auto Window=Viewport()->FindWindow();Window.IsValid()){if(World->WorldType==EWorldType::Game)Window->Resize(FVector2D(R.Width,R.Height));Window->BringToFront(true);}
  Player->SetActorLocation(FVector(-760,-1410,50.15),false,nullptr,ETeleportType::TeleportPhysics);
  const TCHAR* MeshPath=V2?TEXT("/Game/Characters/NPCs/RangerMotionV2/Meshes/SK_Ranger_AQV2"):TEXT("/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1");
  auto* M=LoadObject<USkeletalMesh>(nullptr,MeshPath);
  auto* Idle=LoadObject<UAnimSequence>(nullptr,V2?TEXT("/Game/Characters/NPCs/RangerMotionV2/Animations/A_Ranger_Idle_AQV2"):TEXT("/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Idle_V1"));
  auto* Talk=LoadObject<UAnimSequence>(nullptr,V2?TEXT("/Game/Characters/NPCs/RangerMotionV2/Animations/A_Ranger_Talk_AQV2"):TEXT("/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Talk_V1"));
  if(!M||!Idle||!Talk){Stop(TEXT("NPC assets missing"));return;}
  Ranger->Visual->SetSkeletalMeshAsset(M);Ranger->IdleAnimation=Idle;Ranger->ConversationAnimation=Talk;Ranger->bEnableMotionPresentation=false;Ranger->bEnableAccessoryMotion=V2;Ranger->RefreshPresentation();
  Settings+=FString::Printf(TEXT("segment=%d condition=%s mesh=%s idle=%s resolution=%dx%d quality=%d SP=%d shadow_method=%d sync=%d\n"),Index,*R.Condition,*M->GetPathName(),*Idle->GetPathName(),R.Width,R.Height,R.Quality,R.Percentage,IConsoleManager::Get().FindConsoleVariable(TEXT("r.Shadow.Virtual.Enable"))->GetInt(),IConsoleManager::Get().FindConsoleVariable(TEXT("rhi.SyncInterval"))->GetInt());
  Start=Last=FPlatformTime::Seconds();Capturing=false;
 }
 void Save(){FFileHelper::SaveStringToFile(Frames,*(Directory/(Label+TEXT("_Frames.csv"))));FFileHelper::SaveStringToFile(Segments,*(Directory/(Label+TEXT("_Segments.csv"))));FFileHelper::SaveStringToFile(Settings,*(Directory/(Label+TEXT("_Settings.txt"))));}
 void Stop(const FString& Error=TEXT(""))
 {
  if(Capturing&&World.IsValid())GEngine->Exec(World.Get(),TEXT("csvprofile stop"));RestoreFactors();Observer.Reset();
  if(Ranger.IsValid()){Ranger->Visual->SetSkeletalMeshAsset(SavedMesh.Get());Ranger->IdleAnimation=SavedIdle.Get();Ranger->ConversationAnimation=SavedTalk.Get();Ranger->bEnableMotionPresentation=SavedMotion;Ranger->bEnableAccessoryMotion=SavedAccessories;Ranger->RefreshPresentation();}
  // Restore factors before scalability so their lower-priority settings can take effect again.
  for(const auto& P:CVars)if(!P.Key.StartsWith(TEXT("sg.")))RestoreVar(P.Key,P.Value,Priorities[P.Key]);
  for(const auto& P:CVars)if(P.Key.StartsWith(TEXT("sg.")))RestoreVar(P.Key,P.Value,Priorities[P.Key]);
  if(auto* V=Viewport())V->SetFixedViewportSize(0,0);if(Player.IsValid())Player->SetActorTransform(PlayerBefore,false,nullptr,ETeleportType::TeleportPhysics);
  Save();FFileHelper::SaveStringToFile(Error.IsEmpty()?TEXT("Complete"):Error,*(Directory/(Label+TEXT("_Done.txt"))));UE_LOG(LogTemp,Display,TEXT("PM_ENV_PERF3_DONE %s %s"),*Label,*Error);FTSTicker::GetCoreTicker().RemoveTicker(Handle);
  if(Mode==TEXT("Standalone")&&World.IsValid())
  {
   TWeakObjectPtr<UWorld> QuitWorld=World;
   FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([QuitWorld](float){if(QuitWorld.IsValid())GEngine->Exec(QuitWorld.Get(),TEXT("quit"));return false;}),5.f);
  }
 }
 bool Tick(float)
 {
  if(!Initialized){if(!Initialize())return true;}if(!Player.IsValid()||!Viewport()){Stop(TEXT("PIE or viewport lost"));return false;}
  double Now=FPlatformTime::Seconds(),Elapsed=Now-Start,Ms=(Now-Last)*1000;Last=Now;if(Elapsed<Warmup)return true;const auto& R=Rows[Index];
  if(!Capturing){GEngine->Exec(World.Get(),*FString::Printf(TEXT("csvprofile startfile=NPC2_%s_%03d"),*Label,Index));GEngine->Exec(World.Get(),TEXT("csvprofile start"));Capturing=true;Segments+=FString::Printf(TEXT("%d,%s,%s,%d,%s,"),Index,*R.Site,*R.Condition,R.Repeat,*FDateTime::UtcNow().ToIso8601());return true;}
  auto* VP=Viewport();auto Size=VP->GetSizeXY(),Target=VP->GetRenderTargetTextureSizeXY();auto Window=VP->FindWindow();auto WS=Window.IsValid()?Window->GetSizeInScreen():FVector2D::ZeroVector;float DPI=Window.IsValid()?Window->GetDPIScaleFactor():0;
  FIntPoint View,Internal;float Primary,Secondary;uint64 Samples;{FScopeLock L(&Resolution->Lock);View=Resolution->Output;Internal=Resolution->Internal;Primary=Resolution->Primary;Secondary=Resolution->Secondary;Samples=Resolution->Samples;}
  auto* Cam=UGameplayStatics::GetPlayerController(World.Get(),0)->PlayerCameraManager.Get();auto P=Cam->GetCameraLocation();auto Rot=Cam->GetCameraRotation();
  Frames+=FString::Printf(TEXT("%d,%s,%s,%d,%d,%d,%s,%.6f,%d,%d,%d,%d,%.2f,%.2f,%.3f,%d,%d,%d,%d,%.5f,%.5f,%llu,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%d\n"),Index,*R.Site,*R.Condition,R.Repeat,R.Quality,R.Percentage,*FDateTime::UtcNow().ToIso8601(),Ms,Size.X,Size.Y,Target.X,Target.Y,WS.X,WS.Y,DPI,View.X,View.Y,Internal.X,Internal.Y,Primary,Secondary,Samples,P.X,P.Y,P.Z,Rot.Pitch,Rot.Yaw,Cam->GetFOVAngle(),Window.IsValid()&&Window->IsActive());
  if(Elapsed<Warmup+Duration)return true;GEngine->Exec(World.Get(),TEXT("csvprofile stop"));Capturing=false;Segments+=FString::Printf(TEXT("%s,%s,%d,%d,%d,%d\n"),*FDateTime::UtcNow().ToIso8601(),*Mode,Size.X,Size.Y,R.Quality,R.Percentage);Save();
  Settings+=FString::Printf(TEXT("segment=%d final_predicted_lod=%d\n"),Index,Ranger->Visual->GetPredictedLODLevel());if(++Index>=Rows.Num()){Stop();return false;}BeginRow();return true;
 }
};
static TSharedPtr<FProbe> Active;
#if WITH_EDITOR
static FAutoConsoleCommand AuditLODs(TEXT("pm.NPCMotion2.AuditLODs"),TEXT("Read new NPC LOD render data; optional screen-size applies only to Ranger AQV2."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 auto* M=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/NPCs/RangerMotionV2/Meshes/SK_Ranger_AQV2"));if(!M)return;FString Out;
 for(int32 I=0;I<M->GetLODNum();++I)
 {
  auto* L=M->GetLODInfo(I);
  if(Args.Num()==1){L->ScreenSize.Default=I==0?1.f:FMath::Clamp(FCString::Atof(*Args[0]),.05f,.5f);L->LODHysteresis=.01f;M->MarkPackageDirty();}
  const auto& Data=M->GetResourceForRendering()->LODRenderData[I];uint32 Tri=0;for(const auto& S:Data.RenderSections)Tri+=S.NumTriangles;
  Out+=FString::Printf(TEXT("LOD%d triangles=%u renderVertices=%u screenSize=%.6f hysteresis=%.6f bones=%d\n"),I,Tri,Data.GetNumVertices(),L->ScreenSize.Default,L->LODHysteresis,M->GetRefSkeleton().GetNum());
 }
 FFileHelper::SaveStringToFile(Out,*(FPaths::ProjectSavedDir()/TEXT("RangerAnimationV2/NativeLODAudit.txt")));UE_LOG(LogTemp,Display,TEXT("%s"),*Out);
}));
#endif
static FAutoConsoleCommand SetViewport(TEXT("pm.NPCMotion2.Viewport"),TEXT("Explicit review viewport width height; 0 0 restores automatic sizing. Does not move the player."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=2||Active)return;
 const int32 Width=FCString::Atoi(*Args[0]),Height=FCString::Atoi(*Args[1]);
 if(!((Width==0&&Height==0)||(Width>=320&&Height>=240&&Width<=4096&&Height<=4096)))return;
 for(const auto& Context:GEngine->GetWorldContexts())if(auto* W=Context.World())if(Context.WorldType==EWorldType::PIE||Context.WorldType==EWorldType::Game)
  if(auto* GI=W->GetGameInstance())if(auto* Client=GI->GetGameViewportClient())if(auto* VP=Client->GetGameViewport()){VP->SetFixedViewportSize(Width,Height);return;}
}));
static FAutoConsoleCommand Run(TEXT("pm.NPCMotion2.Run"),TEXT("Opt-in scoped environment probe. TSV header label/mode/warmup/duration; rows site/factor/repeat/width/height/quality/percentage."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||Active)return;FString Text;if(!FFileHelper::LoadFileToString(Text,*Args[0]))return;TArray<FString> Lines;Text.ParseIntoArrayLines(Lines);if(Lines.Num()<2)return;TArray<FString> H;Lines[0].ParseIntoArray(H,TEXT("\t"),false);if(H.Num()!=4)return;
 auto P=MakeShared<FProbe>();P->Label=H[0];P->Mode=H[1];P->Warmup=FCString::Atof(*H[2]);P->Duration=FCString::Atof(*H[3]);P->Directory=FPaths::ProjectSavedDir()/TEXT("RangerAnimationV2");IFileManager::Get().MakeDirectory(*P->Directory,true);
 for(int32 I=1;I<Lines.Num();++I){TArray<FString> F;Lines[I].ParseIntoArray(F,TEXT("\t"),false);if(F.Num()==7)P->Rows.Add({F[0],F[1],FCString::Atoi(*F[2]),FCString::Atoi(*F[3]),FCString::Atoi(*F[4]),FCString::Atoi(*F[5]),FCString::Atoi(*F[6])});}
 if(P->Rows.IsEmpty())return;Active=P;P->Handle=FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([](float D){auto P=Active;bool Keep=P->Tick(D);if(!Keep)Active.Reset();return Keep;}));
}));
static FAutoConsoleCommand Stop(TEXT("pm.NPCMotion2.Stop"),TEXT("Stop explicit environment probe and restore all temporary state."),FConsoleCommandDelegate::CreateLambda([](){if(Active){Active->Stop(TEXT("Cancelled"));Active.Reset();}}));
}
#endif
