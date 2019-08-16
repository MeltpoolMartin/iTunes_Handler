import psutil

def check_if_proc_is_running(process_name):
    '''
        Check if there is any running process
        that contains the given name process_name.
    '''
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
