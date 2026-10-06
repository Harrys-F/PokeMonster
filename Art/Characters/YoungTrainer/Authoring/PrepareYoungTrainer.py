"""Phases 8–11: curve conversion, quad cleanup, palette UV atlas and FK prep.
The palette atlas intentionally shares repeatable material tiles, not lightmap UVs.
"""
import bpy,bmesh,numpy as np,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
COLORS=json.loads((ROOT/'Authoring/Palette.json').read_text())
scene=bpy.context.scene;coll=bpy.data.collections['YT_Character']
assert Path(bpy.data.filepath).name=='05_LikenessPolish.blend', 'Prepare only the unrigged likeness checkpoint.'
PARTS=[o for o in coll.objects if o.type in ['MESH','CURVE']]
root=bpy.data.objects['YT_CharacterRoot']
# Convert only this task's authored ornament curves, then recalculate normals.
for o in list(PARTS):
 if o.type=='CURVE':
  o['uv_generated']=True
  o.data.use_fill_caps=True
  for sp in list(o.data.splines):
   if sp.type=='POLY' and len(sp.points)>2 and (sp.points[0].co-sp.points[-1].co).length<.000001:
    pts=[tuple(p.co) for p in sp.points][:-1];ns=o.data.splines.new('POLY');ns.points.add(len(pts)-1)
    for p,co in zip(ns.points,pts):p.co=co
    ns.use_cyclic_u=True;o.data.splines.remove(sp)
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
  o['part']=o.get('part','Equipment');o['rig_mode']=o.get('rig_mode','torso')
 bpy.context.view_layer.update()
for o in PARTS:
 if o.type!='MESH':continue
 if o.get('uv_generated'):
  for uv in list(o.data.uv_layers):o.data.uv_layers.remove(uv)
 if o.name.startswith(('YT_ScarfFront','YT_ScarfTail','YT_ShirtCollar','YT_VestLeaf_','YT_PackLeaf_')):
  m=o.modifiers.new('Authored fabric thickness','SOLIDIFY');m.thickness=.0015;bpy.context.view_layer.objects.active=o;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.ops.object.modifier_apply(modifier=m.name)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 for p in o.data.polygons:p.use_smooth=True
# Normalize geometry in metres, not a negative/global object scale.
height=max(v.co.z for o in PARTS for v in o.data.vertices);zs=1.4/height
for o in PARTS:
 for v in o.data.vertices:v.co.z*=zs
 o.data.update()
scene['height_normalization']=zs
# Authored soft color fields, fabric/wood-like brush strokes: no downloaded maps.
cols=8;rows=4;tile=256;W=cols*tile;H=rows*tile
palette=list(COLORS);pixels=np.ones((H,W,4),dtype=np.float32);orm=np.ones((H,W,4),dtype=np.float32)
x=np.arange(tile,dtype=np.float32)[None,:]/(tile-1);y=np.arange(tile,dtype=np.float32)[:,None]/(tile-1)
for i,n in enumerate(palette):
 cx=i%cols;cy=i//cols;rgb=np.array(COLORS[n][:3],dtype=np.float32)
 broad=.93+.08*y+.035*np.sin(x*9+y*3)+.025*np.sin(x*21-y*8)
 amplitude=.035 if n not in ['Hair','HairLight','Leather','LeatherLight','Blue','Cream','Olive'] else .065
 brush=amplitude*np.sin(x*57+1.4*np.sin(y*17))*.55+amplitude*np.sin(x*19+y*13)*.45
 field=broad+brush
 if n in ['EyeWhite','Pupil','Highlight']:field=np.ones_like(field)
 pixels[cy*tile:(cy+1)*tile,cx*tile:(cx+1)*tile,:3]=np.clip(field[:,:,None]*rgb,0,1)
 if n=='Skin':
  blush=np.exp(-((x-.08)**2/.002+(y-.36)**2/.007))+np.exp(-((x-.92)**2/.002+(y-.36)**2/.007))
  area=pixels[cy*tile:(cy+1)*tile,cx*tile:(cx+1)*tile,:3];area[:,:,0]+=blush*.025;area[:,:,1]-=blush*.018
 orm[cy*tile:(cy+1)*tile,cx*tile:(cx+1)*tile,1]=.65 if n in ['Skin','Iris','EyeWhite'] else .83
 orm[cy*tile:(cy+1)*tile,cx*tile:(cx+1)*tile,2]=.25 if n=='Brass' else 0
 if n=='Brass':orm[cy*tile:(cy+1)*tile,cx*tile:(cx+1)*tile,1]=.58
pixels[:,:,:3]=np.where(pixels[:,:,:3]<=.0031308,pixels[:,:,:3]*12.92,1.055*np.power(pixels[:,:,:3],1/2.4)-.055)
base=bpy.data.images.new('YT_PaintedBaseColor',width=W,height=H,alpha=True);base.colorspace_settings.name='sRGB';base.pixels.foreach_set(pixels.ravel());base.filepath_raw=str(ROOT/'Textures/YT_PaintedBaseColor.png');base.file_format='PNG';base.save();base.pack()
mask=bpy.data.images.new('YT_ORM',width=W,height=H,alpha=True);mask.colorspace_settings.name='Non-Color';mask.pixels.foreach_set(orm.ravel());mask.filepath_raw=str(ROOT/'Textures/YT_ORM.png');mask.file_format='PNG';mask.save();mask.pack()
base.filepath='//../Textures/YT_PaintedBaseColor.png';mask.filepath='//../Textures/YT_ORM.png'
# Encode palette values as sRGB for the sRGB image texture; ORM stays linear.
mat=bpy.data.materials.new('YT_IllustratedAtlas');mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');p=nodes.new('ShaderNodeBsdfPrincipled');tex=nodes.new('ShaderNodeTexImage');tex.image=base;tex.interpolation='Linear';rm=nodes.new('ShaderNodeTexImage');rm.image=mask;sep=nodes.new('ShaderNodeSeparateColor');sep.mode='RGB'
L=mat.node_tree.links;L.new(tex.outputs['Color'],p.inputs['Base Color']);L.new(rm.outputs['Color'],sep.inputs['Color']);L.new(sep.outputs['Green'],p.inputs['Roughness']);L.new(sep.outputs['Blue'],p.inputs['Metallic']);L.new(p.outputs['BSDF'],out.inputs['Surface'])
# Give authored lofts proper seam UVs; project compact ornaments where appropriate.
for o in PARTS:
 if not o.data.uv_layers:
  uv=o.data.uv_layers.new(name='UVMap');vs=o.data.vertices
  mins=np.array([min(v.co[k] for v in vs) for k in range(3)]);maxs=np.array([max(v.co[k] for v in vs) for k in range(3)]);span=maxs-mins
  axes=np.argsort(span)[-2:]
  for loop in o.data.loops:
   co=vs[loop.vertex_index].co;uv.data[loop.index].uv=[(co[k]-mins[k])/max(span[k],.00001) for k in axes]
 else:uv=o.data.uv_layers.active
 # Seam correction before moving into the tile.
 for poly in o.data.polygons:
  ids=list(poly.loop_indices);us=[uv.data[j].uv.x for j in ids]
  if max(us)-min(us)>.65:
   for j in ids:
    if uv.data[j].uv.x<.25:uv.data[j].uv.x+=1
 idx=palette.index(o['palette']);cx=idx%cols;cy=idx//cols
 for d in uv.data:
  u,v=d.uv;d.uv=((cx*tile+4+u*(tile-8))/W,(cy*tile+4+v*(tile-8))/H)
 o.data.materials.clear();o.data.materials.append(mat)
# Basic FK skeleton; animation-friendly rest A-pose. No automatic-heat black box.
armdata=bpy.data.armatures.new('YT_Skeleton');arm=bpy.data.objects.new('YT_Rig',armdata);coll.objects.link(arm);arm.parent=root;arm.show_in_front=True
bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
bones={}
def bone(n,h,t,parent=None):
 b=armdata.edit_bones.new(n);b.head=(h[0],h[1],h[2]*zs);b.tail=(t[0],t[1],t[2]*zs)
 if parent:b.parent=bones[parent]
 b.use_deform=n!='root';bones[n]=b
bone('root',(0,0,0),(0,0,.12));bone('pelvis',(0,0,.64),(0,0,.74),'root');bone('spine',(0,0,.74),(0,0,.88),'pelvis');bone('chest',(0,0,.88),(0,0,.99),'spine');bone('neck',(0,0,.99),(0,0,1.075),'chest');bone('head',(0,0,1.075),(0,0,1.30),'neck')
for side in [-1,1]:
 s='L' if side==1 else 'R'
 bone('clavicle.'+s,(0,0,.974),(side*.15,0,.98),'chest')
 bone('upperarm.'+s,(side*.15,0,.98),(side*.258,0,.826),'clavicle.'+s)
 bone('forearm.'+s,(side*.258,0,.826),(side*.328,0,.689),'upperarm.'+s)
 bone('hand.'+s,(side*.328,0,.689),(side*.379,0,.62),'forearm.'+s)
 for f in range(4):
  z=.635+(f-1.5)*.014;x=side*(.366+(.003 if f in [1,2] else 0))
  bone('finger%d.'%f+s,(x,-.017,z),(x+side*.022,-.02,z-.033),'hand.'+s)
 bone('thumb.'+s,(side*.325,-.025,.668),(side*.348,-.047,.64),'hand.'+s)
 bone('thigh.'+s,(side*.087,0,.64),(side*.105,0,.375),'pelvis')
 bone('shin.'+s,(side*.105,0,.375),(side*.108,0,.235),'thigh.'+s)
 bone('foot.'+s,(side*.108,0,.235),(side*.108,-.09,.05),'shin.'+s)
 bone('toe.'+s,(side*.108,-.07,.05),(side*.108,-.145,.045),'foot.'+s)
bpy.ops.object.mode_set(mode='OBJECT')
def clamp(x):return max(0,min(1,x))
def weights(o,v):
 z=v.co.z/zs;mode=o['rig_mode'];part=o['part'];s='L' if v.co.x>0 else 'R'
 if mode=='head':return {'head':1}
 if mode=='neck':return {'neck':1}
 if mode=='chest':return {'chest':1}
 if mode=='pelvis':return {'pelvis':1}
 if mode.startswith('foot'):return {mode:1}
 if mode.startswith('hand'):
  suf=mode.split('.')[-1]
  if o.name.startswith('YT_Finger_'):return {'finger'+o.name[-1]+'.'+suf:1}
  if o.name.startswith('YT_Thumb_'):return {'thumb.'+suf:1}
  return {mode:1}
 if mode.startswith('leg'):
  s=mode.split('.')[-1];k=clamp((z-.335)/.08);hip=clamp((z-.59)/.065)
  return {'pelvis':hip,'thigh.'+s:(1-hip)*k,'shin.'+s:(1-hip)*(1-k)}
 if mode.startswith('arm') or mode.startswith('forearm'):
  s=mode.split('.')[-1];k=clamp((z-.788)/.076);return {'upperarm.'+s:k,'forearm.'+s:1-k}
 if z<.74:
  t=clamp((z-.66)/.08);w={'pelvis':1-t,'spine':t}
 else:
  t=clamp((z-.80)/.11);w={'spine':1-t,'chest':t}
 if part in ['Shirt','Vest'] and abs(v.co.x)>.145 and z>.85:
  a=clamp((abs(v.co.x)-.145)/.055)*.7;w={n:val*(1-a) for n,val in w.items()};w['upperarm.'+s]=a
 return w
for o in PARTS:
 groups={b.name:o.vertex_groups.new(name=b.name) for b in armdata.bones if b.use_deform}
 for v in o.data.vertices:
  ww=weights(o,v);total=sum(ww.values());assert total>.999
  for n,val in ww.items():
   if val>.00001:groups[n].add([v.index],val/total,'REPLACE')
 mod=o.modifiers.new('YT_Armature','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=False
 o.parent=arm
# Consolidate by semantic part; vertex groups and UVs remain editable.
grouped={}
for o in PARTS:grouped.setdefault(o['part'],[]).append(o)
final=[]
for part,objs in grouped.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0]
 if len(objs)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='YT_'+part;o.data.name='YT_'+part+'_Mesh';o['part']=part
 # Joining repeats identical atlas slots; collapse to one draw material.
 o.data.materials.clear();o.data.materials.append(mat)
 for poly in o.data.polygons:poly.material_index=0
 final.append(o)
PARTS=final
scene['palette_uv_shared']='Intentional per-material tile sharing; not unique lightmap/bake UVs.'
scene.camera=bpy.data.objects['YT_ReviewThreeQuarter']
bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  a.spaces.active.region_3d.view_distance=2.8;a.spaces.active.region_3d.view_location=Vector((0,0,.72));a.spaces.active.shading.type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Source/YoungTrainer_Reference_V1.blend'),check_existing=False)
bpy.app.driver_namespace['YT_ENV']=globals().copy()
print('UV_RIG_COMPLETE',len(PARTS),'semantic meshes',len(armdata.bones),'bones','height',1.4)
