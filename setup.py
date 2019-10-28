import setuptools

setuptools.setup(
    name='genequery',
    license='GPL-3',
    version='0.1dev',
    author='Matthew Lazeroff',
    author_email='lazeroff@unlv.nevada.edu',
    description='Utilties for analyzing Fasta DNA Sequences with GeneMark/Glimmer',
    url='https://github.com/mlazeroff/GeneQuery',
    packages=['genequery'],
    package_data={'genequery': ['species.txt', 'prodigal.windows.exe', 'GuiWidgets/*', 'Utilities/*']},
    install_requires=['requests',
                      'bs4',
                      'openpyxl',
                      'pyqt5',
                      'biopython'],
    entry_points={'gui_scripts': 'genequery = genequery.gquery:main'},
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GPL-3",
                 "Operating System :: Windows"],
    include_package_data=True,
)
