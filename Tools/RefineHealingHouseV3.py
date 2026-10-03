"""PIE-driven correction of V3 light strength and Paper2D ground placement.

Run in the full editor with PIE stopped. No gameplay actor is modified.
"""
import unreal, json
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Dev_HealingHouseTestMap'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
strengths={'HH_V3_EntranceGlow':2.8,'HH_V3_CounterGlow':3.6,'HH_V3_RestAreaGlow':2.4}
changes=[]
for actor in actors:
    if not actor.actor_has_tag('HealingHouse_V3'):continue
    name=actor.get_actor_label()
    if name in strengths:
        component=actor.point_light_component
        before=component.get_editor_property('intensity')
        component.set_editor_property('intensity',strengths[name])
        changes.append({'actor':name,'old_intensity':before,'new_intensity':strengths[name]})
    elif isinstance(actor,unreal.PaperSpriteActor):
        component=actor.get_editor_property('render_component')
        asset_name='S_Wildflowers' if 'FlowerPatch' in name else 'S_GrassCluster' if 'GrassPatch' in name else 'S_MossStones'
        sprite=unreal.load_asset('/Game/Environment/Prototype2D/Details/'+asset_name)
        component.set_mobility(unreal.ComponentMobility.MOVABLE)
        if component.get_sprite()!=sprite:assert component.set_sprite(sprite)
        assert component.get_sprite()==sprite
        component.set_mobility(unreal.ComponentMobility.STATIC)
        origin,extent,radius=unreal.SystemLibrary.get_component_bounds(component)
        assert extent.length()>1, 'Assigned sprite must have real bounds'
        position=actor.get_actor_location()
        before=position.z
        position.z+=3-(origin.z-extent.z)
        actor.set_actor_location(position,False,False)
        changes.append({'actor':name,'old_z_cm':before,'new_z_cm':position.z})
assert unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_HealingHouseTestMap')
path=Path(unreal.Paths.project_dir()).resolve()/'Art/HealingHouse/Review/V3/Dressing/VisualCorrections.json'
path.write_text(json.dumps(changes,indent=2)+'\n')
unreal.SystemLibrary.execute_console_command(world,'MAP CHECK')
unreal.log('HH_V3_VISUAL_CORRECTIONS_SAVED '+str(len(changes)))
