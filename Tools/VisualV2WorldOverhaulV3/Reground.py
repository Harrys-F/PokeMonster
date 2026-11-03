import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Common.py')));assert (D/'SceneBefore.json').is_file()and not(D/'Reground.json').exists(),'One-time pass already completed or missing task-start evidence';rows=[]
def oldheight(x,y):return max([0]+[h for cx,cy,h,rx,ry in [(-1120,620,20,125,115),(-900,800,40,125,115),(-620,1010,60,200,160)]if abs(x-cx)<=rx and abs(y-cy)<=ry])
for a in actors.values():
 label=a.get_actor_label()
 if not label.startswith(('V2_Tree','V2_Stone','V2_Bush','V2_Instanced','WA','EQ3','ArtV','FAT_','EP2_')):continue
 if a.get_editor_property('hidden'):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh or not c.is_visible()or c.get_editor_property('hidden_in_game'):continue
  if isinstance(c,unreal.InstancedStaticMeshComponent):
   n=0
   for j in range(c.get_instance_count()):
    t=c.get_instance_transform(j,True);p=t.translation;dz=height(p.x,p.y)-oldheight(p.x,p.y)
    if abs(dz)>.4:a.modify();t.translation=unreal.Vector(p.x,p.y,p.z+dz);c.update_instance_transform(j,t,True,False,True);n+=1
   if n:c.update_instance_transform(0,c.get_instance_transform(0,True),True,True,True);rows.append(dict(actor=a.get_name(),instances=n))
  else:
   p=a.get_actor_location();dz=height(p.x,p.y)-oldheight(p.x,p.y)
   if abs(dz)>.4:a.modify();a.set_actor_location(unreal.Vector(p.x,p.y,p.z+dz),False,False);rows.append(dict(actor=a.get_name(),label=label,delta_z=dz))
# Exact bridge ramp-end diagnostics: a slope must rise toward the deck, not away.
ramps=[]
for side in [-1,1]:
 a=next(x for x in A.get_all_level_actors()if x.get_actor_label()=='WOV3_BridgeApproach_'+str(side));t=a.get_actor_transform();one=unreal.MathLibrary.transform_location(t,unreal.Vector(0,-50,50));two=unreal.MathLibrary.transform_location(t,unreal.Vector(0,50,50));near=min([one,two],key=lambda p:abs(p.y+320));far=max([one,two],key=lambda p:abs(p.y+320))
 if near.z<far.z:a.modify();r=a.get_actor_rotation();a.set_actor_rotation(unreal.Rotator(roll=-r.roll),False)
 ramps.append(dict(label=a.get_actor_label(),roll=a.get_actor_rotation().roll))
save('Reground.json',dict(regrounded=rows,ramps=ramps))
