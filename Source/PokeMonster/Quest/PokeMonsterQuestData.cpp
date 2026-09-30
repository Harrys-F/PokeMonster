#include "PokeMonsterQuestData.h"

bool UPokeMonsterQuestData::IsConfigured() const
{
	if (InternalId.IsNone() || DisplayName.IsEmpty() || Objectives.IsEmpty()) return false;
	for (const FPokeMonsterQuestObjective& Objective : Objectives)
		if (Objective.TargetId.IsNone() || Objective.Description.IsEmpty()) return false;
	return true;
}
