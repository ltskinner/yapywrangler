from setuptools import setup

setup(name='yapywrangler',
      version='0.1',
      description='Collects historical finance data from Yahoo Finance',
      url='https://github.com/ltskinner/yapywrangler',
      author='ltskinner',
      license='MIT',
      install_requires=['requests', 'datetime'],
      packages=['yapywrangler'],
      zip_safe=False)
