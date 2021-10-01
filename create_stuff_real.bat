python setup.py sdist bdist_wheel
python -m twine upload dist/*
pip install --upgrade PySimpleProperties
@echo off
set /P name="END (press Enter to continue)"