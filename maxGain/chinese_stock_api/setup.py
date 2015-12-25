#!/usr/bin/env python

NAME = 'chinesestockapi'
VERSION = '1.4'
DESCRIPTION = 'Python API to get Chinese stock price'
LONG_DESCRIPTION = """\
Library to get Chinese stock price

Supported Engines:
 - Hexun API
 - Sina Finance API
 - Yahoo Finance API

Usage:

 from cstock.request import Requests

 from cstock.hexun_engine import HexunEngine

 engine = HexunEngine()

 requester = Requester(engine)

 stock = requester.request('000626')

 print stock.as_dict()

Github Site: https://github.com/godsarmy/chinese-stock-api.
"""
AUTHOR = 'Walt Chen'
AUTHOR_EMAIL = 'godsarmycy@gmail.com'
URL = 'https://pypi.python.org/pypi/chinesestockapi'
PLATFORM = 'any'
LICENSE = 'Apache Software License'

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        packages=find_packages(exclude=["test"]),
        platforms=PLATFORM ,
        license=LICENSE,
        test_suite = 'nose.collector'
    )
