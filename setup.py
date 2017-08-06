#! /usr/bin/python3

try:
	from setuptools import setup
except ImportError:
	print("Missing package setuptools. Please install to continue\n(https://pypi.python.org/pypi/setuptools)")
	
DESCRIPTION = 'Command-line torrent search tool for Windows and Linux OS'
LONG_DESCRIPTION = 'Program to search and download torrents from existing torrent-hosting sites.'
VERSION = '1.0.1.20170807'

setup(
    name = "torrench",
    version = VERSION,
    author = "Rijul Gulati",
    author_email = "kryptxy@protonmail.com",
    description = (DESCRIPTION),
    license = "GPL",
    url = "https://github.com/kryptxy/torrench",
    packages=['torrench', 'torrench.tpb', 'torrench.linuxtracker'],
    install_requires=['beautifulsoup4','lxml','requests','tabulate','termcolor'],
    long_description=(LONG_DESCRIPTION),
    entry_points = {'console_scripts': ['torrench = torrench.__main__:main']},
    zip_safe = False,
    keywords = ['torrents', 'thepiratebay', 'linuxtracker'], 
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ],
)
