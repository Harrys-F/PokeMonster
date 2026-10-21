#include "PokeMonsterCreaturePath.h"
#include "PokeMonsterCreatureOverworldSettings.h"
#include "Algo/Reverse.h"

bool FPokeMonsterCreatureOverworldSettings::IsValid() const
{
	const float Values[] = {RoamRadius, MinimumTravel, WalkSpeedOverride, RunSpeedOverride,
		PauseMinimum, PauseMaximum, TurnDegreesPerSecond, MaxStepHeight, BodyRadius,
		CompanionRoamRadius, RecallDistance, CompanionMaximumSpeed, MaximumActiveDistance, SprintReferenceSpeed};
	for (float V : Values) if (!FMath::IsFinite(V)) return false;
	return RoamRadius >= 150.f && RoamRadius <= 5000.f && MinimumTravel >= 50.f
		&& MinimumTravel < RoamRadius && WalkSpeedOverride >= 0.f && RunSpeedOverride >= 0.f
		&& PauseMinimum >= .25f && PauseMaximum >= PauseMinimum && TurnDegreesPerSecond > 0.f
		&& MaxStepHeight > 0.f && MaxStepHeight <= 50.f && BodyRadius > 0.f
		&& CompanionRoamRadius >= 100.f && RecallDistance > CompanionRoamRadius
		&& CompanionMaximumSpeed > 0.f && MaximumActiveDistance > RecallDistance
		&& (SprintAnimation.IsNull() ? SprintReferenceSpeed == 0.f : SprintReferenceSpeed > 0.f);
}

bool FPokeMonsterCreaturePath::Find(const FVector& Start, const FVector& Goal,
	TFunctionRef<bool(const FVector&, FVector&)> Project,
	TFunctionRef<bool(const FVector&, const FVector&)> CanCross,
	TArray<FVector>& Out, float CellSize, int32 MaximumExpanded)
{
	Out.Reset();
	if (Start.ContainsNaN() || Goal.ContainsNaN() || CellSize < 10.f || MaximumExpanded < 1
		|| FVector::Dist2D(Start, Goal) > 1250.f) return false;
	if (CanCross(Start, Goal)) { Out.Add(Goal); return true; }
	struct FNode { FVector Ground; FIntPoint Parent; float Cost = TNumericLimits<float>::Max(); };
	const FIntPoint Origin(0, 0);
	const FIntPoint Target(FMath::RoundToInt((Goal.X - Start.X) / CellSize),
		FMath::RoundToInt((Goal.Y - Start.Y) / CellSize));
	TMap<FIntPoint, FNode> Nodes;
	Nodes.Add(Origin, {Start, Origin, 0.f});
	TArray<FIntPoint> Open = {Origin};
	TSet<FIntPoint> Closed, Invalid;
	for (int32 Expanded = 0; !Open.IsEmpty() && Expanded < MaximumExpanded; ++Expanded)
	{
		int32 Best = 0; float Score = TNumericLimits<float>::Max();
		for (int32 I = 0; I < Open.Num(); ++I)
		{
			const auto& N = Nodes.FindChecked(Open[I]);
			const float S = N.Cost + FVector::Dist2D(N.Ground, Goal);
			if (S < Score) { Score = S; Best = I; }
		}
		const FIntPoint Key = Open[Best]; Open.RemoveAtSwap(Best);
		const FNode Current = Nodes.FindChecked(Key); Closed.Add(Key);
		if (Key == Target && CanCross(Current.Ground, Goal))
		{
			Out.Add(Goal); FIntPoint Trace = Key;
			while (Trace != Origin && Out.Num() <= MaximumExpanded)
			{
				const auto& N = Nodes.FindChecked(Trace);
				if (!N.Ground.Equals(Out.Last(), .1f)) Out.Add(N.Ground); Trace = N.Parent;
			}
			Algo::Reverse(Out); return true;
		}
		for (int32 X = -1; X <= 1; ++X) for (int32 Y = -1; Y <= 1; ++Y)
		{
			if (!X && !Y) continue;
			const FIntPoint Next = Key + FIntPoint(X, Y);
			if (Closed.Contains(Next) || Invalid.Contains(Next) || FMath::Abs(Next.X) > 20
				|| FMath::Abs(Next.Y) > 20) continue;
			FVector Ground;
			if (const auto* Cached = Nodes.Find(Next)) Ground = Cached->Ground;
			else if (!Project(Start + FVector(Next.X * CellSize, Next.Y * CellSize, 0), Ground))
			{ Invalid.Add(Next); continue; }
			if (!CanCross(Current.Ground, Ground)) continue;
			const float Cost = Current.Cost + FVector::Dist(Current.Ground, Ground);
			if (const auto* Old = Nodes.Find(Next); Old && Cost >= Old->Cost) continue;
			Nodes.Add(Next, {Ground, Key, Cost}); Open.AddUnique(Next);
		}
	}
	Out.Reset(); return false;
}
