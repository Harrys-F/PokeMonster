#include "PokeMonsterItemData.h"
#include "../Creatures/PokeMonsterCreatureInstance.h"
#include "Engine/StaticMesh.h"
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
	if (Category == EPokeMonsterItemCategory::Healing)
 {
  switch(MedicineEffect) {
  case EPokeMonsterMedicineEffect::RestoreHP: return bFullRestore || HealAmount>0;
  case EPokeMonsterMedicineEffect::CureStatus: return bAllStatuses || (CuredStatus>0 && CuredStatus<=uint8(EPokeMonsterCreatureStatus::Freeze));
  case EPokeMonsterMedicineEffect::Revive: return true;
  case EPokeMonsterMedicineEffect::RestorePP: return bFullRestore || RestorePPAmount>0;
  default: return false;
  }
 }
	return true;
}

UStaticMesh* UPokeMonsterItemData::GetWorldMesh() const { return WorldMesh.LoadSynchronous(); }

bool UPokeMonsterItemData::ApplyMedicine(FPokeMonsterCreatureInstance& C,int32 MoveSlot) const
{
 if(!IsConfigured() || Category!=EPokeMonsterItemCategory::Healing || !C.IsValid()) return false;
 switch(MedicineEffect) {
 case EPokeMonsterMedicineEffect::RestoreHP:
  if(C.CurrentHP<=0 || C.CurrentHP>=C.GetMaxHP()) return false;
  C.CurrentHP=bFullRestore?C.GetMaxHP():int32(FMath::Min<int64>(C.GetMaxHP(),int64(C.CurrentHP)+HealAmount));return true;
 case EPokeMonsterMedicineEffect::CureStatus:
  if(C.CurrentHP<=0 || C.Status==EPokeMonsterCreatureStatus::None || (!bAllStatuses && uint8(C.Status)!=CuredStatus))return false;
  C.Status=EPokeMonsterCreatureStatus::None;C.StatusTurns=0;return true;
 case EPokeMonsterMedicineEffect::Revive:
  if(C.CurrentHP!=0)return false;
  C.CurrentHP=bFullRestore?C.GetMaxHP():FMath::Max(1,C.GetMaxHP()/2);
  C.Status=EPokeMonsterCreatureStatus::None;C.StatusTurns=0;return true;
 case EPokeMonsterMedicineEffect::RestorePP:
  if(C.CurrentHP<=0 || (!bAllMoves && !C.GetMoveSlots().IsValidIndex(MoveSlot)))return false;
  {bool Changed=false;for(int32 I=0;I<C.GetMoveSlots().Num();++I)
    if(bAllMoves || I==MoveSlot)Changed|=C.RestoreMovePP(I,RestorePPAmount,bFullRestore);
   return Changed;}
 default:return false;
 }
}
