"""Read-only proof that the V4 rigged mesh retains original posed geometry/UVs; original material used in Unreal."""
import bpy,hashlib,json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2];C=R/'Art/Characters/NPCs/SilverLady/Source';files=[C/'SilverLady_HealerPose.blend',C/'Westland_Healer_ArtV4.blend'];before={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}
def snapshot(m):
 h=hashlib.sha256()
 for v in m.vertices:h.update(struct.pack('<3f',*v.co))
 poly=hashlib.sha256()
 for p in m.polygons:poly.update(struct.pack('<I',len(p.vertices)));poly.update(struct.pack('<'+str(len(p.vertices))+'I',*p.vertices))
 uv=hashlib.sha256()
 for layer in m.uv_layers:
  for d in layer.data:uv.update(struct.pack('<2f',*d.uv))
 return {'vertices':len(m.vertices),'triangles':sum(len(p.vertices)-2 for p in m.polygons),'geometry_sha256':h.hexdigest(),'polygons_sha256':poly.hexdigest(),'uv_sha256':uv.hexdigest()}
bpy.ops.wm.open_mainfile(filepath=str(files[0]),load_ui=False);o=bpy.data.objects['SilverLady_HealerPose'];m=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()),preserve_all_data_layers=True,depsgraph=bpy.context.evaluated_depsgraph_get());old=snapshot(m);matrix=[list(x)for x in o.matrix_world]
bpy.ops.wm.open_mainfile(filepath=str(files[1]),load_ui=False);o=bpy.data.objects['Westland_Healer'];new=snapshot(o.data);assert old==new,(old,new);assert matrix==[list(x)for x in o.matrix_world];assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in before.items())
j={'passed':True,'original_pose':str(files[0].relative_to(R)),'current_rigged_mesh_source':str(files[1].relative_to(R)),'original_pose_geometry_uv_and_transform_identical':True,'fingerprints':new,'source_hashes':before,'no_source_saved':True,'material_requirement':'Unreal component must bind exact MI_SilverLady_V1; V4 recoloring must not remain active.'};(R/'Art/Characters/NPCs/SilverLady/ArtV5_OriginalAppearance.json').write_text(json.dumps(j,indent=2));print('SILVERLADY_ORIGINAL_GEOMETRY_UV_PASS')
