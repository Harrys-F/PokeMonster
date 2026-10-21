#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Engine/SkeletalMesh.h"
#include "Rendering/SkeletalMeshRenderData.h"
#include "Rendering/SkeletalMeshLODRenderData.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FSchiggySurfaceCompatibility,"PokeMonster.Creatures.Schiggy.LocalSurfaceCompatibility",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FSchiggySurfaceCompatibility::RunTest(const FString&)
{
 auto* Original=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Schiggy/MeshyV1/DA_Schiggy_Presentation.DA_Schiggy_Presentation"));
 auto* Current=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Schiggy/SurfaceV2/DA_Schiggy_Presentation.DA_Schiggy_Presentation"));
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Schiggy.DA_Schiggy"));
 if(!Original||!Current||!Species||!Current->Mesh||!Original->Mesh){AddError(TEXT("Required original and local repair sources missing"));return false;}
 TestTrue(TEXT("Active species uses validated surface profile"),Species->GetVisuals().Presentation.LoadSynchronous()==Current);
 TestEqual(TEXT("Stable species ID"),Species->GetInternalId(),FName(TEXT("Schiggy")));
 TestTrue(TEXT("Original rig retained"),Current->Mesh->GetSkeleton()==Original->Mesh->GetSkeleton());
 TestEqual(TEXT("Original scale retained"),Current->ReferenceSizeCm,50.f);
 const auto& Ref=Current->Mesh->GetRefSkeleton();const auto& OldRef=Original->Mesh->GetRefSkeleton();
 TestEqual(TEXT("Original imported hierarchy including FBX root retained"),Ref.GetNum(),OldRef.GetNum());
 for(int32 I=0;I<FMath::Min(Ref.GetNum(),OldRef.GetNum());++I)
 {
  TestEqual(TEXT("Original bone names retained"),Ref.GetBoneName(I),OldRef.GetBoneName(I));
  TestEqual(TEXT("Original parent indices retained"),Ref.GetParentIndex(I),OldRef.GetParentIndex(I));
  TestTrue(TEXT("Original imported rest transforms retained"),Ref.GetRefBonePose()[I].Equals(OldRef.GetRefBonePose()[I],.001f));
 }
 TestTrue(TEXT("Presentation remains valid"),Current->GetValidationErrors().IsEmpty());
 TestEqual(TEXT("Only one local repair material added"),Current->Mesh->GetMaterials().Num(),2);
 if(Current->Mesh->GetMaterials().Num()==2)
 {
  TestTrue(TEXT("Original body material and all atlas textures retained"),Current->Mesh->GetMaterials()[0].MaterialInterface==Original->Mesh->GetMaterials()[0].MaterialInterface);
  TestNotNull(TEXT("Local cap material assigned"),Current->Mesh->GetMaterials()[1].MaterialInterface.Get());
 }
 for(auto Clip:{EPokeMonsterCreatureClip::Idle,EPokeMonsterCreatureClip::Walk,EPokeMonsterCreatureClip::Run,EPokeMonsterCreatureClip::Attack,EPokeMonsterCreatureClip::Hit,EPokeMonsterCreatureClip::Faint,EPokeMonsterCreatureClip::Happy})
  TestTrue(TEXT("Existing animation object reused"),Current->Clips.FindRef(Clip)==Original->Clips.FindRef(Clip));
 auto* Data=Current->Mesh->GetResourceForRendering();
 if(TestNotNull(TEXT("Actual Unreal LOD data"),Data)&&TestTrue(TEXT("LOD0 available"),Data->LODRenderData.Num()>0))
  TestEqual(TEXT("Bounded repair, nine new triangles"),Data->LODRenderData[0].GetTotalFaces(),21282);
 return true;
}
#endif
