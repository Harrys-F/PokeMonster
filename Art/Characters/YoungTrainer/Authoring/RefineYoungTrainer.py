"""Reference corrections after four-view model review, before UV/rig work."""
import bpy
E=bpy.app.driver_namespace['YT_ENV'];globals().update(E)
# Flatten the facial mask slightly; keep the cranium and soft chin.
o=bpy.data.objects['YT_Head']
rr=[(0,.013,1.035,.035,.035),(0,.006,1.055,.080,.068),(0,0,1.095,.121,.104),(0,0,1.135,.147,.127),(0,.008,1.185,.156,.142),(0,.012,1.23,.149,.145),(0,.013,1.275,.131,.133),(0,.016,1.315,.09,.094),(0,.018,1.335,.03,.035)]
for i,row in enumerate(rr):
 for j in range(40):
  a=math.tau*j/40;c=math.cos(a)
  if c>0:o.data.vertices[i*40+j].co.y=row[1]-row[4]*c**.4
# Shallow eye surfaces, iris embedded rather than protruding globes.
for side in [-1,1]:
 s='L' if side==1 else 'R';x=side*.064
 w=bpy.data.objects['YT_EyeWhite_'+s]
 for v in w.data.vertices:
  if v.index==0:v.co.y=-.134
  else:v.co.y=-.126
 for name,cy,depth in [('Iris',-.135,.003),('Pupil',-.139,.0013),('EyeCatch',-.141,.001),('EyeCatchSmall',-.141,.0008)]:
  ob=bpy.data.objects['YT_'+name+'_'+s];ys=[v.co.y for v in ob.data.vertices];old=(max(ys)+min(ys))/2;span=(max(ys)-min(ys))/2
  for v in ob.data.vertices:v.co.y=cy+(v.co.y-old)/max(span,.0001)*depth
  if name=='Iris':
   for v in ob.data.vertices:v.co.x=x+(v.co.x-x)*.9
 ob=bpy.data.objects['YT_CheekTone_'+s];PARTS.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)
 ellipsoid('ShoulderShape_'+s,(side*.171,0,.987),(.053,.057,.036),'Cream','Shirt','arm.'+s,20,8).parent=bpy.data.objects['YT_CharacterRoot']
for ob in PARTS:
 if ob.name.startswith('YT_Forelock_'):
  i=int(ob.name.rsplit('_',1)[-1]);points=[(v.co.x,v.co.y,v.co.z) for v in ob.data.vertices]
  for k in range(18):
   verts=list(ob.data.vertices[k*10:(k+1)*10]);center=sum((v.co for v in verts),Vector())/10
   for v in verts:
    d=v.co-center;v.co=center+Vector((d.x*.78,d.y*.35,d.z*.7));v.co.z-=.013*(k/17) if i in [1,4] else 0
 elif ob.name.startswith('YT_CurlRidge_'):
  # Tapered strand ridge was too sausage-like in silhouette.
  for k in range(21):
   verts=list(ob.data.vertices[k*6:(k+1)*6]);center=sum((v.co for v in verts),Vector())/6
   for v in verts:v.co=center+(v.co-center)*.50
# Broad locks cover the sides/nape instead of leaving a bald lower hemisphere.
for level,(z,rx,ry,n) in enumerate([(1.175,.156,.136,13),(1.22,.169,.148,15)]):
 for j in range(n):
  a=math.tau*j/n
  if abs((a+math.pi)%math.tau-math.pi)<1.03:continue
  x=rx*math.sin(a);y=.027-ry*math.cos(a)
  ob=ellipsoid('NapeCurl_%d_%d'%(level,j),(x,y,z+random.uniform(-.008,.008)),(.044,.034,.045),'Hair','Hair','head',16,8);ob.parent=bpy.data.objects['YT_CharacterRoot']
  pts=[(x+.03*(1-k/24)*math.cos(a+k/24*math.pi*1.4),y+.018*math.sin(a),z+.033*math.sin(a+k/24*math.pi*1.4)) for k in range(25)]
  ob=tube('NapeCurlRidge_%d_%d'%(level,j),pts,[.004*(1-k/26)+.001 for k in range(25)],'HairLight','Hair','head',6);ob.parent=bpy.data.objects['YT_CharacterRoot']
# Fine stitched cloth/leather seams, never microgeometry in every surface.
for side in [-1,1]:
 s='L' if side==1 else 'R'
 for j in range(9):
  x=side*.075;z=.682+j*.026
  ob=curve('VestStitch_'+s+str(j),[(x-.0015,-.119,z),(x+.0015,-.12,z+.004)],.0008,'Cream','Vest');ob.parent=bpy.data.objects['YT_CharacterRoot']
for ob in PARTS:
 if ob.parent is None:ob.parent=bpy.data.objects['YT_CharacterRoot']
checkpoint('04_ReferenceRefined.blend')
bpy.app.driver_namespace['YT_ENV']=globals().copy()
print('REFERENCE_CORRECTIONS_COMPLETE',len(PARTS))
