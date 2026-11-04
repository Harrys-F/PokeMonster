"""Repeat three identical room-only CSV windows after the final visual connector."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();source=R/'Tools/WestlandVisualV2IntegrationV1/CaptureBenchmark.py';s=source.read_text();needle='cases=[(rep,s)for rep in range(3)for s in sites]';assert needle in s;s=s.replace(needle,"cases=[(rep,s)for rep in range(3)for s in sites if s[0]=='Heilhaus']");exec(compile(s,str(source),'exec'),{'__name__':'__main__'})
