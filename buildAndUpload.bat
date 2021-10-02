python setup.py sdist
twine upload dist/*
pip install --upgrade PySimpleProperties
@echo off
set /P name="END (press Enter to continue)"