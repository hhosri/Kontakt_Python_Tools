#A program that checks the availability / naming / dimensions of the required png files for NKS SDK 1.6
#copy the script to root of the png files folder, and run it

import os
from PIL import Image

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

cur_dir = os.path.dirname(os.path.abspath(__file__))
success_files = 0
REQUIRED_NUM_OF_PNGS = 11

required_files = {
    'VB_logo.png': [227, 47],
    'OSO_logo.png': [417, 65],
    'MST_logo.png': [240, 196],
    'VB_artwork.png': [96, 47],
    'MST_artwork.png': [134, 66],
    'VB_artwork@8x.png': [768, 376],
    'OSO_logo@2x.png': [834, 130],
    'VB_artwork@2x.png': [192, 94],
    'VB_cardview.png': [384, 188],
    'VB_cardview@2x.png': [768, 376],
    'MST_plugin.png': [190, 100]
}

def printer(msg, msg_type):
    if msg_type == 'good':
        color = GREEN
    elif msg_type == 'bad':
        color = RED
    else:
        color = RESET
    print(color + msg)

def  open_image_get_size(filename):
    img = Image.open(filename)
    width, height = img.size
    img.close()
    return(width, height)

def check_size(filename, expected_size, width, height):
    global success_files
    if (filename == 'MST_plugin.png'):
            if (width <= 190) and (height <= 100):
                printer(f"{filename} exists in the directory, and is no more than (190 x 100)", 'good')
                success_files += 1
            else:
                printer(f"{filename} has incorrect dimensions ({width} x {height}) --should be--> <= (190 x 100).", 'bad')
    else:
        if width == expected_size[0] and height == expected_size[1]:
            printer(f"{filename} has the correct dimensions ({width} x {height}).", 'good')
            success_files += 1
        else:
            printer(f"{filename} has incorrect dimensions ({width} x {height}) --should be--> ({expected_size[0]} x {expected_size[1]}).", 'bad')

def exit_status():
    global success_files
    if (success_files == 11):
        printer(f' *** SUCCESS *** {success_files} verified files', 'good')
    else:
        printer(f'*** WARNING *** {success_files} verified files out of: {REQUIRED_NUM_OF_PNGS} required files', 'bad')

def main():
    for filename, expected_size in required_files.items():
        if os.path.isfile(filename):
            width, height = open_image_get_size(filename)
            check_size(filename, expected_size, width, height)
        else:
            printer(f"{filename} does not exist in the directory.", 'bad')
    exit_status()

if __name__ == '__main__':
    main()