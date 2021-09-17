from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1.6'
DESCRIPTION = 'A simple adaptation of java properties'
LONG_DESCRIPTION = """A simple adaptation of java properties.
Includes a Properties objects manager to help in managing multiple objects, useful for example if you have multi language support.
GitHub repo: https://github.com/JariBou/PySimpleProperties
Feel free to contact me at my mail: bourdietome@gmail.com

-JariBou (Tomé Bourdié)"""

# Setting up
setup(
    name="PySimpleProperties",
    license='LICENSE',
    version=VERSION,
    author="JariBou (Tomé Bourdié)",
    author_email="<bourdietome@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url='https://github.com/JariBou/PySimpleProperties',
    install_requires=[],
    keywords=['python', 'properties', 'file manager'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        ]
    )
