"""Bind approved PBR surfaces only in Westland; preserve all original geometry and collision."""
import unreal,runpy,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandVisualV2IntegrationV1/Common.py')));assert not(D/'Surfaces.json').exists();bindings=[];roads=[];root='/Game/Environment/VisualV2WorldRefinementV4/Materials/M_WR4_';v7='/Game/Environment/VisualV2InteriorV7/Materials/M_V7_'
for a in actors.values():
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if not old:continue
   n=old.get_name();p=None
   if a.get_actor_label().startswith('WR_Terrain_'):p=ROOT+'/Materials/M_WI_RegionalGround'
   elif a.get_actor_label().startswith('WR_Forecourt_'):p=root+'Paving'
   elif n in ['M_WL_Wood','M_WL_Plaster','M_WL_Roof','M_WL_Stone']:p=ROOT+'/Materials/M_WI_Fade'+{'M_WL_Wood':'Timber','M_WL_Plaster':'Plaster','M_WL_Roof':'Roof','M_WL_Stone':'Stone'}[n]
   elif n.startswith('M_HH_Q3_Fade_')and n.rsplit('_',1)[-1]in ['Wood','Timber','Plaster','Stone','Roof']:p=ROOT+'/Materials/M_WI_Fade'+{'Wood':'Timber','Timber':'Timber','Plaster':'Plaster','Stone':'Stone','Roof':'Roof'}[n.rsplit('_',1)[-1]]
   elif n in ['M_HH_Q2_Wood','M_HH_Q2_Timber','M_HH_Q2_WoodLight','M_HH_Q2_WoodDark','M_HH_Wood','M_HH_Timber','M_HH_V2_Wood','M_HH_V2_Timber','MI_Slice_Wood']:p=v7+'OakJoinery'
   elif n in ['M_HH_Q2_Plaster','M_HH_Plaster']:p=v7+'LimePlaster'
   elif n in ['M_HH_Q2_Stone','M_HH_Stone','M_HH_V2_Stone']:p=root+'Stone'
   elif n in ['M_HH_Roof','MI_Slice_Roof']:p=root+'Roof'
   if p:
    m=unreal.load_asset(p);assert m,p
    if old!=m:a.modify();c.set_material(i,m);bindings.append(dict(actor=a.get_actor_label(),component=c.get_name(),slot=i,before=old.get_path_name(),after=m.get_path_name()))
  if a.get_actor_label().startswith('WR_Path_'):
   a.modify();c.set_visibility(False,False);roads.append(a.get_actor_label())
before=json.loads((D/'Inventory.json').read_text())['Dev_WestlandRegion'];original={(r['label'],r['component']):r['materials']for r in before};bindings=[]
for a in actors.values():
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  prior=original.get((a.get_actor_label(),c.get_name()),[])
  for i in range(min(len(prior),c.get_num_materials())):
   m=c.get_material(i);path=m.get_path_name()if m else None
   if path!=prior[i]:bindings.append(dict(actor=a.get_actor_label(),component=c.get_name(),slot=i,before=prior[i],after=path))
assert len(roads)==17 and sum(x['actor'].startswith('WR_Terrain_')for x in bindings)==80;finish('Surfaces.json',dict(bindings=bindings,hidden_redundant_road_renderers=roads,collision_and_geometry_unchanged=True))
