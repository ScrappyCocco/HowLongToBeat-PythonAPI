# HowLongToBeat Python API
[![Build Status](https://travis-ci.org/ScrappyCocco/HowLongToBeat-PythonAPI.svg?branch=master)](https://travis-ci.org/ScrappyCocco/HowLongToBeat-PythonAPI)
[![codecov](https://codecov.io/gh/ScrappyCocco/HowLongToBeat-PythonAPI/branch/master/graph/badge.svg)](https://codecov.io/gh/ScrappyCocco/HowLongToBeat-PythonAPI)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ScrappyCocco_HowLongToBeat-PythonAPI&metric=bugs)](https://sonarcloud.io/dashboard?id=ScrappyCocco_HowLongToBeat-PythonAPI)

A simple Python API to read data from howlongtobeat.com.

It is inspired by [ckatzorke - howlongtobeat](https://github.com/ckatzorke/howlongtobeat) JS API.

## Usage

## Installation

### Installing the package downloading the last release

```python
pip install howlongtobeatpy
```

### Installing the package from the source code

Download the repo, enter the folder with 'setup.py' and run the command

```python
pip install .
```

## Usage in code

### Start including it in your file

```python
from howlongtobeatpy import HowLongToBeat
```

### Now call search()

The API main functions are:

```python
results = HowLongToBeat().search("Awesome Game")
```

or, if you prefer using async:

```python
results = await HowLongToBeat().async_search("Awesome Game")
```

The return of that function is a **list** of possible games, or **None** in case you passed an invalid "game name" as parameter or if there was an error in the request.

If the list **is not None** you should choose the best entry checking the Similarity value with the original name, example:

```python
results_list = await HowLongToBeat().async_search("Awesome Game")
if results_list is not None and len(results_list) > 0:
    best_element = max(results_list, key=lambda element: element.similarity)
```

Once done, "best_element" will contain the best game found in the research.

### Alternative search (by id)

If you prefer, you can get a game by id, this can be useful if you already have the game's howlongtobeat-id.
Unluckily, is not worth to make a parser for the single-page game info, because is a user page that can change frequently and full of HTML.

To avoid a new parser, the search by id use a first request to get the game title, and then use the standard search, filtering the results and returning the unique game with that id.

Remember that it could be a bit slower, but you avoid searching the game in the array.

Here's the example:

```python
result = HowLongToBeat().search_from_id(123456)
```

or, if you prefer using async:

```python
result = await HowLongToBeat().async_search_from_id(123456)
```

This call will return an unique [HowLongToBeatEntry](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/blob/master/howlongtobeatpy/howlongtobeatpy/HowLongToBeatEntry.py) or None in case of errors.

### Reading an entry

An entry is made of few values, you can check them [in the Entry class file](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/blob/master/howlongtobeatpy/howlongtobeatpy/HowLongToBeatEntry.py)

## Found a bug?

Please report it as soon as you can creating an [issue](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/issues/new), the code may not be perfect.

## Authors

* **ScrappyCocco**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
