#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/Overworld/PokeMonsterCreatureBehavior.h"
#include "../Characters/PokeMonsterCharacterFillComponent.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FOverworldBehaviorPolicy,"PokeMonster.Overworld.Behavior.PerceptionAndHysteresis",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FOverworldBehaviorPolicy::RunTest(const FString&)
{
 using T=EPokeMonsterOverworldTemperament;using S=EPokeMonsterOverworldState;FPokeMonsterCreatureBehaviorProfile P;
 P.Temperament=T::Curious;
 TestEqual(TEXT("Curious notices and approaches"),FPokeMonsterCreatureBehavior::Decide(P,450,true,false,false),S::Approach);
 TestEqual(TEXT("Curious observes at a respectful distance"),FPokeMonsterCreatureBehavior::Decide(P,220,true,true,false),S::Observe);
 TestEqual(TEXT("Curious retreats inside personal space"),FPokeMonsterCreatureBehavior::Decide(P,120,true,true,false),S::Retreat);
 P.Temperament=T::Shy;
 TestEqual(TEXT("Shy flees"),FPokeMonsterCreatureBehavior::Decide(P,400,true,false,false),S::Retreat);
 TestEqual(TEXT("Hysteresis retains fleeing outside initial detection"),FPokeMonsterCreatureBehavior::Decide(P,650,true,true,false),S::Retreat);
 TestEqual(TEXT("Unseen player behind obstacle is not pursued"),FPokeMonsterCreatureBehavior::Decide(P,300,false,true,false),S::Wander);
 TestEqual(TEXT("Beyond disengagement returns to habitat wander"),FPokeMonsterCreatureBehavior::Decide(P,800,true,true,false),S::Wander);
 P.Temperament=T::Calm;
 TestEqual(TEXT("Calm doesn't chase"),FPokeMonsterCreatureBehavior::Decide(P,400,true,false,false),S::Wander);
 TestEqual(TEXT("Calm nearby observes without attacking"),FPokeMonsterCreatureBehavior::Decide(P,120,true,false,false),S::Observe);
 P.NoticeRadius=P.PersonalSpace;TestFalse(TEXT("Invalid distance contract rejected"),P.IsValid());
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FOverworldTerritoryPolicy,"PokeMonster.Overworld.Behavior.TerritorialEncounterGate",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FOverworldTerritoryPolicy::RunTest(const FString&)
{
 FPokeMonsterCreatureBehaviorProfile P;P.Temperament=EPokeMonsterOverworldTemperament::Territorial;
 TestFalse(TEXT("Cannot bypass warning by contact"),FPokeMonsterCreatureBehavior::CanInitiate(P,100,0,true,true,false));
 TestTrue(TEXT("Warned visible near player may start normal encounter"),FPokeMonsterCreatureBehavior::CanInitiate(P,100,3,true,true,false));
 TestFalse(TEXT("Not through a wall"),FPokeMonsterCreatureBehavior::CanInitiate(P,100,3,false,true,false));
 TestFalse(TEXT("Not at arbitrary distance"),FPokeMonsterCreatureBehavior::CanInitiate(P,500,3,true,true,false));
 TestFalse(TEXT("Cooldown prevents repeat"),FPokeMonsterCreatureBehavior::CanInitiate(P,100,3,true,true,true));
 TestFalse(TEXT("Time alone doesn't rearm territory"),FPokeMonsterCreatureBehavior::CanInitiate(P,100,3,true,false,false));
 P.bCanInitiateEncounter=false;TestFalse(TEXT("Encounter override can disable auto battle"),FPokeMonsterCreatureBehavior::CanInitiate(P,100,3,true,true,false));
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
