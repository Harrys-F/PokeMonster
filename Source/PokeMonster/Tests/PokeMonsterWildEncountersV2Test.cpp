#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Encounter/PokeMonsterVisibleWildCreatureActor.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWildExactContact,"PokeMonster.Encounter.WildV2.ExactCapsuleContact",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWildExactContact::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* Wild=W->SpawnActor<APokeMonsterVisibleWildCreatureActor>();auto* Player=W->SpawnActor<APokeMonsterPlayerCharacter>();
 const auto* Body=Wild->FindComponentByClass<UCapsuleComponent>();const float Sum=Body->GetScaledCapsuleRadius()+Player->GetCapsuleComponent()->GetScaledCapsuleRadius();
 Player->SetActorLocation(FVector(Sum+20,0,0),false);
 TestFalse(TEXT("Old proximity sphere must not start contact"),Wild->IsTouchingPlayer(Player));
 Player->SetActorLocation(FVector(Sum+1,0,0),false);TestTrue(TEXT("Actual surfaces within movement skin touch"),Wild->IsTouchingPlayer(Player));
 Player->SetActorLocation(FVector(0,0,400),false);TestFalse(TEXT("Different floors do not touch"),Wild->IsTouchingPlayer(Player));
 TestFalse(TEXT("Companion/non-player cannot touch-trigger"),Wild->IsTouchingPlayer(nullptr));
 TestTrue(TEXT("Keyboard E is preserved"),Player->GetInteractionKeys().Contains(EKeys::E));
 TestEqual(TEXT("No physical controller key forced by default"),Player->GetInteractionKeys().Num(),2);
 TestFalse(TEXT("Controller customization does not replace keyboard"),Player->SetInteractionControllerKey(EKeys::Q));
 TestTrue(TEXT("Optional chosen gamepad key maps the SAME action"),Player->SetInteractionControllerKey(EKeys::Gamepad_FaceButton_Right));
 TestTrue(TEXT("Chosen optional key present"),Player->GetInteractionKeys().Contains(EKeys::Gamepad_FaceButton_Right));
 TestTrue(TEXT("Keyboard Enter still present"),Player->GetInteractionKeys().Contains(EKeys::Enter));
 TestTrue(TEXT("User may clear provisional controller key"),Player->SetInteractionControllerKey(FKey()));
 TestEqual(TEXT("Clearing optional key restores original mappings"),Player->GetInteractionKeys().Num(),2);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWildTargetRanking,"PokeMonster.Encounter.WildV2.DirectionalTargetRanking",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWildTargetRanking::RunTest(const FString&)
{
 // A short diagonal corner crossing can fall entirely between 25-cm ground samples.
 const FBox Rock(FVector(0,0,0),FVector(20,20,50));const FVector Start(-40,98,0),End(160,-102,0);
 bool SparseSamplesClear=true;const int32 Steps=FMath::CeilToInt(FVector::Dist2D(Start,End)/25.f);
 const FBox Expanded(Rock.Min-FVector(10,10,60),Rock.Max+FVector(10,10,25));
 for(int32 I=1;I<=Steps;++I)SparseSamplesClear &= !Expanded.IsInsideOrOn(FMath::Lerp(Start,End,float(I)/Steps));
 TestTrue(TEXT("Regression fixture passes the old sparse point checks"),SparseSamplesClear);
 TestTrue(TEXT("Continuous path rejects the actual narrow corner crossing"),UPokeMonsterCreatureRoamingComponent::IsDecorativeSegmentBlocked(Rock,Start,End,10,30,25));
 TestFalse(TEXT("Clear path remains allowed"),UPokeMonsterCreatureRoamingComponent::IsDecorativeSegmentBlocked(Rock,FVector(-40,100,0),FVector(160,100,0),10,30,25));
 TestFalse(TEXT("Another floor above the rock is not blocked"),UPokeMonsterCreatureRoamingComponent::IsDecorativeSegmentBlocked(Rock,Start+FVector(0,0,300),End+FVector(0,0,300),10,30,25));
 const FVector Facing(1,0,0);using FPlayer=APokeMonsterPlayerCharacter;
 TestTrue(TEXT("Facing is preferred over similar off-axis distance"),FPlayer::InteractionTargetScore(FVector(130,0,0),Facing,182)<FPlayer::InteractionTargetScore(FVector(70,90,0),Facing,182));
 TestTrue(TEXT("Closer target on same bearing wins"),FPlayer::InteractionTargetScore(FVector(90,0,0),Facing,182)<FPlayer::InteractionTargetScore(FVector(140,0,0),Facing,182));
 TestEqual(TEXT("Behind player rejected"),FPlayer::InteractionTargetScore(FVector(-60,0,0),Facing,182),-1.f);
 TestEqual(TEXT("Out of interaction range rejected"),FPlayer::InteractionTargetScore(FVector(220,0,0),Facing,182),-1.f);
 TestEqual(TEXT("Another floor rejected"),FPlayer::InteractionTargetScore(FVector(60,0,300),Facing,182),-1.f);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FWildBlockedEscape,"PokeMonster.Encounter.WildV2.SealedEscapeSafeFallback",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FWildBlockedEscape::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* Cube=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));
 auto Box=[&](FVector P,FVector Scale){auto* A=W->SpawnActor<AStaticMeshActor>(P,FRotator::ZeroRotator);A->GetStaticMeshComponent()->SetStaticMesh(Cube);A->SetActorScale3D(Scale);A->GetStaticMeshComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);A->GetStaticMeshComponent()->SetCollisionResponseToAllChannels(ECR_Block);};
 Box(FVector(0,0,-10),FVector(30,30,.2));
 Box(FVector(100,0,100),FVector(.2,2.4,2));Box(FVector(-100,0,100),FVector(.2,2.4,2));
 Box(FVector(0,100,100),FVector(2.4,.2,2));Box(FVector(0,-100,100),FVector(2.4,.2,2));
 auto* Owner=W->SpawnActor<AActor>();auto* M=NewObject<UPokeMonsterCreatureRoamingComponent>(Owner);Owner->AddInstanceComponent(M);M->RegisterComponent();
 M->Configure(LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf")),0,20,30);
 TestTrue(TEXT("Defeat escape may leave normal habitat"),M->BeginDefeatEscape());
 for(int32 I=0;I<5;++I)M->TickComponent(1.6f,LEVELTICK_All,nullptr);
 TestTrue(TEXT("Sealed route exposes blocked fallback"),M->bEscapeBlocked);
 TestTrue(TEXT("Escape phase remains active and can retry"),M->bEscapingDefeat);
 TestTrue(TEXT("No teleport through the ring"),Owner->GetActorLocation().Equals(FVector::ZeroVector));
 TestEqual(TEXT("No false movement distance"),M->DistanceTravelled,0.f);
 return true;
}
#endif
