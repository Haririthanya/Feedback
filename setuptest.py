import cx_Freeze
import sys
import matplotlib

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("Feedbackpy.py",base=base,icon="icon.ico")]

cx_Freeze.setup(
    name = "Performance Analysis",
    options = {"build_exe":{"packages":["tkinter","matplotlib"],"include_files":["icon.ico"]}},
    version = "0.1",
    description = "Faculty Performance Analysis",
    executables = executables
    )
