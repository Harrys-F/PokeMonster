"""Select complete replacement configurations; retain rejected raw measurements."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2'
def resolve(data):
 required=['RepairPIEQHD','RepairNative1','RepairNative2','RepairNativeHighDorf']
 if not all((O/(n+'_Done.txt')).exists() for n in required):return data
 out={label:[dict(r,origin_label=label,origin_segment=r['segment']) for r in rows] for label,rows in data.items()}
 out['FinalPairedPIE']=[r for r in out['FinalPairedPIE'] if r['extent'][0][0]==1280]+out['RepairPIEQHD']
 out['StandalonePair1']=out['RepairNative1'];out['StandalonePair2']=out['RepairNative2'];out['StandalonePair6']=[r for r in out['StandalonePair6'] if r['site']!='Dorf']+out['RepairNativeHighDorf']
 selection={'reason':'Reject foreground loss or changing window extent; replace the whole affected site/configuration, not individual favourable frames. No raw files removed.','excluded':[{'label':'FinalPairedPIE','filter':'all QHD rows, 72 segments'},{'label':'StandalonePair1','filter':'all 18 segments'},{'label':'StandalonePair2','filter':'all 18 segments'},{'label':'StandalonePair6','filter':'all 6 Dorf segments'}],'replacement_labels':required,'standard_PIE_retained':36,'required_active_window_fraction':1.0,'required_stable_window_extent':True}
 (O/'MeasurementSelection.json').write_text(json.dumps(selection,indent=2));(O/'MeasurementsResolved.json').write_text(json.dumps(out,indent=2));return out
