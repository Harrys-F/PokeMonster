"""Reopen the authored detail source, inspect UV/degeneracy and remove only collapsed leaf tips."""
import bpy,bmesh,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/HealingHouse';p=A/'Source/HealingHouse_ApothecaryDetails.blend';bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;out=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);collapsed=sum(f.calc_area()<1e-12 for f in bm.faces);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bad=[f for f in bm.faces if f.calc_area()<1e-12]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles()
 assert all(f.area>1e-12 for f in o.data.polygons),o.name
 assert o.data.uv_layers.active and all(v.co.length<5 for v in o.data.vertices)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;old=o.location.copy();o.location=(0,0,0)
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_HH_'+o.name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False);o.location=old
 out.append({'name':o.name,'collapsed_faces_before':collapsed,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'materials':len(o.data.materials),'uv_layer':o.data.uv_layers.active.name,'dimensions_m':list(o.dimensions)})
bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p));assert len([o for o in bpy.data.objects if o.type=='MESH'])==3
(A/'ApothecaryDetails.json').write_text(json.dumps({'source':str(p.relative_to(R)),'assets':out,'units':'metres','reopened':True,'rig':False},indent=2));print('DETAIL_SOURCE_QA_OK',json.dumps(out))
