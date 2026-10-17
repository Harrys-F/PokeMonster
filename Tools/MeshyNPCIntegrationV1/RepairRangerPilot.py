import bpy,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');C=R/'Art/Characters/NPCs/Ranger';I=R/'Art/Characters/NPCs/IntegrationV1';s=bpy.context.scene;run=s.objects['Ranger_Runtime_Pilot'];rig=s.objects['Ranger_Pilot_Rig'];groups={g.name:g for g in run.vertex_groups}
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
count=0
for v in run.data.vertices:
 x,y,z=v.co;ax=abs(x);side='l' if x>0 else 'r'
 if ax>.18 and z>1.18:
  strength=smooth(.18,.29,ax)
  if ax<.70:t=smooth(.48,.60,ax);a={'upperarm_'+side:1-t,'lowerarm_'+side:t}
  else:t=smooth(.74,.81,ax);a={'lowerarm_'+side:1-t,'hand_'+side:t}
  w={'chest':1-strength};w.update({n:q*strength for n,q in a.items()})
  for g in groups.values():g.remove([v.index])
  for n,q in w.items():
   if q>1e-5:groups[n].add([v.index],q,'REPLACE')
  count+=1
# Measure actual deformed surface at every idle/gesture source frame.
audit=[]
for name,end in [('A_Ranger_Idle_Pilot',91),('A_Ranger_Gesture_Pilot',61)]:
 rig.animation_data.action=bpy.data.actions[name];lo=100;hi=-100
 for f in range(1,end+1):
  s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();o=run.evaluated_get(dg);m=o.to_mesh();a=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',a);a=a.reshape(-1,3);lo=min(lo,float(a[:,2].min()));hi=max(hi,float(np.abs(a[:,0]).max()));o.to_mesh_clear()
 audit.append({'clip':name,'frames':end,'surface_floor_min_m':lo,'maximum_half_width_m':hi})
rig.animation_data.action=bpy.data.actions['A_Ranger_Idle_Pilot'];s.frame_start=1;s.frame_end=91;s.frame_set(1);s['status']='Repaired stationary Ranger candidate; visual and Unreal validation pending'
f=C/'Source/Ranger_NPC_V1.blend';assert not f.exists();bpy.ops.wm.save_as_mainfile(filepath=str(f))
views=[]
for name,clip,frame,loc,size in [('06_Idle_Repaired','A_Ranger_Idle_Pilot',1,(3,-5,2.1),2.1),('07_Gesture_Repaired','A_Ranger_Gesture_Pilot',31,(3,-5,2.1),2.1),('08_Shoulders_Repaired','A_Ranger_Idle_Pilot',46,(2,-4,1.45),1.2)]:
 rig.animation_data.action=bpy.data.actions[clip];s.frame_set(frame);s.camera.location=loc;aim=Vector((0,0,1.22 if 'Shoulders' in name else .9));s.camera.rotation_euler=(aim-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=size;s.render.filepath=str(C/'Previews'/(name+'.png'));bpy.ops.render.render(write_still=True);views.append(s.render.filepath)
(I/'Ranger_RepairAudit.json').write_text(json.dumps({'changed_arm_vertices':count,'correction':'Arm blend independent of sleeve lower Z; full arm weighting across sleeve cross-section','clips':audit,'renders':views,'status':'pending visual review'},indent=2));print('REPAIR_DONE',flush=True)
