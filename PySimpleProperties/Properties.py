import copy
from collections import KeysView, ValuesView
from typing import Optional
import os
import platform
from pathlib import Path


#####     STATIC METHODS     #####
def clean_path(uncleaned_path: str):
    print(f'{uncleaned_path=}')
    platformSeparator = getPlatformSeparators()
    rPath = copy.deepcopy(uncleaned_path).replace('/', '\\') #+ '\\'  #????????????
    print(f'{rPath=}')
    struct_path = rPath.split(
        '\\')  ## Just to be sure there are no problems with mutable stuff
    i = 0
    while i < len(struct_path):
        if struct_path[i] == '..':
            struct_path.pop(i)
            struct_path.pop(i)
        else:
            i += 1
    print(f'{struct_path=}\n')
    path = struct_path[0]
    if path == '':
        path = platformSeparator
    for element in struct_path[1:]:
        if element != '':
            path += platformSeparator + element
    return path


def getPlatformSeparators():
    system = platform.system()
    if system == 'Linux':
        return '/'
    elif system == 'Windows':
        return '\\'
    elif system == 'Darwin':
        raise SystemError(f'Platform {system} not supported!')


class Properties:
    content: dict
    path: str  ## self.path is absolute
    prev_key: str
    comment_char: str
    separator_char: str
    platformSeparator: str

    def __init__(self, path: str = False, **kwargs):
        """ Creates a Properties object used to manage a .properties file
        :param path: string path as relative {used with a context manager}
        :param kwargs: comment_char (default:#) and separator_char (default:=)
        """
        self.content = {}
        self.path = ''
        self.prev_key = ''
        self.separator_char = kwargs.get('separator_char', '=')
        self.comment_char = kwargs.get('comment_char', '#')
        self.platformSeparator = getPlatformSeparators()
        is_absolute: bool = kwargs.get('is_absolute', False)
        if path:
            self.load(path, self.separator_char, self.comment_char, is_absolute)

    def __repr__(self):
        return f"<{self.__class__}, loaded_file: '{self.path if self.path else 'None'}'>"

    def getPath(self) -> str:
        """Used to get the path of the file stored
        :return: str, the path of the file stored
        """
        return self.path

    def load(self, path: str, separator_char: str = '=', comment_char: str = '#',
             is_absolute: bool = False) -> 'Properties':
        """ Loads Properties and stores them in a dict and returns the dict
        :param path: string path as relative {used with a context manager}
        :param comment_char: comment_char (default:#)
        :param separator_char: separator_char (default:=)
        :return: Dict of content
        """
        print(f'Loading file: {path}')
        if not is_absolute:
            # path = str(os.getcwd()) + ('\\' if not (path.startswith('\\') or path.startswith('/')) else '') + path
            print(f'{path=}')
            print(f'{clean_path(path)=}')
            path = str(os.getcwd()) + self.platformSeparator + clean_path(path)
        print('Finalcleaning')
        path = clean_path(path)
        self.content = {}
        self.prev_key = ''
        try:
            with open(path, 'r') as f:
                strContent = f.readlines()
                for line in strContent:
                    line = line.replace('\n', '').strip()
                    if self.prev_key != '':
                        self.content[self.prev_key] += ' ' + line

                    elif line[0] != comment_char:
                        key, key_value = line.split(separator_char)
                        self.content[key] = key_value

                    if line[-1] == '\\':
                        self.prev_key = key if self.prev_key == '' else self.prev_key
                        self.content[key] = self.content[key].replace('\\', '')
                    if line[-1] != '\\' and self.prev_key != '':
                        self.prev_key = ''

                f.close()
            self.prev_key = ''
            self.path = path
            self.separator_char = separator_char
            self.comment_char = comment_char
        except FileNotFoundError as e:
            print(e)
        return self

    def reload(self):
        """Reloads the property file"""
        if not self.path:
            return print("No path given, cannot reload properties. Skipping...")
        self.load(self.path, self.separator_char, self.comment_char, is_absolute=True)

    def getProperty(self, key: str) -> str:
        """Returns the key
        :param key: str, key of dict
        :return: value of key, Undefined if not found
        """
        return self.content.get(key, 'Undefined')

    def replaceProperty(self, key: str, val: str, create_if_needed: bool = False):
        """Used to change the value of an existing property
        :param key: str, key to change value from
        :param val: str, new value
        :param create_if_needed: bool, if True will create property if it doesn't exist
        :return:
        """
        if self.containsProperty(key) or create_if_needed:
            self.content[key] = val
        else:
            print(f"Undefined property {key}")

    def getContent(self) -> dict:
        """Returns the full content as a dict
        :return: dict, content of property file
        """
        return self.content

    def setProperty(self, key: str, val: any):
        """Used to set properties to create file
        :param key: str, key
        :param val:  str, value for key
        :return:
        """
        self.content[key] = str(val)

    def clone(self) -> 'Properties':
        """Used to clone the <Properties> object
        :return: copy of self
        """
        return copy.deepcopy(self)

    def clear(self):
        """Clears the content stored and the path of the file"""
        self.path = ''
        self.content = {}

    def getKeySet(self) -> KeysView:
        """
        :return: Set of Keys of the content
        """
        return self.content.keys()

    def getValuesSet(self) -> ValuesView:
        """
        :return: Set of Values of the content
        """
        return self.content.values()

    def removeProperty(self, key: str) -> str:
        """Used to remove a property
        :param key: key to be removed
        :return: the value of the removed key
        """
        return self.content.pop(key)

    def containsProperty(self, key: str) -> bool:
        """Used to test if the property file contains a certain key
        :param key: the key to test
        :return: boolean, True if contains the key
        """
        return self.content.__contains__(key)

    def out(self, path: str = None, separator_char: str = '=', comment_char: str = '#', comments=None,
            comments_pos: str = 'top', is_absolute: bool = False):
        """Used to write a properties file
        :param path: string path as relative {used with a context manager}
        :param comment_char: comment_char (default:#)
        :param separator_char: separator_char (default:=)
        :param comments: A list of strings to be written in the file as comments
        :type comments: list[str]
        :param comments_pos: position of the comments, must be 'top' or 'bottom'
        """
        if path is None:
            if self.path != '':
                path = self.path
            else:
                return False
        else:
            if not is_absolute:
                # path = str(os.getcwd()) + (
                #     '\\' if not (path.startswith('\\') or path.startswith('/')) else '') + path
                path = str(os.getcwd()) + clean_path(path)
        path = clean_path(path)
        print(path)
        if comments is None:
            comments = []
        if not hasattr(comments, '__iter__'):
            raise AttributeError(
                f"Comments type is not valid: not iterable. Given={comments.__class__} | Should be a list")
        with open(path, 'w') as f:
            if comments and comments_pos == 'top':
                for comment in comments:
                    f.write(comment_char + comment + '\n')
            for key in self.content.keys():
                f.write(key + separator_char + self.content[key] + '\n')
            if comments and comments_pos == 'bottom':

                for comment in comments:
                    f.write(comment_char + comment + '\n')
            f.close()

    def close(self, comments=None):   ## TODO: Ambiguopus names and stuff, should destroy self?
        self.out(self.path, self.separator_char, self.comment_char, comments, comments_pos='top', is_absolute=True)
        self.clear()


class PropertiesHandler:
    properties_dict: dict[str, Properties]
    curr_prop: Optional[Properties]
    directories_dict: dict
    platformSeparators: str

    def __init__(self, properties_list=None):
        """Creates a 'PropertiesHandler' object used to manage and switch easily between Properties objects,
        useful for supporting languages for example
        :param properties_list: A list of Properties objects if you have one
        """
        if properties_list is None:
            properties_list = []
        self.properties_dict = {}
        self.directories_dict = {}
        self.curr_prop = None
        self.platformSeparators = getPlatformSeparators()
        if properties_list:
            for prop in properties_list:
                if not isinstance(prop, Properties):
                    print(f"[Init Error] Object {prop} is not an instance of {Properties.__class__}, skipping...")
                    continue
                self.addProperty(prop)

    def __repr__(self):
        return f"<{self.__class__.__name__} class, number_of_childs={len(self.properties_dict)}, " \
               f"selected_properties_class={self.curr_prop if self.curr_prop else 'None'}, " \
               f"list_of_childs={self.properties_dict}>"

    def passFiles(self, files_list: list, input_order: str = 's,c') -> 'PropertiesHandler':
        """Used when creating the object or to pass multiple files at once;
        Multiple lists are valid, you can do a list with only paths or replace some paths wit a lsit containing the path,
        followed by the separator character then followed by the comment character. (According to the input order,
        defaults to separator then comment, can be changed by setting 'input_order' to 'c,s'.
        :param files_list: a list of .properties files path. Can be used as [[path, separator_char, comment_char], [path, separator_char]]
        :param input_order: defines the input order in sublists, separator character first or second (default=s,c)
        :return: self so that it can be used to instantiate
        """
        for file in files_list:
            if isinstance(file, list):
                length = len(file)
                if length == 1:
                    self.addProperty(Properties(file[0]))
                elif length == 2:
                    if input_order == 'c,s':
                        self.addProperty(Properties(file[0], comment_char=file[1]))
                    else:
                        self.addProperty(Properties(file[0], separator_char=file[1]))
                elif length == 3:
                    if input_order == 'c,s':
                        self.addProperty(Properties(file[0], comment_char=file[1], separator_char=file[2]))
                    else:
                        self.addProperty(Properties(file[0], separator_char=file[1], comment_char=file[2]))
                else:
                    print(f'Invalid input file={file}')

            else:
                try:
                    self.addProperty(Properties(file))
                except FileNotFoundError:
                    print(f"File '{file}' not found")
                    continue
        return self

    def setDirectory(self, relative_path: str, is_absolute: bool = False):
        """Used to set a single directory as the container for all .properties files,
         removes every other Properties objects stored
        :param absolute_path: absolute path to directory
        """
        if not is_absolute:
            # absolute_path = str(os.getcwd()) + (
            #     '\\' if not (relative_path.startswith('\\') or relative_path.startswith('/')) else '') + relative_path
            absolute_path = str(os.getcwd()) + self.platformSeparators + clean_path(relative_path)
        else:
            absolute_path = relative_path
        absolute_path = clean_path(absolute_path)
        if not absolute_path.endswith(self.platformSeparators):
            absolute_path += self.platformSeparators
        self.directories_dict = {absolute_path: []}
        self.properties_dict = {}
        self.curr_prop = None
        for file in os.listdir(absolute_path):
            if file.endswith(".properties"):
                self.directories_dict[absolute_path].append(absolute_path + file)
                self.addProperty(Properties(os.path.join(absolute_path + file), is_absolute=True))

    def addDirectory(self, relative_path: str, is_absolute: bool = False):
        """Used to add a directory to the Properties directories list
        :param absolute_path: absolute path to directory
        """
        if not is_absolute:
            # absolute_path = str(os.getcwd()) + (
            #     '\\' if not (relative_path.startswith('\\') or relative_path.startswith('/')) else '') + relative_path
            absolute_path = str(os.getcwd()) + self.platformSeparators + clean_path(relative_path)
        else:
            absolute_path = relative_path
        absolute_path = clean_path(absolute_path)
        if not absolute_path.endswith(self.platformSeparators):
            absolute_path += self.platformSeparators
        self.directories_dict[absolute_path] = []
        for file in os.listdir(absolute_path):
            if file.endswith(".properties"):
                self.directories_dict[absolute_path].append(absolute_path + file)
                self.addProperty(Properties(os.path.join(absolute_path + file), is_absolute=True))

    def removeDirectories(self):
        """Removes every directory added to the Directories list
        Keeps externally added files"""
        print(f'{list(self.directories_dict.values())=}')
        for absolute_path in copy.deepcopy(list(self.directories_dict.keys())):
            self.removeDirectory(absolute_path, is_absolute=True)

    def removeDirectory(self, relative_path: str, is_absolute: bool = False):
        """Removes a directory and it's properties objects from the directories list
        :param absolute_path: absolute path to the directory
        """
        if not is_absolute:
            # absolute_path = str(os.getcwd()) + (
            #     '\\' if not (relative_path.startswith('\\') or relative_path.startswith('/')) else '') + relative_path
            absolute_path = str(os.getcwd()) + self.platformSeparators + clean_path(relative_path)
        else:
            absolute_path = relative_path
        absolute_path = clean_path(absolute_path)
        if not absolute_path.endswith(self.platformSeparators):
            absolute_path += self.platformSeparators
        if absolute_path not in self.directories_dict.keys():
            raise AttributeError(f"Directory '{absolute_path}' isn't registered.")
        for prop_path in self.directories_dict[absolute_path]:
            prop = self._getPropertyByPath(prop_path)
            self.properties_dict.pop(list(self.properties_dict.keys())
                                     [list(self.properties_dict.values()).index(prop)])
        self.directories_dict.pop(absolute_path)

    def updateDirectories(self):
        """Reloads every Properties objects contained in a stored directory
        and adds new files that were created after previous loading"""
        for relative_path in self.directories_dict.keys():
            for file in os.listdir(relative_path):
                if file.endswith(".properties"):
                    fileName = relative_path + file
                    if fileName not in self.directories_dict[relative_path]:
                        self.addProperty(Properties(os.path.join(relative_path + file), is_absolute=True))
                        self.directories_dict[relative_path].append(relative_path + file)
                    else:
                        self._getPropertyByPath(fileName).reload()

    def reloadAll(self):
        """Reloads every Properties objects"""
        for prop in self.properties_dict.values():
            prop.reload()

    def _getPropertyByPath(self, path: str) -> Properties:
        """Used to get a Property object using it's absolute path
        :param path: str, absolute path to the property
        """
        for prop in self.properties_dict.values():
            if prop.getPath() == path:
                return prop

    def addProperty(self, prop: Properties, name: str = ''):
        """Adds a Properties object
        :param prop: Properties object
        :param name: name of the prop in the dict, will default to prop+a_number to fill the list
        """
        if not name:
            num = 1
            name = 'prop' + str(num)
            while self.properties_dict.__contains__(name):
                num += 1
                name = 'prop' + str(num)
        self.properties_dict[name] = prop
        if not self.curr_prop:
            self.curr_prop = prop

    def removeProperty(self, **kwargs) -> Properties:
        """Used to remove a Properties object, returns the removed Properties class
        :param kwargs: name or index of the object in the internal dict
        :return: the popped object
        """
        name = kwargs.get('name', False)
        index = kwargs.get('index', 'False')
        relative_path = kwargs.get('relative_path', False)
        absolute_path = kwargs.get('absolute_path', False)
        prop: Optional[Properties] = None
        if isinstance(name, str):
            if not self.properties_dict.__contains__(name):
                raise KeyError(f'Unknown key {name}')
            prop = self.properties_dict.get(name)
        elif isinstance(index, int):
            if len(self.properties_dict) <= index or index < -len(self.properties_dict):
                raise IndexError(
                    f"index '{index}' out of bounds: max={len(self.properties_dict) - 1}, min={-len(self.properties_dict)}")
            prop = self.properties_dict.get(list(self.properties_dict.keys())[index])
        elif isinstance(relative_path, str):
            # absolute_path = str(os.getcwd()) + (
            #     '\\' if not (relative_path.startswith('\\') or relative_path.startswith('/')) else '') + relative_path
            absolute_path = str(os.getcwd()) + self.platformSeparators + clean_path(relative_path)
            absolute_path = clean_path(absolute_path)
            prop = self._getPropertyByPath(absolute_path)
            # for prop in list(self.properties_dict.values()):
            #     if prop.getPath() == absolute_path:
            #         prop = self.properties_dict.get(
            #             list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])
            #         break
        elif isinstance(absolute_path, str):
            absolute_path = clean_path(absolute_path)
            prop = self._getPropertyByPath(absolute_path)
            # for prop in list(self.properties_dict.values()):
            #     if prop.getPath() == absolute_path:
            #         prop = self.properties_dict.get(
            #             list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])
            #         break

        if prop == self.curr_prop:
            curr_index = list(self.properties_dict.values()).index(prop)

            if curr_index == 0:
                self.switchUp()
            else:
                self.switchDown()

            # self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())
            #                                           [(
            #         curr_index - 1 if curr_index == len(self.properties_dict) else curr_index)])
        return self.properties_dict.pop(list(self.properties_dict.keys())
                                        [list(self.properties_dict.values()).index(prop)])

    def changeProperty(self, **kwargs):
        """Used to change between Properties objects
        :param kwargs: name or index of the object in the internal dict
        """
        name = kwargs.get('name', False)
        index = kwargs.get('index', 'False')
        relative_path = kwargs.get('relative_path', False)
        absolute_path = kwargs.get('absolute_path', False)
        if name:
            if not self.properties_dict.__contains__(name):
                raise KeyError(f'Unknown key {name}')
            self.curr_prop = self.properties_dict.get(str(name), None)
        elif isinstance(index, int):
            if len(self.properties_dict) <= index or index < -len(self.properties_dict):
                raise IndexError(
                    f"index '{index}' out of bounds: max={len(self.properties_dict) - 1}, min={-len(self.properties_dict)}")
            self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())[index])
        elif isinstance(relative_path, str):
            # absolute_path = str(os.getcwd()) + (
            #     '\\' if not (relative_path.startswith('\\') or relative_path.startswith('/')) else '') + relative_path
            absolute_path = str(os.getcwd()) + self.platformSeparators + clean_path(relative_path)
            absolute_path = clean_path(absolute_path)
            for prop in list(self.properties_dict.values()):
                if prop.getPath() == absolute_path:
                    self.curr_prop = self.properties_dict.get(
                        list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])
                    break
        elif isinstance(absolute_path, str):
            absolute_path = clean_path(absolute_path)
            for prop in list(self.properties_dict.values()):
                if prop.getPath() == absolute_path:
                    self.curr_prop = self.properties_dict.get(
                        list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])
                    break

    def getProperty(self, **kwargs):
        """Used to get a Properties object
        :param kwargs: name or index of the object in the internal dict
        """
        name = kwargs.get('name', False)
        index = kwargs.get('index', 'False')
        relative_path = kwargs.get('relative_path', False)
        absolute_path = kwargs.get('absolute_path', False)
        if name:
            if not self.properties_dict.__contains__(name):
                raise KeyError(f'Unknown key {name}')
            return self.properties_dict.get(name)
        elif isinstance(index, int):
            if len(self.properties_dict) <= index or index < -len(self.properties_dict):
                raise IndexError(
                    f"index '{index}' out of bounds: max={len(self.properties_dict) - 1}, min={-len(self.properties_dict)}")
            return self.properties_dict.get(list(self.properties_dict.keys())[index])
        elif isinstance(relative_path, str):
            # absolute_path = str(os.getcwd()) + (
            #     '\\' if not (relative_path.startswith('\\') or relative_path.startswith('/')) else '') + relative_path
            # TODO: add self.systemSeparator and stuff
            absolute_path = str(os.getcwd()) + self.platformSeparators + clean_path(relative_path)
            absolute_path = clean_path(absolute_path)
            for prop in list(self.properties_dict.values()):
                if prop.getPath() == absolute_path:
                    return self.properties_dict.get(
                        list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])
        elif isinstance(absolute_path, str):
            absolute_path = clean_path(absolute_path)
            for prop in list(self.properties_dict.values()):
                if prop.getPath() == absolute_path:
                    return self.properties_dict.get(
                        list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])

    def switchUp(self):
        """Switches to the next Properties object in the internal dict (or to the first one if the last is passed)"""
        curr_pos = list(self.properties_dict.values()).index(self.curr_prop)
        next_pos = curr_pos + 1 if curr_pos + 1 < len(self.properties_dict) else 0
        self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())[next_pos])

    def switchDown(self):
        """Switches to the previous Properties object in the internal dict (or to the last one if the first is passed)"""
        curr_pos = list(self.properties_dict.values()).index(self.curr_prop)
        next_pos = len(self.properties_dict) - 1 if curr_pos - 1 < 0 else curr_pos - 1
        self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())[next_pos])

    def getProperties(self) -> ValuesView:
        """Used to get the values (Properties objects) of the internal dict
        :return: ValuesView of the internal dict
        """
        return self.properties_dict.values()

    def getContent(self) -> dict:
        """Used to get the internal dict
        :return: The internal dict
        """
        return self.properties_dict

    def getNames(self) -> KeysView:
        """Used to get the keys (Properties objects name's in the dict) of the internal dict
        :return: KeysView of the internal dict
        """
        return self.properties_dict.keys()

    def get(self) -> Optional[Properties]:
        """Used to get the current Properties object
        :return: Current selected Properties object
        """
        return self.curr_prop

    def testFunc(self):
        import os
        return os.getcwd()

    def closeProp(self, **kwargs):
        """Used to close a Properties object (basically clear it), and keep it in memory
            :param kwargs: name or index of the object in the internal dict
            """
        name = kwargs.get('name', False)
        index = kwargs.get('index', 'False')
        relative_path = kwargs.get('relative_path', False)
        absolute_path = kwargs.get('absolute_path', False)
        prop: Optional[Properties] = None
        if isinstance(name, str):
            if not self.properties_dict.__contains__(name):
                raise KeyError(f'Unknown key {name}')
            prop = self.properties_dict.get(name)
        elif isinstance(index, int):
            if len(self.properties_dict) <= index or index < -len(self.properties_dict):
                raise IndexError(
                    f"index '{index}' out of bounds: max={len(self.properties_dict) - 1}, min={-len(self.properties_dict)}")
            prop = self.properties_dict.get(list(self.properties_dict.keys())[index])
        elif isinstance(relative_path, str):
            absolute_path = str(os.getcwd()) + (
                '\\' if not (relative_path.startswith('\\') or relative_path.startswith('/')) else '') + relative_path
            absolute_path = clean_path(absolute_path)
            for prop in list(self.properties_dict.values()):
                if prop.getPath() == absolute_path:
                    prop = self.properties_dict.get(
                        list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])
                    break
        elif isinstance(absolute_path, str):
            absolute_path = clean_path(absolute_path)
            for prop in list(self.properties_dict.values()):
                if prop.getPath() == absolute_path:
                    prop = self.properties_dict.get(
                        list(self.properties_dict.keys())[list(self.properties_dict.values()).index(prop)])
                    break

        if prop == self.curr_prop:
            curr_index = list(self.properties_dict.values()).index(prop)
            self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())
                                                      [(
                    curr_index - 1 if curr_index == len(self.properties_dict) else curr_index)])
        prop.close()

    def closeProps(self):
        for prop in self.properties_dict.values():
            prop.close()
