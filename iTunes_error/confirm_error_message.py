import sys_proc.check_if_proc_is_running as check_if_proc_is_running
import time


if __name__ == '__main__':

    #define inital conditions
    proc_name = 'excel'
    proc_found = 'false'

    #wait unitl proc_name was started
    while proc_found != True:
        time.sleep(1) #wait for 1 second until checking for process
        proc_found = check_if_proc_is_running.check_if_proc_is_running(proc_name)
    print(f'{proc_name} was started')

else:
    print(f'{__name__} is not run as main')

