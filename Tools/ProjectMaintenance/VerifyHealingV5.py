"""Read-only reopen audit for the new not-yet-staged V5 source; historical tracked-source guard stays unchanged."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];p=R/'Art/HealingHouse/Source/HealingHouse_ArtV5.blend';before=hashlib.sha256(p.read_bytes()).hexdigest();assert bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)=={'FINISHED'};expected=json.loads((R/'Art/HealingHouse/ArtV5_Props.json').read_text())['assets'];rows=[]
for row in expected:
 o=bpy.data.objects[row['name']];m=o.data;m.calc_loop_triangles();assert len(m.vertices)==row['vertices']and len(m.loop_triangles)==row['triangles'];assert not any(f.area<1e-12 for f in m.polygons);assert m.uv_layers;rows.append({'mesh':o.name,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'zero_area_faces':0,'uv_layers':len(m.uv_layers)})
missing=[i.filepath for i in bpy.data.images if i.source=='FILE'and not i.packed_file and not Path(bpy.path.abspath(i.filepath)).is_file()];assert not missing;assert hashlib.sha256(p.read_bytes()).hexdigest()==before
(R/'Saved/ArtPassV5/BlenderReopen.json').write_text(json.dumps({'passed':True,'file':str(p.relative_to(R)),'sha256':before,'unchanged_by_check':True,'reopened_in_independent_process':True,'missing_textures':missing,'mesh_checks':rows},indent=2));print('ART_V5_BLEND_READ_ONLY_PASS')
