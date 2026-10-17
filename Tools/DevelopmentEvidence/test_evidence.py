"""Meaningful safety tests: mandatory sources must fail; optional evidence may skip."""
from pathlib import Path
import contextlib,hashlib,io,json,os,tempfile,unittest
from unittest.mock import patch
import evidence

class EvidenceSafety(unittest.TestCase):
    def test_required_missing_fails(self):
        with tempfile.TemporaryDirectory() as d:
            r=evidence.validate_core(Path(d),{'Required.txt':{'bytes':1,'sha256':'0'*64}})
            self.assertFalse(r['passed']);self.assertEqual(r['missing_required'],['Required.txt'])
    def test_required_corrupt_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'Required.txt';p.write_bytes(b'b')
            r=evidence.validate_core(Path(d),{'Required.txt':{'bytes':1,'sha256':hashlib.sha256(b'a').hexdigest()}})
            self.assertFalse(r['passed']);self.assertEqual(r['changed_required'],['Required.txt'])
    def test_valid_required_passes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'Required.txt';p.write_bytes(b'a')
            self.assertTrue(evidence.validate_core(Path(d),{'Required.txt':{'bytes':1,'sha256':hashlib.sha256(b'a').hexdigest()}})['passed'])
    def test_unknown_source_is_not_optional(self):
        with self.assertRaises(KeyError):evidence.resolve_optional('Source/PokeMonster/PokeMonster.cpp')
    def test_path_escape_rejected(self):
        for path in ['../Source.cpp','/tmp/image.png','Art/../../escape','Art\\escape']:
            with self.assertRaises(ValueError):evidence.safe_name(path)
    def test_missing_optional_is_explicit(self):
        tool=next(iter(json.loads((evidence.HERE/'ReviewPolicies.json').read_text())))
        with patch.dict(os.environ,{'POKEMONSTER_REQUIRE_EVIDENCE':'1'}),contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as e:evidence.review_preflight(evidence.ROOT/tool)
            self.assertEqual(e.exception.code,2)
            self.assertIn('REVIEW_NOT_EXECUTED',output.getvalue());self.assertIn('NOT a test pass',output.getvalue())
    def test_corrupt_archive_rejected(self):
        name,item=next(iter(evidence.manifest().items()))
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/item['archive_object'];p.parent.mkdir(parents=True);p.write_bytes(b'bad')
            with self.assertRaises(ValueError):evidence.resolve_optional(name,d)
    def test_no_archive_does_not_read_original_worktree(self):
        name=next(iter(evidence.manifest()))
        with patch.dict(os.environ,{'POKEMONSTER_EVIDENCE_ARCHIVE':''}):self.assertIsNone(evidence.resolve_optional(name))

if __name__=='__main__':unittest.main()
