import shutil
import re
import glob
from pathlib import Path

# TODO: Find out a better way to drag in filepaths in Windows with spaces and weird characters
# TODO: Add flag for sort by rate/unrated or rating number
# TODO: Add support for multiple file formats


# Extract the XMP data from the Canon RAW CR2 file and return the star rating.
def return_star_rating(filepath):
    with open(filepath, "rb") as file:
        for line in file.readlines():
            if re.search("<x:xmpmeta",  str(line), 0):
                star_rating_match = re.findall(r"<xmp:Rating>(\d)<\/xmp:Rating>", str(line))

                if star_rating_match:
                    star_rating = int(star_rating_match[0])
                else:
                    star_rating = "?"
                return (star_rating)
                
def process_folder(folder):
    file_list = []

    # Scan input folder for CR2 photos recursively
    for name in sorted(input_folder.glob('**/*.CR2')):
        # check if photo is not already in a rated or unrated folder, if so, skip file
        if name.parts[-2] != "rated" and name.parts[-2] != "unrated":
            file_list.append(name)

    print (str(len(file_list)) + " CR2 files found in input folder...")

    # Loop over the photo files and check their ratings
    for file in file_list:
        photo_rating = return_star_rating(file)
        print (str(file) + " -  Rating: " + \
            str(photo_rating))
        
        # Check if photo has a rating 
        if photo_rating is 0:
            # check if rated folder already exists, otherwise create it
            if not Path.exists(file.parent / "unrated"):
                Path.mkdir(file.parent / "unrated")
            # Move the photo file to the folder
            shutil.move(str(file), str(file.parent / "unrated")) # Convert to string due to bug in Python
                        
        # If the photo has a rating above 1 
        elif photo_rating >= 1: 
            # check if rated folder already exists, otherwise create it
            if not Path.exists(file.parent / "rated"):
                Path.mkdir(file.parent / "rated")
            # Move the photo file to the folder
            shutil.move(str(file), str(file.parent / "rated")) # Convert to string due to bug in Python


def main():
    print("""\n
'########:::::'###::::'########:'####:'##::: ##::'######:::::: 
 ##.... ##:::'## ##:::... ##..::. ##:: ###:: ##:'##... ##::::: 
 ##:::: ##::'##:. ##::::: ##::::: ##:: ####: ##: ##:::..:::::: 
 ########::'##:::. ##:::: ##::::: ##:: ## ## ##: ##::'####:::: 
 ##.. ##::: #########:::: ##::::: ##:: ##. ####: ##::: ##::::: 
 ##::. ##:: ##.... ##:::: ##::::: ##:: ##:. ###: ##::: ##::::: 
 ##:::. ##: ##:::: ##:::: ##::::'####: ##::. ##:. ######:::::: 
..:::::..::..:::::..:::::..:::::....::..::::..:::......::::::: 
:'######:::'#######::'########::'########:'########:'########::
'##... ##:'##.... ##: ##.... ##:... ##..:: ##.....:: ##.... ##:
 ##:::..:: ##:::: ##: ##:::: ##:::: ##:::: ##::::::: ##:::: ##:
. ######:: ##:::: ##: ########::::: ##:::: ######::: ########::
:..... ##: ##:::: ##: ##.. ##:::::: ##:::: ##...:::: ##.. ##:::
'##::: ##: ##:::: ##: ##::. ##::::: ##:::: ##::::::: ##::. ##::
. ######::. #######:: ##:::. ##:::: ##:::: ########: ##:::. ##:
:......::::.......:::..:::::..:::::..:::::........::..:::::..::
\nSort Canon CR2 photo's by moving them in \nstar rated or unrated folders. (V1.02 - 2020) \nContact: hello@piet.re
""")
    global input_folder
    input_folder = Path(input("Paste the path to your input folder and press enter: "))

    if input_folder.is_dir():
        process_folder(input_folder)
        input("Done! Press enter to exit...")
    else:
        input("Input directory does not exist...")

main()