"""Reuse existing strict packed-source/UV/weight/FBX roundtrip validation, including Habitak's extra flight clips."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
code=(R/'Tools/GlutexoEvolutionV2/ValidateSource.py').read_text()
code=code.replace("O=R/'Saved/GlutexoEvolutionV2'/label","O=R/'Saved/BiomeTestV11'/label")
code=code.replace('assert len(bpy.data.actions)==7','assert len(bpy.data.actions)==len(a["clips"])')
code=code.replace("for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:","for role in a['clips']:")
exec(compile(code,'ExistingPackedSourceRoundtripValidation','exec'))
