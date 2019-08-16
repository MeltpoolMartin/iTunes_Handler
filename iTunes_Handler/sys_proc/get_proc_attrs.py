import psutil

def get_proc_attrs(process_name):
    '''
        returns the process attributes as dictionary
        of the given name process_name.
    '''
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                return pinfo
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None
