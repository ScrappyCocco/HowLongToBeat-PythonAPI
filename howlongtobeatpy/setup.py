from setuptools import setup, find_packages

setup(name='howlongtobeatpy',
      version='0.1',
      packages=find_packages(exclude=['tests']),
      description='A Python API for How Long to Beat',
      url='https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI',
      author='ScrappyCocco',
      license='MIT',
      keywords='howlongtobeat gaming steam uplay origin time length how long to beat',
      install_requires=[
            'aiohttp',
            'requests',
            'aiounittest'
      ],
      zip_safe=False)
