from pathlib import Path
import json,subprocess,sys
from Control import R,O,job
config=json.loads((R/'Art/World/VisualV2ShadowQualityV8/Variants.json').read_text());(O/'Request.json').write_text(json.dumps({'label':'FinalMedium','config':[2560,1440,1,100]}));job('Preset.py');job('StartPIE.py')
for variant in ['A','B','C']:
 c=config[variant];subprocess.run([sys.executable,str(Path(__file__).with_name('RunReview.py')),variant,'PIE_'+variant,str(c['gain']),'0'],check=True)
job('StopPIE.py');job('CaptureProtectedLighting.py');job('ValidateOriginal.py');print('FINAL PIE A/B/C COMPLETE; ORIGINAL PRESERVED',flush=True)
