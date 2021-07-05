import copy
from collections import KeysView, ValuesView
from typing import Optional


class Properties:
    content: dict
    path: str
    prev_key: str
    comment_char: str
    separator_char: str

    def __init__(self, path: str = False, **kwargs):
        """
        :param path: string path as relative {used with a context manager}
        :param kwargs: comment_char (default:#) and separator_char (default:=)
        """
        self.content = {}
        self.path = ''
        self.prev_key = ''
        self.comment_char = kwargs.get('comment_char', '#')
        self.separator_char = kwargs.get('separator_char', '=')
        if path:
            self.load(path, self.comment_char, self.separator_char)

    def __repr__(self):
        return f"<{self.__class__}, loaded_file: '{self.path if self.path else 'None'}'>"

    def load(self, path: str, comment_char: str = '#', separator_char: str = '=') -> 'Properties':
        """ Loads Properties and stores them in a dict and returns the dict
        :param path: string path as relative {used with a context manager}
        :param comment_char: comment_char (default:#)
        :param separator_char: separator_char (default:=)
        :return: Dict of content
        """
        self.content = {}
        self.path = path
        self.prev_key = ''
        self.comment_char = comment_char
        self.separator_char = separator_char
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
        except FileNotFoundError as e:
            print(e)
        return self

    def reload(self):
        """Reloads the property file"""
        if not self.path:
            raise Exception('No path given, cannot reload properties')
        self.load(self.path, self.comment_char, self.separator_char)

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

    def out(self, path: str, comment_char: str = '#', separator_char: str = '=', comments=None, comments_pos: str = 'top'):
        """Used to write a properties file
        :param path: string path as relative {used with a context manager}
        :param comment_char: comment_char (default:#)
        :param separator_char: separator_char (default:=)
        :param comments: A list of strings to be written in the file as comments
        :type comments: list[str]
        :param comments_pos: position of the comments, must be 'top' or 'bottom'
        """
        if comments is None:
            comments = []
        if not hasattr(comments, '__iter__'):
            raise AttributeError(f"Comments type is not valid: not iterable. Given={comments.__class__} | Should be a list")
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


class PropertiesHandler:
    properties_dict: dict
    curr_prop: Optional[Properties]

    def __init__(self, properties_list=None):
        if properties_list is None:
            properties_list = []
        self.properties_dict = {}
        self.curr_prop = None
        if properties_list:
            for prop in properties_list:
                if not isinstance(prop, Properties):
                    print(f"object {prop} is not an instance of {Properties.__class__}, skipping...")
                    continue
                self.addProperty(prop)

    def addProperty(self, prop: Properties, name: str = ''):
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
        name = kwargs.get('name', False)
        index = kwargs.get('index', False)
        prop: Optional[Properties] = None
        if name:
            if not self.properties_dict.__contains__(name):
                raise KeyError(f'Unknown key {name}')
            prop = self.properties_dict.get(name)
        elif isinstance(index, int):
            if len(self.properties_dict) <= index or index < -len(self.properties_dict):
                raise IndexError(f"index '{index}' out of bounds: max={len(self.properties_dict) - 1}, min={-len(self.properties_dict)}")
            prop = self.properties_dict.get(list(self.properties_dict.keys())[index])

        if prop == self.curr_prop:
            curr_index = list(self.properties_dict.values()).index(prop)
            self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())
                                                      [(curr_index - 1 if curr_index == len(self.properties_dict) else curr_index)])
        return self.properties_dict.pop(list(self.properties_dict.keys())
                                        [list(self.properties_dict.values()).index(prop)])

    def changeProperty(self, **kwargs):
        name = kwargs.get('name', False)
        index = kwargs.get('index', False)
        if name:
            if not self.properties_dict.__contains__(name):
                raise KeyError(f'Unknown key {name}')
            self.curr_prop = self.properties_dict.get(name, None)
        elif isinstance(index, int):
            if len(self.properties_dict) <= index or index < -len(self.properties_dict):
                raise IndexError(f"index '{index}' out of bounds: max={len(self.properties_dict)-1}, min={-len(self.properties_dict)}")
            self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())[index])

    def getProperty(self, **kwargs):
        name = kwargs.get('name', False)
        index = kwargs.get('index', False)
        if name:
            if not self.properties_dict.__contains__(name):
                raise KeyError(f'Unknown key {name}')
            return self.properties_dict.get(name)
        elif isinstance(index, int):
            if len(self.properties_dict) <= index or index < -len(self.properties_dict):
                raise IndexError(f"index '{index}' out of bounds: max={len(self.properties_dict) - 1}, min={-len(self.properties_dict)}")
            return self.properties_dict.get(list(self.properties_dict.keys())[index])

    def switchUp(self):
        curr_pos = list(self.properties_dict.values()).index(self.curr_prop)
        next_pos = curr_pos + 1 if curr_pos + 1 < len(self.properties_dict) else 0
        self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())[next_pos])

    def switchDown(self):
        curr_pos = list(self.properties_dict.values()).index(self.curr_prop)
        next_pos = len(self.properties_dict) - 1 if curr_pos - 1 < 0 else curr_pos - 1
        self.curr_prop = self.properties_dict.get(list(self.properties_dict.keys())[next_pos])

    def getProperties(self) -> ValuesView:
        return self.properties_dict.values()

    def getContent(self) -> dict:
        return self.properties_dict

    def getNames(self) -> KeysView:
        return self.properties_dict.keys()

    def get(self) -> Optional[Properties]:
        return self.curr_prop
