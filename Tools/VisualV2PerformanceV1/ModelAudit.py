"""Read actual asset-registry LOD0 tags, plus the real SkyLight component.
No shader-statistics compilation or asset mutation.
"""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world()or E.get_editor_world();A=unreal.AssetRegistryHelpers.get_asset_registry();rows=[]
inv=json.loads((D/'RuntimeInventory.json').read_text())
for p,row in inv['skeletal_meshes'].items():
 d=A.get_asset_by_object_path(p);rows.append({'asset':p,'components':row['components'],'material_slots':len(row['materials']),'registry_LOD0':{k:d.get_tag_value(k)for k in ['Triangles','Vertices','LODs','Bones','NaniteEnabled']}})
def prop(c,n):
 try:return str(c.get_editor_property(n))
 except Exception:return None
sky=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.SkyLight):
 c=a.get_component_by_class(unreal.SkyLightComponent);sky.append({'actor':a.get_actor_label(),'properties':{n:prop(c,n)for n in ['mobility','intensity','real_time_capture','source_type','cubemap_resolution','cast_shadows','lower_hemisphere_is_black','occlusion_max_distance']}})
(D/'ModelAndSkyAudit.json').write_text(json.dumps({'skeletal':rows,'skylights':sky},indent=2))
