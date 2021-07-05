python setup.py sdist bdist_wheel
python -m twine upload --repository testpypi dist/*
pip install --upgrade -i https://test.pypi.org/simple/ PySimpleProperties