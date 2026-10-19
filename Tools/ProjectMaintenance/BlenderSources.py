"""Read-only reopen of every tracked Blender source in a separate factory process."""
import bpy,json,subprocess,hashlib,time,traceback,argparse,sys
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');O=R/'Saved/ProjectMigration'
paths=[p for p in subprocess.check_output(['git','ls-files','-z','--','*.blend'],cwd=R).decode().split('\0') if p]
parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='*');parser.add_argument('--report',default='BlenderSources.json');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
assert Path(args.report).name==args.report
if args.only:assert set(args.only)<=set(paths);paths=args.only
rows=[];failures=[];oldroots=['/Users/harry/Developer/PokeMonster/Game/PokeMonster','/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree']
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
for i,rel in enumerate(paths):
 p=R/rel;before=digest(p)
 try:
  assert bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)=={'FINISHED'}
  missing=[];relocated=[]
  for lib in bpy.data.libraries:
   target=Path(bpy.path.abspath(lib.filepath))
   if not target.is_file():
    candidate=None
    for old in oldroots:
     if str(target).startswith(old+'/'):
      q=R/str(target)[len(old)+1:]
      if q.is_file():candidate=str(q)
    missing.append({'kind':'library','path':str(target),'new_location':candidate})
  for img in bpy.data.images:
   if not img.users or img.source!='FILE' or img.packed_file:continue
   target=Path(bpy.path.abspath(img.filepath))
   if not target.is_file():
    candidate=None
    for old in oldroots:
     if str(target).startswith(old+'/'):
      q=R/str(target)[len(old)+1:]
      if q.is_file():candidate=str(q)
    missing.append({'kind':'unpacked_image','name':img.name,'path':str(target),'new_location':candidate})
  row={'file':rel,'opened':True,'mesh_objects':sum(o.type=='MESH' for o in bpy.data.objects),'armatures':sum(o.type=='ARMATURE' for o in bpy.data.objects),'actions':len(bpy.data.actions),'file_images':sum(i.source=='FILE' and i.users>0 for i in bpy.data.images),'packed_images':sum(i.source=='FILE' and i.users>0 and bool(i.packed_file) for i in bpy.data.images),'missing_dependencies':missing,'source_unchanged':digest(p)==before}
  assert row['source_unchanged']
  if missing:failures.append(rel)
 except Exception:
  row={'file':rel,'opened':False,'error':traceback.format_exc(),'source_unchanged':digest(p)==before};failures.append(rel)
 rows.append(row);(O/args.report).write_text(json.dumps({'total':len(paths),'checked':len(rows),'failures':failures,'files':rows},indent=2))
 print('SOURCE_REOPEN',i+1,'/',len(paths),rel,'PASS' if row.get('opened') and not row.get('missing_dependencies') else 'REVIEW_REQUIRED',flush=True)
print('BLENDER_SOURCE_REOPEN_COMPLETE',len(rows),'review required',len(failures),flush=True)
if failures:raise RuntimeError('Blender source dependencies require review: '+str(failures))
