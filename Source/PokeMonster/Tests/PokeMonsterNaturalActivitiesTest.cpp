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
#endif
