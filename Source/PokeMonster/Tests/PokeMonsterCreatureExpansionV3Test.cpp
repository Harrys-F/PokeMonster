#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "../Creatures/Overworld/PokeMonsterCreatureRoamingComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/Skeleton.h"
#include "Animation/AnimSequence.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCreatureExpansionAssetsTest,
 "PokeMonster.Creature.ExpansionV3.ImportedAssetsAndStableIdentities",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterCreatureExpansionAssetsTest::RunTest(const FString& Parameters)
{
 struct FExpansionCase { const TCHAR* Name; int Dex; float Height; int SourceBones; };
 const FExpansionCase Cases[]={{TEXT("Pikachu"),25,40.f,21},{TEXT("Myrapla"),43,50.f,15},
  {TEXT("Enton"),54,80.f,17},{TEXT("Machomei"),68,160.f,22},{TEXT("Nebulak"),92,130.f,12},
  {TEXT("Gengar"),94,150.f,18},{TEXT("Glurak"),6,170.f,24}};
 TSet<FPrimaryAssetId> Ids;
 for(const auto& Entry:Cases)
 {
  const FString Path=FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),Entry.Name,Entry.Name);
  auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*Path);
  if(!TestNotNull(Path,Species))continue;
  TestEqual(TEXT("Stable species identity"),Species->GetInternalId(),FName(Entry.Name));
  TestEqual(TEXT("National dex number"),Species->GetPokedexNumber(),Entry.Dex);
  TestFalse(TEXT("No duplicated primary asset identity"),Ids.Contains(Species->GetPrimaryAssetId()));Ids.Add(Species->GetPrimaryAssetId());
  const auto* Presentation=Species->GetVisuals().Presentation.LoadSynchronous();
  if(!TestNotNull(TEXT("Presentation loads independently of editor state"),Presentation))continue;
  TestEqual(TEXT("Presentation contract"),Presentation->GetValidationErrors().Num(),0);
  TestEqual(TEXT("All seven explicit roles"),Presentation->Clips.Num(),7);
  TestEqual(TEXT("Documented original height"),Presentation->ReferenceSizeCm,Entry.Height);
  if(!Presentation->Mesh)continue;
  TestTrue(TEXT("Actual imported mesh height, not actor scaling"),FMath::Abs(Presentation->Mesh->GetBounds().BoxExtent.Z*2.f-Entry.Height)<Entry.Height*.05f);
  TestEqual(TEXT("Own anatomy plus FBX armature root"),Presentation->Mesh->GetRefSkeleton().GetNum(),Entry.SourceBones+1);
  for(const auto& Pair:Presentation->Clips)
  {
   if(!Pair.Value)continue;
   TestEqual(TEXT("Exact per-species skeleton"),Pair.Value->GetSkeleton(),Presentation->Mesh->GetSkeleton());
   TestFalse(TEXT("No root-motion extraction"),Pair.Value->bEnableRootMotion);
  }
  auto Instance=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,Species->GetStartingLevel());
  TestTrue(TEXT("Playable instance uses existing data"),Instance.IsValid());
  TestTrue(TEXT("Supported real moves can be assigned"),Instance.AssignSpeciesMoves());
  TestTrue(TEXT("At least one playable move"),!Instance.GetMoveSlots()[0].GetMove().IsNull());
  TestTrue(TEXT("Verified XP yield present"),Species->GetBaseExperienceYield()>0);
 }
 const auto* Original=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 TestTrue(TEXT("Legacy Glumanda save identity survives"),Original&&Original->GetInternalId()==TEXT("Zunderlauf"));
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterCreatureEscapeSeparationTest,
 "PokeMonster.Creature.ExpansionV3.ContactEscapeSeparation",
 EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPokeMonsterCreatureEscapeSeparationTest::RunTest(const FString& Parameters)
{
 const FVector Player=FVector::ZeroVector;
 TestTrue(TEXT("Initial contact may separate without teleporting"),UPokeMonsterCreatureRoamingComponent::CanSeparateFromContact(FVector(-39,0,0),FVector(-42,0,0),Player,40));
 TestFalse(TEXT("Initial contact cannot move into player"),UPokeMonsterCreatureRoamingComponent::CanSeparateFromContact(FVector(-39,0,0),FVector(-20,0,0),Player,40));
 TestFalse(TEXT("A segment cannot tunnel across the player"),UPokeMonsterCreatureRoamingComponent::CanSeparateFromContact(FVector(-60,0,0),FVector(60,0,0),Player,40));
 TestTrue(TEXT("Safe tangent preserves physical body clearance"),UPokeMonsterCreatureRoamingComponent::CanSeparateFromContact(FVector(-60,40,0),FVector(60,40,0),Player,40));
 TestTrue(TEXT("Moving away from an already clear start"),UPokeMonsterCreatureRoamingComponent::CanSeparateFromContact(FVector(-60,0,0),FVector(-80,0,0),Player,40));
 TestFalse(TEXT("No zero-length escape from overlap"),UPokeMonsterCreatureRoamingComponent::CanSeparateFromContact(FVector(-39,0,0),FVector(-39,0,0),Player,40));
 return true;
}
#endif
