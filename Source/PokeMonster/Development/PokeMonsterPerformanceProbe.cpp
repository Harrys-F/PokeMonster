// Explicit development-only measurement tool. No autonomous gameplay behavior.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Engine/GameInstance.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/SkeletalMeshLODSettings.h"
#include "Rendering/SkeletalMeshRenderData.h"
#include "Rendering/SkeletalMeshModel.h"
#include "Materials/MaterialInterface.h"
#include "UObject/StrongObjectPtr.h"
#include "HAL/FileManager.h"
#include "Slate/SceneViewport.h"
#include "HAL/IConsoleManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Containers/Ticker.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Pawn.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Camera/PlayerCameraManager.h"
#include "../Characters/PokeMonsterNPCVisualActor.h"
#if !UE_BUILD_SHIPPING
namespace PMPerf
{
struct FComponentState { TWeakObjectPtr<UPrimitiveComponent> C; bool Visible; bool Shadow; TArray<UMaterialInterface*> Materials; };
struct FRow { FString Site, Condition; int32 Repeat=0; };
struct FProbe : public TSharedFromThis<FProbe>
{
 TWeakObjectPtr<UWorld> World; TWeakObjectPtr<APawn> Player; TWeakObjectPtr<APokeMonsterNPCVisualActor> Ranger;
 TArray<FComponentState> Components; TArray<TPair<TWeakObjectPtr<ULightComponent>,bool>> Lights;
 TMap<FString,FString> CVars; TArray<FRow> Rows; int32 Index=0,Width=0,Height=0; float Warmup=10,Duration=15;
 FString Label,Directory,Mode,FrameOutput,IndexOutput; double Start=0,Last=0; bool Capturing=false,Initialized=false;
 FTransform PlayerBefore; TStrongObjectPtr<USkeletalMesh> MeshBefore; bool PauseBefore=false; int32 LODBefore=0;
 FTSTicker::FDelegateHandle Handle;
 UWorld* FindWorld() { for(const FWorldContext& C:GEngine->GetWorldContexts()) if(C.World()&&(C.WorldType==EWorldType::PIE||C.WorldType==EWorldType::Game)) return C.World(); return nullptr; }
 FSceneViewport* Viewport() { auto* W=World.Get(); auto* V=W&&W->GetGameInstance()?W->GetGameInstance()->GetGameViewportClient():nullptr; return V?V->GetGameViewport():nullptr; }
 void SetCVar(const FString& Name,const FString& Value) { if(auto* V=IConsoleManager::Get().FindConsoleVariable(*Name)) { if(!CVars.Contains(Name))CVars.Add(Name,V->GetString()); V->Set(*Value,ECVF_SetByConsole); } }
 void RestoreFactors()
 {
  for(auto& S:Components)if(auto* C=S.C.Get()){C->SetVisibility(S.Visible);C->SetCastShadow(S.Shadow);for(int32 I=0;I<S.Materials.Num();++I)C->SetMaterial(I,S.Materials[I]);}
  for(auto& S:Lights)if(auto* C=S.Key.Get())C->SetVisibility(S.Value);
  if(auto* R=Ranger.Get()){R->Visual->SetSkeletalMeshAsset(MeshBefore.Get());R->Visual->bPauseAnims=PauseBefore;R->Visual->SetForcedLOD(LODBefore);}
  for(const TCHAR* N:{TEXT("ShowFlag.DynamicShadows"),TEXT("ShowFlag.PostProcessing")})if(CVars.Contains(N))if(auto* V=IConsoleManager::Get().FindConsoleVariable(N))V->Set(*CVars[N],ECVF_SetByConsole);
 }
 bool Initialize()
 {
  auto* W=FindWorld(); if(!W)return false; World=W;Player=UGameplayStatics::GetPlayerPawn(W,0);if(!Player.IsValid()||!Viewport())return false;
  for(TActorIterator<APokeMonsterNPCVisualActor> It(W);It;++It)if(It->SourceActor){Ranger=*It;break;}
  if(!Ranger.IsValid())return false;
  PlayerBefore=Player->GetActorTransform();MeshBefore.Reset(Ranger->Visual->GetSkeletalMeshAsset());PauseBefore=Ranger->Visual->bPauseAnims;LODBefore=Ranger->Visual->GetForcedLOD();
  for(TObjectIterator<UPrimitiveComponent> It;It;++It)if(It->GetWorld()==W&&It->IsRegistered())
  { FComponentState S;S.C=*It;S.Visible=It->IsVisible();S.Shadow=It->CastShadow;for(int32 I=0;I<It->GetNumMaterials();++I)S.Materials.Add(It->GetMaterial(I));Components.Add(MoveTemp(S)); }
  for(TObjectIterator<UPointLightComponent> It;It;++It)if(It->GetWorld()==W)Lights.Emplace(*It,It->IsVisible());
  for(const TCHAR* N:{TEXT("sg.ViewDistanceQuality"),TEXT("sg.AntiAliasingQuality"),TEXT("sg.ShadowQuality"),TEXT("sg.GlobalIlluminationQuality"),TEXT("sg.ReflectionQuality"),TEXT("sg.PostProcessQuality"),TEXT("sg.TextureQuality"),TEXT("sg.EffectsQuality"),TEXT("sg.FoliageQuality"),TEXT("sg.ShadingQuality")})SetCVar(N,TEXT("1"));
  SetCVar(TEXT("r.ScreenPercentage"),TEXT("75"));SetCVar(TEXT("r.VSync"),TEXT("0"));SetCVar(TEXT("t.MaxFPS"),TEXT("0"));SetCVar(TEXT("r.GPUCsvStatsEnabled"),TEXT("1"));SetCVar(TEXT("r.DynamicRes.OperationMode"),TEXT("0"));
  if(Width>0&&Height>0)Viewport()->SetFixedViewportSize(Width,Height);
  FrameOutput=TEXT("segment,site,condition,repeat,utc,frame_ms,viewport_w,viewport_h,target_w,target_h,screen_percentage,predicted_lod,camera_x,camera_y,camera_z,pitch,yaw,fov\n");
  IndexOutput=TEXT("segment,site,condition,repeat,start_utc,end_utc,mode,width,height\n");Initialized=true;BeginRow();return true;
 }
 bool IsVegetation(UPrimitiveComponent* C)
 { auto* S=Cast<UStaticMeshComponent>(C);if(!S||!S->GetStaticMesh())return false; const FString N=S->GetStaticMesh()->GetName();return N.StartsWith(TEXT("SM_WLA_"))&&!N.Contains(TEXT("Ruins"))&&!N.Contains(TEXT("Rune"))&&!N.Contains(TEXT("Column"))&&(N.Contains(TEXT("Oak"))||N.Contains(TEXT("Birch"))||N.Contains(TEXT("Bush"))||N.Contains(TEXT("Grass"))||N.Contains(TEXT("Fern"))||N.Contains(TEXT("Flower"))||N.Contains(TEXT("Herb"))); }
 void BeginRow()
 {
  RestoreFactors();const FRow& Row=Rows[Index];const FString& C=Row.Condition;
  FVector P=Row.Site==TEXT("DorfBauten")?FVector(-4100,450,50.15):Row.Site==TEXT("Dorf")?FVector(-760,-1410,50.15):Row.Site==TEXT("Wald")?FVector(-746.5,-718,50.15):FVector(-36.6,-47.1,50.15);
  Player->SetActorLocation(P,false,nullptr,ETeleportType::TeleportPhysics);
  auto* V=Ranger->Visual.Get();
  if(C.StartsWith(TEXT("V2"))){auto* M=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean.SK_Ranger_NPC_V2_Clean"));if(!M){Stop(TEXT("V2 asset missing"));return;}V->SetSkeletalMeshAsset(M);if(C.EndsWith(TEXT("LOD0")))V->SetForcedLOD(1);if(C.EndsWith(TEXT("LOD1")))V->SetForcedLOD(2);if(C.EndsWith(TEXT("LOD2")))V->SetForcedLOD(3);}
  if(C==TEXT("RangerHidden"))V->SetVisibility(false);
  if(C==TEXT("RangerNoShadow"))V->SetCastShadow(false);
  if(C==TEXT("RangerNoAnimation"))V->bPauseAnims=true;
  if(C==TEXT("RangerFlatMaterial")){if(auto* M=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Characters/NPCs/RangerV2/Materials/M_Ranger_FlatDiagnostic.M_Ranger_FlatDiagnostic")))V->SetMaterial(0,M);}
  for(auto& S:Components)if(auto* PComp=S.C.Get())if(IsVegetation(PComp))
  { if(C==TEXT("VegetationHidden"))PComp->SetVisibility(false);if(C==TEXT("VegetationNoShadow"))PComp->SetCastShadow(false); }
  if(C==TEXT("LocalLightsOff"))for(auto& S:Lights)if(auto* L=S.Key.Get())L->SetVisibility(false);
  if(C==TEXT("AllDynamicShadowsOff"))SetCVar(TEXT("ShowFlag.DynamicShadows"),TEXT("0"));
  if(C==TEXT("PostProcessingOff"))SetCVar(TEXT("ShowFlag.PostProcessing"),TEXT("0"));
  Start=Last=FPlatformTime::Seconds();Capturing=false;
 }
 void Stop(const FString& Error=TEXT(""))
 {
  if(Capturing&&World.IsValid())GEngine->Exec(World.Get(),TEXT("csvprofile stop"));
  RestoreFactors();for(auto& Pair:CVars)if(auto* V=IConsoleManager::Get().FindConsoleVariable(*Pair.Key))V->Set(*Pair.Value,ECVF_SetByConsole);
  if(auto* V=Viewport())V->SetFixedViewportSize(0,0);if(Player.IsValid())Player->SetActorTransform(PlayerBefore,false,nullptr,ETeleportType::TeleportPhysics);
  FFileHelper::SaveStringToFile(FrameOutput,*(Directory/ (Label+TEXT("_Frames.csv"))));FFileHelper::SaveStringToFile(IndexOutput,*(Directory/(Label+TEXT("_Segments.csv"))));FFileHelper::SaveStringToFile(Error.IsEmpty()?TEXT("Complete"):Error,*(Directory/(Label+TEXT("_Done.txt"))));
  UE_LOG(LogTemp,Display,TEXT("PM_PERF_DONE %s %s"),*Label,*Error);FTSTicker::GetCoreTicker().RemoveTicker(Handle);if(Mode==TEXT("Standalone")&&World.IsValid())GEngine->Exec(World.Get(),TEXT("quit"));
 }
 bool Tick(float)
 {
  if(!Initialized){if(!Initialize())return true;}
  if(!Player.IsValid()||!Ranger.IsValid()){Stop(TEXT("World or presentation unavailable"));return false;}
  const double Now=FPlatformTime::Seconds(),Elapsed=Now-Start,Ms=(Now-Last)*1000;Last=Now;
  if(Elapsed<Warmup)return true;
  const FRow& Row=Rows[Index];
  if(!Capturing){GEngine->Exec(World.Get(),*FString::Printf(TEXT("csvprofile startfile=RV2_%s_%03d"),*Label,Index));GEngine->Exec(World.Get(),TEXT("csvprofile start"));Capturing=true;IndexOutput+=FString::Printf(TEXT("%d,%s,%s,%d,%s,"),Index,*Row.Site,*Row.Condition,Row.Repeat,*FDateTime::UtcNow().ToIso8601());return true;}
  auto* VP=Viewport();if(!VP){Stop(TEXT("Viewport lost"));return false;}const auto Size=VP->GetSizeXY(),RT=VP->GetRenderTargetTextureSizeXY();auto* PC=UGameplayStatics::GetPlayerController(World.Get(),0);auto* Cam=PC->PlayerCameraManager.Get();const auto CP=Cam->GetCameraLocation();const auto CR=Cam->GetCameraRotation();
  FrameOutput+=FString::Printf(TEXT("%d,%s,%s,%d,%s,%.6f,%d,%d,%d,%d,%.2f,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"),Index,*Row.Site,*Row.Condition,Row.Repeat,*FDateTime::UtcNow().ToIso8601(),Ms,Size.X,Size.Y,RT.X,RT.Y,IConsoleManager::Get().FindConsoleVariable(TEXT("r.ScreenPercentage"))->GetFloat(),Ranger->Visual->GetPredictedLODLevel(),CP.X,CP.Y,CP.Z,CR.Pitch,CR.Yaw,Cam->GetFOVAngle());
  if(Elapsed<Warmup+Duration)return true;
  GEngine->Exec(World.Get(),TEXT("csvprofile stop"));Capturing=false;IndexOutput+=FString::Printf(TEXT("%s,%s,%d,%d\n"),*FDateTime::UtcNow().ToIso8601(),*Mode,Size.X,Size.Y);
  FFileHelper::SaveStringToFile(FrameOutput,*(Directory/(Label+TEXT("_Frames.csv"))));FFileHelper::SaveStringToFile(IndexOutput,*(Directory/(Label+TEXT("_Segments.csv"))));
  if(++Index>=Rows.Num()){Stop();return false;}Initialized=true;BeginRow();return true;
 }
};
static TSharedPtr<FProbe> Active;
static FAutoConsoleCommand Run(TEXT("pm.Perf.Run"),TEXT("Explicit probe: absolute TSV plan path. Restores all factors and CVars."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 if(Args.Num()!=1||Active.IsValid())return;
 FString Text;if(!FFileHelper::LoadFileToString(Text,*Args[0]))return;TArray<FString> Lines;Text.ParseIntoArrayLines(Lines);if(Lines.Num()<2)return;TArray<FString> H;Lines[0].ParseIntoArray(H,TEXT("\t"),false);if(H.Num()!=6)return;
 Active=MakeShared<FProbe>();Active->Label=H[0];Active->Mode=H[1];Active->Width=FCString::Atoi(*H[2]);Active->Height=FCString::Atoi(*H[3]);Active->Warmup=FCString::Atof(*H[4]);Active->Duration=FCString::Atof(*H[5]);Active->Directory=FPaths::ProjectSavedDir()/TEXT("PerformanceRangerV2");IFileManager::Get().MakeDirectory(*Active->Directory,true);
 for(int32 I=1;I<Lines.Num();++I){TArray<FString> P;Lines[I].ParseIntoArray(P,TEXT("\t"));if(P.Num()==3)Active->Rows.Add({P[0],P[1],FCString::Atoi(*P[2])});}if(Active->Rows.IsEmpty())return;
 Active->Handle=FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([](float Dt){auto Probe=Active;bool Keep=Probe->Tick(Dt);if(!Keep)Active.Reset();return Keep;}));
}));
#if WITH_EDITOR
static FAutoConsoleCommand Audit(TEXT("pm.Perf.AuditLODs"),TEXT("Read V1/V2 source/render LODs; optional FixV2 applies only new V2 LOD settings."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
{
 FString Out;
 for(const TCHAR* Path:{TEXT("/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1.SK_Ranger_NPC_V1"),TEXT("/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2.SK_Ranger_NPC_V2"),TEXT("/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean.SK_Ranger_NPC_V2_Clean")})
 {
  auto* M=LoadObject<USkeletalMesh>(nullptr,Path);if(!M)continue;
  if(Args.Contains(TEXT("FixV2"))&&M->GetName()==TEXT("SK_Ranger_NPC_V2"))
  {
   M->GetLODSettings()->SetLODSettingsToMesh(M);
   for(int32 I=0;I<M->GetLODNum();++I){auto* L=M->GetLODInfo(I);L->ReductionSettings.NumOfTrianglesPercentage=1.f;L->ReductionSettings.NumOfVertPercentage=1.f;L->ReductionSettings.BaseLOD=I;L->ReductionSettings.bRecalcNormals=false;}
   M->InvalidateDeriveDataCacheGUID();M->Build();M->MarkPackageDirty();
  }
  if(Args.Contains(TEXT("ConfigureClean"))&&M->GetName()==TEXT("SK_Ranger_NPC_V2_Clean"))
  {for(int32 I=0;I<M->GetLODNum();++I){auto* L=M->GetLODInfo(I);L->ScreenSize.Default=I==0?1.f:.12f;L->LODHysteresis=.015f;}M->MarkPackageDirty();}
  Out+=M->GetPathName()+TEXT("\n");
  for(int32 I=0;I<M->GetLODNum();++I)
  {
   const auto* L=M->GetLODInfo(I);const auto& Render=M->GetResourceForRendering()->LODRenderData[I];uint32 Tri=0;for(const auto& S:Render.RenderSections)Tri+=S.NumTriangles;
   FResourceSizeEx Resource(EResourceSizeMode::Exclusive);Render.GetResourceSizeEx(Resource);
   Out+=FString::Printf(TEXT("LOD%d renderTriangles=%u renderVertices=%u screenSize=%.5f reduction=%.3f base=%d approxResourceBytes=%llu\n"),I,Tri,Render.GetNumVertices(),L->ScreenSize.Default,L->ReductionSettings.NumOfTrianglesPercentage,L->ReductionSettings.BaseLOD,(uint64)Resource.GetTotalMemoryBytes());
  }
 }
 FFileHelper::SaveStringToFile(Out,*(FPaths::ProjectSavedDir()/TEXT("PerformanceRangerV2/NativeLODAudit.txt")));UE_LOG(LogTemp,Display,TEXT("%s"),*Out);
}));
#endif
static FAutoConsoleCommand Cancel(TEXT("pm.Perf.Stop"),TEXT("Restore and stop explicit probe."),FConsoleCommandDelegate::CreateLambda([](){if(Active){Active->Stop(TEXT("Cancelled"));Active.Reset();}}));
}
#endif
