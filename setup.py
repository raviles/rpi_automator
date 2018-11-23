import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpi_automator",
    version="0.0.3",
    author="Ryan Aviles",
    author_email="ryan.aviles@gmail.com",
    description="Raspberry Pi automation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raviles/rpi_automator",
    packages=setuptools.find_packages(),
    zip_safe=False,
    scripts=[
        'bin/rpi_automator'
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Other OS"
    ],
)
