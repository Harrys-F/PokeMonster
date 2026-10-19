"""Reusable runtime-only V1/Merged/V2 authoring comparison; restores every scoped property."""
from pathlib import Path
import unreal,json
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2'
class Variants:
 def __init__(self,w):
  self.w=w;self.groups=[];self.ground=[];source=R/'Art/World/VisualV2WorldArtV2';self.inv=json.loads((source/'BaselineInstances.json').read_text());self.art=json.loads((source/'ArtCandidate.json').read_text());self.merged=json.loads((source/'MeshCandidates.json').read_text());by={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};self.assets={}
  for row in self.inv['groups']:
   c=by[row['actor']].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c.get_instance_count()==row['count'];self.groups.append((row,c));self.load(row['mesh'])
   for m in row['materials']:self.load(m)
  self.palette=self.load('/Game/Environment/VisualV2WorldArtV2/Materials/M_WAQ2_PlantVertexColour')
  for row in self.merged:self.load(row['candidate'])
  material_changes=json.loads((R/'Art/World/VisualV2WorldArtV1/HealingHouseDressing.json').read_text())['material_changes'];maps={r['old']:r['new'] for r in self.art['materials']}
  for row in material_changes:
   a=next(a for a in by.values() if a.get_actor_label()==row['label']);c=a.static_mesh_component;old=self.load(row['new']);new=self.load(maps[row['new']]);assert c.get_material(0) in [old,new];self.ground.append((c,old,new))
  self.pp=[(a,a.settings.export_text()) for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume)];self.light=[(c,c.get_editor_property('intensity'),c.get_world_transform().export_text()) for c in unreal.ObjectIterator(unreal.LightComponentBase) if c.get_world()==w];self.current=None
 def load(self,path):
  if path not in self.assets:self.assets[path]=unreal.load_asset(path);assert self.assets[path],path
  return self.assets[path]
 def apply(self,mode):
  assert mode in ['V1','Merged','V2'];merged=mode in ['Merged','V2'];isv2=mode=='V2';targets={(x['actor'],x['index']):x['transform'] for x in self.art['placements']};mergedpath={x['key']:x['candidate'] for x in self.merged}
  for row,c in self.groups:
   key=row['label'].removeprefix('WAQ1_');m=self.load(mergedpath[key]) if merged and key in mergedpath else self.load(row['mesh']);c.set_static_mesh(m);materials=[self.palette] if merged and key in mergedpath else [self.load(p) for p in row['materials']]
   if unreal.GameplayStatics.get_player_pawn(self.w,0):unreal.SystemLibrary.execute_console_command(self.w,'pm.WorldArt2.ClearMaterials '+row['actor'])
   else:c.set_editor_property('override_materials',[])
   for slot,material in enumerate(materials):c.set_material(slot,material)
   assert c.get_num_materials()==len(materials)
   c.set_forced_lod_model(row['forced_lod'])
   for i,old in enumerate(row['transforms']):
    t=unreal.Transform();t.import_text(targets[(row['actor'],i)] if isv2 else old);assert c.update_instance_transform(i,t,True,i==row['count']-1,True)
  for c,old,new in self.ground:c.set_material(0,new if isv2 else old)
  assert all(a.settings.export_text()==s for a,s in self.pp),'Postprocess changed'
  assert all(c.get_editor_property('intensity')==intensity and c.get_world_transform().export_text()==tf for c,intensity,tf in self.light),'Light settings changed'
  self.current=mode
