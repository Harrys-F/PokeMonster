#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimSequence.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGlutexoIntegrationTest,"PokeMonster.Creatures.Glutexo.ImportedSourceContract",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGlutexoIntegrationTest::RunTest(const FString& Parameters)
{
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Glutexo.DA_Glutexo"));
 if(!TestNotNull(TEXT("Glutexo species loads"),S))return false;
 TestEqual(TEXT("Stable separate ID"),S->GetInternalId(),FName(TEXT("Glutexo")));
 TestEqual(TEXT("Dex 005"),S->GetPokedexNumber(),5);
 TestEqual(TEXT("Fire type"),S->GetPrimaryType(),EPokeMonsterCreatureType::Fire);
 auto* P=S->GetVisuals().Presentation.LoadSynchronous();
 if(!TestNotNull(TEXT("Own presentation"),P))return false;
 TestEqual(TEXT("Valid presentation"),P->GetValidationErrors().Num(),0);
 TestEqual(TEXT("Seven roles"),P->Clips.Num(),7);
 TestEqual(TEXT("Original height cm"),P->ReferenceSizeCm,110.f);
 if(!TestNotNull(TEXT("Own mesh"),P->Mesh.Get()))return false;
 TestTrue(TEXT("Actual imported height"),FMath::Abs(P->Mesh->GetBounds().BoxExtent.Z*2-110)<5.5f);
 TestTrue(TEXT("Tail flame bone"),P->Mesh->GetRefSkeleton().FindBoneIndex(TEXT("flame_tip"))!=INDEX_NONE);
 for(const auto& Pair:P->Clips)if(TestNotNull(TEXT("Clip exists"),Pair.Value.Get()))
 {TestEqual(TEXT("Exact own skeleton"),Pair.Value->GetSkeleton(),P->Mesh->GetSkeleton());TestFalse(TEXT("In place"),Pair.Value->bEnableRootMotion);}
 auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(S,16);TestTrue(TEXT("Valid existing instance path"),C.IsValid());
 TestTrue(TEXT("Productive species moves"),C.AssignSpeciesMoves());TestFalse(TEXT("Active attack exists"),C.GetMoveSlots()[0].GetMove().IsNull());
 TestTrue(TEXT("Existing healing"),C.RestoreFully());
 return true;
}
#endif
