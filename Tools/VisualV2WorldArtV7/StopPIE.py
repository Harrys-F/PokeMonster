import unreal
if hasattr(unreal,'_waq2_review_variants'):
 unreal._waq2_review_variants.apply('V1');del unreal._waq2_review_variants
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
