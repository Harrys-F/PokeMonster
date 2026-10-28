// Copyright Epic Games, Inc. All Rights Reserved.

#include "PokeMonsterCreatureSpeciesData.h"

namespace PokeMonsterCreatureAssetTypes
{
	const FPrimaryAssetType CreatureSpecies(TEXT("CreatureSpecies"));
}

FPrimaryAssetId UPokeMonsterCreatureSpeciesData::GetPrimaryAssetId() const
{
	const FName AssetName = InternalId.IsNone() ? GetFName() : InternalId;
	return FPrimaryAssetId(PokeMonsterCreatureAssetTypes::CreatureSpecies, AssetName);
}

#include "../Moves/PokeMonsterMoveData.h"
TArray<UPokeMonsterMoveData*> UPokeMonsterCreatureSpeciesData::MovesForLevel(int32 Level)const
{
 TArray<FPokeMonsterLevelMove> Ordered=LevelUpMoves;Ordered.StableSort([](const auto& A,const auto& B){return A.Level<B.Level;});TArray<UPokeMonsterMoveData*> R;
 for(const auto& Entry:Ordered)if(Entry.Level>=1&&Entry.Level<=Level)if(auto* M=Entry.Move.LoadSynchronous())if(M->IsConfigured()){R.Remove(M);R.Add(M);}
 while(R.Num()>4)R.RemoveAt(0);return R;
}


#include "Engine/AssetManager.h"
#include "PokeMonsterCreaturePresentation.h"
TArray<UPokeMonsterCreatureSpeciesData*> UPokeMonsterCreatureSpeciesData::GetRegisteredPlayableSpecies()
{
 TArray<FPrimaryAssetId> Ids;
 auto& Manager=UAssetManager::Get();Manager.GetPrimaryAssetIdList(TEXT("CreatureSpecies"),Ids);
 TArray<UPokeMonsterCreatureSpeciesData*> Result;
 for(const auto& Id:Ids)
 {
  auto* Species=Cast<UPokeMonsterCreatureSpeciesData>(Manager.GetPrimaryAssetPath(Id).TryLoad());
  const auto* Presentation=Species?Species->GetVisuals().Presentation.LoadSynchronous():nullptr;
  if(Species && Species->GetPrimaryAssetId()==Id && Species->Overworld.IsValid()
   && Presentation && Presentation->GetValidationErrors().IsEmpty())Result.AddUnique(Species);
 }
 Result.Sort([](const auto& A,const auto& B)
 {
  if(A.GetPokedexNumber()!=B.GetPokedexNumber())return A.GetPokedexNumber()<B.GetPokedexNumber();
  return A.GetPrimaryAssetId().ToString()<B.GetPrimaryAssetId().ToString();
 });
 return Result;
}
