# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
#
# SPDX-License-Identifier: MIT

import os
import io
from setuptools import setup


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with io.open(path, encoding="utf8") as f:
        return f.read()


setup(
    name="pytest-threadleak",
    version="0.5.0",
    author="Nir Soffer",
    author_email="nirsof@gmail.com",
    maintainer="Nir Soffer",
    maintainer_email="nirsof@gmail.com",
    license="MIT",
    url="https://github.com/nirs/pytest-threadleak",
    description="Detects thread leaks",
    long_description=read("README.rst"),
    py_modules=["pytest_threadleak"],
    install_requires=["pytest>=3.1.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "threadleak = pytest_threadleak",
        ],
    },
)
