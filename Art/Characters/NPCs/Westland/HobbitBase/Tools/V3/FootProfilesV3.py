import bpy,bmesh,math
from pathlib import Path
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_Base_V3_Body'];bpy.context.window.scene=s;o=s.objects['HNV3_Body']
ys=[.114,.101,.086,.068,.054,.046,.038,.030,.022,.014,.006,-.002,-.010,-.018,-.026,-.045,-.068,-.087,-.104,-.121,-.135]
profile=[(-.135,.041),(-.110,.047),(-.085,.060),(-.055,.078),(-.026,.105),(.022,.103),(.054,.095),(.086,.0736),(.101,.0631),(.114,.054)]
def height(y):
 for k,(a,b) in enumerate(zip(profile,profile[1:])):
  if a[0]<=y<=b[0]:
   t=(y-a[0])/(b[0]-a[0]);h=b[0]-a[0];aa=profile[max(0,k-1)];bb=profile[min(len(profile)-1,k+2)];ma=(b[1]-aa[1])/(b[0]-aa[0]);mb=(bb[1]-a[1])/(bb[0]-a[0])
   return (2*t**3-3*t*t+1)*a[1]+(t**3-2*t*t+t)*h*ma+(-2*t**3+3*t*t)*b[1]+(t**3-t*t)*h*mb
 raise ValueError(y)
count=0
for v in o.data.vertices:
 x,y,z=v.co
 if z>.110 or z<.006 or abs(x)>.3:continue
 candidates=[yy for yy in ys if abs(y-yy)<1e-6]
 if not candidates:continue
 y=candidates[0]
 if y>.07:old=.054+(.114-y)*.70
 elif y>-.03:old=.105
 elif y>-.10:old=.088-(abs(y)-.03)*.35
 else:old=.054
 v.co.z*=height(y)/old;count+=1
bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
stage=BASE/'Source/StagesV3/Hobbit_NPC_Base_V3_09_FootProfiles.blend';assert not stage.exists();bpy.data.libraries.write(str(stage),{s});bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V3_Body.blend'),{s});print('Continuous foot instep height profile, vertices',count)
