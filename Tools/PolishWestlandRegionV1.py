"""Owned region finishing: smooth road ends, a real river drop and local ground audit.
Call only outside PIE, after the initial complete main-route test.
"""
import unreal,runpy,json,math,sys
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'))
import WestlandRegionLayout as L
B=runpy.run_path(str(ROOT/'Tools/BuildWestlandRegionV1.py'),run_name='region_library');E=B['E'];A=B['A'];assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion'
def update(sm,vs,tri,uv):
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=[unreal.Vector(*v) for v in vs];buf.triangles=[unreal.IntVector(t[0],t[2],t[1]) for t in tri];buf.uv0=[unreal.Vector2D(*p) for p in uv];d=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,buf)
 opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,sm,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
def job():
 # Normalize longitudinal UVs so existing organic shader fades both road ends.
 for name,points,width in L.PATHS:
  pts=L.sample(points);vs=[];uv=[];tri=[]
  for i,p in enumerate(pts):
   q=pts[max(0,i-1)];r=pts[min(len(pts)-1,i+1)];dx=r[0]-q[0];dy=r[1]-q[1];length=max(.01,math.hypot(dx,dy));ww=width*(1+.045*math.sin(i*.2))
   for j in range(5):
    s=j/4*2-1;e=p[0]-dy/length*ww/2*s;n=p[1]+dx/length*ww/2*s;vs.append(L.world(e,n,B['path_height'](e,n)));uv.append((i/(len(pts)-1),j/4))
    if i and j:a=(i-1)*5+j-1;b=a+5;tri.extend([(a,a+1,b+1),(a,b+1,b)])
  update(unreal.load_asset(L.ASSETS+'/Meshes/SM_WR_Path_'+name),vs,tri,uv);yield name
 # Independent geometry and materials stay editable; no regional mega-mesh.
 # The steep reach is a 3.5 m fall; duplicate rows form its vertical water face.
 rows=[(-420+i*2,L.water(-420+i*2)) for i in range(421) if not 166<(-420+i*2)<184]
 rows.extend([(166,3.2),(174.5,3.5),(174.5,7.0),(184,7.0)]);rows.sort(key=lambda p:(p[0],p[1]));vs=[];uv=[];tri=[]
 for i,(n,z) in enumerate(rows):
  e=L.river(n);width=7+.9*math.sin(n/19)
  for j in range(5):vs.append(L.world(e+(j/4*2-1)*width/2,n,z));uv.append((j/4,n/8))
  if i:
   for j in range(4):a=(i-1)*5+j;b=a+5;tri.extend([(a,b,b+1),(a,b+1,a+1)])
 water=unreal.load_asset(L.ASSETS+'/Materials/M_WR_River');water.set_editor_property('two_sided',True);lib=unreal.MaterialEditingLibrary;lib.delete_all_material_expressions(water)
 pos=lib.create_material_expression(water,unreal.MaterialExpressionWorldPosition);tm=lib.create_material_expression(water,unreal.MaterialExpressionTime);c=lib.create_material_expression(water,unreal.MaterialExpressionCustom);c.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
 inputs=[]
 for n in ['P','T']:ii=unreal.CustomInput();ii.set_editor_property('input_name',n);inputs.append(ii)
 c.set_editor_property('inputs',inputs);c.set_editor_property('code','float wave=sin(P.x*.011+P.y*.008+T*.55)*sin(P.y*.026-T*.8);float depth=.5+.5*sin(P.x*.0023+P.y*.0018);return lerp(float3(.022,.12,.16),float3(.08,.28,.31),depth)*(.95+.05*wave);');lib.connect_material_expressions(pos,'',c,'P');lib.connect_material_expressions(tm,'',c,'T');lib.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);rough=lib.create_material_expression(water,unreal.MaterialExpressionConstant);rough.r=.65;lib.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);lib.recompile_material(water);unreal.EditorAssetLibrary.save_loaded_asset(water,False)
 update(unreal.load_asset(L.ASSETS+'/Meshes/SM_WR_River'),vs,tri,uv);yield 'vertical waterfall and restrained water variation'
 # Natural water lip remains blocked by the existing visible river corridor.
 sm=unreal.load_asset(L.ASSETS+'/Meshes/SM_WR_Terrain_05_05');vs=[];uv=[];tri=[]
 for i in range(51):
  for j in range(51):
   e=i*2;n=100+j*2;z=L.height(e,n)
   if 165<n<185 and abs(e-L.river(n))<6:
    zz=3.5 if n<174.5 else 7.;dist=abs(e-L.river(n));f=max(0,1-max(0,dist-4)/2);z=z*(1-f)+(zz-.8)*f
   vs.append(L.world(e,n,z));uv.append((e/2,n/2))
 for i in range(50):
  for j in range(50):a=i*51+j;b=a+51;c=b+1;d=a+1;tri.extend([(a,d,c),(a,c,b)])
 update(sm,vs,tri,uv);yield 'waterfall bed step'
 # The initial farm screenshot was too far from the house. Walk to its forecourt
 # in the test instead of changing PlayerStart or the established main-route origin.
 (OUT/'Polish.json').write_text(json.dumps({'road_end_uvs':[0,1],'waterfall_height_m':3.5,'waterfall_north_m':174.5,'camera_unchanged':True,'player_start_unchanged':True},indent=2));yield 'finish'
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wr_polish);del unreal._wr_polish;unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
 except Exception as ex:unreal.unregister_slate_post_tick_callback(unreal._wr_polish);del unreal._wr_polish;unreal.log_error('REGION_POLISH_FAILED '+repr(ex))
 busy=False
unreal._wr_polish=unreal.register_slate_post_tick_callback(tick)
