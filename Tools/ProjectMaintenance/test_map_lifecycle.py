"""Safety tests for deliberate retirement: missing historical maps fail explicitly; required fixtures stay strict."""
from pathlib import Path
import unittest,tempfile,contextlib,io,json,hashlib
import MapLifecycle as m
class MapLifecycleSafety(unittest.TestCase):
 def test_missing_historical_map_is_not_a_pass(self):
  with tempfile.TemporaryDirectory() as d:
   spec={'tools':{'Tool.py':['/Game/Maps/Old']},'retired_maps':{'/Game/Maps/Old':{'file':'Content/Maps/Old.umap'}},'restore_commit':'abc'}
   with contextlib.redirect_stderr(io.StringIO()) as log, self.assertRaises(SystemExit) as err:m.require_historical_maps(Path(d)/'Tool.py',Path(d),spec)
   self.assertEqual(err.exception.code,2);self.assertIn('NOT a test pass',log.getvalue())
 def test_unrelated_current_tool_is_not_blocked(self):
  with tempfile.TemporaryDirectory() as d:m.require_historical_maps(Path(d)/'Other.py',Path(d),{'tools':{}})
 def test_snapshot_has_expected_provenance(self):
  v=m.npc_baseline();self.assertGreater(len(v['actors']),1300);self.assertEqual(v['map'],'/Game/Maps/Dev_TestMap_NPCMotionV2.Dev_TestMap_NPCMotionV2')
 def test_changed_actor_changes_signature(self):
  self.assertNotEqual(m.actor_digest({'collision':'QueryOnly'}),m.actor_digest({'collision':'NoCollision'}))
 def test_corrupt_required_baseline_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.json';p.write_text('{}')
   with self.assertRaises(ValueError):m.npc_baseline(Path(d),{'frozen_npc_baseline':{'file':'bad.json','sha256':'0'*64}})
if __name__=='__main__':unittest.main()
