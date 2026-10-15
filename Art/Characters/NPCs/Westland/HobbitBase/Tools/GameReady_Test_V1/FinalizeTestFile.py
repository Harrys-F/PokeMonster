import bpy,json,hashlib
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];bpy.context.window.scene=s
s.render.filepath=str(P/'Previews/WorkingScene_Render.png')
s['GameReady_approved']=False;s['test_scope']='Head including hair and bounded upper torso only. QuadriFlow cancelled; triangle meshes are baking controls, not deformable topology.';s['comparison_instructions']='A: HighPoly visible, HeadHair/Torso/Context hidden. B: HighPoly hidden, HeadHair/Torso/Context visible. Context is still HighPoly.'
hp=s.objects['GRT_HighPoly_Reference'];hp.hide_render=False
for name in ['GRT_HeadHair','GRT_Torso','GRT_UnmodifiedContext']:
 o=s.objects[name];o.hide_render=True;o.hide_set(True);o['game_ready_approved']=False
for o in s.objects:o.select_set(False)
hp.select_set(True);bpy.context.view_layer.objects.active=hp;s.cycles.samples=12;s.render.resolution_x=1000;s.render.resolution_y=1000
q={'file':str(B/'Source/Hobbit_NPC_GameReady_Test_V1.blend'),'bake_use_cage':s.render.bake.use_cage,'bake_margin_pixels':s.render.bake.margin,'original_reference_material':hp.data.materials[0].name,'mesh_count':sum(o.type=='MESH' for o in s.objects),'armature_count':sum(o.type=='ARMATURE' for o in s.objects),'baked_material_count':sum(mat.name.startswith('GRT_Baked_') for mat in bpy.data.materials),'original_texture_hashes':[],'baked_texture_paths':[]}
for im in bpy.data.images:
 if im.packed_file:
  if im.name.startswith('GRT_'):q['baked_texture_paths'].append(bpy.path.abspath(im.filepath))
  else:q['original_texture_hashes'].append(hashlib.sha256(bytes(im.packed_file.data)).hexdigest())
expected={x['sha256'] for x in json.loads((B/'Review/4K_Base_V1/InputGLB.json').read_text())['extracted_images']};assert set(q['original_texture_hashes'])==expected
assert q['bake_use_cage'] and q['bake_margin_pixels']==2;assert q['mesh_count']==4 and q['armature_count']==0 and len(q['baked_texture_paths'])==10
bpy.ops.wm.save_as_mainfile(filepath=q['file']);(P/'FinalFile.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
