#pragma once
#include "CoreMinimal.h"

/** Bounded visual contact, not a movement controller. One state per existing foot. */
struct FPokeMonsterFootContact
{
    FVector Anchor = FVector::ZeroVector;
    FQuat Rotation = FQuat::Identity;
    float Weight = 0.f;
    bool bWasStance = false, bLocked = false;

    void Reset() { *this = FPokeMonsterFootContact(); }
    void Update(const FVector& Foot, const FQuat& Facing, bool bStance, bool bValid, float Delta)
    {
        if (!bValid || Delta <= 0.f || Delta > .12f || Foot.ContainsNaN()) { Reset(); return; }
        if (bStance && !bWasStance)
        {
            Anchor = Foot; Rotation = Facing; bLocked = true;
        }
        // A tight pivot must release before it twists a knee or stretches a planted leg.
        if (bLocked && ((Foot - Anchor).Size2D() > 12.f || Rotation.AngularDistance(Facing) > FMath::DegreesToRadians(50.f)))
            bLocked = false;
        const float Target = bStance && bLocked ? 1.f : 0.f;
        Weight = FMath::FInterpConstantTo(Weight, Target, Delta, 14.f);
        bWasStance = bStance;
    }
    FVector Target(const FVector& Foot) const
    {
        return Foot + (Anchor - Foot).GetClampedToMaxSize(12.f) * Weight;
    }
};
