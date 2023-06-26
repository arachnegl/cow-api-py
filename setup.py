from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("dev-requirements.txt") as f:
    dev_requirements = f.read().splitlines()

setup(
    name="cow",
    version="1.0.0",
    author="Your Name",
    description="A cow project",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
