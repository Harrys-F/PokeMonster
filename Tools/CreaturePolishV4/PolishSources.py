"""Targeted new source variants; original vertices/UV/rest poses/actions retained unless listed.
Never overwrite an original or an existing candidate. Export animation-only FBX except Idle.
"""
import bpy,json,hashlib,sys,math
from pathlib import Path
from mathutils import Quaternion,Vector
R=Path(__file__).resolve().parents[2];name=sys.argv[sys.argv.index('--')+1];assert name in ['Enton','Nebulak','Glurak'];A=R/'Art/Characters/Creatures'/name;original=A/'Source'/(name+'_Meshy_V1.blend');source=A/'Source'/(name+'_PolishV4.blend');exports=A/'Exports/PolishV4';assert not source.exists() and not exports.exists();baseline=json.loads((R/'Saved/CreaturePolishV4/InitialState.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert digest(original)==baseline['original_files'][str(original.relative_to(R))]
bpy.ops.wm.open_mainfile(filepath=str(original));bpy.context.preferences.filepaths.save_version=0;body=bpy.data.objects[name+'_Body'];rig=bpy.data.objects[name+'_Rig'];scene=bpy.context.scene;oldverts=[tuple(v.co)for v in body.data.vertices];olduvs=[tuple(v.uv)for v in body.data.uv_layers.active.data];changes={};scene.frame_set(1)
if name=='Enton':
 changed=[]
 for v in body.data.vertices:
  x,y,z=v.co
  if y<=.14 or z>=.30:continue
  t=max(0.,min(1.,(y-.14)/.08));t=t*t*(3-2*t)
  if t<=0:continue
  before={body.vertex_groups[g.group].name:g.weight for g in v.groups};weights={k:w*(1-t)for k,w in before.items()};weights['tail_base']=weights.get('tail_base',0)+t
  for g in body.vertex_groups:g.remove([v.index])
  for k,w in weights.items():
   if w>1e-8:body.vertex_groups[k].add([v.index],w,'REPLACE')
  changed.append(v.index)
 changes['tail_weight_vertices']=len(changed)
else:
 color=body.data.color_attributes.new(name='PolishV4',type='FLOAT_COLOR',domain='CORNER');body.data.color_attributes.active_color=color
 if name=='Nebulak':
  # Only vertices already assigned to peripheral gas bones deform/fade; central face stays solid.
  masks={v.index:sum(g.weight for g in v.groups if body.vertex_groups[g.group].name.startswith('gas_'))for v in body.data.vertices}
  for i,loop in enumerate(body.data.loops):color.data[i].color=(masks[loop.vertex_index],0,0,1)
  changes['gas_vertices']=sum(m>.05 for m in masks.values())
 else:
  material=body.data.materials[0];base=next(n for n in material.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image
  width,height=base.size;pixels=list(base.pixels);n=0
  for poly in body.data.polygons:
   # Mesh faces have independent UV islands; color by the actual rear-facing membrane, not global TwoSidedSign.
   for i in poly.loop_indices:
    v=body.data.vertices[body.data.loops[i].vertex_index];uv=body.data.uv_layers.active.data[i].uv;idx=(int(uv.y%1*(height-1))*width+int(uv.x%1*(width-1)))*4;r,g,b=pixels[idx:idx+3]
    wing=abs(v.co.x)>.40 and v.co.z>.80 and poly.material_index==0
    rear=poly.normal.y>.10
    membrane=(b>r*1.08 or g>r*1.18) and max(r,g,b)<.8
    mask=1. if wing and rear and membrane else 0.;color.data[i].color=(mask,0,0,1);n+=mask>0
  assert n>100,'No proven rear membrane selection; stop before exporting';changes['rear_wing_corners']=n
 # Bake targeted, loop-continuous additional wing/gas movement into only these bone channels.
 for action in bpy.data.actions:
  if not action.name.startswith(name+'_'):continue
  rig.animation_data.action=action;start,end=map(int,action.frame_range);role=action.name.split('_')[-1];bones=[p for p in rig.pose.bones if p.name.startswith('wing_')or(name=='Nebulak'and p.name.startswith('gas_'))];cache={}
  for f in range(start,end+1):
   scene.frame_set(f);cache[f]={p.name:(p.location.copy(),p.rotation_quaternion.copy(),p.scale.copy())for p in bones}
  duration=(end-start)/30
  for f in range(start,end+1):
   scene.frame_set(f);u=(f-start)/(end-start);phase=u*math.tau
   for p in bones:
    loc,q,scale=cache[f][p.name];p.location=loc;p.rotation_quaternion=q;p.scale=scale
    if name=='Nebulak':
     index=int(p.name.split('_')[-1]);breathe=.024*math.sin(phase+index*.67)+.012*math.sin(phase*2-index*.48);p.scale=scale*(1+breathe)
    else:
     side=1 if p.name.endswith('_L')else -1;factor=.55 if 'tip' in p.name else 1.;amp={'Idle':.05,'Walk':.045,'Run':.075,'Attack':.17,'Hit':.045,'Happy':.10,'Faint':.025}.get(role,.04);wave=math.sin(phase)*amp*factor
     rest=p.bone.matrix_local.to_quaternion();delta=Quaternion(Vector((0,1,0)),side*wave)@Quaternion(Vector((0,0,1)),side*(.03+wave*.4));p.rotation_quaternion=q@(rest.inverted()@delta@rest)
    p.keyframe_insert(data_path='location',frame=f);p.keyframe_insert(data_path='rotation_quaternion',frame=f);p.keyframe_insert(data_path='scale',frame=f)
 changes['modified_bone_channels']='peripheral gas scales'if name=='Nebulak'else'wing rotations only'
assert oldverts==[tuple(v.co)for v in body.data.vertices]and olduvs==[tuple(v.uv)for v in body.data.uv_layers.active.data]
exports.mkdir(parents=True,exist_ok=False);roles=['Idle']if name=='Enton'else['Idle','Walk','Run','Attack','Hit','Faint','Happy'];minima={};receipts=[]
for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
 rig.animation_data.action=bpy.data.actions[name+'_'+role];start,end=map(int,rig.animation_data.action.frame_range);zs=[]
 for frame in range(start,end+1):
  scene.frame_set(frame);ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ob.to_mesh();zs.append(min(v.co.z for v in me.vertices));ob.to_mesh_clear()
 minima[role]=dict(min_z_cm=min(zs)*100,max_min_z_cm=max(zs)*100)
 if role not in roles:continue
 scene.frame_start=start;scene.frame_end=end;scene.frame_set(start);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(role=='Idle');bpy.context.view_layer.objects.active=rig;dest=exports/(name+'_'+role+'.fbx');bpy.ops.export_scene.fbx(filepath=str(dest),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE',path_mode='AUTO',colors_type='LINEAR');receipts.append(dict(role=role,sha256=digest(dest),contains_mesh=role=='Idle'))
rig.animation_data.action=bpy.data.actions[name+'_Idle'];scene.frame_start=1;scene.frame_end=61;scene.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(source));assert digest(original)==baseline['original_files'][str(original.relative_to(R))]
(A/'PolishV4_Audit.json').write_text(json.dumps(dict(species=name,source=str(source.relative_to(R)),original_sha256=digest(original),source_sha256=digest(source),geometry_uv_rest_preserved=True,changes=changes,minima=minima,exports=receipts),indent=2));print('POLISH_SOURCE',name,json.dumps(changes),json.dumps(minima),flush=True)
