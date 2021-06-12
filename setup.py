import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygore',
    version='0.4.6',
    author="Go Reverse Engineering Tool Kit",
    description="Python bindings for the Go Reverse Engineering Tool Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goretk/pygore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Development Status :: 4 - Beta",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
    package_data={'': ['libgore.so', 'libgore.dll', 'libgore.dylib']},
    include_package_data=True,
)
