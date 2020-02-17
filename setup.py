import setuptools

setuptools.setup(
    name='phagecommander',
    license='GPL-3',
    version='0.1dev',
    author='Matthew Lazeroff',
    author_email='lazeroff@unlv.nevada.edu',
    description='Utilties for analyzing Fasta DNA Sequences with GeneMark/Glimmer',
    url='https://github.com/mlazeroff/GeneQuery',
    packages=['phagecommander'],
    package_data={'phagecommander': ['species.txt', 'GuiWidgets/*', 'Utilities/*']},
    install_requires=['requests',
                      'bs4',
                      'openpyxl',
                      'pyqt5',
                      'biopython',
                      'ruamel.yaml'],
    entry_points={'gui_scripts': 'phagecom = phagecommander.phagecom:main'},
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GPL-3",
                 "Operating System :: Windows",
                 "Operating System :: MacOS X",
                 "Operating System :: Linux"],
    include_package_data=True,
)
