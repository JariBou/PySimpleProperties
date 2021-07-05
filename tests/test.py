from PySimpleProperties.Properties import Properties, PropertiesHandler


ph = PropertiesHandler().passFiles([['Entity1.properties', '=', '#'], 'test.properties', 'Entity2.properties'])
print(ph.getContent())
# ph.changeProperty(name='prop2')
# print(ph.get())
# ph.removeProperty(index=-3)
# print(ph.get())
# print(ph.getContent())
# print(ph)

