#include "PokeMonsterEvolutionWidget.h"
#include "PokeMonsterEvolutionPresentation.h"
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
#include "Components/ScaleBox.h"
#include "Components/ScaleBoxSlot.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Rendering/DrawElements.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/AssetManager.h"
#include "Engine/GameInstance.h"
#include "Engine/GameViewportClient.h"
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
 // Preserve the capture's 16:9 aspect; the former stretched image flattened both models.
 auto MakeView=[&](){auto* Box=WidgetTree->ConstructWidget<UScaleBox>();Box->SetStretch(EStretch::ScaleToFit);Place(Canvas,Box,FAnchors(.04f,.10f,.96f,.80f));auto* Image=WidgetTree->ConstructWidget<UImage>();auto* Slot=Cast<UScaleBoxSlot>(Box->AddChild(Image));Slot->SetHorizontalAlignment(HAlign_Center);Slot->SetVerticalAlignment(VAlign_Center);FSlateBrush Brush=Image->GetBrush();Brush.SetImageSize(FVector2D(2560,1440));Image->SetBrush(Brush);return Image;};
 View=MakeView();DestinationView=MakeView();DestinationView->SetRenderOpacity(0);
 Flash=WidgetTree->ConstructWidget<UImage>();Flash->SetColorAndOpacity(FLinearColor(1,1,1,0));Flash->SetVisibility(ESlateVisibility::HitTestInvisible);Place(Canvas,Flash,FAnchors(.04f,.10f,.96f,.80f));
 for(int I=0;I<16;++I){auto* Dot=WidgetTree->ConstructWidget<UImage>();Dot->SetBrush(FSlateRoundedBoxBrush(FLinearColor(1,.76f,.25f),4.f));Dot->SetVisibility(ESlateVisibility::HitTestInvisible);Place(Canvas,Dot,FAnchors(.5f,.45f),FMargin(0,0,6,6));Dot->SetRenderOpacity(0);Motes.Add(Dot);}
 Details=Text(20,FAnchors(.08f,.81f,.92f,.875f));Hints=Text(18,FAnchors(.10f,.94f,.90f,.99f));
 auto Button=[&](FAnchors A,const TCHAR* Label,bool Yes){auto* B=WidgetTree->ConstructWidget<UButton>();FButtonStyle Style=B->GetStyle();Style.SetNormal(FSlateRoundedBoxBrush(FLinearColor(.10f,.22f,.15f),8.f));Style.SetHovered(FSlateRoundedBoxBrush(FLinearColor(.22f,.36f,.23f),8.f));Style.SetPressed(FSlateRoundedBoxBrush(FLinearColor(.31f,.43f,.22f),8.f));B->SetStyle(Style);auto* T=WidgetTree->ConstructWidget<UTextBlock>();T->SetFont(FCoreStyle::GetDefaultFontStyle(TEXT("Regular"),20));T->SetColorAndOpacity(FSlateColor(FLinearColor(.98f,.90f,.65f)));T->SetText(FText::FromString(Label));B->AddChild(T);Place(Canvas,B,A);if(Yes){ConfirmButton=B;ConfirmLabel=T;}else{CancelButton=B;CancelLabel=T;}if(Yes)B->OnClicked.AddDynamic(this,&UPokeMonsterEvolutionWidget::Confirm);else B->OnClicked.AddDynamic(this,&UPokeMonsterEvolutionWidget::Cancel);};
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
 SourceName=Source->GetDisplayName().ToString();DestinationName=Destination->GetDisplayName().ToString();
 // Use the existing transient stage, with two separately captured forms for a true dissolve.
 // Neither visual's physical size, species data nor the world camera is changed.
 for(const auto& Dressing:Stage->Dressing)if(Dressing)Dressing->SetVisibility(false);
 Stage->Target->ResizeTarget(2560,1440);
 auto Fit=[&](APokeMonsterCreatureVisualActor* V,USceneCaptureComponent2D* Capture)
 {
  // Project oriented mesh bounds directly. A second world-axis box artificially widened
  // the 135-degree models and left especially Glurak much too distant.
  TArray<FVector> Points;
  auto AddBounds=[&](const FBox& Box,const FTransform& Transform)
  {
   for(int I=0;I<8;++I)Points.Add(Transform.TransformPosition(FVector(I&1?Box.Max.X:Box.Min.X,I&2?Box.Max.Y:Box.Min.Y,I&4?Box.Max.Z:Box.Min.Z)));
  };
  const float Margin=FMath::Max(3.f,V->Presentation->ReferenceSizeCm*.04f);
  AddBounds(V->Presentation->Mesh->GetBounds().GetBox().ExpandBy(Margin),V->Mesh->GetComponentTransform());
  // Effect anchors, unlike legacy TailFlame, are used by the current Meshy models.
  for(const auto& Effect:V->EffectComponents)if(Effect&&Effect->GetStaticMesh())AddBounds(Effect->GetStaticMesh()->GetBounds().GetBox(),Effect->GetComponentTransform());
  if(V->Flame&&V->Flame->GetStaticMesh())AddBounds(V->Flame->GetStaticMesh()->GetBounds().GetBox(),V->Flame->GetComponentTransform());
  const auto Frame=PokeMonsterEvolutionPresentation::FitPoints(Points);
  Capture->SetWorldLocationAndRotation(Frame.Location,Frame.Rotation);Capture->FOVAngle=35.f;
  return Frame.Distance;
 };
 Stage->FramingDistance=Fit(Stage->PlayerVisual,Stage->Capture);View->SetBrushResourceObject(Stage->Target);
 DestinationTarget=NewObject<UTextureRenderTarget2D>(this,NAME_None,RF_Transient);DestinationTarget->RenderTargetFormat=RTF_RGBA8;DestinationTarget->InitAutoFormat(2560,1440);
 DestinationCapture=NewObject<USceneCaptureComponent2D>(Stage,NAME_None,RF_Transient);Stage->AddInstanceComponent(DestinationCapture);DestinationCapture->SetupAttachment(Stage->GetRootComponent());DestinationCapture->RegisterComponent();
 DestinationCapture->PrimitiveRenderMode=ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList;DestinationCapture->CaptureSource=Stage->Capture->CaptureSource;DestinationCapture->TextureTarget=DestinationTarget;DestinationCapture->bCaptureEveryFrame=true;DestinationCapture->bAlwaysPersistRenderingState=true;DestinationCapture->PostProcessBlendWeight=Stage->Capture->PostProcessBlendWeight;
 DestinationCapture->ShowOnlyActors=Stage->Capture->ShowOnlyActors;DestinationCapture->ShowOnlyActors.Remove(Stage->PlayerVisual);Stage->Capture->ShowOnlyActors.Remove(Stage->OpponentVisual);
 Fit(Stage->OpponentVisual,DestinationCapture);DestinationView->SetBrushResourceObject(DestinationTarget);
 Stage->OpponentVisual->SetActorHiddenInGame(false);
 auto* Material=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Characters/Creatures/Shared/EvolutionV2/M_EvolutionGlow.M_EvolutionGlow"));
 if(Material)Glow=UMaterialInstanceDynamic::Create(Material,this);
 Phase=LearningOnly?TEXT("learning"):TEXT("offer");Elapsed=0;bHappyPlayed=false;RefreshText();SetKeyboardFocus();
 // This opaque full-screen widget covers the world. Keep gameplay ticking, but render only
 // its two capture-only forms; restore the prior viewport flag on every exit path.
 CoveredViewport=GetGameInstance()->GetGameViewportClient();
 if(CoveredViewport.IsValid()){bPreviousWorldRenderingDisabled=CoveredViewport->bDisableWorldRendering;CoveredViewport->bDisableWorldRendering=true;}
 Stage->Capture->bCaptureEveryFrame=false;DestinationCapture->bCaptureEveryFrame=false;
 return true;
}
void UPokeMonsterEvolutionWidget::RefreshText()
{
 const auto* C=Individual(this,CreatureId);if(!C||!Title)return;
 auto* S=C->Species.LoadSynchronous();const FString Name=S?S->GetDisplayName().ToString():TEXT("Pokémon");
 if(Phase==TEXT("offer")){Title->SetText(FText::FromString(Name+TEXT(" ist bereit zur Entwicklung")));Details->SetText(FText::FromString(C->PendingEvolutionItemId.IsNone()?TEXT("B / Enter beginnen · A / Esc abbrechen.\nNach einem späteren Levelaufstieg oder Kampfsieg ist ein neues Angebot möglich."):TEXT("B / Enter beginnen · A / Esc abbrechen.\nDer Gegenstand wird nur bei erfolgreicher Entwicklung verbraucht. Abbruch erlaubt eine erneute Auswahl.")));}
 else if(Phase==TEXT("transform")){Title->SetText(FText::FromString(TEXT("Eine neue Kraft erwacht …")));Details->SetText(FText::FromString(TEXT("A / Esc kann bis zum Ende der Lichtverwandlung (5 s) abbrechen.")));}
 else if(Phase==TEXT("reveal")){Title->SetText(FText::FromString(TEXT("Die neue Gestalt erwacht …")));Details->SetText(FText::FromString(TEXT("Die Entwicklung ist übernommen. Dein Pokémon zeigt seine neue Form.")));}
 else if(Phase==TEXT("complete")){Title->SetText(FText::FromString(SourceName+TEXT(" hat sich zu ")+DestinationName+TEXT(" entwickelt!")));Details->SetText(FText::FromString(TEXT("Dein Pokémon hat eine neue Kraft gewonnen.\nBestätigen, um die Reise fortzusetzen.")));}
 else if(Phase==TEXT("cancelled")){Title->SetText(FText::FromString(TEXT("Entwicklung abgebrochen")));Details->SetText(FText::FromString(Name+TEXT(" bleibt unverändert. Später ist ein neues Angebot möglich.")));}
 else if(Phase==TEXT("error")){Title->SetText(FText::FromString(TEXT("Entwicklung nicht übernommen")));Details->SetText(FText::FromString(TEXT("Bedingungen, Zielmodell oder Speichern konnten nicht bestätigt werden.\nDie ursprüngliche Kreatur bleibt erhalten.")));}
 else if(Phase==TEXT("learning"))
 {
  if(C->PendingMoves.IsEmpty()){Finish();return;}
  const auto* Move=C->PendingMoves[0].LoadSynchronous();Title->SetText(FText::FromString(Name+TEXT(" kann ")+(Move?Move->DisplayName.ToString():TEXT("eine Attacke"))+TEXT(" erlernen")));
  FString Lines;for(int32 I=0;I<4;++I){const auto* M=C->GetMoveSlots()[I].GetMove().LoadSynchronous();Lines+=FString::Printf(TEXT("%s %d · %s%s"),I==Selection?TEXT("▶"):TEXT("  "),I+1,M?*M->DisplayName.ToString():TEXT("Freier Platz"),I==3?TEXT(""):TEXT("     "));}
  Details->SetText(FText::FromString(Lines+TEXT("\nSteuerkreuz / Pfeile wählen · B lernen/ersetzen · A ablehnen")));
 }
 const bool Offer=Phase==TEXT("offer"),Learning=Phase==TEXT("learning"),Transform=Phase==TEXT("transform"),Reveal=Phase==TEXT("reveal");
 ConfirmButton->SetVisibility(Transform||Reveal?ESlateVisibility::Collapsed:ESlateVisibility::Visible);
 if(auto* Slot=Cast<UCanvasPanelSlot>(ConfirmButton->Slot))Slot->SetAnchors(Offer||Learning?FAnchors(.24f,.88f,.49f,.93f):FAnchors(.36f,.88f,.64f,.93f));
 CancelButton->SetVisibility(Offer||Learning||Transform?ESlateVisibility::Visible:ESlateVisibility::Collapsed);
 ConfirmLabel->SetText(FText::FromString(Learning?TEXT("Lernen · B / Enter"):Offer?TEXT("Beginnen · B / Enter"):TEXT("Weiter · B / Enter")));
 CancelLabel->SetText(FText::FromString(Learning?TEXT("Ablehnen · A / Esc"):TEXT("Abbrechen · A / Esc")));
 Hints->SetText(FText::FromString(Reveal?TEXT("Entwicklung übernommen · Enthüllung läuft"):Transform?TEXT("A / Esc abbrechen · bis zum Abschluss der Lichtverwandlung"):Offer||Learning?TEXT("B bestätigen · A abbrechen · Tastatur: Enter / Esc"):TEXT("B / Enter weiter")));
}
void UPokeMonsterEvolutionWidget::Confirm()
{
 auto* E=Service(this);if(!E)return;
 if(Phase==TEXT("offer")){Phase=TEXT("transform");Elapsed=0;SequenceStart=GetWorld()->GetTimeSeconds();if(Glow){Stage->PlayerVisual->Mesh->SetOverlayMaterial(Glow);Stage->OpponentVisual->Mesh->SetOverlayMaterial(Glow);}RefreshText();}
 else if(Phase==TEXT("complete"))StartLearning();
 else if(Phase==TEXT("learning")){if(E->ResolveEvolutionLearning(CreatureId,Selection))RefreshText();else{Phase=TEXT("error");RefreshText();}}
 else if(Phase!=TEXT("transform")&&Phase!=TEXT("reveal"))Finish();
}
void UPokeMonsterEvolutionWidget::Cancel()
{
 auto* E=Service(this);if(!E)return;
 if(CanCancelEvolution())
 {
  if(E->ResolveEvolution(CreatureId,Target,false)){Phase=TEXT("cancelled");Elapsed=0;RestoreSourceView();RefreshText();}else{Phase=TEXT("error");RestoreSourceView();RefreshText();}
 }
 else if(Phase==TEXT("learning")){if(E->ResolveEvolutionLearning(CreatureId,INDEX_NONE))RefreshText();else{Phase=TEXT("error");RefreshText();}}
 else if(Phase==TEXT("complete"))StartLearning();
 else if(Phase!=TEXT("transform")&&Phase!=TEXT("reveal"))Finish();
}
void UPokeMonsterEvolutionWidget::StartLearning(){const auto* C=Individual(this,CreatureId);if(C&&!C->PendingMoves.IsEmpty()){Phase=TEXT("learning");Selection=0;RefreshText();}else Finish();}
bool UPokeMonsterEvolutionWidget::CanCancelEvolution() const
{
 return Phase==TEXT("offer")||(Phase==TEXT("transform")&&PokeMonsterEvolutionPresentation::Sample(Elapsed).bCanCancel);
}
void UPokeMonsterEvolutionWidget::RestoreSourceView()
{
 if(Glow)Glow->SetScalarParameterValue(TEXT("Strength"),0);
 if(Stage){Stage->PlayerVisual->Mesh->SetOverlayMaterial(nullptr);Stage->OpponentVisual->Mesh->SetOverlayMaterial(nullptr);}
 if(View)View->SetRenderOpacity(1);if(DestinationView)DestinationView->SetRenderOpacity(0);
 if(Flash)Flash->SetRenderOpacity(0);for(const auto& Dot:Motes)Dot->SetRenderOpacity(0);
}
void UPokeMonsterEvolutionWidget::NativeTick(const FGeometry& G,float Delta)
{
 Super::NativeTick(G,Delta);if(Phase==TEXT("transform")||Phase==TEXT("reveal"))Elapsed=FMath::Max(0.f,GetWorld()->GetTimeSeconds()-SequenceStart);
 using namespace PokeMonsterEvolutionPresentation;
 const bool Active=Phase==TEXT("transform")||Phase==TEXT("reveal");
 const auto Frame=Active?Sample(Elapsed):PokeMonsterEvolutionPresentation::FFrame{};
 if(Glow)Glow->SetScalarParameterValue(TEXT("Strength"),Active?Frame.Glow:0.f);
 if(Flash){Flash->SetRenderOpacity(1);Flash->SetColorAndOpacity(FLinearColor(1,.97f,.88f,Frame.Flash));}
 for(int I=0;I<Motes.Num();++I){const float A=Elapsed*(.40f+I*.035f)+I*2.399f;const float Radius=G.GetLocalSize().Y*(.11f+I*.007f);Motes[I]->SetRenderTranslation(FVector2D(FMath::Cos(A)*Radius,FMath::Sin(A*.83f)*Radius*.8f));Motes[I]->SetRenderOpacity(Frame.Particles*(.25f+.3f*FMath::Sin(A)*FMath::Sin(A)));}
 // Explicit captures also update when the fully covered main view is not drawn.
 const float Now=GetWorld()->GetTimeSeconds();
 if(Stage&&Now!=LastCaptureTime)
 {
  const bool DestinationOnly=Phase==TEXT("reveal")||Phase==TEXT("complete")||(Phase==TEXT("learning")&&bHappyPlayed);
  if(!DestinationOnly&&(!Active||Frame.Morph<1.f))Stage->Capture->CaptureScene();
  if(DestinationCapture&&(DestinationOnly||(Active&&Frame.Morph>0.f)))DestinationCapture->CaptureScene();
  LastCaptureTime=Now;
 }
 if(!Active)return;
 DestinationView->SetRenderOpacity(Frame.Morph);
 if(Phase==TEXT("transform")&&Elapsed>=CommitSeconds)
 {
  auto* E=Service(this);
  if(!E||!E->ResolveEvolution(CreatureId,Target,true)){Phase=TEXT("error");RestoreSourceView();RefreshText();return;}
  Phase=TEXT("reveal");View->SetRenderOpacity(0);RefreshText();
 }
 if(Phase==TEXT("reveal")&&Elapsed>=ColorSeconds&&!bHappyPlayed)
 {
  // Remove the overlay completely, rather than leave a white material at zero strength.
  Stage->PlayerVisual->Mesh->SetOverlayMaterial(nullptr);Stage->OpponentVisual->Mesh->SetOverlayMaterial(nullptr);
  Stage->OpponentVisual->PlayReaction(EPokeMonsterCreatureClip::Happy);bHappyPlayed=true;
 }
 if(Phase==TEXT("reveal")&&Elapsed>=CompleteSeconds){Phase=TEXT("complete");RefreshText();}
}
int32 UPokeMonsterEvolutionWidget::NativePaint(const FPaintArgs& Args,const FGeometry& G,const FSlateRect& Clip,FSlateWindowElementList& Out,int32 Layer,const FWidgetStyle& Style,bool ParentEnabled) const
{
 const int32 Base=Super::NativePaint(Args,G,Clip,Out,Layer,Style,ParentEnabled);
 if(Phase!=TEXT("transform")&&Phase!=TEXT("reveal"))return Base;
 const auto Frame=PokeMonsterEvolutionPresentation::Sample(Elapsed);const auto Size=G.GetLocalSize();const FVector2D Centre=Size*FVector2D(.5f,.45f);
 for(int Wave=0;Wave<3;++Wave)
 {
  const float Progress=FMath::Frac(Elapsed*.38f+Wave/3.f);const float Alpha=Frame.Particles*FMath::Sin(Progress*PI)*.16f;const float Radius=Size.Y*(.10f+.24f*Progress);
  TArray<FVector2D> Points;for(int I=0;I<=64;++I){const float A=I*2.f*PI/64;Points.Add(Centre+FVector2D(FMath::Cos(A)*Radius,FMath::Sin(A)*Radius*.78f));}
  FSlateDrawElement::MakeLines(Out,Base+1,G.ToPaintGeometry(),Points,ESlateDrawEffect::None,FLinearColor(1,.85f,.48f,Alpha*.25f),true,6.f);
  FSlateDrawElement::MakeLines(Out,Base+2,G.ToPaintGeometry(),Points,ESlateDrawEffect::None,FLinearColor(1,.92f,.7f,Alpha),true,1.2f);
 }
 return Base+2;
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
void UPokeMonsterEvolutionWidget::RestoreWorldRendering(){if(CoveredViewport.IsValid())CoveredViewport->bDisableWorldRendering=bPreviousWorldRenderingDisabled;CoveredViewport.Reset();}
void UPokeMonsterEvolutionWidget::Finish(){RestoreWorldRendering();if(Stage){Stage->Destroy();Stage=nullptr;}if(OwnerController)OwnerController->CloseEvolutionPresentation();}
void UPokeMonsterEvolutionWidget::NativeDestruct(){RestoreWorldRendering();if(Stage){Stage->Destroy();Stage=nullptr;}Super::NativeDestruct();}
