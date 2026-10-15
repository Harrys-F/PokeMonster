import bpy,json
from mathutils import Vector
body=bpy.data.objects['HNB_Body'];adjusted=[]
for name,offset in [('HNB_GentleSmile',.0014),('HNB_Brow_L',.0025),('HNB_Brow_R',.0025)]:
 o=bpy.data.objects[name];verts=o.data.vertices
 for i in range(0,len(verts),8):
  rr=list(verts[i:i+8]);centre=sum((v.co for v in rr),Vector())/len(rr);hit,loc,n,face=body.ray_cast(Vector((centre.x,-1,centre.z)),Vector((0,1,0)),distance=2)
  assert hit,(name,centre)
  dy=loc.y-offset-centre.y
  for v in rr:v.co.y+=dy
 adjusted.append(name)
print(json.dumps({'face_details_projected_on_actual_skin':adjusted}))
