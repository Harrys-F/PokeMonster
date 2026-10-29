#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Misc/ScopeExit.h"
#include "../UI/PokeMonsterControllerInput.h"
#include "../UI/PokeMonsterOverworldWidget.h"
#include "../UI/PokeMonsterBattleWidget.h"
#include "../UI/PokeMonsterBattlePresenter.h"
#include "../Items/PokeMonsterItemData.h"
#include "../UI/PokeMonsterDialogueWidget.h"
#include "../Characters/PokeMonsterPlayerCharacter.h"
#include "InputMappingContext.h"
#include "InputAction.h"
#include "Components/Button.h"
#include "Components/TextBlock.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "UObject/StrongObjectPtr.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSwitchProInputTest,"PokeMonster.Input.SwitchPro.MappingsAndPersistentSprint",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterSwitchProInputTest::RunTest(const FString&)
{
 namespace Keys=PokeMonsterControllerInput;
 TestTrue(TEXT("Confirm and cancel cannot collide"),Keys::Confirm()!=Keys::Cancel());
 TestTrue(TEXT("Quick-menu key cannot interact"),Keys::QuickMenu()!=Keys::Confirm()&&Keys::QuickMenu()!=Keys::Cancel());
 UWorld* W=UWorld::CreateWorld(EWorldType::Game,false);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);
 ON_SCOPE_EXIT{GEngine->DestroyWorldContext(W);W->DestroyWorld(false);};
 auto* P=W->SpawnActor<APokeMonsterPlayerCharacter>();auto* M=P->GetCharacterMovement();M->SetMovementMode(MOVE_Walking);
 auto Mapped=[&](const UInputAction* A,FKey K){return P->DefaultMappingContext->GetMappings().ContainsByPredicate([&](const auto& X){return X.Action==A&&X.Key==K;});};
 TestTrue(TEXT("B uses the SAME world interaction action"),Mapped(P->InteractAction,Keys::Confirm()));
 TestTrue(TEXT("Keyboard retained"),Mapped(P->InteractAction,EKeys::E)&&Mapped(P->InteractAction,EKeys::Enter));
 TestTrue(TEXT("X and Tab open the same existing menu"),Mapped(P->MenuAction,Keys::QuickMenu())&&Mapped(P->MenuAction,EKeys::Tab));
 TestTrue(TEXT("Plus main menu"),Mapped(P->MainMenuAction,EKeys::Gamepad_Special_Right));
 TestTrue(TEXT("L3 toggles, Shift still holds"),Mapped(P->SprintToggleAction,EKeys::Gamepad_LeftThumbstick)&&Mapped(P->SprintHoldAction,EKeys::LeftShift));
 TestTrue(TEXT("Existing radial stick mapping retained"),Mapped(P->MoveAction,EKeys::Gamepad_Left2D));
 P->ToggleSprint(FInputActionValue(true));TestTrue(TEXT("L3 may select sprint while stationary"),P->IsSprintModeEnabled());TestFalse(TEXT("Stationary actor does not run"),P->IsSprinting());
 P->Move(FInputActionValue(FVector2D(1,1)));TestEqual(TEXT("Existing 315 sprint speed"),M->MaxWalkSpeed,315.f);
 P->StopMoving(FInputActionValue(FVector2D::ZeroVector));TestTrue(TEXT("Stop retains explicit toggle"),P->IsSprintModeEnabled());TestEqual(TEXT("Stop returns speed to 210"),M->MaxWalkSpeed,210.f);
 P->SetOverworldInputLocked(true);P->ToggleSprint(FInputActionValue(true));TestTrue(TEXT("Menu cannot change mode"),P->IsSprintModeEnabled());TestFalse(TEXT("Menu pauses actual sprint"),P->IsSprinting());
 P->SetOverworldInputLocked(false);P->Move(FInputActionValue(FVector2D(0,1)));TestTrue(TEXT("Mode resumes after UI or battle"),P->IsSprinting());
 P->ToggleSprint(FInputActionValue(true));TestFalse(TEXT("Next L3 switches off"),P->IsSprintModeEnabled());TestEqual(TEXT("Walk speed restored"),M->MaxWalkSpeed,210.f);
 return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPokeMonsterSwitchProWidgetTest,"PokeMonster.Input.SwitchPro.ContextsAndRepeatGuards",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FPokeMonsterSwitchProWidgetTest::RunTest(const FString&)
{
 namespace Keys=PokeMonsterControllerInput;
 auto Event=[](FKey K,bool Repeat=false){return FKeyEvent(K,FModifierKeysState(),0,Repeat,0,0);};
 TStrongObjectPtr<UPokeMonsterOverworldWidget> Widget(NewObject<UPokeMonsterOverworldWidget>());Widget->TakeWidget();
 FPokeMonsterOverworldView View;View.Team.AddDefaulted_GetRef().InstanceId=FGuid::NewGuid();View.Inventory.AddDefaulted_GetRef().Name=FText::FromString(TEXT("Trank"));View.Inventory.AddDefaulted_GetRef().Name=FText::FromString(TEXT("Fanggerät"));Widget->UpdateView(View);Widget->SetMenuOpen(true,EPokeMonsterOverworldMenuSection::Main);
 auto Press=[&](FKey K,bool Repeat=false){return Widget->NativeOnPreviewKeyDown(FGeometry(),Event(K,Repeat)).IsEventHandled();};
 TestTrue(TEXT("B opens selected main-menu entry exactly once"),Press(Keys::Confirm()));TestEqual(TEXT("Team opened"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Team);TestFalse(TEXT("Opening Team did not also select its first creature"),Widget->SelectedInstanceId.IsValid());
 Press(Keys::Confirm(),true);TestFalse(TEXT("Held B cannot select a new context"),Widget->SelectedInstanceId.IsValid());Press(Keys::Confirm());TestTrue(TEXT("Fresh B selects creature"),Widget->SelectedInstanceId.IsValid());
 Press(Keys::Cancel());TestFalse(TEXT("A cancels sorting before closing menu"),Widget->SelectedInstanceId.IsValid());TestTrue(TEXT("Cancel selection keeps menu"),Widget->IsMenuOpen());
 Press(EKeys::Gamepad_RightShoulder);TestEqual(TEXT("R reaches bag"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Inventory);Press(EKeys::Gamepad_RightShoulder,true);TestEqual(TEXT("Held R does not skip categories"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Inventory);
 Press(EKeys::Gamepad_DPad_Down);TestEqual(TEXT("Dpad selects second item"),Widget->FocusedInventorySlot,1);Press(Keys::Confirm());TestTrue(TEXT("Item inspection uses selected item"),Widget->SectionTitle->GetText().ToString().Contains(TEXT("Fanggerät")));
 Press(EKeys::Gamepad_LeftShoulder);TestEqual(TEXT("L reaches team"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Team);Press(EKeys::Gamepad_DPad_Down);TestEqual(TEXT("Dpad selects second team slot"),Widget->FocusedTeamSlot,1);
 TestTrue(TEXT("X is consumed inside menu"),Press(Keys::QuickMenu()));TestTrue(TEXT("X does not reopen/toggle existing menu"),Widget->IsMenuOpen());Press(EKeys::I);TestEqual(TEXT("Keyboard I retained"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Inventory);Press(EKeys::T);TestEqual(TEXT("Keyboard T retained"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Team);
 auto* Healing=LoadObject<UPokeMonsterItemData>(nullptr,TEXT("/Game/Data/Items/DA_TestHealingItem.DA_TestHealingItem"));
 if (!TestNotNull(TEXT("Existing healing item"),Healing)) return false;
 View.Inventory[0].Item=Healing;Widget->UpdateView(View);Widget->SetMenuOpen(true,EPokeMonsterOverworldMenuSection::Inventory);
 Press(Keys::Confirm());TestTrue(TEXT("B selects an existing overworld healing item"),Widget->PendingUseItem==Healing);TestEqual(TEXT("Existing team view is reused for item target"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Team);
 Press(Keys::Cancel());TestTrue(TEXT("A cancels item target without consuming anything"),Widget->PendingUseItem==nullptr);TestEqual(TEXT("A returns to bag"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Inventory);
 auto* Stone=LoadObject<UPokeMonsterItemData>(nullptr,TEXT("/Game/Data/Items/DA_TestEvolutionItem"));
 View.Inventory[0].Item=Stone;Widget->UpdateView(View);Widget->SetMenuOpen(true,EPokeMonsterOverworldMenuSection::Inventory);
 Press(Keys::Confirm());TestTrue(TEXT("B selects evolution item through existing bag"),Widget->PendingUseItem==Stone);
 TestEqual(TEXT("Same team selection, no second item menu"),Widget->GetSection(),EPokeMonsterOverworldMenuSection::Team);
 Press(Keys::Cancel());TestTrue(TEXT("A cancels stone selection before any use"),Widget->PendingUseItem==nullptr);
 TStrongObjectPtr<UPokeMonsterBattleWidget> Battle(NewObject<UPokeMonsterBattleWidget>());Battle->SetEncounterOverlay(true);Battle->TakeWidget();
 TStrongObjectPtr<UPokeMonsterBattlePresenter> Presenter(NewObject<UPokeMonsterBattlePresenter>());
 if (!TestTrue(TEXT("Existing battle data start real presenter"),Presenter->StartDemo())) return false;
 Battle->SetPresenter(Presenter.Get());Battle->SetBattleMenu(EPokeMonsterBattleMenu::Moves);
 TestEqual(TEXT("Battle enters actual moves page before A"),Battle->GetBattleMenu(),EPokeMonsterBattleMenu::Moves);Battle->NativeOnPreviewKeyDown(FGeometry(),Event(Keys::Cancel()));TestEqual(TEXT("A backs out of battle moves"),Battle->GetBattleMenu(),EPokeMonsterBattleMenu::Commands);TestTrue(TEXT("X cannot open world menu in battle"),Battle->NativeOnPreviewKeyDown(FGeometry(),Event(Keys::QuickMenu())).IsEventHandled());TestTrue(TEXT("Plus cannot leak to world in battle"),Battle->NativeOnPreviewKeyDown(FGeometry(),Event(EKeys::Gamepad_Special_Right)).IsEventHandled());
 TStrongObjectPtr<UPokeMonsterDialogueWidget> Dialogue(NewObject<UPokeMonsterDialogueWidget>());Dialogue->TakeWidget();TestTrue(TEXT("Dialogue consumes B before child Slate acceptance"),Dialogue->NativeOnPreviewKeyDown(FGeometry(),Event(Keys::Confirm())).IsEventHandled());TestTrue(TEXT("Dialogue consumes A before generic Bottom acceptance"),Dialogue->NativeOnPreviewKeyDown(FGeometry(),Event(Keys::Cancel())).IsEventHandled());
 Keys::ObserveKey(EKeys::E);
 return true;
}
#endif
