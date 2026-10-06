"""Neutral mesh-only proportion pass. Existing bones, skin weights, topology,
UVs, materials and animations are untouched. Basis + correction shape keys
make the volume pass reversible; the old source is never overwritten.
"""
import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
OUT=ROOT.parents[2]/'Saved/YoungTrainerProportions';OUT.mkdir(parents=True,exist_ok=True)
assert Path(bpy.data.filepath).name=='YoungTrainer_Reference_V1.blend'
scene=bpy.data.scenes['YoungTrainer_Reference_V1'];bpy.context.window.scene=scene
coll=bpy.data.collections['YT_Character'];arm=bpy.data.objects['YT_Rig']
assert all(b.matrix_basis==b.matrix_basis.__class__.Identity(4) for b in arm.pose.bones)
meshes=[o for o in coll.objects if o.type=='MESH'];assert len(meshes)==20
def snapshot():
 return {'bones':[(b.name,list(b.head_local),list(b.tail_local),b.parent.name if b.parent else None,b.use_deform) for b in arm.data.bones],
 'pose':[(b.name,list(b.rotation_quaternion),list(b.rotation_euler),list(b.location),list(b.scale),b.rotation_mode) for b in arm.pose.bones],
 'weights':{o.name:[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices] for o in meshes},
 'uv':{o.name:[list(d.uv) for d in o.data.uv_layers.active.data] for o in meshes},
 'faces':{o.name:[list(p.vertices) for p in o.data.polygons] for o in meshes},
 'material_links':{o.name:[m.name for m in o.data.materials] for o in meshes},
 'modifiers':{o.name:[(m.name,m.type,m.object.name,m.use_deform_preserve_volume) for m in o.modifiers if m.type=='ARMATURE'] for o in meshes}}
protected=snapshot();(OUT/'ProtectedBaseline.json').write_text(json.dumps(protected))
def lerp(z,points):
 if z<=points[0][0]:return points[0][1]+z-points[0][0]
 if z>=points[-1][0]:return points[-1][1]+z-points[-1][0]
 for (a,b),(c,d) in zip(points,points[1:]):
  if a<=z<=c:return b+(d-b)*(z-a)/(c-a)
def clamp(t):return max(0,min(1,t))
def head(p):
 x,y,z=p;f=lerp(z,[(1.03,.94),(1.14,.92),(1.20,.97),(1.335,1)])
 zz=lerp(z,[(1.03,1.070),(1.09,1.104),(1.15,1.130),(1.21,1.177),(1.27,1.247),(1.335,1.325)])
 return Vector((x*f,.012+(y-.012)*.82,zz))
def hair(p):
 x,y,z=p;a=math.atan2(x,-(y-.025));t=clamp((z-1.13)/.27)
 # Only broad silhouette irregularity, no additional locks/strands/details.
 f=.96+.052*math.sin(a*3+.6)+.033*math.cos(a*5-1.0)
 xx=x*f;yy=.025+(y-.025)*.83*f
 zz=z+.012*math.sin(a*3)*(1-t)*t-.010*max(0,-y/.15)*max(0,1-abs(z-1.245)/.06)
 # Pull the existing projecting fringe ends into the overall hair volume.
 # This edits their envelope only, without adding strand geometry.
 tip=clamp((-y-.12)/.05)*clamp((1.31-z)/.07)
 yy+=.024*tip;zz+=.018*tip
 return Vector((xx,yy,min(1.4,zz)))
def torso(p,part):
 x,y,z=p
 if part=='Vest':pts=[(.59,.55),(.65,.62),(.70,.735),(.78,.817),(.85,.879),(.92,.937),(.984,1.024)]
 else:pts=[(.62,.604),(.66,.728),(.74,.786),(.82,.853),(.90,.918),(.96,.988),(1.006,1.035),(1.04,1.062)]
 factor=lerp(z,[(.59,.99),(.70,.93),(.85,.87),(1.02,.84)])
 return Vector((x*factor,y*.88,lerp(z,pts)))
old=[Vector((.150,0,.977083)),Vector((.258,0,.823541)),Vector((.328,0,.686949))]
new=[Vector((.130,0,1.020)),Vector((.227,0,.803)),Vector((.290,0,.650))]
def arm_map(p):
 s=1 if p.x>=0 else -1;q=Vector((abs(p.x),p.y,p.z));candidates=[]
 for i in range(2):
  v=old[i+1]-old[i];t=(q-old[i]).dot(v)/v.length_squared;tc=clamp(t)
  candidates.append(((q-(old[i]+v*tc)).length_squared,i,tc))
 _,i,t=min(candidates);v=(old[i+1]-old[i]);w=(new[i+1]-new[i]);c=old[i]+v*t
 rotation=v.rotation_difference(w);offset=rotation@(q-c)
 offset.x*=.80;offset.y*=.93
 if i==0:offset.z*=.55+.45*clamp(t/.20)
 result=new[i]+w*t+offset;result.x*=s;return result
def hand(p):
 s=1 if p.x>=0 else -1;oldc=Vector((s*.347,-.004,.650));newc=Vector((s*.312,-.004,.609))
 return newc+(p-oldc)*1.10
def pants(p,s):
 x,y,z=p
 oldcx=lerp(z,[(.23,.108),(.38,.100),(.51,.094),(.68,.083)])
 newcx=lerp(z,[(.23,.123),(.38,.119),(.51,.104),(.68,.078)])
 width=lerp(z,[(.23,.96),(.28,.97),(.33,1.06),(.38,1.32),(.44,1.10),(.51,1.02),(.58,.90),(.64,.83),(.68,.87)])
 depth=lerp(z,[(.23,1),(.38,1.16),(.51,1.02),(.68,.95)])
 zz=lerp(z,[(.23,.277),(.28,.320),(.38,.412),(.44,.466),(.51,.535),(.58,.610),(.64,.686),(.68,.735)])
 center_depth=lerp(z,[(.23,0),(.38,-.020),(.51,.010),(.68,.008)])
 return Vector((s*newcx+(x-s*oldcx)*width,y*depth+center_depth,zz))
def boots(p):
 s=1 if p.x>=0 else -1;x,y,z=p
 dx=(x-s*.108)*1.30;yy=y*1.13
 # Broad toe-out stance, preserving planted soles and the existing topology.
 ang=s*math.radians(10);xx=dx*math.cos(ang)-yy*math.sin(ang);yy=dx*math.sin(ang)+yy*math.cos(ang)
 zz=lerp(z,[(0,0),(.026,.030),(.10,.119),(.1745,.207)])
 return Vector((s*.123+xx,yy,zz))
def pack(p):
 x,y,z=p
 fullness=lerp(z,[(.667,.91),(.76,1),(.87,1.01),(.99,.94),(1.06,.94)])
 # A shared soft envelope keeps existing pockets and straps together.
 back_bulge=.010*math.sin(math.pi*clamp((z-.667)/.323))*max(0,1-(x/.21)**2)
 return Vector((x*1.18*fullness,.08+(y-.105)*.60+back_bulge,.600+(z-.666)*1.13))
def islands(o):
 adjacent=[[] for _ in o.data.vertices]
 for e in o.data.edges:a,b=e.vertices;adjacent[a].append(b);adjacent[b].append(a)
 found=set();result={}
 for v in o.data.vertices:
  if v.index in found:continue
  todo=[v.index];found.add(v.index);ids=[]
  while todo:
   k=todo.pop();ids.append(k)
   for n in adjacent[k]:
    if n not in found:found.add(n);todo.append(n)
  c=sum((o.data.vertices[k].co for k in ids),Vector())/len(ids)
  for k in ids:result[k]=c
 return result
for o in meshes:
 assert o.data.shape_keys is None
 centers=islands(o);o.shape_key_add(name='Basis',from_mix=False);key=o.shape_key_add(name='Proportions_Silhouette_V2',from_mix=False)
 part=o['part']
 for v,k in zip(o.data.vertices,key.data):
  p=v.co.copy();x,y,z=p;s=1 if x>=0 else -1;c=centers[v.index]
  names={o.vertex_groups[g.group].name for g in v.groups if g.weight>.95}
  if part in ['Head','Face','Eyes']:q=head(p)
  elif part=='Hair':q=hair(p)
  elif part=='Hands':q=hand(p)
  elif part=='Wristbands':q=arm_map(p)
  elif part=='Body':
   if 'head' in names:q=head(p)
   elif abs(c.x)>.20:q=arm_map(p)
   else:q=Vector((x*.93,y*.89,lerp(z,[(.997,1.037),(1.030,1.062),(1.082,1.088)])))
  elif part=='Shirt':q=arm_map(p) if abs(c.x)>.16 else torso(p,part)
  elif part=='Vest':q=torso(p,part)
  elif part=='Pants':q=pants(p,1 if c.x>=0 else -1)
  elif part=='Boots':q=boots(p)
  elif part=='Socks':q=Vector((s*.123+(x-s*.108)*.93,y*.96,lerp(z,[(.144,.177),(.174,.207),(.237,.283)])))
  elif part=='Scarf':q=Vector((x*.92,y*.87,1.075+(z-1.06)*1.10))
  elif part=='Belt':q=Vector((x*.93,y*.87,.735+(z-.660)*.90))
  elif part=='Pouches':q=Vector((s*.188+(x-s*.191)*1.03,y*.90,z+.075))
  elif part=='Pendant':q=Vector((x*.93,y*.70,lerp(z,[(.840,.827),(.875,.865),(1.015,1.05)])))
  elif part=='Harness':
   q=torso(p,'Shirt')
   if y>.04:q.y=.075+(y-.10)*.60
  elif part=='Backpack':q=pack(p)
  elif part=='Bedroll':q=Vector((x*1.08,.157+(y-.213)*1.04,.950+(z-1.008)*1.08))
  elif part=='Equipment':q=pack(p) if 'chest' in names else Vector((s*.225+(x-s*.225)*1.03,y*.9,z+.075))
  else:raise RuntimeError(part)
  k.co=q
 key.value=1;o['proportion_pass']='V2 mesh-only reversible correction; rig unchanged and not refit.'
assert snapshot()==protected,'Protected rig/material/UV/weights/topology changed.'
# Reference images are verbatim crops with one common pixel scale, not generated art.
refs=bpy.data.collections.new('REF_CHARACTER');scene.collection.children.link(refs)
alignment=json.loads((ROOT/'Reference/Orthographic/Alignment.json').read_text());scale=alignment['scale_m_per_pixel']
for row in alignment['views']:
 image=bpy.data.images.load(str(ROOT/'Reference/Orthographic'/row['file']),check_existing=True);image.pack();image.filepath='//../Reference/Orthographic/'+row['file']
 ob=bpy.data.objects.new('REF_Sheet_'+row['name'],None);refs.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=image
 w,h=image.size;l,t,r,b=row['crop'];ob.empty_display_size=max(w,h)*scale
 ob.empty_image_offset=(-(row['axis_pixel_global']-l)/w,-(b-row['ground_pixel_global'])/h)
 n=Vector(row['normal']).normalized();ob.rotation_euler=n.to_track_quat('Z','Y').to_euler();ob.location=n*.40
 ob.color=(1,1,1,.40);ob.use_empty_image_alpha=True;ob.empty_image_depth='FRONT';ob.empty_image_side='FRONT';ob.show_empty_image_orthographic=True;ob.show_empty_image_perspective=False;ob.show_empty_image_only_axis_aligned=True
 ob.lock_location=(True,True,True);ob.lock_rotation=(True,True,True);ob.lock_scale=(True,True,True);ob.hide_select=True;ob['scale_m_per_pixel']=scale;ob['ground_z']=0.0;ob['reference_view']=row['name'];ob['crop_original_pixels']=row['crop'];ob['use']='Alignment reference only; no runtime mesh.'
scene['proportion_pass']='Mesh-only V2; 1.4 m silhouette, untouched existing rig/materials/UVs.'
scene['reference_side_convention']='Blender RIGHT (+X) shows supplied LEFT; Blender LEFT (-X) supplied RIGHT, for -Y facing character.'
for o in bpy.data.collections['YT_ReviewOnly'].objects:o.hide_set(True)
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  space=a.spaces.active;space.shading.type='SOLID';space.shading.color_type='SINGLE';space.shading.single_color=(.58,.58,.58);space.overlay.show_bones=False
  space.region_3d.view_rotation=Vector((0,-1,0)).to_track_quat('Z','Y');space.region_3d.view_location=(0,0,.7);space.region_3d.view_distance=2.3;space.region_3d.view_perspective='ORTHO'
bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=bpy.data.objects['YT_Head']
bpy.context.view_layer.update()
path=ROOT/'Source/YoungTrainer_Proportions_V2.blend';assert path.name!='YoungTrainer_Reference_V1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path),check_existing=False)
print('SAVED',path,'REFERENCE_EMPTIES',len(refs.objects),'PROTECTED_DATA_UNCHANGED',True)
