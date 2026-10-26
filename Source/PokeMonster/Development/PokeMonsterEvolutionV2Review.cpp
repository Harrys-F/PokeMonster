// Explicit unsaved PIE fixtures only; never a runtime species/level editor.
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "HAL/IConsoleManager.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureProgression.h"
#if WITH_EDITOR
namespace
{
 UPokeMonsterEncounterSubsystem* ReviewParty(){for(const auto& C:GEngine->GetWorldContexts())if(C.WorldType==EWorldType::PIE&&C.World()&&C.World()->GetGameInstance())return C.World()->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();return nullptr;}
 FAutoConsoleCommand Party(TEXT("pm.EvolutionReview.Party"),TEXT("Explicit PIE fixture: Zunderlauf|Glutexo level; independent Glurak reserve, spent PP and 5 missing HP."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& A)
 {
  if(A.Num()!=2||!A[1].IsNumeric()||(A[0]!=TEXT("Zunderlauf")&&A[0]!=TEXT("Glutexo")))return;auto* E=ReviewParty();if(!E||E->IsEncounterActive())return;
  auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*(TEXT("/Game/Data/Creatures/DA_")+A[0]+TEXT(".DA_")+A[0]));
  auto* R=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Glurak.DA_Glurak"));if(!S||!R)return;
  auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(S,FCString::Atoi(*A[1]));C.AssignSpeciesMoves();C.ConsumeMovePP(0,3);C.CurrentHP=FMath::Max(1,C.GetMaxHP()-5);
  auto Reserve=FPokeMonsterCreatureInstance::CreateFromSpecies(R,36);Reserve.AssignSpeciesMoves();E->RestorePersistentState({C,Reserve},E->GetDefeatedTrainerIds(),E->GetCompletedEncounterIds());
 }));
 FAutoConsoleCommand XP(TEXT("pm.EvolutionReview.XP"),TEXT("Explicit PIE-only XP award: next or nonnegative amount, through existing progression."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& A)
 {
  auto* E=ReviewParty();if(A.Num()!=1||!E||E->IsEncounterActive()||E->GetPlayerParty().IsEmpty())return;auto Team=E->GetPlayerParty();const int64 Amount=A[0]==TEXT("next")?Team[0].GetExperienceToNextLevel():A[0].IsNumeric()?FCString::Atoi64(*A[0]):-1;
  if(Team[0].AddExperience(Amount).bSucceeded)E->RestorePersistentState(Team,E->GetDefeatedTrainerIds(),E->GetCompletedEncounterIds());
 }));
}
#endif
#if WITH_EDITOR
#include "../UI/PokeMonsterEvolutionWidget.h"
#include "../UI/PokeMonsterOverworldPlayerController.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "Slate/WidgetRenderer.h"
#include "Engine/TextureRenderTarget2D.h"
#include "RenderingThread.h"
#include "ImageUtils.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/FileManager.h"
namespace
{
 FAutoConsoleCommand Capture(TEXT("pm.EvolutionReview.Capture"),TEXT("QHD live UMG render at 2560x1440; separately identified from the actual Slate viewport size."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& A)
 {
  if(A.Num()!=1||A[0].IsEmpty())return;for(TCHAR C:A[0])if(!FChar::IsAlnum(C)&&C!=TEXT('_'))return;
  for(const auto& C:GEngine->GetWorldContexts())if(C.WorldType==EWorldType::PIE&&C.World())
  {
   auto* PC=Cast<APokeMonsterOverworldPlayerController>(C.World()->GetFirstPlayerController());auto* UI=PC?PC->GetEvolutionWidget():nullptr;if(!UI)return;
   const FString Dir=FPaths::ProjectSavedDir()/TEXT("GlutexoEvolutionV2/QHDCaptures");IFileManager::Get().MakeDirectory(*Dir,true);const FString Path=Dir/(A[0]+TEXT(".png"));if(IFileManager::Get().FileExists(*Path))return;
   auto* Renderer=new FWidgetRenderer(true);auto* Target=FWidgetRenderer::CreateTargetFor(FVector2D(2560,1440),TF_Bilinear,false);
   Renderer->DrawWidget(Target,UI->TakeWidget(),FVector2D(2560,1440),0.f);FlushRenderingCommands();TArray<FColor> Pixels;
   if(Target->GameThread_GetRenderTargetResource()->ReadPixels(Pixels,FReadSurfaceDataFlags(RCM_UNorm))){TArray64<uint8> PNG;FImageUtils::PNGCompressImageArray(2560,1440,Pixels,PNG);FFileHelper::SaveArrayToFile(PNG,*Path);}
   BeginCleanup(Renderer);return;
  }
 }));
 FAutoConsoleCommand Victory(TEXT("pm.EvolutionReview.Victory"),TEXT("Explicit PIE battle fixture, Glumanda level15 one XP short, one-HP Glutexo opponent. Normal battle/XP processing."),FConsoleCommandWithArgsDelegate::CreateLambda([](const TArray<FString>& Args)
 {
  auto* E=ReviewParty();if(!E||E->IsEncounterActive())return;UPokeMonsterCreatureSpeciesData* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));auto* O=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Glutexo.DA_Glutexo"));if(!S||!O)return;
  auto Player=FPokeMonsterCreatureInstance::CreateFromSpecies(S,15);Player.AssignSpeciesMoves();Player.Experience=UPokeMonsterCreatureProgression::ExperienceForLevel(Player.GetExperienceGrowthRate(),16)-1;
  auto Enemy=FPokeMonsterCreatureInstance::CreateFromSpecies(O,1);Enemy.AssignSpeciesMoves();Enemy.CurrentHP=1;
  for(const auto& C:GEngine->GetWorldContexts())if(C.WorldType==EWorldType::PIE&&C.World())if(auto* PC=C.World()->GetFirstPlayerController())
  {FPokeMonsterEncounterStartData Data;Data.Kind=EPokeMonsterEncounterKind::Wild;Data.Source=EPokeMonsterEncounterSource::Scripted;Data.EncounterId=TEXT("ExplicitEvolutionVictoryReview");Data.PlayerTeam=Args.Num()>=1&&Args[0]==TEXT("current")?E->GetPlayerParty():TArray<FPokeMonsterCreatureInstance>{Player};Data.OpponentTeam={Enemy};Data.PresentationMode=Args.Num()==2&&Args[1]==TEXT("world")?EPokeMonsterBattlePresentationMode::WorldBattle:EPokeMonsterBattlePresentationMode::ClassicBattle;Data.RandomSeed=71;Data.bAllowFlee=true;E->StartEncounter(Data,Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()));return;}
 }));
}
#endif
