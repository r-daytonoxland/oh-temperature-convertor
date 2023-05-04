#import setuptools
#
#with open("README.md", "r") as fh:
#    long_description = fh.read()
#
#setuptools.setup(
#    name="oh_einstein_temp_convert",                     # This is the name of the package
#    version="0.0.1",                        # The initial release version
#    author="Rowan Dayton-Oxland",                     # Full name of the author
#    description="Tool to convert temperatures OH*(6-2) between two sets of Einstein A coefficients.",
#    long_description=long_description,      # Long description read from the the readme file
#    long_description_content_type="text/markdown",
#    #packages=setuptools.find_packages(),    # List of all python modules to be installed
#    classifiers=[
#        "Programming Language :: Python :: 3",
#        "License :: OSI Approved :: MIT License",
#        "Operating System :: OS Independent",
#    ],                                      # Information to filter the project on PyPi website
#    python_requires='>=3.6',                # Minimum version requirement of the package
#    packages=['src'],
#    py_modules=["src.oh_einstein_temp_convert"],             # Name of the python package
#    package_data={'oh_einstein_temp_convert':['data/*.txt']},     # Directory of the source code of the package
#)


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("Requirements.txt", 'r') as fh:
	requirements = [s.strip() for s in fh.readlines()] 

setup(
    name="oh_einstein_temp_convert",
    version="0.0.5",
    author="Rowan Dayton-Oxland",
    description="Tool to convert temperatures OH*(6-2) between two sets of Einstein A coefficients.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements
)

