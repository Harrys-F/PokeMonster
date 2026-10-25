#include "PokeMonsterNPCPresentationData.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimSequence.h"
TArray<FString> UPokeMonsterNPCPresentationData::GetValidationErrors() const
{
 TArray<FString> Errors;
 if(TechnicalId.IsNone())Errors.Add(TEXT("Missing technical ID"));
 if(!Mesh||!Mesh->GetSkeleton())Errors.Add(TEXT("Missing skeletal mesh/skeleton"));
 if(Mesh&&!Materials.IsEmpty()&&Materials.Num()!=Mesh->GetMaterials().Num())Errors.Add(TEXT("Material override count mismatch"));
 for(const auto& M:Materials)if(!M)Errors.Add(TEXT("Missing material override"));
 if(!Idle)Errors.Add(TEXT("Missing idle"));
 if(!FMath::IsFinite(ReferenceHeightCm)||ReferenceHeightCm<=0.f)Errors.Add(TEXT("Invalid reference height"));
 if(!FMath::IsFinite(WalkSpeed)||!FMath::IsFinite(RunSpeed)||WalkSpeed<0.f||RunSpeed<0.f)Errors.Add(TEXT("Invalid motion speeds"));
 if((Walk!=nullptr)!=(WalkSpeed>0.f))Errors.Add(TEXT("Walk clip and reference speed must be paired"));
 if((Run!=nullptr)!=(RunSpeed>0.f)||Run&&(!Walk||RunSpeed<=WalkSpeed))Errors.Add(TEXT("Invalid run clip/reference speed"));
 for(auto* Clip:{Idle.Get(),Walk.Get(),Run.Get(),Talk.Get(),Greeting.Get(),TurnLeft.Get(),TurnRight.Get()})
 {
  if(!Clip)continue;
  if(!Mesh||Clip->GetSkeleton()!=Mesh->GetSkeleton())Errors.Add(Clip->GetName()+TEXT(": mismatched skeleton"));
  if(Clip->GetPlayLength()<=0.f||Clip->bEnableRootMotion)Errors.Add(Clip->GetName()+TEXT(": invalid/non-in-place clip"));
 }
 if(Mesh&&bFootContacts)
  for(const TCHAR* Bone:{TEXT("thigh_l"),TEXT("shin_l"),TEXT("foot_l"),TEXT("thigh_r"),TEXT("shin_r"),TEXT("foot_r")})
   if(Mesh->GetRefSkeleton().FindBoneIndex(Bone)==INDEX_NONE)Errors.Add(FString(TEXT("Missing contact bone: "))+Bone);
 return Errors;
}
