exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
body=bpy.data.objects['HNV2_Body'];skin=body.data.materials[0]
# Refresh the authored skin tint after the corrected anatomical mesh replacement.
a=body.data.color_attributes.get('HNV2_SkinTint') or body.data.color_attributes.new(name='HNV2_SkinTint',type='FLOAT_COLOR',domain='POINT')
for v in body.data.vertices:
 x,y,z=v.co;pink=0.
 if y<0 and z>1.07:pink=max(math.exp(-((abs(x)-.065)/.030)**2-((z-1.157)/.022)**2),.7*math.exp(-(x/.020)**2-((z-1.156)/.016)**2))*.05
 a.data[v.index].color=(.47+pink,.245-pink*.12,.145-pink*.10,1)
linen=material('WovenLinen',(.58,.515,.395),.84);linenedge=material('LinenHem',(.47,.405,.30),.88);vestmat=material('WalnutWool',(.116,.046,.023),.87);vestedge=material('WoolBinding',(.178,.079,.036),.85);pantsmat=material('OliveTwill',(.133,.146,.070),.88);pantsedge=material('OliveHem',(.112,.123,.060),.88);leathermat=material('BrownLeather',(.072,.029,.012),.62);metal=material('AgedBrass',(.28,.17,.060),.49)
for mat in [linen,linenedge,vestmat,vestedge,pantsmat,pantsedge,leathermat]:
 nt=mat.node_tree;p=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');base=p.inputs['Base Color'].default_value[:];n=nt.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=250 if mat!=leathermat else 160;n.inputs['Detail'].default_value=2
 ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=(*[c*.94 for c in base[:3]],1);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(*[c*1.05 for c in base[:3]],1);nt.links.new(n.outputs['Fac'],ramp.inputs['Fac']);nt.links.new(ramp.outputs['Color'],p.inputs['Base Color'])
 b=nt.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.10;b.inputs['Distance'].default_value=.00035;nt.links.new(n.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs['Normal'],p.inputs['Normal'])
 p.inputs['Specular IOR Level'].default_value=.25
# Reuse the authored V1 shoulder/joint cage, not an imported character.
src=(BASE/'Tools/BuildHobbitBase.py').read_text();start=src.index('V=[];F=[];zones=[]');end=src.index("body=objmesh('HNB_Body'")
exec(src[start:end]);factor=.9844347990514335*.9984350818434603
V=[tuple(Vector(v)*factor) for v in V]
oldshirt=bpy.data.objects['HNV2_Shirt'];oldvest=bpy.data.objects['HNV2_Waistcoat'];oldpants=bpy.data.objects['HNV2_Breeches'];belt=bpy.data.objects['HNV2_Belt'];buckle=bpy.data.objects['HNV2_Buckle'];archive([oldshirt,oldvest])
fs=[f for f,z in zip(F,zones) if (z=='torso' and min(V[i][2] for i in f)>=.635) or (z=='arm' and max(abs(V[i][0]) for i in f)<=.444)]
used=sorted({i for f in fs for i in f});ids={old:i for i,old in enumerate(used)}
shirt=mesh('Shirt',[V[i] for i in used],[[ids[i] for i in f] for f in fs],'HOBBIT_CLOTHING',[linen]);shirt.data.update()
for v in shirt.data.vertices:
 x,y,z=v.co;offset=.011;fold=0.
 if abs(x)>.22:
  phase=math.atan2(z-.9338,y);fold=.0028*math.exp(-((abs(x)-.35)/.16)**2)*math.sin(6*phase+abs(x)*47)
 else:
  angle=math.atan2(y+.015,x);fold=.0034*math.sin(7*angle+z*17)*math.exp(-((z-.77)/.13)**2)
  fold+=.0018*math.sin(13*angle)*math.exp(-((z-.67)/.028)**2)
 v.co+=v.normal*(offset+fold)
 if z<.65:v.co.z=.646+.002*math.cos(x*38)
su=shirt.modifiers.new('LinenSurface','SUBSURF');su.levels=1;su.render_levels=1;so=shirt.modifiers.new('LinenThickness','SOLIDIFY');so.thickness=.0022;so.offset=0
# Collar stand and two folded, curved collar leaves.
parts=[shirt]
vs=[];fs=[];N=48
for k,z in enumerate([1.026,1.037,1.050,1.056]):
 for j in range(N):
  t=j/(N-1);phi=-math.pi/2+.38+t*(math.tau-.76);rx=.066 if k<2 else .063;ry=.057 if k<2 else .054
  vs.append((rx*math.cos(phi),ry*math.sin(phi),z))
for k in range(3):
 for j in range(N-1):fs.append([k*N+j,k*N+j+1,(k+1)*N+j+1,(k+1)*N+j])
o=mesh('CollarStand',vs,fs,'HOBBIT_CLOTHING',[linen]);so=o.modifiers.new('CollarThickness','SOLIDIFY');so.thickness=.002;parts.append(o)
for sign,side in [(1,'L'),(-1,'R')]:
 v=[];f=[];N=9
 corners=[Vector((sign*.025,-.055,1.047)),Vector((sign*.058,-.043,1.043)),Vector((sign*.079,-.086,1.005)),Vector((sign*.038,-.107,1.005))]
 for k in range(N):
  a=k/(N-1)
  for j in range(N):
   b=j/(N-1);p=corners[0].lerp(corners[1],b).lerp(corners[3].lerp(corners[2],b),a);p.y-=.005*math.sin(math.pi*a)*math.sin(math.pi*b);v.append(tuple(p))
 for k in range(N-1):
  for j in range(N-1):f.append([k*N+j,k*N+j+1,(k+1)*N+j+1,(k+1)*N+j])
 o=mesh('FoldedCollar_'+side,v,f,'HOBBIT_CLOTHING',[linen]);so=o.modifiers.new('CollarThickness','SOLIDIFY');so.thickness=.002;parts.append(o)
 # Rolled sleeves expose the forearms; they are shaped fabric bands, not cylinders.
 v=[];f=[];N=40;K=10
 for k in range(K):
  a=math.tau*k/K;x=sign*(.431+.013*math.cos(a));bulge=.004*math.sin(a)
  for j in range(N):
   th=math.tau*j/N;r=.055+bulge+.0012*math.sin(5*th);v.append((x,r*math.cos(th),.9338+r*.91*math.sin(th)))
 for k in range(K):
  for j in range(N):f.append([k*N+j,k*N+(j+1)%N,((k+1)%K)*N+(j+1)%N,((k+1)%K)*N+j])
 parts.append(mesh('RolledCuff_'+side,v,f,'HOBBIT_CLOTHING',[linen]))
 # Restrained longitudinal sleeve seam and cuff seam.
 pts=[(sign*x,-.014,.992-.011*(x-.25)/.18) for x in [.24+i*.18/24 for i in range(25)]]
 parts.append(tube('SleeveSeam_'+side,pts,.0006,'HOBBIT_CLOTHING',linenedge,6))
# Apply own-clothing modifiers before joining so nothing is silently lost.
for o in parts:
 for m in list(o.modifiers):apply(o,m)
shirt=join(parts,'Shirt')
# New front-open waistcoat with actual armholes, garment edges, and shaped hem.
V=[];F=[];rows=[(.671,.202,.163,-.017,.19),(.689,.204,.166,-.019,.19),(.715,.203,.167,-.019,.19),(.754,.203,.169,-.022,.22),(.801,.202,.177,-.026,.30),(.852,.204,.161,-.018,.39),(.884,.207,.140,-.008,.44),(.907,.218,.131,0,.50),(.934,.222,.126,0,.59),(.961,.210,.110,0,.69),(.982,.179,.090,0,.83),(.997,.140,.074,0,.99)]
N=64
for k,(z,rx,ry,cy,gap) in enumerate(rows):
 for j in range(N):
  u=j/(N-1);th=-math.pi/2+gap+u*(math.tau-2*gap);x=rx*math.cos(th);y=cy+ry*math.sin(th)
  zz=z-(.009 if k<2 else 0)*max(0,-math.sin(th))**4
  fold=.0018*math.sin(th*7+z*21)*math.exp(-((z-.79)/.14)**2)
  V.append((x+fold*math.cos(th),y+fold*math.sin(th),zz))
for k in range(len(rows)-1):
 for j in range(N-1):
  corners=[k*N+j,k*N+j+1,(k+1)*N+j+1,(k+1)*N+j]
  center=sum((Vector(V[i]) for i in corners),Vector())/4
  if .885<center.z<.947 and abs(center.x)>.184 and abs(center.y)<.038:continue
  F.append(corners)
waistcoat=mesh('Waistcoat',V,F,'HOBBIT_CLOTHING',[vestmat]);su=waistcoat.modifiers.new('TailoredSurface','SUBSURF');su.levels=1;su.render_levels=1;so=waistcoat.modifiers.new('WoolThickness','SOLIDIFY');so.thickness=.003;so.offset=0
bindings=[]
for sign,side in [(1,'L'),(-1,'R')]:
 pts=[]
 for z,rx,ry,cy,gap in rows:
  th=-math.pi/2+(gap if sign==1 else -gap);pts.append((rx*math.cos(th),cy+ry*math.sin(th)-.0015,z-(.009 if z<.69 else 0)))
 bindings.append(tube('VestBinding_'+side,pts,.0018,'HOBBIT_CLOTHING',vestedge,8))
 pts=[]
 for j in range(30):
  t=j/29;th=-math.pi/2+(.19 if sign==1 else -.19)+sign*t*math.pi*.77;x=.202*math.cos(th);y=-.017+.163*math.sin(th);z=.671-.009*max(0,-math.sin(th))**4;pts.append((x,y,z))
 bindings.append(tube('VestHem_'+side,pts,.0014,'HOBBIT_CLOTHING',vestedge,8))
for i,(z,x,y) in enumerate([(.751,.064,-.184),(.816,.080,-.180),(.873,.093,-.141)]):
 bindings.append(sphere('VestButton_'+str(i),(x,y-.002,z),(.0035,.0018,.0035),'HOBBIT_CLOTHING',leathermat,16,10))
# Body-safe cloth clearance measured on the actual skin surface at the cage points.
from mathutils.bvhtree import BVHTree
bpy.context.view_layer.update();bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
adjusted=0
for vertex in waistcoat.data.vertices:
 hit,normal,index,dist=bvh.find_nearest(vertex.co)
 if hit is None:continue
 signed=(vertex.co-hit).dot(normal)
 if signed<.018:vertex.co+=normal*(.018-signed);adjusted+=1
for m in list(waistcoat.modifiers):apply(waistcoat,m)
waistcoat=join([waistcoat]+bindings,'Waistcoat')
# Breeches retain their connected waist/crotch but gain restrained cloth folds and hems.
oldpants.data.materials.clear();oldpants.data.materials.append(pantsmat)
for v in oldpants.data.vertices:
 x,y,z=v.co;sign=1 if x>0 else -1;cx=sign*.108
 if z<.51:
  dx=x-cx;aa=math.atan2(y,dx);scale=.93+.07*min(1,max(0,(z-.31)/.20));r=math.hypot(dx,y)
  fold=.0038*math.sin(5*aa+z*24)*math.exp(-((z-.39)/.10)**2)+.0018*math.sin(11*aa)*math.exp(-((z-.289)/.035)**2)
  v.co.x=cx+dx*scale+fold*math.cos(aa);v.co.y=y*scale+fold*math.sin(aa)
for m in list(oldpants.modifiers):apply(oldpants,m)
hem=[]
for sign,side in [(1,'L'),(-1,'R')]:
 pts=[(sign*.108+.065*math.cos(j*math.tau/40),.064*math.sin(j*math.tau/40),.285+.001*math.sin(j*math.tau/40*5)) for j in range(41)]
 hem.append(tube('BreechesHem_'+side,pts,.0023,'HOBBIT_CLOTHING',pantsedge,8))
oldpants=join([oldpants]+hem,'Breeches')
# Preserve the belt proportions; change only the new copy's leather and buckle finish.
belt.data.materials.clear();belt.data.materials.append(leathermat);buckle.data.materials.clear();buckle.data.materials.append(metal)
for m in list(buckle.modifiers):apply(buckle,m)
scene['clothing_scope']='separate shirt, open waistcoat, breeches, belt/buckle; geometric folds/collar/cuffs/seams; no skinning'
save_stage('04_ClothingRefined' if globals().get('REFINED_CLOTHING',False) else '03_Clothing')
print(json.dumps({'waistcoat_clearance_adjusted_vertices':adjusted,'shirt_vertices':len(shirt.data.vertices),'waistcoat_vertices':len(waistcoat.data.vertices),'breeches_vertices':len(oldpants.data.vertices)}))
