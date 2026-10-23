#include "PokeMonsterEvolutionWidget.h"
#include "PokeMonsterOverworldPlayerController.h"
#include "PokeMonsterControllerInput.h"
#include "../Encounter/PokeMonsterClassicBattleScene.h"
#include "../Encounter/PokeMonsterEncounterSubsystem.h"
#include "../Creatures/PokeMonsterCreatureSpeciesData.h"
#include "../Creatures/PokeMonsterCreaturePresentation.h"
#include "../Moves/PokeMonsterMoveData.h"
#include "Blueprint/WidgetTree.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "Components/Button.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/AssetManager.h"
#include "Engine/GameInstance.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Styling/CoreStyle.h"
#include "Brushes/SlateRoundedBoxBrush.h"
namespace
{
 UPokeMonsterEncounterSubsystem* Service(const UUserWidget* W){return W->GetGameInstance()?W->GetGameInstance()->GetSubsystem<UPokeMonsterEncounterSubsystem>():nullptr;}
 const FPokeMonsterCreatureInstance* Individual(const UUserWidget* W,FGuid Id){auto* E=Service(W);return E?E->GetPlayerParty().FindByPredicate([Id](const auto& C){return C.InstanceId==Id;}):nullptr;}
 void Place(UCanvasPanel* C,UWidget* W,FAnchors A,FMargin Margin=FMargin(0)){auto* S=C->AddChildToCanvas(W);S->SetAnchors(A);S->SetOffsets(Margin);}
}
TSharedRef<SWidget> UPokeMonsterEvolutionWidget::RebuildWidget()
{
 if(!WidgetTree)Initialize();SetIsFocusable(true);
 if(WidgetTree->RootWidget)return Super::RebuildWidget();
 auto* Canvas=WidgetTree->ConstructWidget<UCanvasPanel>();WidgetTree->RootWidget=Canvas;
 auto* Back=WidgetTree->ConstructWidget<UImage>();Back->SetColorAndOpacity(FLinearColor(.025f,.065f,.05f,1));Place(Canvas,Back,FAnchors(0,0,1,1));
 auto Text=[&](int Size,FAnchors A){auto* T=WidgetTree->ConstructWidget<UTextBlock>();T->SetFont(FCoreStyle::GetDefaultFontStyle(TEXT("Regular"),Size));T->SetColorAndOpacity(FLinearColor(.94f,.88f,.65f));T->SetJustification(ETextJustify::Center);T->SetAutoWrapText(true);Place(Canvas,T,A);return T;};
 Title=Text(32,FAnchors(.05f,.025f,.95f,.11f));
 View=WidgetTree->ConstructWidget<UImage>();Place(Canvas,View,FAnchors(.04f,.13f,.96f,.75f));
 Flash=WidgetTree->ConstructWidget<UImage>();Flash->SetBrush(FSlateRoundedBoxBrush(FLinearColor(1,.92f,.65f),400.f));Flash->SetColorAndOpacity(FLinearColor(1,1,1,0));Flash->SetVisibility(ESlateVisibility::HitTestInvisible);Place(Canvas,Flash,FAnchors(.29f,.20f,.71f,.71f));
 for(int I=0;I<16;++I){auto* Dot=WidgetTree->ConstructWidget<UImage>();Dot->SetBrush(FSlateRoundedBoxBrush(FLinearColor(1,.76f,.25f),4.f));Dot->SetVisibility(ESlateVisibility::HitTestInvisible);Place(Canvas,Dot,FAnchors(.5f,.45f),FMargin(0,0,6,6));Dot->SetRenderOpacity(0);Motes.Add(Dot);}
 Details=Text(20,FAnchors(.08f,.77f,.92f,.88f));Hints=Text(18,FAnchors(.10f,.94f,.90f,.99f));
 auto Button=[&](FAnchors A,const TCHAR* Label,bool Yes){auto* B=WidgetTree->ConstructWidget<UButton>();FButtonStyle Style=B->GetStyle();Style.SetNormal(FSlateRoundedBoxBrush(FLinearColor(.10f,.22f,.15f),8.f));Style.SetHovered(FSlateRoundedBoxBrush(FLinearColor(.22f,.36f,.23f),8.f));Style.SetPressed(FSlateRoundedBoxBrush(FLinearColor(.31f,.43f,.22f),8.f));B->SetStyle(Style);auto* T=WidgetTree->ConstructWidget<UTextBlock>();T->SetFont(FCoreStyle::GetDefaultFontStyle(TEXT("Regular"),20));T->SetColorAndOpacity(FSlateColor(FLinearColor(.98f,.90f,.65f)));T->SetText(FText::FromString(Label));B->AddChild(T);Place(Canvas,B,A);if(Yes)B->OnClicked.AddDynamic(this,&UPokeMonsterEvolutionWidget::Confirm);else B->OnClicked.AddDynamic(this,&UPokeMonsterEvolutionWidget::Cancel);};
 Button(FAnchors(.24f,.88f,.49f,.93f),TEXT("Bestätigen · B / Enter"),true);Button(FAnchors(.51f,.88f,.76f,.93f),TEXT("Abbrechen · A / Esc"),false);
 return Super::RebuildWidget();
}
bool UPokeMonsterEvolutionWidget::BeginEvolution(APokeMonsterOverworldPlayerController* Owner,int32 Index,bool LearningOnly)
{
 OwnerController=Owner;auto* E=Service(this);if(!E||E->IsEncounterActive()||!E->GetPlayerParty().IsValidIndex(Index))return false;
 const auto& C=E->GetPlayerParty()[Index];CreatureId=C.InstanceId;Target=C.PendingEvolutionTarget;
 auto* Source=C.Species.LoadSynchronous();auto* Destination=LearningOnly?Source:Cast<UPokeMonsterCreatureSpeciesData>(UAssetManager::Get().GetPrimaryAssetPath(Target).TryLoad());
 if(!Source||!Destination)return false;
 FActorSpawnParameters Spawn;Spawn.ObjectFlags|=RF_Transient;Spawn.Owner=Owner;
 Stage=GetWorld()->SpawnActor<APokeMonsterClassicBattleScene>(FVector(0,0,-200000),FRotator::ZeroRotator,Spawn);if(!Stage)return false;
 Stage->Configure(Source,Destination,Owner->GetPawn(),EPokeMonsterBattleEnvironment::Meadow);
 if(!Stage->PlayerVisual||!Stage->OpponentVisual){Stage->Destroy();Stage=nullptr;return false;}
 for(auto* V:{Stage->PlayerVisual.Get(),Stage->OpponentVisual.Get()}){V->SetActorLocation(Stage->GetActorLocation()-FVector(0,0,V->Presentation->GroundOffsetCm));V->SetActorRotation(FRotator(0,135,0));}
 // Refit the two possible forms at ONE central position, without changing creature scale.
 const FVector Origin=Stage->GetActorLocation();const FVector Direction=FRotator(0,-45,0).Vector();
 float MaxHeight=0;for(auto* V:{Stage->PlayerVisual.Get(),Stage->OpponentVisual.Get()})MaxHeight=FMath::Max(MaxHeight,V->Presentation->ReferenceSizeCm);
 float Distance=FMath::Max(120.f,Stage->FramingDistance*.25f);
 for(int Attempt=0;Attempt<90;++Attempt)
 {
  Stage->Capture->SetWorldLocation(Origin-Direction*Distance+FVector(0,0,Distance*.33f));
  Stage->Capture->SetWorldRotation((Origin+FVector(0,0,MaxHeight*.48f)-Stage->Capture->GetComponentLocation()).Rotation());
  bool Fits=true;const float T=FMath::Tan(FMath::DegreesToRadians(Stage->Capture->FOVAngle*.5f));
  for(auto* V:{Stage->PlayerVisual.Get(),Stage->OpponentVisual.Get()})
  {auto Box=V->Mesh->CalcBounds(V->Mesh->GetComponentTransform()).GetBox();
   for(int Corner=0;Corner<8;++Corner){const FVector Point((Corner&1)?Box.Max.X:Box.Min.X,(Corner&2)?Box.Max.Y:Box.Min.Y,(Corner&4)?Box.Max.Z:Box.Min.Z);
    const FVector D=Point-Stage->Capture->GetComponentLocation();const float Z=FVector::DotProduct(D,Stage->Capture->GetForwardVector());
    if(Z<=1){Fits=false;continue;}const float X=.5f+.5f*FVector::DotProduct(D,Stage->Capture->GetRightVector())/(Z*T);const float Y=.5f-.5f*FVector::DotProduct(D,Stage->Capture->GetUpVector())/(Z*T/(2560.f/1440.f));Fits&=X>.10f&&X<.90f&&Y>.12f&&Y<.88f;}}
  if(Fits)break;Distance*=1.05f;
 }
 Stage->FramingDistance=Distance;
 Stage->OpponentVisual->SetActorHiddenInGame(true);Stage->Target->ResizeTarget(2560,1440);View->SetBrushResourceObject(Stage->Target);
 auto* Material=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Characters/Creatures/Shared/EvolutionV2/M_EvolutionGlow.M_EvolutionGlow"));
 if(Material)Glow=UMaterialInstanceDynamic::Create(Material,this);
 Phase=LearningOnly?TEXT("learning"):TEXT("offer");RefreshText();SetKeyboardFocus();return true;
}
void UPokeMonsterEvolutionWidget::RefreshText()
{
 const auto* C=Individual(this,CreatureId);if(!C||!Title)return;
 auto* S=C->Species.LoadSynchronous();const FString Name=S?S->GetDisplayName().ToString():TEXT("Pokémon");
 if(Phase==TEXT("offer")){Title->SetText(FText::FromString(Name+TEXT(" ist bereit zur Entwicklung")));Details->SetText(FText::FromString(TEXT("B / Enter beginnen · A / Esc abbrechen.\nNach einem späteren Levelaufstieg oder Kampfsieg ist ein neues Angebot möglich.")));}
 else if(Phase==TEXT("transform")){Title->SetText(FText::FromString(TEXT("Eine neue Kraft erwacht …")));Details->SetText(FText::FromString(TEXT("A / Esc kann die Entwicklung noch abbrechen.")));}
 else if(Phase==TEXT("complete")){Title->SetText(FText::FromString(Name+TEXT(" – Entwicklung abgeschlossen")));Details->SetText(FText::FromString(TEXT("Dein Pokémon hat eine neue Kraft gewonnen.\nBestätigen, um die Reise fortzusetzen.")));}
 else if(Phase==TEXT("cancelled")){Title->SetText(FText::FromString(TEXT("Entwicklung abgebrochen")));Details->SetText(FText::FromString(Name+TEXT(" bleibt unverändert. Später ist ein neues Angebot möglich.")));}
 else if(Phase==TEXT("error")){Title->SetText(FText::FromString(TEXT("Entwicklung nicht übernommen")));Details->SetText(FText::FromString(TEXT("Bedingungen, Zielmodell oder Speichern konnten nicht bestätigt werden.\nDie ursprüngliche Kreatur bleibt erhalten.")));}
 else if(Phase==TEXT("learning"))
 {
  if(C->PendingMoves.IsEmpty()){Finish();return;}
  const auto* Move=C->PendingMoves[0].LoadSynchronous();Title->SetText(FText::FromString(Name+TEXT(" kann ")+(Move?Move->DisplayName.ToString():TEXT("eine Attacke"))+TEXT(" erlernen")));
  FString Lines;for(int32 I=0;I<4;++I){const auto* M=C->GetMoveSlots()[I].GetMove().LoadSynchronous();Lines+=FString::Printf(TEXT("%s %d · %s%s"),I==Selection?TEXT("▶"):TEXT("  "),I+1,M?*M->DisplayName.ToString():TEXT("Freier Platz"),I==3?TEXT(""):TEXT("     "));}
  Details->SetText(FText::FromString(Lines+TEXT("\nSteuerkreuz / Pfeile wählen · B lernen/ersetzen · A ablehnen")));
 }
 Hints->SetText(FText::FromString(TEXT("B bestätigen · A abbrechen · Tastatur: Enter / Esc")));
}
void UPokeMonsterEvolutionWidget::Confirm()
{
 auto* E=Service(this);if(!E)return;
 if(Phase==TEXT("offer")){Phase=TEXT("transform");Elapsed=0;if(Glow)Stage->PlayerVisual->Mesh->SetOverlayMaterial(Glow);RefreshText();}
 else if(Phase==TEXT("complete"))StartLearning();
 else if(Phase==TEXT("learning")){if(E->ResolveEvolutionLearning(CreatureId,Selection))RefreshText();else{Phase=TEXT("error");RefreshText();}}
 else if(Phase!=TEXT("transform"))Finish();
}
void UPokeMonsterEvolutionWidget::Cancel()
{
 auto* E=Service(this);if(!E)return;
 if(Phase==TEXT("offer")||Phase==TEXT("transform"))
 {
  if(E->ResolveEvolution(CreatureId,Target,false)){Phase=TEXT("cancelled");Elapsed=0;if(const auto* C=Individual(this,CreatureId))if(Stage&&Stage->PlayerVisual)Stage->PlayerVisual->SetSpecies(C->Species.LoadSynchronous());if(Glow)Glow->SetScalarParameterValue(TEXT("Strength"),0);if(Stage&&Stage->PlayerVisual)Stage->PlayerVisual->Mesh->SetOverlayMaterial(nullptr);RefreshText();}else{Phase=TEXT("error");RefreshText();}
 }
 else if(Phase==TEXT("learning")){if(E->ResolveEvolutionLearning(CreatureId,INDEX_NONE))RefreshText();else{Phase=TEXT("error");RefreshText();}}
 else Finish();
}
void UPokeMonsterEvolutionWidget::StartLearning(){const auto* C=Individual(this,CreatureId);if(C&&!C->PendingMoves.IsEmpty()){Phase=TEXT("learning");Selection=0;RefreshText();}else Finish();}
void UPokeMonsterEvolutionWidget::NativeTick(const FGeometry& G,float Delta)
{
 Super::NativeTick(G,Delta);Elapsed+=Delta;
 const bool Transition=Phase==TEXT("transform");const float Pulse=Transition?FMath::Sin(FMath::Clamp(Elapsed/5.f,0.f,1.f)*PI):0.f;
 if(Glow)Glow->SetScalarParameterValue(TEXT("Strength"),Pulse*18.f);
 if(Flash)Flash->SetColorAndOpacity(FLinearColor(1,1,1,Pulse*Pulse*.45f));
 for(int I=0;I<Motes.Num();++I){float A=Elapsed*(.45f+I*.07f)+I*2.399f;Motes[I]->SetRenderTranslation(FVector2D(FMath::Cos(A)*(90+I*7),FMath::Sin(A*.73f)*(40+I*5)));Motes[I]->SetRenderOpacity(Pulse*.8f);}
 if(Transition&&Elapsed>=2.5f&&!bPreviewChanged)
 {
  auto* Destination=Cast<UPokeMonsterCreatureSpeciesData>(UAssetManager::Get().GetPrimaryAssetPath(Target).TryLoad());
  if(!Stage||!Stage->PlayerVisual||!Stage->PlayerVisual->SetSpecies(Destination)){Phase=TEXT("error");RefreshText();return;}
  bPreviewChanged=true;if(Glow)Stage->PlayerVisual->Mesh->SetOverlayMaterial(Glow);
 }
 if(Transition&&Elapsed>=5.f)
 {
  auto* E=Service(this);
  if(!E||!E->ResolveEvolution(CreatureId,Target,true))
  {if(const auto* C=Individual(this,CreatureId))Stage->PlayerVisual->SetSpecies(C->Species.LoadSynchronous());Phase=TEXT("error");RefreshText();return;}
  Stage->PlayerVisual->Mesh->SetOverlayMaterial(nullptr);Stage->PlayerVisual->PlayReaction(EPokeMonsterCreatureClip::Happy);Phase=TEXT("complete");RefreshText();
 }

}
FReply UPokeMonsterEvolutionWidget::NativeOnPreviewKeyDown(const FGeometry& G,const FKeyEvent& Event)
{
 const auto K=Event.GetKey();const bool Yes=K==PokeMonsterControllerInput::Confirm()||K==EKeys::Enter||K==EKeys::SpaceBar;const bool No=K==PokeMonsterControllerInput::Cancel()||K==EKeys::Escape;
 if(Yes||No){if(!Event.IsRepeat()){if(Yes)Confirm();else Cancel();}return FReply::Handled();}
 if(Phase==TEXT("learning"))
 {int D=(K==EKeys::Right||K==EKeys::Down||K==EKeys::Gamepad_DPad_Right||K==EKeys::Gamepad_DPad_Down)?1:(K==EKeys::Left||K==EKeys::Up||K==EKeys::Gamepad_DPad_Left||K==EKeys::Gamepad_DPad_Up)?-1:0;
  if(D){Selection=(Selection+D+4)%4;RefreshText();return FReply::Handled();}}
 return Super::NativeOnPreviewKeyDown(G,Event);
}
void UPokeMonsterEvolutionWidget::Finish(){if(Stage){Stage->Destroy();Stage=nullptr;}if(OwnerController)OwnerController->CloseEvolutionPresentation();}
void UPokeMonsterEvolutionWidget::NativeDestruct(){if(Stage){Stage->Destroy();Stage=nullptr;}Super::NativeDestruct();}
