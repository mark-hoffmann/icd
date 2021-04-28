import setuptools

setuptools.setup(
    name="icd",
    version="0.1.3",
    url="https://github.com/mark-hoffmann/icd",

    author="Mark Hoffmann",
    author_email="markkhoffmann@gmail.com",

    description="Tools for working with icd codes and comorbidities",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['pandas'],
    package_data={'icd': ['comorbidity_mappings/*.json']},
    include_package_data=True,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
