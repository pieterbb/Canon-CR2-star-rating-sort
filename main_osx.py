import os
import shutil
import re
import glob
# from itertools import groupby

#TODO: Make folder scanning recursive
#TODO: Package as EXE for Windows

def return_star_rating(filepath):
    # Extract the XMP data from the Canon RAW CR2 file and return the star rating.
    # Canon Stores star rating in additional XMP not EXIF
    with open(filepath, "rb") as file:
        for line in file.readlines():
            if re.search("<x:xmpmeta",  str(line), 0):
                star_rating_match = re.findall("<xmp:Rating>(\d)<\/xmp:Rating>", str(line))

                # Catch NoneTypes, make sure you always return an int
                if star_rating_match:
                    star_rating = int(star_rating_match[0])
                else:
                    star_rating = 0
                return (star_rating)


def process_folder(folder):
    file_list = []

    # Scan folder for CR2 Photos files and return full filepaths
    # Only add CR2 photo files to the list
    for name in sorted(glob.iglob(folder + '/*.CR2')):
        file_list.append(name)

    print (str(len(file_list)) + " CR2 files found in input folder...")

    # Loop over the photo files and check their ratings
    for file in file_list:
        photo_rating = return_star_rating(file)
        print (str(file) + " -  Rating: " + \
            str(photo_rating))
        
        # Check if photo has a rating 
        if photo_rating is 0:
            # Check if unrated folder already exists otherwise create it
            if not os.path.exists(input_folder + "/unrated"):
                os.makedirs(input_folder + "/unrated")

            #Get the filename from the filepath
            file_name = re.search("\/([^\/]+)$", file)
            shutil.move(file, input_folder + "/unrated/" + file_name[0])
                        
        # If the photo has a rating above 1 
        elif photo_rating >= 1: 

            # check if rated folder already exists, otherwise create it
            if not os.path.exists(input_folder + "/rated"):
                os.makedirs(input_folder + "/rated")
    
            # Move the photo file to the folder
            file_name = re.search("\/([^\/]+)$", file)
            shutil.move(file, input_folder + "/rated/" + file_name[0])

def main():

    print("""\
Canon CR2 RatingSort: Sort photo's in folder by rated and unrated V.01

    """)
    global input_folder
    #input_folder = "/Users/pieter/Downloads/input"
    input_folder = input("Drag in your input folder and press enter: ")
    process_folder(input_folder)

main()
