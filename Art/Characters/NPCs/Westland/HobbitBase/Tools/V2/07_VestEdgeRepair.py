exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
from mathutils.bvhtree import BVHTree
old=bpy.data.objects['HNV2_Waistcoat'];archive([old])
# The original V1 garment has a stable shoulder cage; reuse it as the local repair base.
with bpy.data.libraries.load(str(BASE/'Source/Hobbit_NPC_Base_V1.blend'),link=False) as (a,b):b.objects=['HNB_Waistcoat']
o=b.objects[0];o.name='HNV2_Waistcoat';o.data=o.data.copy();C['HOBBIT_CLOTHING'].objects.link(o);o.data.materials.clear();o.data.materials.append(bpy.data.materials['HNV2_WalnutWool'])
for v in o.data.vertices:
 x,y,z=v.co
 if y<-.035 and abs(x)<.125:
  amount=.008*max(0,min(1,(z-.75)/.24));v.co.x+=amount*(1 if x>0 else -1)
for m in list(o.modifiers):apply(o,m)
# Gentle tailored folds only on the torso panels, leaving joint silhouettes stable.
for v in o.data.vertices:
 x,y,z=v.co
 if .72<z<.94 and abs(x)<.165:
  v.co+=v.normal*(.0023*math.sin(x*28+z*17)*math.exp(-((z-.82)/.12)**2))
body=bpy.data.objects['HNV2_Body'];bpy.context.view_layer.update();bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());fixed=0
for iteration in range(3):
 for v in o.data.vertices:
  h,n,index,d=bvh.find_nearest(v.co);signed=(v.co-h).dot(n)
  if signed<.002:v.co+=n*(.002-signed);fixed+=1
# Thin understated edge finish instead of twisted closed binding tubes around the shoulder.
# Only short front edges receive a seam; their frame never changes abruptly.
bpy.context.view_layer.update();vh=BVHTree.FromObject(o,bpy.context.evaluated_depsgraph_get());parts=[o]
for sign in [-1,1]:
 pts=[]
 for i in range(23):
  z=.699+i*.287/22;x=sign*(.052+.016*(z-.699)/.287);hit=vh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1)[0]
  if hit:pts.append(tuple(hit+Vector((0,-.0005,0))))
 if len(pts)>2:parts.append(tube('SubtleVestFrontSeam_'+str(sign),pts,.00055,'HOBBIT_CLOTHING',bpy.data.materials['HNV2_WoolBinding'],6))
for i,(z,x) in enumerate([(.745,.078),(.816,.085),(.887,.090)]):
 h=vh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1)[0]
 if h:parts.append(sphere('SmallVestButton_'+str(i),(x,h.y-.0016,z),(.003,.0014,.003),'HOBBIT_CLOTHING',bpy.data.materials['HNV2_BrownLeather'],16,10))
o=join(parts,'Waistcoat')
# Hem repair: the shirt bottom is a deliberate continuous hem, no saw-tooth raw edge.
shirt=bpy.data.objects['HNV2_Shirt']
for v in shirt.data.vertices:
 if .632<v.co.z<.650 and abs(v.co.x)<.23:v.co.z=.646+.0008*math.cos(v.co.x*18)
# Minimize source-only strand tessellation where it contributes no visible curl shape.
# Body/joint geometry is retained; no global subdivision or decimation applied.
save_stage('07_VestEdgeRepair');bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V2.blend'),{scene});print(json.dumps({'stable_vest_vertices':len(o.data.vertices),'local_skin_clearance_fixes':fixed}))
