# Python 2.7 for compatibility with EXIFRead. Sigh...

import exifread  # External Library
import os
import shutil
import re
import time
import glob
import collections  # for ordered dictionary
import datetime
from itertools import groupby


def return_date_from_raw(filepath):
    # Extract the EXIF information from a Canon RAW CR2 file and return a date.
    f = open(filepath, 'rb')
    # , stop_tag='DateTimeOriginal')
    data = exifread.process_file(f, details=False)
    f.close()
    date_str = data.values

    # Parse the RAW date string into a date time object for calculations
    parse_date = datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

    return (parse_date)


def move_to_timelapse_folder(cr2_category):
    # iterate over the CR2 items and create the right file paths
    for item, key in cr2_category.iteritems():
        if not os.path.exists(input_folder + "/" + str(key)):
            os.makedirs(input_folder + "/" + str(key))

        # Move the CR2 items
        file_name = re.search("\/([^\/]+)$", item)
        print file_name
        # shutil.copy2(item, output_folder + str(key) + "/" + file_name.group(1))
        shutil.move(input_folder + "/" + file_name.group(1), output_folder + "/" +
                    str(key) + "/" + file_name.group(1))


def folder_to_file_list(folder_path):
    print "Scanning: " + str(folder_path)
    # Scan folder for CR2 files and return full file filepath.
    file_list = []
    # Only add CR2 files to the list
    for name in sorted(glob.iglob(folder_path + '/*.CR2')):
        file_list.append(name)
        print(name)
    # Sort the file list by number
    return file_list


def cat_algo(folder):
    # Get a list with all the CR2 files in the folder we are processing
    file_list = folder_to_file_list(folder)

    # Extract the timestamp out of the CR2 file into a sorted dictionary
    cr2_timestamp = collections.OrderedDict()

    for file in file_list:
        cr2_timestamp[file] = return_date_from_raw(file)
        print str(file) + " - METADATA TIMESTAMP: " + \
            str(return_date_from_raw(file))

    cr2_category = collections.OrderedDict()
    item_count = 1
    group_count = 0
    sequence_count = 0
    index = 0
    photo_difference_with_previous = collections.OrderedDict()

    # Loop over the dictionary to compare the timestamps and create a new dictionary
    # with a suspected timelapse group number per shot
    # get item and the next item out of the sorted dictionary
    for item, nextitem in zip(cr2_timestamp.items(), cr2_timestamp.items()[1::]):
        # if not the first CR2 file
        if item_count >= 2:
            # get the datestamp of the current and the next photo in the dict
            current_date_stamp = item[1]
            next_date_stamp = nextitem[1]

            # Algo that determines by time percentage difference to which timelaps group the photo belongs. Needs improvement
            delta_previous = current_date_stamp - previous_date_stamp
            delta_next = next_date_stamp - current_date_stamp
            previous_difference_score = 0

            if delta_previous > datetime.timedelta(minutes=5):
                # if difference_score < 20:
                print item[0] + " - hit - " + str(delta_previous)
                group_count += 1
                cr2_category[item[0]] = group_count
            else:
                cr2_category[item[0]] = group_count

            # Calculations done, make the current date stamp the previous datestamp for the next iteration
            previous_date_stamp = current_date_stamp

            # If time difference with previous over X make a dict with name:number, in the end everything which has the
            # same number 5+ times in a row can be assumed as a timelapse.
        else:
            # If it is the first date stamp, assign it the current one to be used in the next loop
            previous_date_stamp = item[1]

        # To help make sure this is not the first image in the sequence.
            item_count += 1

    print cr2_category

    move_to_timelapse_folder(cr2_category)


def main():
    print "____________ \n \n Sorter V.01"

    global input_folder
    global output_folder

    input_folder = raw_input("\n Drag in your input folder and press enter: ")
    # output_folder = input("\n Drag in your output folder and press enter: ")
    input_folder = input_folder.replace("\\", "") + "/"
    print input_folder
    output_folder = input_folder

    # Replace with function to scan for folders and generate list of folders to process.
    # Double check the syntax here with dashes at the end, see how the file path comes out of the folder scan lanter

    folder_list = [input_folder]
    # return folder list, return only folders with footage inside them. Otherwise traverse deeper.
    # only folders to be actually processed.

    # Scan folder for CR2 files and assign them a timelapse number.
    for folder in folder_list:
        # This returns a dictionary of Filenames with the Timelapse number attached to it
        cat_algo(folder)

        # Print out the results and sleep. later add a function to move them.  Set color labels?


# Run Main thread
main()
