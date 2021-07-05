from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.3'
DESCRIPTION = 'A simple adaptation of java properties'
LONG_DESCRIPTION = 'A simple adaptation of java properties'

# Setting up
setup(
    name="PySimpleProperties",
    version=VERSION,
    author="JariBou (Tomé Bourdié)",
    author_email="<bourdietome@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url='https://github.com/JariBou/PySimpleProperties',
    install_requires=[],
    keywords=['python', 'properties'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)