"""Three sibling V3 assets, metres, grounded pivots. Never saves or replaces V2.
Painted multi-leaf sprays on bent, interlocking cards; no opaque crown spheres.
Run with V2 source open in background. Re-running backs up the working V3 first.
"""
import bpy, math, random, json, shutil
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2]; A=R/'Art/World/WestlandAssetLibrary'; O=R/'Saved/WestlandAssetLibraryV3'; O.mkdir(exist_ok=True)
assert bpy.app.background and Path(bpy.data.filepath).name=='WestlandAssetLibrary_V2.blend'
target=A/'Source/WestlandAssetLibrary_V3.blend'
if target.exists(): shutil.copy2(target,O/('V3_WorkingBackup_'+str(len(list(O.glob('V3_WorkingBackup_*.blend'))))+'.blend'))
bpy.context.preferences.filepaths.save_version=0
s=bpy.data.scenes.new('WestlandAssetLibrary_V3_Source'); bpy.context.window.scene=s; s.unit_settings.system='METRIC'; s.unit_settings.scale_length=1
col=bpy.data.collections.new('V3_Oak_and_WildShrubs'); s.collection.children.link(col)
def material(name,image,leaf=False):
 m=bpy.data.materials.new(name); m.use_nodes=True; n=m.node_tree.nodes; n.clear(); l=m.node_tree.links
 out=n.new('ShaderNodeOutputMaterial'); bs=n.new('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value=.95; bs.inputs['Specular IOR Level'].default_value=.06
 tex=n.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(str(image),check_existing=True); tex.interpolation='Linear'
 vc=n.new('ShaderNodeVertexColor'); vc.layer_name='PaintTint'; mul=n.new('ShaderNodeMixRGB'); mul.blend_type='MULTIPLY'; mul.inputs[0].default_value=1
 l.new(tex.outputs['Color'],mul.inputs[1]); l.new(vc.outputs['Color'],mul.inputs[2]); l.new(mul.outputs[0],bs.inputs['Base Color']); l.new(bs.outputs[0],out.inputs[0])
 if leaf:
  l.new(tex.outputs['Alpha'],bs.inputs['Alpha']); m.surface_render_method='DITHERED'; m.use_backface_culling=False
 m.diffuse_color=(.30,.44,.18,1) if leaf else (.30,.19,.09,1)
 return m
bark=material('WLA_V3_Bark',A/'Textures/T_WLA_Bark.png'); leaf=material('WLA_V3_FoliageGroups',A/'Textures/T_WLA_FoliageGroups_V3.png',True)
rng=random.Random(903711); verts=[]; faces=[]; uv=[]; pigments=[]; slots=[]
def surface(v,f,t,mi,color):
 off=len(verts); verts.extend([tuple(p) for p in v]); uv.extend(t); pigments.extend([color]*len(v)); faces.extend([tuple(off+i for i in face) for face in f]); slots.extend([mi]*len(f))
def tube(points,radii,sides=12,moss=False):
 pts=[Vector(p) for p in points]; v=[]; t=[]; f=[]; dist=0
 for j,p in enumerate(pts):
  if j:dist+=(p-pts[j-1]).length
  d=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized(); ref=Vector((0,1,0)) if abs(d.z)>.9 else Vector((0,0,1)); x=d.cross(ref).normalized(); y=d.cross(x).normalized()
  for i in range(sides+1):
   a=i/sides*math.tau; rr=radii[j]*(1+.10*math.sin(a*5+j*.31)+.055*math.sin(a*9-j*.19)); v.append(p+rr*(x*math.cos(a)+y*math.sin(a))); t.append((i/sides*1.4,dist*.55))
 for j in range(len(pts)-1):
  for i in range(sides):q=j*(sides+1)+i; f.extend([(q,q+1,q+sides+2),(q,q+sides+2,q+sides+1)])
 surface(v,f,t,0,(.86,.91,.76,1) if moss else (.98,.92,.83,1))
 for j,reverse in [(0,True),(len(pts)-1,False)]:
  vv=[pts[j]]+[v[j*(sides+1)+i] for i in range(sides)]; ff=[(0,(i+1)%sides+1,i+1) if reverse else (0,i+1,(i+1)%sides+1) for i in range(sides)]; tt=[(.5,.5)]+[(.5+.48*math.cos(i/sides*math.tau),.5+.48*math.sin(i/sides*math.tau)) for i in range(sides)]; surface(vv,ff,tt,0,(.90,.91,.76,1) if moss else (1,1,1,1))
def card(center,normal,width,height,shade=1):
 """Bent 4x4 card with trimmed octagonal corners and a nondegenerate atlas UV.
 Each card represents a branch spray of many small leaves, not one giant leaf.
 """
 n=Vector(normal).normalized(); ref=Vector((0,0,1)) if abs(n.z)<.90 else Vector((0,1,0)); x=n.cross(ref).normalized(); y=n.cross(x).normalized(); rot=rng.uniform(-math.pi,math.pi); xx=x*math.cos(rot)+y*math.sin(rot); yy=-x*math.sin(rot)+y*math.cos(rot); c=Vector(center)
 q=rng.randrange(4); u0=(q%2)*.5+.012; v0=(q//2)*.5+.012; extent=.476; v=[]; t=[]; f=[]
 # Nine vertices, bowed center. All edge cards curve; no flat intersecting quads.
 outline=[(-.32,-.5),(.32,-.5),(.5,-.28),(.5,.28),(.32,.5),(-.32,.5),(-.5,.28),(-.5,-.28)]
 v.append(c+n*(width*.035)); t.append((u0+extent*.5,v0+extent*.5))
 for a,b in outline:v.append(c+xx*(a*width)+yy*(b*height)+n*(width*.015*math.sin(a*5+b*3))); t.append((u0+(a+.5)*extent,v0+(b+.5)*extent))
 for i in range(8):f.append((0,i+1,(i+1)%8+1))
 surface(v,f,t,1,(shade*.91,shade*.96,shade*.88,1))
def crown(center,radii,count,card_size,seedshade=1):
 """Irregular shell plus crossing interior sprays: intersecting masses, never a core mesh."""
 c=Vector(center); rx,ry,rz=radii
 for i in range(count):
  z=1-2*(i+.5)/count; a=i*2.399963+rng.uniform(-.14,.14); r=math.sqrt(1-z*z); n=Vector((math.cos(a)*r,math.sin(a)*r,z)); wiggle=.83+.22*math.sin(a*3+z*4)+.10*math.sin(a*7-z*3)+rng.uniform(-.09,.09)
  p=c+Vector((rx*n.x,ry*n.y,rz*n.z))*wiggle
  n=Vector((n.x*.7+rng.uniform(-.23,.23),n.y*.7+rng.uniform(-.23,.23),n.z*.35+.65)).normalized(); size=card_size*rng.uniform(.82,1.2)
  card(p,n,size,size*rng.uniform(.78,1.1),rng.uniform(.79,1.07)*seedshade)
 for i in range(count//3):
  a=rng.uniform(0,math.tau); z=rng.uniform(-.7,.8); p=c+Vector((math.cos(a)*rx*.6,math.sin(a)*ry*.6,rz*z)); size=card_size*rng.uniform(.9,1.25); card(p,(math.cos(a),math.sin(a),rng.uniform(.1,1)),size,size*.9,rng.uniform(.78,1)*seedshade)
def ancient_oak():
 trunk=[(0,0,0),(.10,-.08,.55),(.18,.03,1.5),(.04,.20,2.6),(-.27,.29,3.8),(-.40,.22,4.8),(-.10,.38,5.6),(.12,.42,6.4),(.3,.2,7.4),(.18,.10,8.1)]
 tube(trunk,[1.02,.80,.69,.61,.58,.48,.39,.28,.17,.07],24,True)
 for i in range(8):
  a=i*2.399; d=Vector((math.cos(a),math.sin(a),0)); side=Vector((-d.y,d.x,0)); reach=rng.uniform(1.1,1.75); tube([d*.36+Vector((0,0,.9)),d*.75+Vector((0,0,.30)),d*reach*.77+Vector((0,0,.10)),d*reach+side*.12+Vector((0,0,.055))],[.30,.25,.12,.045],12,True)
 lobes=[((-2.7,.2,8.5),(2.9,2.5,1.8),105,1.35),((2.3,.3,8.7),(3.25,2.35,1.85),118,1.4),((-.35,1.8,9.6),(3.5,2.8,1.85),132,1.4),((-.45,-2,8.0),(3.2,2.5,1.5),112,1.3),((2.5,-1.95,8),(2.4,2.2,1.4),87,1.25),((-3.3,-1.4,8),(2.6,2,1.5),80,1.25),((.8,-.2,10.0),(2.2,2.0,1.65),85,1.3)]
 for i,(center,rad,num,size) in enumerate(lobes):
  end=Vector(center); start=Vector(trunk[4+i%3]); mid=start.lerp(end,.45)+Vector((-.20 if i%2 else .12,0,.10)); elbow=start.lerp(end,.72)+Vector((.05,.1,.22)); tube([start,start.lerp(mid,.5),mid,elbow,end],[.30 if i<4 else .23,.26,.19,.12,.04],14)
  for j in range(4):
   a=i*1.83+j*2.39; tip=end+Vector((math.cos(a)*rad[0]*.8,math.sin(a)*rad[1]*.8,rad[2]*rng.uniform(-.2,.65))); tube([mid.lerp(end,.65),end.lerp(tip,.45),tip],[.10,.052,.013],8)
  crown(center,rad,num,size,.98 if i%3 else .94)
 # Raised twisting bark ribs/root buttresses are silhouette-scale form, not microdetail.
 for i in range(12):
  a=i/math.pi*1.66; pts=[]
  for j in range(7):
   z=.15+j*.65; r=.69-.036*j+.09*math.sin(i*1.1+j*.4); pts.append((r*math.cos(a+j*.08),r*math.sin(a+j*.08),z))
  tube(pts,[.045,.049,.043,.035,.025,.018,.008],5,i%3==0)
def bush(variant):
 lobes=([((-.22,.02,.8),(1.23,.82,.55),122,.6),((.40,.12,1.12),(.86,.67,.73),75,.60),((.38,-.45,.59),(1.02,.64,.40),68,.56)] if variant==0 else [((.12,.05,.52),(1.52,.82,.40),152,.53),((.60,.16,.77),(.83,.62,.49),68,.55),((-.71,-.34,.31),(.84,.60,.25),56,.49)])
 for i,(c,rad,num,size) in enumerate(lobes):
  end=Vector(c); start=Vector((end.x*.35,end.y*.3,.035)); tube([start,start.lerp(end,.45)+Vector((0,0,.12)),end],[.055,.035,.01],8)
  for j in range(3):
   a=j*2.399+i; tip=end+Vector((math.cos(a)*rad[0]*.75,math.sin(a)*rad[1]*.75,rad[2]*.4)); tube([end*.7+Vector((0,0,.1)),end.lerp(tip,.4),tip],[.025,.018,.004],6)
  crown(c,rad,num,size,1 if variant==0 else .94)
def finish(name,kind):
 # Never sink root tips/low foliage below the grounded origin.
 grounded=[(p[0],p[1],max(0.,p[2])) for p in verts]
 m=bpy.data.meshes.new(name+'_Geometry'); m.from_pydata(grounded,[],faces); m.update(); m.materials.append(bark); m.materials.append(leaf)
 u=m.uv_layers.new(name='UV0'); paint=m.color_attributes.new(name='PaintTint',type='BYTE_COLOR',domain='CORNER')
 for poly,mi in zip(m.polygons,slots):
  poly.material_index=mi; poly.use_smooth=True
  for li in poly.loop_indices:idx=m.loops[li].vertex_index; u.data[li].uv=uv[idx]; paint.data[li].color=pigments[idx]
 m.calc_loop_triangles(); m.calc_tangents(uvmap='UV0'); o=bpy.data.objects.new(name,m); col.objects.link(o); o['Revision']='V3 painted foliage groups'; o['GroundPivot_m']=0; o['AssetFamily']=kind
 return o
assets=[]
for name,kind,build in [('SM_WLA_OakAncient_V3','Trees',ancient_oak),('SM_WLA_WildBush_V3_A','Vegetation',lambda:bush(0)),('SM_WLA_WildBush_V3_B','Vegetation',lambda:bush(1))]:
 verts=[];faces=[];uv=[];pigments=[];slots=[];build();o=finish(name,kind); collision=[]
 if kind=='Trees':
  # Explicit tapered grounded trunk hull. Copying only V2 mesh data would lose
  # its object-space Z translation and incorrectly put half the collider underground.
  cv=[];cf=[];rings=[((0,0,0),.85),((.18,.03,1.5),.68),((.04,.20,2.6),.59),((-.40,.22,4.8),.48)];sides=16
  for c,rad in rings:
   for i in range(sides):a=i/sides*math.tau;cv.append((c[0]+rad*math.cos(a),c[1]+rad*math.sin(a),c[2]))
  for j in range(3):
   for i in range(sides):q=j*sides+i;nextq=j*sides+(i+1)%sides;cf.append((q,nextq,nextq+sides,q+sides))
  cf.append(tuple(reversed(range(sides))));cf.append(tuple(3*sides+i for i in range(sides)));cm=bpy.data.meshes.new('V3_TrunkHull');cm.from_pydata(cv,[],cf);cm.update();ucx=bpy.data.objects.new('UCX_'+name+'_00',cm);col.objects.link(ucx);ucx.hide_render=True;ucx.hide_set(True);collision=[ucx.name]
 assets.append({'object':name,'family':kind,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'dimensions_m':list(o.dimensions),'material_slots':['WLA_V3_Bark','WLA_V3_FoliageGroups'],'collision_objects':collision,'leaf_group_count':slots.count(1)//8,'art_status':'V3_visual_review_required'})
 o.hide_set(kind!='Trees')
s.world=bpy.data.worlds.new('V3_WorkbenchWorld'); s.world.color=(.16,.18,.14)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.clip_end=1000;area.spaces.active.region_3d.view_distance=22;area.spaces.active.region_3d.view_location=(0,0,5.5)
bpy.context.view_layer.objects.active=bpy.data.objects['SM_WLA_OakAncient_V3']
data={'revision':'Art Quality V3','source':'Art/World/WestlandAssetLibrary/Source/WestlandAssetLibrary_V3.blend','units':'metres','preserves_v2':True,'assets':assets,'foliage_texture':'Art/World/WestlandAssetLibrary/Textures/T_WLA_FoliageGroups_V3.png','texture_provenance':'Built-in imagegen, 2026-10-11; exact prompt in TextureProvenance_V3.md','bark_texture_reused':'Art/World/WestlandAssetLibrary/Textures/T_WLA_Bark.png'}
(A/'ArtQualityV3.json').write_text(json.dumps(data,indent=2)); bpy.ops.wm.save_as_mainfile(filepath=str(target)); print('V3_SOURCE_SAVED',[(a['object'],a['triangles']) for a in assets])
