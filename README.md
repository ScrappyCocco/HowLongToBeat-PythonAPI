# HowLongToBeat Python API

[![Python Test Released Published Version](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/actions/workflows/python-test-release.yml/badge.svg)](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/actions/workflows/python-test-release.yml)
[![CodeQL](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/actions/workflows/codeql-analysis.yml)

[![codecov](https://codecov.io/gh/ScrappyCocco/HowLongToBeat-PythonAPI/branch/master/graph/badge.svg)](https://codecov.io/gh/ScrappyCocco/HowLongToBeat-PythonAPI)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ScrappyCocco_HowLongToBeat-PythonAPI&metric=bugs)](https://sonarcloud.io/dashboard?id=ScrappyCocco_HowLongToBeat-PythonAPI)

A simple Python API to read data from howlongtobeat.com.

It is inspired by [ckatzorke - howlongtobeat](https://github.com/ckatzorke/howlongtobeat) JS API.

## Content

- [Usage](#usage)
- [Installation](#installation)
  - [Installing the package downloading the last release](#installing-the-package-downloading-the-last-release)
  - [Installing the package from the source code](#installing-the-package-from-the-source-code)
- [Usage in code](#usage-in-code)
  - [Start including it in your file](#start-including-it-in-your-file)
  - [Now call search()](#now-call-search)
  - [Alternative search (by ID)](#alternative-search-by-id)
  - [DLC search](#dlc-search)
  - [Results auto-filter](#results-auto-filter)
  - [Reading an entry](#reading-an-entry)
- [Issues, Questions & Discussions](#issues-questions--discussions)
- [Authors](#authors)
- [License](#license)

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
Every entry in the list (if not None in case of errors) is an object of type: [HowLongToBeatEntry](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/blob/master/howlongtobeatpy/howlongtobeatpy/HowLongToBeatEntry.py).

### Alternative search (by ID)

If you prefer, you can get a game by ID, this can be useful if you already have the game's howlongtobeat-id (the ID is the number in the URL, for example in [https://howlongtobeat.com/game/7231]([hello](https://howlongtobeat.com/game/7231)) the ID is 7231).

To avoid a new parser, the search by ID use a first request to get the game title, and then use the standard search with that title, filtering the results and returning the unique game with that ID.

Remember that it could be a bit slower, but you avoid searching the game in the array by similarity.

Here's the example:

```python
result = HowLongToBeat().search_from_id(123456)
```

or, if you prefer using async:

```python
result = await HowLongToBeat().async_search_from_id(123456)
```

This call will return an unique [HowLongToBeatEntry](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/blob/master/howlongtobeatpy/howlongtobeatpy/HowLongToBeatEntry.py) or None in case of errors.

### DLC search

An `enum` has been added to have a filter in the search:

```python
SearchModifiers.NONE # default
SearchModifiers.ISOLATE_DLC
SearchModifiers.HIDE_DLC
```

This optional parameter allow you to specify in the search if you want the default search (with DLCs), to HIDE DLCs and only show games, or to ISOLATE DLCs (show only DLCs).

### Results auto-filter

To ignore games with a very different name, the standard search automatically filter results with a game name that has a similarity with the given name > than `0.4`, not adding the others to the result list.
If you want all the results, or you want to change this value, you can put a parameter in the constructor:

```python
results = HowLongToBeat(0.0).search("Awesome Game")
```

putting `0.0` (or just `0`) will return all the found games, otherwise you can write another (`float`) number between 0...1 to set a new filter, such as `0.7`.

Also remember that by default the similarity check **is case-sensitive** between the name given and the name found, if you want to ignore the case you can use:

```python
results = HowLongToBeat(0.0).search("Awesome Game", similarity_case_sensitive=False)
```

**Remember** that, when searching by ID, the similarity value and the case-sensitive bool are **ignored**.

### Reading an entry

An entry is made of few values, you can check them [in the Entry class file](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/blob/master/howlongtobeatpy/howlongtobeatpy/HowLongToBeatEntry.py). It also include the full JSON of values (already converted to Python dict) received from HLTB.

## Issues, Questions & Discussions

If you found a bug report it as soon as you can creating an [issue](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/issues/new), the code may not be perfect.

If you need any new feature, or want to discuss the current implementation/features, consider opening a [discussion](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/discussions) or even propose a change with a [Pull Request](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI/pulls).

## Authors

* **ScrappyCocco** - Thank you for using my API

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
