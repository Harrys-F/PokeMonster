"""Read the existing Meshy working rig; render diagnostic poses without saving source/model edits."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GaradosWaterV2/PoseIntake';D.mkdir(exist_ok=False);A=R/'Art/Characters/Creatures/Garados';source=A/'Source/Garados_Meshy_V1.blend';before=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));body=bpy.data.objects['Garados_Body'];rig=bpy.data.objects['Garados_Rig'];s=bpy.context.scene;rig.animation_data.action=None
for p in rig.pose.bones:p.matrix_basis=Matrix.Identity(4)
bpy.context.view_layer.update();bones={b.name:{'head':list(b.head_local),'tail':list(b.tail_local),'parent':b.parent.name if b.parent else None}for b in rig.data.bones};rest={b.name:b.matrix_local.copy()for b in rig.data.bones};lengths=[rig.data.bones['body_'+str(i)].length for i in range(10)]
s.world=bpy.data.worlds.new('DiagnosticWorld');s.world.color=(.2,.2,.2);s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=960;s.render.resolution_y=640;s.render.resolution_percentage=100
for loc,power in [((4,-6,8),1000),((-4,2,6),800),((0,4,8),900)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=5;o.rotation_euler=(Vector((0,0,1.8))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=8;s.camera=cam
rows=[]
def capture(n,loc,target):
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(D/(n+'.png'));bpy.ops.render.render(write_still=True)
def metrics(n):
 ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();ratios=[]
 for e in body.data.edges:
  a,b=e.vertices;old=(body.data.vertices[a].co-body.data.vertices[b].co).length
  if old>.001:ratios.append((m.vertices[a].co-m.vertices[b].co).length/old)
 ps=[v.co for v in m.vertices];ratios.sort();rows.append({'pose':n,'min':[min(p[i]for p in ps)for i in range(3)],'max':[max(p[i]for p in ps)for i in range(3)],'edge_ratio_max':ratios[-1],'edge_ratio_p99':ratios[int(len(ratios)*.99)]});ev.to_mesh_clear()
metrics('Original');capture('Original',(8,0,2),(0,0,1.8))
def setbone(n,h,d):
 b=rig.data.bones[n];od=b.tail_local-b.head_local;q=Quaternion((1,0,0),math.atan2(d.z,d.y)-math.atan2(od.z,od.y));m=q.to_matrix().to_4x4()@rest[n];m.translation=h;rig.pose.bones[n].matrix=m;bpy.context.view_layer.update()
pos=Vector((0,-sum(lengths)/2,1.85));setbone('head',pos,Vector((0,-1,0)))
for i,L in enumerate(lengths):
 d=Vector((0,1,0));setbone('body_'+str(i),pos,d);pos+=d*L
metrics('Flat');capture('FlatSide',(8,0,2),(0,0,1.65));capture('FlatGame',(6,-9,8),(0,0,1.65))
assert hashlib.sha256(source.read_bytes()).hexdigest()==before;(D/'Result.json').write_text(json.dumps({'source':str(source.relative_to(R)),'source_sha256':before,'bones':bones,'lengths':lengths,'poses':rows,'source_not_saved':True},indent=2));print('POSE_DIAGNOSTICS',json.dumps(rows),flush=True)
