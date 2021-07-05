from PySimpleProperties.Properties import Properties, PropertiesHandler


ph = PropertiesHandler([Properties("Entity1.properties"), Properties("test.properties"), Properties("Entity2.properties")])
print(ph.getContent())
ph.changeProperty(name='prop2')
print(ph.get())
ph.removeProperty(index=-3)
print(ph.get())
print(ph.getContent())
print(ph)

