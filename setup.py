from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='yapywrangler',
      version='1.2',
      description='Tool for reqesting stock data from the Yahoo Finance API',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ltskinner/yapywrangler',
      author='ltskinner',
      license='MIT',
      install_requires=['requests', 'datetime'],
      packages=['yapywrangler'],
      zip_safe=False)
