import bpy,bmesh,json,time,numpy as np
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];bpy.context.window.scene=s
for other in list(bpy.data.scenes):
 if other!=s and not other.objects:bpy.data.scenes.remove(other)
hp=s.objects['GRT_HighPoly_Reference'];report={}
def stats(o):
 m=o.data;m.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(m);q={'vertices':len(m.vertices),'polygons':len(m.polygons),'triangles':len(m.loop_triangles),'quads':sum(len(p.vertices)==4 for p in m.polygons),'boundary_edges':sum(e.is_boundary for e in bm.edges),'edges_gt2_faces':sum(len(e.link_faces)>2 for e in bm.edges),'loose_vertices':sum(not v.link_faces for v in bm.verts)};bm.free();return q
for name,ratio,budget in [('HeadHair',.025,6000),('Torso',.08,5000)]:
 o=s.objects['GRT_'+name];bpy.ops.object.select_all(action=next(i.identifier for i in bpy.ops.object.select_all.get_rna_type().properties['action'].enum_items if i.identifier=='DESELECT'));o.hide_render=False;o.select_set(True);bpy.context.view_layer.objects.active=o
 t=time.time();before={'vertices':len(o.data.vertices),'polygons':len(o.data.polygons)}
 # Only numerical preconditioning of this bounded test proxy; not final global decimation.
 dec=o.modifiers.new('Bounded_Solver_Preconditioning','DECIMATE');dec.ratio=ratio;bpy.ops.object.modifier_apply(modifier=dec.name);proxy=stats(o);print('PRECONDITION_DONE',name,proxy,flush=True)
 try:
  mode=next(i.identifier for i in bpy.ops.object.quadriflow_remesh.get_rna_type().properties['mode'].enum_items if i.identifier=='FACES')
  result=bpy.ops.object.quadriflow_remesh(mode=mode,target_faces=budget,use_mesh_symmetry=False,use_preserve_sharp=False,use_preserve_boundary=True,preserve_attributes=False,smooth_normals=True,seed=42)
  status=list(result)
 except Exception as e:status=['ERROR',str(e)]
 after=stats(o);method='QuadriFlow automatic trial' if after['quads']>0 and after['polygons']!=proxy['polygons'] else 'Triangle diagnostic control; automatic QuadriFlow did not produce usable replacement'
 print('QUADRIFLOW_DONE',name,status,after,flush=True)
 if after['quads']>0:
  sw=o.modifiers.new('Reproject_to_unmodified_HP','SHRINKWRAP');sw.target=hp;sw.wrap_method=next(i.identifier for i in bpy.types.ShrinkwrapModifier.bl_rna.properties['wrap_method'].enum_items if i.identifier=='NEAREST_SURFACEPOINT');sw.offset=0;bpy.ops.object.modifier_apply(modifier=sw.name)
 for p in o.data.polygons:p.use_smooth=True
 if not o.data.uv_layers:o.data.uv_layers.new(name='BakeUV')
 bpy.ops.object.mode_set(mode=next(i.identifier for i in bpy.ops.object.mode_set.get_rna_type().properties['mode'].enum_items if i.identifier=='EDIT'));bpy.ops.mesh.select_all(action=next(i.identifier for i in bpy.ops.mesh.select_all.get_rna_type().properties['action'].enum_items if i.identifier=='SELECT'));bpy.ops.uv.smart_project(angle_limit=.9,island_margin=.008);bpy.ops.object.mode_set(mode=next(i.identifier for i in bpy.ops.object.mode_set.get_rna_type().properties['mode'].enum_items if i.identifier=='OBJECT'))
 o['method']=method;o['animation_approved']=False;report[name]={'input':before,'precondition_ratio':ratio,'precondition':proxy,'quadriflow_target_faces':budget,'quadriflow_status':status,'final':stats(o),'method':method,'uv':'Smart Project angle 0.9 rad, island_margin 0.008; new BakeUV','seconds':time.time()-t}
 o.hide_render=True
(P/'RetopoTrial.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(B/'Source/Hobbit_NPC_GameReady_Test_V1.blend'));print('RETOPO_STAGE_SAVED',flush=True)
