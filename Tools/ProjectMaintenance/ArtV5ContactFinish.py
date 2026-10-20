"""QHD-driven final corrections: guaranteed shrub clearance and measured tabletop contacts, no other actor change."""
import unreal,json,math,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not(S/'ContactsFinished.json').exists();actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};routes=json.loads((R/'Art/World/VisualV2WorldArtV7/RouteField.json').read_text())['segments']
def closest(x,y):
 rows=[]
 for r in routes:
  a,b=r['a'],r['b'];dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));px=a[0]+t*dx;py=a[1]+t*dy;d=math.hypot(x-px,y-py);rows.append((d-r['base_half_width_cm'],px,py,r['base_half_width_cm']))
 return min(rows)
file=R/'Art/HealingHouse/ArtV5_ReviewFinish.json';j=json.loads(file.read_text());g=next(g for g in j['group_adjustments']if g['label']=='ArtV4_Edge_Shrubs');a=actors['ArtV4_Edge_Shrubs'];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);rows=[]
for i,row in enumerate(g['changed_instances']):
 t=c.get_instance_transform(i,True);before=t.translation.to_tuple();x,y=t.translation.x,t.translation.y
 for attempt in range(8):
  edge,px,py,half=closest(x,y)
  if edge>=140:break
  dx=x-px;dy=y-py;length=max(.01,math.hypot(dx,dy));x=px+dx/length*(half+145+(i%4)*17);y=py+dy/length*(half+145+(i%4)*17)
 assert closest(x,y)[0]>=140,(i,x,y);t.translation=unreal.Vector(x,y,.25);c.update_instance_transform(i,t,True,True,True);row['after']['position']=t.translation.to_tuple();rows.append({'index':i,'before':before,'after':t.translation.to_tuple(),'minimum_center_to_road_edge_cm':closest(x,y)[0]})
moves=[]
for label,x,y,z in [('ArtV5_HerbWorkBooks',16535,883,82.32),('ArtV5_BedsideRemedies',16590,905,84),('ArtV5_ReadingBooks',16805,268,46.06)]:
 a=actors[label];before=a.get_actor_location().to_tuple();a.set_actor_location(unreal.Vector(x,y,z),False,True);moves.append({'actor':a.get_name(),'label':label,'before':before,'after':a.get_actor_location().to_tuple()})
j['qhd_safety_finish']='All 23 shrub centers projected outside minimum 140 cm from route edge, replacing the draft inward shift.';file.write_text(json.dumps(j,indent=2));interior=R/'Art/HealingHouse/ArtV5_Interior.json';I=json.loads(interior.read_text())
for row in I['new_actors']:
 for move in moves:
  if row['actor']==move['actor']:row['position']=move['after']
interior.write_text(json.dumps(I,indent=2));assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');record={'passed':True,'shrub_clearance':rows,'new_prop_contacts':moves,'table_top_cm':{'reading_table':47.74,'herbal_table':84.0},'old_signatures_changed_only_for':[actors['ArtV4_Edge_Shrubs'].get_name()]+[m['actor']for m in moves]};(R/'Art/HealingHouse/ArtV5_Contacts.json').write_text(json.dumps(record,indent=2));(S/'ContactsFinished.json').write_text(json.dumps(record,indent=2))
# Replace only our new V5 signature entries for the four explicitly measured corrections.
import sys
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canonical(v):
 if isinstance(v,dict):
  d={k:canonical(x)for k,x in v.items()}
  if 'components'in d:d['components']=sorted([c for c in d['components']if not(c['name']=='NPCStaticVisual'and c['props'].get('static_mesh')in[None,'None'])],key=lambda c:c['name'])
  return d
 if isinstance(v,list):return[canonical(x)for x in v]
 if isinstance(v,float)and v==0:return 0.0
 return v
p=R/'Tools/ProjectMaintenance/ArtV5Signatures.json';old=json.loads(p.read_text());now=canonical(scene(w));new={n:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()for n,v in now['actors'].items()};assert old['world_settings']==now['world_settings']and set(old['actors'])==set(new);changed={n for n in new if new[n]!=old['actors'][n]};assert changed==set(record['old_signatures_changed_only_for']),changed;old['actors']=new;p.write_text(json.dumps(old,indent=2));unreal.log('ART_V5_CONTACTS_FINISHED')
