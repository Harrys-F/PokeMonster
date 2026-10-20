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
