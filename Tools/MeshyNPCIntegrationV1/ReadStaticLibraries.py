# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
import bpy,json,sys
from pathlib import Path
R=_evidence_root;I=R/'Art/Characters/NPCs/IntegrationV1';out=[]
# No scene linking/evaluation: read each new review datablock without rebuilding its expensive unapplied modifier.
for c in json.loads((I/'Characters.json').read_text()):
 id=c['id']
 if id=='Ranger':continue
 p=R/'Art/Characters/NPCs'/id/'Source'/(id+'_NPC_StaticReview_V1.blend')
 with bpy.data.libraries.load(str(p),link=False) as (a,b):b.objects=[n for n in a.objects if 'HP_' in n or 'StaticPreview' in n or 'StaticReview' in n or 'STATIC_REVIEW' in n]
 meshes=[o for o in b.objects if o and o.type=='MESH'];assert len(meshes)==2,(id,[o.name for o in meshes]);out.append({'id':id,'file':str(p),'datablock_read_ok':True,'meshes':[{'name':o.name,'polygons':len(o.data.polygons),'modifiers':[m.type for m in o.modifiers]} for o in meshes],'verification':'Blender library read only; no full scene/modifier evaluation during this check'})
 print('LIBRARY_READ_OK',id,flush=True)
 # Release only unsaved inspection copies in this factory-startup process.
 for o in meshes:bpy.data.objects.remove(o,do_unlink=True)
 for m in list(bpy.data.meshes):
  if m.users==0:bpy.data.meshes.remove(m)
(I/'StaticLibraryRead.json').write_text(json.dumps(out,indent=2))
