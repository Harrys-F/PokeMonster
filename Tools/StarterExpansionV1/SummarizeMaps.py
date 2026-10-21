"""Parse the actual English/German Map Check summaries; absence never means success."""
from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parents[2];log=(R/sys.argv[1]).resolve();out=(R/sys.argv[2]).resolve();assert log.is_relative_to(R/'Saved')and out.is_relative_to(R/'Saved')and not out.exists();blocks=re.findall(r'STARTER_EXPANSION_FINAL_MAPCHECK_BEGIN ([^\r\n]+)(.*?)STARTER_EXPANSION_FINAL_MAPCHECK_END',log.read_text(),re.S);rows=[]
for name,body in blocks:
 matches=re.findall(r'(\d+) Fehler, (\d+) Warnung\(en\)',body)or re.findall(r'(\d+) Error\(s\), (\d+) Warning\(s\)',body);assert len(matches)==1,(name,matches);errors,warnings=map(int,matches[0]);rows.append({'map':name.strip(),'errors':errors,'warnings':warnings})
assert len(rows)==len(list((R/'Content/Maps').glob('*.umap')));result={'log':str(log.relative_to(R)),'rows':rows,'passed':all(x['errors']==0 and x['warnings']==0 for x in rows)};out.write_text(json.dumps(result,indent=2));assert result['passed'];print('ALL_EXISTING_MAPS_PASS',len(rows))
