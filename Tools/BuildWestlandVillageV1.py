"""Deterministic, additive Westland village authoring, not runtime gameplay.

Run with system Python --write-layout to write the human-reviewable source layout.
Run this saved file in the full Unreal Editor to assemble only Dev_WestlandVillage.
Existing assets and maps are loaded read-only. Re-running replaces only actors tagged
WestlandVillageOwned in this task's map; generated terrain/path meshes are updated in
place. No Blender/FBX round-trip, new architecture modules, plugins or C++ required.
"""
import json, math, random, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'Art/Architecture/Westland'
SOURCE = ROOT / 'Art/World/Westland/WestlandVillage_V1.json'
MAP = '/Game/Maps/Dev_WestlandVillage'
DEST = '/Game/Environment/WestlandVillage/Meshes'
TAG = 'WestlandVillageOwned'


def rotated(p, yaw):
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return [c*p[0]-s*p[1], s*p[0]+c*p[1], p[2] if len(p)>2 else 0]


def world_point(b, p):
    v = rotated(p, b['yaw'])
    return [v[i]+b['origin_cm'][i] for i in range(3)]


def home(depth, width, door_bay, window_kind, chimney_side):
    """Assemble a rectangular home without stretching any kit mesh."""
    d, h = depth/2, width/2
    ridge = 3 + h*2/3
    roof = 'RoofPanel1m' if width == 6 else 'RoofPanel8mSpan1m'
    roof_end = 'RoofPanelEnd30cm' if width == 6 else 'RoofPanel8mSpanEnd30cm'
    gable = 'GableHalf3m' if width == 6 else 'GableHalf4m'
    trim = 'GableTrimHalf3m' if width == 6 else 'GableTrimHalf4m'
    out = []
    def place(mod, p, yaw=0, fade=False, role='Architecture'):
        p = list(p)
        if mod == 'CornerPost3m':
            p[0] += math.copysign(.06, p[0]); p[1] += math.copysign(.06,p[1])
        elif mod in ('HorizontalBeam2m','VerticalPost3m','DiagonalBrace1m'):
            if abs(p[0]) == d: p[0] += math.copysign(.14,p[0])
            elif abs(p[1]) == h: p[1] += math.copysign(.14,p[1])
        out.append({'module':mod,'position_m':p,'yaw':yaw,'cutaway':fade,'role':role})
    ys = list(range(-int(h),int(h),2)); xs = list(range(-int(d),int(d),2))
    door_y = ys[door_bay]+1
    for x in range(-int(d),int(d)):
        for y in range(-int(h),int(h)): place('Floor1m',(x,y,0))
    for front in (True,False):
        x, yaw = (-d,0) if front else (d,180)
        for i,y in enumerate(ys):
            mod = 'WallDoor2m' if front and i==door_bay else 'WallWindow'+window_kind+'2m' if front or (i==0 and depth==8) else 'WallSolid2m'
            start=y if front else -y
            place(mod,(x,start,0),yaw,front)
            place('HorizontalBeam2m',(x,start,3),yaw,front)
            if 'Window' in mod: place('Window'+window_kind,(x,y+1 if front else -y-1,1),yaw,front)
        for side in (-1,1):
            place(gable,(x,side*h,3),0 if side==-1 else 180,front)
            place(trim,(x+(-.08 if front else .08),0,ridge),0 if side==1 else 180,front)
        for y in range(-int(h),int(h)):
            if not front or abs(y+.5-door_y)>.7:
                place('StonePlinth1m',(x,y if front else -y,0),yaw,front)
    for side in (-1,1):
        y, yaw = side*h, -90 if side==1 else 90
        for i,x in enumerate(xs):
            start=x if side==1 else -x
            mod='WallWindowDouble2m' if i==len(xs)//2 else 'WallSolid2m'
            place(mod,(start,y,0),yaw)
            place('HorizontalBeam2m',(start,y,3),yaw)
            if 'Window' in mod: place('WindowDouble',(start+(1 if side==1 else -1),y,1),yaw)
        for x in range(-int(d),int(d)): place('StonePlinth1m',(x if side==1 else -x,y,0),yaw)
        for x in xs[1:]: place('VerticalPost3m',(x,y,0))
        place('DiagonalBrace1m',(-d+1,y,1.75),90)
    for x in (-d,d):
        for y in (-h,h): place('CornerPost3m',(x,y,0),fade=x==-d)
        for y in ys[1:]: place('VerticalPost3m',(x,y,0),fade=x==-d)
    for side in (-1,1):
        for x in range(-int(d),int(d)):
            place(roof,(x if side==1 else -x,0,ridge),0 if side==1 else 180,True)
            place('EaveTrim1m',(x,side*(h+.3),2.8),fade=True)
        for x in (-d-.3,d): place(roof_end,(x if side==1 else -x,0,ridge),0 if side==1 else 180,True)
    for x in range(-int(d),int(d)): place('RidgeCap1m',(x,0,ridge),fade=True)
    place('DoorFrame130x200',(-d,door_y,0),fade=True)
    place('DoorLeaf130x200',(-d-.22,door_y-.65,0),90,True)
    place('Porch160cm',(-d,door_y,0),fade=True)
    place('Threshold130cm',(-d,door_y,0))
    place('Chimney60cm',(d-.95,chimney_side*(h-1.35),ridge-1.1),fade=True)
    return out, [-d*100,door_y*100,100], ridge


def write_layout():
    cottage=json.loads((ART/'Buildings/WL_Cottage_V1.json').read_text())
    inn=json.loads((ART/'Buildings/WL_Inn_V1.json').read_text())
    buildings=[]
    for name,origin,yaw,depth,width,bay,kind,side in [
        ('Birkenhof',[-250,1050,0],-35,6,6,1,'Arch',1),
        ('Kraeuterhaus',[650,1600,20],-55,4,6,1,'Double',-1),
        ('Langhaus',[1800,1000,0],-20,8,6,0,'Arch',-1),
        ('Wiesenhaus',[400,-1600,0],-65,4,8,2,'Double',1)]:
        ps,door,ridge=home(depth,width,bay,kind,side)
        # The first home is the validated original cottage, merely repositioned.
        if name=='Birkenhof': ps=cottage['placements'];door=[-300,0,100];ridge=5
        buildings.append({'id':name,'kind':'Home','origin_cm':origin,'yaw':yaw,'body_m':[depth,width,3],
                          'ridge_m':ridge,'door_local_cm':door,'door_m':[1.3,2],
                          'camera_distance_cm':2000,'placements':ps,'primitive_proxies':[]})
    buildings.append({'id':'Gasthaus','kind':'Inn','origin_cm':[850,-250,0],'yaw':-40,
                      'body_m':[8,8,3],'ridge_m':5.75,'door_local_cm':[-300,-100,107.5],
                      'door_m':[1.6,2.15],'camera_distance_cm':2200,
                      'placements':inn['placements'],'primitive_proxies':inn['primitive_proxies'],
                      'cutaway_focus_local_cm':[100,0,150],
                      'interior_regions':[{'center':[-100,0,0],'extent':[310,410,200]},
                                          {'center':[300,100,0],'extent':[110,310,200]}]})
    for b in buildings:
        b['module_counts']=dict(sorted(Counter(p['module'] for p in b['placements']).items()))
        b['door_world_cm']=world_point(b,b['door_local_cm'])
        b['forecourt_cm']=world_point(b,[b['door_local_cm'][0]-300,b['door_local_cm'][1],0])
    a,b,c,d,inn=buildings
    paths=[{'id':'Hauptweg','width_cm':340,'points':[[-3500,100],[-2300,100],[-1600,120],[-1000,-100],[-650,-250],[-200,-150],[0,-60],inn['forecourt_cm'][:2],inn['door_world_cm'][:2]]},
           {'id':'Wohnweg','width_cm':250,'points':[[-1000,-100],[-1120,270],[-930,650],a['forecourt_cm'][:2],a['door_world_cm'][:2]]},
           {'id':'Kraeuterweg','width_cm':220,'points':[a['forecourt_cm'][:2],[-650,1780],[-120,2160],[140,2080],b['forecourt_cm'][:2],b['door_world_cm'][:2]]},
           {'id':'Ostweg','width_cm':250,'points':[[0,-60],[190,540],[790,750],c['forecourt_cm'][:2],c['door_world_cm'][:2]]},
           {'id':'Wiesenbogen','width_cm':240,'points':[[-1000,-100],[-1500,-490],[-1600,-1200],[-1250,-1880],[-440,-1870],d['forecourt_cm'][:2],d['door_world_cm'][:2]]},
           {'id':'Gasthausgarten','width_cm':210,'points':[inn['forecourt_cm'][:2],[-260,-450],[-350,-900],d['forecourt_cm'][:2]]},
           {'id':'Heilhausplatz','width_cm':220,'points':[[-1600,-1200],[-1450,-1410],[-1130,-1350]]}]
    data={'schema':'PokeMonster.WestlandVillage.v1','map':MAP,'units':'cm unless suffix _m',
          'seed':3103,'playable_bounds_cm':[-2100,-2300,2400,2500],'ground_extent_cm':7000,
          'player_start_cm':[-2050,100,60],'public_tree_cm':[-450,260,0],
          'healing_house_reserve':{'center_cm':[-1000,-1400,0],'size_cm':[1000,1100],
                                   'purpose':'Future HealingHouse V3 plot; no HealingHouse runtime actors copied'},
          'buildings':buildings,'paths':paths,'new_architecture_modules':[],
          'camera_contract':{'exterior_distance_cm':2500,'fov':35,'yaw':-45,'pitch':-55,
                             'fade_seconds':.4,'movement_cm_per_second':210,'player_visible_height_cm':140},
          'notes':['Rotated independent door thresholds; explicit roof/front occluders only',
                   'Native editor-generated landscape/path meshes, existing Paper2D vegetation',
                   'No NPCs, quests, save, battle or existing map changes']}
    SOURCE.parent.mkdir(parents=True,exist_ok=True)
    SOURCE.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')


def catmull(points, steps=12):
    out=[]
    for i in range(len(points)-1):
        p0=points[max(0,i-1)];p1=points[i];p2=points[i+1];p3=points[min(len(points)-1,i+2)]
        for j in range(steps):
            t=j/steps
            out.append([.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in (0,1)])
    return out+[list(points[-1])]


def terrain_height(data,x,y):
    height=18*math.sin(x/1700)+16*math.sin(y/1100)+11*math.cos((x+y)/1500)-15
    # The coarse triangulation must remain below every floor at shared pads.
    # Prefer the lower adjoining pad instead of lifting a neighbour's floor corner.
    core=[]
    for b in data['buildings']:
        q=rotated([x-b['origin_cm'][0],y-b['origin_cm'][1]],-b['yaw'])
        if abs(q[0])<=b['body_m'][0]*50+220 and abs(q[1])<=b['body_m'][1]*50+220:
            core.append(b['origin_cm'][2]-4)
    if core:return min(core)
    # Flat, feathered house pads preserve exact door/floor levels.
    for b in data['buildings']:
        q=rotated([x-b['origin_cm'][0],y-b['origin_cm'][1]],-b['yaw'])
        dx=max(abs(q[0])-b['body_m'][0]*50-220,0)
        dy=max(abs(q[1])-b['body_m'][1]*50-220,0)
        distance=math.hypot(dx,dy);f=max(0,1-distance/220);f=f*f*(3-2*f)
        height=height*(1-f)+(b['origin_cm'][2]-4)*f
    return height


def build():
    import unreal
    data=json.loads(SOURCE.read_text());out=ROOT/'Saved/WestlandVillage';out.mkdir(parents=True,exist_ok=True)
    editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    assert not editor.get_game_world(), 'Stop PIE before authoring'
    if unreal.EditorAssetLibrary.does_asset_exist(MAP):
        assert unreal.EditorLoadingAndSavingUtils.load_map(MAP)
    else: assert unreal.EditorLevelLibrary.new_level(MAP)
    world=editor.get_editor_world();assert world.get_name()=='Dev_WestlandVillage'
    actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in actors.get_all_level_actors():
        if a.actor_has_tag(TAG): assert actors.destroy_actor(a)
    world.get_world_settings().set_editor_property('default_game_mode',unreal.load_class(None,'/Script/PokeMonster.PokeMonsterGameMode'))
    kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text())['modules']+json.loads((ART/'WestlandBuildingKit_InnExtensions_V1.json').read_text())['modules']
    desc={m['name']:m for m in kit};meshes={m['name']:unreal.load_asset('/Game/Environment/Architecture/Westland/Meshes/'+m['category']+'/'+m['mesh']) for m in kit};assert all(meshes.values())
    def spawn(cls,label,p,yaw=0,folder='Terrain'):
        a=actors.spawn_actor_from_class(cls,unreal.Vector(*p),unreal.Rotator(yaw=yaw))
        assert a;a.set_actor_location(unreal.Vector(*p),False,False);a.set_actor_label('WV_'+label);a.set_folder_path('WestlandVillage/'+folder);a.set_editor_property('tags',[TAG]);return a
    def mesh_actor(label,mesh,p,yaw=0,material=None,collision=False,folder='Terrain',scale=None):
        a=spawn(unreal.StaticMeshActor,label,p,yaw,folder);c=a.static_mesh_component;c.set_static_mesh(mesh)
        c.set_cast_shadow(False);c.set_collision_profile_name('BlockAll' if collision else 'NoCollision');c.set_editor_property('generate_overlap_events',False)
        if collision:c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE)
        if material:c.set_material(0,material)
        if scale:a.set_actor_scale3d(unreal.Vector(*scale))
        return a
    def native_mesh(name,vs,tris,uv,material,collision):
        buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=[unreal.Vector(*v) for v in vs];buf.triangles=[unreal.IntVector(*t) for t in tris];buf.uv0=[unreal.Vector2D(*v) for v in uv]
        dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf)
        unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions())
        path=DEST+'/'+name
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            sm=unreal.load_asset(path);opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True
            unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,sm,opt,unreal.GeometryScriptMeshWriteLOD())
        else:
            opt=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();opt.enable_collision=collision;opt.collision_mode=unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE;opt.enable_nanite=False;opt.enable_recompute_normals=True
            sm,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,path,opt);assert sm,(path,result)
        if collision:
            sm.get_editor_property('body_setup').set_editor_property('double_sided_geometry',True)
            unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).enable_section_collision(sm,True,0,0)
        sm.set_material(0,material);assert unreal.EditorAssetLibrary.save_asset(path,False)
        return sm
    groundmat=unreal.load_asset('/Game/Environment/Prototype2D/Materials/M_PaintedGround')
    path_name='/Game/Environment/WestlandVillage/Materials/M_WV_Path'
    pathmat=unreal.load_asset(path_name)
    if not pathmat:
        pathmat=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_WV_Path','/Game/Environment/WestlandVillage/Materials',unreal.Material,unreal.MaterialFactoryNew())
        pathmat.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT);pathmat.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT);pathmat.set_editor_property('two_sided',True)
        lib=unreal.MaterialEditingLibrary
        pos=lib.create_material_expression(pathmat,unreal.MaterialExpressionWorldPosition,-600,0)
        tex=lib.create_material_expression(pathmat,unreal.MaterialExpressionTextureCoordinate,-600,200)
        custom=lib.create_material_expression(pathmat,unreal.MaterialExpressionCustom,-350,100)
        custom.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT4)
        inputs=[]
        for name in ('P','UV'):
            item=unreal.CustomInput();item.set_editor_property('input_name',name);inputs.append(item)
        custom.set_editor_property('inputs',inputs)
        custom.set_editor_property('code','float n=sin(P.x*.019+sin(P.y*.026)*1.7)*sin(P.y*.017); float fine=sin(P.x*.21+P.y*.14)*sin(P.y*.31); float edge=abs(UV.y*2-1); float a=1-smoothstep(.72,.995,edge+n*.035); float end=smoothstep(0,.018,UV.x)*(1-smoothstep(.982,1,UV.x)); return float4(float3(.22,.155,.081)*(1+n*.085+fine*.035),a*end);')
        lib.connect_material_expressions(pos,'',custom,'P');lib.connect_material_expressions(tex,'',custom,'UV')
        rgb=lib.create_material_expression(pathmat,unreal.MaterialExpressionComponentMask,-100,0);rgb.set_editor_property('r',True);rgb.set_editor_property('g',True);rgb.set_editor_property('b',True);rgb.set_editor_property('a',False)
        alpha=lib.create_material_expression(pathmat,unreal.MaterialExpressionComponentMask,-100,200);alpha.set_editor_property('r',False);alpha.set_editor_property('g',False);alpha.set_editor_property('b',False);alpha.set_editor_property('a',True)
        lib.connect_material_expressions(custom,'',rgb,'');lib.connect_material_expressions(custom,'',alpha,'')
        lib.connect_material_property(rgb,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR);lib.connect_material_property(alpha,'',unreal.MaterialProperty.MP_OPACITY);lib.recompile_material(pathmat)
        assert unreal.EditorAssetLibrary.save_asset(path_name,False)
    # ComponentMask's unnamed input is an empty pin name, not 'Input'.
    nodes=[e for e in unreal.ObjectIterator(unreal.MaterialExpression) if e.get_outer()==pathmat]
    custom=next(e for e in nodes if isinstance(e,unreal.MaterialExpressionCustom))
    for e in nodes:
        if isinstance(e,unreal.MaterialExpressionComponentMask):
            assert unreal.MaterialEditingLibrary.connect_material_expressions(custom,'',e,'')
    unreal.MaterialEditingLibrary.recompile_material(pathmat)
    assert unreal.EditorAssetLibrary.save_asset(path_name,False)
    vs=[];uv=[];tris=[];n=71
    for i in range(n):
        for j in range(n):
            x=-7000+i*200;y=-7000+j*200;vs.append((x,y,terrain_height(data,x,y)));uv.append((i/70,j/70))
    for i in range(n-1):
        for j in range(n-1):
            a=i*n+j;b=(i+1)*n+j;c=b+1;d=a+1;tris.extend([(a,b,c),(a,c,d)])
    ground=native_mesh('SM_WV_Ground',vs,tris,uv,groundmat,True);mesh_actor('MeadowTerrain',ground,(0,0,0),collision=True)
    def ground_surface(x,y):
        # Match the already triangulated terrain, not its analytic authoring field.
        i=max(0,min(69,math.floor((x+7000)/200)));j=max(0,min(69,math.floor((y+7000)/200)))
        x0=-7000+i*200;y0=-7000+j*200;fx=(x-x0)/200;fy=(y-y0)/200
        a=terrain_height(data,x0,y0);b=terrain_height(data,x0+200,y0)
        c=terrain_height(data,x0+200,y0+200);d=terrain_height(data,x0,y0+200)
        return a+(b-a)*fx+(c-b)*fy if fy<=fx else a+(c-d)*fx+(d-a)*fy
    vs=[];uv=[];tris=[];paths=[]
    for path in data['paths']:
        authored=catmull(path['points']);paths.append((authored,path['width_cm']))
        pts=[]
        for a,b in zip(authored,authored[1:]):
            steps=max(1,math.ceil(math.hypot(b[0]-a[0],b[1]-a[1])/25))
            pts.extend([[a[k]+(b[k]-a[k])*j/steps for k in (0,1)] for j in range(steps)])
        pts.append(authored[-1]);start=len(vs);cross_steps=8
        for i,p in enumerate(pts):
            q=pts[max(0,i-1)];r=pts[min(len(pts)-1,i+1)];dx=r[0]-q[0];dy=r[1]-q[1];length=max(1,math.hypot(dx,dy));width=path['width_cm']*(1+.055*math.sin(i*.11))
            for j in range(cross_steps+1):
                sign=j/cross_steps*2-1;x=p[0]-dy/length*width/2*sign;y=p[1]+dx/length*width/2*sign
                vs.append((x,y,ground_surface(x,y)+3));uv.append((.015+.97*i/(len(pts)-1),j/cross_steps))
                if i and j:
                    a=start+(i-1)*(cross_steps+1)+j-1;b=a+cross_steps+1
                    tris.extend([(a,b,b+1),(a,b+1,a+1)])
    ribbon=native_mesh('SM_WV_Paths',vs,tris,uv,pathmat,False);mesh_actor('CurvedFootpaths',ribbon,(0,0,0))
    cutclass=unreal.load_class(None,'/Script/PokeMonster.PokeMonsterBuildingCutaway');cuts=[]
    for b in data['buildings']:
        folder='Buildings/'+b['id'];occluders=[]
        for i,p in enumerate(b['placements']):
            a=mesh_actor(b['id']+'_'+str(i).zfill(3)+'_'+p['module'],meshes[p['module']],world_point(b,[v*100 for v in p['position_m']]),b['yaw']+p['yaw'],collision=bool(desc[p['module']]['collision_boxes']),folder=folder)
            a.set_editor_property('tags',[TAG,'WV_Building_'+b['id'],'WV_Module_'+p['module'],'WV_Occluder' if p['cutaway'] else 'WV_Retained'])
            if p.get('role')=='HearthReserve':
                for slot in range(a.static_mesh_component.get_num_materials()):a.static_mesh_component.set_material(slot,unreal.load_asset('/Game/Environment/Architecture/Westland/Materials/M_WL_Stone'))
            if p['cutaway']:occluders.append(a)
        cube=unreal.load_asset('/Engine/BasicShapes/Cube')
        for i,p in enumerate(b['primitive_proxies']):
            mesh_actor(b['id']+'_Counter_'+str(i),cube,world_point(b,[v*100 for v in p['position_m']]),b['yaw'],unreal.load_asset('/Game/Environment/Architecture/Westland/Materials/M_WL_'+p['material']),True,folder,p['size_m'])
        focus=b.get('cutaway_focus_local_cm',[0,0,150]);cut=spawn(cutclass,b['id']+'_Cutaway',world_point(b,focus),b['yaw'],folder)
        for prop,value in {'use_interior_camera':True,'interior_camera_distance':b['camera_distance_cm'],'interior_camera_pitch':-50,'interior_camera_yaw_offset':0,'interior_camera_target':unreal.Vector(0,0,-70),'fade_duration':.4,'threshold_hysteresis':4,'occluding_actors':occluders}.items():cut.set_editor_property(prop,value)
        cut.get_editor_property('interior_area').set_box_extent(unreal.Vector(b['body_m'][0]*50+10,b['body_m'][1]*50+10,200))
        threshold=cut.get_editor_property('door_threshold');door=b['door_local_cm'];threshold.set_relative_location(unreal.Vector(*(door[i]-focus[i] for i in range(3))),False,False);threshold.set_box_extent(unreal.Vector(20,b['door_m'][0]*50,b['door_m'][1]*50))
        if b.get('interior_regions'):
            regions=[]
            for item in b['interior_regions']:
                r=unreal.PokeMonsterBuildingInteriorRegion();r.set_editor_property('center',unreal.Vector(*item['center']));r.set_editor_property('extent',unreal.Vector(*item['extent']));regions.append(r)
            cut.set_editor_property('interior_regions',regions)
        cuts.append({'id':b['id'],'modules':len(b['placements']),'occluders':len(occluders)})
    sprites={name:unreal.load_asset('/Game/Environment/Prototype2D/Sprites/'+asset) for name,asset in [('Tree','S_Oak'),('Bush','S_Bush'),('Rock','S_Rock')]}
        # Existing small flora paths are resolved by asset name, never created/imported.
    flora=unreal.EditorAssetLibrary.list_assets('/Game/Environment/Prototype2D/Details',True,False)
    extras=[p for p in flora if any(n in p.lower() for n in ('grass','flower'))]
    assert all(sprites.values())
    cube=unreal.load_asset('/Engine/BasicShapes/Cube');cylinder=unreal.load_asset('/Engine/BasicShapes/Cylinder')
    wood=unreal.load_asset('/Game/Environment/Architecture/Westland/Materials/M_WL_Wood')
    stone=unreal.load_asset('/Game/Environment/Architecture/Westland/Materials/M_WL_Stone')
    def sprite(label,kind,x,y,scale,foreground=False):
        z=terrain_height(data,x,y);a=spawn(unreal.PaperSpriteActor,label,(x,y,z),45,'Vegetation/Foreground' if foreground else 'Vegetation')
        c=a.render_component;c.set_mobility(unreal.ComponentMobility.MOVABLE);assert c.set_sprite(sprites[kind]);c.set_mobility(unreal.ComponentMobility.STATIC);c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False)
        if kind=='Flora':a.set_actor_rotation(unreal.Rotator(yaw=45,roll=-55),False)
        a.set_actor_scale3d(unreal.Vector(scale,scale,scale));a.set_editor_property('tags',[TAG,'WV_Vegetation_'+kind]);return a
    def on_path(x,y,padding=0):
        for pts,width in paths:
            if any(math.hypot(x-p[0],y-p[1])<width/2+padding for p in pts):return True
        return False
    def on_building(x,y,padding=0):
        for b in data['buildings']:
            q=rotated([x-b['origin_cm'][0],y-b['origin_cm'][1]],-b['yaw'])
            if abs(q[0])<b['body_m'][0]*50+padding and abs(q[1])<b['body_m'][1]*50+padding:return True
        reserve=data['healing_house_reserve'];return abs(x-reserve['center_cm'][0])<500 and abs(y-reserve['center_cm'][1])<550
    def tree(label,x,y,scale):
        sprite(label,'Tree',x,y,scale)
        collider=mesh_actor(label+'_TrunkCollision',cylinder,(x,y,terrain_height(data,x,y)+60),material=wood,collision=True,folder='Vegetation/Trunks',scale=(.65,.65,1.2));collider.set_actor_hidden_in_game(True)
    tree('OldVillageOak',*data['public_tree_cm'][:2],1.35)
    rng=random.Random(data['seed']);counts=Counter()
    # Deliberate loose groves/hedges, rather than a uniform grid or map-wide scatter.
    clusters=[(-2000,700,220,300),(-1600,1700,250,470),(100,2650,850,200),(2200,2300,440,350),(2800,700,220,750),(1700,-1850,280,490),(-350,-2650,920,180),(-2200,-1150,210,650),(-450,260,120,90)]
    for ci,(cx,cy,rx,ry) in enumerate(clusters):
        for j in range(12 if ci<8 else 0):
            x=cx+rng.uniform(-rx,rx);y=cy+rng.uniform(-ry,ry)
            if on_path(x,y,140) or on_building(x,y,170):continue
            tree('Grove_'+str(ci)+'_'+str(j),x,y,rng.uniform(.72,1.15));counts['trees']+=1
        for j in range(18):
            x=cx+rng.uniform(-rx,rx);y=cy+rng.uniform(-ry,ry)
            if on_path(x,y,40) or on_building(x,y,110):continue
            sprite('Hedge_'+str(ci)+'_'+str(j),'Bush',x,y,rng.uniform(.62,1.1),ci in (5,6,7));counts['bushes']+=1
    for i in range(330):
        p=data['paths'][i%len(data['paths'])];pts=catmull(p['points']);idx=rng.randrange(1,len(pts)-1);q=pts[idx];r=pts[idx+1];dx=r[0]-q[0];dy=r[1]-q[1];length=max(1,math.hypot(dx,dy));offset=p['width_cm']/2+rng.uniform(35,110);sign=rng.choice((-1,1));x=q[0]-dy/length*offset*sign;y=q[1]+dx/length*offset*sign
        if on_building(x,y,85) or on_path(x,y,22):continue
        sprite('Wayside_'+str(i),'Bush' if i%5 else 'Rock',x,y,rng.uniform(.4,.75));counts['wayside']+=1
    if extras:
        for i in range(210):
            x=rng.uniform(-2100,2500);y=rng.uniform(-2300,2550)
            if on_building(x,y,120) or on_path(x,y,20):continue
            asset=unreal.load_asset(extras[1 if i%9==0 else 0]);sprites['Flora']=asset;sprite('SmallFlora_'+str(i),'Flora',x,y,rng.uniform(.55,.9));counts['flora']+=1
    # Modest home plots: two discontinuous low fences, two herb beds, a wood stack.
    for b in data['buildings'][:2]:
        for i in range(3):
            pp=[b['body_m'][0]*50+190,-350+i*100,terrain_height(data,*world_point(b,[b['body_m'][0]*50+190,-350+i*100,0])[:2])-b['origin_cm'][2]+44]
            mesh_actor(b['id']+'_FenceRail_'+str(i),cube,world_point(b,pp),b['yaw'],wood,True,'Properties',(.12,.88,.08))
            mesh_actor(b['id']+'_FencePost_'+str(i),cube,world_point(b,[pp[0],pp[1]-48,pp[2]-12]),b['yaw'],wood,True,'Properties',(.13,.13,.68))
        for i in range(6):
            wp=world_point(b,[b['body_m'][0]*50+135,120+i*40,0]);sprite(b['id']+'_Herbs_'+str(i),'Bush',wp[0],wp[1],.32)
    b=data['buildings'][2]
    for i in range(4):
        wp=world_point(b,[b['body_m'][0]*50+135,100+i*35,36]);mesh_actor('Langhaus_WoodStack_'+str(i),cylinder,wp,b['yaw'],wood,False,'Properties',(.23,.23,.7))
    reserve=data['healing_house_reserve'];cx,cy,_=reserve['center_cm']
    for i in range(9):sprite('HealingPlotBoundary_'+str(i),'Rock',cx+400,cy-450+i*110,.38)
    for i in range(7):sprite('HealingPlotHerbs_'+str(i),'Bush',cx-350+i*110,cy-430,.45)
    spawn(unreal.PlayerStart,'PlayerStart',data['player_start_cm'],folder='Test')
    sun=spawn(unreal.DirectionalLight,'SoftDaylight',(0,0,900),folder='Lighting');sun.set_actor_rotation(unreal.Rotator(pitch=-55,yaw=-30),False);sun.light_component.set_editor_property('intensity',2.2);sun.light_component.set_editor_property('cast_shadows',False)
    sky=spawn(unreal.SkyLight,'SoftAmbient',(0,0,700),folder='Lighting');sky.light_component.set_editor_property('source_type',unreal.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP);sky.light_component.set_editor_property('cubemap',unreal.load_asset('/Engine/EngineResources/DefaultTextureCube'));sky.light_component.set_editor_property('intensity',.7)
    pp=spawn(unreal.PostProcessVolume,'StableExposure',(0,0,0),folder='Lighting');pp.set_editor_property('unbound',True)
    settings=pp.get_editor_property('settings');settings.set_editor_property('override_auto_exposure_method',True);settings.set_editor_property('auto_exposure_method',unreal.AutoExposureMethod.AEM_MANUAL);settings.set_editor_property('override_auto_exposure_apply_physical_camera_exposure',True);settings.set_editor_property('auto_exposure_apply_physical_camera_exposure',False);settings.set_editor_property('override_auto_exposure_bias',True);settings.set_editor_property('auto_exposure_bias',0);pp.set_editor_property('settings',settings)
    assert unreal.EditorLoadingAndSavingUtils.save_map(world,MAP)
    (out/'Authoring.json').write_text(json.dumps({'map':MAP,'buildings':cuts,'vegetation_counts':dict(counts),'small_flora_assets':extras,'actors':len(actors.get_all_level_actors()),'new_assets':[DEST+'/SM_WV_Ground',DEST+'/SM_WV_Paths',path_name],'terrain_triangles':9800,'no_cpp_changes':True},indent=2)+'\n')
    unreal.log('WESTLAND_VILLAGE_BUILD_COMPLETE')


if __name__=='__main__':
    if '--write-layout' in sys.argv: write_layout()
    else: build()
