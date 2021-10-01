from PySimpleProperties.Properties import Properties, PropertiesHandler, clean_path

#.passFiles([['Entity1.properties', '=', '#'], 'test.properties', 'Entity2.properties'])
ph = PropertiesHandler()
print(ph.getContent())
# print(ph.get().getContent())


import os
import platform

# print(platform.system())
# print('/1/2/3'.split('/'))

# dir_path = ''
# for file in os.listdir("../tests/tests2/"):
#     if file.endswith(".properties"):
#         # print(clean_path(str(os.getcwd()) + '/../tests/tests2/'+file))
#         ph.addProperty(Properties('../tests/tests2/'+file, is_absolute=False))
#//home/jari/PycharmProjects/PySimpleProperties/teststests/tests2/Entity1.properties
#//home/jari/PycharmProjects/PySimpleProperties/teststests/tests2'
ph.addDirectory('../tests//')
ph.addDirectory('..///tests/tests2/')
ph.addDirectory('..///tests/tests2/')
print(f"{ph.directories_name_dict=}")
print()
ph.updateDirectory(name='tests')
print(ph.directories_name_dict)
print(ph.getContent())
ph.removeProperty(relative_path="..//tests/tests2//Entity1.properties")

# ph.changeProperty(name='prop2')
# print(ph.get())
# ph.removeProperty(index=-3)
# print(ph.get())
# print(ph.getContent())
# print(ph)

