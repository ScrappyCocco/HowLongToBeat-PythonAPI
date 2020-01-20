from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='howlongtobeatpy',
      version='0.1.12',
      packages=find_packages(exclude=['tests']),
      description='A Python API for How Long to Beat',
      long_description=long_description,
      long_description_content_type="text/markdown",
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
