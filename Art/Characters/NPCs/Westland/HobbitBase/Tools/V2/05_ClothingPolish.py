import bpy
from pathlib import Path
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
s=bpy.data.scenes['Hobbit_NPC_Base_V2'];bpy.context.window.scene=s
# These are exclusively new V2 objects; stage 03 preserves the previous result.
for name in ['HNV2_Shirt','HNV2_Waistcoat','HNV2_Breeches']:
 o=bpy.data.objects[name];bpy.data.objects.remove(o,do_unlink=True)
with bpy.data.libraries.load(str(BASE/'Source/Stages/Hobbit_NPC_Base_V2_00_WorkingCopy.blend'),link=False) as (a,b):b.objects=['HNV2_Shirt','HNV2_Waistcoat','HNV2_Breeches']
c=next(c for c in s.collection.children if c.name=='HNV2_HOBBIT_CLOTHING')
for o,name in zip(b.objects,['HNV2_Shirt','HNV2_Waistcoat','HNV2_Breeches']):
 c.objects.link(o);o.name=name;o.data=o.data.copy()
REFINED_CLOTHING=True
exec(compile(open(str(BASE/'Tools/V2/03_Clothing.py')).read(),'03_Clothing.py','exec'))
from mathutils.bvhtree import BVHTree
body=bpy.data.objects['HNV2_Body'];bpy.context.view_layer.update();bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());shirt=bpy.data.objects['HNV2_Shirt'];vest=bpy.data.objects['HNV2_Waistcoat'];pants=bpy.data.objects['HNV2_Breeches'];linen=bpy.data.materials['HNV2_WovenLinen'];edge=bpy.data.materials['HNV2_LinenHem']
# Shape two restrained sleeve creases and diagonal gathers, not periodic rings.
for v in shirt.data.vertices:
 x,y,z=v.co;ax=abs(x)
 if .23<ax<.416:
  angle=math.atan2(z-.9338,y);dy=y;dz=z-.9338;d=(dy*dy+dz*dz)**.5
  if d>.001:
   fold=-.0038*math.exp(-((ax-(.293+.023*math.sin(angle)))/.014)**2)-.003*math.exp(-((ax-(.375+.019*math.sin(angle+.5)))/.014)**2)
   fold+=.0021*math.exp(-((ax-(.316+.023*math.sin(angle)))/.016)**2)
   v.co.y+=fold*dy/d;v.co.z+=fold*dz/d
 if ax<.17 and .66<z<.79:
  n=v.normal;fold=.0026*math.sin(x*50+z*13)*math.exp(-((z-.707)/.045)**2);v.co+=n*fold
# Add an actual front placket and seams fitted to the shirt's surface.
bpy.context.view_layer.update();shbvh=BVHTree.FromObject(shirt,bpy.context.evaluated_depsgraph_get());V=[];F=[]
for k in range(25):
 z=.684+k*(.987-.684)/24
 for x in [-.008,.008]:
  hit=shbvh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1)[0]
  V.append((x,hit.y-.0008,z))
for k in range(24):F.append([k*2,k*2+1,(k+1)*2+1,(k+1)*2])
placket=mesh('ShirtPlacket',V,F,'HOBBIT_CLOTHING',[linen]);so=placket.modifiers.new('PlacketThickness','SOLIDIFY');so.thickness=.0012;apply(placket,so);parts=[shirt,placket]
for sign in [-1,1]:
 pts=[(x+sign*.0008,y-.0002,z) for x,y,z in V[(0 if sign<0 else 1)::2]];parts.append(tube('PlacketStitch_'+str(sign),pts,.00045,'HOBBIT_CLOTHING',edge,6))
for z in [.748,.827,.900,.967]:
 hit=shbvh.ray_cast(Vector((0,-.5,z)),Vector((0,1,0)),1)[0];parts.append(sphere('LinenButton_'+str(z),(0,hit.y-.002,z),(.0028,.0010,.0028),'HOBBIT_CLOTHING',edge,14,8))
shirt=join(parts,'Shirt')
# Local skin-clearance repair includes the inner garment surfaces; no body scaling.
fixed={}
for o in [shirt,pants]:
 total=0
 for iteration in range(3):
  for v in o.data.vertices:
   hit,n,index,dist=bvh.find_nearest(v.co);signed=(v.co-hit).dot(n)
   if signed<.0015:v.co+=n*(.0015-signed);total+=1
 fixed[o.name]=total
# Match the eye skin patches to the body skin, avoiding a different plastic shader.
mat=bpy.data.materials['HNV2_FaceSkin'];p=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(.47,.245,.145,1);p.inputs['Subsurface Weight'].default_value=.065;p.inputs['Subsurface Scale'].default_value=.008;p.inputs['Roughness'].default_value=.62
# The light lip tint belongs to flesh, not a dark outlined smile.
lip=bpy.data.materials['HNV2_MutedLips'];p=next(n for n in lip.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(.37,.174,.110,1)
save_stage('05_ClothingPolish');print(json.dumps({'skin_clearance_corrections':fixed}))
bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V2.blend'),{scene})
