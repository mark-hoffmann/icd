# uploading to pip

#Need to remember to update the version number before running this
#or else you run into an error that the file already exists on pypi

python setup.py sdist bdist_wheel
twine upload dist/*

