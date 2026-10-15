import bpy,bmesh,json,math
from pathlib import Path
from mathutils.kdtree import KDTree
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V1'];o=s.objects['HNM1_Body'];me=o.data;bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table();bm.edges.ensure_lookup_table();uv=me.uv_layers.active
rows=[]
def weights(v):return {g.group:g.weight for g in me.vertices[v.index].groups}
def diff(a,b):
 aa,bb=weights(a),weights(b);return max(abs(aa.get(k,0)-bb.get(k,0)) for k in set(aa)|set(bb))
for e in bm.edges:
 if not e.is_boundary:continue
 p,q=e.verts;mid=(p.co+q.co)*.5
 dominant=o.vertex_groups[max(me.vertices[p.index].groups,key=lambda g:g.weight).group].name
 region='Forearm' if .35<abs(mid.x)<.61 and .96<mid.z<1.09 and ('arm' in dominant or 'hand' in dominant) else 'Cape' if .25<mid.z<.88 and mid.y>.09 and dominant.startswith('cape') else None
 if not region:continue
 f=e.link_faces[0];loop=next(l for l in f.loops if l.edge==e);a=loop.vert;b=loop.link_loop_next.vert
 uvmap={v:uv.data[f.index*3+j].uv.copy() for j,v in enumerate(f.verts)}
 rows.append({'edge':e,'a':a,'b':b,'mid':mid,'normal':f.normal.copy(),'uv':uvmap,'region':region})
kd=KDTree(len(rows))
for i,r in enumerate(rows):kd.insert(r['mid'],i)
kd.balance();possible=[]
for i,r in enumerate(rows):
 for _,j,d in kd.find_range(r['mid'],.001):
  if j<=i:continue
  t=rows[j];a,b,c,dv=r['a'],r['b'],t['a'],t['b']
  if r['region']!=t['region'] or {a.index,b.index}&{c.index,dv.index}:continue
  # Equal-length, opposite-directed boundaries of the same UV/skin surface only.
  la=(b.co-a.co).length;lb=(dv.co-c.co).length
  if min(la,lb)<.001 or abs(la-lb)/max(la,lb)>.20:continue
  if (b.co-a.co).normalized().dot((dv.co-c.co).normalized())>-.97:continue
  if r['normal'].dot(t['normal'])<.95:continue
  gaps=[(a.co-dv.co).length,(b.co-c.co).length]
  if max(gaps)>.0005 or min(gaps)<1e-6:continue
  if max((r['uv'][a]-t['uv'][dv]).length,(r['uv'][b]-t['uv'][c]).length)>.002:continue
  if max(diff(a,dv),diff(b,c))>.005:continue
  n=(a.co-b.co).cross(dv.co-b.co)
  if n.length<1e-12 or n.normalized().dot(r['normal'])<.95:continue
  n2=(dv.co-b.co).cross(c.co-b.co)
  if n2.length<1e-12 or n2.normalized().dot(r['normal'])<.95:continue
  possible.append({'edges':[r['edge'].index,t['edge'].index],'region':r['region'],'triangles':[[b.index,a.index,dv.index],[b.index,dv.index,c.index]],'uvs':[[list(r['uv'][b]),list(r['uv'][a]),list(t['uv'][dv])],[list(r['uv'][b]),list(t['uv'][dv]),list(t['uv'][c])]],'gap_m':gaps,'normal':list(r['normal'])})
possible.sort(key=lambda p:max(p['gap_m']));used=set();accepted=[]
for p in possible:
 if any(e in used for e in p['edges']):continue
 used.update(p['edges']);accepted.append(p)
(B/'Review/MeshyBaseV2/SeamCandidates.json').write_text(json.dumps({'criteria':'Forearm/cape only; gap <=0.5mm, opposing boundaries, surface normal dot>=0.95, UV continuity <=0.002, weights maxdiff<=0.005; candidate only until visual/crossing validation','possible':len(possible),'accepted_candidates':accepted},indent=2));print('Examined',len(rows),'eligible boundaries;',len(possible),'possible;',len(accepted),'non-conflicting candidates');bm.free()
