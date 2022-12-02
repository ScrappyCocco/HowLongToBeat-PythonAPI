from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='howlongtobeatpy',
      version='1.0.5',
      packages=find_packages(exclude=['tests']),
      description='A Python API for How Long to Beat',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI',
      author='ScrappyCocco',
      license='MIT',
      keywords='howlongtobeat gaming steam uplay origin time length how long to beat',
      install_requires=[
          'aiohttp>=3.8.3',
          'requests>=2.28.1',
          'aiounittest>=1.4.2',
          'fake_useragent>=1.1.0'
      ],
      zip_safe=False)
