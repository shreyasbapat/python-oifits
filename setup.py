#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# https://packaging.python.org/guides/single-sourcing-package-version/
version = {}
with open(os.path.join("src", "oifits", "__init__.py")) as fp:
    exec(fp.read(), version)


# http://blog.ionelmc.ro/2014/05/25/python-packaging/
setup(
    name="oifits",
    version=version["__version__"],
    description="Python package for working with OIFITS files!",
    author="Shreyas Bapat",
    author_email="bapat.shreyas@gmail.com",
    url="https://python-oifits.shreyasb.com",
    download_url="https://github.com/shreyasbapat/python-oifits",
    license="MIT",
    keywords=["oifits", "fits", "radio-astronomy", "vlbi"],
    python_requires=">=3.6",
    install_requires=["numpy", "astropy"],
    extras_require={
        "dev": [
            "black ; python_version>='3.6'",
            "coverage",
            "tox",
            "isort",
            "pytest",
            "pytest-cov<2.6.0",
            "pycodestyle",
            "sphinx",
            "alabaster",
            "nbsphinx",
            "ipython>=5.0",
            "jupyter-client",
            "ipykernel",
        ]
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    long_description=open("README.rst", encoding="utf-8").read(),
    include_package_data=True,
    zip_safe=False,
)
