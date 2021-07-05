import copy
from collections import KeysView, ValuesView


class Properties:
    content: dict
    path: str
    prev_key: str

    def __init__(self, path: str = False, **kwargs):
        self.content = {}
        self.prev_key = ''
        if path:
            self.load(path, kwargs.get('comment_char', '#'), kwargs.get('separator_char', '='))

    def __repr__(self):
        return f'{self.__class__.__name__} class, loaded_file: {self.path} '

    def load(self, path: str, comment_char: str = '#', separator_char: str = '='):
        self.content = {}
        self.path = path
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
        except FileNotFoundError as e:
            print(e)

    def getProperty(self, key: str) -> str:
        return self.content.get(key, 'Undefined')

    def getContent(self) -> dict:
        return self.content

    def setProperty(self, key: str, val: any):
        self.content[key] = str(val)

    def clone(self) -> 'Properties':
        return copy.deepcopy(self)

    def clear(self):
        self.path = ''
        self.content = {}

    def getKeySet(self) -> KeysView:
        return self.content.keys()

    def getValuesSet(self) -> ValuesView:
        return self.content.values()

    def remove(self, key: str) -> str:
        return self.content.pop(key)

    def containsProperty(self, key: str):
        return self.content.__contains__(key)

    def out(self, path: str, comment_char: str = '#', separator_char: str = '=', comments: list[str] = [], comments_pos: str = 'top'):
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
