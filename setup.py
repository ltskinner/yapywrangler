from setuptools import setup

setup(name='yapywrangler',
      version='1.1',
      description='Tool for reqesting stock data from the Yahoo Finance API',
      url='https://github.com/ltskinner/yapywrangler',
      author='ltskinner',
      license='MIT',
      install_requires=['requests', 'datetime'],
      packages=['yapywrangler'],
      zip_safe=False)
