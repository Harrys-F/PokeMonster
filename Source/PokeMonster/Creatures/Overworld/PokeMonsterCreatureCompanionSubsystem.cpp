#include "PokeMonsterCreatureCompanionSubsystem.h"
#include "PokeMonsterCreatureRoamingComponent.h"
#include "../PokeMonsterCreaturePresentation.h"
#include "../PokeMonsterCreatureSpeciesData.h"
#include "../../Characters/PokeMonsterPlayerCharacter.h"
#include "../../Checkpoint/PokeMonsterCheckpointSubsystem.h"
#include "../../Encounter/PokeMonsterEncounterSubsystem.h"
#include "Components/CapsuleComponent.h"
#include "Animation/AnimSequence.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"

bool UPokeMonsterCreatureCompanionSubsystem::DoesSupportWorldType(EWorldType::Type Type) const
{
	return Type == EWorldType::Game || Type == EWorldType::PIE;
}
TStatId UPokeMonsterCreatureCompanionSubsystem::GetStatId() const
{
	RETURN_QUICK_DECLARE_CYCLE_STAT(PokeMonsterCreatureCompanion, STATGROUP_Tickables);
}
void UPokeMonsterCreatureCompanionSubsystem::ClearVisual()
{
	if (IsValid(Visual)) Visual->Destroy();
	Visual = nullptr; Movement = nullptr; CurrentSpecies = nullptr; CurrentId.Invalidate(); bPlaced = false;
}
void UPokeMonsterCreatureCompanionSubsystem::SetEnabled(bool Enabled)
{
	bEnabled = Enabled; if (!Enabled) ClearVisual();
}
void UPokeMonsterCreatureCompanionSubsystem::HideForEncounter()
{
	if (Visual) Visual->SetActorHiddenInGame(true);
	if (Movement) Movement->SetMovementPaused(true);
}
bool UPokeMonsterCreatureCompanionSubsystem::PlaceNearPlayer(AActor* Player)
{
	if (!Visual || !Movement || !Player) return false;
	const auto* Pawn = Cast<APokeMonsterPlayerCharacter>(Player);
	FVector Base = Player->GetActorLocation();
	if (Pawn) Base.Z -= Pawn->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
	for (float Radius : {155.f, 220.f}) for (float Angle : {180.f, 135.f, 225.f, 90.f, 270.f})
	{
		const float Radians = FMath::DegreesToRadians(Player->GetActorRotation().Yaw + Angle);
		FVector Ground;
		if (!Movement->ProjectWalkable(Base + FVector(FMath::Cos(Radians)*Radius,FMath::Sin(Radians)*Radius,0), Ground)) continue;
		Visual->SetActorLocation(Ground - FVector(0,0,Visual->Presentation->GroundOffsetCm));
		Visual->SetActorRotation(Player->GetActorRotation());
		bPlaced = true; return true;
	}
	return false;
}
void UPokeMonsterCreatureCompanionSubsystem::Tick(float Delta)
{
	Super::Tick(Delta); RefreshRemaining -= Delta;
	if (RefreshRemaining > 0 || !bEnabled || !GetWorld() || !GetWorld()->GetGameInstance()) return;
	RefreshRemaining = .2f;
	auto* Player = Cast<APokeMonsterPlayerCharacter>(UGameplayStatics::GetPlayerPawn(GetWorld(), 0));
	if (!Player) { ClearVisual(); return; }
	auto* GI = GetWorld()->GetGameInstance();
	auto* E = GI->GetSubsystem<UPokeMonsterEncounterSubsystem>();
	auto* Checkpoint = GI->GetSubsystem<UPokeMonsterCheckpointSubsystem>();
	if (!E) return;
	if (BoundEncounter != E)
	{
		if (BoundEncounter) BoundEncounter->OnEncounterStarted.RemoveDynamic(this, &UPokeMonsterCreatureCompanionSubsystem::HideForEncounter);
		BoundEncounter = E; E->OnEncounterStarted.AddUniqueDynamic(this, &UPokeMonsterCreatureCompanionSubsystem::HideForEncounter);
	}
	if (E->IsEncounterActive() || (Checkpoint && Checkpoint->IsReturningFromDefeat()))
	{ HideForEncounter(); return; }
	UPokeMonsterCreatureSpeciesData* Species = nullptr; FGuid Id;
	const auto& Team=E->GetPlayerParty();
	if(SelectPartyIndex(Team)==0)
	{
		Species=Team[0].Species.LoadSynchronous(); Id=Team[0].InstanceId;
	}
	if (!Species) { ClearVisual(); return; }
	if (!Visual)
	{
		FActorSpawnParameters Params; Params.Owner = Player; Params.ObjectFlags |= RF_Transient;
		Visual = GetWorld()->SpawnActor<APokeMonsterCreatureVisualActor>(Player->GetActorLocation(), FRotator::ZeroRotator, Params);
		if (!Visual) return;
		Visual->Tags.Add(TEXT("CreaturePartyCompanion")); Visual->SetActorHiddenInGame(true);
		Movement = NewObject<UPokeMonsterCreatureRoamingComponent>(Visual, TEXT("PartyRoaming"));
		Visual->AddInstanceComponent(Movement); Movement->RegisterComponent();
		Visual->AddTickPrerequisiteComponent(Movement);
	}
	if (Species != CurrentSpecies || Id != CurrentId)
	{
		if (!Visual->SetSpecies(Species)) { ClearVisual(); return; }
		if (auto* Sprint = Species->Overworld.SprintAnimation.LoadSynchronous())
		{
			auto* CompanionProfile = DuplicateObject<UPokeMonsterCreaturePresentationData>(Visual->Presentation, this);
			CompanionProfile->Clips.Add(EPokeMonsterCreatureClip::Run, Sprint);
			CompanionProfile->RunSpeed = Species->Overworld.SprintReferenceSpeed;
			if (CompanionProfile->GetValidationErrors().IsEmpty()) Visual->SetPresentation(CompanionProfile);
		}
		CurrentSpecies = Species; CurrentId = Id;
		Movement->Configure(Species, -Visual->Presentation->GroundOffsetCm, Species->Overworld.BodyRadius,
			FMath::Max(Visual->Presentation->ReferenceSizeCm * .5f, Species->Overworld.BodyRadius), Player, GetTypeHash(Id));
		bPlaced = false;
	}
	const FVector PlayerLocation = Player->GetActorLocation();
	const bool bTeleport = bHavePlayerLocation && FVector::Dist2D(PreviousPlayerLocation, PlayerLocation) > 800.f;
	PreviousPlayerLocation = PlayerLocation; bHavePlayerLocation = true;
	const bool bFar = FVector::Dist2D(Visual->GetActorLocation(), PlayerLocation) > Species->Overworld.MaximumActiveDistance;
	if (bFar && !bTeleport && Visual->Mesh->WasRecentlyRendered(.4f))
	{ Movement->SetMovementPaused(true); return; }
	if (bTeleport || bFar)
	{
		// Actual world relocation/return, never a routine visible sprint shortcut.
		Visual->SetActorHiddenInGame(true); bPlaced = false;
		Movement->SetMovementPaused(true);
	}
	if (!bPlaced && !PlaceNearPlayer(Player)) { Visual->SetActorHiddenInGame(true); return; }
	// Follow the existing room-only lighting contract; never alter the room or exterior lights.
	if (const auto* PlayerMesh = Player->FindComponentByClass<USkeletalMeshComponent>())
	{
		const FLightingChannels Channels = PlayerMesh->LightingChannels;
		Visual->Mesh->SetLightingChannels(Channels.bChannel0, Channels.bChannel1, false);
		Visual->Mesh->SetCastShadow(PlayerMesh->CastShadow);
		Visual->Flame->SetLightingChannels(Channels.bChannel0, Channels.bChannel1, false);
		for (const auto& Effect : Visual->EffectComponents) if (Effect)
			Effect->SetLightingChannels(Channels.bChannel0, Channels.bChannel1, false);
	}
	Movement->SetMovementPaused(Player->IsOverworldInputLocked());
	Visual->SetActorHiddenInGame(false);
}
void UPokeMonsterCreatureCompanionSubsystem::Deinitialize()
{
	if (BoundEncounter) BoundEncounter->OnEncounterStarted.RemoveDynamic(this, &UPokeMonsterCreatureCompanionSubsystem::HideForEncounter);
	ClearVisual(); BoundEncounter = nullptr; Super::Deinitialize();
}

int32 UPokeMonsterCreatureCompanionSubsystem::SelectPartyIndex(const TArray<FPokeMonsterCreatureInstance>& Team)
{
 if(Team.IsEmpty()||Team[0].CurrentHP<=0||!Team[0].IsValid())return INDEX_NONE;
 const auto* S=Team[0].Species.LoadSynchronous();
 const auto* Profile=S?S->GetVisuals().Presentation.LoadSynchronous():nullptr;
 return Profile&&Profile->GetValidationErrors().IsEmpty()?0:INDEX_NONE;
}
