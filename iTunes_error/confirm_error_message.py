import sys_proc.get_proc_attrs as get_proc_attrs
import sys_proc.check_if_proc_is_running as check_if_proc_is_running
import logging
import json
import logging.handlers
import subprocess
import os
import time
import pyautogui as gui
from enum import Enum


def write_cfg(lib_data={}):
    with open('iTunes_error_cfg/iTunes_error_cfg.json', 'w') as cfg:
        json.dump(lib_data, cfg)


def read_cfg(path):
    """
    Reads in a json file from the given path and returns a dictionary
    @param path: path of the json file
    @return: content of the json file as dictionary
    """
    if os.path.splitext(path)[-1] == '.json':
        with open(path, 'r') as cfg:
            return json.load(cfg)
    else:
        return None


def count_files(path):
    """
    count_files considers every file in the given path and counts it to a dict
    @param path:path, which will be analyzed for changes/modifications
    @return:dictionary with the count result
    """

    if os.path.isdir(path) is True:
        lib_data = {}
        for folder_name, sub_folders, file_names in os.walk(path):
            for file_name in file_names:
                name, extension = os.path.splitext(os.path.join(path, folder_name,  file_name))
                #sort out ".DS_Store
                if os.path.split(name)[-1] != ".DS_Store":
                    lib_data.setdefault(extension.lower(), 0)
                    lib_data[extension.lower()] += 1
        return lib_data
    else:
        print('Given path should only be a directory')


def check_4_lib_update(json_path, lib_path):
    """
    Compares the counted extension from the json script and the current music library, if any files were added or removed
    @param json_path: path of the json file
    @param lib_path:  path of the music library
    @return: False --> no update required; True --> update required
    """
    if (os.path.splitext(json_path)[-1] == '.json') and (os.path.isdir(lib_path) is True):
        new_lib_data = count_files(lib_path)
        old_lib_data = read_cfg(json_path)
        for key in new_lib_data.keys():
            if key in old_lib_data.keys():
                if new_lib_data[key] != old_lib_data[key]:
                    print(f'{key} new:{new_lib_data[key]} old: {old_lib_data[key]}')
                    return True
            else:
                print(f'missing in old keys: {key}')
                return True
        return False
    else:
        return None


class State(Enum):

    INIT = 1
    LAUNCH_PROCESS = 2
    FIND_PROCESS = 3
    CHECK_TIME = 4
    CHECK_4_UPDATE = 5
    UPDATE_LIBRARY = 6
    KILL_PROCESS = 7
    SHUTDOWN = 8
    STOP = 9


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
            app_path = 'C:\Program Files\iTunes\iTunes.exe'
            lib_path = '/Volumes/music'
            json_path = 'iTunes_error_cfg/iTunes_error_cfg.json'

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
                proc = subprocess.Popen([app_path], stdout=subprocess.PIPE)
                logger.info(f"{State} - {proc_name} was started")
            except ValueError as err:
                logger.info(f"{State} - {proc_name} could not be started")

            State = State.FIND_PROCESS

        if State == State.FIND_PROCESS:

            #wait unitl proc_name was started or timeout
            time.sleep(10)
            proc_info = get_proc_attrs.get_proc_attrs(proc_name)
            proc_found = check_if_proc_is_running.check_if_proc_is_running(proc_name)

            if proc_found == True:
                logger.info(f"{State} - {proc_name} was started")
                logger.info('%s - %s', State, proc_info)
                time.sleep(5)
                gui.press('enter') # enter key confirms the error message
                logger.info("%s - Enter key was pressed", State)
                State = State.CHECK_4_UPDATE

            time.sleep(1)  # wait for 1 second until checking for process
            counter += 1

            if counter == 10:
                logger.warning('%s - Timeout after 10 sec', State)
                break

        if State == State.CHECK_TIME:

            while True:
                hour, minute, second = time.localtime()[3:6] # get current hour, min and sec
                print('\r', f'Current Time: {hour}:{minute}:{second}', end="")
                time.sleep(1)  # wait for 1 sec to slow down loop
                if hour >= hh and minute >= mm and second >= ss:
                    logger.info(f'{State} - Shutdown time reached')
                    State = State.KILL_PROCESS
                    break

        if State == State.CHECK_4_UPDATE:
            if check_4_lib_update(json_path, lib_path) is True:
                State = State.UPDATE_LIBRARY
            else:
                State = State.CHECK_TIME

        if State == State.UPDATE_LIBRARY:
            logger.info(f"{State} - Updating iTunes library")
            time.sleep(30)
            gui.press('alt') #open menu
            time.sleep(1)
            for i in range(1, 6):
                gui.press('down')
                time.sleep(1)
            gui.press('enter')
            time.sleep(1)
            gui.press('enter')
            State = State.CHECK_TIME

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


