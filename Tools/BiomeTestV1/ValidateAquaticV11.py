"""Reuse the existing read-only seven-clip Blender/FBX validator for the new aquatic rigs."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
code=(R/'Tools/GlutexoEvolutionV2/ValidateSource.py').read_text().replace("'Saved/GlutexoEvolutionV2'","'Saved/BiomeTestV11'")
exec(compile(code,'ExistingSevenClipValidator','exec'))
