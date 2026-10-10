"""Reopen validated source and export only seven independent reusable region meshes."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/World/WestlandRegion'
assert Path(bpy.data.filepath)==ART/'WestlandRegion_PropsV1.blend'
assert (ROOT/'Saved/WestlandRegion/BlenderPropsReview.png').exists()
audit=[]
for name in ['StoneBridge','WoodBridge','Waterwheel','RuinArch','RuinColumn','StandingStone','Crag']:
 o=bpy.data.objects['WR_'+name];assert o.type=='MESH' and len(o.data.polygons)>0
 bpy.ops.object.select_all(action='DESELECT');o.hide_set(False);o.hide_render=False;o.select_set(True);bpy.context.view_layer.objects.active=o
 audit.append({'object':o.name,'dimensions_m':list(o.dimensions),'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'materials':[m.name for m in o.data.materials]})
 path=ART/'Exports'/(o.name+'.fbx');path.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.export_scene.fbx(filepath=str(path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='X',axis_up='Z',use_mesh_modifiers=True,bake_anim=False,use_triangles=True,mesh_smooth_type='FACE')
(ROOT/'Saved/WestlandRegion/BlenderReopenAudit.json').write_text(json.dumps({'reopened':True,'source':str(bpy.data.filepath),'meshes':audit},indent=2))
print('REGION_SOURCE_REOPENED_AND_EXPORTED',len(audit))
