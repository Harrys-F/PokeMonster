import unreal
if hasattr(unreal,'_sv8_motion'):
 unreal.unregister_slate_post_tick_callback(unreal._sv8_motion);del unreal._sv8_motion
import unreal
if hasattr(unreal,'_sv8_contact_callback'):
 unreal.unregister_slate_post_tick_callback(unreal._sv8_contact_callback);del unreal._sv8_contact_callback
if hasattr(unreal,'_sv8_mid'):del unreal._sv8_mid
import unreal
if hasattr(unreal,'_waq2_review_variants'):
 unreal._waq2_review_variants.apply('V1');del unreal._waq2_review_variants
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
