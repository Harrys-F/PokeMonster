#include "PokeMonsterWildEncounterZone.h"
#include "PokeMonsterEncounterSubsystem.h"
#include "../Habitats/PokeMonsterHabitatSubsystem.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Dialogue/PokeMonsterDialogueSubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Time/PokeMonsterWorldClock.h"
#include "../World/PokeMonsterBuildingCutaway.h"
#include "Components/BoxComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "HAL/IConsoleManager.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"

namespace
{
 TAutoConsoleVariable<int32> BushEnabled(TEXT("pm.BushEncounters.Enable"),-1,TEXT("-1=config, 0=off, 1=on; session-only bush encounter override."));
 TAutoConsoleVariable<int32> BushDebug(TEXT("pm.BushEncounters.Debug"),0,TEXT("1 logs eligible distance checks and shared battle starts."));
}
bool UPokeMonsterBushEncounterSettings::IsValidConfiguration()const
{
 return FMath::IsFinite(ChancePerStep)&&ChancePerStep>=0&&ChancePerStep<=1
  &&FMath::IsFinite(StepDistanceCm)&&StepDistanceCm>=50&&StepDistanceCm<=2000
  &&FMath::IsFinite(CooldownSeconds)&&CooldownSeconds>=1&&CooldownSeconds<=300
  &&FMath::IsFinite(MinimumTravelBetweenEncountersCm)&&MinimumTravelBetweenEncountersCm>=0&&MinimumTravelBetweenEncountersCm<=15000
  &&FMath::IsFinite(SampleSeconds)&&SampleSeconds>=.1f&&SampleSeconds<=1
  &&FMath::IsFinite(MaximumAcceptedDisplacementCm)&&MaximumAcceptedDisplacementCm>=100&&MaximumAcceptedDisplacementCm<=1500
  &&!AllowedHabitats.IsEmpty();
}
bool FPokeMonsterBushTravel::Advance(FVector Position,bool Eligible,const UPokeMonsterBushEncounterSettings& S,float& Travel)
{
 Travel=0;
 if(!Eligible||Position.ContainsNaN()||!S.IsValidConfiguration()){Reset();return false;}
 if(!bAnchored){Previous=Position;bAnchored=true;return false;}
 const float Distance=FVector::Dist2D(Position,Previous);Previous=Position;
 if(!FMath::IsFinite(Distance)||Distance>S.MaximumAcceptedDisplacementCm){Reset();Previous=Position;bAnchored=true;return false;}
 Travel=Distance;Remainder+=Distance;
 if(Remainder<S.StepDistanceCm)return false;
 Remainder=FMath::Fmod(Remainder,S.StepDistanceCm);return true; // At most one check per bounded sample.
}
bool APokeMonsterWildEncounterZone::AreBushEncountersEnabled()
{
 const int32 Override=BushEnabled.GetValueOnGameThread();const auto* S=GetDefault<UPokeMonsterBushEncounterSettings>();
 return S->IsValidConfiguration()&&(Override<0?S->bEnabled:Override!=0);
}
void APokeMonsterWildEncounterZone::BeginBushTracking(APokeMonsterPlayerCharacter* Player)
{
 if(!bDistanceBasedBushEncounters||!IsValid(Player)||Player!=UGameplayStatics::GetPlayerPawn(this,0))return;
 if(!GetDefault<UPokeMonsterBushEncounterSettings>()->IsValidConfiguration())return;
 BushPlayer=Player;BushTravel.Reset();
 GetWorldTimerManager().SetTimer(BushTimer,this,&APokeMonsterWildEncounterZone::SampleBushTravel,
  FMath::Clamp(GetDefault<UPokeMonsterBushEncounterSettings>()->SampleSeconds,.1f,1.f),true);
}
void APokeMonsterWildEncounterZone::OnLeft(UPrimitiveComponent*,AActor* Other,UPrimitiveComponent*,int32)
{
 if(Other==BushPlayer.Get()){GetWorldTimerManager().ClearTimer(BushTimer);BushPlayer.Reset();BushTravel.Reset();}
}
void APokeMonsterWildEncounterZone::SampleBushTravel()
{
 auto* P=BushPlayer.Get();if(!IsValid(P)||!Trigger->IsOverlappingActor(P))
 {GetWorldTimerManager().ClearTimer(BushTimer);BushPlayer.Reset();BushTravel.Reset();return;}
 auto* H=GetWorld()->GetSubsystem<UPokeMonsterHabitatSubsystem>();const auto* S=GetDefault<UPokeMonsterBushEncounterSettings>();float Distance=0;
 const bool Due=BushTravel.Advance(P->GetActorLocation(),H&&AreBushEncountersEnabled()&&H->CanCheckBushEncounters(P),*S,Distance);
 if(H&&Distance>0)H->AdvanceBushTravel(Distance);
 if(!Due||!H||H->GetBushCooldownRemaining()>0||H->GetBushTravelRemaining()>0)return;
 ++BushChecks;const float Roll=BushRandom.FRand();
 if(BushDebug.GetValueOnGameThread())UE_LOG(LogTemp,Display,TEXT("PM_BUSH check %s #%d roll=%.4f chance=%.3f"),*GetName(),BushChecks,Roll,S->ChancePerStep);
 if(Roll<S->ChancePerStep&&H->TryStartBushEncounter(P,HabitatZoneId,this,BushRandom))++BushStarts;
}
void APokeMonsterWildEncounterZone::EndPlay(const EEndPlayReason::Type Reason)
{
 GetWorldTimerManager().ClearTimer(BushTimer);BushPlayer.Reset();BushTravel.Reset();
 if(auto* GI=GetGameInstance())if(auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>())E->OnPersistentStateRestored.RemoveDynamic(this,&APokeMonsterWildEncounterZone::RefreshPersistentState);
 Super::EndPlay(Reason);
}
bool UPokeMonsterHabitatSubsystem::CanCheckBushEncounters(APokeMonsterPlayerCharacter* P)const
{
 auto* W=GetWorld();auto* GI=W?W->GetGameInstance():nullptr;if(!W||!GI||!IsValid(P)||P!=UGameplayStatics::GetPlayerPawn(W,0)||P->IsOverworldInputLocked()||UGameplayStatics::IsGamePaused(W))return false;
 const auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>();const auto* D=GI->GetSubsystem<UPokeMonsterDialogueSubsystem>();const auto* S=GI->GetSubsystem<UPokeMonsterSaveSubsystem>();const auto* C=GI->GetSubsystem<UPokeMonsterWorldClock>();
 if(!bEnabled||!E||E->IsEncounterActive()||!D||D->IsDialogueActive()||!S||S->IsLoadInProgress()||!C||C->IsClockPaused())return false;
 for(TActorIterator<APokeMonsterBuildingCutaway> B(W);B;++B)if(B->IsViewerInside(P->GetActorLocation())||B->IsViewerRelocated()||B->GetCutawayAmount()>0)return false;
 return true;
}
double UPokeMonsterHabitatSubsystem::GetBushCooldownRemaining()const{return GetWorld()?FMath::Max(0.,BushCooldownUntil-GetWorld()->GetTimeSeconds()):0.;}
void UPokeMonsterHabitatSubsystem::AdvanceBushTravel(float Distance)
{
 if(FMath::IsFinite(Distance)&&Distance>0)BushTravelRemaining=FMath::Max(0.f,BushTravelRemaining-Distance);
}
void UPokeMonsterHabitatSubsystem::HandleBushEncounterFinished(const FPokeMonsterEncounterEndData&)
{
 const auto* S=GetDefault<UPokeMonsterBushEncounterSettings>();BushCooldownUntil=GetWorld()->GetTimeSeconds()+S->CooldownSeconds;BushTravelRemaining=S->MinimumTravelBetweenEncountersCm;
}
bool UPokeMonsterHabitatSubsystem::TryStartBushEncounter(APokeMonsterPlayerCharacter* P,FName ZoneId,AActor* Source,FRandomStream& BushStream)
{
 if(!APokeMonsterWildEncounterZone::AreBushEncountersEnabled()||!CanCheckBushEncounters(P)||GetBushCooldownRemaining()>0||BushTravelRemaining>0||!IsValid(Source)||Source->GetWorld()!=GetWorld())return false;
 const auto* S=GetDefault<UPokeMonsterBushEncounterSettings>();APokeMonsterHabitatZone* Z=nullptr;
 for(auto Candidate:Zones)if(IsValid(Candidate)&&Candidate->ZoneId==ZoneId){Z=Candidate;break;}
 if(!Z||Z->Medium!=EPokeMonsterBiomeMedium::Land||!S->AllowedHabitats.Contains(Z->HabitatType))return false;
 const FVector Local=Z->Bounds->GetComponentTransform().InverseTransformPosition(P->GetActorLocation());const FVector Extent=Z->Bounds->GetUnscaledBoxExtent();
 if(FMath::Abs(Local.X)>Extent.X||FMath::Abs(Local.Y)>Extent.Y||FMath::Abs(Local.Z)>Extent.Z)return false;
 auto* GI=GetWorld()->GetGameInstance();auto* E=GI->GetSubsystem<UPokeMonsterEncounterSubsystem>();const auto* C=GI->GetSubsystem<UPokeMonsterWorldClock>();FPokeMonsterEncounterContext Context;Context.RegionId=Z->HabitatType;
 switch(C->GetPhase())
 {
 case EPokeMonsterDayPhase::EarlyMorning:case EPokeMonsterDayPhase::Dawn:Context.Time=EPokeMonsterEncounterTime::Morning;break;
 case EPokeMonsterDayPhase::Day:Context.Time=EPokeMonsterEncounterTime::Day;break;
 case EPokeMonsterDayPhase::Dusk:Context.Time=EPokeMonsterEncounterTime::Evening;break;
 default:Context.Time=EPokeMonsterEncounterTime::Night;break;
 }
 const auto* H=GetDefault<UPokeMonsterHabitatSettings>();TArray<int32> Candidates;TArray<float> Weights;float Total=0;
 for(int32 I=0;I<H->Rules.Num();++I)
 {
  const auto& Rule=H->Rules[I];const auto* Profile=Profiles.IsValidIndex(I)?Profiles[I].Get():nullptr;
  if(!Rule.Allows(Z->HabitatType)||!Profile||!Registered.ContainsByPredicate([&](const auto& Species){return Species&&Species->GetInternalId()==Rule.Species;}))continue;
  if(!Profile->Entries.ContainsByPredicate([&](const auto& Entry){return Entry.Matches(Context);}))continue;
  const float Weight=Rule.WeightAt(C->GetTime().SecondsOfDay);if(Weight<=0||!FMath::IsFinite(Weight))continue;
  Candidates.Add(I);Weights.Add(Weight);Total+=Weight;
 }
 if(Total<=0)return false;
 float Pick=BushStream.FRand()*Total;int32 Selected=Candidates.Last();
 for(int32 I=0;I<Candidates.Num();++I){Pick-=Weights[I];if(Pick<0){Selected=Candidates[I];break;}}
 // No visible actor is spawned, and repeatable bush battles create no permanent completion ID.
 if(!E->EnsureDevPlayerParty()||!E->StartWildEncounter(Profiles[Selected],Context,EPokeMonsterEncounterSource::Zone,P,Source,BushStream.RandRange(1,MAX_int32-1),NAME_None))return false;
 BushCooldownUntil=GetWorld()->GetTimeSeconds()+S->CooldownSeconds;BushTravelRemaining=S->MinimumTravelBetweenEncountersCm;
 UE_LOG(LogTemp,Display,TEXT("PM_BUSH start habitat=%s species=%s profile=%s cooldown=%.1fs travel=%.0fcm"),*ZoneId.ToString(),*H->Rules[Selected].Species.ToString(),*Profiles[Selected]->GetPathName(),S->CooldownSeconds,S->MinimumTravelBetweenEncountersCm);return true;
}
