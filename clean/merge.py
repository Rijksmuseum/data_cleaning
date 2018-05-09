#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merge CSV

Merge CSV files into one Adlib file that can be imported.
"""

__author__ = "Chris Dijkshoorn"
__version__ = "0.0.1"
__license__ = "MIT"


import os
import csv
import codecs


def merge_dat():
    print('Started merge csv script')
    # file paths
    os.chdir('data')
    source_folder = 'split'
    merged_file = 'out/merged.dat'
    # get list of relvant files
    file_paths = list_file_paths(source_folder)
    # open (all?) files
    readers = open_files(file_paths)
    # create dat file
    file = codecs.open(merged_file, 'w', 'utf-8')
    file.write(u'\ufeff')
    # write each value of each object to new dat
    file.write('DAT')
    # close files
    file.close()
    close_readers = close_files(readers)


def open_files(paths):
    readers = []

    for path in paths:
        # extract tag from file name
        tag = 'stub'
        file = open(path)
        readers.append([tag, file])
    return readers


def close_files(readers):
    for reader in readers:
        file = reader[1]
        file.close()

def list_file_paths(source_folder):
    return ['split/TI.csv', 'split/VV.csv']

if __name__ == "__main__":
    merge_dat()