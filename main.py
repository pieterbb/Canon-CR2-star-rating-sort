import exifread  # External Library
import os
import shutil
import re
import glob
import collections  # for ordered dictionary
from itertools import groupby
from bs4 import BeautifulSoup


def return_star_rating(filepath):
     # Extract the XMP data from the Canon RAW CR2 file and return the star rating.
    with open(filepath, "rb") as file:
        img = file.read()
    imgAsString = str(img)
    xmp_start = imgAsString.find('<x:xmpmeta')
    xmp_end = imgAsString.find('</x:xmpmeta')
    if xmp_start != xmp_end:
        xmpString = imgAsString[xmp_start:xmp_end+12]

    xmpAsXML = BeautifulSoup(xmpString, features="lxml")
    star_rating = int(xmpAsXML.find('xmp:rating').text)

    return (star_rating)


def move_photos_to_folders(star_rating):
    # iterate over the photos and create the right file path
    for item, key in star_rating.iteritems():
        if not os.path.exists(input_folder + "/" + str(key)):
            os.makedirs(input_folder + "/" + str(key))

        # Move the photos
        file_name = re.search("\/([^\/]+)$", item)
        shutil.move(input_folder + "/" + file_name.group(1),
                    input_folder + "/" + str(key) + "/" + file_name.group(1))


def folder_to_filelist(folder_path):
    print "Scanning: " + str(folder_path)
    # Scan folder for CR2 Photos files and return full file filepath.
    file_list = []
    # Only add CR2 photo files to the list
    for name in sorted(glob.iglob(folder_path + '/*.CR2')):
        file_list.append(name)
    return file_list


def process_folder(folder):
    # Get a list with all the CR2 files in the folder we are processing
    file_list = folder_to_filelist(folder)

    # Datatype that remembers the order entries where added. Key:Value
    photo_rating = collections.OrderedDict()

    # Extract the photorating out of the CR2 file into a sorted dictionary for all files
    for file in file_list:
        photo_rating[file] = return_star_rating(file)
        print str(file) + " -  Rating: " + \
            str(photo_rating[file])
        os.system('clear')

    move_photos_to_folders(photo_rating)


def main():
    print "____________ \n \n RatingSort: Sort photo's by Star Rating and move to folder V.01"
    global input_folder

    # input_folder = raw_input("\n Drag in your input folder and press enter to start: ")
    input_folder = "/Users/Kevin/Downloads/Jack Script/Day 2 copsdfy/0/"
    process_folder(input_folder)


main()
