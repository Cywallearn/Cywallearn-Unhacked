#!/usr/bin/env python3
"""
Cywallearn Unhacked - Setup Script
"""

from setuptools import setup, find_packages

setup(
    name="cywallearn-unhacked",
    version="1.0.0",
    description="World-class password generator with personal touch - Unhackable by Design",
    long_description=open("README.md", encoding="utf-8").read() if __import__('os').path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Cywallearn",
    url="https://github.com/cywallearn/cywallearn-unhacked",
    packages=find_packages(),
    py_modules=["cywallearn"],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "cywallearn=cywallearn:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
    ],
    keywords="password generator security termux privacy cryptography",
)
