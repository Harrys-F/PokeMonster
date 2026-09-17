#include "PokeMonsterTypeChart.h"

namespace
{
	using T = EPokeMonsterCreatureType;
	struct FTypeRow
	{
		T Attacking;
		TArray<T> Resists;
		TArray<T> Weak;
		TArray<T> Immune;
	};
	// Columns describe DEFENDING types. Unlisted pairs are neutral (1x).
	// Generation 2 rules, including Steel resisting Ghost and Dark.
	// Reference: https://github.com/pret/pokecrystal/blob/master/data/types/type_matchups.asm
	const FTypeRow Rows[] = {
		{T::Normal, {T::Rock, T::Steel}, {}, {T::Ghost}},
		{T::Fire, {T::Fire, T::Water, T::Rock, T::Dragon}, {T::Grass, T::Ice, T::Bug, T::Steel}, {}},
		{T::Water, {T::Water, T::Grass, T::Dragon}, {T::Fire, T::Ground, T::Rock}, {}},
		{T::Electric, {T::Electric, T::Grass, T::Dragon}, {T::Water, T::Flying}, {T::Ground}},
		{T::Grass, {T::Fire, T::Grass, T::Poison, T::Flying, T::Bug, T::Dragon, T::Steel}, {T::Water, T::Ground, T::Rock}, {}},
		{T::Ice, {T::Fire, T::Water, T::Ice, T::Steel}, {T::Grass, T::Ground, T::Flying, T::Dragon}, {}},
		{T::Fighting, {T::Poison, T::Flying, T::Psychic, T::Bug}, {T::Normal, T::Ice, T::Rock, T::Dark, T::Steel}, {T::Ghost}},
		{T::Poison, {T::Poison, T::Ground, T::Rock, T::Ghost}, {T::Grass}, {T::Steel}},
		{T::Ground, {T::Grass, T::Bug}, {T::Fire, T::Electric, T::Poison, T::Rock, T::Steel}, {T::Flying}},
		{T::Flying, {T::Electric, T::Rock, T::Steel}, {T::Grass, T::Fighting, T::Bug}, {}},
		{T::Psychic, {T::Psychic, T::Steel}, {T::Fighting, T::Poison}, {T::Dark}},
		{T::Bug, {T::Fire, T::Fighting, T::Poison, T::Flying, T::Ghost, T::Steel}, {T::Grass, T::Psychic, T::Dark}, {}},
		{T::Rock, {T::Fighting, T::Ground, T::Steel}, {T::Fire, T::Ice, T::Flying, T::Bug}, {}},
		{T::Ghost, {T::Dark, T::Steel}, {T::Psychic, T::Ghost}, {T::Normal}},
		{T::Dragon, {T::Steel}, {T::Dragon}, {}},
		{T::Dark, {T::Fighting, T::Dark, T::Steel}, {T::Psychic, T::Ghost}, {}},
		{T::Steel, {T::Fire, T::Water, T::Electric, T::Steel}, {T::Ice, T::Rock}, {}}
	};
	static_assert(UE_ARRAY_COUNT(Rows) == 17, "Keep all seventeen attacking types in the chart.");

	float AgainstSingle(const T Attack, const T Defense)
	{
		for (const FTypeRow& Row : Rows)
		{
			if (Row.Attacking != Attack) continue;
			if (Row.Immune.Contains(Defense)) return 0.0f;
			if (Row.Resists.Contains(Defense)) return 0.5f;
			if (Row.Weak.Contains(Defense)) return 2.0f;
			return 1.0f;
		}
		return -1.0f;
	}
}

bool PokeMonsterTypeChart::IsValidType(const EPokeMonsterCreatureType Type)
{
	return Type >= T::Normal && Type <= T::Steel;
}

float PokeMonsterTypeChart::GetMultiplier(const T Attack, const T Primary, const T Secondary)
{
	if (!IsValidType(Attack) || !IsValidType(Primary) || (Secondary != T::None && !IsValidType(Secondary))) return -1.0f;
	const float First = AgainstSingle(Attack, Primary);
	return Secondary == T::None || Secondary == Primary ? First : First * AgainstSingle(Attack, Secondary);
}
