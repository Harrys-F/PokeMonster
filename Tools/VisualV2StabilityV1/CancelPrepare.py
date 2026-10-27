import unreal
if hasattr(unreal,'_stability_prepare'):unreal.unregister_slate_post_tick_callback(unreal._stability_prepare)
