// Explicit development-only Slate input simulation. Never reports a physical hardware test.
#include "HAL/IConsoleManager.h"
#include "Framework/Application/SlateApplication.h"
#include "Input/Events.h"
#include "InputCoreTypes.h"
#include "Engine/World.h"
#if !UE_BUILD_SHIPPING
namespace
{
 FAutoConsoleCommandWithWorldAndArgs Key(TEXT("pm.Input.Key"),
  TEXT("Simulated Slate key: <UE key name> <down|up|tap> [repeat]. Not hardware evidence."),
  FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args,UWorld* W)
 {
  if (!W || !W->IsGameWorld() || Args.Num()<2 || !FSlateApplication::IsInitialized()) return;
  const FKey K(*Args[0]); if (!K.IsValid()) return;
  FKeyEvent E(K,FModifierKeysState(),0,Args.Num()>2 && Args[2]==TEXT("repeat"),0,0);
  UE_LOG(LogTemp,Display,TEXT("PM_INPUT_SIMULATED key=%s phase=%s"),*K.ToString(),*Args[1]);
  if (Args[1]==TEXT("down") || Args[1]==TEXT("tap")) FSlateApplication::Get().ProcessKeyDownEvent(E);
  if (Args[1]==TEXT("up") || Args[1]==TEXT("tap")) FSlateApplication::Get().ProcessKeyUpEvent(E);
 }));
 FAutoConsoleCommandWithWorldAndArgs Axis(TEXT("pm.Input.Axis"),
  TEXT("Simulated Slate analog input: <UE axis name> <value>. Not hardware evidence."),
  FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args,UWorld* W)
 {
  if (!W || !W->IsGameWorld() || Args.Num()!=2 || !FSlateApplication::IsInitialized()) return;
  const FKey K(*Args[0]);if (!K.IsValid() || !K.IsAxis1D()) return;
  FAnalogInputEvent E(K,FModifierKeysState(),0,false,0,0,FMath::Clamp(FCString::Atof(*Args[1]),-1.f,1.f));
  FSlateApplication::Get().ProcessAnalogInputEvent(E);
 }));
}
#endif
