#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "Animation/AnimSequence.h"
#include "Animation/Skeleton.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/StaticMesh.h"
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FMeshyGlumandaContract,"PokeMonster.Creatures.MeshyGlumanda.ImportedContract",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FMeshyGlumandaContract::RunTest(const FString&)
{
 auto* D=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Zunderlauf/MeshyV1/DA_Glumanda_Presentation.DA_Glumanda_Presentation"));
 if(!TestNotNull(TEXT("Independent Meshy candidate"),D))return false;
 if(!TestTrue(TEXT("Pipeline contract"),D->GetValidationErrors().IsEmpty()))return false;TestEqual(TEXT("Original height reference"),D->ReferenceSizeCm,60.f);TestEqual(TEXT("Fitted walk speed"),D->WalkSpeed,22.f);TestEqual(TEXT("Fitted run speed"),D->RunSpeed,36.f);
 TestTrue(TEXT("Imported body height is 60cm"),FMath::Abs(D->Mesh->GetBounds().BoxExtent.Z*2-60.f)<.2f);TestEqual(TEXT("Seven independent clips"),D->Clips.Num(),7);
 const auto& R=D->Mesh->GetRefSkeleton();TestEqual(TEXT("Own 23 bones plus FBX root"),R.GetNum(),24);TestEqual(TEXT("Own root wrapper"),R.GetBoneName(0),FName(TEXT("Glumanda_Meshy_Rig")));
 TestNull(TEXT("No duplicate legacy flame"),D->TailFlame.Get());
 if(TestEqual(TEXT("Only one tail effect"),D->EffectAnchors.Num(),1)){TestEqual(TEXT("Flame socket"),D->EffectAnchors[0].Socket,FName(TEXT("tail_socket")));TestNotNull(TEXT("Original Meshy flame geometry"),D->EffectAnchors[0].Mesh.Get());}
 for(int32 I=0;I<7;++I){auto* Clip=D->Clips.FindRef(static_cast<EPokeMonsterCreatureClip>(I)).Get();if(TestNotNull(TEXT("Clip"),Clip)){TestEqual(TEXT("Exact candidate skeleton"),Clip->GetSkeleton(),D->Mesh->GetSkeleton());TestFalse(TEXT("No extracted root motion"),Clip->bEnableRootMotion);}}
 if(D->EffectAnchors.Num()==1)
 {
  int32 Index=R.FindBoneIndex(TEXT("tail_socket"));FTransform Socket=R.GetRefBonePose()[Index];while((Index=R.GetParentIndex(Index))!=INDEX_NONE)Socket=Socket*R.GetRefBonePose()[Index];
  const FVector Scale=Socket.GetScale3D()*D->EffectAnchors[0].Offset.GetScale3D();TestTrue(TEXT("FBX socket scale is compensated"),Scale.Equals(FVector::OneVector,.001f));
  const float Height=D->EffectAnchors[0].Mesh->GetBounds().BoxExtent.Z*2;TestTrue(TEXT("Original flame has plausible 15-35cm height, not a giant proxy"),Height>15.f&&Height<35.f);
 }
 auto* Walk=D->Clips.FindRef(EPokeMonsterCreatureClip::Walk).Get();FVector Last;
 for(int32 Frame=0;Frame<=8;++Frame)
 {
  TArray<FTransform> CS;CS.SetNum(R.GetNum());for(int32 I=0;I<CS.Num();++I){FTransform Local;Walk->GetBoneTransform(Local,FSkeletonPoseBoneIndex(I),FAnimExtractContext(Frame/30.,false),true);int32 Parent=R.GetParentIndex(I);CS[I]=Parent<0?Local:Local*CS[Parent];}
  const FVector Foot=CS[R.FindBoneIndex(TEXT("foot_L"))].GetTranslation();const FVector Hip=CS[R.FindBoneIndex(TEXT("thigh_L"))].GetTranslation();const FVector Knee=CS[R.FindBoneIndex(TEXT("shin_L"))].GetTranslation();
  TestTrue(TEXT("Natural forward knee"),Knee.X>FMath::Min(Hip.X,Foot.X));TestTrue(TEXT("Sagittal leg plane"),FMath::Abs(Foot.Y-Knee.Y)<.05f);
  if(Frame>0){TestTrue(TEXT("Stance cancels 22cm/s"),FMath::Abs((Foot-Last).X+22.f/30.f)<.05f);TestTrue(TEXT("Stance has stable ankle height"),FMath::Abs((Foot-Last).Z)<.05f);}Last=Foot;
 }
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));if(!TestNotNull(TEXT("Existing species"),S))return false;TestEqual(TEXT("Gameplay identity retained"),S->GetInternalId(),FName(TEXT("Zunderlauf")));TestEqual(TEXT("Active species uses the Meshy candidate"),S->GetVisuals().Presentation.LoadSynchronous(),D);return true;
}
#endif
