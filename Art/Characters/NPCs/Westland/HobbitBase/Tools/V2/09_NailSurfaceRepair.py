exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
from mathutils.bvhtree import BVHTree
body=bpy.data.objects['HNV2_Body'];bpy.context.view_layer.update()
bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
archive([o for o in list(C['HOBBIT_FACE'].objects) if o.name=='HNV2_FingerAndToeNails' or o.name.startswith('HNV2_Fitted')])
mat=bpy.data.materials['HNV2_NaturalNails'];patches=[]
def nail(name,cx,cy,rx,ry,top):
 vertices=[];faces=[];N=24;R=5
 def point(x,y,r):
  hit,normal,_,_=bvh.ray_cast(Vector((x,y,top)),Vector((0,0,-1)),.25)
  assert hit is not None,(name,x,y)
  return tuple(hit+normal*(.00065+.00025*(1-r*r)))
 vertices.append(point(cx,cy,0))
 for k in range(1,R+1):
  r=k/R
  for j in range(N):
   a=math.tau*j/N;vertices.append(point(cx+rx*r*math.cos(a),cy+ry*r*math.sin(a),r))
 for j in range(N):faces.append([0,1+j,1+(j+1)%N])
 for k in range(R-1):
  for j in range(N):faces.append([1+k*N+j,1+k*N+(j+1)%N,1+(k+1)*N+(j+1)%N,1+(k+1)*N+j])
 o=mesh(name,vertices,faces,'HOBBIT_FACE',[mat]);so=o.modifiers.new('ThinNailShell','SOLIDIFY');so.thickness=.00025;so.offset=-1;apply(o,so);patches.append(o)
for sign,side in [(1,'L'),(-1,'R')]:
 for i,(yy,xx) in enumerate([(-.032,.752),(-.010,.765),(.014,.758),(.035,.736),(-.069,.703)]):
  nail('FittedFingerNail_'+side+'_'+str(i),sign*(xx-.004),yy,.0036,.0032,1.02)
 for i,(xx,yy,r) in enumerate([(.068,-.211,.009),(.092,-.216,.0077),(.116,-.210,.007),(.138,-.199,.006),(.158,-.179,.005)]):
  nail('FittedToeNail_'+side+'_'+str(i),sign*xx,yy,r*.72,(.008 if i<2 else .006)*.72,.14)
nails=join(patches,'FingerAndToeNails')
save_stage('09_NailSurfaceRepair');bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V2.blend'),{scene});print('Rebuilt 20 thin, raised nail shells',len(nails.data.vertices))
