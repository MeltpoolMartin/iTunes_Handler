import sys
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["sys_proc.get_proc_attrs", "sys_proc.check_if_proc_is_running",
                                  "logging.handlers", "subprocess", "os", "time", "pyautogui", "enum"],
                     "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Console"

setup(  name = "iTunes_Handler",
        version = "0.1",
        description = "iTunes_Handler to manage execution time of iTunes in VM",
        options = {"build_exe": build_exe_options},
        executables = [Executable("confirm_error_message.py", base=base)])