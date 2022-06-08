from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["requests","clint"],  "excludes": ["tkinter", "test", "distutils"]}

setup(
    name="PySN",
    version="0.1",
    description="PySN Title Update Utility",
    options={"build_exe": build_exe_options},
    executables=[Executable("PySN.py")],
)