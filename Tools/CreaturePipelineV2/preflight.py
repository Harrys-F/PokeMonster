"""Read-only Meshy intake/scale plan. Does not import, replace, retarget or save assets."""
from pathlib import Path
import argparse,hashlib,json,math,re
ROOT=Path(__file__).resolve().parents[2]
RIGS={'custom','biped','quadruped','serpentine','winged','aquatic','floating'}
CLIPS={'Idle','Walk','Run','Attack','Hit','Faint','Happy'}
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def local_path(root,value):
 if not isinstance(value,str) or not value:raise ValueError('Missing project-relative source path')
 p=(root/value).resolve()
 if Path(value).is_absolute() or not p.is_relative_to(root.resolve()):raise ValueError('Source must stay inside active project')
 return p

def scale_factor(reference_cm,measured_m):
 if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and x>0 for x in [reference_cm,measured_m]):raise ValueError('Scale requires finite positive reference cm and measured metres')
 return reference_cm/(100*measured_m)

def validate(plan,root=ROOT):
 errors=[];warnings=[];ratio=None
 def require(ok,message):
  if not ok:errors.append(message)
 require(plan.get('schema')==1,'Unknown schema')
 require(plan.get('rig_family') in RIGS,'Explicit rig family required; never infer from filename')
 n=plan.get('national_number');require(type(n) is int and 1<=n<=251,'National number must be 1..251; independent of existing prototype numbers')
 require(bool(re.fullmatch(r'/Game/Data/Creatures/[A-Za-z0-9_]+',str(plan.get('species_asset','')))),'Existing species asset path required')
 require(bool(re.fullmatch(r'CreatureSpecies:[A-Za-z0-9_]+',str(plan.get('expected_primary_asset_id','')))),'Stable species identity required')
 species=plan.get('species_asset','').replace('/Game/','Content/',1)+'.uasset'
 if re.fullmatch(r'Content/Data/Creatures/[A-Za-z0-9_]+\.uasset',species):require((root/species).is_file(),'Species asset not found; no new gameplay species is created by this tool')
 ns=plan.get('destination_namespace','');require(bool(re.fullmatch(r'/Game/Characters/Creatures/[A-Za-z0-9_]+/[A-Za-z0-9_]+',ns)),'Dedicated candidate namespace required; existing V1 is not a destination')
 for key in ['mesh_asset','presentation_asset']:
  value=plan.get(key,'');require(isinstance(value,str) and value.startswith(ns+'/') and bool(re.fullmatch(r'/Game/[A-Za-z0-9_/]+',value)),key+' must be in candidate namespace')
  if isinstance(value,str) and value.startswith('/Game/'):require(not (root/(value.replace('/Game/','Content/',1)+'.uasset')).exists(),key+' already exists; never overwrite')
 clips=plan.get('clip_exports',{});require(isinstance(clips,dict) and set(clips)==CLIPS,'Seven explicit clip exports required for full integration')
 require(plan.get('blender_forward')=='-Y' and plan.get('blender_up')=='Z','Blender authoring convention is -Y forward, +Z up')
 size=plan.get('size',{});require(size.get('basis') in ['standing_height','body_length'],'Size basis must be standing_height or body_length')
 require(isinstance(size.get('source_url'),str) and size['source_url'].startswith('https://'),'Original size needs a cited source URL')
 try:scale_factor(size.get('reference_cm'),1)
 except ValueError as e:errors.append(str(e))
 try:
  original=local_path(root,plan.get('original_glb'));require(original.suffix.lower()=='.glb' and original.is_file(),'Original Meshy GLB not yet supplied')
  if original.is_file():require(digest(original)==plan.get('original_glb_sha256'),'Original GLB SHA-256 missing or different')
 except ValueError as e:errors.append(str(e))
 source=None
 try:
  source=local_path(root,plan.get('source_model'));require(source.suffix.lower()=='.blend' and source.is_file(),'Prepared Blender source not yet supplied')
  if source.is_file():require(digest(source)==plan.get('source_sha256'),'Source SHA-256 missing or different')
 except ValueError as e:errors.append(str(e))
 try:
  auditpath=local_path(root,plan.get('blender_audit'));require(auditpath.is_file(),'Blender inspection required')
  if auditpath.is_file():
   audit=json.loads(auditpath.read_text());require(audit.get('source_sha256')==plan.get('source_sha256'),'Audit belongs to a different source')
   require(audit.get('forward_confirmed_by_human') is True,'Front/profile direction requires visual confirmation')
   require(audit.get('size_basis')==size.get('basis'),'Audit measurement basis differs from reference basis')
   ratio=scale_factor(size.get('reference_cm'),audit.get('measured_size_m'))
 except (ValueError,OSError,json.JSONDecodeError) as e:errors.append(str(e))
 if isinstance(clips,dict):
  for role,value in clips.items():
   try:
    if not isinstance(value,dict):raise ValueError('Clip needs path and SHA-256')
    path=local_path(root,value.get('path'));require(path.suffix.lower()=='.fbx' and path.is_file(),'Missing FBX clip '+role)
    if path.is_file():require(digest(path)==value.get('sha256'),'FBX SHA-256 differs for '+role)
   except ValueError as e:errors.append(role+': '+str(e))
 require(plan.get('in_place_confirmed') is True,'In-place motion and actual speeds must be confirmed')
 warnings.append('Reference size is not always vertical height; do not rescale roots from an unreviewed bounding box.')
 warnings.append('Plan readiness does not certify weights, silhouette, materials or deformation quality.')
 return {'ready_for_manual_import':not errors,'errors':errors,'warnings':warnings,'proposed_uniform_authoring_scale':ratio,'writes_assets':False,'species_asset':plan.get('species_asset'),'expected_primary_asset_id':plan.get('expected_primary_asset_id')}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('manifest',type=Path);args=ap.parse_args()
 result=validate(json.loads(args.manifest.read_text()));print(json.dumps(result,indent=2,ensure_ascii=False));raise SystemExit(0 if result['ready_for_manual_import'] else 2)
