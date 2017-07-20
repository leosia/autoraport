import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning. 'atexit',
build_exe_options = {"includes": ['atexit', 'video'],
                     "include_files": ['auto.kv',
                                       'logo.png',
                                       'logo2.png',
                                       'video.py'],
                     "packages": ["kivy",
                                  "getpass",
                                  "shutil",
                                  "kivy.deps.sdl2",
                                  "kivy.deps.glew",
                                  "cv2",
                                  "re",
                                  "datetime",
                                  "reportlab"],
                     "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r'C:\Users\mateusz.sobek\AppData\Local\Continuum\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\mateusz.sobek\AppData\Local\Continuum\Anaconda3\tcl\tk8.6'

executables = [
    Executable('main.py', base=base, targetName="Autoliv_AFR.exe", icon='logo3.ico')
]

setup(  name = "afrgui",
        version = "0.1",
        description = "Autoliv Automatic Fiat Reports GUI",
        options = {"build_exe": build_exe_options},
        executables = executables
        )
