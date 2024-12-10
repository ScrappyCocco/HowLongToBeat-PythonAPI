from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='howlongtobeatpy',
      version='1.0.14',
      packages=find_packages(exclude=['tests']),
      description='A Python API for How Long to Beat',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI',
      author='ScrappyCocco',
      license='MIT',
      keywords='howlongtobeat gaming steam uplay origin time length how long to beat',
      install_requires=[
          'aiohttp>=3.10.1',
          'requests>=2.32.3',
          'aiounittest>=1.4.2',
          'fake_useragent>=1.5.1',
          'beautifulsoup4>=4.12.3'
      ],
      zip_safe=False)
