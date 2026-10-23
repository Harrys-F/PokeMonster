/** Explicit transient integration fixture. Never edits move assets, levels, models or save slots. */
#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "HAL/IConsoleManager.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#if !UE_BUILD_SHIPPING
namespace PMMoveEffectsV4Review
{
FAutoConsoleCommandWithWorldAndArgs Review(TEXT("pm.MoveEffectsV4.Start"),TEXT("Explicit runtime technical fixture: classic|world stages|status|heal|drain|recoil|multi|confusion|protect|screen <existing species>. Stop PIE afterwards; never saves."),FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args,UWorld* W)
{
 if(Args.Num()!=3 || !W || !W->IsGameWorld() || !W->GetGameInstance() || (Args[0]!=TEXT("classic")&&Args[0]!=TEXT("world")))return;
 const TArray<FString> Names={TEXT("Zunderlauf"),TEXT("Schiggy"),TEXT("Bisasam"),TEXT("Pikachu"),TEXT("Myrapla"),TEXT("Enton"),TEXT("Machomei"),TEXT("Nebulak"),TEXT("Gengar"),TEXT("Glurak")};
 const TArray<FString> Cases={TEXT("stages"),TEXT("status"),TEXT("heal"),TEXT("drain"),TEXT("recoil"),TEXT("multi"),TEXT("confusion"),TEXT("protect"),TEXT("screen")};
 if(!Names.Contains(Args[2]) || !Cases.Contains(Args[1]))return;
 auto* E=W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>();auto* PC=W->GetFirstPlayerController();auto* P=PC?Cast<APokeMonsterPlayerCharacter>(PC->GetPawn()):nullptr;if(!E||!P||E->IsEncounterActive()||P->IsOverworldInputLocked())return;
 auto* Species=LoadObject<UPokeMonsterCreatureSpeciesData>(nullptr,*FString::Printf(TEXT("/Game/Data/Creatures/DA_%s.DA_%s"),*Args[2],*Args[2]));auto* Scratch=LoadObject<UPokeMonsterMoveData>(nullptr,TEXT("/Game/Data/Moves/DA_Scratch.DA_Scratch"));if(!Species||!Scratch)return;
 auto A=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,10),B=FPokeMonsterCreatureInstance::CreateFromSpecies(Species,10);
 for(auto* C:{&A,&B}){C->CurrentHP=C->CalculatedStats.MaxHP=500;C->CalculatedStats.Attack=C->CalculatedStats.SpecialAttack=C->CalculatedStats.Defense=C->CalculatedStats.SpecialDefense=100;C->CalculatedStats.Speed=50;C->AssignMove(0,Scratch);}A.CalculatedStats.Speed=100;
 auto* M=NewObject<UPokeMonsterMoveData>(E);M->InternalId=FName(*(TEXT("V4Technical_")+Args[1]));M->DisplayName=FText::FromString(TEXT("Effektprüfung · ")+Args[1]);M->Category=EPokeMonsterMoveCategory::Status;M->BasePower=0;M->MaxPP=20;
 FPokeMonsterMoveEffectComponent C;using K=EPokeMonsterEffectKind;const FString& Case=Args[1];
 if(Case==TEXT("stages")){C.Kind=K::Stage;C.Stat=EPokeMonsterBattleStat::SpecialAttack;C.Stages=2;C.bSelf=true;}
 if(Case==TEXT("status")){C.Kind=K::PrimaryStatus;C.Status=EPokeMonsterCreatureStatus::Paralysis;}
 if(Case==TEXT("heal")){C.Kind=K::Heal;C.bSelf=true;A.CurrentHP=100;}
 if(Case==TEXT("drain")){C.Kind=K::Drain;C.bSelf=true;M->Category=EPokeMonsterMoveCategory::Special;M->BasePower=40;A.CurrentHP=100;}
 if(Case==TEXT("recoil")){C.Kind=K::Recoil;C.bSelf=true;C.Denominator=4;M->Category=EPokeMonsterMoveCategory::Physical;M->BasePower=40;}
 if(Case==TEXT("multi")){C.Kind=K::MultiHit;C.HitWeights={3,3,1,1};M->Category=EPokeMonsterMoveCategory::Physical;M->BasePower=18;}
 if(Case==TEXT("confusion")){C.Kind=K::Confusion;C.MinTurns=C.MaxTurns=4;}
 if(Case==TEXT("protect")){C.Kind=K::Protect;C.bSelf=true;M->Priority=4;}
 if(Case==TEXT("screen")){C.Kind=K::Screen;C.bSelf=true;C.MaxTurns=5;}
 M->Effects={C};if(!M->IsConfigured()||!A.AssignMove(0,M))return;
 FPokeMonsterEncounterStartData D;D.EncounterId=FName(*(TEXT("ExplicitMoveEffectsV4_")+Case));D.Kind=EPokeMonsterEncounterKind::Wild;D.Source=EPokeMonsterEncounterSource::VisibleCreature;D.bAllowFlee=true;D.RandomSeed=71;D.EffectRules.bExtendedStatus=true;D.PlayerTeam={A};D.OpponentTeam={B};D.PresentationMode=Args[0]==TEXT("classic")?EPokeMonsterBattlePresentationMode::ClassicBattle:EPokeMonsterBattlePresentationMode::WorldBattle;
 if(E->StartEncounter(D,P))UE_LOG(LogTemp,Display,TEXT("MOVE_EFFECTS_V4_TECHNICAL_FIXTURE %s %s %s. No production move or save modified."),*Args[0],*Case,*Args[2]);
}));
}
#endif
