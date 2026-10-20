#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Items/PokeMonsterInventorySubsystem.h"
#include "../Save/PokeMonsterSaveSubsystem.h"
#include "../Save/PokeMonsterSaveGame.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Animation/AnimSequence.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
namespace
{
UPokeMonsterCreatureSpeciesData* Species(){return LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,TEXT("/Game/Data/Creatures/DA_Zunderlauf.DA_Zunderlauf"));}
UPokeMonsterCreaturePresentationData* Profile(){auto* S=Species();return S?S->GetVisuals().Presentation.LoadSynchronous():nullptr;}
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCreatureImportContract,"PokeMonster.Creatures.Pipeline.ImportContract",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FCreatureImportContract::RunTest(const FString&)
{
 auto* Original=Profile();if(!TestNotNull(TEXT("V1 presentation retained"),Original))return false;
 TestTrue(TEXT("Unmodified V1 passes new contract"),Original->GetValidationErrors().IsEmpty());
 auto* D=DuplicateObject<UPokeMonsterCreaturePresentationData>(Original,GetTransientPackage());
 D->Clips.Remove(EPokeMonsterCreatureClip::Idle);TestFalse(TEXT("Missing idle rejected"),D->GetValidationErrors().IsEmpty());
 D->Clips=Original->Clips;D->Clips.Add(EPokeMonsterCreatureClip::Walk,nullptr);TestFalse(TEXT("Null clip rejected"),D->GetValidationErrors().IsEmpty());
 D->Clips=Original->Clips;auto* Foreign=NewObject<UAnimSequence>();D->Clips.Add(EPokeMonsterCreatureClip::Walk,Foreign);TestFalse(TEXT("Wrong skeleton/empty sequence rejected"),D->GetValidationErrors().IsEmpty());
 D->Clips=Original->Clips;auto* Root=NewObject<UAnimSequence>();Root->SetSkeleton(Original->Mesh->GetSkeleton());Root->bEnableRootMotion=true;D->Clips.Add(EPokeMonsterCreatureClip::Walk,Root);TestTrue(TEXT("Root extraction explicitly rejected"),D->GetValidationErrors().Contains(TEXT("Presentation requires in-place animation, not root-motion extraction")));
 D->Clips=Original->Clips;D->RunSpeed=1;TestFalse(TEXT("Inverted speed contract rejected"),D->GetValidationErrors().IsEmpty());D->RunSpeed=Original->RunSpeed;
 D->FlameBone=TEXT("missing_anchor");TestFalse(TEXT("Missing tail anchor rejected"),D->GetValidationErrors().IsEmpty());D->FlameBone=Original->FlameBone;
 FPokeMonsterCreatureEffectAnchor A;A.Id=TEXT("Aura");A.Socket=Original->FlameBone;A.Mesh=Original->TailFlame;
 D->TailFlame=nullptr;D->EffectAnchors={A};TestTrue(TEXT("General anchor accepted without legacy flame"),D->GetValidationErrors().IsEmpty());
 D->EffectAnchors.Add(A);TestFalse(TEXT("Duplicate effect IDs rejected"),D->GetValidationErrors().IsEmpty());D->EffectAnchors.SetNum(1);
 D->EffectAnchors[0].Offset.SetScale3D(FVector(-1));TestFalse(TEXT("Mirrored effect scale rejected"),D->GetValidationErrors().IsEmpty());D->EffectAnchors.Reset();
 // A different existing rig is accepted with its own clip; no Zunderlauf bone convention required.
 D->Mesh=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1.SK_Ranger_NPC_V1"));
 auto* Idle=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Idle_V1.A_Ranger_Idle_V1"));
 if(!TestNotNull(TEXT("Independent existing rig fixture"),D->Mesh.Get())||!TestNotNull(TEXT("Independent idle fixture"),Idle))return false;
 D->Clips.Empty();D->Clips.Add(EPokeMonsterCreatureClip::Idle,Idle);D->RigFamily=EPokeMonsterCreatureRigFamily::Custom;
 TestTrue(TEXT("Different skeleton and idle-only presentation accepted"),D->GetValidationErrors().IsEmpty());
 TestTrue(TEXT("No original asset edited"),Original->GetValidationErrors().IsEmpty());return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCreatureVisualSwap,"PokeMonster.Creatures.Pipeline.AtomicVisualSwap",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FCreatureVisualSwap::RunTest(const FString&)
{
 auto* S=Species();auto* D=Profile();if(!S||!D){AddError(TEXT("Missing Zunderlauf fixtures"));return false;}
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* V=W->SpawnActor<APokeMonsterCreatureVisualActor>();TestTrue(TEXT("V1 visual binds"),V->SetSpecies(S));auto* Before=V->Mesh->GetSkeletalMeshAsset();
 auto* Copy=DuplicateObject<UPokeMonsterCreatureSpeciesData>(S,GetTransientPackage());auto* Candidate=DuplicateObject<UPokeMonsterCreaturePresentationData>(D,GetTransientPackage());
 const_cast<FPokeMonsterCreatureVisuals&>(Copy->GetVisuals()).Presentation=Candidate;
 Candidate->Clips.Remove(EPokeMonsterCreatureClip::Idle);TestFalse(TEXT("Invalid candidate rejected"),V->SetSpecies(Copy));TestEqual(TEXT("Working visual preserved on failure"),V->Mesh->GetSkeletalMeshAsset(),Before);
 Candidate->Clips=D->Clips;FPokeMonsterCreatureEffectAnchor A;A.Id=TEXT("TailTip");A.Socket=D->FlameBone;A.Mesh=D->TailFlame;A.Material=D->FlameMaterial;A.Offset.SetTranslation(FVector(0,0,2));A.bWorldUpright=true;
 Candidate->TailFlame=nullptr;Candidate->EffectAnchors={A};TestTrue(TEXT("Valid independent candidate binds"),V->SetSpecies(Copy));
 if(TestEqual(TEXT("One general effect created"),V->EffectComponents.Num(),1))
 {
  auto* C=V->EffectComponents[0].Get();TestEqual(TEXT("Anchored to candidate socket"),C->GetAttachSocketName(),A.Socket);TestEqual(TEXT("Effect has no gameplay collision"),C->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
  TestTrue(TEXT("Effect is registered"),C->IsRegistered());V->Mesh->RefreshBoneTransforms();
  const FVector Expected=V->Mesh->GetSocketTransform(A.Socket).TransformPosition(A.Offset.GetTranslation());TestTrue(TEXT("Offset follows actual socket"),C->GetComponentLocation().Equals(Expected,.01f));
 }
 TestFalse(TEXT("Legacy flame disabled for general binding"),V->Flame->IsVisible());
 TestTrue(TEXT("Original profile can be rebound"),V->SetSpecies(S));TestTrue(TEXT("Replacement effects cleaned up"),V->EffectComponents.IsEmpty());TestTrue(TEXT("Original tail flame retained"),V->Flame->IsVisible());
 // Exercise an actual skeleton exchange, not merely validation of a different profile.
 Candidate->EffectAnchors.Reset();Candidate->Mesh=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1.SK_Ranger_NPC_V1"));Candidate->Clips.Empty();
 Candidate->Clips.Add(EPokeMonsterCreatureClip::Idle,LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Idle_V1.A_Ranger_Idle_V1")));
 TestTrue(TEXT("Different existing skeleton can actually bind"),V->SetSpecies(Copy));TestEqual(TEXT("Own skeleton preserved"),V->Mesh->GetSkeletalMeshAsset(),Candidate->Mesh.Get());TestFalse(TEXT("No tail is required for another rig"),V->Flame->IsVisible());
 V->Mesh->TickAnimation(.1f,false);V->Mesh->RefreshBoneTransforms();TestNotNull(TEXT("Shared proxy supports independent rig"),V->Mesh->GetAnimInstance());
 TestTrue(TEXT("V1 remains available after different-skeleton exchange"),V->SetSpecies(S));
 TestEqual(TEXT("Creature visual has no collider"),V->Mesh->GetCollisionEnabled(),ECollisionEnabled::NoCollision);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCreatureSwapPersistence,"PokeMonster.Creatures.Pipeline.SaveSurvivesPresentationSwap",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FCreatureSwapPersistence::RunTest(const FString&)
{
 auto* S=Species();auto* D=Profile();auto* Move=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_TestNormalPhysical.DA_TestNormalPhysical"));if(!S||!D||!Move)return false;
 auto C=FPokeMonsterCreatureInstance::CreateFromSpecies(S,8);C.AssignMove(0,Move);C.ConsumeMovePP(0,2);C.CurrentHP=3;const FGuid Id=C.InstanceId;const int32 PP=C.GetMoveSlots()[0].GetCurrentPP();
 auto* GI=NewObject<UGameInstance>();auto* E=NewObject<UPokeMonsterEncounterSubsystem>(GI);auto* I=NewObject<UPokeMonsterInventorySubsystem>(GI);
 TestTrue(TEXT("Party fixture restored"),E->RestorePersistentState({C},{TEXT("Liora")},{TEXT("Dev_VisibleWild")}));auto* Save=UPokeMonsterSaveSubsystem::CaptureSnapshot(E,I,GI);if(!TestNotNull(TEXT("Snapshot"),Save))return false;
 auto& Visuals=const_cast<FPokeMonsterCreatureVisuals&>(S->GetVisuals());const auto Old=Visuals.Presentation;ON_SCOPE_EXIT{Visuals.Presentation=Old;};
 auto* Candidate=DuplicateObject<UPokeMonsterCreaturePresentationData>(D,GetTransientPackage());Candidate->RigFamily=EPokeMonsterCreatureRigFamily::Biped;Visuals.Presentation=Candidate;
 TestTrue(TEXT("Party cleared"),E->RestorePersistentState({},{},{}));TestTrue(TEXT("Same species identity restores after visual exchange"),UPokeMonsterSaveSubsystem::RestoreSnapshot(Save,E,I));
 if(TestEqual(TEXT("One creature"),E->GetPlayerParty().Num(),1)){const auto& R=E->GetPlayerParty()[0];TestEqual(TEXT("Individual identity"),R.InstanceId,Id);TestEqual(TEXT("Species asset identity"),R.Species.Get(),S);TestEqual(TEXT("HP unchanged by visuals"),R.CurrentHP,3);TestEqual(TEXT("PP unchanged by visuals"),R.GetMoveSlots()[0].GetCurrentPP(),PP);TestEqual(TEXT("Level unchanged"),R.Level,8);}
 TestTrue(TEXT("Encounter progress preserved"),E->IsEncounterCompleted(TEXT("Dev_VisibleWild")));TestTrue(TEXT("Trainer progress preserved"),E->IsTrainerDefeated(TEXT("Liora")));TestTrue(TEXT("Existing heal still works"),E->RestorePlayerPartyAtRestPoint());
 TestEqual(TEXT("No save version migration"),Save->SaveVersion,UPokeMonsterSaveGame::CurrentVersion);return true;
}
#endif
