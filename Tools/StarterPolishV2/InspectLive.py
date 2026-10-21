"""Read-only asset inventory. Outputs only to ignored Saved/."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();rows=[]
for name in ['Zunderlauf','Schiggy','Bisasam']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);p=s.get_visuals().presentation;mesh=p.mesh
 rows.append({'species':name,'id':str(s.get_internal_id()),'profile':p.get_path_name(),'height_cm':p.reference_size_cm,'mesh':mesh.get_path_name(),'skeleton':mesh.skeleton.get_path_name(),'lods':unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem).get_lod_count(mesh),'materials':[x.material_interface.get_path_name()for x in mesh.materials],'clips':{str(k):{'asset':v.get_path_name(),'duration':v.get_play_length()}for k,v in p.clips.items()},'textures':[]})
 for typ in ['BaseColor','Normal','MetallicRoughness']:
  path='/Game/Characters/Creatures/'+name+('/MeshyV1/Textures/T_Glumanda_'if name=='Zunderlauf'else'/MeshyV1/Textures/T_'+name+'_')+typ
  t=unreal.load_asset(path)
  if t:rows[-1]['textures'].append({'path':t.get_path_name(),'class':t.get_class().get_name(),'size':[t.blueprint_get_size_x(),t.blueprint_get_size_y()],'mips':str(t.get_editor_property('mip_gen_settings')),'lod_bias':t.get_editor_property('lod_bias'),'max_size':t.get_editor_property('max_texture_size'),'filter':str(t.get_editor_property('filter'))})
(R/'Saved/StarterPolishV2/LiveInventory.json').write_text(json.dumps(rows,indent=2))
