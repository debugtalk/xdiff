# XDiff

A CLI tool to compare data structures, files, folders, http responses, etc.

## Install

```bash
$ python setup.py install
```

## Usage

```text
$ xdiff -h
usage: xdiff [-h] [--log-level LOG_LEVEL]
             [--compare-files COMPARE_FILES [COMPARE_FILES ...]]
             [--compare-folders COMPARE_FOLDERS [COMPARE_FOLDERS ...]]

A CLI tool to compare data structures, files, folders, http responses, etc.

optional arguments:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        Specify logging level, default is INFO.
  --compare-files COMPARE_FILES [COMPARE_FILES ...]
                        Specify origin file and new file to be compared.
  --compare-folders COMPARE_FOLDERS [COMPARE_FOLDERS ...]
                        Specify origin folder and new folder to be compared.
```

## Examples

Compare two files.

```text
$ xdiff --compare-files 20170410223650/200/slug111.json 20170410202558/200/slug111.json
```

Compare files in two folders.

```text
$ xdiff --compare-folders 20170410223650 20170410202558
```

Compare files in two folders, and ignore specified keys.

```text
$ xdiff --compare-folders 20170410223650 20170410202558 --ignore-keys 'overview, faq, cover, photo, uuid, photos'
```
