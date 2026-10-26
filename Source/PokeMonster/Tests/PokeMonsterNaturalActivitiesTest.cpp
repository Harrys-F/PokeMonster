#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/Pawn.h"
#include "Engine/GameInstance.h"
#include "UObject/StrongObjectPtr.h"

struct FPokeMonsterNaturalActivityTestAccess
{
 static void Ready(UPokeMonsterCreatureRoamingComponent* M){M->Path.Reset();M->PauseRemaining=0;M->PeerQueryRemaining=0;M->bActivityRunning=false;M->BehaviorState=EPokeMonsterOverworldState::Wander;}
 static bool Invite(UPokeMonsterCreatureRoamingComponent* A,UPokeMonsterCreatureRoamingComponent* B)
 {return A->TryStartSocial(B,A->GetOwner()->GetActorLocation()-FVector(0,0,A->Offset));}
 static void Rest(UPokeMonsterCreatureRoamingComponent* M,float Elapsed)
 {Ready(M);M->bActivityRunning=true;M->BehaviorState=EPokeMonsterOverworldState::Rest;M->ActivityElapsed=Elapsed;M->ActivityRemaining=15;}
 static void React(UPokeMonsterCreatureRoamingComponent* M,APawn* Player)
 {float Speed=60;M->UpdateBehavior(.1f,M->GetOwner()->GetActorLocation()-FVector(0,0,M->Offset),Player,Speed);}
 static bool Available(UPokeMonsterCreatureRoamingComponent* M){return M->CanSocialize();}
 static bool Pair(UPokeMonsterCreatureRoamingComponent* M){return M->FindSocialPartner();}
 static void Update(UPokeMonsterCreatureRoamingComponent* M,float D=.1f)
 {float Speed=60;M->UpdateActivities(D,M->GetOwner()->GetActorLocation()-FVector(0,0,M->Offset),nullptr,Speed);}
 static void Finish(UPokeMonsterCreatureRoamingComponent* M){M->FinishActivity();}
 static void BindClock(UPokeMonsterCreatureRoamingComponent* M,UPokeMonsterWorldClock* C,EPokeMonsterActivityRhythm Type)
 {M->Rhythm.Rhythm=Type;M->RhythmOffsetMinutes=0;M->BindRhythm(C);}
 static void UnbindClock(UPokeMonsterCreatureRoamingComponent* M){M->UnbindRhythm();}
 static int Anchors(UPokeMonsterCreatureRoamingComponent* M){return M->ForageAnchors.Num();}
};
namespace NaturalActivityTests
{
 struct WorldFixture
 {
  UWorld* World;
  WorldFixture(FName Name=TEXT("Dev_TestMap_VisualV2"))
  {
   World=UWorld::CreateWorld(EWorldType::Game,false,Name);
   GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
   auto* Floor=World->SpawnActor<AStaticMeshActor>(FVector(0,0,-10),FRotator::ZeroRotator);
   Floor->GetStaticMeshComponent()->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));
   Floor->SetActorScale3D(FVector(40,40,.2));Floor->GetStaticMeshComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
   Floor->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);
  }
  ~WorldFixture(){GEngine->DestroyWorldContext(World);World->DestroyWorld(false);}
  UPokeMonsterCreatureRoamingComponent* Spawn(FVector Position=FVector(0,0,60),FName Species=TEXT("Zunderlauf"))
  {
   auto* A=World->SpawnActor<APokeMonsterVisibleWildCreatureActor>(Position,FRotator::ZeroRotator);
   auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*(FString(TEXT("/Game/Data/Creatures/DA_"))+Species.ToString()));
   A->OverworldMovement->Configure(S,60,38,60,nullptr,91);return A->OverworldMovement;
  }
 };
 FPokeMonsterCreatureActivityProfile Only(EPokeMonsterOverworldState State)
 {
  using S=EPokeMonsterOverworldState;FPokeMonsterCreatureActivityProfile P;P.bEnabled=true;P.SocialAcceptance=1.f;
  P.WanderWeight=.00001f;P.ObserveWeight=P.RestWeight=P.SleepWeight=P.ForageWeight=P.SocialWeight=0;
  if(State==S::Rest)P.RestWeight=100;
  if(State==S::Sleep)P.SleepWeight=100;
  if(State==S::Forage)P.ForageWeight=100;
  if(State==S::Social)P.SocialWeight=100;
  return P;
 }
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalProfilesTest,"PokeMonster.Creatures.NaturalActivities.ProfilesAndDeterminism",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalProfilesTest::RunTest(const FString&)
{
 using P=FPokeMonsterCreatureActivityProfile;using S=EPokeMonsterOverworldState;
 for(const TCHAR* Id:{TEXT("Bisasam"),TEXT("Pikachu"),TEXT("Zunderlauf"),TEXT("Myrapla"),TEXT("Enton"),TEXT("Nebulak")})
 {auto V=P::ForSpecies(Id);TestTrue(Id,V.bEnabled&&V.IsValid());}
 TestFalse(TEXT("Other species not silently enabled"),P::ForSpecies(TEXT("Glurak")).bEnabled);
 auto Invalid=P::ForSpecies(TEXT("Bisasam"));Invalid.MinimumSeconds=.1;TestFalse(TEXT("Hectic activity intervals rejected"),Invalid.IsValid());
 Invalid=P::ForSpecies(TEXT("Enton"));Invalid.SocialRadius=NAN;TestFalse(TEXT("NaN rejected"),Invalid.IsValid());
 FRandomStream A(827),B(827),Night(827);int DaySleep=0,NightSleep=0;auto Config=P::ForSpecies(TEXT("Myrapla"));
 for(int I=0;I<4000;++I)
 {
  auto X=P::Select(Config,A,EPokeMonsterActivityPeriod::Day,true,true,true);
  TestEqual(TEXT("Seeded reproducible decisions"),X,P::Select(Config,B,EPokeMonsterActivityPeriod::Day,true,true,true));
  if(X==S::Sleep)++DaySleep;
  if(P::Select(Config,Night,EPokeMonsterActivityPeriod::Night,true,true,true)==S::Sleep)++NightSleep;
 }
 TestTrue(TEXT("Quiet period favors longer sleep without forcing all creatures"),NightSleep>DaySleep*2);
 auto Restricted=NaturalActivityTests::Only(S::Sleep);FRandomStream R(91);
 for(int I=0;I<50;++I)TestEqual(TEXT("Sleep cooldown blocks repeat"),P::Select(Restricted,R,EPokeMonsterActivityPeriod::Day,false,false,false),S::Wander);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalRestTest,"PokeMonster.Creatures.NaturalActivities.SleepRestAndInterrupt",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalRestTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using Access=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* M=F.Spawn();TestTrue(TEXT("Enabled only on actual wild VisualV2 actor"),M->bActivitiesEnabled);
 M->Activities=Only(S::Sleep);Access::Ready(M);Access::Update(M);
 TestEqual(TEXT("Sleep selected"),M->BehaviorState,S::Sleep);
 const FVector Before=M->GetOwner()->GetActorLocation();
 for(int I=0;I<50;++I)M->TickComponent(.1f,LEVELTICK_All,nullptr);
 TestEqual(TEXT("Sleep persists over minimum duration"),M->BehaviorState,S::Sleep);
 TestTrue(TEXT("Sleep never walks/slides"),Before.Equals(M->GetOwner()->GetActorLocation(),.01));TestEqual(TEXT("Zero locomotion speed"),M->CurrentSpeed,0.f);
 M->SetMovementPaused(true);TestTrue(TEXT("Encounter pause releases ambient state"),M->ActivityRemaining==0);M->SetMovementPaused(false);
 TestTrue(TEXT("Sleep not immediately repeated"),M->BehaviorState!=S::Sleep);
 Access::Ready(M);M->Activities=Only(S::Rest);Access::Update(M);TestEqual(TEXT("Long rest uses existing state"),M->BehaviorState,S::Rest);
 Access::Finish(M);Access::Ready(M);M->Activities=Only(S::Sleep);Access::Update(M);TestTrue(TEXT("Interrupted sleep retains cooldown"),M->BehaviorState!=S::Sleep);
 M->BeginDefeatEscape();TestTrue(TEXT("Existing defeat escape wins priority"),M->bEscapingDefeat);TestEqual(TEXT("Existing escape state retained"),M->BehaviorState,S::Retreat);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalForageTest,"PokeMonster.Creatures.NaturalActivities.ForageUsesRealGround",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalForageTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using Access=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* M=F.Spawn();M->Activities=Only(S::Forage);Access::Ready(M);Access::Update(M);
 TestEqual(TEXT("Forage actually plans a route"),M->BehaviorState,S::Forage);TestTrue(TEXT("Travel before examining ground"),M->IsActivityTravelling());
 for(int I=0;I<550&&M->ForageCompleted==0;++I)M->TickComponent(.05f,LEVELTICK_All,nullptr);
 TestTrue(TEXT("Reaches, dwells and completes forage"),M->ForageCompleted>0);TestTrue(TEXT("No teleport substituted"),M->DistanceTravelled>60);TestTrue(TEXT("Stays in original habitat"),M->IsInsideHabitat(M->GetOwner()->GetActorLocation()-FVector(0,0,60)));
 Access::Ready(M);Access::Update(M);TestTrue(TEXT("Forage cooldown avoids immediate repetition"),M->BehaviorState!=S::Forage);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalSocialTest,"PokeMonster.Creatures.NaturalActivities.SocialReservationAndObstacle",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalSocialTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using Access=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* A=F.Spawn();auto* B=F.Spawn(FVector(280,0,60));auto* C=F.Spawn(FVector(320,180,60));
 for(auto* M:{A,B,C}){M->Activities=Only(S::Social);Access::Ready(M);}
 TestTrue(TEXT("Broadphase finds real peer"),Access::Pair(A));Access::Update(A);
 TestEqual(TEXT("Social state shares existing behavior enum"),A->BehaviorState,S::Social);TestNotNull(TEXT("Peer reserved"),A->SocialPartner.Get());
 auto* Partner=A->SocialPartner.Get();if(!Partner)return false;
 TestTrue(TEXT("Reciprocal single reservation"),Partner->SocialPartner==A);
 Access::Pair(C);Access::Update(C);TestFalse(TEXT("Third actor cannot steal occupied peer"),C->SocialPartner==A||C->SocialPartner==Partner);
 A->SetMovementPaused(true);TestNull(TEXT("Interruption releases both partners"),Partner->SocialPartner.Get());TestNull(TEXT("No stuck social state"),A->SocialPartner.Get());
 A->SetMovementPaused(false);A->Configure(LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf")),60,38,60);
 B->Configure(LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf")),60,38,60);Access::Ready(A);Access::Ready(B);C->SetMovementPaused(true);
 auto* Wall=F.World->SpawnActor<AStaticMeshActor>(FVector(140,0,100),FRotator::ZeroRotator);Wall->GetStaticMeshComponent()->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));Wall->SetActorScale3D(FVector(.5,5,2));Wall->GetStaticMeshComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);Wall->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);
 TestFalse(TEXT("Social perception cannot see through wall"),Access::Pair(A));
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalRolloutTest,"PokeMonster.Creatures.NaturalActivities.RolloutAndCompanionIsolation",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalRolloutTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;
 {WorldFixture F(TEXT("OtherExistingMap"));TestFalse(TEXT("Other maps unchanged"),F.Spawn()->bActivitiesEnabled);}
 {WorldFixture F;auto* M=F.Spawn();auto* Follow=F.World->SpawnActor<AActor>();M->Configure(LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf")),60,38,60,Follow);TestFalse(TEXT("Companion never enters wild activity scheduler"),M->bActivitiesEnabled);}
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalSocialCompletionTest,"PokeMonster.Creatures.NaturalActivities.SocialCompletionAndRecovery",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalSocialCompletionTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using Access=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* A=F.Spawn();auto* B=F.Spawn(FVector(280,0,60));
 for(auto* M:{A,B}){M->Activities=Only(S::Social);Access::Ready(M);}
 TestTrue(TEXT("Finds partner"),Access::Pair(A));Access::Update(A);
 float Closest=10000;
 for(int I=0;I<600 && A->SocialCompleted==0;++I)
 {
  A->TickComponent(.05f,LEVELTICK_All,nullptr);B->TickComponent(.05f,LEVELTICK_All,nullptr);
  Closest=FMath::Min(Closest,float(FVector::Dist2D(A->GetOwner()->GetActorLocation(),B->GetOwner()->GetActorLocation())));
 }
 TestTrue(TEXT("Actually approaches and finishes social visit"),A->SocialCompleted==1 && B->SocialCompleted==1);
 TestTrue(TEXT("Partners keep safe body distance"),Closest>120);
 TestNull(TEXT("Timed visit releases leader"),A->SocialPartner.Get());TestNull(TEXT("Timed visit releases waiting partner"),B->SocialPartner.Get());
 TestFalse(TEXT("Social cooldown prevents endless pursuit"),Access::Pair(A));
 TestTrue(TEXT("Leader really moved rather than teleported"),A->DistanceTravelled>80 && A->DistanceTravelled<250);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalInitialSocialTest,"PokeMonster.Creatures.NaturalActivities.FirstDecisionPerceivesClosePeer",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalInitialSocialTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* A=F.Spawn();auto* B=F.Spawn(FVector(125,0,60));
 A->Activities=Only(S::Social);B->Activities=Only(S::Social);
 A->TickComponent(.01f,LEVELTICK_All,nullptr);B->TickComponent(.01f,LEVELTICK_All,nullptr);
 TestEqual(TEXT("Initial choice waits for staggered perception"),A->ActivityDecisions,0);
 for(int I=0;I<100 && !A->SocialPartner;++I){A->TickComponent(.05f,LEVELTICK_All,nullptr);B->TickComponent(.05f,LEVELTICK_All,nullptr);}
 TestTrue(TEXT("First actual decision includes the nearby peer"),A->SocialPartner==B);
 for(int I=0;I<600 && A->SocialCompleted==0;++I){A->TickComponent(.05f,LEVELTICK_All,nullptr);B->TickComponent(.05f,LEVELTICK_All,nullptr);}
 TestEqual(TEXT("Close neighbours finish without rejecting a short separation step"),A->SocialCompleted,1);
 TestTrue(TEXT("Final spacing is safe"),FVector::Dist2D(A->GetOwner()->GetActorLocation(),B->GetOwner()->GetActorLocation())>=140);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalSocialConsentTest,"PokeMonster.Creatures.NaturalActivities.SocialConsentAndMinimumRest",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalSocialConsentTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using Access=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* A=F.Spawn();auto* B=F.Spawn(FVector(280,0,60));
 A->Activities=B->Activities=Only(S::Social);Access::Ready(A);Access::Rest(B,0);
 TestFalse(TEXT("Minimum rest cannot be interrupted by invitation"),Access::Invite(A,B));
 Access::Rest(B,B->Activities.MinimumSeconds+.1f);TestTrue(TEXT("Established rest can accept a visit"),Access::Available(B));
 B->Activities.SocialAcceptance=0;const float Remaining=B->ActivityRemaining;
 TestFalse(TEXT("Receiver can explicitly decline"),Access::Invite(A,B));
 TestEqual(TEXT("Refusal leaves receiver resting"),B->BehaviorState,S::Rest);
 TestEqual(TEXT("Refusal does not reset receiver activity"),B->ActivityRemaining,Remaining);
 TestEqual(TEXT("Decline diagnostic"),B->SocialDeclined,1);TestNull(TEXT("No reservation on refusal"),A->SocialPartner.Get());
 TestFalse(TEXT("Refusal cooldown avoids repeated requests"),Access::Available(A));
 // Fresh independent pair exercises 100% consent without a test bypass in production code.
 auto* C=F.Spawn(FVector(-280,0,60));auto* D=F.Spawn(FVector(-560,0,60));
 C->Activities=D->Activities=Only(S::Social);Access::Ready(C);Access::Rest(D,6);
 TestTrue(TEXT("Accept after minimum rest"),Access::Invite(C,D));
 TestFalse(TEXT("Simultaneous reverse invitation cannot create a second pair"),Access::Invite(D,C));
 TestTrue(TEXT("Exactly reciprocal reservation"),C->SocialPartner==D && D->SocialPartner==C);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalSocialInvalidationTest,"PokeMonster.Creatures.NaturalActivities.SocialPartnerInvalidation",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalSocialInvalidationTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using Access=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 for(int Case=0;Case<6;++Case)
 {
  WorldFixture F;auto* A=F.Spawn();auto* B=F.Spawn(FVector(280,0,60));
  A->Activities=B->Activities=Only(S::Social);Access::Ready(A);Access::Ready(B);
  if(!TestTrue(TEXT("Reservation succeeds before interruption"),Access::Invite(A,B)))continue;
  switch(Case)
  {
   case 0:B->SetMovementPaused(true);break; // Same gate used by encounter transition.
   case 1:B->BeginDefeatEscape();break;
   case 2:B->SetComponentTickEnabled(false);break;
   case 3:B->GetOwner()->SetActorHiddenInGame(true);break;
   case 4:B->GetOwner()->SetActorLocation(FVector(1600,0,60));break;
   case 5:B->Configure(LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf")),60,38,60);break;
  }
  Access::Update(A);
  TestNull(TEXT("Initiator releases on pause/flee/disable/hide/distance/reconfigure"),A->SocialPartner.Get());
  TestNull(TEXT("Receiver also releases"),B->SocialPartner.Get());
  TestTrue(TEXT("Initiator leaves social state"),A->BehaviorState!=S::Social);
  TestFalse(TEXT("Cooldown prevents immediate repeated pursuit"),Access::Available(A));
 }
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalSpontaneousSocialTest,"PokeMonster.Creatures.NaturalActivities.SpontaneousStandardProfiles",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalSpontaneousSocialTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;
 WorldFixture F;TArray<UPokeMonsterCreatureRoamingComponent*> Group;
 for(int I=0;I<3;++I)Group.Add(F.Spawn(FVector(I*220,0,60),TEXT("Bisasam")));
 int32 Completed=0;float Closest=10000;
 for(int I=0;I<3600;++I)
 {
  for(auto* M:Group)M->TickComponent(.05f,LEVELTICK_All,nullptr);
  for(int A=0;A<3;++A)if(Group[A]->SocialPartner)
  {
   TestTrue(TEXT("Every live reservation is reciprocal"),Group[A]->SocialPartner->SocialPartner==Group[A]);
   Closest=FMath::Min(Closest,float(FVector::Dist2D(Group[A]->GetOwner()->GetActorLocation(),Group[A]->SocialPartner->GetOwner()->GetActorLocation())));
  }
 }
 for(auto* M:Group){Completed+=M->SocialCompleted;M->SetMovementPaused(true);}
 TestTrue(TEXT("Unmodified Bisasam profiles complete spontaneous visits"),Completed>=2);
 TestTrue(TEXT("No body overlap during real motion"),Closest>=120);
 for(auto* M:Group)TestNull(TEXT("Group interruption releases all reservations"),M->SocialPartner.Get());
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNaturalSocialThreatTest,"PokeMonster.Creatures.NaturalActivities.SocialPlayerThreatPriority",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNaturalSocialThreatTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using Access=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* A=F.Spawn(FVector(0,0,60),TEXT("Enton"));auto* B=F.Spawn(FVector(280,0,60),TEXT("Enton"));
 A->Activities=B->Activities=Only(S::Social);Access::Ready(A);Access::Ready(B);
 if(!TestTrue(TEXT("Shy pair accepts before danger"),Access::Invite(A,B)))return false;
 auto* Player=F.World->SpawnActor<APawn>(FVector(-100,0,60),FRotator::ZeroRotator);
 Access::React(A,Player);
 TestEqual(TEXT("Actual existing shy policy takes priority"),A->BehaviorState,S::Retreat);
 TestNull(TEXT("Player approach clears initiator reservation"),A->SocialPartner.Get());TestNull(TEXT("Player approach also clears receiver"),B->SocialPartner.Get());
 TestTrue(TEXT("Receiver returns to a valid ambient state"),B->BehaviorState==S::Rest && !B->IsActivityTravelling());
 TestTrue(TEXT("Both record the same interruption"),A->SocialInterrupted==1&&B->SocialInterrupted==1);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRhythmConfigurationTest,"PokeMonster.Creatures.DayRhythms.SixProfilesAndSafeConfiguration",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FRhythmConfigurationTest::RunTest(const FString&)
{
 const auto* C=GetDefault<UPokeMonsterCreatureRhythmSettings>();FPokeMonsterCreatureRhythm R;
 const FName Names[]={TEXT("Bisasam"),TEXT("Pikachu"),TEXT("Zunderlauf"),TEXT("Myrapla"),TEXT("Enton"),TEXT("Nebulak")};
 const EPokeMonsterActivityRhythm Types[]={EPokeMonsterActivityRhythm::Diurnal,EPokeMonsterActivityRhythm::Diurnal,EPokeMonsterActivityRhythm::Flexible,EPokeMonsterActivityRhythm::Nocturnal,EPokeMonsterActivityRhythm::Crepuscular,EPokeMonsterActivityRhythm::Nocturnal};
 TestEqual(TEXT("Only six species configured"),C->SpeciesProfiles.Num(),6);
 for(int I=0;I<6;++I){TestTrue(TEXT("Data configuration resolves stable species"),C->Find(Names[I],R));TestEqual(TEXT("Requested rhythm"),R.Rhythm,Types[I]);TestTrue(TEXT("Valid default offset"),R.IsValid());}
 TestFalse(TEXT("Other species not silently enabled"),C->Find(TEXT("Glurak"),R));
 auto* Bad=NewObject<UPokeMonsterCreatureRhythmSettings>();Bad->SpeciesProfiles=C->SpeciesProfiles;Bad->SpeciesProfiles.Add(C->SpeciesProfiles[0]);TestFalse(TEXT("Ambiguous duplicated rows fail closed"),Bad->Find(TEXT("Bisasam"),R));
 R.QuietWander=0;TestFalse(TEXT("Zero mobility configuration rejected"),R.IsValid());R={};R.ActiveSleep=NAN;TestFalse(TEXT("NaN rejected"),R.IsValid());R={};R.IndividualOffsetMinutes=121;TestFalse(TEXT("Unbounded offsets rejected"),R.IsValid());
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRhythmWeightsTest,"PokeMonster.Creatures.DayRhythms.ActivitySleepForageAndSocialDistributions",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FRhythmWeightsTest::RunTest(const FString&)
{
 using S=EPokeMonsterOverworldState;const auto* Clock=GetDefault<UPokeMonsterWorldClockSettings>();
 for(FName Id:{FName("Bisasam"),FName("Pikachu"),FName("Myrapla"),FName("Nebulak"),FName("Enton")})
 {
  FPokeMonsterCreatureRhythm R;GetDefault<UPokeMonsterCreatureRhythmSettings>()->Find(Id,R);
  const double ActiveHour=R.Rhythm==EPokeMonsterActivityRhythm::Nocturnal?22:R.Rhythm==EPokeMonsterActivityRhythm::Crepuscular?6:12;
  const double QuietHour=R.Rhythm==EPokeMonsterActivityRhythm::Diurnal?22:12;
  auto Base=FPokeMonsterCreatureActivityProfile::ForSpecies(Id);auto Active=R.Weight(Base,R.ActivityAt(ActiveHour*3600,0,*Clock)),Quiet=R.Weight(Base,R.ActivityAt(QuietHour*3600,0,*Clock));
  TestTrue(TEXT("Active feeding and social weights increase"),Active.ForageWeight>Quiet.ForageWeight&&Active.SocialWeight>Quiet.SocialWeight&&Active.SocialAcceptance>Quiet.SocialAcceptance);
  FRandomStream A(913),Q(913);int ActiveSleep=0,QuietSleep=0,ActiveForage=0,QuietForage=0;
  for(int I=0;I<12000;++I)
  {
   const auto X=FPokeMonsterCreatureActivityProfile::Select(Active,A,EPokeMonsterActivityPeriod::Day,true,true,true),Y=FPokeMonsterCreatureActivityProfile::Select(Quiet,Q,EPokeMonsterActivityPeriod::Day,true,true,true);
   ActiveSleep+=X==S::Sleep;QuietSleep+=Y==S::Sleep;ActiveForage+=X==S::Forage;QuietForage+=Y==S::Forage;
  }
  TestTrue(TEXT("Quiet sleep is more frequent, never a forced schedule"),QuietSleep>ActiveSleep*3&&ActiveSleep>0);
  TestTrue(TEXT("Active forage is more frequent; quiet remains possible"),ActiveForage>QuietForage&&QuietForage>0);
 }
 FPokeMonsterCreatureRhythm Flexible;TestTrue(TEXT("Flexible remains substantially active at night"),Flexible.ActivityAt(0,0,*Clock)>.6f);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRhythmContinuityTest,"PokeMonster.Creatures.DayRhythms.ContinuousMidnightOffsetsAndNoSecondClock",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FRhythmContinuityTest::RunTest(const FString&)
{
 const auto* C=GetDefault<UPokeMonsterWorldClockSettings>();TestEqual(TEXT("120-minute rule untouched"),C->RealMinutesPerDay,120.);
 FPokeMonsterCreatureRhythm R;
 for(auto Type:{EPokeMonsterActivityRhythm::Diurnal,EPokeMonsterActivityRhythm::Nocturnal,EPokeMonsterActivityRhythm::Crepuscular,EPokeMonsterActivityRhythm::Flexible})
 {
  R.Rhythm=Type;
  for(float Offset:{-45.f,0.f,45.f})for(int M=0;M<1440;++M)
  {
   const float A=R.ActivityAt(M*60,Offset,*C),B=R.ActivityAt(M*60+.01,Offset,*C);
   TestTrue(TEXT("All day including boundaries continuous and bounded"),A>=0&&A<=1&&FMath::Abs(A-B)<.001f);
   TestEqual(TEXT("Next day same rhythm, no stored independent time"),A,R.ActivityAt(M*60+86400,Offset,*C));
  }
 }
 R.Rhythm=EPokeMonsterActivityRhythm::Diurnal;TestTrue(TEXT("Individuals do not all change together"),R.ActivityAt(6*3600,-45,*C)<R.ActivityAt(6*3600,45,*C));
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRhythmClockEventsTest,"PokeMonster.Creatures.DayRhythms.ClockJumpsAndUnbindingPreserveCurrentActivity",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FRhythmClockEventsTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using A=FPokeMonsterNaturalActivityTestAccess;
 WorldFixture F;auto* M=F.Spawn();TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* Clock=NewObject<UPokeMonsterWorldClock>(GI.Get());
 A::Rest(M,7);A::BindClock(M,Clock,EPokeMonsterActivityRhythm::Diurnal);const float Remaining=M->ActivityRemaining;
 for(int H:{12,22,6,18,4})
 {
  FPokeMonsterWorldTime T;T.SecondsOfDay=H*3600;const int Before=M->RhythmRefreshes;Clock->RestoreTime(T,true);
  TestTrue(TEXT("Actual world-clock event immediately refreshes weights"),M->RhythmRefreshes>Before);
  TestTrue(TEXT("Existing rest not abruptly ended by time set"),M->BehaviorState==EPokeMonsterOverworldState::Rest&&M->ActivityRemaining==Remaining);
  TestEqual(TEXT("Weight derived from actual central clock"),M->RhythmActivity,M->Rhythm.ActivityAt(T.SecondsOfDay,0,*GetDefault<UPokeMonsterWorldClockSettings>()));
 }
 A::UnbindClock(M);const int Before=M->RhythmRefreshes;Clock->RestoreTime({},false);TestEqual(TEXT("Unbinding removes delegates"),M->RhythmRefreshes,Before);TestFalse(TEXT("No stale rhythm flag"),M->bRhythmEnabled);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRhythmPauseTest,"PokeMonster.Creatures.DayRhythms.PauseFreezesAmbientButThreatStillWakes",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FRhythmPauseTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using A=FPokeMonsterNaturalActivityTestAccess;using S=EPokeMonsterOverworldState;
 WorldFixture F;auto* M=F.Spawn();M->Activities=Only(S::Sleep);A::Ready(M);A::Update(M);TestEqual(TEXT("Real activity enters sleep"),M->BehaviorState,S::Sleep);
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* Clock=NewObject<UPokeMonsterWorldClock>(GI.Get());A::BindClock(M,Clock,EPokeMonsterActivityRhythm::Nocturnal);
 const float Before=M->ActivityRemaining;const FVector Position=M->GetOwner()->GetActorLocation();
 for(int I=0;I<100;++I)A::Update(M,.1f);
 TestEqual(TEXT("Authoritative loading/pause guard freezes activity timer"),M->ActivityRemaining,Before);TestEqual(TEXT("No paused ambient movement"),M->GetOwner()->GetActorLocation(),Position);TestFalse(TEXT("Sleeping cannot accept social contact"),A::Available(M));
 M->Settings.Behavior.Temperament=EPokeMonsterOverworldTemperament::Shy;auto* Player=F.World->SpawnActor<APawn>(FVector(100,0,60),FRotator::ZeroRotator);A::React(M,Player);
 TestEqual(TEXT("Danger retains priority even with paused ambient clock"),M->BehaviorState,S::Retreat);TestEqual(TEXT("Sleep activity cleanly interrupted"),M->ActivityRemaining,0.f);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRhythmSocialPauseTest,"PokeMonster.Creatures.DayRhythms.ReservationsSurviveTimeChangeAndReleaseInvalidPausedPeer",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FRhythmSocialPauseTest::RunTest(const FString&)
{
 using namespace NaturalActivityTests;using A=FPokeMonsterNaturalActivityTestAccess;
 WorldFixture F;auto* X=F.Spawn();auto* Y=F.Spawn(FVector(280,0,60));for(auto* M:{X,Y}){M->Activities=Only(EPokeMonsterOverworldState::Social);A::Ready(M);}TestTrue(TEXT("Original mutual invitation succeeds"),A::Invite(X,Y));
 TStrongObjectPtr<UGameInstance> GI(NewObject<UGameInstance>());auto* Clock=NewObject<UPokeMonsterWorldClock>(GI.Get());for(auto* M:{X,Y})A::BindClock(M,Clock,EPokeMonsterActivityRhythm::Diurnal);
 FPokeMonsterWorldTime T;T.SecondsOfDay=22*3600;Clock->RestoreTime(T,true);const float Remaining=X->ActivityRemaining;
 for(int I=0;I<400;++I){A::Update(X,.1f);A::Update(Y,.1f);}
 TestTrue(TEXT("Paused reciprocal reservations stay bounded and intact"),X->SocialPartner==Y&&Y->SocialPartner==X);TestEqual(TEXT("Dwell not advanced while clock paused"),X->ActivityRemaining,Remaining);
 Y->GetOwner()->SetActorHiddenInGame(true);A::Update(X);TestNull(TEXT("Invalid peer clears leader even during clock pause"),X->SocialPartner.Get());TestNull(TEXT("Invalid peer clears receiver"),Y->SocialPartner.Get());
 return true;
}
#endif
