#!/usr/bin/env python3

import os, codecs
from os import path
from setuptools import setup

pwd = path.abspath(path.dirname(__file__))
with codecs.open(path.join(pwd, 'README.md'), 'r', encoding='utf8') as input:
	long_description = input.read()

name='ClassyData'
user='eddo888'
version='1.4'

setup(
	name=name,
	version=version,
	license='MIT',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/%s/%s'%(user,name),
	download_url='https://github.com/%s/%s/archive/%s.tar.gz'%(user, name, version),
	author='David Edson',
	author_email='eddo888@tpg.com.au',
	packages=[
		'Classes',
		'Handlers',
	],
	install_requires=[
		'mysql-connector',
		'sqlalchemy',
                'jsonweb',
		'Baubles',
		'Perdy',
		'Argumental',
		'Spanners',
		'GoldenChild',
	],
	scripts=[
		'bin/TopHat.py',
	], 
)

