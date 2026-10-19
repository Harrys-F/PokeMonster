"""Read-only saved-world and source-palette checks, not a substitute for visual acceptance."""
import unreal,json,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
actual=scene(w);expected=json.loads((S/'AfterScene.json').read_text())
for x in [actual,expected]:
 for a in x['actors'].values():a['components'].sort(key=lambda c:c['name'])
assert actual==expected
inv=json.loads((R/'Art/World/VisualV2WorldArtV2/BaselineInstances.json').read_text());candidates=json.loads((R/'Art/World/VisualV2WorldArtV2/MeshCandidates.json').read_text());rows=[];actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)}
for old in inv['groups']:
 c=actors[old['actor']].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);m=c.static_mesh
 assert c.get_instance_count()==old['count']
 rows.append({'label':old['label'],'instances':c.get_instance_count(),'mesh':m.get_path_name(),'lod_triangles':[m.get_num_triangles(i) for i in range(m.get_num_lods())],'sections':[m.get_num_sections(i) for i in range(m.get_num_lods())],'slots':c.get_num_materials(),'materials':[c.get_material(i).get_path_name() for i in range(c.get_num_materials())]})
assert sum(r['slots'] for r in rows)==12 and sum(r['sections'][0] for r in rows)==10 and sum(r['instances'] for r in rows)==175
stats={}
for path in ['/Game/Environment/VisualV2WorldArtV2/Materials/M_WAQ2_'+n for n in ['PlantVertexColour','HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']]:
 m=unreal.load_asset(path);st=unreal.MaterialEditingLibrary.get_statistics(m);stats[path]={'blend_mode':str(m.get_editor_property('blend_mode')),'two_sided':m.get_editor_property('two_sided'),**{k:st.get_editor_property(k) for k in ['num_vertex_shader_instructions','num_pixel_shader_instructions','num_samplers','num_pixel_texture_samples']}}
(S/'Validation.json').write_text(json.dumps({'groups':rows,'material_statistics':stats,'saved_world_matches':True,'no_gameplay_or_lighting_delta':True},indent=2));unreal.log('WAQ2_SAVED_ART_VALIDATION_PASS')
