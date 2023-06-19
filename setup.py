
import tkinter
import sys
from cx_Freeze import setup, Executable
import os
import json
import webbrowser

from datetime import datetime

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"], 
    "includes": ["tkinter"],
    "include_files": [
        "tempData.json",
    ]
}
target = Executable(
    script="main.py",
    base='Win32GUI',
    icon="app.ico",
)

base = "Win32GUI"

setup(  name = "Sistema de Calculo de Planilha | Corro Variedades",
        version = "1.0",
        description = "Corro Variedades",
        autthor="Aldenir Luiz",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
