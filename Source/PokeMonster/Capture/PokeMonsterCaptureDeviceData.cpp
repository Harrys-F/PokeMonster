#include "PokeMonsterCaptureDeviceData.h"

FPrimaryAssetId UPokeMonsterCaptureDeviceData::GetPrimaryAssetId() const
{
	return FPrimaryAssetId(TEXT("CaptureDevice"), InternalId.IsNone() ? GetFName() : InternalId);
}

bool UPokeMonsterCaptureDeviceData::IsConfigured() const
{
	return !InternalId.IsNone() && !DisplayName.IsEmpty() && FMath::IsFinite(CaptureBonus) && CaptureBonus > 0.0f;
}
