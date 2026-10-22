#include "PokeMonsterControllerInput.h"
#include "Framework/Application/IInputProcessor.h"
#include "Framework/Application/SlateApplication.h"
#include "HAL/IConsoleManager.h"
#include "Engine/Engine.h"

namespace
{
 TAutoConsoleVariable<int32> Trace(TEXT("pm.Input.Trace"), 0,
  TEXT("Show raw gamepad keys in PIE and log. Observes only; never consumes input."));
 bool bGamepad = false;
 bool UsesAppleGC()
 {
  const auto* Variable = IConsoleManager::Get().FindConsoleVariable(TEXT("Slate.MacControllerPreferGCImpl"));
  return !Variable || Variable->GetInt() != 0;
 }
 class FObserver final : public IInputProcessor
 {
 public:
  virtual void Tick(float, FSlateApplication&, TSharedRef<ICursor>) override {}
  virtual bool HandleKeyDownEvent(FSlateApplication&, const FKeyEvent& Event) override
  {
   PokeMonsterControllerInput::ObserveKey(Event.GetKey());
   if (Trace.GetValueOnGameThread() && Event.GetKey().IsGamepadKey() && !Event.IsRepeat())
   {
    const FString Message = FString::Printf(TEXT("UE key: %s | Switch B=%s A=%s X=%s | backend=%s"),
     *Event.GetKey().ToString(), *PokeMonsterControllerInput::Confirm().ToString(),
     *PokeMonsterControllerInput::Cancel().ToString(), *PokeMonsterControllerInput::QuickMenu().ToString(),
     UsesAppleGC() ? TEXT("Apple GC") : TEXT("legacy HID"));
    UE_LOG(LogTemp, Display, TEXT("PM_CONTROLLER_INPUT %s"), *Message);
    if (GEngine) GEngine->AddOnScreenDebugMessage(0x53574954, 6.f, FColor::Cyan, Message);
   }
   return false;
  }
  virtual bool HandleAnalogInputEvent(FSlateApplication&, const FAnalogInputEvent& Event) override
  {
   if (Event.GetKey().IsGamepadKey() && FMath::Abs(Event.GetAnalogValue()) > .25f) bGamepad = true;
   return false;
  }
  virtual bool HandleMouseButtonDownEvent(FSlateApplication&, const FPointerEvent&) override
  { bGamepad = false; return false; }
 };
}
FKey PokeMonsterControllerInput::Confirm() { return UsesAppleGC() ? EKeys::Gamepad_FaceButton_Right : EKeys::Gamepad_FaceButton_Bottom; }
FKey PokeMonsterControllerInput::Cancel() { return UsesAppleGC() ? EKeys::Gamepad_FaceButton_Bottom : EKeys::Gamepad_FaceButton_Right; }
FKey PokeMonsterControllerInput::QuickMenu() { return UsesAppleGC() ? EKeys::Gamepad_FaceButton_Left : EKeys::Gamepad_FaceButton_Top; }
bool PokeMonsterControllerInput::IsGamepadActive() { return bGamepad; }
void PokeMonsterControllerInput::ObserveKey(FKey Key) { bGamepad = Key.IsGamepadKey(); }
TSharedRef<IInputProcessor> PokeMonsterControllerInput::MakeObserver() { return MakeShared<FObserver>(); }
