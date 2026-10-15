from setuptools import setup

setup(
	name='pybeamer',
	version='0.0.1',
	description='Python package for interacting with Codebeamer',
	author='Austin Heil',
	author_email='austinmh12@gmail.com',
	packages=['pybeamer', 'pybeamer.api_client', 'pybeamer.models'],
	requires=['requests', 'loguru'],
	install_requires=['requests', 'loguru'],
)