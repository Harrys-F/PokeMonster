import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster');C=Path(bpy.data.filepath).parent.parent;id=C.name;I=R/'Art/Characters/NPCs/IntegrationV1';s=bpy.context.scene;hp=next(o for o in s.objects if o.type=='MESH')
# Trace the actual Blender material bindings, not guessed image indices.
mat=hp.data.materials[0];bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
def tex_upstream(socket,seen=None):
 seen=seen or set()
 for link in socket.links:
  n=link.from_node
  if n in seen:continue
  seen.add(n)
  if n.type=='TEX_IMAGE':return n.image
  for pin in n.inputs:
   out=tex_upstream(pin,seen)
   if out:return out
 return None
bindings={k:bpy.path.abspath(tex_upstream(bs.inputs[k]).filepath) if tex_upstream(bs.inputs[k]) else None for k in ['Base Color','Normal','Roughness','Metallic']}
if id=='Ranger':
 (I/(id+'_MaterialBindings.json')).write_text(json.dumps(bindings,indent=2));print('RANGER_BINDINGS_ONLY');raise SystemExit()
run=hp.copy();run.data=hp.data.copy();run.name=id+'_STATIC_REVIEW_NOT_RIGGED';c=bpy.data.collections.new('STATIC_RUNTIME_REVIEW');s.collection.children.link(c);c.objects.link(run);hp.hide_render=True;hp.hide_set(True)
bpy.context.view_layer.objects.active=run
for o in s.objects:o.select_set(False)
run.select_set(True)
mod=run.modifiers.new('NonDestructive_StaticPreview_Reduction','DECIMATE');mod.decimate_type='COLLAPSE';mod.ratio=min(1,150000/len(run.data.polygons));mod.use_collapse_triangulate=True
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();e=run.evaluated_get(dg);m=e.to_mesh();count=len(m.polygons);vertices=len(m.vertices);e.to_mesh_clear()
s['status']='Static reference only; no rig, no animation, no map placement approval'
out=C/'Source'/(id+'_NPC_StaticReview_V1.blend');assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out))
export=C/'Exports'/('SM_'+id+'_Reference_V1.fbx');bpy.ops.export_scene.fbx(filepath=str(export),use_selection=True,object_types={'MESH'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim=False,path_mode='AUTO')
report={'id':id,'source_blend':str(out),'export':str(export),'reference_triangles':len(hp.data.polygons),'preview_triangles':count,'preview_vertices':vertices,'reduction_method':'Unapplied Decimate on independent mesh copy for STATIC preview only, not retopology or animation readiness','material_bindings':bindings,'status':'Static reference pending Unreal review','rig':None,'animations':[]}
(I/(id+'_StaticExport.json')).write_text(json.dumps(report,indent=2));(I/(id+'_MaterialBindings.json')).write_text(json.dumps(bindings,indent=2))
h=float(s['review_height_m']);s.camera.location=(0,-h*3,h*.5);s.camera.rotation_euler=(Vector((0,0,h*.5))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(C/'Previews/04_StaticReduced_Front.png');bpy.ops.render.render(write_still=True);print('STATIC_EXPORT_DONE',id,count,flush=True)
