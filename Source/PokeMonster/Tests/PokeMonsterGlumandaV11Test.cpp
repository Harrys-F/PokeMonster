#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Engine/SkeletalMesh.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FGlumandaV11Assets,"PokeMonster.Creatures.GlumandaV11.IdentityAndRepairedSkin",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FGlumandaV11Assets::RunTest(const FString&)
{
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 auto* Before=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Zunderlauf/MeshyV1/DA_Glumanda_Presentation.DA_Glumanda_Presentation"));
 auto* After=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Zunderlauf/MeshyV11/DA_Glumanda_V11.DA_Glumanda_V11"));
 if(!TestNotNull(TEXT("Stable species asset"),S)||!TestNotNull(TEXT("Original profile retained"),Before)||!TestNotNull(TEXT("Repaired skin profile"),After))return false;
 TestEqual(TEXT("Visible name"),S->GetDisplayName().ToString(),FString(TEXT("Glumanda")));
 TestEqual(TEXT("Saved identity unchanged"),S->GetPrimaryAssetId().ToString(),FString(TEXT("CreatureSpecies:Zunderlauf")));
 TestEqual(TEXT("Only active presentation replaced"),S->GetVisuals().Presentation.LoadSynchronous(),After);
 if(!TestTrue(TEXT("Complete valid profile"),After->GetValidationErrors().IsEmpty()))return false;
 TestTrue(TEXT("Independent mesh"),After->Mesh!=Before->Mesh);TestEqual(TEXT("Exact original skeleton reused"),After->Mesh->GetSkeleton(),Before->Mesh->GetSkeleton());
 TestTrue(TEXT("Original 60cm silhouette"),FMath::Abs(After->Mesh->GetBounds().BoxExtent.Z*2-60.f)<.2f);
 TestEqual(TEXT("Seven original clips"),After->Clips.Num(),7);
 for(const auto& P:Before->Clips)TestEqual(TEXT("No animation duplication or replacement"),After->Clips.FindRef(P.Key),P.Value);
 TestEqual(TEXT("Original material count"),After->Mesh->GetMaterials().Num(),Before->Mesh->GetMaterials().Num());
 for(int32 I=0;I<Before->Mesh->GetMaterials().Num();++I)TestEqual(TEXT("Original material reused"),After->Mesh->GetMaterials()[I].MaterialInterface,Before->Mesh->GetMaterials()[I].MaterialInterface);
 TestEqual(TEXT("One original tail flame"),After->EffectAnchors.Num(),1);TestNull(TEXT("No duplicate legacy fire"),After->TailFlame.Get());
 if(After->EffectAnchors.Num()==1)TestEqual(TEXT("Original tail effect geometry"),After->EffectAnchors[0].Mesh,Before->EffectAnchors[0].Mesh);
 return true;
}
#endif
