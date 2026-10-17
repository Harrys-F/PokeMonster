import runpy,json,time
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();I=R/'Art/Characters/NPCs/IntegrationV1';out=[]
items=[('WhiteHairedWarrior','skeletal'),('ElvenArcher','skeletal'),('DwarfWarrior','skeletal'),('SilverLady','static'),('TreeBeing','static'),('ElvenScholar','static'),('Wizard','static'),('DarkArmored','static'),('CrouchedCreature','static')]
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX')
for id,kind in items:
 try:
  (I/'ImportRequest.json').write_text(json.dumps({'id':id,'kind':kind}));runpy.run_path(str(R/'Tools/MeshyNPCIntegrationV1/ImportNPCAssets.py'));out.append({'id':id,'ok':True})
 except Exception as e:out.append({'id':id,'ok':False,'error':str(e)})
 (I/'ImportBatch.json').write_text(json.dumps(out,indent=2))
unreal.SystemLibrary.execute_console_command(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
