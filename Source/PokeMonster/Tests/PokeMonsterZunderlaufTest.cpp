#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Encounter/PokeMonsterEncounterProfile.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Capture/PokeMonsterCaptureDeviceData.h"
#include "../Capture/PokeMonsterCaptureLibrary.h"
#include "../Battle/PokeMonsterBattleSession.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Animation/AnimSequence.h"
#include "Animation/Skeleton.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/AssetManager.h"
#include "Engine/GameInstance.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterZunderlaufAssets,"PokeMonster.Creatures.Zunderlauf.AssetContract",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterZunderlaufAssets::RunTest(const FString&)
{
 TestEqual(TEXT("Long editor frames retain actual walk speed"),APokeMonsterCreatureVisualActor::SampleSpeed(FVector(14,0,0),.4f,true),35.f);
 TestEqual(TEXT("Run speed follows distance and time"),APokeMonsterCreatureVisualActor::SampleSpeed(FVector(12,0,0),.2f,true),60.f);
 TestEqual(TEXT("Teleports do not trigger locomotion"),APokeMonsterCreatureVisualActor::SampleSpeed(FVector(1000,0,0),.1f,true),0.f);
 TestEqual(TEXT("First sample cannot invent motion"),APokeMonsterCreatureVisualActor::SampleSpeed(FVector(14,0,0),.4f,false),0.f);
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 if(!TestNotNull(TEXT("Species loads"),S))return false;
 TestEqual(TEXT("Stable species identity"),S->GetInternalId(),FName(TEXT("Zunderlauf")));
 TestEqual(TEXT("Fire typing"),S->GetPrimaryType(),EPokeMonsterCreatureType::Fire);
 TestEqual(TEXT("Species discovered for cooking/save restoration"),UAssetManager::Get().GetPrimaryAssetPath(S->GetPrimaryAssetId()),FSoftObjectPath(S));
 auto* D=LoadObject<UPokeMonsterCreaturePresentationData>(nullptr,TEXT("/Game/Characters/Creatures/Zunderlauf/DA_Zunderlauf_Presentation.DA_Zunderlauf_Presentation"));if(!TestNotNull(TEXT("Presentation loads"),D)||!TestNotNull(TEXT("Mesh loads"),D->Mesh.Get()))return false;
 TestEqual(TEXT("Seven explicit actions"),D->Clips.Num(),7);
 for(int32 I=0;I<7;++I){auto* P=D->Clips.Find(static_cast<EPokeMonsterCreatureClip>(I));UAnimSequence* A=P?P->Get():nullptr;if(TestNotNull(TEXT("Clip exists"),A)){TestEqual(TEXT("Clip uses creature skeleton"),A->GetSkeleton(),D->Mesh->GetSkeleton());TestTrue(TEXT("Clip has duration"),A->GetPlayLength()>.3f);TestFalse(TEXT("In-place clips don't extract root motion"),A->bEnableRootMotion);}}
 TestNotNull(TEXT("One flame mesh"),D->TailFlame.Get());TestNotNull(TEXT("One flame material"),D->FlameMaterial.Get());
 TestEqual(TEXT("Flame belongs exclusively to tail"),D->FlameBone,FName(TEXT("tail_socket")));
 TestTrue(TEXT("Tail attachment exists"),D->Mesh->GetRefSkeleton().FindBoneIndex(D->FlameBone)!=INDEX_NONE);
 const auto& Ref=D->Mesh->GetRefSkeleton();
 TestEqual(TEXT("23 authored bones plus FBX armature root"),Ref.GetNum(),24);
 TestEqual(TEXT("Additional root is the FBX armature wrapper"),Ref.GetBoneName(0),FName(TEXT("Zunderlauf_Rig")));
 auto* Walk=D->Clips.FindRef(EPokeMonsterCreatureClip::Walk).Get();
 if(Walk)
 {
  TArray<FVector> Previous;Previous.SetNum(2);
  for(int32 Frame=0;Frame<=8;++Frame)
  {
   TArray<FTransform> CS;CS.SetNum(Ref.GetNum());
   for(int32 I=0;I<CS.Num();++I){FTransform Local;Walk->GetBoneTransform(Local,FSkeletonPoseBoneIndex(I),FAnimExtractContext(Frame/30.,false),true);const int32 Parent=Ref.GetParentIndex(I);CS[I]=Parent<0?Local:Local*CS[Parent];}
   int32 SideIndex=0;
   for(const TCHAR* Side:{TEXT("L"),TEXT("R")})
   {
    const FVector Hip=CS[Ref.FindBoneIndex(FName(FString(TEXT("thigh_"))+Side))].GetTranslation();
    const FVector Knee=CS[Ref.FindBoneIndex(FName(FString(TEXT("shin_"))+Side))].GetTranslation();
    const FVector Foot=CS[Ref.FindBoneIndex(FName(FString(TEXT("foot_"))+Side))].GetTranslation();
    TestTrue(TEXT("Knee bends along real Unreal forward axis"),Knee.X>FMath::Min(Hip.X,Foot.X));
    TestTrue(TEXT("Foot remains in its sagittal track"),FMath::Abs(FMath::Abs(Foot.Y)-13.2f)<.15f);
    if(SideIndex==0&&Frame>0){const FVector Delta=Foot-Previous[SideIndex];TestTrue(TEXT("Imported stance cancels 35 cm/s forward motion"),FMath::Abs(Delta.X+35.f/30.f)<.05f);TestTrue(TEXT("Imported stance stays at the same ground height"),FMath::Abs(Delta.Z)<.05f);}
    Previous[SideIndex++]=Foot;
   }
  }
 }
 auto* Profile=LoadObject<UPokeMonsterEncounterProfile>(nullptr,TEXT("/Game/Data/Encounters/DA_Zunderlauf_Wild.DA_Zunderlauf_Wild"));
 if(TestNotNull(TEXT("Wild profile loads"),Profile)){FPokeMonsterCreatureInstance C;FRandomStream Random(3817);FPokeMonsterEncounterContext Context;TestTrue(TEXT("Existing encounter roller accepts species"),Profile->Roll(Context,Random,C));TestEqual(TEXT("Visible species matches encounter"),C.Species.Get(),S);}
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterZunderlaufPersistence,"PokeMonster.Creatures.Zunderlauf.CaptureHealSave",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterZunderlaufPersistence::RunTest(const FString&)
{
 auto* S=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));
 auto* W=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_TestWater.DA_TestWater"));
 auto* Move=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));
 auto* Device=LoadObject<UPokeMonsterCaptureDeviceData>(nullptr,TEXT("/Game/Data/Capture/DA_TestCaptureDevice.DA_TestCaptureDevice"));
 if(!S||!W||!Move||!Device){AddError(TEXT("Required creature fixtures missing"));return false;}
 auto Wild=FPokeMonsterCreatureInstance::CreateFromSpecies(S,5);Wild.AssignMove(0,Move);Wild.CurrentHP=1;
 auto Player=FPokeMonsterCreatureInstance::CreateFromSpecies(W,20);Player.AssignMove(0,Move);
 const float Chance=FPokeMonsterCaptureLibrary::CalculateChance(Wild.CurrentHP,Wild.GetMaxHP(),S->GetBaseCaptureRate(),Device->GetCaptureBonus());int32 Seed=0;
 for(;Seed<1000;++Seed){FRandomStream R(Seed);if(FPokeMonsterCaptureLibrary::CheckCapture(Chance,R.RandRange(0,9999)))break;}
 auto* Battle=NewObject<UPokeMonsterBattleSession>();TestTrue(TEXT("Existing wild battle initializes"),Battle->InitializeTeams({Player},{Wild},Seed,true).bSucceeded);
 FPokeMonsterBattleChoice Capture,Enemy;Capture.Type=EPokeMonsterBattleChoiceType::Capture;Capture.CaptureDevice=Device;Enemy.Index=0;
 TestTrue(TEXT("Capture executes"),Battle->ResolveTurn(Capture,Enemy).bSucceeded);TestEqual(TEXT("Existing capture rules capture Zunderlauf"),Battle->GetState().EndReason,EPokeMonsterBattleEndReason::Captured);
 auto C=Battle->GetState().CapturedCreature;TestEqual(TEXT("Capture preserves individual identity"),C.InstanceId,Wild.InstanceId);
 auto* GI=NewObject<UGameInstance>();auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI);auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI);
 TestTrue(TEXT("Existing party accepts captured creature"),E->RestorePersistentState({C},{},{TEXT("Dev_VisibleWild")}));
 TestTrue(TEXT("Existing healing restores creature"),E->RestorePlayerPartyAtRestPoint());
 auto* Snapshot=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI);if(!TestNotNull(TEXT("Snapshot captured"),Snapshot))return false;
 TestTrue(TEXT("Party cleared"),E->RestorePersistentState({},{},{}));TestTrue(TEXT("Same save schema restores Zunderlauf"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Snapshot,E,I));
 if(TestEqual(TEXT("One creature restored"),E->GetPlayerParty().Num(),1)){const auto& Restored=E->GetPlayerParty()[0];TestEqual(TEXT("Identity restored"),Restored.InstanceId,Wild.InstanceId);TestEqual(TEXT("Species restored"),Restored.Species.Get(),S);TestEqual(TEXT("Healed HP restored"),Restored.CurrentHP,Restored.GetMaxHP());TestEqual(TEXT("Move restored"),Restored.GetMoveSlots()[0].GetMove().Get(),Move);}
 return true;
}
#endif
