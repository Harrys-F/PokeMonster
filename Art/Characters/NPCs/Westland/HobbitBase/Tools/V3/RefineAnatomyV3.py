import bpy,math,json
from pathlib import Path
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
s=bpy.data.scenes['Hobbit_NPC_Base_V3_Body'];bpy.context.window.scene=s;o=s.objects['HNV3_Body']
def g(x,z,cx,cz,rx,rz):return math.exp(-((x-cx)/rx)**2-((z-cz)/rz)**2)
# Local form controls on the freshly built cage, no subdivision/remesh or V2.
for v in o.data.vertices:
 x,y,z=v.co
 if z>1.055:
  side=min(1,abs(x)/.11)
  v.co.z+=.004*side**2*math.exp(-((z-1.084)/.021)**2)
  if z>1.205:v.co.x*=1-.055*math.exp(-((z-1.232)/.031)**2)
  if y<-.020:
   # Jochbein and brow plane rather than an undifferentiated round face.
   v.co.y-=.0028*g(abs(x),z,.071,1.148,.029,.018)
   v.co.y-=.0028*g(abs(x),z,.052,1.184,.032,.007)
   fold_x=.029+.23*(1.117-z)
   v.co.y+=.0012*g(abs(x),z,fold_x,1.103,.0035,.012)
   v.co.y-=.0015*g(x,z,0,1.082,.025,.0035)
   v.co.y+=.0015*g(x,z,0,1.072,.034,.004)
 # Quietly shaped patella, olecranon, thumb pad and Achilles planes.
 if .350<z<.412 and y<-.024:
  v.co.y-=.004*g(abs(x),z,.112,.373,.029,.022)
 if .16<z<.26 and y>.022:
  v.co.y+=.002*g(abs(x),z,.112,.203,.012,.041)
 if .372<abs(x)<.415 and z<1.003:
  v.co.z-=.0016*math.exp(-((abs(x)-.392)/.012)**2)

# Continuous spherical eye shading eliminates faceted vertex-colour pupils.
for eye in [s.objects['HNV3_Eyeball_L'],s.objects['HNV3_Eyeball_R']]:
 mat=bpy.data.materials.new('HNV3_NaturalEye_'+eye.name[-1]);mat.use_nodes=True;nt=mat.node_tree;p=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Roughness'].default_value=.28;p.inputs['Specular IOR Level'].default_value=.28
 tc=nt.nodes.new('ShaderNodeTexCoord');split=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(tc.outputs['Generated'],split.inputs[0])
 def mathnode(op,a,b=None):
  n=nt.nodes.new('ShaderNodeMath');n.operation=op
  if hasattr(a,'is_output'):nt.links.new(a,n.inputs[0])
  else:n.inputs[0].default_value=a
  if b is not None:
   if hasattr(b,'is_output'):nt.links.new(b,n.inputs[1])
   else:n.inputs[1].default_value=b
  return n.outputs[0]
 dx=mathnode('SUBTRACT',split.outputs['X'],.5);dz=mathnode('SUBTRACT',split.outputs['Z'],.5)
 rad=mathnode('SQRT',mathnode('ADD',mathnode('MULTIPLY',dx,dx),mathnode('MULTIPLY',dz,dz)))
 ramp=nt.nodes.new('ShaderNodeValToRGB');nt.links.new(rad,ramp.inputs[0]);cr=ramp.color_ramp;cr.elements.remove(cr.elements[-1]);cr.elements[0].position=.075;cr.elements[0].color=(.009,.007,.005,1)
 for pos,col in [(.102,(.17,.070,.022,1)),(.165,(.23,.113,.036,1)),(.194,(.085,.040,.015,1)),(.205,(.70,.68,.62,1))]:cr.elements.new(pos).color=col
 front=mathnode('LESS_THAN',split.outputs['Y'],.5);mix=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(front,mix.inputs[0]);mix.inputs[1].default_value=(.70,.68,.62,1);nt.links.new(ramp.outputs['Color'],mix.inputs[2]);nt.links.new(mix.outputs[0],p.inputs['Base Color']);eye.data.materials.clear();eye.data.materials.append(mat)

p=next(n for n in o.data.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Roughness'].default_value=.72;p.inputs['Specular IOR Level'].default_value=.20
bpy.context.view_layer.update();stage=BASE/'Source/StagesV3/Hobbit_NPC_Base_V3_08_AnatomicalPlanes.blend';assert not stage.exists();bpy.data.libraries.write(str(stage),{s});bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V3_Body.blend'),{s});print('Saved local anatomical planes and continuous eyes')
