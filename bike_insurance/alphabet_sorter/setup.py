# setup.py
from setuptools import setup, find_packages

setup(
    name="ascending-sort",  # Name of your library
    version="0.2",          # Version of your library
    packages=find_packages(),  # Automatically find packages in the directory
    description="A simple library to sort lists alphabetically in ascending order.",
    author="Prasanna",     # Replace with your name or organization
    author_email="x23278480@student.ncirl.ie",  # Replace with your email
    url="https://github.com/ppankajs/ascending-sort.git",  # Your project’s GitHub URL
    long_description=open('README.md').read(),  # Read the content of README.md for description
    long_description_content_type="text/markdown",  # Specify the format of your README
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your chosen license
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[],  # List any dependencies here (none for this example)
    python_requires=">=3.6",  # Minimum Python version required
)
