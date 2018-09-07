import setuptools

setuptools.setup(
    name="icd",
    version="0.1.2",
    url="https://github.com/mark-hoffmann/icd",

    author="Mark Hoffmann",
    author_email="markkhoffmann@gmail.com",

    description="Tools for working with icd codes and comorbidities",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['pandas'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
