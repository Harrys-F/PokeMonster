#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Development/BiomeTestV1/PokeMonsterBiomeHabitat.h"
#include "../Creatures/Overworld/PokeMonsterCreaturePath.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBiomeMediumRules,"PokeMonster.BiomeV1.ExplicitMediaAndContinuousShore",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBiomeMediumRules::RunTest(const FString&)
{
 using H=APokeMonsterBiomeHabitat;using M=EPokeMonsterBiomeMedium;float Z=0,Previous=0;
 TestTrue(TEXT("Land remains dry"),H::MediumFootHeight(M::Land,0,-20,23,45,20,Z));TestEqual(TEXT("Land contact retained"),Z,0.f);
 TestFalse(TEXT("Land never picks deep water"),H::MediumFootHeight(M::Land,-100,-20,23,45,20,Z));
 TestFalse(TEXT("Water only never picks land"),H::MediumFootHeight(M::WaterOnly,0,-20,12,45,20,Z));
 TestFalse(TEXT("Water only never strands on too-shallow bank"),H::MediumFootHeight(M::WaterOnly,-25,-20,12,45,20,Z));
 TestTrue(TEXT("Water only rests at configured draft"),H::MediumFootHeight(M::WaterOnly,-125,-20,12,45,20,Z));TestEqual(TEXT("Draft is not type-derived"),Z,-32.f);
 for(int I=0;I<=125;++I){TestTrue(TEXT("Continuous shore is valid"),H::MediumFootHeight(M::Amphibious,-float(I),-20,23,45,20,Z));if(I)TestTrue(TEXT("No water transition teleport"),FMath::Abs(Z-Previous)<=1.01f);Previous=Z;}
 TestEqual(TEXT("Floating root at safe draft"),Z,-43.f);
 TestTrue(TEXT("Floating follows raised terrain"),H::MediumFootHeight(M::Floating,300,-20,23,45,20,Z));TestEqual(TEXT("Ground-relative float height"),Z,345.f);
 TestFalse(TEXT("Invalid configuration fails closed"),H::MediumFootHeight(M::WaterOnly,-100,-20,-1,45,20,Z));
 TestTrue(TEXT("Normal maps retain gameplay by default"),GetDefault<APokeMonsterGameMode>()->bEnablePersistentGameplay);
 TestFalse(TEXT("Test map explicitly disables persistence and encounters"),GetDefault<APokeMonsterBiomeTestGameMode>()->bEnablePersistentGameplay);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBiomeBoundedWaterPath,"PokeMonster.BiomeV1.ExistingPathRespectsWaterAndWalls",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBiomeBoundedWaterPath::RunTest(const FString&)
{
 TArray<FVector> Path;
 auto Project=[](const FVector& P,FVector& G){if(FMath::Abs(P.X)>450||FMath::Abs(P.Y)>350)return false;G=FVector(P.X,P.Y,0);return true;};
 auto Wall=[](const FVector& A,const FVector& B){const FBox Obstacle(FVector(-45,-180,-10),FVector(45,180,200));return !FMath::LineBoxIntersection(Obstacle,A,B,B-A);};
 TestTrue(TEXT("Existing bounded A* finds water detour"),FPokeMonsterCreaturePath::Find(FVector(-300,0,0),FVector(300,0,0),Project,Wall,Path));
 FVector Previous(-300,0,0);for(const auto& P:Path){FVector G;TestTrue(TEXT("Every waypoint inside allowed water habitat"),Project(P,G));TestTrue(TEXT("Every full segment avoids wall, not just endpoints"),Wall(Previous,P));Previous=P;}
 TestFalse(TEXT("Endpoint outside habitat rejected by combined project/traverse contract"),FPokeMonsterCreaturePath::Find(FVector(-300,0,0),FVector(600,0,0),Project,[&](const FVector& A,const FVector& B){FVector G;return Project(A,G)&&Project(B,G)&&Wall(A,B);},Path));
 return true;
}
#endif

#if WITH_DEV_AUTOMATION_TESTS
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "Animation/AnimSequence.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FBiomeSwimContract,"PokeMonster.BiomeV11.OptionalSwimmingContract",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FBiomeSwimContract::RunTest(const FString&)
{
 auto* Original=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Zunderlauf/DA_Zunderlauf_Presentation.DA_Zunderlauf_Presentation"));
 if(!TestNotNull(TEXT("Existing independent fixture"),Original))return false;
 TestTrue(TEXT("Existing profile remains valid without swim clips"),Original->GetValidationErrors().IsEmpty());
 auto* Candidate=DuplicateObject<UPokeMonsterCreaturePresentationData>(Original,GetTransientPackage());
 Candidate->SwimIdleClip=Candidate->Clips.FindRef(EPokeMonsterCreatureClip::Idle);
 TestFalse(TEXT("Incomplete swim pair rejected atomically"),Candidate->GetValidationErrors().IsEmpty());
 Candidate->SwimClip=Candidate->Clips.FindRef(EPokeMonsterCreatureClip::Walk);
 TestTrue(TEXT("Exact skeleton pair is supported"),Candidate->GetValidationErrors().IsEmpty());
 Candidate->SwimReferenceSpeed=0;TestFalse(TEXT("Zero swim reference rejected"),Candidate->GetValidationErrors().IsEmpty());Candidate->SwimReferenceSpeed=35;
 Candidate->SwimClip=NewObject<UAnimSequence>();TestFalse(TEXT("Foreign skeleton/empty swim rejected"),Candidate->GetValidationErrors().IsEmpty());
 TestTrue(TEXT("Original source still unchanged"),Original->GetValidationErrors().IsEmpty());
 return true;
}
#endif
