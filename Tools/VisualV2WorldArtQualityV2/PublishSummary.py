"""Publish compact measured numbers and provenance only; never copy screenshots/videos/raw frames into Git."""
from pathlib import Path
import hashlib,json,shutil,csv,collections
from Aggregate import aggregate
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtQualityV2';D=R/'Docs/Data/VisualV2WorldArtQualityV2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=aggregate();assert len(a['runs'])==8 and sum(r['segments'] for r in a['runs'].values())==396
D.mkdir(parents=True,exist_ok=False);shutil.copy2(S/'Aggregate.csv',D/'Messwerte.csv');runproof={}
for label,meta in a['runs'].items():
 f=R/'Saved/EnvironmentPerfV2'/(label+'_Frames.csv');proof=S/(label+'_VariantProof.json');rows=json.loads(proof.read_text());assert len(rows)==meta['segments']
 assert all(r['original_instance_count']==175 for r in rows) if '_Cost_' in label else all(r['instances']==175 and r['pp_and_light_settings_unchanged'] for r in rows)
 runproof[label]={**meta,'frame_csv_sha256':sha(f),'variant_proof_sha256':sha(proof),'plan':str((R/'Tools/VisualV2WorldArtQualityV2/Plans'/(label+'.tsv')).relative_to(R))}
thermal=[json.loads(r) for r in (S/'Thermal.jsonl').read_text().splitlines() if r];counts=collections.Counter(r['thermal_label'] for r in thermal)
(D/'Messmethode.json').write_text(json.dumps({'source_commit':'371190e69776d906288e9772c7fdfcb0d635f4b1','method':a['method'],'series':runproof,'counter_gaps':a['counter_gaps'],'hardware':json.loads((S/'Hardware.json').read_text()),'thermal_samples':len(thermal),'thermal_states':dict(counts),'thermal_period_utc':[thermal[0]['utc'],thermal[-1]['utc']],'known_counter_limitations':['All-zero DrawCall/RHI counters are unavailable, not zero real draws.','Three-second final measurement windows; no long-run FPS guarantee.','Separate CPU thread times include waits; not additive to GPU time.'],'normal_gameplay_cvars_unchanged':True},indent=2))
print('Published compact measured CSV and provenance; raw media remain local.')
