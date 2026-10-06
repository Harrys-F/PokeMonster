"""Phases 3–7: facial identity, curl clumps, layered clothes and equipment."""
import bpy
E=bpy.app.driver_namespace['YT_ENV'];globals().update(E)
# Friendly portrait. Eyes are independent closed shallow almond volumes.
def almond(name,x,y,z,rx,rz):
 vs=[(x,y-.014,z)];uv=[(.5,.5)];fs=[];n=32
 for j in range(n):
  a=math.tau*j/n;vx=math.cos(a);vz=math.sin(a)*(abs(math.sin(a))**.12)
  vs.append((x+rx*vx,y,z+rz*vz));uv.append((.5+.5*vx,.5+.5*vz))
 for j in range(n):fs.append((0,j+1,(j+1)%n+1))
 back=len(vs);vs.append((x,y+.006,z));uv.append((.5,.5))
 for j in range(n):fs.append((back,(j+1)%n+1,j+1))
 return mesh(name,vs,fs,'EyeWhite','Eyes','head',uv=uv)
for side in [-1,1]:
 s='L' if side==1 else 'R';x=side*.064
 almond('EyeWhite_'+s,x,-.126,1.211,.041,.027)
 ellipsoid('Iris_'+s,(x,-.143,1.211),(.0205,.007,.025),'Iris','Eyes','head',24,10)
 ellipsoid('Pupil_'+s,(x,-.150,1.212),(.009,.0028,.0165),'Pupil','Eyes','head',20,8)
 ellipsoid('EyeCatch_'+s,(x-.006,-.154,1.224),(.006,.002,.006),'Highlight','Eyes','head',12,6)
 ellipsoid('EyeCatchSmall_'+s,(x+.006,-.153,1.202),(.0025,.0015,.0025),'Highlight','Eyes','head',10,4)
 curve('UpperLid_'+s,[(x+.041*math.cos(a),-.131-.013*math.sin(a),1.211+.029*math.sin(a)) for a in [math.pi*j/24 for j in range(25)]],.0028,'Hair','Face','head')
 curve('LowerLid_'+s,[(x+.040*math.cos(a),-.129,1.211+.0255*math.sin(a)) for a in [math.pi+math.pi*j/24 for j in range(25)]],.0016,'SkinWarm','Face','head')
 curve('Brow_'+s,[(x-.036+.072*j/16,-.119-.015*math.sin(math.pi*j/16),1.254+.009*math.sin(math.pi*j/16)-side*.004*(2*j/16-1)) for j in range(17)],.0048,'Hair','Face','head')
 ellipsoid('Ear_'+s,(side*.15,.006,1.17),(.033,.022,.044),'Skin','Body','head',20,10)
 ellipsoid('InnerEar_'+s,(side*.161,-.011,1.17),(.020,.009,.029),'SkinWarm','Face','head',16,8)
 ellipsoid('CheekTone_'+s,(side*.089,-.111,1.148),(.023,.006,.012),'SkinWarm','Face','head',16,8)
loft('Nose',[(0,-.127,1.15,.005,.004),(0,-.145,1.159,.016,.010),(0,-.153,1.17,.019,.016),(0,-.144,1.186,.011,.008),(0,-.13,1.207,.004,.004)],'Skin','Face','head',20)
curve('Smile',[(-.025+.05*j/24,-.118+.004*abs(2*j/24-1),1.108+.0045*(2*j/24-1)**2) for j in range(25)],.0016,'SkinWarm','Face','head')
curve('LowerLip',[(-.015+.03*j/16,-.119,1.102+.002*(2*j/16-1)**2) for j in range(17)],.001,'Skin','Face','head')
# Phase 4: broad curl clusters; silhouette clumps rather than individual strands.
loft('HairCap',[(0,.035,1.24,.146,.116),(0,.024,1.27,.165,.145),(0,.020,1.30,.164,.147),(0,.015,1.33,.146,.135),(0,.015,1.358,.105,.104),(0,.02,1.375,.035,.035)],'Hair','Hair','head',32,.05)
for level in range(3):
 count=[13,11,7][level]
 for j in range(count):
  a=math.tau*(j+.34*level)/count
  if level==0 and abs((a+math.pi)%(math.tau)-math.pi)<.75:continue
  rx=[.153,.13,.075][level];ry=[.14,.12,.075][level]
  x=rx*math.sin(a);y=.02-ry*math.cos(a);z=[1.272,1.321,1.356][level]+random.uniform(-.006,.006)
  o=ellipsoid('CurlCluster_%d_%d'%(level,j),(x,y,z),(.052,.04,.035),'HairLight' if j%5==0 else 'Hair','Hair','head',16,8)
  pts=[]
  for k in range(21):
   t=k/20;ang=a+t*math.pi*1.5;rad=.041*(1-t)+.003
   pts.append((x+rad*math.cos(ang),y-.022-.009*math.sin(t*math.pi),z+.027*math.sin(ang)))
  tube('CurlRidge_%d_%d'%(level,j),pts,[.009*(1-k/22)+.001 for k in range(21)],'HairLight','Hair','head',6)
for i in range(7):
 x=-.125+i*.041
 pts=[]
 for k in range(18):
  t=k/17
  pts.append((x+.023*math.sin(t*math.pi*1.4),-.134-.009*math.sin(t*math.pi),1.333-.072*t+.014*math.sin(t*math.pi)))
 tube('Forelock_'+str(i),pts,[.024*(1-k/19)+.003 for k in range(18)],'HairLight' if i%3==0 else 'Hair','Hair','head',10)
checkpoint('02_FaceHair.blend')
# Phase 5: open vest panels, collar, folded scarf and illustrated ornamental edge.
vs=[];uv=[];fs=[];rings=[(.636,.174,.113),(.70,.177,.118),(.78,.175,.12),(.85,.18,.12),(.92,.19,.112),(.984,.175,.097)]
n=36
for i,(z,rx,ry) in enumerate(rings):
 for j in range(n):
  a=.28+(math.tau-.56)*j/(n-1);h=z
  if i==len(rings)-1:h-=.078*math.sin(a)**8
  if i==0:h-=.038*math.cos(a)**4
  vs.append((rx*math.sin(a),-ry*math.cos(a),h));uv.append((j/(n-1),i/(len(rings)-1)))
for i in range(len(rings)-1):
 for j in range(n-1):fs.append((i*n+j,i*n+j+1,(i+1)*n+j+1,(i+1)*n+j))
vest=mesh('Vest',vs,fs,'Blue','Vest',uv=uv)
mod=vest.modifiers.new('Clothing thickness','SOLIDIFY');mod.thickness=.003
bpy.context.view_layer.objects.active=vest;vest.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name);vest.select_set(False)
for side in [-1,1]:
 s='L' if side==1 else 'R'
 mesh('ShirtCollar_'+s,[(side*.052,-.07,1.018),(side*.095,-.096,.973),(side*.053,-.13,.954),(side*.015,-.096,.996)],[(0,1,2,3)],'Cream','Shirt')
 edge=[(side*rx*math.sin(.28),-ry*math.cos(.28)-.002,z-(.038*math.cos(.28)**4 if i==0 else 0)) for i,(z,rx,ry) in enumerate(rings)]
 curve('VestFrontBraid_'+s,edge,.002,'Brass','Vest')
 curve('VestHem_'+s,[(side*.173*math.sin(a),-.115*math.cos(a),.636-.038*math.cos(a)**4) for a in [.28+(math.pi-.28)*j/30 for j in range(31)]],.002,'Brass','Vest')
 for k in range(3):
  x=side*(.075+.012*k);z=.72+.065*k
  pts=[(x+side*.016*math.sin(t*math.tau),-.116+.006*k-.007*math.cos(t*math.pi),z+.032*(t-.5)) for t in [j/26 for j in range(27)]]
  curve('VestLeafScroll_'+s+str(k),pts,.0018,'Brass','Vest')
  for leaf in [-1,1]:
   mesh('VestLeaf_'+s+str(k)+str(leaf),[(x,-.126+.006*k,z),(x+side*.017,-.126+.006*k,z+leaf*.012),(x+side*.006,-.128+.006*k,z+leaf*.02)],[(0,1,2)],'Brass','Vest')
loft('ScarfNeck',[(0,0,1.01,.097,.081),(0,0,1.031,.107,.09),(0,.008,1.06,.101,.088),(0,.008,1.08,.084,.075)],'Red','Scarf','neck',28,.028)
# Folded kerchief body: a closed thin triangle with an irregular front ridge.
mesh('ScarfFront',[(-.102,-.076,1.04),(-.051,-.12,1.022),(0,-.133,1.016),(.066,-.116,1.03),(.104,-.072,1.046),(0,-.146,.945),(-.044,-.137,.988),(.025,-.141,.981)],[(0,1,6),(1,2,7,6),(2,3,4,7),(6,7,5),(7,4,5),(0,6,5)],'Red','Scarf','neck')
curve('ScarfFold',[(-.095,-.097,1.02),(-.051,-.132,1.005),(0,-.145,.993),(.069,-.119,1.023)],.003,'RedLight','Scarf','neck')
mesh('ScarfTail',[(.08,-.071,1.035),(.102,-.115,1.005),(.158,-.118,.949),(.17,-.104,.916),(.184,-.08,.947),(.141,-.083,1.011)],[(0,1,2,5),(5,2,3,4)],'Red','Scarf','neck')
for z in [.905,.81,.746]:ellipsoid('ShirtButton_'+str(z),(0,-.125,z),(.0045,.003,.0045),'Brass','Shirt',seg=10,rings=6)
# Phase 6: harness, belts, pouches, stitches, robust boots.
loft('WaistBelt',[(0,0,.636,.182,.123),(0,0,.685,.183,.125)],'Leather','Belt','pelvis',32)
def ribbon(name,pts,width,mat,part,bone=None):
 vs=[];fs=[];uv=[]
 for i,(x,y,z) in enumerate(pts):
  vs.extend([(x-width/2,y,z),(x+width/2,y,z)]);uv.extend([(0,i/(len(pts)-1)),(1,i/(len(pts)-1))])
 for i in range(len(pts)-1):fs.append((i*2,i*2+1,i*2+3,i*2+2))
 o=mesh(name,vs,fs,mat,part,bone,uv);mod=o.modifiers.new('Strap thickness','SOLIDIFY');mod.thickness=.003;bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name);o.select_set(False);return o
for side in [-1,1]:
 s='L' if side==1 else 'R'
 ribbon('PackHarness_'+s,[(side*.13,.155,.752),(side*.142,.10,.94),(side*.135,.018,1.015),(side*.13,-.071,.98),(side*.133,-.112,.896),(side*.139,-.125,.80)],.033,'LeatherLight','Harness')
 for z in [.92,.83]:
  x=side*.132
  curve('HarnessBuckle_'+s+str(z),[(x-.020,-.127,z-.011),(x+.020,-.127,z-.011),(x+.020,-.127,z+.011),(x-.020,-.127,z+.011),(x-.020,-.127,z-.011)],.002,'Brass','Harness')
 box('BeltPouch_'+s,(side*.191,-.032,.595),(.087,.074,.105),'Leather','Pouches','pelvis',.013)
 box('PouchFlap_'+s,(side*.191,-.074,.629),(.095,.016,.065),'LeatherLight','Pouches','pelvis',.009)
 ribbon('PouchStrap_'+s,[(side*.191,-.085,.665),(side*.191,-.086,.61),(side*.191,-.083,.579)],.018,'LeatherDark','Pouches','pelvis')
 ellipsoid('PouchRivet_'+s,(side*.191,-.089,.604),(.004,.002,.004),'Brass','Pouches','pelvis',12,6)
 tube('WristBand_'+s,[(side*.317,0,.72),(side*.331,0,.692)],[(.034,.034),(.034,.034)],'LeatherDark','Wristbands','forearm.'+s,16)
 box('WristClasp_'+s,(side*.324,-.033,.706),(.019,.005,.018),'Brass','Wristbands','forearm.'+s,.002)
 for k in range(4):
  z=.082+k*.016;y=-.096+k*.013
  curve('BootLace_'+s+str(k),[(side*.108-.023,y,z),(side*.108+.02,y-.004,z+.008)],.0022,'Brass','Boots','foot.'+s)
 curve('BootTop_'+s,[(side*.108+.061*math.sin(a),-.062*math.cos(a),.169) for a in [math.tau*j/32 for j in range(33)]],.005,'LeatherLight','Boots','foot.'+s)
 curve('BootToeSeam_'+s,[(side*.108+.061*math.sin(a),-.034-.094*math.cos(a),.048+.012*math.cos(a)) for a in [math.tau*j/32 for j in range(33)]],.0017,'LeatherLight','Boots','foot.'+s)
 ellipsoid('KneePatch_'+s,(side*.125,-.079,.375),(.030,.009,.035),'OliveLight','Pants','leg.'+s,16,8)
 for k in range(7):
  a=math.tau*k/7;x=side*.125+.028*math.sin(a);z=.375+.031*math.cos(a)
  curve('KneeStitch_'+s+str(k),[(x-.002,-.090,z-.002),(x+.002,-.090,z+.002)],.0009,'Canvas','Pants','leg.'+s)
curve('BeltBuckle',[(-.024,-.129,.644),(.024,-.129,.644),(.024,-.13,.676),(-.024,-.13,.676),(-.024,-.129,.644)],.003,'Brass','Belt','pelvis')
ribbon('CrossBelt',[(.159,-.11,.733),(.08,-.132,.708),(0,-.139,.683),(-.082,-.13,.662),(-.158,-.106,.638)],.025,'LeatherLight','Belt','pelvis')
curve('PendantCord',[(-.045,-.089,1.018),(-.034,-.13,.955),(0,-.155,.867),(.035,-.13,.955),(.045,-.089,1.018)],.002,'LeatherDark','Pendant')
ellipsoid('PendantBase',(0,-.157,.875),(.030,.006,.030),'Brass','Pendant',seg=28,rings=10)
curve('PendantRim',[(.027*math.sin(a),-.163,.875+.027*math.cos(a)) for a in [math.tau*j/32 for j in range(33)]],.002,'LeatherLight','Pendant')
for j in range(8):
 a=math.tau*j/8;curve('PendantRay_'+str(j),[(.005*math.sin(a),-.164,.875+.005*math.cos(a)),(.023*math.sin(a),-.164,.875+.023*math.cos(a))],.0015,'Cream','Pendant')
# Phase 7: separate backpack and blanket, external pockets, straps and leaf badge.
box('PackBody',(0,.194,.826),(.309,.177,.314),'Leather','Backpack','chest',.025)
box('PackFlap',(0,.294,.92),(.317,.026,.141),'LeatherLight','Backpack','chest',.016)
box('PackOuterPocket',(0,.311,.753),(.221,.060,.133),'Leather','Backpack','chest',.012)
box('PackPocketFlap',(0,.347,.805),(.232,.020,.066),'LeatherLight','Backpack','chest',.009)
for side in [-1,1]:
 s='L' if side==1 else 'R'
 box('PackSidePocket_'+s,(side*.16,.212,.788),(.052,.119,.171),'LeatherLight','Backpack','chest',.013)
 ribbon('PackClosure_'+s,[(side*.108,.303,.98),(side*.108,.324,.90),(side*.108,.348,.80),(side*.108,.345,.716)],.022,'LeatherDark','Backpack','chest')
 curve('PackBuckle_'+s,[(side*.108-.018,.354,.872),(side*.108+.018,.354,.872),(side*.108+.018,.354,.900),(side*.108-.018,.354,.900),(side*.108-.018,.354,.872)],.0025,'Brass','Backpack','chest')
 ellipsoid('PackRivet_'+s,(side*.108,.355,.887),(.0035,.002,.0035),'Brass','Backpack','chest',10,6)
tube('Bedroll',[(-.194,.213,1.011),(-.186,.213,1.011),(0,.213,1.011),(.186,.213,1.011),(.194,.213,1.011)],[.05,.056,.058,.056,.05],'Canvas','Bedroll','chest',24)
for side in [-1,1]:
 curve('RollSpiral_'+str(side),[(side*.195,.213+(.005+.043*j/70)*math.cos(j/70*math.pi*5),1.011+(.005+.043*j/70)*math.sin(j/70*math.pi*5)) for j in range(71)],.0018,'LeatherLight','Bedroll','chest')
 curve('RollBinding_'+str(side),[(side*.121,.213+.060*math.sin(a),1.011+.060*math.cos(a)) for a in [math.tau*j/32 for j in range(33)]],.006,'LeatherDark','Bedroll','chest')
curve('CarryLoop',[(-.039,.236,1.0),(-.039,.25,1.045),(0,.263,1.052),(.039,.25,1.045),(.039,.236,1.0)],.006,'LeatherDark','Backpack','chest')
for side in [-1,1]:
 mesh('PackLeaf_'+str(side),[(0,.320,.925),(side*.026,.322,.95),(side*.037,.32,.933),(side*.023,.322,.908)],[(0,1,2,3)],'Leaf','Equipment','chest')
curve('LeafVein',[(0,.323,.902),(0,.324,.959)],.0015,'Brass','Equipment','chest')
# Reference accessory: a small field device with a warm red cap, no logo.
ellipsoid('FieldDevice',( .225,.04,.562),(.041,.039,.041),'Cream','Equipment','pelvis',20,10)
loft('FieldDeviceCap',[(.225,.04,.562,.041,.039),(.225,.04,.584,.034,.032),(.225,.04,.599,.014,.013)],'Red','Equipment','pelvis',20)
curve('FieldDeviceBand',[(.225+.042*math.sin(a),.04-.041*math.cos(a),.562) for a in [math.tau*j/28 for j in range(29)]],.002,'LeatherDark','Equipment','pelvis')
checkpoint('03_Modelled.blend')
bpy.app.driver_namespace['YT_ENV']=globals().copy()
print('PHASE_3_7_COMPLETE',len(PARTS))
