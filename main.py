# Python 2.7 for compatibility with EXIFRead. Sigh...
# ctrl - alt - n for running
# Start with virtualenv next time
# Don't use it as offload tool. But for folder sort only.

import exifread  # External Library
import os
import shutil
import re
import time
import glob
import collections  # for ordered dictionary
import datetime
from itertools import groupby
from bs4 import BeautifulSoup


def return_star_rating(filepath):
     # Extract the XMP data from the Canon RAW CR2 file and return the star rating.
     # Todo: Close the file so it doesn't hog up memory
    with open(filepath, "rb") as file:
        img = file.read()
    imgAsString = str(img)
    xmp_start = imgAsString.find('<x:xmpmeta')
    xmp_end = imgAsString.find('</x:xmpmeta')
    if xmp_start != xmp_end:
        xmpString = imgAsString[xmp_start:xmp_end+12]

    xmpAsXML = BeautifulSoup(xmpString, features="html")
    star_rating = int(xmpAsXML.find('xmp:rating').text)

    return (star_rating)


def move_photos_to_folders(cr2_category):
    # iterate over the CR2 items and create the right file paths
    for item, key in cr2_category.iteritems():
        if not os.path.exists(input_folder + "/" + str(key)):
            os.makedirs(input_folder + "/" + str(key))

        # Move the CR2 items
        file_name = re.search("\/([^\/]+)$", item)
        shutil.move(input_folder + "/" + file_name.group(1), output_folder + "/" +
                    str(key) + "/" + file_name.group(1))


def folder_to_filelist(folder_path):
    print "Scanning: " + str(folder_path)
    # Scan folder for CR2 files and return full file filepath.
    file_list = []
    # Only add CR2 files to the list
    for name in sorted(glob.iglob(folder_path + '/*.CR2')):
        file_list.append(name)
        print(name)
    # Sort the file list by number
    return file_list


def process_folder(folder):
    # Get a list with all the CR2 files in the folder we are processing
    file_list = folder_to_filelist(folder)

    # Extract the photorating out of the CR2 file into a sorted dictionary
    photo_rating = collections.OrderedDict()

    for file in file_list:
        photo_rating[file] = return_star_rating(file)
        print str(file) + " - Photo Rating: " + \
            str(return_star_rating(file))

    photoRatingDict = collections.OrderedDict()

    move_photos_to_folders(photoRatingDict)


def main():
    print "____________ \n \n Canon Star Sorter V.01"

    global input_folder
    global output_folder

    #input_folder = raw_input("\n Drag in your input folder and press enter: ")
    input_folder = "/Users/Kevin/Downloads/Jack Script/Day 2 copsdfy/0/"

    # output_folder = input("\n Drag in your output folder and press enter: ")
    #input_folder = input_folder.replace("\\", "") + "/"
    print input_folder
    output_folder = input_folder

    # Replace with function to scan for folders and generate list of folders to process.
    # Double check the syntax here with dashes at the end, see how the file path comes out of the folder scan lanter

    folder_list = [input_folder]
    # return folder list, return only folders with footage inside them. Otherwise traverse deeper.
    # only folders to be actually processed.

    # Scan folder for CR2 files and assign them a timelapse number.
    for folder in folder_list:
        # This returns a dictionary of files
        process_folder(folder)

        # Print out the results and sleep. later add a function to move them.  Set color labels?


# Run Main thread
main()
