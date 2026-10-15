#include "PokeMonsterMeshyAnimInstance.h"
#include "PokeMonsterMeshyVisualComponent.h"
#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimSequence.h"
#include "Animation/AnimationPoseData.h"
#include "AnimationRuntime.h"
#include "BoneContainer.h"

namespace
{
struct FAccessorySpring
{
    float Angle = 0.f, Velocity = 0.f;
    void Step(float Target, float Delta, float Limit)
    {
        // Bounded substeps are stable under editor hitches; discard excess hitch time.
        float Remaining = FMath::Min(Delta, .1f);
        while (Remaining > 0.f)
        {
            const float Dt = FMath::Min(Remaining, 1.f / 120.f);
            Velocity += ((Target - Angle) * 100.f - Velocity * 14.f) * Dt;
            Angle += Velocity * Dt;
            const float Clamped = FMath::Clamp(Angle, -Limit, Limit);
            if (Clamped != Angle) Velocity = 0.f;
            Angle = Clamped; Remaining -= Dt;
        }
    }
};

struct FMeshyAnimationProxy : FAnimInstanceProxy
{
    explicit FMeshyAnimationProxy(UAnimInstance* Instance) : FAnimInstanceProxy(Instance) {}
    UAnimSequence* Idle = nullptr;
    UAnimSequence* Walk = nullptr;
    UAnimSequence* Run = nullptr;
    float RunAlpha = 0.f, RunRate = 0.f, RunTime = 0.f;
    float Alpha = 0.f, Rate = 0.f, IdleTime = 0.f, WalkTime = 0.f;
    float PreviousYaw = 0.f, PreviousSpeed = 0.f;
    bool bHavePrevious = false;
    FAccessorySpring CapePitch, CapeSwing, BagSwing;

    virtual void PreUpdate(UAnimInstance* Instance, float Delta) override
    {
        FAnimInstanceProxy::PreUpdate(Instance, Delta);
        const auto* Visual = Cast<UPokeMonsterMeshyVisualComponent>(Instance->GetSkelMeshComponent());
        if (!Visual) return;
        Idle = Visual->IdleAnimation; Walk = Visual->WalkAnimation; Run = Visual->RunAnimation;
        const float Speed = Visual->GetOwner() ? Visual->GetOwner()->GetVelocity().Size2D() : 0.f;
        Rate = Speed > 3.f ? FMath::Clamp(Speed / FMath::Max(Visual->AuthoredWalkSpeed, 1.f), .05f, 3.f) : 0.f;
        RunRate = Speed / FMath::Max(Visual->AuthoredRunSpeed, 1.f);
        const float RunTarget = Run ? FMath::Clamp((Speed - Visual->AuthoredWalkSpeed)
            / FMath::Max(Visual->AuthoredRunSpeed - Visual->AuthoredWalkSpeed, 1.f), 0.f, 1.f) : 0.f;
        RunAlpha = FMath::FInterpConstantTo(RunAlpha, RunTarget, Delta, 1.f / .18f);
        const float Target = Rate > 0.f ? 1.f : 0.f;
        Alpha = FMath::FInterpConstantTo(Alpha, Target, Delta, 1.f / .18f);
        const float Yaw = Visual->GetComponentRotation().Yaw;
        const float Dt = FMath::Max(Delta, .001f);
        const float Turn = bHavePrevious ? FMath::Clamp(FMath::FindDeltaAngleDegrees(PreviousYaw, Yaw) / Dt, -540.f, 540.f) : 0.f;
        const float Acceleration = bHavePrevious ? FMath::Clamp((Speed - PreviousSpeed) / Dt, -1000.f, 1000.f) : 0.f;
        CapePitch.Step(FMath::Clamp(Speed / 210.f * 3.f + Acceleration * .004f, -1.f, 7.f), Delta, 9.f);
        CapeSwing.Step(-Turn * .022f, Delta, 12.f);
        BagSwing.Step(Turn * .012f + Acceleration * .004f, Delta, 9.f);
        PreviousYaw = Yaw; PreviousSpeed = Speed; bHavePrevious = true;
    }
    virtual void Update(float Delta) override
    {
        if (Idle) IdleTime = FMath::Fmod(IdleTime + Delta, FMath::Max(Idle->GetPlayLength(), .01f));
        // Retain cycle phase at stop; resume continuously rather than restarting one foot.
        if (Walk && Rate > 0.f)
        {
            const float WalkLength = FMath::Max(Walk->GetPlayLength(), .01f);
            const float RunLength = Run ? FMath::Max(Run->GetPlayLength(), .01f) : WalkLength;
            // Both clips share left/right contact phase; changing speed cannot swap the feet.
            const float CyclesPerSecond = FMath::Lerp(Rate / WalkLength, RunRate / RunLength, RunAlpha);
            WalkTime = FMath::Fmod(WalkTime + Delta * CyclesPerSecond * WalkLength, WalkLength);
            RunTime = WalkTime / WalkLength * RunLength;
        }
    }
    virtual bool Evaluate(FPoseContext& Output) override
    {
        Output.ResetToRefPose();
        if (!Idle || !Walk) return true;
        FPoseContext IdlePose(Output), WalkPose(Output);
        IdlePose.ResetToRefPose(); WalkPose.ResetToRefPose();
        FAnimationPoseData A(IdlePose), B(WalkPose), Result(Output);
        Idle->GetAnimationPose(A, FAnimExtractContext(IdleTime, false));
        Walk->GetAnimationPose(B, FAnimExtractContext(WalkTime, false));
        if (Run && RunAlpha > 0.f)
        {
            FPoseContext RunPose(Output), LocomotionPose(Output);
            RunPose.ResetToRefPose(); LocomotionPose.ResetToRefPose();
            FAnimationPoseData C(RunPose), Locomotion(LocomotionPose);
            Run->GetAnimationPose(C, FAnimExtractContext(RunTime, false));
            FAnimationRuntime::BlendTwoPosesTogether(B, C, 1.f - RunAlpha, Locomotion);
            FAnimationRuntime::BlendTwoPosesTogether(A, Locomotion, 1.f - Alpha, Result);
        }
        else FAnimationRuntime::BlendTwoPosesTogether(A, B, 1.f - Alpha, Result);
        const FBoneContainer& Bones = Output.Pose.GetBoneContainer();
        auto Offset = [&](FName Name, float Pitch, float Swing)
        {
            const int32 SkeletonIndex = Bones.GetReferenceSkeleton().FindBoneIndex(Name);
            if (SkeletonIndex == INDEX_NONE) return;
            const FCompactPoseBoneIndex Index = Bones.MakeCompactPoseIndex(FMeshPoseBoneIndex(SkeletonIndex));
            if (Index.GetInt() == INDEX_NONE) return;
            // Convert component axes to this bone's parent space; do not move the strap/root.
            FQuat ParentRotation = FQuat::Identity;
            auto Parent = Bones.GetParentBoneIndex(Index);
            while (Parent.GetInt() != INDEX_NONE)
            {
                ParentRotation = Output.Pose[Parent].GetRotation() * ParentRotation;
                Parent = Bones.GetParentBoneIndex(Parent);
            }
            const FQuat ComponentDelta = FQuat(FVector::YAxisVector, FMath::DegreesToRadians(Pitch)) * FQuat(FVector::XAxisVector, FMath::DegreesToRadians(Swing));
            auto& Transform = Output.Pose[Index];
            Transform.SetRotation((ParentRotation.Inverse() * ComponentDelta * ParentRotation * Transform.GetRotation()).GetNormalized());
        };
        Offset(TEXT("cape_upper"), CapePitch.Angle, CapeSwing.Angle * .35f);
        Offset(TEXT("cape_lower"), CapePitch.Angle * .4f, CapeSwing.Angle * .45f);
        Offset(TEXT("cape_left"), CapePitch.Angle * .35f, CapeSwing.Angle * .5f);
        Offset(TEXT("cape_right"), CapePitch.Angle * .35f, CapeSwing.Angle * .5f);
        Offset(TEXT("bag"), BagSwing.Angle, BagSwing.Angle * .3f);
        Output.Pose.NormalizeRotations();
        return true;
    }
    virtual void PostUpdate(UAnimInstance* Instance) const override
    {
        FAnimInstanceProxy::PostUpdate(Instance);
        auto* View = CastChecked<UPokeMonsterMeshyAnimInstance>(Instance);
        View->WalkAlpha = Alpha; View->WalkPlayRate = Rate; View->WalkTime = WalkTime;
        View->RunAlpha = RunAlpha; View->RunPlayRate = RunRate;
        View->CapePitch = CapePitch.Angle; View->CapeSwing = CapeSwing.Angle; View->BagSwing = BagSwing.Angle;
    }
};
}
FAnimInstanceProxy* UPokeMonsterMeshyAnimInstance::CreateAnimInstanceProxy() { return new FMeshyAnimationProxy(this); }
void UPokeMonsterMeshyAnimInstance::DestroyAnimInstanceProxy(FAnimInstanceProxy* Proxy) { delete static_cast<FMeshyAnimationProxy*>(Proxy); }
