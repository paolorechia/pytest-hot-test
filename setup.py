#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-hot-test",
    version="0.1.1",
    author="Paolo Rechia",
    author_email="paolorechia@gmail.com",
    maintainer="Paolo Rechia",
    maintainer_email="paolorechia@gmail.com",
    license="MIT",
    url="https://github.com/paolorechia/pytest-hot-test",
    description="A plugin that tracks test changes ",
    long_description=read("README.rst"),
    py_modules=[
        "pytest_hot_test",
        "hot_test_plugin.dependency_tracker",
        "hot_test_plugin.file_hash_manager",
        "hot_test_plugin.session_manager",
        "hot_test_plugin.settings",
        "hot_test_plugin.message_handler",
        "hot_test_plugin.errors",
    ],
    python_requires=">=3.7",
    install_requires=["pytest>=3.5.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "hot-test = pytest_hot_test",
        ],
    },
)
