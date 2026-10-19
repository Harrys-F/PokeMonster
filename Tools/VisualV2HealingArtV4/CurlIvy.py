from pathlib import Path
import bpy,json,shutil,math
R=Path(__file__).resolve().parents[2];A=R/'Art/World/VisualV2HealingArtV4';S=R/'Saved/VisualV2HealingArtV4';p=A/'Source/HealingHouse_GardenDetails_V4.blend';assert bpy.app.background;backup=S/'GardenDetails_BeforeIvyCurl.blend';assert not backup.exists();shutil.copy2(p,backup);bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0
for key in ['IvySprigA','IvySprigB']:
 o=bpy.data.objects['HA4_'+key];me=o.data;uvs={me.loops[li].vertex_index:me.uv_layers.active.data[li].uv.copy() for li in range(len(me.loops))}
 for v in me.vertices:v.co.x+=(uvs[v.index].y-.5)*.95
 me.update();bpy.context.view_layer.update();location=o.location.copy();o.location=(0,0,0);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_HA4_'+key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False,path_mode='COPY',embed_textures=False);o.location=location
 info=json.loads((A/'Details.json').read_text());info[key]['dimensions_m']=[max(v.co[i] for v in me.vertices)-min(v.co[i] for v in me.vertices) for i in range(3)];(A/'Details.json').write_text(json.dumps(info,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(p));(S/'IvyCurlFix.json').write_text(json.dumps({'reason':'Thin vertical leaves remained unlit in actual unchanged lighting. Tilt real leaf surfaces upward; preserve actor transforms.','outward_upward_leaf_normals':True}));print('IVY_CURL_SAVED')
