"""Run in a full editor after the V3 import (not a PythonScript commandlet).

The Interchange import does not reliably honor the FbxImportUI collision flag.
Generate one inexpensive hull per fixed furniture prop, then save only these
five new assets. Equivalent MCP tool: StaticMeshTools.generate_convex_collisions.
"""
import unreal
subsystem=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
assert subsystem, 'Use a full Unreal Editor session, not a commandlet.'
for name in ('TreatmentBedSmall','TreatmentBedLarge','HerbShelf','Bookcase','HerbTable'):
    mesh=unreal.load_asset('/Game/Environment/HealingHouse/V3/Meshes/SM_HH_V3_'+name)
    assert mesh
    assert subsystem.set_convex_decomposition_collisions(mesh,1,8,10000)
    assert unreal.EditorAssetLibrary.save_loaded_asset(mesh)
unreal.log('HEALING_HOUSE_V3_FURNITURE_COLLISION_SAVED')
