#include "PokeMonsterHabitatSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Creatures/Overworld/PokeMonsterCreatureCompanionSubsystem.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "../Time/PokeMonsterWorldClock.h"
#include "Components/BoxComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/AssetManager.h"
#include "Engine/GameInstance.h"
#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"
#include "HAL/IConsoleManager.h"
#include "HAL/PlatformTime.h"
#include "TimerManager.h"

APokeMonsterHabitatZone::APokeMonsterHabitatZone()
{
 bAllowNaturalActivities=true;bAllowGroundFlight=true;
 Tags.Add(TEXT("PokemonNaturalHabitat"));
}
float FPokeMonsterHabitatRule::WeightAt(double Second)const
{
 FPokeMonsterCreatureRhythm R;R.Rhythm=Rhythm;
 const float Activity=R.ActivityAt(Second,0,*GetDefault<UPokeMonsterWorldClockSettings>());
 return Weight*FMath::Lerp(.35f,1.f,Activity);
}
bool FPokeMonsterHabitatRule::IsValid()const
{
 return !Species.IsNone()&&!Profile.IsNull()&&!Habitats.IsEmpty()&&FMath::IsFinite(Weight)&&Weight>0&&Maximum>0&&Maximum<=10
  && FMath::IsFinite(MinimumPlayerDistance)&&MinimumPlayerDistance>=600&&FMath::IsFinite(MinimumPeerDistance)&&MinimumPeerDistance>=120;
}
bool UPokeMonsterHabitatSettings::IsValidConfiguration()const
{
 if(MaximumPopulation<1||MaximumPopulation>20||MaximumSpecies<1||MaximumSpecies>MaximumPopulation||!FMath::IsFinite(UpdateSeconds)||UpdateSeconds<1
  ||!FMath::IsFinite(MinimumResidenceSeconds)||MinimumResidenceSeconds<30||!FMath::IsFinite(DespawnDistance)||DespawnDistance<2000)return false;
 TSet<FName> Ids,Species;
 for(const auto& Z:VisualV2Zones)
 {
  if(Z.Id.IsNone()||Ids.Contains(Z.Id)||Z.Type.IsNone()||Z.Center.ContainsNaN()||Z.Extent.ContainsNaN()||Z.Extent.X<200||Z.Extent.Y<200||Z.Extent.Z<100||Z.Maximum<1||Z.Maximum>MaximumPopulation)return false;
  Ids.Add(Z.Id);
 }
 for(const auto& R:Rules){if(!R.IsValid()||Species.Contains(R.Species))return false;Species.Add(R.Species);}
 return !Rules.IsEmpty();
}
bool UPokeMonsterHabitatSubsystem::DoesSupportWorldType(EWorldType::Type T)const{return T==EWorldType::PIE||T==EWorldType::Game;}
bool UPokeMonsterHabitatSubsystem::IsVisualV2(const FString& Name){return UWorld::RemovePIEPrefix(Name)==TEXT("Dev_TestMap_VisualV2");}
FName UPokeMonsterHabitatSubsystem::PopulationId(FName Zone,int32 Slot,FName Species,int32 Day)
{
 return FName(*FString::Printf(TEXT("HabitatV2_%s_%d_%s_D%d"),*Zone.ToString(),Slot,*Species.ToString(),FMath::Max(1,Day)));
}
void UPokeMonsterHabitatSubsystem::OnWorldBeginPlay(UWorld& W)
{
 Super::OnWorldBeginPlay(W);const auto* S=GetDefault<UPokeMonsterHabitatSettings>();
 if(!S->IsValidConfiguration()){UE_LOG(LogTemp,Warning,TEXT("PM_HABITATS invalid configuration; authored encounters retained"));return;}
 if(IsVisualV2(W.GetName())&&S->bEnableVisualV2)
 {
  FActorSpawnParameters P;P.ObjectFlags|=RF_Transient;
  for(const auto& L:S->VisualV2Zones)
  {
   auto* Z=W.SpawnActor<APokeMonsterHabitatZone>(L.Center,FRotator::ZeroRotator,P);if(!Z)continue;
   Z->ZoneId=L.Id;Z->HabitatType=L.Type;Z->HabitatName=L.Id.ToString();Z->MaximumPopulation=L.Maximum;Z->Bounds->SetBoxExtent(L.Extent);
  }
 }
 for(TActorIterator<APokeMonsterHabitatZone> I(&W);I;++I)
  if(!I->ZoneId.IsNone()&&!I->HabitatType.IsNone()&&I->MaximumPopulation>0&&I->MaximumPopulation<=S->MaximumPopulation)Zones.Add(*I);
 if(Zones.IsEmpty())return; // No other map opts in implicitly.
 for(const auto& R:S->Rules)
 {
  // Resolve only curated candidates through the same primary registry. Future production
  // maps need not synchronously load every model in the development exhibition.
  const FPrimaryAssetId Id(TEXT("CreatureSpecies"),R.Species);
  auto* Species=Cast<UPokeMonsterCreatureSpeciesData>(UAssetManager::Get().GetPrimaryAssetPath(Id).TryLoad());
  auto* Presentation=Species?Species->GetVisuals().Presentation.LoadSynchronous():nullptr;
  if(Species&&Species->GetPrimaryAssetId()==Id&&Species->Overworld.IsValid()&&Presentation&&Presentation->GetValidationErrors().IsEmpty())Registered.AddUnique(Species);
  auto* P=R.Profile.LoadSynchronous();bool Exact=P&&!P->Entries.IsEmpty();
  if(P)for(const auto& E:P->Entries){const auto* C=E.Species.LoadSynchronous();Exact&=C&&C->GetInternalId()==R.Species;}
  Profiles.Add(Exact?P:nullptr);
  if(!Exact)UE_LOG(LogTemp,Warning,TEXT("PM_HABITATS rejected mismatched encounter profile for %s"),*R.Species.ToString());
 }
 // Keep authored gallery identities in the map/save data, but not as an all-species wild exhibition.
 if(IsVisualV2(W.GetName()))for(TActorIterator<APokeMonsterVisibleWildCreatureActor> I(&W);I;++I)I->SuspendForHabitatPopulation();
 bEnabled=true;W.GetTimerManager().SetTimer(UpdateTimer,this,&UPokeMonsterHabitatSubsystem::RefreshPopulation,S->UpdateSeconds,true,3.f);
 UE_LOG(LogTemp,Display,TEXT("PM_HABITATS %d zones, %d registered models, population cap %d"),Zones.Num(),Registered.Num(),S->MaximumPopulation);
}
bool UPokeMonsterHabitatSubsystem::CandidateOutsideView(const FVector& Foot,const FVector& Extent)const
{
 auto* PC=UGameplayStatics::GetPlayerController(this,0);if(!PC||!PC->PlayerCameraManager)return false;
 int32 X=0,Y=0;PC->GetViewportSize(X,Y);if(X<=0||Y<=0)return false;
 FVector2D Min(DBL_MAX,DBL_MAX),Max(-DBL_MAX,-DBL_MAX);bool AnyFront=false;
 for(int32 I=0;I<8;++I)
 {
  const FVector P=Foot+FVector((I&1)?Extent.X:-Extent.X,(I&2)?Extent.Y:-Extent.Y,(I&4)?Extent.Z*2:0);
  FVector2D Screen;if(PC->ProjectWorldLocationToScreen(P,Screen))
  {AnyFront=true;Min.X=FMath::Min(Min.X,Screen.X);Min.Y=FMath::Min(Min.Y,Screen.Y);Max.X=FMath::Max(Max.X,Screen.X);Max.Y=FMath::Max(Max.Y,Screen.Y);}
 }
 return !AnyFront||Max.X < -160||Max.Y < -160||Min.X>X+160||Min.Y>Y+160;
}
void UPokeMonsterHabitatSubsystem::Retire(APokeMonsterVisibleWildCreatureActor* A)
{
 if(!A)return;A->OverworldMovement->SetMovementPaused(true);BirthTimes.Remove(A);Population.Remove(A);A->Destroy();++Retired;
}
void UPokeMonsterHabitatSubsystem::SetPopulationEnabled(bool Enabled)
{
 if(Zones.IsEmpty())return;
 const auto* GI=GetWorld()->GetGameInstance();
 const auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 if(E&&E->IsEncounterActive())return;
 bEnabled=Enabled;
 if(!Enabled){const auto Copy=Population;for(auto A:Copy)Retire(A);}
}
void UPokeMonsterHabitatSubsystem::RefreshPopulation()
{
 const double Start=FPlatformTime::Seconds();++Updates;
 auto* GI=GetWorld()->GetGameInstance();auto* C=GI?GI->GetSubsystem<UPokeMonsterWorldClock>():nullptr;
 auto* E=GI?GI->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;
 auto* P=Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this,0));
 if(!bEnabled||!C||!E||!P||C->IsClockPaused()||E->IsEncounterActive()||P->IsOverworldInputLocked())return;
 const auto* S=GetDefault<UPokeMonsterHabitatSettings>();const double Now=GetWorld()->GetTimeSeconds();
 const auto Copy=Population;
 for(auto A:Copy)
 {
  if(!IsValid(A)){Population.Remove(A);BirthTimes.Remove(A);continue;}
  const float Distance=FVector::Dist2D(P->GetActorLocation(),A->GetActorLocation());
  const bool Far=Distance>3500;
  A->OverworldMovement->SetComponentTickInterval(Far?.5f:0.f);A->SetActorTickInterval(Far?.5f:0.f);
  if((A->LifeState==EPokeMonsterWildLifeState::Removed||(Distance>S->DespawnDistance&&Now-BirthTimes.FindRef(A)>S->MinimumResidenceSeconds))&&A->IsOutsidePlayerView())Retire(A);
 }
 if(Population.Num()<S->MaximumPopulation)
 {
  // One source per update bounds spawn/loading work; random zone order avoids a persistent first-zone bias.
  const int32 First=Random.RandRange(0,Zones.Num()-1);
  for(int32 I=0;I<Zones.Num();++I)if(TryPopulate(Zones[(First+I)%Zones.Num()]))break;
 }
 LastUpdateMicroseconds=(FPlatformTime::Seconds()-Start)*1e6;
}
bool UPokeMonsterHabitatSubsystem::TryPopulate(APokeMonsterHabitatZone* Z)
{
 if(!IsValid(Z))return false;
 const auto* S=GetDefault<UPokeMonsterHabitatSettings>();auto* GI=GetWorld()->GetGameInstance();
 auto* C=GI->GetSubsystem<UPokeMonsterWorldClock>();auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>();
 auto* P=UGameplayStatics::GetPlayerPawn(this,0);if(!P)return false;
 // Do not populate distant unexplored map sections until useful, or relocated interiors/model review.
 const FVector Center=Z->GetActorLocation();if(FVector::Dist2D(P->GetActorLocation(),Center)>5000)return false;
 TSet<int32> Occupied;TMap<FName,int32> Counts;
 for(auto A:Population)if(IsValid(A))
 {
  if(auto* Species=A->VisualSpecies.Get())++Counts.FindOrAdd(Species->GetInternalId());
  if(A->OverworldMovement->BiomeHabitat==Z)
   for(int32 Slot=0;Slot<Z->MaximumPopulation;++Slot)
    if(A->Tags.Contains(FName(*FString::Printf(TEXT("HabitatSlot%d"),Slot))))Occupied.Add(Slot);
 }
 if(Occupied.Num()>=Z->MaximumPopulation)return false;
 int32 Slot=0;while(Occupied.Contains(Slot))++Slot;
 TArray<int32> Eligible;float Total=0;
 for(int32 I=0;I<S->Rules.Num();++I)
 {
  const auto& R=S->Rules[I];if(!Profiles.IsValidIndex(I)||!Profiles[I]||!R.Allows(Z->HabitatType)||Counts.FindRef(R.Species)>=R.Maximum)continue;
  if(!Counts.Contains(R.Species)&&Counts.Num()>=S->MaximumSpecies)continue;
  if(E->IsEncounterCompleted(PopulationId(Z->ZoneId,Slot,R.Species,C->GetDay())))continue;
  Eligible.Add(I);Total+=R.WeightAt(C->GetTime().SecondsOfDay);
 }
 if(Eligible.IsEmpty())return false;
 float Pick=Random.FRand()*Total;int32 Index=Eligible.Last();
 for(int32 I:Eligible){Pick-=S->Rules[I].WeightAt(C->GetTime().SecondsOfDay);if(Pick<=0){Index=I;break;}}
 const auto& R=S->Rules[Index];UPokeMonsterCreatureSpeciesData* Species=nullptr;
 for(auto A:Registered)if(A->GetInternalId()==R.Species){Species=A;break;}
 if(!Species)return false;
 const auto* Visual=Species->GetVisuals().Presentation.LoadSynchronous();if(!Visual||!Visual->Mesh)return false;
 const FVector Extent=Visual->Mesh->GetBounds().BoxExtent;const float Radius=FMath::Max(38.f,Species->Overworld.BodyRadius);
 FCollisionQueryParams Q(SCENE_QUERY_STAT(NaturalHabitatSpawn),false);Q.AddIgnoredActor(P);
 for(int32 Attempt=0;Attempt<12;++Attempt)
 {
  const FVector B=Z->Bounds->GetScaledBoxExtent();const FVector Point=Center+FVector(Random.FRandRange(-B.X+Radius,B.X-Radius),Random.FRandRange(-B.Y+Radius,B.Y-Radius),0);
  FVector Foot;if(!Z->ProjectFoot(Point,Radius,60,Q,Foot)||FVector::Dist2D(P->GetActorLocation(),Foot)<R.MinimumPlayerDistance||!CandidateOutsideView(Foot,Extent)){++RejectedPositions;continue;}
  bool Clear=true;
  const auto* Companion=GetWorld()->GetSubsystem<UPokeMonsterCreatureCompanionSubsystem>();
  const auto* Buddy=Companion?Companion->GetVisual():nullptr;
  if(Buddy&&!Buddy->IsHidden()&&FVector::Dist2D(Buddy->GetActorLocation(),Foot)<R.MinimumPeerDistance)Clear=false;
  for(auto A:Population)if(IsValid(A)&&FVector::Dist2D(A->GetActorLocation(),Foot)<R.MinimumPeerDistance){Clear=false;break;}
  for(TActorIterator<APokeMonsterBuildingCutaway> I(GetWorld());I;++I)if(I->IsViewerInside(Foot+FVector(0,0,60))){Clear=false;break;}
  if(!Clear){++RejectedPositions;continue;}
  const FTransform Transform(FRotator(0,Random.FRandRange(-180,180),0),Foot+FVector(0,0,60));
  auto* A=GetWorld()->SpawnActorDeferred<APokeMonsterVisibleWildCreatureActor>(APokeMonsterVisibleWildCreatureActor::StaticClass(),Transform,nullptr,nullptr,ESpawnActorCollisionHandlingMethod::AlwaysSpawn);
  if(!A)return false;
  A->SetFlags(RF_Transient);A->Tags.Add(TEXT("PokemonHabitatPopulation"));A->Tags.Add(FName(*FString::Printf(TEXT("HabitatSlot%d"),Slot)));
  A->VisualSpecies=Species;A->Profile=Profiles[Index];A->EncounterId=PopulationId(Z->ZoneId,Slot,R.Species,C->GetDay());A->Seed=Random.RandRange(1,MAX_int32-1);A->bAmbientMotion=true;
  A->Context.RegionId=NAME_None;A->Context.Time=EPokeMonsterEncounterTime::Any;
  auto* M=A->OverworldMovement.Get();M->BiomeHabitat=Z;M->HabitatRadiusOverride=FMath::Clamp(B.Size2D()*2.f,300.f,5000.f);
  if(!FPokeMonsterCreatureActivityProfile::ForSpecies(R.Species).bEnabled)
  {
   M->bOverrideActivities=true;M->ActivityOverride.bEnabled=true;M->ActivityOverride.bPreferVegetation=Z->HabitatType!=TEXT("Rock");
  }
  FPokeMonsterCreatureRhythm Existing;
  if(!GetDefault<UPokeMonsterCreatureRhythmSettings>()->Find(R.Species,Existing)){M->bOverrideRhythm=true;M->RhythmOverride.Rhythm=R.Rhythm;}
  UGameplayStatics::FinishSpawningActor(A,Transform);
  // Reuse the shared planner's cached art-prop/building exclusions before admitting the source.
  FVector Verified;if(!M->ProjectWalkable(Foot,Verified)||!M->CanTraverse(Foot,Foot)){A->Destroy();++RejectedPositions;continue;}
  Population.Add(A);BirthTimes.Add(A,GetWorld()->GetTimeSeconds());++Spawned;return true;
 }
 return false;
}
void UPokeMonsterHabitatSubsystem::Deinitialize()
{
 if(GetWorld())GetWorld()->GetTimerManager().ClearTimer(UpdateTimer);
 for(auto A:Population)if(IsValid(A))A->OverworldMovement->SetMovementPaused(true);
 Population.Reset();Zones.Reset();Registered.Reset();Profiles.Reset();BirthTimes.Reset();Super::Deinitialize();
}
#if !UE_BUILD_SHIPPING
namespace
{
FAutoConsoleCommandWithWorldAndArgs HabitatCommand(TEXT("pm.Habitats"),TEXT("status | 0 | 1: natural population diagnostics; authored gallery remains dormant."),
 FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args,UWorld* W)
 {
  if(!W)return;auto* H=W->GetSubsystem<UPokeMonsterHabitatSubsystem>();if(!H)return;
  if(Args.Num()&&Args[0]==TEXT("0"))H->SetPopulationEnabled(false);else if(Args.Num()&&Args[0]==TEXT("1"))H->SetPopulationEnabled(true);
  UE_LOG(LogTemp,Display,TEXT("PM_HABITATS enabled=%d zones=%d active=%d spawned=%d retired=%d rejected=%d update_us=%.0f"),H->IsPopulationEnabled(),H->Zones.Num(),H->Population.Num(),H->Spawned,H->Retired,H->RejectedPositions,H->LastUpdateMicroseconds);
 }));
}
#endif
