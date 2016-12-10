#!/usr/bin/env python3

from distutils.core import setup

setup(	name = 'animal-farm',
		version = '0.0.1a1',
		description = 'Animal Farm Distributed Computing',
		author = 'Sofus Rose',
		author_email = 'sofus@sofusrose.com',
		url = 'http://www.sofusrose.com/afarm',

		license ='Apache Software License Version 2.0',

		package_dir = {'': 'src'},

		packages = [
			'lib',
			'master',
			'soft_api'
		],

		platforms = [
			'debian'
		],

		classifiers = [
			'License :: OSI Approved :: Apache Software License'
		]
)
