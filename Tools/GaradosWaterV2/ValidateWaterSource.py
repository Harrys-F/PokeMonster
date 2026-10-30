"""Independent deformation review of all water clips; never rewrites a source or export."""
import bpy,json,math,sys
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GaradosWaterV2'/('WaterReviewRelease'if '--label'not in sys.argv else sys.argv[sys.argv.index('--label')+1]);D.mkdir(exist_ok=False);A=R/'Art/Characters/Creatures/Garados';bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Garados_Water_V2.blend'));body=bpy.data.objects['Garados_Water_Body'];rig=bpy.data.objects['Garados_Water_Rig'];s=bpy.context.scene;s.world=bpy.data.worlds.new('ReviewWorld');s.world.color=(.25,.25,.25);s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
for loc,power in [((4,-6,8),1200),((-4,2,6),1000),((0,4,8),1200)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=5;o.rotation_euler=(Vector((0,0,2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=9;s.camera=cam
rows=[];overall=[]
for action in sorted([a for a in bpy.data.actions if '_Swim'in a.name],key=lambda a:a.name):
 rig.animation_data.action=action
 for f in range(1,int(action.frame_range.y)+1):
  s.frame_set(f);bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();ratios=[]
  if f in [1,13,25,37,49,int(action.frame_range.y)]:
   for e in body.data.edges:
    a,b=e.vertices;old=(body.data.vertices[a].co-body.data.vertices[b].co).length
    if old>.001:ratios.append((m.vertices[a].co-m.vertices[b].co).length/old)
  ps=[v.co.copy()for v in m.vertices];ratios.sort();row={'clip':action.name,'frame':f,'min':[min(p[i]for p in ps)for i in range(3)],'max':[max(p[i]for p in ps)for i in range(3)],'radius_xy_m':max(math.hypot(p.x,p.y)for p in ps)}
  if ratios:row.update(edge_ratio_max=ratios[-1],edge_ratio_p99=ratios[int(len(ratios)*.99)])
  rows.append(row);overall.extend(ps);ev.to_mesh_clear()
  if f==13 and any(x in action.name for x in ['Normal','Observe']):
   for name,loc in [('Game',(7,-10,9)),('Side',(9,0,2.2))]:
    cam.location=loc;cam.rotation_euler=(Vector((0,0,2))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(D/(action.name+'_'+name+'.png'));bpy.ops.render.render(write_still=True)
original=bpy.data.objects['Garados_Body'].data;rest_ratios=[]
for e in original.edges:
 a,b=e.vertices;L=(original.vertices[a].co-original.vertices[b].co).length
 if L>.001:rest_ratios.append((body.data.vertices[a].co-body.data.vertices[b].co).length/L)
continuity={'original_faces':all(list(p.vertices)==list(q.vertices)for p,q in zip(original.polygons,body.data.polygons)),'original_uvs':all((p.uv-q.uv).length<1e-8 for p,q in zip(original.uv_layers.active.data,body.data.uv_layers.active.data)),'edge_ratio_percentiles_from_original_rest':{str(p):float(np.percentile(rest_ratios,p))for p in [1,50,95,99,100]}}
result={'source_continuity':continuity,'poses':rows,'bounds_blender_m':{'min':[min(p[i]for p in overall)for i in range(3)],'max':[max(p[i]for p in overall)for i in range(3)]},'max_radius_cm':max(math.hypot(p.x,p.y)for p in overall)*100};(D/'Result.json').write_text(json.dumps(result,indent=2));print('WATER_REVIEW',json.dumps({k:v for k,v in result.items()if k!='poses'}),flush=True)
