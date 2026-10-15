import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
OUT=BASE/'Source/SculptV4/Hobbit_NPC_V4_HeadSculpt.blend'
assert not OUT.exists(),'Do not replace an existing V4'
with bpy.data.libraries.load(str(BASE/'Source/Hobbit_NPC_Base_V3_Body.blend'),link=False) as (a,b):
 b.scenes=['Hobbit_NPC_Base_V3_Body']
s=b.scenes[0];s.name='Hobbit_NPC_V4_HeadSculpt';bpy.context.window.scene=s
reference=bpy.data.collections.new('HNV4_V3_UNCHANGED_COMPARISON');s.collection.children.link(reference)
for o in list(s.objects):
 if o.name.startswith('HNV3_'):
  if o.type=='MESH' and ('Body' in o.name or 'Eyeball' in o.name):
   r=o.copy();r.data=o.data.copy();r.name='REF_V3_'+o.name.split('.')[0];reference.objects.link(r);r.hide_render=True;r.hide_set(True);r.hide_select=True
  o.name=o.name.replace('HNV3_','HNV4_',1)
  if o.data is not None:o.data=o.data.copy()
for c in s.collection.children:
 if c.name.startswith('HNV3_'):c.name=c.name.replace('HNV3_','HNV4_',1)
body=next(o for o in s.objects if o.name.startswith('HNV4_Body'))
s['source_v3']=str(BASE/'Source/Hobbit_NPC_Base_V3_Body.blend');s['art_status']='Limited form correction; manual sculpt and adult reference required, no art approval'
s['current_height_without_hair_m']=1.282;s['future_height_with_hair_m']=1.32
# Save an own checkpoint before all V4 geometry changes.
bpy.data.libraries.write(str(BASE/'Source/SculptV4/Hobbit_NPC_V4_00_V3Copy.blend'),{s})
# Controlled local edge division, no surface smoothing and no body subdivision.
bm=bmesh.new();bm.from_mesh(body.data)
head_faces=[f for f in bm.faces if all(v.co.z>1.067 and abs(v.co.x)<.18 for v in f.verts)]
head_edges=set(e for f in head_faces for e in f.edges)
bmesh.ops.subdivide_edges(bm,edges=list(head_edges),cuts=1,use_grid_fill=True,smooth=0)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free();body.data.update()
body.shape_key_add(name='Basis_V3_LocalDensity');key=body.shape_key_add(name='V4_LimitedHeadFormPass');key.value=1
# Compact local proportional edits. These are mesh/shape-key operations, not hand sculpt strokes.
def fall(v,c,r):
 d=sum(((v[i]-c[i])/r[i])**2 for i in range(3))
 return (1-d)**2 if d<1 else 0.0
edited=0;maxdelta=0
for idx,v in enumerate(body.data.vertices):
 x,y,z=v.co;co=v.co.copy()
 if z<=1.067 or abs(x)>=.18:continue
 if y<-.025:
  # fuller lower cheeks and calmer chin/jaw planes
  w=fall((abs(x),y,z),(.072,-.073,1.117),(.040,.060,.037));co.y-=.0040*w
  w=fall((x,y,z),(0,-.060,1.074),(.070,.067,.025));co.y-=.0035*w
  # lower elevated mouth corners; reduce the beaked upper-lip projection
  w=fall((x,y,z),(0,-.080,1.087),(.061,.070,.018));co.z-=.0030*(min(1,abs(x)/.041)**1.8)*w
  co.y+=.0018*fall((x,y,z),(0,-.085,1.091),(.035,.065,.008))
  # rounded alar volume; orient nostril region slightly toward underside
  w=fall((abs(x),y,z),(.021,-.094,1.119),(.017,.040,.012))
  co.y-=.0015*w;co.z-=.0014*w
  # decrease shelf above orbital region without moving the eyeballs
  co.y+=.0015*fall((abs(x),y,z),(.049,-.076,1.183),(.029,.035,.012))
 # lobule and helix: small continuous changes of existing ear surface
 w=fall((abs(x),y,z),(.120,.005,1.124),(.018,.028,.031))
 co.x+=math.copysign(.0013*w,x)
 co.y-=.0012*fall((abs(x),y,z),(.118,.018,1.153),(.020,.025,.025))
 key.data[idx].co=co
 delta=(co-v.co).length
 if delta>1e-9:edited+=1;maxdelta=max(maxdelta,delta)
# Protect all non-head regions; a 1-cm blended neck collar prevents accidental deformation.
mask=body.data.attributes.get('.sculpt_mask') or body.data.attributes.new('.sculpt_mask','FLOAT','POINT')
for i,v in enumerate(body.data.vertices):mask.data[i].value=1.0 if abs(v.co.x)>.18 or v.co.z<=1.067 else max(0,1-(v.co.z-1.067)/.010)
for o in s.objects:o.select_set(False)
body.hide_set(False);body.select_set(True);bpy.context.view_layer.objects.active=body;body.active_shape_key_index=1
mode_ids=[i.identifier for i in bpy.ops.object.mode_set.get_rna_type().properties["mode"].enum_items]
bpy.ops.object.mode_set(mode=next(x for x in mode_ids if x=="SCULPT"))
sc=s.tool_settings.sculpt;sc.use_symmetry_x=True;sc.use_symmetry_y=False;sc.use_symmetry_z=False
# Load native shipped Blender brushes locally; no downloads/add-ons.
assets='/Applications/Blender.app/Contents/Resources/5.2/datafiles/assets/brushes/essentials_brushes-mesh_sculpt.blend'
with bpy.data.libraries.load(assets,link=False) as (a,b):b.brushes=[n for n in ['Grab','Clay Strips','Draw Sharp','Smooth','Inflate/Deflate','Crease Polish','Mask'] if n in a.brushes]
for br in b.brushes:
 if br:
  br.use_fake_user=True;br.use_frontface=True;br.strength=.15 if br.name!='Grab' else .20;br.size=65
# Native asset activation will be done with the visible viewport after save preparation.
mode_ids=[i.identifier for i in bpy.ops.object.mode_set.get_rna_type().properties['mode'].enum_items]
bpy.ops.object.mode_set(mode=next(x for x in mode_ids if x=='SCULPT'))
bpy.context.view_layer.update()
info={'edited_head_vertices':edited,'max_displacement_m':maxdelta,'local_subdivision_cuts':1,'subdivision_smooth':0,'whole_body_subdivision':False,'native_brush_strokes_performed':False,'shape_key_reversible':True,'native_brushes':[br.name for br in b.brushes if br],'body_vertices':len(body.data.vertices),'body_faces':len(body.data.polygons)}
(BASE/'Review/V4/Operations.json').write_text(json.dumps(info,indent=2))
bpy.data.libraries.write(str(OUT),{s})
print(json.dumps(info,indent=2));print('Saved isolated V4 scene',OUT)
