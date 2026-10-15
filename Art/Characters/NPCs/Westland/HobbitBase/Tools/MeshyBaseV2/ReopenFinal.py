import bpy,json,hashlib
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];o=s.objects['HNM2_Body'];r=s.objects['HNM2_Rig'];images=[n.image for n in o.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and n.image];tex=[]
for im in images:
 p=Path(bpy.path.abspath(im.filepath));kind=next(k for k in ['BaseColor','ORM','Normal'] if k in im.name);old=B/'Textures/MeshyBaseV1'/('T_Hobbit_MeshyBase_'+kind+'.png')
 tex.append({'image':im.name,'path':str(p),'exists':p.exists(),'packed':bool(im.packed_file),'packed_filenames':[pf.filepath for pf in im.packed_files],'packed_matches_disk':bytes(im.packed_file.data)==p.read_bytes(),'texture_same_as_V1':p.read_bytes()==old.read_bytes()})
result={'opened_source':bpy.data.filepath,'body_height_m':max(v.co.z for v in o.data.vertices)-min(v.co.z for v in o.data.vertices),'minimum_z_m':min(v.co.z for v in o.data.vertices),'units':s.unit_settings.system,'unit_scale':s.unit_settings.scale_length,'fps':s.render.fps,'mesh_objects':sum(q.type=='MESH' for q in s.objects),'rigs':sum(q.type=='ARMATURE' for q in s.objects),'bones':len(r.data.bones),'rest_pose':r.data.pose_position,'actions':[a.name for a in bpy.data.actions if a.name.startswith('HNM2_')],'weights_groups':len(o.vertex_groups),'textures':tex,'external_library_model_data':[q.name for q in [o,o.data,r,r.data,*o.data.materials,*images] if q.library]}
(B/'Review/MeshyBaseV2/ReopenFinal.json').write_text(json.dumps(result,indent=2));print(result);assert abs(result['body_height_m']-1.4)<1e-6;assert result['minimum_z_m']==0;assert len(result['actions'])==3;assert len(images)==3;assert all(t['packed_matches_disk'] and t['texture_same_as_V1'] for t in tex);assert not result['external_library_model_data']

assert all(all(name for name in t['packed_filenames']) for t in tex)
