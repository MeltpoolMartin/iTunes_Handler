import json
import os
import time


def write_cfg(lib_data={}, playlist_data={}):
    with open('iTunes_error_cfg/iTunes_error_cfg.json', 'w') as cfg:
        json.dump(lib_data, cfg)
        json.dump(playlist_data, cfg) #JSON conflict


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
                        playlist_data.setdefault(file_name, '')
                        playlist_data[file_name] = get_last_mod(path=os.path.join(path, folder_name,  file_name), type='string')
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


def get_last_mod(path, type='integer'):
    '''
    Function to get the last modification data of the given file path as string in the format %Y-%m-%d %H:%M:%S or as integer in seconds
    @param path: filepath
    @param type: integer = seconds as integer value; string = timestamp as string
    @return:
    '''
    if os.path.isfile(path) is True:
        # Get file's Last modification time stamp only in terms of seconds since epoch
        last_mod_in_sec = os.path.getmtime(path)
        if type == 'integer':
            return last_mod_in_sec
        else:
            # Convert seconds since epoch to readable timestamp
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_mod_in_sec))



data = {'.plist': 1, '.jpg': 1072, '.ini': 176, '.mp3': 5991, '.db': 58, '.nfo': 7, '.m4a': 4, '.rar': 2, '.r00': 1, '.tmp': 1, '.txt': 4, '.png': 1, '.pdf': 2, '.p4u': 1, '.cld': 2, '.m3u': 37, '.sfv': 6, '.url': 4, '.jpeg': 1, '.zip': 1, '.strings': 39}
path= 'iTunes_error_cfg/iTunes_error_cfg.json'
lib_data, playlist_data = count_files('/Volumes/music')
write_cfg(lib_data, playlist_data)
#data = read_cfg('/Users/Martin/GitKraken/iTunes_error/iTunes_error/')
#print(check_4_lib_update(json_path='iTunes_error_cfg/iTunes_error_cfg.json', lib_path='/Volumes/music'))
# if os.path.isfile(path):
#     file_name = os.path.split(path)[-1]
#     if (os.path.splitext(file_name)[0] == 'iTunes_error_cfg') and (os.path.splitext(file_name)[1] == '.json'):
#         print('the right file')
