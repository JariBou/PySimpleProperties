from PySimpleProperties.Properties import Properties, PropertiesHandler

#.passFiles([['Entity1.properties', '=', '#'], 'test.properties', 'Entity2.properties'])
ph = PropertiesHandler()
print(ph.getContent())
# print(ph.get().getContent())


import os

dir_path = ''
for file in os.listdir("..\\tests\\tests2\\"):
    if file.endswith(".properties"):
        ph.addProperty(Properties(os.path.join(file)))

print(ph.getContent())

# ph.changeProperty(name='prop2')
# print(ph.get())
# ph.removeProperty(index=-3)
# print(ph.get())
# print(ph.getContent())
# print(ph)

