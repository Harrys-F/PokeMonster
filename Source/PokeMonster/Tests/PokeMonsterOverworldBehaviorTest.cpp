#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/Overworld/PokeMonsterCreatureBehavior.h"
#include "../Characters/PokeMonsterCharacterFillComponent.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FOverworldBehaviorPolicy,"PokeMonster.Overworld.Behavior.PerceptionAndHysteresis",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FOverworldBehaviorPolicy::RunTest(const FString&)
{
 using EOverworldTemperament = EPokeMonsterOverworldTemperament;using EOverworldState = EPokeMonsterOverworldState;FPokeMonsterCreatureBehaviorProfile P;
 P.Temperament=EOverworldTemperament::Curious;
 TestEqual(TEXT("Curious notices and approaches"),FPokeMonsterCreatureBehavior::Decide(P,450,true,false,false),EOverworldState::Approach);
 TestEqual(TEXT("Curious observes at a respectful distance"),FPokeMonsterCreatureBehavior::Decide(P,220,true,true,false),EOverworldState::Observe);
 TestEqual(TEXT("Curious retreats inside personal space"),FPokeMonsterCreatureBehavior::Decide(P,120,true,true,false),EOverworldState::Retreat);
 P.Temperament=EOverworldTemperament::Shy;
 TestEqual(TEXT("Shy flees"),FPokeMonsterCreatureBehavior::Decide(P,400,true,false,false),EOverworldState::Retreat);
 TestEqual(TEXT("Hysteresis retains fleeing outside initial detection"),FPokeMonsterCreatureBehavior::Decide(P,650,true,true,false),EOverworldState::Retreat);
 TestEqual(TEXT("Unseen player behind obstacle is not pursued"),FPokeMonsterCreatureBehavior::Decide(P,300,false,true,false),EOverworldState::Wander);
 TestEqual(TEXT("Beyond disengagement returns to habitat wander"),FPokeMonsterCreatureBehavior::Decide(P,800,true,true,false),EOverworldState::Wander);
 P.Temperament=EOverworldTemperament::Calm;
 TestEqual(TEXT("Calm doesn't chase"),FPokeMonsterCreatureBehavior::Decide(P,400,true,false,false),EOverworldState::Wander);
 TestEqual(TEXT("Calm nearby observes without attacking"),FPokeMonsterCreatureBehavior::Decide(P,120,true,false,false),EOverworldState::Observe);
 P.NoticeRadius=P.PersonalSpace;TestFalse(TEXT("Invalid distance contract rejected"),P.IsValid());
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FOverworldTerritoryPolicy,"PokeMonster.Overworld.Behavior.TerritorialEncounterGate",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FOverworldTerritoryPolicy::RunTest(const FString&)
{
 FPokeMonsterCreatureBehaviorProfile P;P.Temperament=EPokeMonsterOverworldTemperament::Territorial;
 TestFalse(TEXT("Warning/proximity never initiates"),FPokeMonsterCreatureBehavior::CanInitiate(P,false,false,false));
 TestTrue(TEXT("Actual territorial contact initiates"),FPokeMonsterCreatureBehavior::CanInitiate(P,true,false,false));
 TestFalse(TEXT("Contact mode does not accept a remote interaction"),FPokeMonsterCreatureBehavior::CanInitiate(P,false,true,false));
 TestFalse(TEXT("Cooldown blocks actual contact"),FPokeMonsterCreatureBehavior::CanInitiate(P,true,false,true));
 for(auto Temperament:{EPokeMonsterOverworldTemperament::Calm,EPokeMonsterOverworldTemperament::Curious,EPokeMonsterOverworldTemperament::Shy})
 {
  P.Temperament=Temperament;
  TestFalse(TEXT("Peaceful/shy contact is not a challenge"),FPokeMonsterCreatureBehavior::CanInitiate(P,true,false,false));
  TestTrue(TEXT("Peaceful/shy explicit challenge allowed"),FPokeMonsterCreatureBehavior::CanInitiate(P,false,true,false));
  TestFalse(TEXT("Challenge respects cooldown"),FPokeMonsterCreatureBehavior::CanInitiate(P,false,true,true));
 }
 P.Temperament=EPokeMonsterOverworldTemperament::Aggressive;
 TestTrue(TEXT("Aggressive actual contact initiates"),FPokeMonsterCreatureBehavior::CanInitiate(P,true,false,false));
 P.Initiation=EPokeMonsterEncounterInitiation::Challenge;
 TestFalse(TEXT("Encounter-specific override disables contact"),FPokeMonsterCreatureBehavior::CanInitiate(P,true,false,false));
 TestTrue(TEXT("Encounter-specific override allows challenge"),FPokeMonsterCreatureBehavior::CanInitiate(P,false,true,false));
 P.bCanInitiateEncounter=false;TestFalse(TEXT("Disabled means no initiation"),FPokeMonsterCreatureBehavior::CanInitiate(P,false,true,false));
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCharacterCanopyEstimate,"PokeMonster.Player.Visibility.ConservativeCanopyCore",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FCharacterCanopyEstimate::RunTest(const FString&)
{
 const FBox Tree(FVector(-250,-250,0),FVector(250,250,900));
 TestTrue(TEXT("Core below canopy can activate"),UPokeMonsterCharacterFillComponent::CanopyOcclusion(FVector(0,0,100),FVector::UpVector,Tree)>.99f);
 TestEqual(TEXT("Open area doesn't activate"),UPokeMonsterCharacterFillComponent::CanopyOcclusion(FVector(700,0,100),FVector::UpVector,Tree),0.f);
 TestEqual(TEXT("No underground sun fill"),UPokeMonsterCharacterFillComponent::CanopyOcclusion(FVector(0,0,100),-FVector::UpVector,Tree),0.f);
 TestEqual(TEXT("Small ground shrub not treated as a canopy"),UPokeMonsterCharacterFillComponent::CanopyOcclusion(FVector::ZeroVector,FVector::UpVector,FBox(FVector(-30),FVector(30))),0.f);
 return true;
}
#endif
