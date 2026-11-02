"""Saved scene, terrain seam, protected-route and per-asset checks; no writes to assets."""
import unreal,json,sys,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world()and W.get_name()=='Dev_WestlandRegion';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
sys.path.insert(0,str(R/'Tools/WestlandEnvironmentPolishV2'));import Shapes as S
before=json.loads((D/'Dev_WestlandRegion_Before.json').read_text());after=scene(W);(D/'SceneAfter.json').write_text(json.dumps(after,indent=2));old=before['actors'];new=after['actors'];assert set(old)<=set(new);allowed=set(r['actor']for r in json.loads((D/'Ground.json').read_text()));allowed.update(a['label']for a in old.values()if a['label'].startswith(('WR_Terrain_','WVU_','WR_Grass','WR_MeadowHerbs')));allowed.update(['WR_WindingRiver','WR_RockyContours']);changed=[]
for k,a in old.items():
 b=new[k];assert a['transform']==b['transform'],('Original actor transform',a['label'])
 if a!=b:assert a['label']in allowed,('Unexpected original scene change',a['label']);changed.append(a['label'])
assert before['world_settings']==after['world_settings'];actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()};groups=[]
for label,a in actors.items():
 if label.startswith(('WVU_','WEP_')):
  c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
  if c:groups.append(dict(label=label,instances=c.get_instance_count(),mesh=c.static_mesh.get_path_name(),shadow=c.cast_shadow,collision=str(c.get_collision_enabled())))
seams={};seam_error=0;terrain_triangles=0
for label,a in actors.items():
 if not label.startswith('WR_Terrain_'):continue
 m=a.static_mesh_component.static_mesh;dm=unreal.DynamicMesh();dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(m,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;_,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);terrain_triangles+=m.get_num_triangles(0)
 for p in unreal.GeometryScript_List.convert_vector_list_to_array(vs):
  e,n=S.L.en(p.x,p.y);key=(round(e,3),round(n,3))
  if key in seams:seam_error=max(seam_error,abs(seams[key]-p.z))
  else:seams[key]=p.z
assert seam_error<.02,('Terrain crack',seam_error)
route_delta=max(abs(S.delta(e,n,S.L.height(e,n)))for _,ps,width in S.L.PATHS for e,n in S.L.sample(ps,spacing=1));bank_route_delta=max(abs(S.bank_height(e,n,S.L.height(e,n)+S.delta(e,n,S.L.height(e,n)))-S.L.height(e,n))for _,ps,width in S.L.PATHS for e,n in S.L.sample(ps,spacing=1));assert bank_route_delta==0;assert route_delta==0
water=actors['WR_WindingRiver'].static_mesh_component.get_material(0);assert water.get_editor_property('shading_model')==unreal.MaterialShadingModel.MSM_SINGLE_LAYER_WATER;assert water.get_editor_property('blend_mode')==unreal.BlendMode.BLEND_OPAQUE
result=dict(passed=True,original_actors=len(old),final_actors=len(new),original_actor_transforms_unchanged=True,intentional_original_visual_actor_edits=changed,new_actors=[a['label']for k,a in new.items()if k not in old],original_gameplay_and_light_actor_signatures_unchanged=True,terrain_edge_max_error_cm=seam_error,terrain_triangles=terrain_triangles,protected_route_max_height_change_m=route_delta,groups=groups);(D/'SceneAudit.json').write_text(json.dumps(result,indent=2));unreal.log('WESTLAND_ENVIRONMENT_POLISH_V2_AUDIT_PASS')
