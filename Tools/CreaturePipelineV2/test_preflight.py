"""Small synthetic file fixtures only in ignored Saved; no game/model asset generated."""
import unittest,tempfile,json,copy,sys
from pathlib import Path
sys.dont_write_bytecode=True
from preflight import validate,scale_factor,digest,ROOT,CLIPS
class PreflightTests(unittest.TestCase):
 def setUp(self):
  base=ROOT/'Saved/CreaturePipelineV2';base.mkdir(exist_ok=True);self.temp=tempfile.TemporaryDirectory(prefix='unit_',dir=base);self.r=Path(self.temp.name)
  self.source=self.r/'prepared.blend';self.source.write_bytes(b'synthetic test data, not a Blender model')
  self.glb=self.r/'original.glb';self.glb.write_bytes(b'synthetic test data, not a GLB model')
  p=self.r/'Content/Data/Creatures/DA_Zunderlauf.uasset';p.parent.mkdir(parents=True);p.write_bytes(b'fixture, not an Unreal asset')
  self.clip=self.r/'clip.fbx';self.clip.write_bytes(b'synthetic fixture, not an FBX model')
  self.audit=self.r/'audit.json';self.audit.write_text(json.dumps({'source_sha256':digest(self.source),'forward_confirmed_by_human':True,'size_basis':'standing_height','measured_size_m':1.2}))
  self.plan={'schema':1,'national_number':4,'species_asset':'/Game/Data/Creatures/DA_Zunderlauf','expected_primary_asset_id':'CreatureSpecies:Zunderlauf','rig_family':'biped','source_model':'prepared.blend','source_sha256':digest(self.source),'original_glb':'original.glb','original_glb_sha256':digest(self.glb),'blender_audit':'audit.json','destination_namespace':'/Game/Characters/Creatures/Zunderlauf/Candidate','mesh_asset':'/Game/Characters/Creatures/Zunderlauf/Candidate/Meshes/SK_New','presentation_asset':'/Game/Characters/Creatures/Zunderlauf/Candidate/DA_New','blender_forward':'-Y','blender_up':'Z','size':{'basis':'standing_height','reference_cm':60,'source_url':'https://ph.portal-pokemon.com/pokedex/0004/'},'clip_exports':{k:{'path':'clip.fbx','sha256':digest(self.clip)} for k in CLIPS},'in_place_confirmed':True}
 def tearDown(self):self.temp.cleanup()
 def test_valid_plan_scale_and_no_mutation(self):
  before={str(p):p.read_bytes() for p in self.r.rglob('*') if p.is_file()};result=validate(self.plan,self.r);self.assertTrue(result['ready_for_manual_import'],result);self.assertEqual(result['proposed_uniform_authoring_scale'],.5);self.assertEqual(before,{str(p):p.read_bytes() for p in self.r.rglob('*') if p.is_file()})
 def test_pending_model_rejected(self):
  plan=json.loads((ROOT/'Tools/CreaturePipelineV2/Glumanda_Pending.json').read_text());self.assertFalse(validate(plan,ROOT)['ready_for_manual_import'])
 def test_changed_sources_or_exports_rejected(self):
  for path in [self.source,self.glb,self.clip]:
   old=path.read_bytes();path.write_bytes(b'changed');self.assertFalse(validate(self.plan,self.r)['ready_for_manual_import']);path.write_bytes(old)
 def test_escape_and_symlink_rejected(self):
  for value in ['../outside.glb',str(self.source.resolve())]:
   p=copy.deepcopy(self.plan);p['source_model']=value;self.assertFalse(validate(p,self.r)['ready_for_manual_import'])
  link=self.r/'escape.blend';link.symlink_to(self.r.parent/'outside.blend');p=copy.deepcopy(self.plan);p['source_model']='escape.blend';self.assertFalse(validate(p,self.r)['ready_for_manual_import'])
 def test_no_existing_asset_overwrite(self):
  p=self.r/'Content/Characters/Creatures/Zunderlauf/Candidate/DA_New.uasset';p.parent.mkdir(parents=True);p.write_bytes(b'protected');self.assertFalse(validate(self.plan,self.r)['ready_for_manual_import']);self.assertEqual(p.read_bytes(),b'protected')
 def test_length_not_height(self):
  p=copy.deepcopy(self.plan);p['rig_family']='serpentine';p['size']['basis']='body_length';self.assertFalse(validate(p,self.r)['ready_for_manual_import']);a=json.loads(self.audit.read_text());a['size_basis']='body_length';self.audit.write_text(json.dumps(a));self.assertTrue(validate(p,self.r)['ready_for_manual_import'])
 def test_incomplete_clips_and_invalid_numbers(self):
  for change in [{'clip_exports':{}},{'national_number':252},{'blender_forward':'+Y'},{'in_place_confirmed':False}]:
   p=copy.deepcopy(self.plan);p.update(change);self.assertFalse(validate(p,self.r)['ready_for_manual_import'])
 def test_invalid_numeric_sizes(self):
  for v in [0,-1,float('nan'),float('inf'),None,True]:
   with self.assertRaises(ValueError):scale_factor(v,1)
if __name__=='__main__':unittest.main()
