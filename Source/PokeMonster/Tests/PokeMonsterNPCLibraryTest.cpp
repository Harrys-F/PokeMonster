#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../Characters/PokeMonsterNPCPresentationData.h"
#include "../Characters/PokeMonsterNPCVisualActor.h"
#include "../Dialogue/PokeMonsterNPC.h"
#include "../Development/PokeMonsterNPCTestGround.h"
#include "Animation/AnimSequence.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/CapsuleComponent.h"
namespace
{
 const TCHAR* NPCIds[]={TEXT("Ranger"),TEXT("SilverLady"),TEXT("TreeBeing"),TEXT("ElvenScholar"),TEXT("Wizard"),TEXT("WhiteHairedWarrior"),TEXT("DwarfWarrior"),TEXT("CrouchedCreature"),TEXT("ElvenArcher"),TEXT("DarkArmored"),TEXT("HobbitBase")};
 UPokeMonsterNPCPresentationData* Profile(const TCHAR* Id){return LoadObject<UPokeMonsterNPCPresentationData>(nullptr,*FString::Printf(TEXT("/Game/Characters/NPCs/Library/Profiles/DA_NPC_%s"),Id));}
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNPCLibraryProfiles,"PokeMonster.NPC.Library.RealAssetsAndSkeletonContracts",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNPCLibraryProfiles::RunTest(const FString&)
{
 int32 Walking=0,Running=0;
 for(const TCHAR* Id:NPCIds)
 {
  auto* P=Profile(Id);if(!TestNotNull(Id,P))return false;
  for(const FString& E:P->GetValidationErrors())AddError(FString(Id)+TEXT(": ")+E);
  if(!P->Mesh||!P->Idle)return false;
  TestEqual(TEXT("Technical identity remains distinct"),P->TechnicalId,FName(Id));TestEqual(TEXT("Original material override available"),P->Materials.Num(),1);
  TestTrue(TEXT("Breathing, speaking and greeting available"),P->Idle&&P->Talk&&P->Greeting);Walking+=P->Walk!=nullptr;Running+=P->Run!=nullptr;
  for(auto* A:{P->Idle.Get(),P->Walk.Get(),P->Run.Get(),P->Talk.Get(),P->Greeting.Get()})
  {
   if(!A)continue;const auto& Ref=A->GetSkeleton()->GetReferenceSkeleton();
   for(int32 Frame=0;Frame<=30;++Frame)
   {
    const double Time=A->GetPlayLength()*Frame/30.;
    for(int32 Bone=0;Bone<Ref.GetNum();++Bone)
    {
     FTransform T;A->GetBoneTransform(T,FSkeletonPoseBoneIndex(Bone),FAnimExtractContext(Time,false),true);
     TestFalse(TEXT("Imported animation contains no NaN"),T.ContainsNaN());TestTrue(TEXT("Rotation stays normalized"),T.GetRotation().IsNormalized());
     if(Bone==0)TestTrue(TEXT("No root-motion displacement"),T.GetTranslation().Size()<.01);
    }
   }
  }
 }
 TestEqual(TEXT("Nine individually authored walking models"),Walking,9);TestEqual(TEXT("Six appropriate running models"),Running,6);
 for(const TCHAR* Id:{TEXT("WhiteHairedWarrior"),TEXT("DwarfWarrior"),TEXT("ElvenArcher")})
 {
  auto* Original=LoadObject<USkeletalMesh>(nullptr,*FString::Printf(TEXT("/Game/Characters/NPCs/%s/Meshes/SK_%s_NPC_V1"),Id,Id));
  TestTrue(TEXT("Previously suitable mesh reused instead of duplicated"),Profile(Id)->Mesh==Original);
 }
 TestFalse(TEXT("Rooted tree not misrepresented as walking"),Profile(TEXT("TreeBeing"))->Walk!=nullptr);
 TestFalse(TEXT("Unsafe robe locomotion not adopted"),Profile(TEXT("SilverLady"))->Walk!=nullptr);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNPCLibraryAtomic,"PokeMonster.NPC.Library.AtomicAppearanceAndInteractionIdentity",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNPCLibraryAtomic::RunTest(const FString&)
{
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* N=W->SpawnActor<APokeMonsterNPC>();auto* V=W->SpawnActor<APokeMonsterNPCVisualActor>();V->SourceActor=N;const FTransform Before=N->GetActorTransform();
 auto* P=Profile(TEXT("Ranger"));if(!TestNotNull(TEXT("Ranger profile"),P))return false;
 TestTrue(TEXT("Valid profile applied"),V->ApplyPresentation(P));auto* M=V->Visual->GetSkeletalMeshAsset();
 auto* Broken=NewObject<UPokeMonsterNPCPresentationData>();Broken->TechnicalId=TEXT("Invalid");Broken->Mesh=P->Mesh;Broken->Idle=Profile(TEXT("DwarfWarrior"))->Idle;
 TestFalse(TEXT("Mismatched skeleton rejected before changing presentation"),V->ApplyPresentation(Broken));TestTrue(TEXT("Previous working mesh retained"),V->Visual->GetSkeletalMeshAsset()==M);
 TestTrue(TEXT("Dialogue identity preserved"),V->SourceActor==N);TestTrue(TEXT("Source never moved"),N->GetActorTransform().Equals(Before));
 TestEqual(TEXT("Presentation adds no gameplay collider"),V->Visual->GetCollisionEnabled(),ECollisionEnabled::NoCollision);
 TestTrue(TEXT("Greeting request accepted"),V->PlayGreeting());TestEqual(TEXT("Exactly one request token"),V->GreetingSerial,1);
 TestTrue(TEXT("Healer original profile available"),V->ApplyPresentation(Profile(TEXT("SilverLady"))));
 TestTrue(TEXT("Original SilverLady material bound on component, source mesh untouched"),V->Visual->GetMaterial(0)==Profile(TEXT("SilverLady"))->Materials[0]);
 TestFalse(TEXT("No invalid leg solver on three-bone healer"),V->bEnableFootContacts);
 return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNPCLibraryGround,"PokeMonster.NPC.Library.OrdinaryPIEGroundAndIsolation",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FNPCLibraryGround::RunTest(const FString&)
{
 using G=UPokeMonsterNPCTestGround;
 TestTrue(TEXT("Normal VisualV2 PIE supported"),G::IsSupportedMap(TEXT("UEDPIE_0_Dev_TestMap_VisualV2"),EWorldType::PIE));
 TestFalse(TEXT("Biome excluded"),G::IsSupportedMap(TEXT("Dev_BiomeTestMap_V1"),EWorldType::PIE));TestFalse(TEXT("Westland excluded"),G::IsSupportedMap(TEXT("Dev_WestlandRegion"),EWorldType::PIE));TestFalse(TEXT("Regular build excluded"),G::IsSupportedMap(TEXT("Dev_TestMap_VisualV2"),EWorldType::Game));
 UWorld* W=UWorld::CreateWorld(EWorldType::PIE,false,FName(TEXT("Dev_TestMap_VisualV2")),CreatePackage(TEXT("/Temp/NPCLibrary/Dev_TestMap_VisualV2")));GEngine->CreateNewWorldContext(EWorldType::PIE).SetCurrentWorld(W);
 ON_SCOPE_EXIT{W->DestroyWorld(false);GEngine->DestroyWorldContext(W);};auto* Ground=W->GetSubsystem<G>();if(!TestNotNull(TEXT("Normal world subsystem"),Ground))return false;Ground->OnWorldBeginPlay(*W);
 TestEqual(TEXT("Eleven real NPCs"),Ground->Specimens.Num(),11);TestEqual(TEXT("Eleven real presentations"),Ground->Visuals.Num(),11);
 for(int32 I=0;I<Ground->Specimens.Num();++I)
 {
  const auto* N=Ground->Specimens[I].Get();TestTrue(TEXT("Transient, no saved gameplay identity"),N->HasAnyFlags(RF_Transient));TestTrue(TEXT("Existing NPC interaction class used"),N->IsA<APokeMonsterNPC>());TestFalse(TEXT("No final role or NPC service assigned"),N->Service!=EPokeMonsterNPCService::None);TestTrue(TEXT("Existing dialogue asset referenced"),!N->Dialogue.IsNull());
  const auto* C=CastChecked<UCapsuleComponent>(N->GetRootComponent());TestEqual(TEXT("Movement sweeps block real static obstacles"),C->GetCollisionResponseToChannel(ECC_WorldStatic),ECR_Block);
  for(int32 J=I+1;J<11;++J)TestTrue(TEXT("Independent test walking areas"),FVector::Dist2D(G::Station(I),G::Station(J))>1000.f);
 }
 if(!Ground->Specimens.IsEmpty())
 {
  FHitResult Hit;auto* N=Ground->Specimens[0].Get();FVector Destination=N->GetActorLocation();Destination.X=G::Center().X+3500.f;
  N->SetActorLocation(Destination,true,&Hit);
  TestTrue(TEXT("Real capsule sweep stops at development perimeter"),Hit.IsValidBlockingHit());
  TestTrue(TEXT("Character cannot fall through the test boundary"),N->GetActorLocation().X<G::Center().X+2490.f);
 }
 TestFalse(TEXT("No teleport without player / RAM guard"),Ground->Visit());TestFalse(TEXT("No fabricated return anchor"),Ground->ReturnToWorld());TestFalse(TEXT("Invalid mode rejected"),Ground->SetMode(TEXT("bad")));TestTrue(TEXT("Run mode available"),Ground->SetMode(TEXT("run")));return true;
}
#endif
