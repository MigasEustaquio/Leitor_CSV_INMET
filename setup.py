import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Leitor_CSV_INMET",
    version="1.0.0",
    description="Ferramenta computacional desenvolvida para apuração de dados meteorológicos, com finalidade de promover métricas auxiliares em projetos  fotovoltaicos",
    options={"build_exe": build_exe_options},
    executables=[Executable("Leitor_CSV_INMET.py", base=base)],
)