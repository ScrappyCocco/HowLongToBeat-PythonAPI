from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='howlongtobeatpy',
      version='1.0.18',
      packages=find_packages(exclude=['tests']),
      description='A Python API for How Long to Beat',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI',
      author='ScrappyCocco',
      license='MIT',
      keywords='howlongtobeat gaming steam uplay origin time length how long to beat',
      install_requires=[
          'aiohttp~=3.12',
          'requests~=2.32',
          'aiounittest~=1.5',
          'fake_useragent~=2.2',
          'beautifulsoup4~=4.13'
      ],
      zip_safe=False)
