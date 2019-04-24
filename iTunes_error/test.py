import sys_proc.check_if_proc_is_running
import sys_proc.get_proc_attrs

name = "excel"
print(sys_proc.check_if_proc_is_running.check_if_proc_is_running(name))
print(sys_proc.get_proc_attrs.get_proc_attrs(name))
