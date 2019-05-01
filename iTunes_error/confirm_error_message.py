import sys_proc.get_proc_attrs as get_proc_attrs
import sys_proc.check_if_proc_is_running as check_if_proc_is_running
import logging
import time
import pyautogui as gui


if __name__ == '__main__':

    #Initialize Logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('logs/iTunes_error.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    # yyyy-MM-dd HH:mm:ss,SSS


    #define inital conditions
    proc_name = 'excel'
    proc_found = 'false'
    counter = 0
    logger.info("Initialization finished")

    #wait unitl proc_name was started or timeout
    while proc_found != True:
        proc_info = get_proc_attrs.get_proc_attrs(proc_name)
        proc_found = check_if_proc_is_running.check_if_proc_is_running(proc_name)
        if proc_found == True:
            logger.info(f"{proc_name} was started")
            logger.info('%s', proc_info)
            time.sleep(5)
            gui.press('enter')
            logger.info("Enter key was pressed")
        time.sleep(1)  # wait for 1 second until checking for process
        counter += 1
        if counter == 10:
            logger.warning('Timeout after 10 sec')
            break
else:
    print(f'{__name__} is not run as main')

