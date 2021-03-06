#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merge CSV

Merge CSV files into one Adlib file that can be imported.
"""

__author__ = "Chris Dijkshoorn"
__version__ = "0.0.2"
__license__ = "MIT"


import os
import glob
import csv
import codecs
import datetime
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='merge.log',
    level=logging.INFO
)

def merge_dat():
    logging.info('Started merge csv script')
    # file paths
    os.chdir('data')
    source_folder = 'merge'
    merged_file = 'out/merge-' + datetime.datetime.now().strftime("%Y%m%d") + '.dat'
    # get list of relvant files
    file_paths = list_file_paths(source_folder)
    # create dictionary for data
    data = csv_to_dict(file_paths)
    # write dat file
    write_dict_to_dat(data, merged_file)
    logging.info('Finished merge script')


def list_file_paths(source_folder):
    logging.info('Listing csv files in folder ' + source_folder)
    csv_files = []

    for file in glob.glob(source_folder + "/*.csv"):
        csv_files.append(file)
    return csv_files


def csv_to_dict(paths):
    logging.info('Loading csv files into dictionary')
    dict = {}

    for path in paths:
        file = codecs.open(path, 'r', 'utf-8')
        # sniff out delimiter and reset position
        dialect = csv.Sniffer().sniff(file.readline())
        file.seek(0)
        csv_reader = csv.reader(file, dialect)
        # extract tag from first row
        tag = next(csv_reader)[1]

        for row in csv_reader:
            object_number = row[0]
            value = row[1]

            if not object_number in dict:
                # add new object dict with value and object number
                dict[object_number] = {tag: [value], "IN": [object_number]}
            else:
                object_dict = dict[object_number]
                if not tag in object_dict:
                    # add new tag list with value
                    object_dict[tag] = [value]
                else:
                    # append value to existing list
                    object_dict[tag].append(value)
        file.close()
    return dict


def write_dict_to_dat(dict, file):
    logging.info('Writing dictionary to ' + file)
    file = codecs.open(file, 'w', 'utf-8')
    object_numbers = sorted(dict.keys())

    # write each value of each object
    for object_number in object_numbers:
        object_dict = dict[object_number]
        tags = sorted(object_dict.keys())

        for tag in tags:
            values = object_dict[tag]
            for value in values:
                file.write(tag)
                if not value == "":
                    file.write(" " + value)
                file.write("\r\n")
        # write sepperator
        file.write("**\r\n")
    file.close()


if __name__ == "__main__":
    merge_dat()
