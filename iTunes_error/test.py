import json
import os
import time


def write_cfg(data):
    with open('iTunes_error_cfg/iTunes_error_cfg.json', 'w') as cfg:
        json.dump(data, cfg)



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
        return (lib_data, playlist_data)
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
        new_lib_data, new_playlist_data = count_files(lib_path)
        old_lib_data, old_playlist_data = read_cfg(json_path)
        #Checking for changed amount of files
        for key in new_lib_data.keys():
            if key in old_lib_data.keys():
                if new_lib_data[key] != old_lib_data[key]:
                    print(f'{key} new:{new_lib_data[key]} old: {old_lib_data[key]}')
                    return True
            else:
                print(f'missing in old keys: {key}')
                return True
        #Checking for modified playlists
        for key in new_playlist_data.keys():
            #print(key, new_playlist_data[key])
            if key in old_playlist_data.keys():
                if new_playlist_data[key] > old_playlist_data[key]:
                    print(f'{key} new:{new_playlist_data[key]} old: {old_playlist_data[key]}')
                    return True
        return False
    else:
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




#path= 'iTunes_error_cfg/iTunes_error_cfg.json'
#data = count_files('/Volumes/music')
#write_cfg(data)
#lib = read_cfg('iTunes_error_cfg/iTunes_error_cfg.json')
#print(check_4_lib_update(json_path='iTunes_error_cfg/iTunes_error_cfg.json', lib_path='/Volumes/music'))

json_path='iTunes_error_cfg/iTunes_error_cfg.json'
lib_path='/Volumes/music'

if (os.path.isfile(json_path)) and (os.path.split(json_path)[-1] == 'iTunes_error_cfg.json'):  # check if json file is already there, if not create on and update lib
    if check_4_lib_update(json_path, lib_path) is True:
        print('Update Lib')
    else:
        print('Check Time')
else:
    write_cfg((count_files(lib_path)))
    print('Update Lib2')
