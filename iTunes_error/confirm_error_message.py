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


def write_cfg(data):
    with open('iTunes_error_cfg/iTunes_error_cfg.json', 'w') as cfg:
        json.dump(data, cfg)
        logger.info(f"{State} - {cfg_name} was created")


def read_cfg(path):
    """
    Reads in a json file from the given path and returns a dictionary
    @param path: path of the json file
    @return: content of the json file as dictionary
    """
    if os.path.splitext(path)[-1] == '.json':
        with open(path, 'r') as cfg:
            logger.info(f"{State} - {cfg_name} was read ")
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
        playlist_data = {}
        for folder_name, sub_folders, file_names in os.walk(path):
            for file_name in file_names:
                name, extension = os.path.splitext(os.path.join(path, folder_name,  file_name))
                #sort out ".DS_Store
                if os.path.split(name)[-1] != ".DS_Store":
                    lib_data.setdefault(extension.lower(), 0)
                    lib_data[extension.lower()] += 1
                    if extension == ".m3u":
                        playlist_data.setdefault(file_name, 0.0)
                        playlist_data[file_name] = get_last_mod(path=os.path.join(path, folder_name,  file_name), type='float')
        logger.info(f"{State} - files in {path} were analyzed")
        return (lib_data, playlist_data)
    else:
        logger.warning(f"{State} - {path} is not a directory")


def check_4_lib_update(json_path, lib_path):
    """
    Compares the counted extension from the json script and the current music library, if any files were added or removed
    @param json_path: path of the json file
    @param lib_path:  path of the music library
    @return: False --> no update required; True --> update required
    """
    if (os.path.splitext(json_path)[-1] == '.json') and (os.path.isdir(lib_path) is True):
        new_lib_data, new_playlist_data = count_files(lib_path)
        old_lib_data, old_playlist_data = read_cfg(json_path)
        #Checking for changed amount of files
        for key in new_lib_data.keys():
            if key in old_lib_data.keys():
                if new_lib_data[key] != old_lib_data[key]:
                    logger.info(f"{State} - {key} new:{new_lib_data[key]} old: {old_lib_data[key]}")
                    return True
            else:
                logger.info(f"{State} - missing in old keys: {key}")
                return True
        #Checking for modified playlists
        for key in new_playlist_data.keys():
            #print(key, new_playlist_data[key])
            if key in old_playlist_data.keys():
                if new_playlist_data[key] > old_playlist_data[key]:
                    logger.info(f"{State} - {key} new:{new_playlist_data[key]} old: {old_playlist_data[key]}")
                    return True
        logger.info(f"{State} - no update necessary")
        return False
    else:
        logger.warning(f"{State} - invalid file paths")
        return None


def get_last_mod(path, type='float'):
    '''
    Function to get the last modification data of the given file path as string in the format %Y-%m-%d %H:%M:%S or as float in seconds
    @param path: filepath
    @param type: float = seconds as float value; string = timestamp as string
    @return:
    '''
    if os.path.isfile(path) is True:
        # Get file's Last modification time stamp only in terms of seconds since epoch
        last_mod_in_sec = os.path.getmtime(path)
        if type == 'float':
            return last_mod_in_sec
        else:
            # Convert seconds since epoch to readable timestamp
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_mod_in_sec))


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
            cfg_name = 'iTunes_error_cfg.json'
            json_path = os.path.join('iTunes_error_cfg', cfg_name)

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
            if (os.path.isfile(json_path)) and (os.path.split(json_path)[-1] == cfg_name): #check if json file is already there, if not create on and update lib
                if check_4_lib_update(json_path, lib_path) is True:
                    State = State.UPDATE_LIBRARY
                else:
                    State = State.CHECK_TIME
            else:
                write_cfg((count_files(lib_path)))
                State = State.UPDATE_LIBRARY

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
            State = State.CHECK_TIME #Restart iTunes after lib update to enable private share

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


