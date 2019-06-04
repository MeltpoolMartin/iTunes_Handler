import sys_proc.get_proc_attrs as get_proc_attrs
import sys_proc.check_if_proc_is_running as check_if_proc_is_running
import logging
import logging.handlers
import subprocess
import os
import time
import pyautogui as gui
from enum import Enum


class State(Enum):

    INIT = 1
    LAUNCH_PROCESS = 2
    FIND_PROCESS = 3
    CHECK_TIME = 4
    KILL_PROCESS = 5
    SHUTDOWN = 6
    STOP = 7

if __name__ == '__main__':

    State = State.INIT
    while State != State.STOP:

        if State == State.INIT:

            #Initialize Logger
            logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO,
                               format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            #logging.basicConfig(level=logging.INFO, filename='iTunes_error.log',
            #                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            #handler = logging.handlers.RotatingFileHandler('iTunes_error.log', maxBytes=10000)  # adding handler for rotating log files
            #logger.addHandler(handler)

            #Initialize LAUNCH PROCESS
            #app_name = 'calc.exe'
            app_name = 'iTunes'

            #define inital conditions
            hh, mm, ss = 23, 55, 0 # timestamp to initialize termination of the application
            proc_name = app_name #'iTunes'  # name of the application to search for
            proc_found = 'false'
            counter = 0
            logger.info("%s - Initialization finished", State)
            logger.info(f"{State} - App Name = {app_name}")
            logger.info(f"{State} - Termination Time = {hh}:{mm}:{ss}")
            State = State.LAUNCH_PROCESS

        if State == State.LAUNCH_PROCESS:

            try:
                # subprocess.Popen(['open', '-a', app_name], cwd='/Applications',
                #                  stdout=subprocess.PIPE)  # open /Applications/Calculator.app
                #proc = subprocess.Popen([app_name], cwd="C:\Program Files\iTunes",
                #                                   stdout=subprocess.PIPE)
                proc = subprocess.Popen(["C:\Program Files\iTunes\iTunes.exe"], stdout=subprocess.PIPE)
                logger.info(f"{State} - {proc_name} was started")
            except ValueError as err:
                logger.info(f"{State} - {proc_name} could not be started")

            State = State.FIND_PROCESS

        if State == State.FIND_PROCESS:

            #wait unitl proc_name was started or timeout
            proc_info = get_proc_attrs.get_proc_attrs(proc_name)
            proc_found = check_if_proc_is_running.check_if_proc_is_running(proc_name)

            if proc_found == True:
                logger.info(f"{State} - {proc_name} was started")
                logger.info('%s - %s', State, proc_info)
                time.sleep(5)
                gui.press('enter') # enter key confirms the error message
                logger.info("%s - Enter key was pressed", State)
                State = State.CHECK_TIME

            time.sleep(1)  # wait for 1 second until checking for process
            counter += 1

            if counter == 10:
                logger.warning('%s - Timeout after 10 sec', State)
                break

        if State == State.CHECK_TIME:

            while True:
                hour, minute, second = time.localtime()[3:6] # get current hour, min and sec
                print('\r', f'{hour}:{minute}:{second}', end="")
                time.sleep(1)  # wait for 1 sec to slow down loop
                if hour >= hh and minute >= mm and second >= ss:
                    logger.info(f'{State} - Shutdown time reached')
                    State = State.KILL_PROCESS
                    break

        if State == State.KILL_PROCESS:

            try:
                proc.kill() #kill process by name Windows
                logger.info(f"{State} - {proc_name} was terminated")
            except ValueError as err:
                logger.info(f"{State} - {proc_name} could not be terminated")
            time.sleep(10) # wait until shutting down OS
            State = State.SHUTDOWN

        if State == State.SHUTDOWN:

            logger.info(f'{State} - Operating system will be shut down')
            os.system('shutdown /p /f') #for Windows
            #os.system("shutdown /s /t 1") #for MAC
            State = State.STOP

else:
    print(f'{__name__} is not run as main')


