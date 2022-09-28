from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='howlongtobeatpy',
      version='1.0.2',
      packages=find_packages(exclude=['tests']),
      description='A Python API for How Long to Beat',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI',
      author='ScrappyCocco',
      license='MIT',
      keywords='howlongtobeat gaming steam uplay origin time length how long to beat',
      install_requires=[
          'aiohttp>=3.7.3',
          'requests>=2.25.1',
          'aiounittest>=1.4.0',
          'fake_useragent==0.1.11'
      ],
      zip_safe=False)
