#coding: utf-8
import os
import sys
import logging
import argparse
from .core import compare_files, compare_folder_files
from .helpers import color_logging

def main():
    """ parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(
        description='A CLI tool to compare data structures, files, folders, http responses, etc.')

    parser.add_argument(
        '--log-level', default='INFO',
        help="Specify logging level, default is INFO.")
    parser.add_argument(
        '--compare-files', nargs='+', help="Specify origin file and new file to be compared.")
    parser.add_argument(
        '--compare-folders', nargs='+',
        help="Specify origin folder and new folder to be compared.")

    args = parser.parse_args()
    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)
    main_compare(args)

def main_compare(args):
    files = args.compare_files
    folders = args.compare_folders

    if files and len(files) == 2:
        origin_file, new_file = files
        color_logging("Start to compare two files: {}, {}".format(origin_file, new_file))

        origin_file_suffix = os.path.splitext(origin_file)[1]
        new_file_suffix = os.path.splitext(new_file)[1]
        if origin_file_suffix != new_file_suffix:
            color_logging('Compared files should be the same format.', 'WARNING')
            sys.exit(1)

        difference = compare_files(origin_file, new_file, origin_file_suffix)
        if difference:
            color_logging("Difference exist: {}".format(difference))
        else:
            color_logging("No difference exist.")
    elif folders and len(folders) == 2:
        origin_folder, new_folder = folders
        color_logging("Start to compare two folders: {}, {}".format(origin_folder, new_folder))
        log_files = compare_folder_files(origin_folder, new_folder)
        if log_files:
            color_logging("Difference exist, view in log files: {}".format(log_files))
        else:
            color_logging("No difference exist.")
    else:
        color_logging('Run python main.py compare -h for usage help.', 'WARNING')
        sys.exit(1)
