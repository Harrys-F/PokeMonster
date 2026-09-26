#include "PokeMonsterItemData.h"
#include "../Capture/PokeMonsterCaptureDeviceData.h"

FPrimaryAssetId UPokeMonsterItemData::GetPrimaryAssetId() const
{
	return FPrimaryAssetId(TEXT("Item"), InternalId.IsNone() ? GetFName() : InternalId);
}

UPokeMonsterCaptureDeviceData* UPokeMonsterItemData::GetCaptureDevice() const
{
	return CaptureDevice.LoadSynchronous();
}

bool UPokeMonsterItemData::IsConfigured() const
{
	if (InternalId.IsNone() || DisplayName.IsEmpty() || MaxStackSize < 1) return false;
	if (Category == EPokeMonsterItemCategory::Capture)
	{
		const auto* Device = GetCaptureDevice();
		return bUsableInBattle && IsValid(Device) && Device->IsConfigured();
	}
	if (Category == EPokeMonsterItemCategory::Healing) return HealAmount > 0;
	return true;
}
