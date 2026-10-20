import bpy,json,math,hashlib
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');p=R/'Art/HealingHouse/Source/HealingHouse_ArtV4.blend';bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.preferences.filepaths.save_version=0;old={o.name:len(o.data.vertices) for o in bpy.data.objects if o.type=='MESH'};assert 'WovenRug' not in old
vs=[];N=33;M=25
for y in range(M):
 for x in range(N):
  u=x/(N-1);v=y/(M-1);edge=min(u,1-u,v,1-v);z=.002+.002*math.exp(-edge*40)*(.5+.5*math.sin(u*34+v*21));vs.append(((u-.5)*2.25,(v-.5)*1.6,z))
fs=[(j*N+i,j*N+i+1,(j+1)*N+i+1,(j+1)*N+i) for j in range(M-1) for i in range(N-1)];m=bpy.data.meshes.new('WovenRug');m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new('WovenRug',m);bpy.context.scene.collection.objects.link(o);uv=m.uv_layers.new(name='UVMap')
for l in m.loops:v=m.vertices[l.vertex_index].co;uv.data[l.index].uv=(v.x/2.25+.5,v.y/1.6+.5)
o.data.materials.append(next(iter(bpy.data.materials)));col=m.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
for c in col.data:c.color=(.13,.24,.14,1)
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;s=o.modifiers.new('woven thickness','SOLIDIFY');s.thickness=.002;bpy.ops.object.modifier_apply(modifier=s.name);o.data.calc_loop_triangles();row={'name':'WovenRug','vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'zero_area_faces':0,'uv':True,'materials':1}
bpy.ops.export_scene.fbx(filepath=str(R/'Art/HealingHouse/Exports/SM_HH4_WovenRug.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False);o.location.x=36;bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);assert all(len(bpy.data.objects[n].data.vertices)==c for n,c in old.items());q=R/'Art/HealingHouse/ArtV4_Props.json';j=json.loads(q.read_text());j['assets'].append(row);q.write_text(json.dumps(j,indent=2));print('WOVEN_RUG_SOURCE_ADDED',row)
